"""Offline Camoufox smoke and same-host persistence probes.

This is Phase 1 research code, not a production launcher. It intentionally
uses only synthetic pages and disposable profile data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROBE_SCHEMA_VERSION = "0.1.0"
SYNTHETIC_ORIGIN = "https://probe.invalid/"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalize_observation(raw: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic, JSON-safe observation without raw canvas data."""
    normalized = dict(raw)
    canvas = normalized.pop("canvasDataUrl", None)
    if canvas is not None:
        normalized["canvasSha256"] = sha256_text(canvas)
    extensions = normalized.get("webglExtensions")
    if isinstance(extensions, list):
        normalized["webglExtensions"] = sorted(str(item) for item in extensions)
    return normalized


def _collect_page(page: Any) -> dict[str, Any]:
    page.set_content("<!doctype html><html><body><canvas id='c' width='64' height='32'></canvas></body></html>")
    raw = page.evaluate(
        """
        async () => {
          const canvas = document.getElementById('c');
          const ctx = canvas.getContext('2d');
          ctx.font = '14px Arial';
          ctx.fillStyle = '#123456';
          ctx.fillText('multi-profiles-probe', 2, 18);
          const gl = document.createElement('canvas').getContext('webgl');
          const dbg = gl && gl.getExtension('WEBGL_debug_renderer_info');
          const worker = await new Promise((resolve) => {
            const source = `onmessage = () => postMessage({
              userAgent: navigator.userAgent,
              platform: navigator.platform,
              language: navigator.language,
              hardwareConcurrency: navigator.hardwareConcurrency
            })`;
            const url = URL.createObjectURL(new Blob([source], {type: 'text/javascript'}));
            const w = new Worker(url);
            w.onmessage = (event) => { resolve(event.data); w.terminate(); URL.revokeObjectURL(url); };
            w.onerror = (event) => resolve({error: String(event.message || 'worker-error')});
            w.postMessage(null);
          });
          return {
            userAgent: navigator.userAgent,
            platform: navigator.platform,
            language: navigator.language,
            languages: Array.from(navigator.languages || []),
            hardwareConcurrency: navigator.hardwareConcurrency,
            maxTouchPoints: navigator.maxTouchPoints,
            webdriver: navigator.webdriver,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            screen: {
              width: screen.width,
              height: screen.height,
              availWidth: screen.availWidth,
              availHeight: screen.availHeight,
              colorDepth: screen.colorDepth,
              pixelDepth: screen.pixelDepth,
              devicePixelRatio
            },
            window: {
              innerWidth,
              innerHeight,
              outerWidth,
              outerHeight
            },
            canvasDataUrl: canvas.toDataURL(),
            webglVendor: gl && dbg ? gl.getParameter(dbg.UNMASKED_VENDOR_WEBGL) : null,
            webglRenderer: gl && dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : null,
            webglExtensions: gl ? (gl.getSupportedExtensions() || []) : [],
            worker
          };
        }
        """
    )
    return normalize_observation(raw)


def run_smoke() -> dict[str, Any]:
    from camoufox.sync_api import Camoufox

    started = utc_now()
    with Camoufox(headless=True, os="windows") as browser:
        observation = _collect_page(browser.new_page())
    return {
        "schemaVersion": PROBE_SCHEMA_VERSION,
        "kind": "offline-smoke",
        "startedAt": started,
        "finishedAt": utc_now(),
        "host": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        "contexts": {"mainFrame": observation, "dedicatedWorker": observation.get("worker")},
        "networkPolicy": "synthetic-page-only",
    }


def _route_synthetic(route: Any) -> None:
    route.fulfill(status=200, content_type="text/html", body="<!doctype html><title>probe</title>")


def run_checkpoint() -> dict[str, Any]:
    """Check basic clean-close persistence; this is not a fidelity qualification."""
    from camoufox.sync_api import Camoufox

    sentinel = "synthetic-checkpoint-sentinel-v1"
    started = utc_now()
    with tempfile.TemporaryDirectory(prefix="multi-profiles-camoufox-checkpoint-") as profile_dir:
        with Camoufox(
            headless=True,
            os="windows",
            persistent_context=True,
            user_data_dir=profile_dir,
        ) as context:
            page = context.new_page()
            page.route("**/*", _route_synthetic)
            page.goto(SYNTHETIC_ORIGIN)
            page.evaluate(
                """async (sentinel) => {
                  localStorage.setItem('sentinel', sentinel);
                  document.cookie = `probe=${sentinel}; Max-Age=86400; Path=/; SameSite=Strict; Secure`;
                  await new Promise((resolve, reject) => {
                    const request = indexedDB.open('probe-db', 1);
                    request.onupgradeneeded = () => request.result.createObjectStore('values');
                    request.onerror = () => reject(request.error);
                    request.onsuccess = () => {
                      const tx = request.result.transaction('values', 'readwrite');
                      tx.objectStore('values').put(sentinel, 'sentinel');
                      tx.oncomplete = resolve;
                      tx.onerror = () => reject(tx.error);
                    };
                  });
                }""",
                sentinel,
            )

        with Camoufox(
            headless=True,
            os="windows",
            persistent_context=True,
            user_data_dir=profile_dir,
        ) as context:
            page = context.new_page()
            page.route("**/*", _route_synthetic)
            page.goto(SYNTHETIC_ORIGIN)
            observed = page.evaluate(
                """async () => {
                  const indexedDb = await new Promise((resolve, reject) => {
                    const request = indexedDB.open('probe-db', 1);
                    request.onerror = () => reject(request.error);
                    request.onsuccess = () => {
                      const tx = request.result.transaction('values', 'readonly');
                      const get = tx.objectStore('values').get('sentinel');
                      get.onsuccess = () => resolve(get.result || null);
                      get.onerror = () => reject(get.error);
                    };
                  });
                  return {
                    localStorage: localStorage.getItem('sentinel'),
                    cookie: document.cookie,
                    indexedDb
                  };
                }"""
            )

    checks = {
        "localStorage": observed.get("localStorage") == sentinel,
        "cookie": f"probe={sentinel}" in observed.get("cookie", ""),
        "indexedDb": observed.get("indexedDb") == sentinel,
    }
    return {
        "schemaVersion": PROBE_SCHEMA_VERSION,
        "kind": "clean-close-checkpoint",
        "startedAt": started,
        "finishedAt": utc_now(),
        "checks": checks,
        "passed": all(checks.values()),
        "scopeLimit": "One disposable profile, clean close, same host and core only",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("smoke", "checkpoint"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_smoke() if args.mode == "smoke" else run_checkpoint()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if result.get("passed", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())

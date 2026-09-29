# Probe Workspace

Phase 1 research probes now exist. They are not production adapters or complete qualification suites. Each declares its bounded purpose in code and is linked to a pre-registration/evidence manifest.

| Probe | Scope | Tests | Explicit limit |
|---|---|---|---|
| `smoke_probe.py` | Offline main-frame/dedicated-worker observation and same-host clean-close cookie/LocalStorage/IndexedDB persistence | `test_smoke_probe.py` | No deterministic-relaunch, crash, portability, or full context claim |
| `sidecar_protocol_probe.py` | Canonical bounded framing and HMAC challenge transcript | `test_sidecar_protocol_probe.py` | No Windows named-pipe transport/ACL/process identity claim |
| `windows_security_probe.py` | DPAPI CurrentUser and suspended-process Job Object feasibility | `test_windows_security_probe.py` | No production secret store or Camoufox tree containment claim |

Run with the locked Phase 1 Python environment:

```powershell
python -m pytest research/camoufox/probes -q
```

Research probes remain experimental until reviewed under `AUD-019`, mapped to [FINGERPRINT_SPEC.md](../../../docs/FINGERPRINT_SPEC.md), and promoted into product/contract test ownership. A probe pass is not proof of completeness.

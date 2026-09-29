# Phase 1 Initial Camoufox/Windows Spike Report

## Control

- Audits: `AUD-001`, `AUD-003`, `AUD-005`, `AUD-012`, `AUD-015`, `AUD-016`, `AUD-024`, `AUD-031`, `AUD-034`
- Owner/operator: Codex Phase 1 audit
- Started (UTC): 2026-09-29T12:57:07Z
- Last updated (UTC): 2026-09-29T13:02:00Z
- Candidate status: Researching; distribution hold

## Pinned inputs

- Repository tag: `v152.0.4-beta.31`; tag object `ba8a8100abda7bc18b9f42c5d01d10c1d264f3ca`; peeled commit `eb5dc3bc5b917d1e6c71d9cacfecdddb55fbfc4a`; annotated tag has no signature.
- Windows x86_64 artifact: `camoufox-152.0.4-beta.31-win.x86_64.zip`, 493,147,697 bytes, SHA-256 `ed63ea51d2a07f99bacdae0f43b9ff5518bfc9ac2f15d84e2251fe06c7141e81`.
- Launcher: Camoufox Python `0.5.6`, BrowserForge `1.2.4`, Playwright Python `1.62.0`, Python `3.11.9`.
- Smoke host: Windows `10.0.19045`, AMD64, Intel HD Graphics observation, `en-US`, `Asia/Bangkok`; this is not the proposed Windows 11 qualification baseline.

## Source observations

| Claim | Exact source | Observation | Quality |
|---|---|---|---|
| Python is the upstream-owned launcher candidate | `pythonlib/pyproject.toml`, `pythonlib/camoufox/sync_api.py` at the peeled commit | Package is `0.5.6`, uses BrowserForge and Playwright `<1.63`, and supports persistent Playwright contexts. | `SOURCE_CONFIRMED` |
| Default launch is not deterministic | `pythonlib/camoufox/utils.py:904-907`; `fingerprints.py:838-840,1006-1008` | Font-spacing, audio, and canvas seeds are randomized unless explicitly overridden; the product cannot treat default launcher output as profile identity. | `SOURCE_CONFIRMED` |
| Current artifact provenance is incomplete | GitHub release metadata and tag inspection | Asset digest is available and matched by the downloader, but the source tag is unsigned, the artifact is attached to `font-bundle-v1`, and no detached artifact signature was found. | `SOURCE_CONFIRMED` |
| Current Windows artifact has a distribution blocker | `bundle/fonts/000_README.txt:11-18`, `Makefile:181-190`, `scripts/package.py:82-97`; installed artifact `fonts/` | The source says bundled fonts are for academic/research use and that commercial use/distribution is not intended or permitted. Windows packaging includes macOS and Linux font bundles, and the downloaded Windows artifact contains a large `fonts/` tree. | `SOURCE_CONFIRMED` |
| Top-level source and Python wrapper have different declared licenses | `LICENSE`; `pythonlib/pyproject.toml` | Repository declares MPL-2.0; Python package metadata declares MIT. This does not settle Firefox, fonts, extensions, vendored code, or binary redistribution. | `SOURCE_CONFIRMED` |

## Runtime results

| Run | Expected | Observed | Disposition |
|---|---|---|---|
| Offline smoke | Launch pinned artifact and collect bounded main-frame/worker observations without external navigation | Passed; UA/platform/language/hardware concurrency matched across main frame and dedicated worker; `navigator.webdriver` was false; canvas/WebGL/screen observations recorded | Passed as a single-host smoke only |
| Checkpoint run 1 | Cookie, LocalStorage, IndexedDB persist after clean close | LocalStorage and IndexedDB passed; cookie failed because fixture created a session cookie | Failed fixture; retained |
| Checkpoint run 2 | Persistent cookie, LocalStorage, IndexedDB persist after clean close | All three passed | Passed within one same-host/same-core clean-close run |
| Protocol unit suite | Framing and HMAC rules reject malformed/tampered inputs | 9 protocol tests passed as part of 11-test suite | Passed; no named-pipe transport claim |
| Windows primitive suite | DPAPI CurrentUser and suspended-process Job Object primitives work | DPAPI round trip/wrong-purpose rejection passed; suspended child was assigned before resume and terminated on job close | Passed; synthetic child/user only |

Unit results: 3 smoke-probe tests passed, then 11 protocol/Windows tests passed. No Camoufox/browser process remained after the recorded probes.

## Launcher recommendation

Use Python as the Phase 1 Camoufox launcher candidate, not as the product-policy or storage authority. The selected Python wrapper is maintained in the official Camoufox repository and supports the exact Playwright range used by this spike. `camoufox-js` `0.12.0` describes itself as experimental and requires `playwright-core <1.61.0`, preventing a like-for-like comparison with Playwright Python `1.62.0`. `AUD-012` therefore remains open; this is a candidate recommendation, not final parity acceptance.

## Decision recommendation

- Continue source/runtime research only.
- Hold any commercial/public distribution of the current Windows artifact until qualified legal review and/or a redistributable font-free build path resolves the explicit bundled-font notice.
- Do not use default launcher randomness for persistent profile identity. Generate and persist versioned deterministic inputs only after the source-to-surface inventory and 50-relaunch mutation suite exist.
- Do not advertise checkpoint or portability fidelity from the clean-close smoke. Crash, concurrent access, profile locking, SQLite/WAL, saved credentials, service workers, session restore, extension state, and cross-host behavior remain untested.
- Carry the concrete Job Object, DPAPI CurrentUser, named-pipe, and Tauri design in `docs/WINDOWS_SECURITY_BOUNDARIES.md` into focused integration spikes.

## Confounders and limits

- Only one Windows 10 host was used; Windows 11, GPU/font matrices, multi-monitor/DPI, other users, and security products were not tested.
- Headless execution is a smoke fixture and not an approved production mode.
- The smoke used default randomly generated fingerprint inputs; it cannot measure relaunch stability.
- The intercepted synthetic origin exercised only a cookie, LocalStorage, and IndexedDB across a clean close.
- No full binary inventory, malware scan, reproducible build, Firefox checksum signature verification, or qualified legal review was completed.
- The Job Object test used a sleeping Python child, not a sidecar/Camoufox tree.
- The DPAPI test did not attempt cross-user decrypt or protect persisted production material.

## Remaining work

`AUD-015` is blocked on the font-distribution issue and legal review. All other linked audits remain `RESEARCHING`; none is `CONFIRMED` or `RESOLVED`. The next safe work is the full license/binary inventory, deterministic input/source map, actual Camoufox-in-Job-Object spike, named-pipe ACL/bootstrap test, and crash/state inventory.

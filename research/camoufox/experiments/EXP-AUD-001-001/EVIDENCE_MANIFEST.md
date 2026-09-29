# Evidence Manifest — EXP-AUD-001-001

## Run metadata

- Run IDs: `20260929T125707Z-offline-smoke`, `20260929T125759Z-checkpoint-session-cookie`, `20260929T125841Z-checkpoint-persistent-cookie`, `20260929T130156Z-windows-primitives`
- Evidence IDs: `EVD-AUD-001-001`, `EVD-AUD-003-001`, `EVD-AUD-005-001`, `EVD-AUD-012-001`, `EVD-AUD-015-001`, `EVD-AUD-016-001`, `EVD-AUD-024-001`, `EVD-AUD-031-001`, `EVD-AUD-034-001`
- Operator: Codex Phase 1 audit
- Environment: `ENV-WIN10-SMOKE-01`
- Procedure: probe schema `0.1.0`; repository working tree version recorded by artifact hash below
- Redaction: no real account/profile/credential/proxy; user-specific interpreter/cache paths omitted from committed results

## Artifact inventory

| Relative path | Kind | Raw/redacted | Size | SHA-256 | Sensitive | Note |
|---|---|---|---:|---|---|---|
| `smoke.json` | runtime | reviewed | 2,785 | `81e03866c21c65e408d192e107a623a657a5b1e6244ed3513e71172e1a903e17` | No | Single-host observation |
| `checkpoint.json` | runtime | reviewed | 360 | `631ff59f7ec4a7c04fccd5fd67f2a28bae64db54622296ae50b8b10dfe336e28` | No | Failed session-cookie fixture retained |
| `checkpoint-run2.json` | runtime | reviewed | 358 | `7bb4a46c06d6d377268e40edc02d66b349b81c18a38a9726667b9d6c3543c2f6` | No | Persistent-cookie rerun |
| `windows-security.json` | runtime | reviewed | 720 | `4a6bcb3ae7be676938ed3fed57634293d24925b040bc922a0097054981f68df8` | No | Synthetic DPAPI/job results only |
| `../../probes/smoke_probe.py` | procedure | source | 8,581 | `21922f2b65932b41776e61496741594e3bfa3dd5f3893f33617e15d6dbd4bc7f` | No | Offline smoke/checkpoint procedure |
| `../../probes/sidecar_protocol_probe.py` | procedure | source | 2,420 | `da826250f22c6629dbf100cbfe889e8ceae1f98bb53eb4e3c7c8f7dbb34a5ad2` | No | Framing/HMAC primitive |
| `../../probes/windows_security_probe.py` | procedure | source | 9,546 | `331c5654867e526b6ac8a78e0632154f782f96255568c45571529281bfc64dc4` | No | DPAPI/Job Object primitive |

Source observations are reproducible from the exact repository/tag/commit and platform artifact in `UPSTREAM_LOCK.json`; the browser ZIP and temporary source clones are intentionally not committed.

## Integrity and review

- Hash tool: PowerShell `Get-FileHash -Algorithm SHA256`
- Hash time: 2026-09-29 UTC
- Raw artifacts unchanged after capture: Yes for JSON result files
- Redacted derivatives: committed JSON contains no secret or user path
- Reviewer: pending independent review

- [x] No real secret, cookie, token, password, identity seed, or user profile data is committed.
- [x] Exact candidate versions and smoke environment are recorded.
- [x] Expected results were written before runtime execution.
- [x] Failed/inconclusive checkpoint run is retained and labeled.
- [x] Large browser/source inputs remain outside Git and are identified by immutable locators/hashes.

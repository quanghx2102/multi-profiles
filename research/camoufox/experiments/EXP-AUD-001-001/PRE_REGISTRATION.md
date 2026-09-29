# EXP-AUD-001-001 — Windows offline smoke and clean-close persistence

- Status: Authorized / running
- Audits: `AUD-001`, `AUD-003`, `AUD-005`, `AUD-012`, `AUD-016`
- Candidate source: `daijro/camoufox` annotated tag object `ba8a8100abda7bc18b9f42c5d01d10c1d264f3ca`, tag `v152.0.4-beta.31`, peeled commit `eb5dc3bc5b917d1e6c71d9cacfecdddb55fbfc4a`
- Browser artifact: `camoufox-152.0.4-beta.31-win.x86_64.zip`, SHA-256 `ed63ea51d2a07f99bacdae0f43b9ff5518bfc9ac2f15d84e2251fe06c7141e81`
- Launcher: Python package `camoufox==0.5.6`, Playwright `1.62.0`, BrowserForge `1.2.4`
- Environment: `ENV-WIN10-SMOKE-01`; unqualified Windows 10 smoke host

## Expected results

1. The exact browser artifact starts through the pinned Python launcher without external navigation.
2. Main-frame fingerprint fields and a dedicated-worker subset can be collected into a redacted JSON record.
3. A cleanly closed persistent context preserves one synthetic cookie, LocalStorage value, and IndexedDB value across one relaunch on the same host/core.

These results do not establish deterministic identity, completeness of surface coverage, crash-safe checkpoint semantics, cross-host portability, credential-safe export, or Windows 11 support.

## Stop conditions

- Stop on unexpected external navigation, secret/profile discovery, an unowned browser process after probe exit, artifact mismatch, or writes outside the disposable profile and Camoufox's already-created package cache.
- The synthetic origin is intercepted locally; no real account, credential, proxy, or user browser profile is used.

## Commands

```powershell
python -m pytest research/camoufox/probes/test_smoke_probe.py
python research/camoufox/probes/smoke_probe.py smoke --output <evidence>/smoke.json
python research/camoufox/probes/smoke_probe.py checkpoint --output <evidence>/checkpoint.json
```

The interpreter and evidence directory are recorded in the run manifest without embedding a user-specific absolute path in committed evidence.

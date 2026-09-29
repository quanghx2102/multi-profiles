# Camoufox Results Index

- Status: Active; evidence remains subject to independent review and audit thresholds

| Evidence/report ID | Audit ID | Source lock | Environment | Summary | Quality | Reviewer | Location |
|---|---|---|---|---|---|---|---|
| `EVD-AUD-001-001` | `AUD-001` | beta.31 candidate | source + `ENV-WIN10-SMOKE-01` | Confirmed three default per-launch seeds; inventory incomplete | `SOURCE_CONFIRMED` | Pending | [EXP-AUD-001-001](experiments/EXP-AUD-001-001/REPORT.md) |
| `EVD-AUD-003-001` | `AUD-003` | beta.31 candidate | `ENV-WIN10-SMOKE-01` | Main/dedicated-worker smoke only | `DOCUMENTED` | Pending | [smoke.json](experiments/EXP-AUD-001-001/smoke.json) |
| `EVD-AUD-005-001` | `AUD-005` | beta.31 candidate | `ENV-WIN10-SMOKE-01` | Clean-close persistent cookie/LocalStorage/IndexedDB smoke | `DOCUMENTED` | Pending | [report](experiments/EXP-AUD-001-001/REPORT.md) |
| `EVD-AUD-012-001` | `AUD-012` | beta.31 candidate | source + `ENV-WIN10-SMOKE-01` | Python candidate launched; TypeScript parity untested | `DOCUMENTED` | Pending | [report](experiments/EXP-AUD-001-001/REPORT.md) |
| `EVD-AUD-015-001` | `AUD-015` | beta.31 candidate | source/artifact | Bundled-font notice creates distribution hold | `SOURCE_CONFIRMED` | Pending legal review | [report](experiments/EXP-AUD-001-001/REPORT.md) |
| `EVD-AUD-016-001` | `AUD-016` | beta.31 candidate | source/artifact | Asset digest verified; unsigned tag/no detached artifact signature | `SOURCE_CONFIRMED` | Pending | [UPSTREAM_LOCK.json](UPSTREAM_LOCK.json) |
| `EVD-AUD-024-001` | `AUD-024` | protocol draft 0.1 | `ENV-WIN10-SMOKE-01` | Framing/HMAC unit rules passed; transport untested | `DOCUMENTED` | Pending | [report](experiments/EXP-AUD-001-001/REPORT.md) |
| `EVD-AUD-031-001` | `AUD-031` | Windows primitive draft | `ENV-WIN10-SMOKE-01` | Suspended child + Job Object kill-on-close passed | `DOCUMENTED` | Pending | [windows-security.json](experiments/EXP-AUD-001-001/windows-security.json) |
| `EVD-AUD-034-001` | `AUD-034` | Windows primitive draft | `ENV-WIN10-SMOKE-01` | DPAPI CurrentUser synthetic round trip passed | `DOCUMENTED` | Pending | [windows-security.json](experiments/EXP-AUD-001-001/windows-security.json) |

Adding a row does not update the authoritative audit status. The reviewed evidence must also be linked from [AUDIT_REGISTER.md](../../docs/AUDIT_REGISTER.md).

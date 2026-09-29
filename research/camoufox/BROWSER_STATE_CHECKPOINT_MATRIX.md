# Camoufox beta.31 Browser-State Checkpoint and Portability Matrix

- Status: Initial clean-close smoke only
- Upstream lock: beta.31 candidate
- Audit: `AUD-005`, with portability dependencies `AUD-010`, `AUD-021`, `AUD-026`
- Last reviewed: 2026-09-29

## Observed state

| State | Write fixture | Clean close + same host/core relaunch | Crash | Snapshot/restore | Cross-host portability | Credential/session sensitivity |
|---|---|---|---|---|---|---|
| Persistent cookie | Synthetic `Secure`, `SameSite=Strict`, `Max-Age=86400` cookie | Passed once | Untested | Untested | Untested | Session-bearing; sensitive |
| Session cookie | Synthetic cookie without expiry | Not retained, as expected for session scope | Untested | Not applicable as persistence promise | Not portable by default | Session-bearing; sensitive |
| LocalStorage | One synthetic origin/key/value | Passed once | Untested | Untested | Untested | May contain tokens; sensitive by policy |
| IndexedDB | One synthetic database/store/key/value | Passed once | Untested | Untested | Untested | May contain tokens/content; sensitive by policy |
| History | Not seeded | Untested | Untested | Untested | Untested | Privacy-sensitive |
| Session restore/tabs | Not seeded | Untested | Untested | Untested | Untested | Must not navigate externally before preflight |
| Saved passwords/form data | Prohibited in initial fixture | Untested | Untested | Untested | Untested | Secret-bearing; default exclusion target unproven |
| Permissions/media IDs | Not seeded | Untested | Untested | Untested | Untested | Host/privacy-sensitive |
| Service worker/cache | Not seeded | Untested | Untested | Untested | Untested | Background traffic/preflight risk |
| Extensions/state | Not seeded | Untested | Untested | Untested | Untested | Compatibility/fingerprint/security risk |
| Certificates | Not seeded | Untested | Untested | Untested | Untested | Potentially secret/trust-bearing |

## Checkpoint contract candidate

A profile directory is eligible for snapshot only when all of the following are positively established:

1. no browser/sidecar process in the verified Job Object remains;
2. graceful close was requested and the owned process tree exited within policy, or the result is explicitly a crash-recovery snapshot class;
3. the operation journal records the close generation and process exit evidence;
4. SQLite/WAL and browser-owned file handles are closed or a documented engine checkpoint primitive confirms consistency;
5. the source directory is locked against concurrent launch/mutation during enumeration and copy;
6. every copied record is streamed into an immutable snapshot with size, path, type, and integrity metadata;
7. reparse points, external paths, devices, alternate streams, and files outside the approved profile root are rejected;
8. restore occurs into a private staging directory, verifies integrity/compatibility, atomically switches only after success, and retains a rollback point;
9. restored/imported state always returns to `LAUNCHED_UNVERIFIED` and passes preflight before external activity.

The current probe establishes only item-level clean-close persistence for three synthetic state types. It does not prove any checkpoint condition above.

## Portability fidelity levels to qualify

| Level | Meaning | Required evidence |
|---|---|---|
| Byte fidelity | Snapshot/container reproduces the selected files and metadata exactly | Manifest/hash round trip, locked source, corruption/truncation tests |
| Browser readability | The same pinned core opens restored state without repair/data loss | Same-host restore matrix and browser diagnostics |
| Session fidelity | Intended cookies/storage/sessions remain usable | Explicit sensitive full-state fixture; never real credentials |
| Identity fidelity | Restored profile retains required semantic fingerprint identity | Full preflight/semantic diff after restore |
| Cross-host fidelity | Approved Windows hardware/environment changes remain within policy | Multi-environment `AUD-010`/`AUD-022` matrix |
| Sanitized fidelity | Excluded secrets/sessions are absent while allowed data works | File/key-level inventory, negative secret scans, per-state functional tests |

A raw user-data-directory copy cannot be called both full fidelity and credential/session free. Until `AUD-026` maps the Firefox key/database linkage, the safe product behavior is to label opaque full state as sensitive and keep sanitized export unimplemented.

## Next tests

- Record a redacted relative-file inventory after each synthetic state fixture.
- Repeat clean close 10 times, then forced browser/sidecar/core termination at defined boundaries.
- Run two profiles with unique sentinels and prove negative cross-profile reads.
- Snapshot under lock, restore on the same host/core, then compare state and fingerprint preflight.
- Repeat on a second qualified Windows 11 host before making any portability claim.

# Test Strategy

## Principle

Tests establish the behavioral contract; README claims do not. Camoufox assertions remain hypotheses until reproducible source or test evidence is attached to the relevant audit item.

Planned acceptance evidence has stable `AT-*` identifiers in [REQUIREMENTS.md](REQUIREMENTS.md). Phase 1 audit reports use [docs/audit](audit/README.md), while exact evidence records and artifacts follow [research/camoufox/evidence](../research/camoufox/evidence/README.md). A template or planned test ID is not completed evidence. Environment descriptors use IDs and dimensions from [SUPPORTED_ENVIRONMENTS.md](SUPPORTED_ENVIRONMENTS.md).

## Test layers

| Layer | Purpose |
|---|---|
| Unit tests | Pure rules, parsing, validation, derivation, diff policy, and state transitions |
| Domain invariant tests | Immutability, legal lifecycle transitions, lock and migration rules |
| Storage integration tests | transactions, atomic manifest writes, schema migration, journaling, and recovery |
| Engine contract tests | common adapter operations, capabilities, idempotency, timeouts, and typed failures |
| Fingerprint restart tests | persistence across repeated clean and crash relaunches |
| Multi-profile isolation tests | distinct identities, directories, state, processes, and no interference |
| Cross-context tests | main frame, iframe, worker, service worker, and worklet propagation |
| Proxy leak tests | HTTP/HTTPS/SOCKS, authentication, DNS, WebRTC, failure and bypass paths |
| Coherence tests | TLS/HTTP headers, locale/timezone/geolocation/proxy, display/DPI, and media-device cross-context behavior |
| Crash/fault-injection tests | process, sidecar, app, disk, and transaction failures at operation boundaries |
| Migration/rollback tests | semantic diffs, storage compatibility, commit, rollback, and retained core |
| Import/export tests | cryptography, mode rules, hostile containers, portability, partial failure |
| Security tests | IPC/API authorization, input bounds, path attacks, redaction, artifact tampering |
| TOCTOU tests | preflight generation invalidation, revalidation triggers, navigation/lease containment, and lost-event races |
| Resource benchmarks | RAM, CPU, GPU, handles, startup/stop time at concurrent profile counts |
| Desktop E2E tests | user-visible workflows through the application boundary in later phases |

## Phase 1 technical-spike minimums

- Restart one profile 50 times with identity observations compared to the accepted baseline.
- Show that two profiles have different intended identities and do not share cookies or storage.
- Exercise main frame, same/cross-origin iframe where feasible, dedicated/shared worker, service worker, and applicable worklets.
- Run multiple independent Camoufox processes and test startup/stop interleavings.
- Inject a crash and restart without regenerating identity.
- Export/import on the same OS and compare identity and browser-state outcomes.
- Test migration between two cores when suitable versions are available.
- Roll back to the prior core and prove the profile remains usable.

These are objectives, not current results. Procedures and gates are tracked in [AUDIT_REGISTER.md](AUDIT_REGISTER.md).

## Evidence protocol

Each experiment records:

- audit ID, hypothesis, repository/core/launcher revisions, artifact hashes;
- OS build, hardware/GPU/driver, locale/timezone, proxy/network topology;
- exact command/config with secrets redacted;
- fixture/profile IDs and whether data is disposable;
- probe schema and raw-result artifact hashes;
- repetitions, timing, resource data, exit codes, and logs;
- expected versus observed outcome;
- reproducibility notes and known confounders.

An observation from one machine is `TEST_CONFIRMED`, not `MULTI_ENV_CONFIRMED`. Source inspection uses exact file paths and commit IDs.

## Fingerprint comparison

The probe inventory must be defined by `AUD-019`. Results distinguish immutable configured values, version-derived values, render-derived values, and uncontrolled host surfaces. A raw hash is diagnostic data, not by itself a pass criterion. Cross-context disagreement and unexplained immutable-field changes fail preflight.

## Isolation assertions

Tests use sentinel cookies/storage values and independent data directories. They verify process trees, filesystem ownership, ports/endpoints, extension state, identity material, and cleanup. A pass requires negative checks: profile B must be unable to observe profile A's sentinel state.

## Fault injection

Inject failure before and after each durable boundary in create, start, stop, snapshot, migration, import, and export. On restart, reconciliation must produce one explainable state, never silently create a new identity, and never report completion when the outcome is unknown.

## Exit criteria relationship

Phase exit criteria are in [DEVELOPMENT_PHASES.md](DEVELOPMENT_PHASES.md). An audit changes status only when its recorded evidence meets the quality needed for its required decision.

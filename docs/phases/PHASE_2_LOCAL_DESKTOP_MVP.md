# Phase 2 — Local Desktop MVP

## Status

`PLANNED`. Production implementation is not authorized until Phase 1 records a `GO` or acceptable `CONDITIONAL GO`.

## Objective

Deliver a Windows-first local desktop MVP that creates, lists, starts, stops, and recovers isolated Camoufox profiles using verified identity and engine contracts. The MVP proves the end-to-end architecture while keeping data portability, full snapshots, automated core migration, and external automation in later phases.

## Entry criteria

- Phase 1 exit decision permits implementation.
- Every Phase 2 blocking audit has an accepted outcome.
- Phase-2-blocking pending decisions in [DECISIONS_REQUIRED.md](../DECISIONS_REQUIRED.md) are approved or explicitly deferred with an enforceable exclusion.
- Camoufox core, launcher, sidecar language/transport, schemas, support matrix, and concurrency limit are pinned.
- Architecture ADRs remain accepted or have explicit superseding ADRs.
- Threat boundaries and test fixtures are approved.
- Any Phase 1-required patches have reproducible builds/artifacts and regression tests.

## Dependencies and assumptions

- Pinned qualified Camoufox core and launcher/sidecar inputs from Phase 1.
- Accepted sidecar protocol, fingerprint probe, proxy modes, process-ownership/containment mechanism, and concurrency cap.
- Windows development/signing is not yet a release requirement, but the supported runtime matrix is available for tests.
- Approved Rust/Tauri/React/SQLite/keychain implementation choices remain adapters behind the documented boundaries.
- Phase 1 regression fixtures can run against the integrated desktop path.

## In scope

- Initial repository/application scaffolding under the accepted architecture.
- Domain and application modules independent of frameworks and engines.
- Profile catalogue: create, inspect, edit allowed metadata, archive/unarchive, move to trash, restore from trash, and permanent purge according to the approved lifecycle decision.
- Search, sort, filter, and basic folders/tags/notes/status.
- Basic non-identity default/template settings and startup URL configuration; each created profile still receives unique identity material.
- SQLite metadata through Rust-side repositories.
- Integrity-protected immutable identity manifest, separate runtime configuration/baseline/compatibility records, and protected profile-secret handle.
- Dedicated data directory and one supervised process tree per running profile.
- Versioned browser-driver sidecar and Camoufox adapter.
- Create/Start/Stop and bounded crash-recovery workflows.
- Exclusive local profile lock and orphan reconciliation.
- Basic per-profile proxy configuration for the Phase 1-approved modes.
- Fingerprint preflight using the approved minimum probe.
- Structured logs, operation IDs, event journal, process exit data, and redaction.
- Minimal internal recovery checkpoint required for safe lifecycle reconciliation.
- Basic UI for supported workflows and actionable errors.

## Out of scope

- User-managed snapshot history and general restore UI; these begin in Phase 3.
- Encrypted backup/transfer/duplicate containers.
- Cookie editor/import/export and extension manager.
- Automatic browser-core migration and rollback orchestration.
- Local REST API, SDKs, Cookie Bot, human typing, or Run with Sync.
- Bulk actions beyond safe UI selection affordances that still execute one profile at a time.
- Cloud, team/workspace, remote browser, mobile, owned proxy network, Puppeteer/CDP parity.

## Phase deliverables

- Implemented domain/application boundaries and typed contracts.
- Local metadata store, separated identity/runtime/observation records, protected secret references, and operation journal.
- Qualified Camoufox adapter, sidecar client/process, and process supervisor.
- Create/Start/Stop/recovery lifecycle with lock and preflight enforcement.
- Basic proxy support and profile catalogue UI.
- Structured diagnostics and redaction baseline.
- MVP test suite, supported environment/concurrency statement, and Phase 3 handoff schemas.

## Functional increments

### Increment 2.1 — Foundations and contracts

- Establish module/package boundaries from [MODULE_BOUNDARIES.md](../MODULE_BOUNDARIES.md).
- Implement domain identifiers, lifecycle states, value validation, typed errors, and capability requirements.
- Accept or revise the [draft schemas](../../contracts/README.md), then generate or maintain typed IPC/protocol bindings from the accepted versions.
- Create composition roots without leaking framework types into domain/application modules.
- Add unit, invariant, contract, and architecture-boundary tests.

Exit signal: pure domain and contract suites pass without Tauri, SQLite, Playwright, or Camoufox dependencies.

### Increment 2.2 — Metadata, identity, and secure storage

- Implement profile, operation, immutable manifest, runtime configuration, core reference, baseline, compatibility, and proxy reference repositories.
- Add transactional schema migration and atomic identity-manifest writes.
- Integrate the approved OS-protected secret mechanism through opaque handles.
- Enforce immutable `profileId`, `engineId`, and `profileSecret` lineage.
- Validate path ownership and prevent profiles from sharing a data directory.

Exit signal: storage crash tests and identity-integrity tests preserve an explainable state without exposing secrets.

### Increment 2.3 — Sidecar, adapter, and process supervision

- Implement the approved protocol and instance authentication.
- Implement the authority split in [SIDECAR_PROCESS_MODEL.md](../SIDECAR_PROCESS_MODEL.md): the supervisor spawns/owns the tree and the sidecar invokes the launcher/owns the automation session.
- Implement Camoufox capability reporting, validated launch, graceful stop, typed exit/error events, and uncertain-outcome reconciliation.
- Track the complete owned process tree and prevent blind duplicate launch.
- Enforce the qualified core/artifact and supported environment.

Exit signal: engine contract suite and protocol crash/authorization suite pass.

### Increment 2.4 — Profile lifecycle

- Implement Create, Start, Stop, and recovery according to [PROFILE_LIFECYCLE.md](../PROFILE_LIFECYCLE.md).
- Run initial verification before `READY` and preflight before `RUNNING`.
- Journal prepare/effect/commit boundaries.
- Retain the lock during uncertain stop/start recovery.
- Create a minimal internal recovery checkpoint where required by the approved persistence strategy.

Exit signal: clean and injected-failure lifecycle matrices produce only allowed states.

### Increment 2.5 — Basic proxy and catalogue UI

- Support only Phase 1-approved proxy schemes and failure policies.
- Store credentials as protected handles and show sanitized connectivity/preflight results.
- Provide profile list, create/edit form, status, search/filter, grouping metadata, start/stop, archive/unarchive, trash/trash-restore, purge, and recovery/quarantine views according to approved lifecycle semantics.
- Allow approved basic defaults/templates and startup URLs without copying identity IDs, secrets, seeds, or accepted baselines.
- Keep renderer models presentation-safe and prohibit raw paths/secrets unless explicitly approved and sanitized.

Exit signal: desktop E2E tests complete core user journeys without database, filesystem, process, or shell access from the renderer.

### Increment 2.6 — MVP hardening

- Exercise supported concurrency and enforce admission limits.
- Test application restart with running, stopping, crashed, and orphaned browser states.
- Validate diagnostic redaction and operation correlation.
- Run supported Windows E2E, storage integration, engine contract, isolation, and security suites.
- Update documentation and ADRs to match implemented behavior.

## Primary user journeys and acceptance

Planned evidence for these journeys uses the `AT-P2-*` identifiers in the [Requirement Catalogue](../REQUIREMENTS.md).

### Create profile

Given a valid supported preset and optional approved proxy, the application creates one profile identity and isolated directory, verifies it, and enters `READY`. On failure, it does not leave an apparently usable profile or regenerate identity on retry without an explicit new create operation.

### Start profile

The application acquires the lock, validates core and manifest, starts exactly one process tree, runs preflight, and enters `RUNNING`. Duplicate starts return a typed state result. Unknown outcomes are reconciled before retry.

### Stop profile

The application blocks new mutations, requests graceful shutdown, confirms process-tree exit and checkpoint status, journals the result, updates metadata, and releases the lock. Forced stop leads to recovery-required status when flush safety is not established.

### Restart application after crash

The application finds incomplete operations and owned orphan processes, reconciles them, preserves identity, and either returns the profile to a known stopped/ready state or quarantines it with a recoverable explanation.

### Run multiple profiles

Within the supported concurrency cap, profiles keep distinct processes, paths, cookies/storage sentinels, extension state where applicable, proxy configuration, and identity material. A failure in one profile does not mutate another.

## MVP UI surfaces

- Profile catalogue and status indicators.
- Create/edit allowed metadata and device-preset selection.
- Start/stop and operation progress.
- Basic proxy assignment/test result.
- Quarantine/recovery explanation.
- Sanitized lifecycle event view.
- Core/engine version and capability information.

Custom table behavior and visual polish may be incremental, but safety-critical states and failures cannot be hidden behind generic errors.

## Data and security requirements

- Renderer has no direct SQL, filesystem, process, keychain, or shell authority.
- Sidecar and browser accept only core-resolved resources for the locked profile.
- No cookie, token, proxy password, profile secret, derived seed, or API credential appears in normal logs.
- Database, manifest, and journal transitions follow the consistency rules in [STORAGE_MODEL.md](../STORAGE_MODEL.md).
- Unverified core, manifest-integrity failure, unsupported capability, or failed preflight prevents `RUNNING`.
- Basic proxy failure follows the approved close/reject behavior; it never silently falls back to direct access.

## Test obligations

- Domain invariant and illegal-transition tests.
- Repository, schema migration, atomic-write, and crash-recovery integration tests.
- Sidecar protocol conformance, authorization, timeout, duplicate-request, and crash tests.
- Engine contract and minimum fingerprint-preflight tests.
- Profile restart and multi-profile isolation tests on the supported matrix.
- Proxy failure/leak regression for supported modes.
- Desktop E2E for every primary journey and quarantine path.
- Structured-log and diagnostic redaction tests.

## Exit criteria

- Core profile catalogue and lifecycle journeys pass end to end on every supported Windows environment.
- Existing profile identities do not regenerate during ordinary restart or crash reconciliation.
- Supported concurrent profiles pass negative state-isolation checks within the published cap.
- No browser reaches `RUNNING` without qualified core, valid manifest, lock, and successful preflight.
- Every injected lifecycle fault resolves to an allowed known state or quarantine.
- Basic proxy modes meet their Phase 1-approved behavior.
- Renderer boundary and secret-redaction security tests pass.
- No open critical defect or unresolved Phase 2 audit assumption remains.
- Phase 3 receives stable storage, checkpoint, manifest, engine, and compatibility contracts.

## Risks and controls

| Risk | Control |
|---|---|
| Spike behavior differs in packaged app | Run contract/E2E tests against the packaged integration, not only laboratory scripts |
| UI races lifecycle operations | Application-owned operation serialization and idempotent UI commands |
| SQLite says stopped while browser remains | Operation journal and process reconciliation before state commit |
| MVP checkpoint is mistaken for full backup | Label it internal and defer user-managed snapshots/restore to Phase 3 |
| Resource pressure violates isolation | Enforce measured admission cap; never overcommit silently |
| Framework types leak inward | Architecture-boundary tests and module review |

## Handoff to Phase 3

The handoff includes stable profile, immutable manifest, runtime configuration, baseline, and compatibility schemas; repository contracts; checkpoint semantics; browser-state inventory; extension capability result; supported proxy modes; keychain abstraction; lifecycle recovery behavior; compatibility-report inputs; and production-grade regression fixtures.

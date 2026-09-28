# Phase 3 — Data Safety and Portability

## Status

`PLANNED`.

## Objective

Turn the MVP's locally persistent profiles into recoverable, inspectable, and deliberately portable assets. Add policy-governed snapshots, restore, cookie operations, Firefox-extension management, a complete third-party proxy manager, OS-backed secret handling, and encrypted Backup/Transfer/Duplicate workflows without weakening identity invariants.

## Entry criteria

- Phase 2 is complete with stable lifecycle, repository, manifest, checkpoint, and sidecar contracts.
- Browser-state ownership and safe checkpoint behavior from `AUD-005` and `AUD-013` are accepted.
- Cross-host portability (`AUD-010`), extension compatibility (`AUD-011`), same-OS round trip (`AUD-021`), and browser-state credential/session boundaries (`AUD-026`) have evidence-backed scope decisions.
- Host-dependent constraints from `AUD-022` are expressible in compatibility reports.
- Cryptographic design and key-recovery policy have been reviewed before portability implementation begins.
- `DEC-PORTABILITY-001` is approved and the [data inclusion matrix](../IMPORT_EXPORT.md#data-inclusion-policy-matrix) is evidence-compatible.

## Dependencies and assumptions

- Stable Phase 2 profile, immutable identity, runtime configuration, baseline/compatibility, operation, and checkpoint schemas.
- Verified browser-state inventory and safe stopped/checkpointed-copy procedure.
- Approved cryptographic primitives/libraries and OS keychain adapter.
- Disposable portability fixtures on every supported source/target environment.
- A tested compatibility-report input model for OS, engine, core, identity, state, extension, and proxy data.

## In scope

- User-visible snapshots, retention, verification, and restore.
- Cookie view/import/export/delete for explicitly supported formats and fields.
- Encrypted portability container and compatibility report.
- Backup, Transfer, and Duplicate-as-new workflows.
- Per-profile Firefox-compatible extension inventory and lifecycle.
- Full third-party proxy inventory, import, assignment, health status, and encrypted credentials.
- OS keychain integration and secret lifecycle hardening.
- Host/core/engine/schema compatibility validation before restore/import.
- Security tests for hostile containers, paths, metadata, and corrupted recovery artifacts.

## Out of scope

- Cloud synchronization, shared remote storage, team transfer, or distributed locking.
- Automatic browser-core migration; Phase 4 owns updater orchestration.
- Chrome-only extensions or Chrome Web Store parity.
- Importing opaque state into a different browser engine.
- Any default export of separately managed credentials, or any claim that opaque browser state is credential/session-free without `AUD-026` evidence.
- Claiming cross-machine identity preservation beyond the tested compatibility envelope.

## Phase deliverables

- Verified snapshot catalogue, retention, integrity, and restore workflow.
- Supported cookie operation formats and per-record validation.
- Versioned authenticated portability-container specification and implementation.
- Backup, Transfer, and Duplicate-as-new workflows.
- Firefox-extension support catalogue and manager.
- Full third-party proxy inventory/health/assignment manager.
- OS-protected secret lifecycle and import/restore compatibility report.
- Evidence-backed browser-state sensitivity inventory and approved sanitized/full-state mode boundaries from `AUD-026`.
- Recovery, hostile-input, portability, and security regression suites.

## Workstreams

### 1. Snapshot recovery

Implement snapshot recovery only from a confirmed stopped/checkpointed state. The snapshot manager records profile, engine/core, identity-schema, browser-state inventory, source checkpoint, content integrity, creation operation, and compatibility requirements. This is distinct from backup recovery and trash restoration in [Profile Lifecycle](../PROFILE_LIFECYCLE.md).

Required behavior:

- immutable completed snapshots;
- configurable retention that never deletes the only required rollback point;
- integrity verification before restore;
- restore staging rather than in-place partial overwrite;
- profile lock during restore;
- identity manifest preserved exactly for same-profile recovery;
- post-restore storage checks and fingerprint preflight;
- quarantine and original-data preservation on uncertain failure.

The exact copy/deduplication/archive mechanism is an implementation choice constrained by Windows correctness and the measured profile layout; it is not fixed by this phase document.

### 2. Cookie and browser-state operations

Target JSON, Netscape, and plain-text cookie import/export only after their exact accepted schemas are specified. Validate domain, path, expiry, SameSite, Secure, HttpOnly, partitioning, and unsupported attributes. Do not edit a live browser database directly.

Operations must run through an engine-supported or checkpoint-safe path and return per-record validation outcomes. Bulk extraction excludes secrets from logs and diagnostic bundles. LocalStorage, IndexedDB, session state, history, login/key databases, and extension data follow the `AUD-005`/`AUD-026` support matrix rather than being advertised generically. Opaque state is treated as sensitive until classified.

### 3. Encrypted portability container

Implement [IMPORT_EXPORT.md](../IMPORT_EXPORT.md) as a streaming, authenticated, versioned format without plaintext ZIP staging. The container includes only a bounded public header before authentication and rejects traversal, unsafe reparse/symlink behavior, duplicate paths, decompression/resource abuse, unknown critical fields, and partially authenticated content.

The cryptographic specification must define:

- algorithms and parameter profiles;
- key derivation and domain separation;
- passphrase or keychain flows;
- per-record nonce and ordering rules;
- authenticated metadata and finalization;
- interrupted export/import behavior;
- format upgrade and deprecation policy;
- recovery limitations and secure cleanup expectations.

### 4. Mode-specific workflows

#### Backup

Preserve profile ID, engine binding, identity lineage, secret, selected browser state, and compatibility metadata. The source remains valid. If the target catalogue already contains the profile ID, only the explicit staged replace/recovery workflow may proceed; a second runnable entry is forbidden. An absent target identity may be imported, with a warning that exported copies outside local control can represent the same identity.

#### Transfer

Preserve identity and selected state, then archive/mark the locally coordinated source only after the destination is positively committed. Clearly state that exported copies cannot be globally revoked or locked by a local-only product.

#### Duplicate as new profile

Create a new profile ID, profile secret, derived identity, manifest, baseline, and data directory. Copy only approved non-identity data and configuration. Never relabel copied browser state as a new identity without per-type compatibility and privacy rules.

### 5. Firefox-extension management

- Maintain an allow/support matrix from `AUD-011`.
- Install/update/remove only while lifecycle policy says the profile state is safe.
- Keep extension files and state isolated per profile.
- Surface permissions and fingerprint/security effects.
- Preserve approved extension state in snapshot/export only when its support classification permits.
- Reject Chrome-only or incompatible extension claims explicitly.

### 6. Complete third-party proxy manager

- Proxy inventory with normalized scheme/endpoint and opaque credential handle.
- Bulk import with per-entry validation and no secret echo.
- Assignment and reassignment with explicit running-profile policy.
- Health, latency, observed egress IP/country, last error, and status history.
- Static/rotating or sticky-session parameters only when the provider syntax and engine behavior are explicitly supported.
- Profile-usage visibility and safe archive/delete constraints.
- Regression leak test after material configuration change.

No traffic billing, residential/mobile network, or phone proxy device is included.

### 7. Keychain and secret lifecycle

Move all supported durable credentials to the approved OS-protected store. Define creation, lookup, access failure, backup/transfer inclusion, rotation, removal, and orphan cleanup. UI, logs, argv, diagnostic bundles, and normal database rows retain only opaque handles or redacted metadata.

## Compatibility report

Before restore or import, generate a report covering:

- container and schema versions;
- source/target OS compatibility;
- engine ID and required capabilities;
- browser-core availability and artifact identity;
- identity/device preset versions;
- host-dependent surface risks;
- browser-state and extension support;
- proxy configuration versus credential availability;
- fields omitted by policy;
- required migrations, blockers, warnings, and expected semantic changes.

Warnings cannot override hard blockers such as engine mismatch, failed authentication, missing required identity secret, or unsupported critical schema.

## Acceptance scenarios

Planned evidence for these scenarios uses the `AT-P3-*` identifiers in the [Requirement Catalogue](../REQUIREMENTS.md).

- Create several snapshots after safe stops, verify retention, corrupt one artifact, and prove it is rejected.
- Restore a verified snapshot without changing the identity manifest and pass post-restore preflight.
- Import malformed and hostile cookie records with isolated per-record errors and no live-database corruption.
- Complete encrypted Backup round trips under supported same-OS scenarios with no plaintext staging remnants detected by the defined test.
- Reject a same-identity catalogue collision unless explicit replace/recovery is selected; prove the staged replacement commits fully or restores the prior state.
- Complete Transfer with correct source state for success, destination failure, and acknowledgement loss.
- Complete Duplicate as new and prove profile/secret/identity differ while approved copied data remains usable.
- Reject wrong passphrase/key, tampered header/payload/index, traversal, oversized content, and interrupted containers.
- Seed saved logins, sessions, tokens, and browser storage and prove every approved sanitized/full-state mode matches the `AUD-026` inventory and sensitivity policy.
- Install and persist only supported Firefox-extension fixtures with permission visibility.
- Import/test/assign supported proxy types without exposing credentials and without silent direct fallback.

## Test obligations

- Snapshot integrity, interruption, retention, restore, and fault-injection tests.
- Cookie parser property/fuzz tests and supported-format fixtures.
- Portability cryptographic known-answer, tamper, truncation, replay, resource-bound, and cleanup tests.
- Mode-invariant tests for identity and source-state behavior.
- Credential/session file-and-key inventory, exclusion, residual-secret scan, and restored-usability tests from `AUD-026`.
- Cross-path/user and supported cross-host compatibility matrix.
- Extension permission, persistence, snapshot, and incompatibility tests.
- Proxy inventory/import/credential/health/leak tests.
- Keychain denial, missing-entry, rotation, and orphan-cleanup tests.
- Desktop E2E for recovery and every portability mode.

## Exit criteria

- Snapshot and restore preserve identity and supported browser state across the declared matrix.
- Encrypted containers authenticate all protected metadata/content and leave no approved plaintext staging artifact.
- Backup, Transfer, and Duplicate enforce distinct identity/source semantics in success and failure paths.
- Same-catalogue identity collisions never create a second runnable entry; replace/recovery is staged, verified, and rollback-safe.
- Cookie operations preserve supported fields and reject unsafe/invalid data without touching a running browser database directly.
- Extension support is accurately bounded to tested Firefox-compatible behavior.
- Proxy credentials and profile secrets are protected by the approved keychain flow.
- Compatibility reports block unsupported imports/restores before mutation.
- No critical portability, crypto, path-handling, or recovery defect remains.
- Phase 4 receives stable snapshots and compatibility primitives suitable for update rollback.

## Risks and controls

| Risk | Control |
|---|---|
| Snapshot captures active database state | Require confirmed checkpoint and profile lock |
| Transfer creates two live identities | Explicit warning/source state; acknowledge local-only enforcement limit |
| Backup or Duplicate carries hidden credential/session state | Treat opaque data as sensitive; require `AUD-026` inventory, explicit mode policy, and seeded residual tests |
| Cross-host import changes rendering | Compatibility report plus `AUD-010`/`AUD-022` constraints and preflight |
| Archive parser becomes an attack surface | Streaming bounds, canonical paths, authentication before commit, hostile fixtures |
| Extension changes fingerprint or reads data | Permission disclosure, support matrix, isolation, explicit user action |

## Handoff to Phase 4

The handoff includes verified recovery snapshots, import/export schema, compatibility report, protected credential interfaces, core-artifact references, rollback-safe staging primitives, extension/proxy capability data, and complete portability/security regression suites.

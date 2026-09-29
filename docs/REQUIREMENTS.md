# Requirements Catalogue

**Status:** Accepted catalogue; individual requirement status is shown below  
**Owner:** Product and architecture maintainers  
**Review trigger:** scope, architecture, contract, or phase-gate change

This file assigns stable IDs to concise normative requirements. The linked owner document defines full behavior; ADRs explain decisions; `AUD-*` items hold unverified runtime claims. A documented requirement is not evidence that Camoufox satisfies it.

## Product and lifecycle requirements

| ID | Statement | Rationale | Owner | Phase | Audit dependencies | Verification | Status |
|---|---|---|---|---|---|---|---|
| `REQ-PROFILE-001` | Create a profile only after identity, storage, preset, and integrity validation succeeds. | Prevent partial identities. | [Profile Lifecycle](PROFILE_LIFECYCLE.md) | 2 | `AUD-001`–`AUD-007`, `AUD-013` | `AT-P2-001`, fault injection | Accepted |
| `REQ-PROFILE-002` | Give every running profile a dedicated browser-data directory and supervised process tree. | Enforce isolation. | [Profile Lifecycle](PROFILE_LIFECYCLE.md) | 1–2 | `AUD-004`, `AUD-005`, `AUD-014`, `AUD-024` | `AT-P1-002`, `AT-P2-003` | Accepted |
| `REQ-PROFILE-003` | Serialize profile mutations with a profile lock and durable operation record. | Make crash recovery deterministic. | [Operations Model](OPERATIONS_MODEL.md) | 2 | `AUD-013`, `AUD-024` | `AT-P2-002` | Accepted |
| `REQ-PROFILE-004` | Distinguish archive, trash, purge, snapshot recovery, backup recovery, transfer, and duplication. | Avoid destructive ambiguity. | [Profile Lifecycle](PROFILE_LIFECYCLE.md) | 2–3 | `AUD-005`, `AUD-013`, `AUD-021`, `AUD-026` | lifecycle and recovery contract tests | Proposed |
| `REQ-PROFILE-005` | Do not grant external navigation, restored external tabs, or automation lease before preflight passes. | Contain an unverified launch. | [Profile Lifecycle](PROFILE_LIFECYCLE.md) | 2 | `AUD-019`, `AUD-032` | `AT-P2-004` | Accepted |
| `REQ-PROFILE-006` | Represent uncertain lifecycle outcomes explicitly and reconcile before retry. | Avoid duplicate launch or destructive guesses. | [Operations Model](OPERATIONS_MODEL.md) | 2 | `AUD-013`, `AUD-024` | `AT-P1-005`, `AT-P2-002` | Accepted |

## Identity and engine requirements

| ID | Statement | Rationale | Owner | Phase | Audit dependencies | Verification | Status |
|---|---|---|---|---|---|---|---|
| `REQ-IDENTITY-001` | Keep `profileId`, `engineId`, `profileSecret`, lineage, and derivation namespace immutable after creation. | Preserve identity meaning. | [Identity Model](IDENTITY_MODEL.md) | 1–2 | `AUD-001`–`AUD-007`, `AUD-022` | `AT-P1-001`, invariant tests | Accepted |
| `REQ-IDENTITY-002` | Derive configured identity material deterministically using versioned, domain-separated derivation. | Prevent restart randomness and cross-surface coupling. | [Identity Model](IDENTITY_MODEL.md) | 1–2 | `AUD-001`–`AUD-003`, `AUD-006`, `AUD-007` | `AT-P1-001` | Accepted |
| `REQ-IDENTITY-003` | Separate immutable identity, version-derived configuration, render observations, mutable runtime configuration, proxy data, and user metadata. | Give each datum one authority and lifecycle. | [Identity Model](IDENTITY_MODEL.md) | 2 | `AUD-022`, `AUD-032` | schema and repository tests | Accepted |
| `REQ-IDENTITY-004` | Compare observations semantically using a versioned policy; raw hash equality is not the sole criterion. | Distinguish expected rendering variance from identity drift. | [Fingerprint Specification](FINGERPRINT_SPEC.md) | 1–2 | `AUD-019`, `AUD-022`, `AUD-027`–`AUD-030` | `AT-P1-003` | Accepted |
| `REQ-IDENTITY-005` | Never auto-accept a candidate baseline or unexpected drift. | Prevent evidence from rewriting its own expectation. | [Fingerprint Specification](FINGERPRINT_SPEC.md) | 1–2 | `AUD-019`, `AUD-032` | baseline lifecycle tests | Accepted |
| `REQ-ENGINE-001` | Access browser engines only through the versioned capability contract. | Keep domain and application engine-neutral. | [Engine Contract](ENGINE_CONTRACT.md) | 1–2 | `AUD-012`, `AUD-024` | `AT-P1-007`, `AT-P2-005` | Accepted |
| `REQ-ENGINE-002` | Fail with a typed error when a required identity capability is unavailable; never use random or best-effort fallback. | Avoid silent identity mutation. | [Engine Contract](ENGINE_CONTRACT.md) | 2 | engine-specific audits | contract conformance tests | Accepted |
| `REQ-ENGINE-003` | Treat Camoufox/Firefox as the first unverified engine candidate and audit Chromium independently as a separate adapter. | Prevent unsupported capability inheritance. | [Product Scope](PRODUCT_SCOPE.md) | 1/5 | `AUD-001`–`AUD-034` as applicable | audit decisions, `AT-P5-008` | Accepted |

## Storage, update, portability, and operations requirements

| ID | Statement | Rationale | Owner | Phase | Audit dependencies | Verification | Status |
|---|---|---|---|---|---|---|---|
| `REQ-STORAGE-001` | Keep authoritative records distinct from caches, indexes, and derived projections. | Prevent competing sources of truth. | [Data Authority](DATA_AUTHORITY.md) | 2 | `AUD-013` | repository consistency tests | Accepted |
| `REQ-STORAGE-002` | Store plaintext secrets only through an approved protected-secret boundary and use opaque handles elsewhere. | Limit disclosure. | [Security Model](SECURITY_MODEL.md) | 2 | `AUD-018`, `AUD-026`, `AUD-034` | `AT-P2-007` | Accepted |
| `REQ-STORAGE-003` | Transition active core and accepted baseline as one journaled activation unit. | Avoid core/baseline mismatch. | [Data Authority](DATA_AUTHORITY.md) | 4 | `AUD-009`, `AUD-019`, `AUD-020`, `AUD-032` | `AT-P4-002`, `AT-P4-003` | Proposed |
| `REQ-UPDATE-001` | Install immutable cores side by side and activate only after provenance, qualification, canary, and rollback preparation. | Bound update risk. | [Update Strategy](UPDATE_STRATEGY.md) | 4A | `AUD-009`, `AUD-015`, `AUD-016`, `AUD-020` | `AT-P4-001`–`AT-P4-004` | Accepted |
| `REQ-PORTABILITY-001` | Expose Backup, Transfer, and Duplicate as new as separate authenticated-encryption workflows. | Their identity and source semantics differ. | [Import/Export](IMPORT_EXPORT.md) | 3 | `AUD-010`, `AUD-021`, `AUD-022`, `AUD-026` | `AT-P3-004`–`AT-P3-007` | Accepted |
| `REQ-PORTABILITY-002` | Never create a second runnable catalogue entry with the same `profileId`. | Preserve local identity uniqueness. | [Import/Export](IMPORT_EXPORT.md) | 3 | `AUD-021`, `AUD-026` | collision tests | Accepted |
| `REQ-PORTABILITY-003` | Treat opaque browser state as session- and credential-bearing until audited otherwise. | Exclusion cannot be inferred from filenames. | [Import/Export](IMPORT_EXPORT.md) | 1–3 | `AUD-005`, `AUD-026` | inventory and leakage tests | Accepted |
| `REQ-OPERATIONS-001` | Give every effectful request an operation ID and every causal workflow a correlation ID. | Support idempotency and diagnosis. | [Operations Model](OPERATIONS_MODEL.md) | 2 | `AUD-013`, `AUD-024` | operation-store tests | Accepted |
| `REQ-OPERATIONS-002` | Implement bulk work as bounded independent profile operations with per-profile outcomes. | Isolate failure and cancellation. | [Operations Model](OPERATIONS_MODEL.md) | 4A | `AUD-014` | `AT-P4-005` | Accepted |

## Security and architectural invariants

| ID | Statement | Rationale | Owner | Phase | Audit dependencies | Verification | Status |
|---|---|---|---|---|---|---|---|
| `SEC-001` | Keep plaintext secrets out of renderer models, argv, ordinary logs, diagnostic bundles, and plaintext staging. | These paths are broadly observable. | [Threat Model](THREAT_MODEL.md) | 2–5 | `AUD-018`, `AUD-026`, `AUD-034` | seeded-secret scans | Accepted |
| `SEC-002` | Authenticate, version, authorize, and bound every local core/sidecar or local-API request. | Localhost and same-user are not trust boundaries. | [Threat Model](THREAT_MODEL.md) | 1–4A | `AUD-024`, `AUD-033`, `AUD-034` | protocol abuse tests | Accepted |
| `SEC-003` | Pin and verify provenance and integrity before accepting executable artifacts. | Reduce supply-chain risk. | [Upstream Dependencies](UPSTREAM_DEPENDENCIES.md) | 1–5 | `AUD-015`, `AUD-016`, `AUD-023`, `AUD-031` | provenance review and tamper tests | Accepted |
| `SEC-004` | Reject path traversal, junction/reparse escape, and unsafe executable/DLL resolution. | Windows filesystem indirection crosses trust boundaries. | [Threat Model](THREAT_MODEL.md) | 2–5 | `AUD-031`, `AUD-033` | adversarial path tests | Accepted |
| `INV-001` | Domain and application logic do not depend on Tauri, SQLite, Playwright, Camoufox, Chromium, or concrete filesystem APIs. | Preserve testability and adapter replaceability. | [Architecture](ARCHITECTURE.md) | 2–5 | — | architecture boundary tests | Accepted |
| `INV-002` | UI code cannot access the database, spawn processes, execute arbitrary shell commands, or handle plaintext secrets. | Keep the renderer outside trusted capabilities. | [Architecture](ARCHITECTURE.md) | 2–5 | `AUD-033` | IPC allowlist and dependency tests | Accepted |
| `INV-003` | No product claim promises undetectability or unlinkability. | Host, network, account, and behavioral correlation remain possible. | [Product Scope](PRODUCT_SCOPE.md) | all | — | release claim review | Accepted |
| `INV-004` | Do not promote an audit conclusion without the evidence required by governance. | Preserve epistemic integrity. | [Documentation Governance](DOCUMENTATION_GOVERNANCE.md) | all | all | `scripts/docs-check.ps1`, review | Accepted |

## Planned verification identifiers

`AT-*` identifiers reserve names for future evidence; they do not assert that a test ran. Phase documents own their detailed procedure.

| Range | Purpose | Owner |
|---|---|---|
| `AT-P1-001`–`AT-P1-007` | identity, isolation, fingerprint, proxy, protocol, upstream/resource, and launcher audit evidence | [Phase 1](phases/PHASE_1_AUDIT_AND_TECHNICAL_SPIKE.md) |
| `AT-P2-001`–`AT-P2-008` | desktop lifecycle, recovery, isolation, preflight, contracts, proxy, security/renderer, and architecture tests | [Phase 2](phases/PHASE_2_LOCAL_DESKTOP_MVP.md) |
| `AT-P3-001`–`AT-P3-009` | snapshot, restore, portability, extension, and proxy tests | [Phase 3](phases/PHASE_3_DATA_SAFETY_AND_PORTABILITY.md) |
| `AT-P4-001`–`AT-P4-008` | update, migration, bulk, API, lease, and optional automation tests | [Phase 4](phases/PHASE_4_CORE_UPDATE_AUTOMATION_AND_BULK.md) |
| `AT-P5-001`–`AT-P5-009` | distribution, environment, security, soak, diagnostics, release, registry, Chromium, and claim tests | [Phase 5](phases/PHASE_5_PRODUCTION_HARDENING_AND_EXTENSIBILITY.md) |

## Legacy ID aliases

Earlier drafts used `FR-*` and `NFR-*`. They are not canonical. Review history may map them to the closest `REQ-*`, `SEC-*`, or `INV-*` entry, but new documents and contracts must use the canonical IDs above.

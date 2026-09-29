# Physical Schema, Local API, and Generated-Binding Readiness

- Status: Proposed implementation blueprint; production artifacts gated
- Owner: Data, application API, and contract workstreams
- Last reviewed: 2026-09-29
- Review trigger: Phase 1 gate or `DEC-DATA-001`, `DEC-LIFECYCLE-001`, `DEC-PROFILE-001`, `DEC-API-001`, or contract-schema change

## Why production generation is not started

The repository is still in Phase 1. Creating final SQL migrations, accepting endpoint behavior, or generating production Rust/TypeScript/Python bindings now would silently choose unresolved authority and lifecycle decisions. The blockers are:

- `DEC-DATA-001`: physical ownership of `activeCoreId` and the activation unit;
- `DEC-LIFECYCLE-001`: persisted `READY`/`STOPPED` vocabulary;
- `DEC-PROFILE-001`: archive/trash/purge fields and retention semantics;
- `DEC-SIDECAR-001`: protocol topology and implementation language;
- `DEC-API-001`: whether the Phase 4 local API is enabled by default;
- Phase 1 `GO`/`CONDITIONAL GO` and accepted schema-generation tooling.

This is a bounded blueprint, not a migration or public API promise. It prevents later work from improvising ownership while preserving the current gates.

## Candidate SQLite schema modules

Every table has a schema-owned migration, UTC timestamp representation selected once, foreign keys enabled, explicit constraints, and no plaintext secret columns. JSON is used only for versioned canonical records or bounded diagnostics, not as a substitute for known relational keys.

| Module | Candidate tables | Required key/authority | Explicitly excluded |
|---|---|---|---|
| Catalogue | `profiles` | `profile_id`; engine/profile/secret reference immutable; lifecycle, archive/trash fields and row version | Absolute browser path as identity; plaintext secret |
| Identity | `identity_manifests` | one active immutable manifest per profile plus retained version lineage and integrity hash | Mutable proxy/core choices; observed fingerprint |
| Runtime | `runtime_configurations`, `proxy_assignments` | versioned mutable config referenced by profile | Proxy credential value |
| Core | `core_installations`, `profile_core_activations` | artifact/hash/provenance identity; atomic profile/core/baseline/generation activation | Mutable files inside a verified core |
| Observation | `fingerprint_baselines`, `compatibility_records` | immutable candidates/history; exactly one accepted pointer through the activation unit | Auto-accepting probe output |
| Operations | `operations`, `operation_events`, `process_exits` | idempotency key, durable phase/outcome, sequence, safe details | Treating requested intent as observed success |
| Recovery | `snapshots`, `snapshot_members`, `import_export_jobs` | immutable integrity-addressed records and staged commit state | Raw secret/session values in metadata |
| Infrastructure | `schema_migrations`, `application_metadata` | applied migration ID/checksum and database format version | Browser-core migration hidden in DB migration |

The initial migration must encode these constraints rather than rely only on application checks:

- unique `profile_id` and immutable `engine_id`, `profile_secret_ref`, and original identity lineage;
- unique non-null active operation/lease per profile where SQLite constraints can express it, with transactional enforcement otherwise;
- foreign-key protection for active core/baseline references;
- compare-and-swap `row_version` or activation generation for concurrent lifecycle changes;
- operation idempotency uniqueness scoped to caller/operation kind;
- no successful snapshot/migration/stop outcome without the required evidence reference;
- cascading delete is forbidden for profiles, cores, baselines, operations, and snapshots until the approved purge workflow executes.

The DDL cannot be finalized until the three data/lifecycle/profile decisions above are approved. `STORAGE_MODEL.md` and `DATA_AUTHORITY.md` remain authoritative meanwhile.

## Candidate application-facing local API

The API exposes application use cases, not storage or Playwright. All mutating calls return a durable operation reference; clients observe terminal status instead of holding an HTTP connection across browser effects.

| Method/path | Application operation | Result shape | Gate |
|---|---|---|---|
| `GET /v1/capabilities` | negotiated product/API capabilities | versioned capability document | API enabled and authenticated |
| `GET /v1/profiles` | list/filter catalogue metadata | bounded page + cursor | no secret/runtime internals |
| `POST /v1/profiles` | create profile | `202` operation reference | accepted identity/profile decisions |
| `GET /v1/profiles/{profileId}` | get safe profile view | profile projection + current operation | ownership authorization |
| `POST /v1/profiles/{profileId}:start` | start and preflight | `202` operation reference | qualified engine/proxy/preflight |
| `POST /v1/profiles/{profileId}:stop` | graceful stop | `202` operation reference | checkpoint semantics |
| `POST /v1/profiles/{profileId}:archive` | archive | `202` operation reference | `DEC-PROFILE-001` |
| `POST /v1/profiles/{profileId}:unarchive` | unarchive | `202` operation reference | `DEC-PROFILE-001` |
| `POST /v1/profiles/{profileId}:trash` | enter retention trash | `202` operation reference | `DEC-PROFILE-001` |
| `POST /v1/profiles/{profileId}:restore-from-trash` | reverse trash within retention | `202` operation reference | `DEC-PROFILE-001` |
| `POST /v1/profiles/{profileId}:purge` | explicit irreversible purge | `202` operation reference + confirmation token policy | `DEC-PROFILE-001`, retention/security review |
| `GET /v1/operations/{operationId}` | inspect durable operation | typed operation status/result | caller scope |
| `POST /v1/operations/{operationId}:cancel` | request cancellation | accepted/rejected cancellation state | operation capability |

Not in the initial API: arbitrary URLs or scripts, raw Playwright/CDP/Juggler, SQL, filesystem paths, shell commands, keychain access, browser PID termination, raw cookies, plaintext proxy credentials, automatic baseline acceptance, or unrestricted bulk execution.

All calls require a versioned content type, loopback binding, high-entropy bearer credential from the protected store, strict body/header/time limits, origin policy where relevant, idempotency keys for mutations, rate/admission limits, and typed redacted errors. The precise OpenAPI document remains a Phase 4A deliverable after `DEC-API-001` and `AUD-018`; freezing it in Phase 1 would incorrectly imply implementation support.

## Generated bindings

The JSON Schemas under `contracts/schemas` remain the wire authority. Once Phase 1 accepts the protocol and generator stack, one deterministic command must generate:

```text
contracts/generated/
  rust/       # trusted core/engine-contract wire DTOs
  typescript/ # renderer/API client DTOs
  python/     # Python sidecar DTOs if Python is selected
```

Rules:

- pin generator names, versions, package hashes, configuration, and runtime version;
- generated files carry `GENERATED — DO NOT EDIT`, schema version, and generation fingerprint;
- generation is offline/reproducible from committed schemas and locked tools;
- CI regenerates into a temporary directory and fails on any diff;
- validate canonical positive/negative fixtures against JSON Schema and every language binding;
- keep domain types separate from wire DTOs; conversion code enforces invariants;
- never generate logging/serialization permission from field presence; `x-sensitive` remains a documentation/security annotation;
- a Python sidecar does not make Python the database or product-policy authority.

Generator selection is intentionally open. Choosing a convenient tool before verifying draft-2020-12 support, format handling, closed enums, numeric bounds, relative `$ref`, and Rust/TypeScript/Python parity would create false type safety.

## Acceptance sequence

1. Resolve the named decisions and Phase 1 gate.
2. Freeze physical identifiers/constraints in a data ADR and reviewed migration design.
3. Freeze sidecar/API schemas and select locked generators through a small parity spike.
4. Generate bindings and add stale-output/fixture tests.
5. Implement SQLite repositories behind application ports and run migration/crash tests.
6. Implement Tauri commands in Phase 2; implement the authenticated HTTP API only in Phase 4A if approved.

Until then, `TASK-P2-001`, `TASK-P2-002`, and `TASK-P4A-005` correctly remain pending behind their phase gates.

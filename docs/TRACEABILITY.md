# Traceability Index

**Status:** Accepted index
**Owner:** Architecture maintainers

This index supplies the required path:

`requirement → owning specification → ADR → audit → contract/schema → test/evidence → delivery phase`

It does not duplicate requirement text or imply that planned evidence exists. Executable units, module ownership, blockers, and current task status are indexed separately in [WORK_BREAKDOWN.md](WORK_BREAKDOWN.md).

| Requirement(s) | Owning specification | ADR | Audit gate | Contract/schema | Planned test/evidence | Phase |
|---|---|---|---|---|---|---|
| `REQ-PROFILE-001`, `REQ-PROFILE-003`, `REQ-PROFILE-006` | [Lifecycle](PROFILE_LIFECYCLE.md), [Operations](OPERATIONS_MODEL.md) | [ADR-0012](adr/0012-supervised-sidecar-process-ownership.md) | `AUD-013`, `AUD-024` | [operation record](../contracts/schemas/operation-record.schema.json), [lifecycle event](../contracts/schemas/lifecycle-event.schema.json), [typed error](../contracts/schemas/typed-error.schema.json) | `AT-P1-005`, `AT-P2-001`, `AT-P2-002` | 1–2 |
| `REQ-PROFILE-002` | [Lifecycle](PROFILE_LIFECYCLE.md), [Sidecar model](SIDECAR_PROCESS_MODEL.md) | [ADR-0004](adr/0004-one-process-per-profile.md), [ADR-0012](adr/0012-supervised-sidecar-process-ownership.md) | `AUD-004`, `AUD-005`, `AUD-014`, `AUD-024` | [sidecar request](../contracts/schemas/sidecar-request.schema.json), [sidecar result](../contracts/schemas/sidecar-result.schema.json) | `AT-P1-002`, `AT-P2-003` | 1–2 |
| `REQ-PROFILE-004` | [Lifecycle](PROFILE_LIFECYCLE.md), [Import/Export](IMPORT_EXPORT.md) | [ADR-0013](adr/0013-identity-preserving-restore-collision-policy.md), [ADR-0017](adr/0017-launchable-steady-state.md) (Proposed) | `AUD-005`, `AUD-013`, `AUD-021`, `AUD-026` | operation and portability schemas | recovery test matrix | 2–3 |
| `REQ-PROFILE-005`, `REQ-IDENTITY-004`, `REQ-IDENTITY-005` | [Fingerprint specification](FINGERPRINT_SPEC.md) | [ADR-0011](adr/0011-semantic-fingerprint-comparison.md) | `AUD-019`, `AUD-022`, `AUD-027`–`AUD-030`, `AUD-032` | [probe](../contracts/schemas/fingerprint-probe.schema.json), [semantic diff](../contracts/schemas/semantic-diff.schema.json) | `AT-P1-003`, `AT-P2-004` | 1–2 |
| `REQ-IDENTITY-001`–`REQ-IDENTITY-003` | [Identity model](IDENTITY_MODEL.md), [Data authority](DATA_AUTHORITY.md) | [ADR-0007](adr/0007-immutable-engine-binding.md), [ADR-0010](adr/0010-deterministic-identity-derivation.md), [ADR-0014](adr/0014-separate-identity-runtime-and-observation-records.md), [ADR-0015](adr/0015-profile-owned-active-core-pointer.md) (Proposed) | `AUD-001`–`AUD-007`, `AUD-022`, `AUD-032` | [identity manifest](../contracts/schemas/identity-manifest.schema.json) | `AT-P1-001`, identity invariant tests | 1–2 |
| `REQ-ENGINE-001`–`REQ-ENGINE-003` | [Engine contract](ENGINE_CONTRACT.md) | [ADR-0003](adr/0003-browser-engine-adapter.md), [ADR-0006](adr/0006-versioned-browser-driver-sidecar.md) | `AUD-012`, `AUD-024`, engine-specific audits | [capabilities](../contracts/schemas/engine-capabilities.schema.json), sidecar schemas | `AT-P1-007`, `AT-P2-005`, `AT-P5-008` | 1–2/5 |
| `REQ-STORAGE-001`, `REQ-STORAGE-003` | [Data authority](DATA_AUTHORITY.md), [Storage](STORAGE_MODEL.md) | [ADR-0014](adr/0014-separate-identity-runtime-and-observation-records.md), [ADR-0015](adr/0015-profile-owned-active-core-pointer.md) (Proposed) | `AUD-009`, `AUD-013`, `AUD-019`, `AUD-020`, `AUD-032` | operation, lifecycle, semantic-diff schemas | repository and activation fault tests | 2/4A |
| `REQ-STORAGE-002`, `SEC-001` | [Security](SECURITY_MODEL.md), [Threat model](THREAT_MODEL.md) | [ADR-0009](adr/0009-encrypted-portability-modes.md) | `AUD-018`, `AUD-026`, `AUD-034` | public portability header only; secret-bearing payload remains separately specified | seeded-secret scan, `AT-P2-007`, `AT-P3-007` | 2–5 |
| `REQ-UPDATE-001` | [Update strategy](UPDATE_STRATEGY.md) | [ADR-0008](adr/0008-staged-core-updates.md) | `AUD-009`, `AUD-015`, `AUD-016`, `AUD-020`, `AUD-023` | operation and semantic-diff schemas | `AT-P4-001`–`AT-P4-004` | 4A |
| `REQ-PORTABILITY-001`–`REQ-PORTABILITY-003` | [Import/Export](IMPORT_EXPORT.md) | [ADR-0009](adr/0009-encrypted-portability-modes.md), [ADR-0013](adr/0013-identity-preserving-restore-collision-policy.md) | `AUD-005`, `AUD-010`, `AUD-021`, `AUD-022`, `AUD-026` | [public header](../contracts/schemas/portability-public-header.schema.json) | `AT-P3-004`–`AT-P3-007` | 3 |
| `REQ-OPERATIONS-001`, `REQ-OPERATIONS-002` | [Operations model](OPERATIONS_MODEL.md) | — | `AUD-013`, `AUD-014`, `AUD-024` | operation, lifecycle, typed-error schemas | `AT-P2-002`, `AT-P4-005` | 2/4A |
| `SEC-002`, `SEC-004`, `INV-002` | [Threat model](THREAT_MODEL.md), [Architecture](ARCHITECTURE.md) | [ADR-0002](adr/0002-tauri-rust-core.md), [ADR-0012](adr/0012-supervised-sidecar-process-ownership.md) | `AUD-024`, `AUD-031`, `AUD-033`, `AUD-034` | sidecar and typed-error schemas | protocol/path/IPC abuse suites | 1–5 |
| `SEC-003` | [Upstream dependencies](UPSTREAM_DEPENDENCIES.md), [Fork strategy](CAMOUFOX_FORK_STRATEGY.md) | [ADR-0008](adr/0008-staged-core-updates.md) | `AUD-015`, `AUD-016`, `AUD-023`, `AUD-031` | upstream lock and patch records | `AT-P1-006`, `AT-P4-001`, `AT-P5-001` | 1–5 |
| `INV-001` | [Architecture](ARCHITECTURE.md), [Repository layout](REPOSITORY_LAYOUT.md) | [ADR-0002](adr/0002-tauri-rust-core.md), [ADR-0003](adr/0003-browser-engine-adapter.md) | — | module APIs and generated bindings after schema acceptance | `AT-P2-008` | 2–5 |
| `INV-003` | [Product scope](PRODUCT_SCOPE.md) | — | — | — | `AT-P5-009` | all |
| `INV-004` | [Documentation governance](DOCUMENTATION_GOVERNANCE.md) | — | all | [audit schema](../audit/schema.json) | `scripts/docs-check.ps1`, evidence review | all |

Phase documents own sequencing only. If a phase document conflicts with an Accepted ADR or owning specification, follow [Documentation Governance](DOCUMENTATION_GOVERNANCE.md) and record the conflict instead of silently choosing a behavior.

# Decision and Requirement Traceability

This index maps the agreed design to its owning specification, ADR, audit gate, and delivery phase. It does not duplicate detailed requirements.

| Agreed item | Owning specification | Decision record | Evidence gate | Delivery |
|---|---|---|---|---|
| Windows-first, local-only, single-user | [Product Scope](PRODUCT_SCOPE.md) | [ADR-0001](adr/0001-local-first.md), [ADR-0005](adr/0005-no-cloud-in-v1.md) | — | All phases |
| Tauri shell, Rust trusted core, React/TypeScript UI | [Architecture](ARCHITECTURE.md) | [ADR-0002](adr/0002-tauri-rust-core.md) | Implementation validation later | Phase 2 |
| Camoufox is first adapter, not a domain dependency | [Engine Contract](ENGINE_CONTRACT.md) | [ADR-0003](adr/0003-browser-engine-adapter.md) | `AUD-001`–`AUD-024` as applicable | Phase 1 decision, Phase 2 implementation |
| One process and data directory per profile | [Profile Lifecycle](PROFILE_LIFECYCLE.md) | [ADR-0004](adr/0004-one-process-per-profile.md) | `AUD-004`, `AUD-005`, `AUD-014` | Phase 2 |
| Stable secret-derived identity across stop/start | [Identity Model](IDENTITY_MODEL.md) | — | `AUD-001`, `AUD-002`, `AUD-003`, `AUD-006`, `AUD-007`, `AUD-019`, `AUD-022` | Phase 1 gate, Phase 2 implementation |
| Language-neutral browser-driver sidecar | [Architecture](ARCHITECTURE.md), [Engine Contract](ENGINE_CONTRACT.md) | [ADR-0006](adr/0006-versioned-browser-driver-sidecar.md) | `AUD-012`, `AUD-024` | Phase 1 decision, Phase 2 implementation |
| Immutable engine binding | [Identity Model](IDENTITY_MODEL.md) | [ADR-0007](adr/0007-immutable-engine-binding.md) | `AUD-025` for future adapter | All phases |
| Third-party proxy per profile | [Product Scope](PRODUCT_SCOPE.md) | — | `AUD-008` | Phase 2/3 |
| Safe snapshots and crash reconciliation | [Storage Model](STORAGE_MODEL.md), [Profile Lifecycle](PROFILE_LIFECYCLE.md) | — | `AUD-005`, `AUD-013` | Phase 2/3 |
| Three encrypted portability modes | [Import/Export](IMPORT_EXPORT.md) | [ADR-0009](adr/0009-encrypted-portability-modes.md) | `AUD-010`, `AUD-021`, `AUD-022` | Phase 3 |
| Side-by-side core update with canary and rollback | [Update Strategy](UPDATE_STRATEGY.md) | [ADR-0008](adr/0008-staged-core-updates.md) | `AUD-009`, `AUD-016`, `AUD-020` | Phase 4 |
| Local authenticated automation API | [Security Model](SECURITY_MODEL.md), [Engine Contract](ENGINE_CONTRACT.md) | — | `AUD-018`, `AUD-024` | Phase 4 |
| Firefox extensions only unless proven compatible | [Product Scope](PRODUCT_SCOPE.md) | [ADR-0007](adr/0007-immutable-engine-binding.md) | `AUD-011` | Phase 3 |
| Future Chromium support via a new adapter/profile | [Architecture](ARCHITECTURE.md) | [ADR-0003](adr/0003-browser-engine-adapter.md), [ADR-0007](adr/0007-immutable-engine-binding.md) | `AUD-025` | Phase 5 spike |
| No undetectable/unlinkable claim | [Product Scope](PRODUCT_SCOPE.md) | — | Continuous validation of product claims | All phases |

Detailed delivery and acceptance criteria are maintained in the [five phase specifications](phases/README.md). Phase documents schedule work but do not override the owning specification, ADR, or audit evidence state.

## Source status

The source conversation was used to recover agreed product and architectural decisions. Its earlier repository research is not treated as retained audit evidence. Technical claims become authoritative only through the evidence workflow in [AUDIT_REGISTER.md](AUDIT_REGISTER.md).

# Feature Disposition Matrix

## Purpose

This matrix records whether product ideas discussed during planning are committed, conditional, deferred, or rejected. It prevents a named capability from becoming an implicit requirement merely because it appeared in a comparison or conversation. Detailed behavior remains in the owning specification.

| Disposition | Meaning |
|---|---|
| Planned | Included in the stated phase, subject to its entry and exit gates |
| Conditional | Included only if the cited audit/capability decision supports it |
| Deferred | Not committed to Phases 1–5; requires later scope and acceptance criteria |
| Rejected v1 | Explicitly outside the local-first Version 1 boundary |
| Rejected | Incompatible with the product's stated assurance boundary |

## Catalogue and profile experience

| Capability | Disposition | Phase / owner | Boundary |
|---|---|---|---|
| Profile create, inspect, edit allowed metadata, archive, delete, recover | Planned | Phase 2; [Product Scope](PRODUCT_SCOPE.md) | Identity-bearing fields remain immutable |
| Search, sort, filter, folders, tags, notes, status | Planned | Phase 2 | Presentation details remain product-design work |
| Generic profile clone | Rejected v1 | [Import/Export](IMPORT_EXPORT.md) | Ambiguous identity semantics are not allowed |
| Duplicate as new profile | Planned | Phase 3 | New ID, secret, identity, baseline, and data directory |
| Backup and Transfer | Conditional | Phase 3; `AUD-010`, `AUD-021`, `AUD-022`, `AUD-026` | Only within an evidence-backed fidelity envelope |
| Default profile settings/templates | Planned | Phase 2 | Templates may set non-secret policy/preset choices but never reuse IDs, secrets, seeds, or accepted baselines |
| Start page / startup URL settings | Planned | Phase 2 profile configuration | Must not bypass lifecycle or become an automation scheduler |
| Dedicated bookmark manager/editor | Deferred | Later product decision | Phase 3 may preserve/copy supported bookmark state without promising a full manager |
| CSV metadata/config import and export | Deferred | Candidate Phase 4 bulk extension | May not carry identity secrets, credentials, cookies, or raw browser state |

## Browser state, identity, and extensions

| Capability | Disposition | Phase / owner | Boundary |
|---|---|---|---|
| Stable secret-derived configured identity | Conditional | Phase 1 evidence, Phase 2 implementation | `AUD-001`–`AUD-007`, `AUD-019`, `AUD-022` |
| Semantic fingerprint preflight | Conditional | Phase 1/2 | Policy requires evidence; no byte-equality promise |
| Cookie view/import/export/delete | Conditional | Phase 3 | Supported formats/fields only; no live DB edits |
| LocalStorage/IndexedDB/history/session preservation | Conditional | Phase 3 | Per-type `AUD-005`/`AUD-026` support matrix |
| Firefox-compatible extension management | Conditional | Phase 3; `AUD-011` | Per-profile isolation and permission visibility |
| Bundled/default extensions | Conditional | Phase 3 may approve through explicit support policy | Nothing is silently installed; every default requires compatibility, security, and fingerprint review |
| Chrome Web Store / Chrome-only extensions | Rejected v1 | Product scope | Requires a future Chromium path |
| Saved-password/authenticated-session export | Conditional | Phase 3; `AUD-026` | Rejected by default; opaque raw state is treated as sensitive until classified |

## Network, automation, and operations

| Capability | Disposition | Phase / owner | Boundary |
|---|---|---|---|
| Third-party HTTP/HTTPS/SOCKS proxy assignment and tests | Conditional | Phase 2/3; `AUD-008` | No owned proxy network; fail closed for approved strict modes |
| Proxy marketplace/network, traffic billing, phone proxy devices | Rejected v1 | Product scope | Separate service/backend product |
| Browser-core pinning, qualification, staged update, rollback | Planned | Phase 4 | Evidence-backed core-pair rules |
| Bulk lifecycle and safe metadata/config operations | Planned | Phase 4 | Per-profile results; not a cross-process atomic transaction |
| Local authenticated REST API | Planned | Phase 4 | Loopback by default; application use cases only |
| Human typing and Cookie Bot | Conditional | Phase 4B; `DEC-PHASE4B-001` | Optional functional experiments, not an anti-detection guarantee; do not block Phase 4A or Phase 5 |
| Run with Sync | Conditional | Phase 4B optional prototype; `DEC-PHASE4B-001` | May be rejected or remain deferred without blocking the mandatory roadmap |
| Node SDK | Deferred | After stable local API | REST API is the integration contract; no SDK commitment |
| Python SDK | Deferred | After stable local API | REST API is the integration contract; no SDK commitment |
| Selenium support | Deferred | Future engine/automation capability review | Playwright sidecar is the planned initial automation path |
| Direct raw Playwright access from API/UI | Rejected v1 | Architecture/security | Must go through bounded application use cases |

## Platform and collaboration

| Capability | Disposition | Phase / owner | Boundary |
|---|---|---|---|
| Windows desktop, local-only, single user | Planned | All phases | Initial supported product |
| Chromium adapter | Conditional | Phase 5 spike; `AUD-025` | New profile/identity; no in-place conversion |
| Cloud sync, remote browser execution | Rejected v1 | [ADR-0005](adr/0005-no-cloud-in-v1.md) | Separate architecture and threat model |
| Team/workspace/RBAC/sharing | Rejected v1 | [ADR-0005](adr/0005-no-cloud-in-v1.md) | No hidden backend requirement |
| Mobile/Android execution | Rejected v1 | Product scope | Separate mobile/backend product |
| “Undetectable” or “unlinkable” guarantee | Rejected | Product claims | Only browser-level isolation and measured consistency may be claimed |

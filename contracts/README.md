# Contract Schemas

- Status: Proposed drafts
- Owner: Engine contract and application boundary
- Last reviewed: 2026-09-28
- Review trigger: `AUD-012`/`AUD-024` decision or any wire/domain contract change

## Purpose and evidence boundary

`contracts/schemas` contains language-neutral JSON Schema drafts for Phase 1 review and future generated bindings. They define desired data shape, validation, limits, and failure semantics. They do **not** prove that Camoufox, a launcher, Playwright, Windows transport, or a future adapter implements the behavior.

## Schemas

| Schema | Purpose | Sensitive-data policy |
|---|---|---|
| `identity-manifest.schema.json` | Immutable identity lineage/derivation inputs and compatibility constraints | Secret reference only; no plaintext secret |
| `engine-capabilities.schema.json` | Versioned granular capability report | No credentials or profile data |
| `sidecar-request.schema.json` | Common sidecar request envelope | Non-secret references only; payload must follow operation-specific schema before acceptance |
| `sidecar-result.schema.json` | Outcome-aware response envelope | Safe diagnostics only |
| `typed-error.schema.json` | Machine-readable error contract | Redacted/safe message; no raw logs/secrets |
| `lifecycle-event.schema.json` | Versioned lifecycle/process events | Redacted details only |
| `operation-record.schema.json` | Durable operation state and reconciliation metadata | Opaque references; no secret value |
| `fingerprint-probe.schema.json` | Normalized probe result and coverage context | No raw secret/seed; raw artifacts remain evidence-controlled |
| `semantic-diff.schema.json` | Field-level semantic comparison | Normalized/redacted values only |
| `portability-public-header.schema.json` | Bounded unauthenticated container header | No profile name, credential, secret, URL, or content inventory before authentication |

## Compatibility policy

- Every document carries `schemaVersion`; protocol envelopes also carry `protocolVersion`.
- Schema versions use semantic-version strings. A breaking field/meaning/requiredness change increments the major version and requires compatibility review.
- Unknown top-level fields are rejected (`additionalProperties: false`) unless an explicitly versioned extension map says otherwise.
- Senders do not assume readers ignore unknown fields. Version/capability negotiation occurs before effect.
- Enums are closed per schema version. A new enum value is incompatible unless negotiation declares support.
- Size constraints are security requirements and may become stricter through a versioned policy; implementations must also apply transport/container total-size limits.
- Timestamps are UTC RFC 3339/JSON Schema `date-time`; IDs use UUID where the draft requires it.
- `$id` uses repository-local URNs and does not imply a hosted schema registry.
- Cross-schema references are relative files and must resolve in `docs-check`.

## Sensitive annotations

`x-sensitive` is a documentation annotation. `true` means the field is sensitive even if it contains an opaque handle; `"reference-only"` means plaintext material is forbidden. Schemas intentionally contain no real or example secret. Generated code must not derive logging/serialization permission from schema presence.

## Binding generation

When bindings exist, schemas remain authoritative for wire shape. Generation is deterministic, outputs live under an explicit `generated/` directory, generated files contain a do-not-edit header, and `docs-check`/CI verifies synchronization. No binding is generated in Phase 1 documentation work.


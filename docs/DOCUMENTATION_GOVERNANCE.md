# Documentation Governance

- Status: Accepted
- Owner: Repository maintainers
- Last reviewed: 2026-09-29
- Next review: Before any Phase 2 scaffold or after a governing decision changes

## Purpose

This document defines where authoritative information lives, how conflicts are resolved, and how documentation changes are reviewed. It governs documentation structure; it does not provide Camoufox capability evidence.

## Authority map

| Information class | Authoritative location | Supporting material |
|---|---|---|
| Product boundary and non-goals | [PRODUCT_SCOPE.md](PRODUCT_SCOPE.md) | [FEATURE_MATRIX.md](FEATURE_MATRIX.md) |
| Stable normative requirement IDs | [REQUIREMENTS.md](REQUIREMENTS.md) | [TRACEABILITY.md](TRACEABILITY.md) |
| Accepted architecture decisions | [Accepted ADRs](adr/) | [ARCHITECTURE.md](ARCHITECTURE.md), [MODULE_BOUNDARIES.md](MODULE_BOUNDARIES.md) |
| Pending product/architecture choices | [DECISIONS_REQUIRED.md](DECISIONS_REQUIRED.md) and Proposed ADRs | Options in owning specifications |
| Logical data authority | [DATA_AUTHORITY.md](DATA_AUTHORITY.md) | [STORAGE_MODEL.md](STORAGE_MODEL.md), [IDENTITY_MODEL.md](IDENTITY_MODEL.md) |
| Lifecycle and operation behavior | [PROFILE_LIFECYCLE.md](PROFILE_LIFECYCLE.md), [OPERATIONS_MODEL.md](OPERATIONS_MODEL.md) | [SIDECAR_PROCESS_MODEL.md](SIDECAR_PROCESS_MODEL.md) |
| Engine behavior contract | [ENGINE_CONTRACT.md](ENGINE_CONTRACT.md) and [contract schemas](../contracts/README.md) | Adapter-specific qualification evidence |
| Security policy and threats | [SECURITY_MODEL.md](SECURITY_MODEL.md), [THREAT_MODEL.md](THREAT_MODEL.md) | Audit evidence and test reports |
| Proposed Windows process/secret/IPC mechanisms | [WINDOWS_SECURITY_BOUNDARIES.md](WINDOWS_SECURITY_BOUNDARIES.md) | `AUD-024`, `AUD-031`, `AUD-033`, `AUD-034` evidence |
| Physical schema/API/binding readiness | [PHYSICAL_SCHEMA_API_BINDINGS.md](PHYSICAL_SCHEMA_API_BINDINGS.md) | Data/API decisions and accepted contract schemas |
| Technical uncertainty and evidence status | [AUDIT_REGISTER.md](AUDIT_REGISTER.md) | [research/camoufox](../research/camoufox/README.md), audit reports |
| Delivery order, gates, and handoff | [DEVELOPMENT_PHASES.md](DEVELOPMENT_PHASES.md), [phase specifications](phases/README.md) | Requirement and audit links |
| Executable task breakdown and task status | [WORK_BREAKDOWN.md](WORK_BREAKDOWN.md) | Phase specifications and acceptance evidence |
| Upstream selection and dependency state | [UPSTREAM_DEPENDENCIES.md](UPSTREAM_DEPENDENCIES.md), `research/camoufox/UPSTREAM_LOCK.json` | Evidence records |
| Terminology | [GLOSSARY.md](GLOSSARY.md) | Owning specifications |

## Precedence

When documents conflict, apply this order:

1. Explicit current user direction that does not silently rewrite an existing Accepted decision.
2. Accepted, non-superseded ADRs for architecture decisions.
3. Product scope and feature disposition for inclusion/exclusion.
4. Requirement catalogue for normative IDs and concise statements.
5. Owning specifications listed above.
6. Phase documents for sequencing only.
7. Research notes and templates, which are never product truth by themselves.

The Audit Register has exclusive authority over evidence status. An Accepted ADR may describe an intended architecture while its feasibility remains unverified in an `AUD-*` item.

If a new recommendation conflicts with an Accepted ADR, create a Proposed superseding ADR and keep the Accepted decision effective until approval. Do not edit the old ADR to make the change appear historical.

## Document status

| Status | Meaning | May be implemented? |
|---|---|---|
| `Draft` | Incomplete working material; not a decision | No |
| `Proposed` | Reviewable recommendation awaiting approval or evidence | Only as an explicitly authorized spike |
| `Accepted` | Approved policy or design, subject to named audit gates | Yes, in the authorized phase |
| `Superseded` | Replaced by a named Accepted document/ADR | No new implementation |
| `Unverified` | Candidate matrix or upstream fact awaiting evidence | No support claim |

Every new governing document records status, owner, last-reviewed date, and a review trigger/date. Existing documents may inherit ownership from this registry until headers are added.

## Change rules

- Product scope changes update `PRODUCT_SCOPE.md`, `FEATURE_MATRIX.md`, requirements, and affected phases.
- Architecture changes require a new ADR; Accepted ADRs are immutable except for typo/link corrections and status/supersession metadata.
- Runtime or upstream uncertainty creates or updates an `AUD-*` item using the next ID.
- Contract changes update the owning prose specification and JSON Schema in the same change. Generated bindings, once introduced, are regenerated rather than edited.
- Requirement changes preserve IDs. A removed requirement becomes `Superseded` or `Rejected` with a replacement/reason; its ID is not reused.
- Audit IDs, evidence IDs, environment IDs, operation IDs, and decision IDs are never renumbered after publication.
- Phase documents own entry/exit gates, sequencing, deliverables, and handoff. They link to—rather than redefine—business invariants.
- The work-breakdown register owns `TASK-*` status. A task status never changes an audit status or phase gate by implication.
- Claims about Camoufox remain hypotheses until the Audit Register links sufficient source or test evidence.

## Generated files

No tracked file is generated at present. `docs/AUDIT_REGISTER.md` remains the hand-maintained source of truth until the migration in [audit/README.md](../audit/README.md) completes atomically.

When generation is introduced:

- generated files must contain a visible `GENERATED — DO NOT EDIT` header;
- their source schema/items and deterministic generator are committed together;
- checks must fail when generated output is stale;
- generated contract bindings live in an explicitly named `generated/` path and are never edited directly.

## Review workflow

1. Identify current phase and governing documents.
2. Name affected `REQ-*`, `INV-*`, `SEC-*`, `ADR-*`, `AUD-*`, and `DEC-*` IDs.
3. Separate facts, hypotheses, recommendations, and decisions.
4. Update the owning document; use links elsewhere.
5. Run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/docs-check.ps1`.
6. Record unresolved decisions in `DECISIONS_REQUIRED.md` and runtime uncertainty in the Audit Register.
7. Review documentation at each phase entry/exit, before a contract version changes, and whenever an upstream lock changes.

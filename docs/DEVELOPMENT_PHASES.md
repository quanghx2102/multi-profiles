# Development Roadmap and Phase Governance

## Purpose

This document defines how the five phases are sequenced and governed. Detailed execution specifications live in [`phases/`](phases/README.md). Product boundaries remain in [PRODUCT_SCOPE.md](PRODUCT_SCOPE.md), technical uncertainty in [AUDIT_REGISTER.md](AUDIT_REGISTER.md), and accepted architectural choices in [`adr/`](adr/).

The roadmap is a decision framework, not a calendar estimate. A phase advances because its evidence and acceptance gates are satisfied, not because a target date arrives.

## Current state

- Active phase: **Phase 1 — Audit and Technical Spike**.
- Completed within Phase 1: documentation baseline and initial audit register.
- Not yet performed: Camoufox source audit, technical experiments, dependency installation, application scaffolding, or browser builds.
- All initial audit items remain `NOT_STARTED` with hypothesis-level evidence.

## Phase map

| Phase | Outcome | Detail | Principal gates |
|---|---|---|---|
| 1 | Evidence-backed Camoufox and architecture go/no-go | [Phase 1 specification](phases/PHASE_1_AUDIT_AND_TECHNICAL_SPIKE.md) | Phase 2 blockers in the audit register |
| 2 | Safe local desktop MVP for profile lifecycle | [Phase 2 specification](phases/PHASE_2_LOCAL_DESKTOP_MVP.md) | Qualified engine/sidecar, deterministic identity, isolation, crash recovery |
| 3 | Recoverable data and encrypted portability | [Phase 3 specification](phases/PHASE_3_DATA_SAFETY_AND_PORTABILITY.md) | Snapshot consistency, portability, extension and key-management decisions |
| 4 | Staged core updates, automation, and bulk operations | [Phase 4 specification](phases/PHASE_4_CORE_UPDATE_AUTOMATION_AND_BULK.md) | Migration/rollback, supply-chain trust, local API security |
| 5 | Production hardening and engine-extensibility decision | [Phase 5 specification](phases/PHASE_5_PRODUCTION_HARDENING_AND_EXTENSIBILITY.md) | Release security, Windows distribution, operational evidence, Chromium spike |

## Sequencing rules

- A later phase may perform documentation or research early, but it may not ship production behavior that assumes an unresolved blocking audit.
- Phase 2 is the first phase authorized to scaffold or implement production application code, and only after a Phase 1 go decision.
- Each phase inherits all accepted invariants and security boundaries from earlier phases.
- A deferred capability stays unavailable; it must not be represented by a silent fallback or placeholder success response.
- A phase may be split into increments, but the phase exit gate applies to the combined outcome.

## Phase states

| State | Meaning |
|---|---|
| `PLANNED` | Scope and gates are documented; execution has not begun. |
| `ACTIVE` | Authorized work is in progress and evidence is being recorded. |
| `GATED` | Work cannot safely advance until named audit or decision conditions are satisfied. |
| `EXIT_REVIEW` | Deliverables exist and are undergoing gate review. |
| `COMPLETE` | Exit criteria and handoff package have been accepted. |
| `STOPPED` | A no-go decision ended this path; alternatives require a new or superseding roadmap decision. |

Current roadmap state: Phase 1 is `ACTIVE` for documentation and `GATED` for conclusions until audit work is authorized and completed; Phases 2–5 are `PLANNED`.

## Common entry requirements

Before a phase becomes `ACTIVE`:

- its predecessor's exit decision is recorded;
- blocking audits have an allowed terminal decision with sufficient evidence;
- required ADRs are accepted or explicitly superseded;
- supported environment and artifact revisions are pinned;
- test fixtures and secret-handling rules are defined;
- destructive or irreversible workflows have a recovery plan.

## Common definition of done

A phase is not complete merely because features exist. It also requires:

- acceptance scenarios pass on the supported environment matrix;
- failure and recovery paths are exercised;
- security boundaries and redaction rules are tested;
- documentation, contracts, and ADRs match implemented behavior;
- unresolved findings are recorded in the audit register with owners and phase impact;
- no critical issue is silently deferred;
- the next phase receives a versioned handoff package.

## Gate decisions

A phase exit review produces one of:

- **GO:** all mandatory criteria pass.
- **CONDITIONAL GO:** only bounded, explicitly owned risks remain; mitigations and regression tests are recorded.
- **HOLD:** more evidence or remediation is required.
- **NO-GO:** the selected technical or product path is rejected.

`ACCEPTED_RISK` requires a named decision owner, rationale, mitigation, monitoring or regression coverage, and review date. It is not equivalent to `CONFIRMED`.

## Change control

- Product-scope changes update [PRODUCT_SCOPE.md](PRODUCT_SCOPE.md).
- Architecture changes require a new or superseding ADR.
- New runtime uncertainty creates or updates an `AUD-*` item.
- Phase ownership or sequencing changes update this roadmap and the affected phase specification.
- Acceptance criteria may become stricter without an ADR; weakening a safety invariant requires an ADR and explicit risk review.

## Cross-phase quality threads

Identity integrity, profile isolation, crash consistency, supply-chain trust, secret containment, diagnostics, and test reproducibility are continuous threads. They do not become “finished” in one phase; each later phase must demonstrate that new capabilities preserve them.


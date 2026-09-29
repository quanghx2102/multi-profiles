# Documentation Review and Rationalization

- Status: Accepted review record
- Owner: Repository maintainers
- Review date: 2026-09-29
- Review trigger: Phase 1 exit review or a material scope/architecture change

## Review boundary

This review evaluates internal consistency, scope discipline, module ownership, evidence honesty, and readiness to break work into phases. It is not Camoufox source or runtime evidence. All Camoufox feasibility claims remain controlled by `AUD-001`–`AUD-034`.

## Overall assessment

The documentation has a sound safety-oriented architecture: local-first scope, inward dependencies, explicit data authority, immutable profile identity, typed engine capabilities, durable operations, strict process ownership, and evidence-gated Camoufox claims. It is suitable for Phase 1 audit preparation, but it is not yet authorization to build the application.

The main execution problem was not missing feature prose; it was the absence of a single task-status authority. The phase specifications described substantial work, but did not answer which unit was pending, blocked, complete, or optional. [WORK_BREAKDOWN.md](WORK_BREAKDOWN.md) now provides that index without making phase documents or the audit register compete for authority.

## Findings and applied resolutions

| Finding | Risk | Resolution |
|---|---|---|
| Phase work had no stable task IDs or task-level state. | Progress could be inferred differently from prose; documentation completion could be mistaken for runtime completion. | Added `TASK-*` register with status, module, dependency, functional outcome, and completion evidence. |
| Sidecar topology options described “one sidecar per profile” and “common Rust supervisor plus isolated worker per profile” as separate choices, although ADR-0012 already requires the common Rust supervisor. | The spike could compare duplicate options or accidentally create a second process authority. | Clarified the real third option as a shared sidecar coordinator with isolated workers; changed the recommendation to the simpler dedicated worker/profile topology, still pending `AUD-024` and user approval. |
| Phase 4B was optional in scope and gating but Human Typing/Cookie Bot appeared as an unconditional deliverable and `Planned` feature. | Optional experiments could silently become release blockers and expand scope. | Reclassified them as conditional, made Phase 4B deliverables conditional, and added `DEC-PHASE4B-001`; all Phase 4B tasks are deferred by default. |
| Phase 1 contains both Phase-2-blocking work and forward-looking audits. | Later portability/API/release/Chromium research could delay the MVP gate or appear mandatory. | The task register separates mandatory Phase 2 evidence from non-blocking `TASK-P1-011`. Existing audit block phases remain authoritative. |
| Proposed decisions are referenced by detailed target behavior. | An implementer could code the recommendation as if approved. | Tasks that depend on ADR-0015/0016/0017 or profile/API/portability choices are explicitly blocked or pending behind `DEC-*` gates. No Proposed ADR was marked Accepted. |
| The identity prose placed a `user_data_dir` reference in the immutable manifest while the canonical draft schema omitted it and portability may relocate physical storage. | A host path could become false identity truth or conflict with import/recovery. | Moved the logical directory binding to profile/storage authority, kept concrete path resolution in the filesystem adapter, and clarified that relocation is journaled rather than an identity mutation. |
| Specifications repeat some behavior across scope, phase, and module documents. | Editing all copies can create drift. | No large rewrite was performed. Authority links remain primary; the new task register states outcomes and evidence only, and does not redefine state machines or data schemas. |

## Scope disposition

### Retain

- Phase 2: profile catalogue, deterministic identity, isolated launch/stop/recovery, preflight, approved proxy modes, and safe diagnostics. These are the minimum system proof, not optional polish.
- Phase 3: snapshots and encrypted portability remain separate because recovery fidelity and identity-copy semantics are different safety problems.
- Phase 4A: staged core updates, rollback, bounded bulk operations, authenticated local API, and policy-bound automation lease remain later work. They must not enter the MVP early.
- Phase 5: release security, diagnostics, resource admission, and upstream maintenance are required before calling the application production-ready.

### Conditional or deferred

- Human Typing, Cookie Bot, and Run with Sync are Phase 4B experiments and are deferred until explicitly activated by `DEC-PHASE4B-001`.
- The Chromium adapter is only a Phase 5 spike under `AUD-025`, not a promised second production engine.
- SDKs, bookmark manager, CSV exchange, Selenium support, cloud/team/mobile behavior, and a proxy network retain their existing Deferred or Rejected v1 disposition.

### Removed or simplified

- No accepted product capability was deleted without a scope decision.
- Duplicate sidecar topology wording was removed; this changes a Proposed recommendation, not an Accepted architecture decision.
- Unconditional Phase 4B delivery wording was removed. Optional experiments no longer block the mandatory roadmap.
- No production module or speculative feature was added by this review.

## Open decisions that still block work

| Decision | Required before | Current risk if unresolved |
|---|---|---|
| `DEC-UPSTREAM-001`, `DEC-LICENSE-001`, `DEC-EVIDENCE-001` | Executing/retaining Phase 1 evidence and distribution conclusions | Unverifiable inputs, unusable evidence, or invalid distribution assumptions. |
| `DEC-DATA-001`, `DEC-LIFECYCLE-001`, `DEC-PROFILE-001`, `DEC-SIDECAR-001` | Phase 2 schema and scaffold | Competing authorities, inconsistent states, destructive ambiguity, or unsafe process topology. |
| `DEC-PORTABILITY-001` | Phase 3 container/data-mode implementation | Secret leakage or fidelity claims that cannot be met. |
| `DEC-API-001` | Phase 4A local API | Unsafe default exposure or inconsistent UX. |
| `DEC-PHASE4B-001` | Any Phase 4B experiment | Optional behavior consumes delivery capacity or increases correlation/security risk without product approval. |

## Residual technical risks

| Risk | Why it remains | Containment |
|---|---|---|
| Camoufox may not meet deterministic identity or cross-context requirements. | No source/runtime audit exists. | Fail Phase 1 gate or constrain/reject unsupported capability; never add random fallback. |
| Safe browser-state checkpoint and selective secret/session exclusion may be impossible. | Firefox/Camoufox state dependencies are unverified. | Keep Phase 3 blocked on `AUD-005`, `AUD-013`, `AUD-026`; label opaque state sensitive. |
| Sidecar/browser adoption and termination may be unsafe on Windows. | The concrete ownership primitive and crash behavior are unknown. | `AUD-024` plus `AUD-031`; never trust PID alone. |
| Preflight can become stale after launch. | Display, proxy, GPU, extension, sleep, and other events may change observations. | `AUD-032` must define validity generations, revalidation triggers, and containment. |
| Scope remains large after the MVP. | Portability, updater, API/automation, and production release each add major attack surfaces. | Enforce phase gates; do not run Phase 4B by default; treat later phases as separately accepted increments. |
| Same-user malware remains outside full protection. | Local ACL/keychain/loopback controls cannot defeat an equivalently privileged hostile process. | Minimize secret exposure and state the residual boundary under `AUD-034`; do not claim complete local secrecy. |

## Recommended next action

Do not scaffold production code yet. Resolve the Phase 1 input/ownership decisions, authorize `TASK-P1-003`, pin immutable inputs, then execute the fail-fast provenance/license work before expensive behavioral experiments. Stop or hold immediately if distribution, artifact trust, or maintenance viability fails.

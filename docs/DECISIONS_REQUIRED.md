# Decisions Required

- Status: Proposed register
- Owner: Product and architecture decision owners
- Last reviewed: 2026-09-29
- Review trigger: Any decision resolution or phase gate review

## Rules

Items remain `Pending user approval` until the user/authorized owner records a choice and, where architectural, accepts the linked ADR. A recommendation is not an Accepted decision. Runtime feasibility still requires audit evidence after approval.

| ID | Decision | Context and options | Recommended option | Trade-offs | Blocks | Status |
|---|---|---|---|---|---|---|
| `DEC-DATA-001` | Authoritative `activeCoreId` location | A: runtime configuration under ADR-0014; B: profile metadata; C: duplicate with reconciliation | B, paired atomically with `acceptedBaselineId`; [ADR-0015](adr/0015-profile-owned-active-core-pointer.md) | Clear aggregate transaction vs changing accepted storage placement | Phase 2 schema/scaffold | Pending user approval |
| `DEC-LIFECYCLE-001` | `READY` versus `STOPPED` | A: keep both with distinct provenance; B: one launchable steady state plus `lastStopDisposition`; C: READY only before first run | B; [ADR-0017](adr/0017-launchable-steady-state.md) | Simpler invariants vs migration/UI change from current vocabulary | Phase 2 lifecycle schema | Pending user approval |
| `DEC-PROFILE-001` | Archive/delete/purge semantics | A: archive only; B: archive + trash retention + explicit purge; C: immediate deletion | B, with no generic “restore” verb | Recovery safety and storage cost vs UX complexity | Phase 2 catalogue semantics | Pending user approval |
| `DEC-SIDECAR-001` | Sidecar process topology | A: one dedicated sidecar worker/profile under the Rust supervisor; B: one shared multi-profile sidecar; C: shared sidecar coordinator + isolated worker/profile | A for the simplest authority and failure boundary, subject to `AUD-024`; [ADR-0016](adr/0016-sidecar-topology.md) | Strong isolation and simpler recovery vs per-profile runtime overhead | Phase 2 sidecar scaffold | Pending user approval and spike evidence |
| `DEC-PORTABILITY-001` | Session-bearing data defaults | A: sensitive full-state default; B: sanitized default; C: separate explicit variants | C, retaining ADR-0009 default exclusion where safe; exact matrix awaits `AUD-026` | Recovery fidelity vs credential/session leakage and selective-copy feasibility | Phase 3 portability | Pending user approval and audit evidence |
| `DEC-API-001` | Local API default enablement | A: enabled loopback; B: disabled until user enables; C: no API in v1 | B | Safer default vs setup friction | Phase 4A API | Pending user approval |
| `DEC-UPSTREAM-001` | Exact Camoufox revision/artifacts | Select commit/tag/release, launcher, Firefox base, generator deps, Windows artifact/hash | Fail-fast provenance/license/sustainability workstream, then choose immutable inputs | Newest release vs stability/security/patch risk | Phase 1 execution and Phase 2 gate | Pending audit selection |
| `DEC-LICENSE-001` | Project license | Choose project license and contribution policy separately from third-party obligations | Obtain owner/legal review before public distribution; do not infer from Camoufox | Openness/reuse/contribution goals and compatibility obligations | Distribution; preferably before Phase 2 collaboration | Pending user approval |
| `DEC-EVIDENCE-001` | Evidence artifact storage | A: Git for small redacted evidence; B: external immutable store; C: hybrid | C: Git manifests/reports, external large/sensitive raw artifacts with hashes/access policy | Reproducibility vs repository size and secret/privacy risk | Phase 1 audit execution | Pending user approval |
| `DEC-PHASE4B-001` | Activate optional Phase 4B experiments | A: defer all; B: select individual Human Typing/Cookie Bot/Run with Sync experiments after Phase 4A evidence; C: reject all for this roadmap | A now; reconsider individual experiments only after Phase 4A safety/resource evidence | Product value and learning vs scope, correlation, security, and support cost | Phase 4B only; does not block Phase 4A or Phase 5 | Pending future product approval |

## Resolution record

When resolved, record selected option, approver, date, rationale, affected ADR/requirements/audits, and required migration. Do not delete the row or reuse its ID.

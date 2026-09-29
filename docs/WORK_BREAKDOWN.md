# Phase Work Breakdown and Progress Register

- Status: Accepted execution index; task completion still requires the evidence named below
- Owner: Product and engineering leads
- Last reviewed: 2026-09-29
- Review trigger: Task-state, phase-gate, scope, requirement, audit, or architecture change

## Purpose

This register turns the governing specifications into executable work without redefining them. Phase documents own scope, sequence, and gates; [Requirements](REQUIREMENTS.md) own normative behavior; the [Audit Register](AUDIT_REGISTER.md) owns evidence status; Accepted ADRs own architecture decisions. This file alone owns `TASK-*` execution status.

## Status rules

| Status | Meaning |
|---|---|
| `PENDING` | In scope, but work has not started; normal predecessor gates may still be outstanding. |
| `IN_PROGRESS` | Authorized work is active and has an owner. |
| `BLOCKED` | A named decision, audit result, input, or predecessor prevents safe progress. |
| `COMPLETE` | The acceptance condition is met and its evidence is linked or named. |
| `DEFERRED` | Deliberately outside the active delivery track; reactivation requires the named decision. |
| `CANCELLED` | Removed by an explicit scope/architecture decision; the task ID is retained. |

A task is never `COMPLETE` because prose or scaffolding exists. Runtime tasks require tests/evidence at the quality required by the owning audit or phase. Changing a task status does not change an `AUD-*` status, accept an ADR, or pass a phase gate.

## Current phase and gate

- Active phase: **Phase 1 — Audit and Technical Spike**.
- Current state: Phase 1 source/runtime work is authorized and active. The beta.31 candidate and a Windows 10 smoke environment are pinned, but distribution is on hold for the bundled-font license finding and mandatory multi-environment/integration evidence remains incomplete.
- Phase 2 entry: prohibited until Phase 1 records `GO` or an acceptable `CONDITIONAL GO` and every mandatory Phase 2 audit has an allowed evidence-backed outcome.
- Production source directories and dependencies remain out of scope in the current phase.

## Module delivery order

Implementation follows the dependency direction in [Module Boundaries](MODULE_BOUNDARIES.md) and the physical target in [Repository Layout](REPOSITORY_LAYOUT.md):

```text
domain / engine-contract / operations
                ↓
            application
                ↓
adapters (storage, filesystem, keychain, process, engine)
                ↓
composition roots (desktop core and sidecar)
                ↓
desktop UI and local API presentation
```

An adapter task may prepare test doubles early, but it may not move policy into the adapter or bypass a public port. Cross-module behavior is accepted through contracts and integration tests, not deep imports.

## Phase 1 — evidence and go/no-go

Detailed procedures live in the [Phase 1 specification](phases/PHASE_1_AUDIT_AND_TECHNICAL_SPIKE.md) and [Camoufox Audit Plan](../research/camoufox/AUDIT_PLAN.md).

| Task | Status | Functional requirement / output | Dependencies and gates | Owning modules/documents | Completion evidence |
|---|---|---|---|---|---|
| `TASK-P1-001` | `COMPLETE` | Establish product boundary, requirements, module ownership, security model, phase gates, ADRs, and evidence rules without asserting unverified Camoufox behavior. | `INV-001`–`INV-004`; no runtime conclusion. | Documentation authorities | Governing documents exist; `scripts/docs-check.ps1` passes. |
| `TASK-P1-002` | `COMPLETE` | Establish the 34-item audit register, fail-fast plan, evidence templates, draft schemas, and empty research indexes. | `INV-004`; `DEC-EVIDENCE-001` remains pending for long-term storage. | Audit/research/contracts documentation | `AUD-001`–`AUD-034` are defined and all remain evidence-honest. |
| `TASK-P1-003` | `IN_PROGRESS` | Select exact Camoufox, launcher, Firefox base, generator/runtime dependencies, Windows artifact, hashes, and candidate environments. | User authorization; this task resolves `DEC-UPSTREAM-001`; no floating revision. | Upstream/audit workstream | Candidate `UPSTREAM_LOCK.json` and `ENV-WIN10-SMOKE-01` exist; transitive/source mapping and review remain. |
| `TASK-P1-004` | `IN_PROGRESS` | Verify source/artifact provenance, distribution obligations, integrity chain, and executable-loading constraints before behavioral testing. | `TASK-P1-003`; qualified license input; `AUD-015`, `AUD-016`, `AUD-031`. | Security, core-updater research | Digest/source evidence exists; current artifact distribution is held by `AUD-015`; full inventory/trust review remains. |
| `TASK-P1-005` | `BLOCKED` | Assess upstream maintenance, security intake, patch burden, and fork sustainability without committing to a fork. | `TASK-P1-003`; `AUD-023`. | Upstream maintenance | Sustainability report with owner/cost/risk recommendation. |
| `TASK-P1-006` | `IN_PROGRESS` | Inventory randomness, configuration consumers, observable surfaces, context coverage, host dependence, and probe blind spots. | `TASK-P1-004`; `AUD-001`, `AUD-003`, `AUD-006`, `AUD-007`, `AUD-019`, `AUD-022`, `AUD-027`–`AUD-030`. | Identity manager, fingerprint probe, engine contract research | Three per-launch seed sources and an initial main/worker probe are evidenced; complete surface/mutation matrix remains. |
| `TASK-P1-007` | `IN_PROGRESS` | Compare launcher parity and sidecar topology; validate authenticated protocol, process ownership, secret delivery, Windows path/process controls, and IPC design. | `TASK-P1-004`; provides evidence for `DEC-SIDECAR-001`; `AUD-012`, `AUD-024`, `AUD-031`, `AUD-033`, `AUD-034`. | Engine contract, process supervisor, sidecar, security | Python candidate, concrete Windows design, framing/HMAC and Job/DPAPI primitive tests exist; transport/tree/parity tests remain. |
| `TASK-P1-008` | `IN_PROGRESS` | Determine persistent browser-state ownership, safe checkpoints, negative cross-profile isolation, and crash reconciliation behavior. | `TASK-P1-007`; `AUD-004`, `AUD-005`, `AUD-013`. | Profile storage, process supervisor, engine adapter research | Clean-close cookie/LocalStorage/IndexedDB smoke exists; inventory, crash, isolation, and portability tests remain. |
| `TASK-P1-009` | `BLOCKED` | Qualify supported proxy modes and prove fail-closed DNS/WebRTC/request/TLS/header and regional-coherence behavior. | `TASK-P1-006`, `TASK-P1-007`; controlled network fixtures; `AUD-008`, `AUD-027`, `AUD-028`. | Proxy manager, engine adapter, fingerprint probe research | Supported-mode matrix and repeatable leak/coherence evidence. |
| `TASK-P1-010` | `BLOCKED` | Run repeated deterministic relaunch, cross-context, concurrency/resource, asymmetric-crash, and preflight-invalidation experiments. | `TASK-P1-006`–`TASK-P1-008`; selected environment matrix; `AUD-002`, `AUD-003`, `AUD-014`, `AUD-032`. | Identity/probe/supervisor research | Required restart matrix, resource envelope, crash results, revalidation-trigger decision inputs. |
| `TASK-P1-011` | `PENDING` | Gather non-Phase-2-blocking evidence for migration, rollback, portability, extensions, local API, release tooling, and a future Chromium evaluation only when prerequisites exist. | `AUD-009`–`AUD-011`, `AUD-017`, `AUD-018`, `AUD-020`, `AUD-021`, `AUD-025`, `AUD-026`; must not delay a valid Phase 2 decision unless a critical cross-cutting finding emerges. | Research workstreams | Per-audit report or explicit prerequisite/blocker record; no production implementation. |
| `TASK-P1-012` | `BLOCKED` | Produce the Phase 1 `GO` / `CONDITIONAL GO` / `HOLD` / `NO-GO` package and pin all Phase 2 implementation inputs. | Mandatory audit gate, `DEC-DATA-001`, `DEC-LIFECYCLE-001`, `DEC-PROFILE-001`, `DEC-SIDECAR-001`; `TASK-P1-003`–`TASK-P1-010`. | Architecture/product/audit owners | Signed decision, accepted risks, pinned handoff, and Phase 2 readiness checklist. |

## Phase 2 — local desktop MVP

All Phase 2 tasks are `PENDING`; their common blocker is `TASK-P1-012`. See the [Phase 2 specification](phases/PHASE_2_LOCAL_DESKTOP_MVP.md).

| Task | Status | Functional requirement | Requirement / decision gate | Owning modules | Acceptance evidence |
|---|---|---|---|---|---|
| `TASK-P2-001` | `PENDING` | Scaffold only the approved modular layout; implement pure identifiers, value objects, state rules, typed errors, capabilities, and generated contract bindings. | `REQ-ENGINE-001`, `INV-001`; accepted schema/tooling decisions. | `domain`, `engine-contract`, `operations`, `application` | Pure unit/contract/architecture tests pass without framework or engine dependencies. |
| `TASK-P2-002` | `PENDING` | Persist profiles, operations, immutable manifests, runtime configuration, core/baseline references, compatibility records, and proxy references with migrations and atomic writes. | `REQ-STORAGE-001`, `REQ-IDENTITY-003`; `DEC-DATA-001`. | `profile-storage`, application repositories | Crash and repository consistency tests prove one authority per record. |
| `TASK-P2-003` | `PENDING` | Create one profile secret, derive identity deterministically, enforce immutable identity/engine fields, and keep plaintext secrets behind opaque protected-store handles. | `REQ-IDENTITY-001`–`REQ-IDENTITY-003`, `REQ-STORAGE-002`, `SEC-001`; `AUD-034`. | `identity-manager`, `security`, keychain adapter | Identity invariant, loss/failure, and seeded-secret leakage tests pass under `AT-P2-007`. |
| `TASK-P2-004` | `PENDING` | Implement the selected sidecar protocol, Camoufox adapter, authenticated session, capability negotiation, one verified process tree per running profile, graceful stop, and uncertain-outcome reconciliation. | `REQ-PROFILE-002`, `REQ-ENGINE-001`–`REQ-ENGINE-003`, `SEC-002`, `SEC-004`; `DEC-SIDECAR-001`. | `engine-camoufox`, `process-supervisor`, `browser-driver-sidecar`, Windows process/filesystem adapters | Engine/protocol contract, authorization, duplicate request, crash, path, and orphan tests pass under `AT-P2-005`. |
| `TASK-P2-005` | `PENDING` | Implement Create/Start/Stop/reconcile plus the approved archive/trash/purge vocabulary; no external navigation or lease before preflight. | `REQ-PROFILE-001`, `REQ-PROFILE-003`–`REQ-PROFILE-006`; `DEC-LIFECYCLE-001`, `DEC-PROFILE-001`. | `profile-manager`, `application`, `fingerprint-probe` | `AT-P2-001`, `AT-P2-002`, `AT-P2-004`; every fault ends known or quarantined. |
| `TASK-P2-006` | `PENDING` | Provide only qualified proxy modes and the catalogue UI for safe metadata, lifecycle, status, search/filter/grouping, proxy assignment, and recovery explanations. | `AUD-008`; `INV-002`, `SEC-001`; approved profile semantics. | `proxy-manager`, `desktop-ui`, application facade | Desktop E2E and leak/failure tests; renderer has no direct privileged authority. |
| `TASK-P2-007` | `PENDING` | Enforce concurrency admission, supported Windows envelope, diagnostic redaction, packaged-path security, and restart/orphan recovery. | `AUD-014`, `AUD-031`, `AUD-033`; `SEC-001`–`SEC-004`. | Supervisor, diagnostics, security, composition roots | `AT-P2-003`, `AT-P2-006`–`AT-P2-008` and Phase 2 exit review pass. |

## Phase 3 — data safety and portability

All Phase 3 tasks are `PENDING` behind Phase 2 completion and their named audit/decision gates. See the [Phase 3 specification](phases/PHASE_3_DATA_SAFETY_AND_PORTABILITY.md).

| Task | Status | Functional requirement | Requirement / audit gate | Owning modules | Acceptance evidence |
|---|---|---|---|---|---|
| `TASK-P3-001` | `PENDING` | Create immutable snapshots only from verified checkpoints; stage snapshot recovery, preserve identity, verify integrity, and roll back or quarantine on uncertainty. | `REQ-PROFILE-004`; `AUD-005`, `AUD-013`. | `snapshot-manager`, profile storage, operations | Snapshot retention/corruption/fault and post-recovery preflight tests. |
| `TASK-P3-002` | `PENDING` | Implement approved cookie view/import/export/delete formats with per-record validation and no unsafe live database edits. | `AUD-005`, `AUD-026`; exact cookie schemas must be accepted first. | engine contract/adapter, import-export | Parser/property/fuzz tests and supported-field round trips. |
| `TASK-P3-003` | `PENDING` | Specify and implement a bounded streaming authenticated container with no plaintext staging and hostile-path/resource defenses. | `REQ-PORTABILITY-001`, `REQ-PORTABILITY-003`, `SEC-004`; cryptographic review. | `import-export`, `security` | Known-answer, tamper, truncation, traversal, resource-bound, and cleanup tests. |
| `TASK-P3-004` | `PENDING` | Implement Backup, Transfer, same-profile replacement recovery, and Duplicate-as-new with distinct identity/source-state rules. | `REQ-PORTABILITY-001`, `REQ-PORTABILITY-002`; `DEC-PORTABILITY-001`, `AUD-010`, `AUD-021`, `AUD-026`. | `import-export`, identity, snapshot, application | `AT-P3-004`–`AT-P3-007`; collision and partial-failure matrices pass. |
| `TASK-P3-005` | `PENDING` | Manage only qualified Firefox-compatible extensions with permission/fingerprint visibility and per-profile isolation. | `AUD-011`, `AUD-030`, `AUD-032`. | extension capability in engine adapter/application | Install/update/remove/persistence/incompatibility tests. |
| `TASK-P3-006` | `PENDING` | Complete proxy inventory/import/health/history/assignment and protected credential lifecycle without adding a proxy network or billing. | `AUD-008`, `AUD-026`, `AUD-034`, `SEC-001`. | `proxy-manager`, `security` | Proxy validation/leak and keychain denial/rotation/orphan tests. |
| `TASK-P3-007` | `PENDING` | Generate compatibility reports that block unsupported recovery/import before mutation and close the Phase 3 recovery/security matrix. | `AUD-010`, `AUD-022`, `AUD-026`. | application, import-export, diagnostics | `AT-P3-001`–`AT-P3-009` and Phase 3 exit review pass. |

## Phase 4A — core update, bulk work, API, and automation lease

Phase 4A is the mandatory Phase 4 track. All tasks are `PENDING` behind Phase 3 completion. See the [Phase 4 specification](phases/PHASE_4_CORE_UPDATE_AUTOMATION_AND_BULK.md).

| Task | Status | Functional requirement | Requirement / audit gate | Owning modules | Acceptance evidence |
|---|---|---|---|---|---|
| `TASK-P4A-001` | `PENDING` | Discover, stage as untrusted, verify, install immutably, retain, revoke, and catalogue browser cores without letting the engine adapter authorize artifacts. | `REQ-UPDATE-001`, `SEC-003`; `AUD-016`. | `core-updater`, security, artifact adapters | Tamper/replay/downgrade/interruption tests; `AT-P4-001`. |
| `TASK-P4A-002` | `PENDING` | Qualify candidates with contract, fingerprint, persistence, proxy, isolation, crash, resource, and canary evidence without changing active profile pointers. | `AUD-009`, `AUD-019`, `AUD-020`. | core-updater, engine contract, fingerprint probe | Immutable qualification report and `AT-P4-002`. |
| `TASK-P4A-003` | `PENDING` | Migrate one locked profile by committing active core and accepted baseline as one activation unit; preserve and test rollback. | `REQ-STORAGE-003`, `REQ-UPDATE-001`; `DEC-DATA-001`, `AUD-020`, `AUD-032`. | profile manager, core-updater, snapshot, operations | Fault-injected migration/rollback evidence; `AT-P4-003`, `AT-P4-004`. |
| `TASK-P4A-004` | `PENDING` | Execute bulk work as bounded independent per-profile operations with dry-run where needed, transparent partial results, and per-item recovery. | `REQ-OPERATIONS-002`; measured resource limits. | application, operations, scheduler | Mixed-result/cancellation/recovery tests; `AT-P4-005`. |
| `TASK-P4A-005` | `PENDING` | Expose versioned application use cases through an authenticated, bounded local API; never expose raw Playwright, database, filesystem, or shell access. | `SEC-002`, `INV-002`; `DEC-API-001`, `AUD-018`, `AUD-034`. | `automation-api`, security, application facade | Auth/authz/origin/rate/idempotency/fuzz/denial tests; `AT-P4-006`. |
| `TASK-P4A-006` | `PENDING` | Grant scoped Playwright automation leases only to the intended running profile and integrate expiry, cancellation, disconnect, navigation, resource, and shutdown policy. | `REQ-PROFILE-003`, `SEC-002`; qualified sidecar capabilities. | application, sidecar, automation policy | Cross-profile/race/cleanup tests; `AT-P4-007`. |
| `TASK-P4A-007` | `PENDING` | Close Phase 4A update, rollback, bulk, API, automation, redaction, and resource gates. | `TASK-P4A-001`–`TASK-P4A-006`. | Product/architecture/security owners | Phase 4A exit review and stable Phase 5 handoff. |

## Phase 4B — optional product experiments

These tasks are not required for Phase 4A completion or Phase 5 entry. They remain `DEFERRED` until `DEC-PHASE4B-001` explicitly activates one or more experiments after Phase 4A has usable safety/resource evidence.

| Task | Status | Functional requirement | Gate | Owning modules | Acceptance evidence |
|---|---|---|---|---|---|
| `TASK-P4B-001` | `DEFERRED` | If activated, provide Unicode/IME/contenteditable-aware typing with testable timing and no human-indistinguishability claim. | `DEC-PHASE4B-001`; automation lease must be stable. | automation policy/sidecar | Unicode, IME, clipboard, and editable-surface fixtures. |
| `TASK-P4B-002` | `DEFERRED` | If activated, run bounded per-profile URL/consent/scroll jobs with cancellation, explicit outcomes, and correlation warnings. | `DEC-PHASE4B-001`; scheduler/resource data. | application automation jobs | Timeout/proxy/resource/cancellation tests. |
| `TASK-P4B-003` | `DEFERRED` | If activated, prototype semantic leader/follower intent and stop on divergence, CAPTCHA, 2FA, authentication, or destructive action. | `DEC-PHASE4B-001`; separate accept/defer/reject result. | application automation jobs/sidecar | Divergence and unsafe-state stop tests; no raw-coordinate design. |

## Phase 5 — production hardening and engine extensibility

All Phase 5 tasks are `PENDING` behind Phase 4A completion. See the [Phase 5 specification](phases/PHASE_5_PRODUCTION_HARDENING_AND_EXTENSIBILITY.md).

| Task | Status | Functional requirement | Requirement / audit gate | Owning modules | Acceptance evidence |
|---|---|---|---|---|---|
| `TASK-P5-001` | `PENDING` | Package and sign Windows releases; test install/update/repair/uninstall/interruption/rollback without silent profile deletion. | `SEC-003`; project license; `AUD-015`–`AUD-017`, `AUD-031`. | Release composition/updater/security | `AT-P5-001`, clean-machine trust-chain matrix. |
| `TASK-P5-002` | `PENDING` | Close the full threat model or accept bounded residual risks with owners and review dates. | `SEC-001`–`SEC-004`; all implemented boundaries. | Security and all adapters | Abuse/regression review; no unresolved critical finding. |
| `TASK-P5-003` | `PENDING` | Enforce measured admission, fairness, throttling, pause/reject states, and checkpoint-aware watchdog recovery. | `AUD-014`; Phase 4 workload data. | scheduler, process supervisor, operations | Saturation/fairness/low-resource/recovery tests; `AT-P5-004`. |
| `TASK-P5-004` | `PENDING` | Produce an allowlisted, user-reviewable diagnostic bundle that excludes seeded sensitive data and raw profile content. | `SEC-001`. | diagnostics, security | Redaction/corruption/size/user-review tests; `AT-P5-005`. |
| `TASK-P5-005` | `PENDING` | Make release, rollback, vulnerability, SBOM/license, documentation, and end-of-support procedures repeatable. | `DEC-LICENSE-001`; `AUD-023`. | Release engineering/upstream maintenance | Rehearsed procedures and `AT-P5-006`. |
| `TASK-P5-006` | `PENDING` | Publish capabilities from qualification records with version/platform/evidence/limits; never infer them from engine name. | `REQ-ENGINE-001`–`REQ-ENGINE-003`. | capability registry, engine contract | Registry consistency and deprecation tests; `AT-P5-007`. |
| `TASK-P5-007` | `PENDING` | Evaluate a current Chromium candidate independently through the common contract; never reinterpret a Camoufox identity in place. | `AUD-025`, ADR-0007. | future `engine-chromium` spike | Evidence-backed GO/CONDITIONAL GO/HOLD/NO-GO ADR; `AT-P5-008`. |
| `TASK-P5-008` | `PENDING` | Verify support matrix, claims, operational evidence, and release handoff for the defined local-first product. | `INV-003`, all Phase 5 tasks. | Product/release owners | Phase 5 exit review; `AT-P5-009`. |

## Task update procedure

For every status change:

1. confirm the governing phase is authorized;
2. name affected `REQ-*`/`SEC-*`/`INV-*`, `AUD-*`, ADR, and decision IDs;
3. assign an owner before `IN_PROGRESS`;
4. link test/evidence before `COMPLETE`;
5. update the owning phase/requirement/audit/ADR if behavior, evidence, or architecture changed;
6. run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/docs-check.ps1`.

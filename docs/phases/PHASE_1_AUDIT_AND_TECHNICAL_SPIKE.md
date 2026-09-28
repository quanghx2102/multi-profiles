# Phase 1 — Audit and Technical Spike

## Status

`ACTIVE` for documentation; `GATED` for technical conclusions.

The architecture baseline, specifications, ADRs, and initial audit register exist. No Camoufox source audit or runtime experiment has been performed by this repository yet. Every planned result below remains prospective until evidence is attached to [AUDIT_REGISTER.md](../AUDIT_REGISTER.md).

## Objective

Determine whether a pinned Camoufox/launcher combination can safely support the product's minimum identity, isolation, persistence, proxy, lifecycle, and distribution requirements. Produce a reproducible go/no-go decision and enough verified contracts to begin the Local Desktop MVP without embedding unknown behavior as product logic.

## In scope

- Exact source/release provenance and licensing review.
- Fingerprint surface and randomness inventory.
- Deterministic identity and repeated-relaunch experiments.
- Cross-context propagation tests.
- Persistent browser-state inventory.
- Concurrent multi-process isolation and resource benchmarks.
- HTTP/HTTPS/SOCKS, DNS, and WebRTC tests.
- TypeScript-versus-Python launcher comparison.
- Sidecar protocol/recovery spike.
- Crash and operation-reconciliation experiments.
- Probe coverage design and mutation testing.
- Initial core migration/rollback and portability experiments when qualified artifacts are available.
- TLS/HTTP, regional, display/DPI, media-device, Windows-hardening, preflight-TOCTOU, Tauri IPC, and protected-secret threat scopes.
- Evidence-backed Camoufox, sidecar, and Phase 2 go/no-go decisions.

## Out of scope

- Production application code or UI.
- Tauri, Rust, or React scaffolding.
- Product database implementation.
- Shipping browser binaries or installers.
- Claims about Camoufox behavior without source/test evidence.
- Optimizing for unsupported websites or promising anti-bot success.

## Entry criteria

- Product scope, architecture, security boundaries, and engine contract are documented.
- Audit schema and initial items exist.
- The user explicitly authorizes source audit or technical-spike work beyond documentation.
- Exact repositories, revisions, releases, and artifact hashes are pinned before examination.
- Test machines and fixtures contain no valuable user profiles or credentials.

## Dependencies and assumptions

- Read access to exact Camoufox, launcher, generator/dependency, and release sources selected for audit.
- Authentic pinned release artifacts or a separately approved reproducible-build path.
- Supported Windows test hosts spanning the intended hardware/GPU/font matrix.
- Controlled proxy, DNS, WebRTC, crash-injection, and resource-observation facilities.
- Disposable profiles and accounts with no production credentials.
- Qualified licensing input before making distribution conclusions.
- Authorization in a later turn before cloning source, installing tools, building a browser, or executing the technical experiments.

## Workstreams

The executable ordering, dependencies, and all audit-to-workstream mappings are owned by [research/camoufox/AUDIT_PLAN.md](../../research/camoufox/AUDIT_PLAN.md). The order is deliberately fail-fast: licensing/provenance, sustainability, randomness/surfaces, launcher/sidecar, persistence/isolation, network containment, resources/crashes, then migration/portability.

### 1. Provenance, licensing, and sustainability

Audit `AUD-015`, `AUD-016`, and `AUD-023` together. Record the exact ownership and license of source, patches, launchers, dependencies, release assets, and build outputs. Separate legal questions from engineering observations and obtain qualified review before distribution conclusions.

Deliverables:

- pinned source/artifact manifest;
- license and notice inventory;
- artifact verification/trust-chain report;
- upstream health and fork-maintenance assessment;
- distribution go/no-go conditions.

### 2. Identity determinism and surface coverage

Audit `AUD-001`, `AUD-002`, `AUD-003`, `AUD-006`, `AUD-007`, `AUD-019`, `AUD-022`, and `AUD-027` through `AUD-030`. Build a source-to-probe coverage map before treating restart results as complete.

Required experiments:

- establish one controlled profile identity;
- restart it at least 50 times without changing identity inputs;
- include clean stop, forced browser exit, sidecar exit, and application-recovery variants;
- compare main frame, applicable iframe types, dedicated/shared worker, service worker, and worklet contexts;
- mutate each controlled input to demonstrate that the probe observes it;
- repeat on representative Windows/GPU/font environments.

Deliverables:

- fingerprint surface catalogue;
- randomness/source-consumer inventory;
- controlled versus host-dependent surface map;
- versioned probe schema and coverage matrix;
- semantic baseline and diff proposal;
- unsupported or patch-required list.

### 3. Profile persistence, isolation, and lifecycle

Audit `AUD-004`, `AUD-005`, `AUD-013`, and `AUD-014`. Use unique sentinel data for every profile and verify negative isolation assertions.

Required experiments:

- enumerate persistent and non-persistent browser state;
- run at least two profiles concurrently and stress 1/5/10/20 where feasible;
- randomize start/stop/crash ordering;
- inspect process trees, endpoints, temporary paths, caches, handles, and data directories;
- inject faults before and after lifecycle durable boundaries;
- measure RAM, CPU, GPU, handles, startup, steady-state, and shutdown behavior.

Deliverables:

- persistence matrix and checkpoint requirements;
- multi-instance collision/isolation report;
- crash reconciliation state table;
- initial supported concurrency/admission recommendation;
- process-supervision requirements.

### 4. Proxy and network containment

Audit `AUD-008`, `AUD-027`, and `AUD-028` using controlled observation infrastructure. Cover request paths, TLS/HTTP behavior, regional coherence, failure behavior, authentication, DNS resolution, WebRTC candidates, redirects, websockets, downloads, and service-worker traffic.

Deliverables:

- supported proxy-mode matrix;
- strict fail-closed policy proposal;
- leak-test procedure and evidence;
- explicit exclusions and user-visible failure model.

### 5. Launcher and sidecar boundary

Audit `AUD-012`, `AUD-024`, `AUD-031`, `AUD-033`, and `AUD-034`. Apply one conformance scenario set to the TypeScript and Python launchers. The TypeScript preference and sidecar topology are not decisions until parity, isolation, resource, authentication, crash-blast-radius, compatibility, and adoption evidence exists.

The protocol spike must exercise:

- version negotiation and capability reporting;
- instance authentication and endpoint ownership;
- duplicate request/idempotency behavior;
- lost response and outcome-unknown reconciliation;
- core, sidecar, and browser crash permutations;
- timeout, cancellation, event ordering, and backpressure;
- safe delivery of sensitive configuration without argv/log exposure.

Use [SIDECAR_PROCESS_MODEL.md](../SIDECAR_PROCESS_MODEL.md) as the intended authority model. The spike must either validate a concrete Windows mechanism for it or record the necessary design change; the document itself is not evidence that containment/adoption works.

Deliverables:

- launcher parity matrix and language decision;
- selected transport recommendation;
- protocol state machine and error taxonomy;
- recovery and process-adoption/termination rules;
- contract-test plan.

### 6. Forward-looking compatibility probes

Gather decision inputs for `AUD-009`, `AUD-010`, `AUD-011`, `AUD-017`, `AUD-018`, `AUD-020`, `AUD-021`, and `AUD-025` without prematurely implementing later phases. Migration and rollback must be attempted when two suitable pinned cores exist; otherwise the missing precondition is documented and the profile stays pinned.

## Evidence workflow

For each audit item:

1. Pin revisions, artifacts, environment, and hypothesis.
2. Record source paths and exact lines or symbols inspected.
3. Define the procedure and expected result before execution.
4. Store raw output with integrity hashes and secret redaction using the [Camoufox evidence workspace](../../research/camoufox/evidence/README.md).
5. Record observed result, confounders, and reproduction steps.
6. Assign evidence quality according to the audit register.
7. Record required decision, patch, and regression test.
8. Update status only when the evidence threshold is met.

A source claim and a runtime claim are separate evidence. A single passing environment is not multi-environment confirmation.

## Phase deliverables

- Updated [Audit Register](../AUDIT_REGISTER.md) with evidence links and decisions.
- Selected [upstream lock](../../research/camoufox/UPSTREAM_LOCK.json) with no floating revisions or unverified hashes.
- Per-item audit reports and evidence manifests following the [Phase 1 templates](../audit/README.md).
- Source/release/artifact inventory.
- Fingerprint-surface and probe coverage specification.
- Reproducible experiment matrix and results.
- Launcher and sidecar decision report.
- Initial Windows support and concurrency envelope.
- Patch backlog separated into required, optional, and rejected work.
- Camoufox go/no-go report.
- Phase 2 readiness checklist and pinned implementation inputs.

Planned acceptance packages use the `AT-P1-*` identifiers in the [Requirement Catalogue](../REQUIREMENTS.md).

## Mandatory Phase 2 gate

The following audits require an evidence-backed decision before Phase 2: `AUD-001` through `AUD-008`, `AUD-012` through `AUD-016`, `AUD-019`, `AUD-022` through `AUD-024`, and `AUD-027` through `AUD-034`. For `AUD-033` and implementation-dependent portions of other audits, Phase 1 must approve the testable design and fail-closed gate; runtime closure remains a Phase 2 exit obligation.

They do not all need the same terminal status. Acceptable outcomes are:

- `CONFIRMED` when the required behavior is demonstrated;
- `RESOLVED` when a verified patch and regression test close the finding;
- `ACCEPTED_RISK` only when the MVP can safely exclude or constrain the capability;
- `REJECTED` when the relevant technical path is explicitly removed.

`NOT_STARTED`, `RESEARCHING`, `TEST_READY`, `BLOCKED`, or an unmitigated `PATCH_REQUIRED` does not clear the gate.

## Exit criteria

The phase may enter exit review only after the mandatory Phase 2 gate has been evaluated and a decision package exists. The technical criteria below are mandatory unless a specific capability is explicitly removed from MVP scope through an accepted decision.

### Mandatory acceptance criteria

- One profile completes the defined 50-restart matrix with no unexplained immutable-identity drift.
- Two or more profiles demonstrate distinct identities and negative cookie/storage/extension-state isolation.
- Required contexts have consistent results or are explicitly unsupported and excluded from the product guarantee.
- Proxy strict mode has a tested supported matrix and closes rather than bypasses on failure.
- Crash tests never regenerate an existing identity or falsely report a completed lifecycle operation.
- A safe initial concurrency limit is supported by measurements.
- Launcher language and sidecar boundary decisions are backed by comparable evidence.
- Artifact provenance and licensing permit the planned Phase 2 development/distribution path, or impose explicit constraints.
- The fingerprint probe has a reviewed coverage map and known blind spots.
- A signed Phase 1 decision records `GO`, `CONDITIONAL GO`, `HOLD`, or `NO-GO`.

## Go/no-go rules

### GO

Minimum identity, isolation, persistence, network, lifecycle, and distribution requirements are demonstrated on the initial support matrix. Phase 2 receives pinned inputs and no critical unknown.

### CONDITIONAL GO

Only bounded limitations remain, such as a reduced proxy/preset/context/support matrix. Each limitation is enforced by capability checks or validation, documented to users, assigned an owner, and covered by regression tests.

### HOLD

Required evidence is incomplete, a patch is still being verified, or qualified test environments are unavailable. Production scaffolding remains unauthorized.

### NO-GO

Camoufox cannot provide a required invariant, distribution is not viable, or ongoing maintenance risk exceeds the accepted boundary. Record whether to evaluate another engine, change scope, or stop the project.

## Risks and controls

| Risk | Mitigation |
|---|---|
| Passing tests miss a surface | Source-to-probe coverage and mutation tests under `AUD-019` |
| Host variability is mistaken for profile randomness | Controlled single-factor and multi-environment tests |
| Test artifacts leak secrets | Disposable fixtures, allowlisted capture, redaction and artifact review |
| Upstream changes during audit | Pin revisions; rebase only as a separate evidence set |
| Benchmark results are not comparable | Fixed workloads, environment capture, repeated distributions |
| Schedule pressure converts hypotheses into decisions | Gate strictly on audit status and evidence quality |

## Handoff to Phase 2

The handoff pins the supported Windows environment, Camoufox core/artifact hash, launcher version/language, sidecar protocol version, capability set, identity/probe schemas, proxy modes, concurrency cap, required patches, regression suite, accepted risks, and open non-blocking audits.

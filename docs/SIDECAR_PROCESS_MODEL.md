# Sidecar and Process Ownership Model

## Scope and evidence boundary

This document defines intended authority and failure semantics for the application, process supervisor, browser-driver sidecar, and browser. It does not select a Windows process-containment primitive or claim that Camoufox exposes all required process information. Those questions remain in `AUD-024`.

## Topology candidates

No topology is selected. [ADR-0016](adr/0016-sidecar-topology.md) is `Proposed`; `AUD-024` must produce spike evidence.

| Candidate | Isolation | Resource cost | Crash blast radius | Authentication | Version compatibility | Adoption/reconciliation |
|---|---|---|---|---|---|---|
| One dedicated sidecar worker per running profile | Strongest protocol/process separation | Highest fixed overhead | Normally one profile | Unique per-instance credential and endpoint | Each instance binds one protocol/launcher version | Straightforward only if ownership survives supervisor restart |
| One shared multi-profile sidecar | Logical isolation only | Lowest fixed overhead | All managed profiles | Per-client plus per-profile authorization | One process must negotiate all active versions | Complex multiplexed recovery and partial failure |
| Shared sidecar coordinator with isolated worker per profile | Worker isolation plus a shared sidecar coordination layer | Highest process count unless shared services offset it | Worker failure local; coordinator failure broad | Coordinator channel plus unique worker capability | Coordinator/worker compatibility matrix required | Two-level recovery must remain subordinate to the Rust supervisor |

Acceptance requires measured startup/steady memory, malicious-client isolation, asymmetric crash tests, mixed-version behavior, credential rotation, and verified process adoption/termination. The recommendation is one dedicated sidecar worker per running profile because the common Rust supervisor already supplies shared policy and durable ownership. A shared sidecar coordinator is justified only if the spike demonstrates material benefit without creating a competing authority or unacceptable common failure point. This recommendation is not an accepted decision.

## Ownership chain

| Actor | Owns | Does not own |
|---|---|---|
| Application lifecycle use case | profile lock, allowed transition, operation journal, retry/recovery decision | OS process handles, launcher calls, browser automation session |
| `process-supervisor` | authoritative supervised-tree record, sidecar spawn, liveness, deadlines, verified orphan handling, escalation and resource observations | engine configuration, fingerprint acceptance, browser commands |
| Browser-driver sidecar | protocol session, engine-launcher invocation, Playwright session, graceful browser command, browser events | durable profile state, profile lock, baseline acceptance, arbitrary process termination |
| Browser process | engine execution and browser-owned profile-state flush | application lifecycle truth or snapshot approval |

The OS process adapter is an implementation detail of `process-supervisor`. The engine launcher is an implementation dependency of the sidecar.

## Start sequence

1. The application acquires the profile lock and journals a start operation.
2. The supervisor creates a unique sidecar session/ownership context and asks the OS adapter to spawn the sidecar.
3. The core authenticates the sidecar endpoint and negotiates protocol/capabilities.
4. The application sends one idempotency-scoped `startProfile` request.
5. The sidecar invokes the selected launcher and reports browser identity/events needed for supervision.
6. The supervisor verifies and records the resulting tree before the application may proceed to fingerprint preflight.
7. The browser enters `LAUNCHED_UNVERIFIED`; only successful preflight permits the configured launchable steady state (`READY` or `STOPPED`, pending ADR-0017) and then `RUNNING` when the user session is admitted.

A timeout at steps 2–6 is `outcome-unknown` until reconciliation proves whether a tree exists. A retry may repeat the same operation identity but may not create a second tree.

## Stop sequence

1. The application enters `STOPPING` and blocks new mutating work.
2. The sidecar requests graceful browser shutdown and reports browser/checkpoint events it can observe.
3. The supervisor independently observes owned-tree exit within the deadline.
4. If policy permits escalation, the supervisor terminates only the verified owned tree.
5. The application records checkpoint confidence, recovery requirements, and final lifecycle state.

Sidecar acknowledgement alone does not prove browser exit or durable browser-state flush.

## Reconciliation matrix

| Observation | Required response |
|---|---|
| Sidecar alive, browser alive, journal expects start/run | Re-authenticate and reconcile the same operation/session before adopting control; no second launch |
| Sidecar dead, browser alive | Keep profile locked, mark recovery required, verify tree ownership, then follow the `AUD-024`-approved terminate/adopt policy |
| Sidecar alive, browser dead | Collect exit/checkpoint evidence, close the sidecar session, and reconcile profile state |
| Both dead, operation incomplete | Compare durable journal, exit records, and storage/checkpoint evidence; return to a known stopped state or quarantine |
| Process found but ownership cannot be proven | Do not kill or adopt it; quarantine/raise operator recovery guidance |
| Core/application restarts with stale endpoint | Reject stale credentials, inspect verified ownership evidence, and reconcile before accepting lifecycle commands |

## Ownership evidence requirements

The eventual mechanism must resist PID reuse and stale endpoint confusion. Evidence is expected to bind an operation, profile, sidecar instance, browser tree, executable/artifact identity, and creation lifetime without putting secrets in argv or logs. Exact tokens, handles, job/container primitives, endpoint transport, and persistence are not selected here.

## Failure invariants

- At most one supervised tree exists for a profile.
- Unknown outcome never becomes success by assumption.
- No process is killed or adopted using an unverified PID alone.
- Sidecar loss cannot unlock a profile while its browser may remain alive.
- Browser loss cannot be reported as a clean stop without checkpoint evidence.
- Reconciliation cannot regenerate identity or accept a new fingerprint baseline.

See [ADR-0012](adr/0012-supervised-sidecar-process-ownership.md), [ADR-0016](adr/0016-sidecar-topology.md), [PROFILE_LIFECYCLE.md](PROFILE_LIFECYCLE.md), and `AUD-024` in the [Audit Register](AUDIT_REGISTER.md).

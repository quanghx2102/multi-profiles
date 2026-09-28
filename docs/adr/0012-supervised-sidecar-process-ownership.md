# ADR-0012: Supervised Sidecar and Browser Process Ownership

- Status: Accepted; Windows mechanism pending `AUD-024`
- Date: 2026-09-28

## Context

The sidecar must invoke the engine launcher, but lifecycle safety requires one authority to prevent duplicate launches, retain process identity, reconcile lost responses, and terminate verified orphans. Treating both the sidecar and Rust core as process owners creates ambiguous recovery behavior.

## Decision

The Rust-side `process-supervisor` is the authoritative owner of the supervised sidecar/browser process tree and its durable ownership record. It asks an OS process adapter to spawn the sidecar. The sidecar, after an authorized `startProfile` request, invokes the selected engine launcher and reports browser process identity and lifecycle events. The sidecar owns the automation/launcher session, not durable lifecycle policy or unrestricted termination authority.

Graceful browser shutdown is requested through the sidecar. Forced termination is performed only by the supervisor against a process tree whose ownership has been verified. Lost responses and mismatched sidecar/browser liveness enter reconciliation; they never trigger a blind second launch. The intended state model is specified in [SIDECAR_PROCESS_MODEL.md](../SIDECAR_PROCESS_MODEL.md).

The concrete Windows containment primitive, endpoint ownership, PID-reuse defense, adoption policy, and core/sidecar/browser crash behavior must be selected and demonstrated by `AUD-024`.

## Consequences

Process authority is unambiguous, while engine-specific launch translation remains isolated in the sidecar. The protocol must report sufficient non-secret ownership and process evidence. The supervisor may terminate a verified tree after policy escalation but may never kill a process based only on an unverified PID.


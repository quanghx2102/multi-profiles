# ADR-0016: Sidecar Process Topology

- Status: Proposed; selection requires `AUD-024` evidence
- Date: 2026-09-28
- Decision owner: Pending user approval (`DEC-SIDECAR-001`)

## Context

Accepted ADRs require a language-neutral sidecar boundary, one isolated browser process tree per running profile, and Rust-side supervision authority. They do not establish whether sidecar execution is per profile, shared, or split into a shared coordinator plus isolated workers.

## Options

| Option | Isolation / blast radius | Resource cost | Authentication/versioning | Adoption/reconciliation |
|---|---|---|---|---|
| One sidecar process per running profile | Strong process/session separation; one worker crash affects one profile | Highest per-profile process/runtime overhead | Per-worker authenticated session and protocol version | Direct worker/browser ownership but many endpoints |
| One shared sidecar for all profiles | Shared memory/runtime and broad crash blast radius | Lowest startup/memory overhead | One endpoint needs strict per-profile authorization and multiplexing | Shared failure complicates partial adoption and event ordering |
| Common Rust supervisor with isolated sidecar worker per profile | Central policy with per-profile failure containment | Similar worker cost plus common supervisor already planned | Supervisor provisions one scoped worker session/profile; version compatibility checked per worker | Clear per-profile tree while common reconciliation policy remains in Rust |

## Recommendation

Use the third topology as the target interpretation: the Rust supervisor is common, and each running profile receives an isolated sidecar worker process/session that launches one browser tree. This is a recommendation, not a final decision.

## Acceptance criteria

`AUD-024` must compare all options for startup/steady resource cost; cross-profile state leakage; one-worker/shared-process crash blast radius; endpoint ACL/authentication; protocol version skew; backpressure/event ordering; lost response/idempotency; core/sidecar/browser asymmetric crashes; and verified process adoption/termination without PID-only trust. The selected topology must preserve ADR-0004 isolation within the Phase 1 concurrency envelope.

## Consequences

The recommendation favors isolation and explainable recovery over minimum process count. If measurements reject it, a superseding proposal must show how a shared sidecar enforces per-profile authority and bounds crash impact without weakening accepted invariants.


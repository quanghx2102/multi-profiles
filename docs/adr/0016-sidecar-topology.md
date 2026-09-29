# ADR-0016: Sidecar Process Topology

- Status: Proposed; selection requires `AUD-024` evidence
- Date: 2026-09-28
- Last reviewed: 2026-09-29
- Decision owner: Pending user approval (`DEC-SIDECAR-001`)

## Context

Accepted ADRs require a language-neutral sidecar boundary, one isolated browser process tree per running profile, and Rust-side supervision authority. They do not establish whether sidecar execution is per profile, shared, or split into a shared coordinator plus isolated workers.

## Options

| Option | Isolation / blast radius | Resource cost | Authentication/versioning | Adoption/reconciliation |
|---|---|---|---|---|
| One dedicated sidecar worker per running profile | Strong process/session separation; one worker crash affects one profile | Highest per-profile process/runtime overhead | Rust supervisor provisions one authenticated worker session/profile | Direct worker/browser ownership but many endpoints |
| One shared sidecar for all profiles | Shared memory/runtime and broad crash blast radius | Lowest startup/memory overhead | One endpoint needs strict per-profile authorization and multiplexing | Shared failure complicates partial adoption and event ordering |
| Shared sidecar coordinator with isolated worker per profile | Per-profile worker isolation, but coordinator failure affects all workers | Worker cost plus coordinator overhead; may share some runtime services | Rust supervisor authenticates the coordinator; coordinator must provision scoped worker capabilities | Two-level adoption, event ordering, and authority must remain subordinate to Rust supervision |

## Recommendation

Prefer the first topology: the already-required Rust supervisor creates one dedicated sidecar worker/session for each running profile, and that worker launches one browser tree. It has the smallest authority model and the narrowest sidecar crash boundary. This is a recommendation, not a final decision; `AUD-024` may reject it if measured overhead exceeds the supported concurrency envelope.

## Acceptance criteria

`AUD-024` must compare all options for startup/steady resource cost; cross-profile state leakage; one-worker/shared-process crash blast radius; endpoint ACL/authentication; protocol version skew; backpressure/event ordering; lost response/idempotency; core/sidecar/browser asymmetric crashes; and verified process adoption/termination without PID-only trust. The selected topology must preserve ADR-0004 isolation within the Phase 1 concurrency envelope.

## Consequences

The recommendation favors isolation and explainable recovery over minimum process count. If measurements reject it, the selected shared topology must show how it enforces per-profile authority, prevents a coordinator from becoming a competing durable owner, and bounds crash impact without weakening accepted invariants.

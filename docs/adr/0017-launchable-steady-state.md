# ADR-0017: Launchable Steady-State Vocabulary

- Status: Proposed
- Date: 2026-09-28
- Decision owner: Pending user approval (`DEC-LIFECYCLE-001`)

## Context

Current lifecycle documents use both `READY` and `STOPPED`, but both mean that no browser is running and a later start may be attempted. The distinction is not strong enough to drive policy and risks illegal or inconsistent transitions.

## Proposed decision

Use `READY` as the single steady state for a non-archived profile that has no owned process tree and is eligible to attempt Start. Record how the previous run ended in `lastStopDisposition` (`NEVER_STARTED`, `CLEAN`, `FORCED_RECOVERY_REQUIRED`, `CRASH_RECONCILED`) and operation history rather than as a second steady state.

Keep `LAUNCHED_UNVERIFIED` as a transient state between browser launch and successful preflight. A clean Stop returns to `READY`; uncertain/forced stop enters `RECOVERING` until reconciled.

## Alternative

Retain both states with strict meaning: `READY` means newly verified or explicitly revalidated; `STOPPED` means no process after a prior run and requires all current start validations. This preserves existing labels but adds little behavior beyond metadata.

## Consequences

The recommended state machine is smaller and avoids UI/state branching that has no safety effect. Accepting it requires updating existing phase/lifecycle references and any draft schemas before Phase 2. Until approval, both labels remain documented with provisional semantics in `PROFILE_LIFECYCLE.md`.


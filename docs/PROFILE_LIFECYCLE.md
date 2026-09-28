# Profile Lifecycle

## States

```text
DRAFT -> CREATING -> VERIFYING -> READY -> STARTING -> RUNNING
                    |              ^         |           |
                    v              |         v           v
                QUARANTINED <------+------ STOPPING <- RECOVERING
                                      |         |
                                      v         v
                                    STOPPED   QUARANTINED

READY/STOPPED -> MIGRATING -> READY/STOPPED
       |             |             ^
       |             v             |
       +--------- ROLLING_BACK -----+

READY/STOPPED/QUARANTINED -> ARCHIVED
```

Implementations may refine transient states, but may not remove the safety gates below.

## Create

1. Validate request and engine capabilities.
2. Reserve identifiers and filesystem location.
3. Select a coherent device preset.
4. Create and protect `profileSecret`; derive versioned seeds.
5. Write an integrity-protected identity manifest.
6. Create the dedicated user data directory.
7. Launch in a controlled verification flow and collect the initial baseline.
8. Commit `READY` only when verification passes.

On failure, clean up only resources proven to belong to the incomplete operation. Preserve evidence needed for diagnosis. If secret/manifest state is uncertain, quarantine rather than retrying identity creation.

## Start

1. Acquire the exclusive profile lock.
2. Reconcile any prior incomplete operation and orphan process.
3. Validate browser-core version, provenance, and files.
4. Validate identity manifest and data-directory ownership.
5. Negotiate sidecar and engine capabilities.
6. Start the browser-driver and exactly one browser process tree.
7. Run fingerprint preflight in required contexts.
8. Mark `RUNNING` only after semantic comparison passes.

Any preflight or integrity failure causes shutdown followed by `QUARANTINED`, or rollback when the failure is part of an eligible core migration. A timeout is reconciled before retry; it never triggers a blind second launch.

## Stop

1. Mark `STOPPING` and reject new mutating automation.
2. Request graceful browser shutdown.
3. Wait for the owned process tree and storage checkpoint within policy deadlines.
4. Escalate termination if authorized and record incomplete-flush risk.
5. Complete the recovery checkpoint required by the current phase. Once the Phase 3 snapshot capability is available, create a policy-governed snapshot only when safe-checkpoint policy passes.
6. Update metadata and event journal transactionally.
7. Release the lock and enter `STOPPED`.

If checkpoint, snapshot, or metadata commit is uncertain, retain the lock and enter recovery rather than reporting a clean stop. The Phase 2 internal recovery checkpoint is not presented as a user-managed backup; snapshot history and general restore are Phase 3 capabilities.

## Crash recovery

- Never create a new identity or overwrite the manifest.
- Record process exit data and the last durable operation state.
- Detect sidecar/browser orphans and verify ownership before termination.
- Inspect storage/checkpoint integrity using engine-supported methods.
- Restore the latest verified snapshot only through an explicit recovery decision.
- Re-run fingerprint preflight before returning to normal operation.
- Quarantine when correctness cannot be established.

Crash consistency is gated by `AUD-013` and sidecar reconciliation by `AUD-024`.

## Core migration

1. Install and verify the new core alongside the old core.
2. Confirm engine/identity/data compatibility without changing the active pointer.
3. Create recovery metadata and a safe snapshot.
4. Run a canary launch with the new core and collect the new-version baseline candidate.
5. Generate a semantic diff and apply policy.
6. Commit the active core and baseline together, or stop and roll back to the retained old core.

The migration must not also change proxy, OS/device preset, or identity secret. Details are in [UPDATE_STRATEGY.md](UPDATE_STRATEGY.md).

## Concurrency

Only one mutating lifecycle operation may hold a profile lock. Read-only queries use committed metadata. Bulk actions are a set of individually journaled profile operations, not a single shared transaction across browser processes.

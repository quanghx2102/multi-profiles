# Operations Model

- Status: Proposed
- Owner: Application and operations
- Last reviewed: 2026-09-28
- Review trigger: Sidecar protocol selection or lifecycle-state approval

## Purpose

This model defines durable semantics for long-running or cross-boundary work. It applies to profile creation, start/stop, recovery, snapshot operations, portability, core installation/migration, automation, and bulk commands.

## Identifiers

- `operationId` uniquely identifies one durable application operation and is reused for idempotent retry/reconciliation of that operation.
- `correlationId` groups related operations and cross-process messages for diagnostics; it grants no authority.
- `idempotencyKey` is a caller-provided or application-generated deduplication key mapped durably to one operation/result within a bounded scope.
- `profileId` scopes profile locks and cannot be inferred from paths or process IDs.
- `sidecarSessionId` and verified process ownership evidence scope one supervised runtime; exact format remains `AUD-024` work.

None of these identifiers is a secret. Authentication material is carried through a separately protected channel.

## Durable stages

| Stage | Meaning | Permitted next stage |
|---|---|---|
| `PREPARED` | Request validated, lock/resources reserved, prior authoritative state recorded | `EFFECTING`, `CANCELLED`, `REJECTED` |
| `EFFECTING` | External process/filesystem/engine effect may have begun | `COMMITTING`, `FAILED`, `OUTCOME_UNKNOWN`, `CANCELLING` |
| `COMMITTING` | Effect verified and authoritative metadata transaction is in progress | `SUCCEEDED`, `OUTCOME_UNKNOWN` |
| `SUCCEEDED` | Required postconditions and durable commit are verified | terminal |
| `FAILED` | Failure is known and compensation/recovery disposition is recorded | retry by new policy decision only |
| `CANCELLED` | Cancellation completed before or after documented compensation | terminal |
| `OUTCOME_UNKNOWN` | Caller cannot prove whether an effect/commit occurred | `RECONCILING` only |
| `RECONCILING` | Durable evidence and external state are being compared | known terminal state or quarantine |

Requested intent, process acknowledgement, and UI progress never equal durable success.

## Deadlines and cancellation

Every operation declares a deadline policy and cancellation points. Deadline expiry returns `OUTCOME_UNKNOWN` whenever an external effect may have started. Cancellation is cooperative first; forced process termination is a separate authorized escalation that records incomplete-flush risk. A cancelled import/migration cannot expose staged data as authoritative.

## Retry eligibility

| Outcome | Retry rule |
|---|---|
| Rejected before effect | A corrected request may create a new operation |
| Known transient failure before effect | Retry may reuse idempotency mapping according to contract |
| Partial effect with successful compensation | New operation after compensation verification |
| `OUTCOME_UNKNOWN` | No retry until reconciliation completes |
| Integrity/security failure | Quarantine or explicit operator decision; no automatic retry |

## Locking

- One mutating profile operation owns the exclusive profile lock.
- Read-only queries see committed metadata and report in-progress operation state separately.
- Locks bind a durable operation, not a UI window or transient process.
- A crash does not imply lock release; startup reconciliation decides release.
- Multi-profile bulk work acquires locks per profile and does not hold one global transaction across browsers.

## Reconciliation

Reconciliation compares the operation journal with authoritative metadata, verified process ownership, filesystem staging/final paths, snapshot/container integrity, and engine-supported checkpoint evidence. It produces one explainable state or quarantine. It never regenerates identity, launches a replacement browser blindly, accepts a baseline, or marks success merely because the requested target appears plausible.

Process adoption or termination follows [SIDECAR_PROCESS_MODEL.md](SIDECAR_PROCESS_MODEL.md) and `AUD-024`: adoption requires authenticated session/version compatibility and verified ownership; termination never uses an unverified PID alone.

## Event journal

Events are append-only observations with `eventId`, `operationId`, correlation, event type/version, timestamp, actor, redacted payload, and causal sequence where known. Events support reconciliation and diagnostics but do not replace authoritative aggregate state. Late/duplicate events are tolerated and deduplicated by identity/sequence rules defined by the selected protocol.

## Long-running status

Application/API/UI status exposes stage, bounded progress, cancellability, safe summary, retry eligibility, last durable event, and whether reconciliation/operator action is required. It never exposes secrets, raw cookies, authenticated URLs, or arbitrary sidecar logs.

## Bulk operations

A bulk request creates one parent correlation record and one independent operation per profile. Validation, locks, outcome, cancellation, retry, and recovery remain per profile. Aggregate status summarizes partial success but cannot claim all-or-nothing atomicity.


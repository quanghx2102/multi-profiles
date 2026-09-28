# Phase 4 — Core Update, Automation, and Bulk Operations

## Status

`PLANNED`.

## Objective

Add controlled browser-core evolution and high-level automation without allowing automation, bulk execution, or updates to bypass profile lifecycle, security, and recovery policy.

## Entry criteria

- Phase 3 provides verified snapshots, restore, compatibility reports, and protected credentials.
- Fingerprint drift (`AUD-009`), artifact trust (`AUD-016`), local endpoint security (`AUD-018`), and rollback compatibility (`AUD-020`) have accepted decisions.
- The engine contract and sidecar protocol are stable under Phase 2/3 operating history.
- Update trust roots, retention, and emergency-disable policies are approved.
- Resource admission inputs exist for batch and automation workloads.

## Dependencies and assumptions

- Stable Phase 3 snapshot/restore and compatibility-report primitives.
- Approved release metadata source, artifact trust roots, and core retention policy.
- At least two compatible pinned core versions for migration/rollback qualification when update support is activated.
- Stable sidecar capability reporting and application operation model.
- Resource measurements sufficient to bound concurrent browser, migration, batch, and automation work.

## In scope

Phase 4 is divided into a mandatory delivery track and an optional product-experiment track. Phase 4B does not block completion of Phase 4A or entry to Phase 5 when it is explicitly deferred or rejected.

### Phase 4A — mandatory

- Immutable multi-core installation catalogue.
- Verified update discovery, download, staging, qualification, and retention.
- Stable Automatic, Manual Approval, and Pinned profile policies.
- Disposable and selected-profile canaries.
- Semantic fingerprint migration reports and automatic rollback.
- Profile-safe bulk operations with independent results.
- Authenticated local REST API and operation-status model.
- Playwright-oriented automation behind application policy.
- Scheduling, cancellation, retry, concurrency, and resource admission for mandatory operations.

### Phase 4B — optional

- Human typing behavior.
- Basic Cookie Bot jobs.
- Optional semantic Run with Sync prototype.
- Scheduling, cancellation, retry, concurrency, and resource admission for any accepted optional behavior.

## Out of scope

- Public internet API, remote multi-user control, team authorization, or cloud browser.
- Puppeteer/CDP compatibility claims for Camoufox.
- Automatic acceptance of unknown fingerprint changes.
- Arbitrary script, shell, filesystem, SQL, or raw sidecar access through API/UI.
- Atomic all-or-nothing semantics across multiple browser processes.
- Claims that Cookie Bot, human typing, or synchronized actions appear human or avoid linkage.

## Phase deliverables

- Verified multi-core catalogue and staged update pipeline.
- Candidate qualification, canary, semantic migration, and rollback workflows.
- Stable Automatic, Manual Approval, and Pinned policy implementations.
- Bounded bulk-operation coordinator with per-profile outcomes.
- Authenticated versioned local REST API and operation-status surface.
- Policy-bound Playwright automation leases.
- Human typing and basic Cookie Bot behavior.
- An accepted, deferred, or rejected Run with Sync prototype decision.
- Update, API, automation, and resource regression suites.

## Workstreams

Workstreams 1–6 are Phase 4A. Workstreams 7–9 are Phase 4B and require individual accept/defer/reject decisions.

### 1. Core catalogue and verified installation

Implement [UPDATE_STRATEGY.md](../UPDATE_STRATEGY.md) with immutable installations identified by engine, platform, version, build/artifact hash, provenance, adapter compatibility, and qualification state.

Update processing must:

- separate discovery, untrusted staging, verification, installation, qualification, and activation;
- fail closed on missing/mismatched trust metadata;
- prevent arbitrary downgrade outside explicit rollback/pinned policy;
- coexist with running profiles that still reference an older core;
- retain the old core and recovery point for the approved rollback window;
- support emergency revocation without deleting evidence or active recovery prerequisites.

`core-updater` owns download, untrusted staging, provenance authorization, installation finalization, catalogue state, and retention. The engine adapter only validates the candidate/installed layout through the engine contract; it cannot install or authorize an artifact.

### 2. Qualification and canary pipeline

For each candidate core:

1. Validate installation and launcher compatibility.
2. Run engine contract and probe coverage suites.
3. Run persistence, proxy, isolation, crash, and resource regressions on disposable fixtures.
4. Compare fingerprint results against version-aware semantic rules.
5. Canary selected recoverable profiles under explicit policy.
6. Generate a signed/immutable qualification report reference.
7. Promote, hold, reject, or patch the candidate.

Qualification does not alter a user profile's active-core pointer.

### 3. Per-profile migration and rollback

- Acquire the profile lock and reject simultaneous identity/proxy/preset changes.
- Create and verify the required recovery snapshot.
- Validate source/target core and profile-data compatibility.
- Launch with the candidate core, run full migration preflight, and produce semantic diff.
- Commit target core and accepted baseline together only after policy approval.
- On failure, terminate the candidate and perform the `AUD-020`-approved rollback path.
- Revalidate the old core after rollback; quarantine if rollback correctness is uncertain.

### 4. Bulk operation framework

Support safe batch forms of start, stop, archive, move/group, tag/status, proxy assignment, extension/configuration actions approved by earlier phases, and migration. Each profile keeps its own operation ID, lock, result, retry eligibility, and recovery path.

The batch coordinator provides:

- bounded concurrency and admission control;
- dry-run/validation for consequential operations where useful;
- per-item progress, error, cancellation, and retry;
- aggregate summary that never hides partial failure;
- no cross-profile transaction claim;
- safe pause when resource or security policy triggers.

### 5. Local REST API

Expose application use cases, not raw implementation adapters. Initial resources may cover profile CRUD/query, lifecycle operations, supported proxy/cookie actions, automation job submission, and operation status.

Required controls:

- disabled or loopback-only by default according to approved product policy;
- strong scoped token, rotation/revocation, and protected storage;
- explicit API/protocol version;
- request body, rate, concurrency, and resource bounds;
- Origin/browser-request defenses where applicable;
- idempotency keys for mutating long operations;
- sanitized errors and auditable security events;
- no token in URL query or normal logs.

### 6. Playwright automation

Automation obtains a lease through application policy and attaches only to the intended running profile. It cannot alter immutable identity, bypass locks, select unqualified cores, access another profile, or write the database directly.

Define:

- session/lease creation and expiry;
- ownership and cancellation;
- allowed browser operations/capabilities;
- navigation/download/upload policy;
- page-event and error reporting;
- browser/profile shutdown interaction;
- resource quotas and cleanup after client disconnect.

### 7. Human typing (Phase 4B optional)

Provide Unicode, IME, clipboard, input, textarea, and contenteditable-aware behavior through approved browser/UI mechanisms. Timing policy must be configurable and testable; it must not be marketed as human indistinguishability.

### 8. Basic Cookie Bot (Phase 4B optional)

Support per-profile URL lists, navigation/consent/scroll rules, timeouts, retry, job log, proxy bandwidth/resource limits, and cancellation. Reused schedules or behavior across profiles are an explicit correlation risk and must not be described as natural browsing.

### 9. Run with Sync prototype (Phase 4B optional)

Mirror semantic intent rather than raw coordinates:

- leader navigation intent;
- stable locator plus action intent;
- field identity and value entry policy;
- per-follower precondition/result;
- stop/pause on divergence, CAPTCHA, 2FA, authentication, or destructive action;
- no promise that simultaneous behavior is safe from correlation.

The prototype may be rejected or deferred without blocking the rest of Phase 4.

## Acceptance scenarios

Planned evidence for these scenarios uses the `AT-P4-*` identifiers in the [Requirement Catalogue](../REQUIREMENTS.md).

- Install a valid core beside the active core and reject tampered, replayed, stale, wrong-platform, or untrusted artifacts.
- Qualify a candidate without changing any production profile pointer.
- Migrate a canary, observe expected semantic changes, commit atomically, then demonstrate the approved rollback path on an injected failure.
- Keep pinned profiles on their core while other profiles migrate.
- Execute a batch with mixed validation, runtime, cancellation, and recovery outcomes and report each accurately.
- Reject local API calls with missing, invalid, expired, revoked, or insufficient-scope tokens.
- Reconcile an API timeout without launching a duplicate browser or job.
- End an automation lease and prove profile/process resources are cleaned according to policy.
- Pause Cookie Bot and Run with Sync on defined unsafe/divergent states.

## Test obligations

- Update metadata/artifact tamper, replay, downgrade, interruption, and key-rotation tests.
- Two-core qualification, migration, semantic diff, data-compatibility, and rollback tests.
- Batch scheduler property/stress tests and resource admission tests.
- Local API authentication, authorization, CSRF/Origin/DNS-rebinding where applicable, rate, idempotency, fuzz, and denial tests.
- Automation lease isolation, cancellation, disconnect, and lifecycle-race tests.
- Unicode/IME/contenteditable typing fixtures.
- Cookie Bot navigation/timeout/proxy/resource tests.
- Run with Sync divergence, CAPTCHA/2FA stop, and partial-result tests.
- Regression that all new logs and diagnostic events obey redaction.

## Exit criteria

- Candidate cores cannot activate without verified provenance and successful qualification.
- Per-profile migration produces a semantic report and preserves a tested rollback path.
- Stable Automatic, Manual Approval, and Pinned policies behave distinctly and predictably.
- Bulk operations are bounded, independently recoverable, and transparent about partial failure.
- Local API security tests pass and no endpoint bypasses application use cases.
- Automation leases cannot cross profile boundaries or mutate identity policy.
- Each Phase 4B behavior that is accepted meets its functional and safety criteria without overstated anti-detection claims; otherwise it is explicitly deferred or rejected.
- No critical supply-chain, migration, API, automation, or resource defect remains.
- Phase 5 receives operational measurements, release candidates, and stable capability metadata.

## Risks and controls

| Risk | Control |
|---|---|
| New core migrates data irreversibly | Verified pre-migration snapshot and `AUD-020`-approved restore/direct rollback path |
| Update channel compromise | Independent trust roots, authenticated metadata, immutable artifact identity, fail closed |
| Bulk action causes resource storm | Admission controller, concurrency limits, queue visibility and cancellation |
| Local API is treated as trusted because it is loopback | Strong scoped authentication and full `AUD-018` abuse suite |
| Automation bypasses lifecycle | Application-owned lease and all commands routed through use cases |
| Synced behavior links profiles | Optional feature, semantic divergence controls, explicit warning and no safety claim |

## Handoff to Phase 5

The handoff includes update trust and qualification records, supported core matrix, migration/rollback evidence, batch/automation resource measurements, API threat-test results, capability registry inputs, diagnostic event coverage, and release-candidate workflows.

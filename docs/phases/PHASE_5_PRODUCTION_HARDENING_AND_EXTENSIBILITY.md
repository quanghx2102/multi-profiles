# Phase 5 — Production Hardening and Engine Extensibility

## Status

`PLANNED`.

## Objective

Convert the feature-complete local product into a supportable Windows release with a defensible trust chain, bounded resource behavior, secure diagnostics, repeatable release operations, and an evidence-backed decision on adding a Chromium-family engine.

## Entry criteria

- Phase 4 core update, rollback, automation, bulk, and API gates pass.
- Representative operating history and resource/diagnostic data exist.
- Windows security-tool compatibility (`AUD-017`) and upstream sustainability (`AUD-023`) are ready for release-level decisions.
- A current Chromium candidate set is selected for `AUD-025`; stale rankings from the original conversation are not reused as evidence.
- Release ownership, signing authority, support policy, and security-response roles are assigned.

## Dependencies and assumptions

- Stable Phase 4 release candidates, operational telemetry, and full regression suites.
- Approved Windows code-signing service/key custody and artifact publication channel.
- Clean supported Windows environments for installer, reputation, and security-tool testing.
- Named security, release, incident, and upstream-maintenance owners.
- Current source/artifacts for any Chromium candidate; candidate availability is not assumed.

## In scope

- Signed Windows installer and update artifacts.
- Code-signing key custody, rotation, revocation, and release authorization.
- Defender/SmartScreen/antivirus compatibility validation.
- Security review and threat-model closure.
- Resource scheduler, admission policy, memory/process watchdog, and safe degradation.
- Redacted diagnostic bundle and reproducible support workflow.
- Release, rollback, incident, vulnerability, and documentation-consistency processes.
- Capability registry based on observed adapter behavior.
- Chromium adapter technical spike and independent go/no-go ADR.
- Long-term Camoufox upstream/fork maintenance plan.

## Out of scope

- Building cloud sync, team/workspace, public remote browser, mobile applications, or a proxy network.
- Declaring a Chromium engine production-ready solely because an adapter compiles.
- Converting an existing Camoufox identity/profile in place to Chromium.
- Weakening common contracts to the least capable engine.
- Marketing claims unsupported by repeatable qualification evidence.

## Phase deliverables

- Signed Windows installer/updater and verified release trust chain.
- Closed or accepted security-review findings and incident procedures.
- Resource scheduler, admission policy, and process/memory watchdog.
- Redacted user-reviewable diagnostic bundle.
- Repeatable release, rollback, vulnerability, SBOM/license, and documentation processes.
- Camoufox upstream/fork maintenance plan.
- Evidence-backed capability registry.
- Chromium adapter spike report and separate go/no-go ADR.

## Workstreams

### 1. Windows packaging, signing, and reputation

- Produce reproducible or independently verifiable release inputs where practical.
- Sign installer, updater, trusted executables, and relevant metadata under an approved key-custody process.
- Verify signature before install/update execution.
- Test clean install, upgrade, repair, uninstall, rollback, and interrupted operations.
- Ensure uninstall does not silently delete user profiles or keys without explicit policy.
- Run the `AUD-017` clean-VM matrix and establish false-positive response procedures.

### 2. Security hardening and review

Review renderer IPC, sidecar transport, local API, updater, import/export, path handling, extension behavior, browser sandbox assumptions, keychain usage, logs, crash dumps, and diagnostic bundles.

Required outcomes:

- updated threat model with trust boundaries and abuse cases;
- resolved critical/high findings or formally accepted bounded risks;
- vulnerability intake and supported-version policy;
- dependency and artifact inventory/SBOM process;
- release secret scanning and signing verification;
- incident containment and update revocation procedure.

### 3. Resource scheduler and watchdog

Use Phase 1/4 measurements to enforce a supported envelope rather than promising arbitrary profile counts.

The scheduler considers:

- host memory/CPU/GPU/handle availability;
- browser, migration, snapshot, Cookie Bot, and automation workloads;
- per-profile priority and user overrides within safe bounds;
- queued, admitted, paused, throttled, and rejected states;
- fairness and cancellation;
- measured recovery after resource exhaustion.

The watchdog observes process liveness and resource thresholds but does not rewrite identity, accept baselines, or kill processes without journaling and recovery policy.

### 4. Diagnostics and support bundle

Generate an allowlisted bundle containing version/capability metadata, sanitized configuration shape, operation/event timeline, process exits, semantic fingerprint diff, update/migration records, and environment descriptors needed to reproduce failures.

It excludes cookies, tokens, credentials, profile secret/seeds, page content by default, raw authenticated URLs, saved form data, and unreviewed browser profile files. Bundle creation produces a manifest and redaction report and supports user review before sharing.

### 5. Release engineering

Define:

- branch/version/support policy;
- build and test provenance;
- release-candidate qualification matrix;
- staged application and core rollout;
- rollback and emergency stop;
- schema compatibility window;
- release notes and known-limitations format;
- documentation/link/contract consistency checks;
- post-release monitoring and regression triage;
- end-of-support behavior for old app/core versions.

### 6. Camoufox maintenance strategy

Close the release-level review of `AUD-023`:

- upstream pin/update cadence;
- security patch intake;
- contribution policy;
- local patch inventory and rebase cost;
- criteria and staffing for a maintained fork;
- contingency if upstream pauses or changes direction;
- supported-core retirement policy.

### 7. Capability registry

Publish machine-readable and user-visible capabilities from adapter qualification, not engine-name assumptions. Each entry includes engine/adapter/core/protocol version constraints, platform, evidence/qualification reference, limits, and deprecation state.

Application features query capabilities; they do not scatter `if Camoufox`/`if Chromium` logic through domain policy.

### 8. Chromium adapter spike

Treat `AUD-025` as a fresh engine evaluation. Audit current candidate source, patch depth, build/release provenance, licensing, maintenance, launcher/automation interfaces, deterministic identity, context propagation, persistence, isolation, proxy behavior, crash recovery, update/rollback, and resource cost.

Apply the common engine contract and the same assurance categories used for Camoufox. Record any contract change as one of:

- genuinely engine-neutral behavior discovered by two implementations;
- adapter-specific capability/constraint;
- product policy that stays above the contract;
- rejected abstraction leakage.

The spike ends with a separate ADR choosing `GO`, `CONDITIONAL GO`, `HOLD`, or `NO-GO`. A Chromium profile is always a new profile with a new identity. Only explicitly compatible user data/configuration may be copied.

## Release acceptance scenarios

- Install and update a signed release on clean supported Windows machines; reject tampered/unsigned substitutions.
- Interrupt install/update at defined boundaries and recover without profile loss.
- Exercise Defender, SmartScreen, and representative antivirus flows without requiring users to disable protection.
- Saturate supported workloads and prove scheduler admission and watchdog recovery preserve profile integrity.
- Generate a diagnostic bundle from seeded sensitive fixtures and prove prohibited data is absent.
- Revoke/rotate an update or signing trust input through the documented incident procedure.
- Reproduce a release from recorded source/artifact/test provenance to the defined assurance level.
- Run a Chromium candidate through the common contract without modifying Camoufox profile identity in place.

## Test obligations

- Installer/update signature, tamper, upgrade, repair, uninstall, interruption, and rollback tests.
- Clean-VM Defender/SmartScreen/AV matrix.
- Full threat-model abuse/regression suite across all trust boundaries.
- Resource saturation, queue fairness, watchdog, low-disk/memory, and recovery tests.
- Diagnostic-bundle allowlist, redaction, size, corruption, and user-review tests.
- Release pipeline provenance, SBOM/license, secret, and documentation consistency checks.
- Sustained/soak operation with representative concurrent profiles and automation.
- Full common engine contract and qualification suite for the Chromium spike.

## Exit criteria

- Installer and updater trust chain is documented, signed, tested, and recoverable.
- Supported Windows/security-tool matrix and known limitations are published.
- No unresolved critical security finding remains; accepted risks have owners and review dates.
- Resource scheduler/watchdog enforce a measured concurrency/workload envelope without identity or state corruption.
- Diagnostic bundles are useful for reproduction and pass seeded-secret redaction tests.
- Release, rollback, vulnerability, upstream-maintenance, and documentation processes are repeatable.
- Capability registry accurately represents qualified behavior.
- Chromium spike has an evidence-backed ADR and does not weaken immutable engine binding or domain independence.
- Product claims remain within browser-level isolation and measured consistency evidence.

## Risks and controls

| Risk | Control |
|---|---|
| Signing key compromise | Hardware/managed custody, limited release authority, rotation/revocation drill |
| SmartScreen or AV blocks launch/update | Signed staged releases, clean-VM matrix, vendor false-positive process |
| Scheduler kills during unsafe write | Checkpoint-aware policy, journaling, graceful pressure response before termination |
| Diagnostic bundle leaks sessions | Strict allowlist, seeded-secret regression, user review, no raw profile files |
| Upstream browser security burden grows | Pinning cadence, patch inventory, contribution/fork contingency and support window |
| Second engine distorts architecture | Shared contract tests, capability registry, ADR review, immutable engine binding |

## Post-Phase 5 posture

Phase 5 completes the defined local-first product roadmap, not every possible GoLogin feature. Cloud, teams, mobile, remote browsers, proxy infrastructure, or additional engines require separate product scope, threat model, architecture decisions, and phases.

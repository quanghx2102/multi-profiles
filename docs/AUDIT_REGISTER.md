# Audit Register

## Evidence policy

This register is the authority for technical uncertainty. The shared design conversation is a source of hypotheses and decisions, not accepted Camoufox source/test evidence. No Camoufox source was audited and no runtime experiment was executed while creating this baseline.

Allowed statuses: `NOT_STARTED`, `RESEARCHING`, `TEST_READY`, `BLOCKED`, `CONFIRMED`, `PATCH_REQUIRED`, `RESOLVED`, `ACCEPTED_RISK`, `REJECTED`.

Evidence quality: `NONE`, `HYPOTHESIS`, `DOCUMENTED`, `SOURCE_CONFIRMED`, `TEST_CONFIRMED`, `MULTI_ENV_CONFIRMED`.

An item may become `CONFIRMED` only when its question has a supported answer. `RESOLVED` additionally requires the required decision/patch and regression coverage. Evidence records must identify exact source revisions or test artifacts.

## Phase 2 blocking summary

Phase 2 is blocked by: `AUD-001`, `AUD-002`, `AUD-003`, `AUD-004`, `AUD-005`, `AUD-006`, `AUD-007`, `AUD-008`, `AUD-012`, `AUD-013`, `AUD-014`, `AUD-015`, `AUD-016`, `AUD-019`, `AUD-022`, `AUD-023`, and `AUD-024`. A go/no-go review may explicitly reject or accept a bounded risk, but may not treat missing evidence as confirmation.

## Items

### AUD-001 — Inventory all Camoufox random-seed sources

- **Category:** Identity determinism
- **Question:** Which Camoufox, launcher, BrowserForge, Firefox, and host paths introduce randomness into configured or observed fingerprint surfaces?
- **Why it matters:** Uncontrolled randomness can change a profile identity after restart.
- **Current hypothesis:** More random inputs may exist than the planned manifest fields cover.
- **Known evidence:** No evidence accepted; the conversation only identified this risk.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Exact pinned Camoufox source, patches, launcher source, fingerprint generator dependencies, defaults, and release notes.
- **Test procedure:** Trace random sources and configuration consumers; instrument two identically configured launches and repeated relaunches; map every varying observation to a source or host dependency.
- **Test environments:** Supported Windows versions; at least two hardware/GPU configurations; pinned core and launcher revisions.
- **Expected result:** Complete inventory with controllable, intentionally random-per-profile, host-derived, and uncontrolled classifications.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Identity drift and false persistence guarantees.
- **Blocks phase:** Phase 2
- **Required decision:** Define the minimum deterministic surface set and Camoufox go/no-go condition.
- **Required patch:** TBD from source evidence; fail fast for any required uncontrolled seed.
- **Regression test:** Seed-inventory assertion plus 50-restart fingerprint suite.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Coordinate with `AUD-002`, `AUD-003`, and `AUD-019`.

### AUD-002 — Canvas, Audio, WebGL, and ClientRects persistence

- **Category:** Identity persistence
- **Question:** Do these surfaces remain within approved semantic baselines across clean and crash relaunches using the same identity and data directory?
- **Why it matters:** These are central promised identity surfaces.
- **Current hypothesis:** Persistence may vary by surface, launcher path, and host rendering.
- **Known evidence:** No accepted source or test evidence.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Pinned engine patches, surface configuration schema/consumers, launcher mapping, and relevant upstream tests/issues.
- **Test procedure:** Establish a baseline, perform 50 clean relaunches and crash/recovery relaunches, compare normalized values and raw artifacts.
- **Test environments:** Two Windows builds and at least two GPU/driver families; stable hardware and controlled locale/network.
- **Expected result:** No unexplained immutable-input drift; render-derived variance is bounded and documented.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Same profile appears as different devices.
- **Blocks phase:** Phase 2
- **Required decision:** Accept/reject each surface and define preflight rules.
- **Required patch:** TBD; adapter/configuration or upstream patch if a required surface is not persistent.
- **Regression test:** 50-restart matrix per qualified core.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Raw fingerprint hash equality alone is insufficient.

### AUD-003 — Fingerprint propagation to iframe, worker, service worker, and worklet

- **Category:** Cross-context consistency
- **Question:** Are configured identity values consistently visible in all relevant browser execution contexts?
- **Why it matters:** Context disagreement is a strong coherence defect.
- **Current hypothesis:** Coverage may differ by API and context; worklet support may be partial.
- **Known evidence:** No accepted source or test evidence.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Engine patches and tests for window, iframe, worker globals, service workers, worklets, and process boundaries.
- **Test procedure:** Run the same versioned probe in main frame, same/cross-origin iframe where feasible, dedicated/shared worker, service worker, and applicable worklets.
- **Test environments:** Supported Windows matrix; clean and persistent profiles; one and multiple processes.
- **Expected result:** Required surfaces agree semantically across every supported context; unsupported contexts are explicit capabilities.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Detectable internal inconsistency and failed preflight coverage.
- **Blocks phase:** Phase 2
- **Required decision:** Approve context coverage or reject/patch the engine.
- **Required patch:** TBD per missing context consumer.
- **Regression test:** Cross-context probe suite on every core qualification.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Depends on the probe inventory in `AUD-019`.

### AUD-004 — Multi-process Camoufox interference

- **Category:** Isolation and concurrency
- **Question:** Can multiple Camoufox process trees with separate profiles interfere through shared ports, temp files, caches, singleton behavior, configuration, or launcher state?
- **Why it matters:** One-process-per-profile is only useful if instances are actually independent.
- **Current hypothesis:** Undocumented global resources or launcher assumptions may create interference.
- **Known evidence:** No accepted source or reproducible test evidence.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Launcher/process setup, runtime-directory logic, environment variables, IPC endpoints, temp/cache paths, upstream multi-instance reports.
- **Test procedure:** Start/stop/crash 2, 5, 10, and where feasible 20 profiles with unique sentinels and randomized interleavings; inspect resources and cross-effects.
- **Test environments:** Windows test hosts representing supported hardware; clean user account and realistic long-lived account.
- **Expected result:** No cross-profile state/config/process effect; resource collisions have explicit prevention.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Cross-profile contamination or browser failure.
- **Blocks phase:** Phase 2
- **Required decision:** Confirm one-process-per-profile feasibility and safe concurrency limit.
- **Required patch:** TBD; isolate every shared runtime resource or cap concurrency.
- **Regression test:** Concurrent lifecycle/isolation stress suite.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Resource capacity is measured separately in `AUD-014`.

### AUD-005 — `user_data_dir` persistence inventory

- **Category:** Browser state
- **Question:** Which cookies, storage types, history, preferences, permissions, certificates, extension state, and other data persist or do not persist in Camoufox's user data directory?
- **Why it matters:** Stop/start, backup, and restore promises depend on exact ownership and flush behavior.
- **Current hypothesis:** Persistence is not uniform and some state may live outside the directory or require graceful shutdown.
- **Known evidence:** No accepted inventory or test evidence.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Camoufox launcher/profile handling, Firefox profile documentation/source relevant to the pinned core, cleanup logic, upstream persistence tests/issues.
- **Test procedure:** Seed each storage/state type, clean-stop and crash, relaunch, snapshot/restore, and verify both persistence and cross-profile absence.
- **Test environments:** Supported Windows builds; clean and upgraded profiles; representative extension fixtures.
- **Expected result:** Versioned state inventory with backup inclusion, checkpoint, and recovery policy per type.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Session loss, leakage, or invalid backups.
- **Blocks phase:** Phase 2
- **Required decision:** Define supported persistent state and explicit exclusions.
- **Required patch:** TBD; storage/checkpoint adapter or documented unsupported state.
- **Regression test:** Persistent-state matrix for clean stop, crash, snapshot, and restore.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Feeds Phase 3 export rules.

### AUD-006 — Generic-font nondeterminism on Windows

- **Category:** Fingerprint surface
- **Question:** Are generic-font selection, metrics, enumeration, and rendered outputs deterministic for a profile on supported Windows hosts?
- **Why it matters:** Font-dependent rendering can drift despite stable explicit seeds.
- **Current hypothesis:** Installed fonts, fallback, language packs, and rendering stack may remain host-dependent.
- **Known evidence:** No accepted source or test evidence.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Camoufox font patches/configuration, Firefox font selection, launcher inputs, and dependency datasets.
- **Test procedure:** Probe font enumeration/fallback/metrics across relaunches and controlled host font changes; compare two hosts.
- **Test environments:** Multiple Windows versions, language packs, DPI settings, and font inventories.
- **Expected result:** Controlled surfaces are stable; remaining host dependence is detectable and bounded.
- **Observed result:** Not observed.
- **Severity:** High
- **Probability:** Unknown
- **Impact:** Identity drift and cross-machine mismatch.
- **Blocks phase:** Phase 2
- **Required decision:** Define supported font policy and portability limits.
- **Required patch:** TBD; bundled/configured fonts or host-compatibility gate if permitted.
- **Regression test:** Font matrix and host-change preflight.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Coordinate with `AUD-010` and `AUD-022`.

### AUD-007 — WebGL preset coverage, crash, and mismatch

- **Category:** GPU/WebGL
- **Question:** Which WebGL parameters are controlled, coherent, unsupported, or crash-prone for each preset and host GPU/driver?
- **Why it matters:** String spoofing without behavioral coherence can expose contradictions or destabilize the browser.
- **Current hypothesis:** Preset coverage and stability vary by host GPU/driver and API path.
- **Known evidence:** No accepted source or test evidence.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** WebGL/GPU patches, preset dataset, validation logic, crash reports, and engine tests for the pinned revision.
- **Test procedure:** Enumerate parameters/extensions, render fixtures, stress contexts, test invalid combinations, crash recovery, and cross-context agreement.
- **Test environments:** Representative Intel/AMD/NVIDIA hardware and drivers on supported Windows.
- **Expected result:** Supported preset matrix with coherent results, rejection rules, and no unexplained crashes.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Detection, browser crashes, or unusable profiles.
- **Blocks phase:** Phase 2
- **Required decision:** Approve a bounded preset catalogue or reject affected configurations.
- **Required patch:** TBD in adapter, dataset, or engine.
- **Regression test:** GPU/preset qualification suite for each core.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Never infer support from vendor/renderer strings alone.

### AUD-008 — HTTP/HTTPS/SOCKS proxy, DNS, and WebRTC leakage

- **Category:** Network privacy
- **Question:** Does per-profile proxy configuration cover supported request paths without DNS, WebRTC, authentication, or bypass leakage?
- **Why it matters:** Browser identity and network location must not contradict the selected proxy policy.
- **Current hypothesis:** Behavior differs by proxy scheme, DNS mode, WebRTC configuration, and failure condition.
- **Known evidence:** No accepted source or test evidence.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Launcher proxy mapping, Firefox networking/WebRTC settings used by Camoufox, authentication handling, and upstream tests/issues.
- **Test procedure:** Exercise HTTP, HTTPS, SOCKS variants, auth, DNS endpoints, WebRTC candidates, redirects, websockets, downloads, service workers, proxy outage, and direct-bypass attempts.
- **Test environments:** Controlled proxy/DNS/WebRTC observation servers and supported Windows hosts.
- **Expected result:** Explicit supported matrix; no direct route under strict mode; failures are closed and diagnosable.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Real IP/DNS disclosure and identity incoherence.
- **Blocks phase:** Phase 2
- **Required decision:** Approve schemes/modes and fail-closed policy.
- **Required patch:** TBD; adapter preferences, network policy, or unsupported-mode rejection.
- **Regression test:** Automated proxy/leak matrix per core.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Proxy reputation is outside product guarantees.

### AUD-009 — Fingerprint drift between Camoufox 152 and the next version

- **Category:** Core migration
- **Question:** What configured and observed fingerprint changes occur between the pinned 152-series core and the next candidate core?
- **Why it matters:** Staged updates require known semantic changes and rollback criteria.
- **Current hypothesis:** Some browser-version-derived change is legitimate, while unexplained identity or render drift may occur.
- **Known evidence:** No accepted cross-version evidence; exact candidate versions must be pinned during audit.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Exact release diffs, patch/config schema changes, datasets, launcher compatibility notes, and Firefox changes.
- **Test procedure:** Run the same profiles and probe schema on both cores, generate semantic diffs, repeat, then roll back.
- **Test environments:** Supported Windows/GPU matrix with retained 152-series and candidate artifacts.
- **Expected result:** Classified diff rules and migration/rollback compatibility report.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** High
- **Impact:** Fleet-wide identity drift or broken profiles after update.
- **Blocks phase:** Phase 4
- **Required decision:** Approve, patch, pin, or reject the candidate core.
- **Required patch:** TBD from semantic diff.
- **Regression test:** Two-core migration matrix for every promoted release.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Do not hard-code “153” until an actual candidate is selected.

### AUD-010 — Portability across two Windows machines with different hardware

- **Category:** Portability
- **Question:** Which identity and browser-state properties survive transfer between Windows machines with different CPU/GPU/fonts/drivers?
- **Why it matters:** Export must not imply device-identity preservation when host surfaces dominate.
- **Current hypothesis:** Some render-derived and host-dependent surfaces will change.
- **Known evidence:** No accepted portability test evidence.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Identity inputs, host probes, engine patches, profile manager behavior, and portability documentation at pinned revisions.
- **Test procedure:** Export on host A, import on host B, compare manifest, state, all contexts, network policy, and semantic baseline; repeat reverse direction.
- **Test environments:** Two or more Windows hosts with intentionally different hardware, GPU drivers, fonts, DPI, and locale.
- **Expected result:** Supported compatibility envelope and explicit incompatible/changed surfaces.
- **Observed result:** Not observed.
- **Severity:** High
- **Probability:** High
- **Impact:** Misleading transfer guarantee and account correlation risk.
- **Blocks phase:** Phase 3
- **Required decision:** Define same-host, compatible-host, and unsupported transfer policies.
- **Required patch:** TBD; compatibility checks or manifest constraints.
- **Regression test:** Cross-host portability matrix.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Related to `AUD-006`, `AUD-021`, and `AUD-022`.

### AUD-011 — Firefox extension compatibility

- **Category:** Extensions
- **Question:** Which Firefox extensions and extension-state operations work safely with Camoufox profiles and automation?
- **Why it matters:** Extension management is a Phase 3 capability and can affect identity, security, and persistence.
- **Current hypothesis:** Compatibility and persistence vary; privileged or fingerprint-changing extensions may be unsafe.
- **Known evidence:** No accepted compatibility matrix.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Camoufox extension behavior/docs, Firefox WebExtensions compatibility, profile packaging, and selected extension manifests.
- **Test procedure:** Install, enable/disable, update, persist settings, restart, snapshot/restore, and exercise representative permission classes.
- **Test environments:** Supported Windows/core matrix with curated test extensions.
- **Expected result:** Allow/support matrix, permission warnings, persistence rules, and rejected classes.
- **Observed result:** Not observed.
- **Severity:** Medium
- **Probability:** Unknown
- **Impact:** Broken profiles, data exposure, or fingerprint changes.
- **Blocks phase:** Phase 3
- **Required decision:** Define supported extension lifecycle and safety policy.
- **Required patch:** TBD; extension manager restrictions or adapter support.
- **Regression test:** Curated extension compatibility suite.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Extension code is untrusted.

### AUD-012 — TypeScript launcher lifecycle and Python parity

- **Category:** Sidecar technology
- **Question:** Does the Camoufox TypeScript launcher support the required persistent lifecycle and features with reliability equal to or better than the Python launcher?
- **Why it matters:** This selects the initial sidecar implementation language without coupling Rust policy to it.
- **Current hypothesis:** The launchers may differ in maturity, configuration coverage, and lifecycle behavior.
- **Known evidence:** No accepted parity matrix or source audit.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Both official launcher sources, tests, schemas, releases, dependency constraints, and issue history at pinned revisions.
- **Test procedure:** Run identical create/start/stop/persist/proxy/probe/error scenarios and compare features, events, crashes, and recovery.
- **Test environments:** Supported Windows versions with identical Camoufox core artifacts.
- **Expected result:** Evidence-backed sidecar language decision and documented gaps.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Unstable lifecycle or missing configuration features.
- **Blocks phase:** Phase 2
- **Required decision:** Select TypeScript or Python and document fallback conditions.
- **Required patch:** TBD; wrapper/adapter gaps only after parity is known.
- **Regression test:** Shared launcher conformance suite.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** TypeScript is preferred only if evidence supports it.

### AUD-013 — Crash consistency during Start, Stop, and snapshot

- **Category:** Recovery
- **Question:** Can application, sidecar, and browser crashes at each lifecycle boundary be reconciled without identity regeneration, unsafe snapshot, or false state?
- **Why it matters:** Browser and database state span multiple processes and filesystems.
- **Current hypothesis:** Naive sequencing will leave uncertain states requiring a durable journal and reconciliation.
- **Known evidence:** Architecture hypothesis only; no fault-injection evidence.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Chosen launcher shutdown semantics, browser profile flush behavior, planned storage primitives, and Windows process behavior.
- **Test procedure:** Inject termination and IO/transaction faults before and after each durable boundary; restart and reconcile.
- **Test environments:** Supported Windows filesystems; normal and resource-pressure conditions.
- **Expected result:** One deterministic safe state or explicit quarantine for every fault point.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** High
- **Impact:** Corrupt browser state, unsafe backup, duplicate process, or lost identity.
- **Blocks phase:** Phase 2
- **Required decision:** Approve journal/checkpoint protocol and forced-stop policy.
- **Required patch:** TBD in lifecycle, storage, or supervisor design.
- **Regression test:** Fault-injection matrix for every lifecycle operation.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Timeouts are uncertain outcomes, not failures-before-effect.

### AUD-014 — Resource benchmark for 1/5/10/20 profiles

- **Category:** Capacity and performance
- **Question:** What RAM, CPU, GPU, handle, process, startup, and shutdown costs occur at 1, 5, 10, and 20 concurrent profiles?
- **Why it matters:** One process per profile may exceed practical host capacity and requires scheduling limits.
- **Current hypothesis:** Cost is nonlinear under GPU/process contention and workload matters.
- **Known evidence:** No accepted benchmark evidence.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Browser/launcher process model, configured feature defaults, and benchmark methodology references.
- **Test procedure:** Measure idle, navigation, scripted workload, and stop phases at each concurrency level; record distributions and failures.
- **Test environments:** At least low/mid/high supported Windows hardware tiers with fixed workload and thermal conditions.
- **Expected result:** Published capacity envelope and inputs for scheduler/watchdog policy.
- **Observed result:** Not observed.
- **Severity:** High
- **Probability:** High
- **Impact:** Host instability, crashes, or unusable concurrency.
- **Blocks phase:** Phase 2
- **Required decision:** Set initial supported concurrent-profile limit and admission policy.
- **Required patch:** TBD; scheduling/caps or process configuration.
- **Regression test:** Release benchmark with threshold comparison.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Twenty profiles is a measurement target, not a promised supported limit.

### AUD-015 — MPL/LGPL/MIT distribution obligations

- **Category:** Licensing and distribution
- **Question:** What obligations apply when distributing Camoufox, Firefox-derived binaries, launcher/dependencies, modifications, and this application?
- **Why it matters:** The product cannot ship legally without a compliant source, notice, and relinking/distribution plan where applicable.
- **Current hypothesis:** Multiple licenses and binary/source-offer obligations may apply; exact conclusions require qualified review.
- **Known evidence:** No license inventory or legal conclusion accepted in this repository.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Exact license files, notices, dependency manifests, binary contents, patch history, upstream distribution terms, and official license texts.
- **Test procedure:** Build a software bill of materials and map each shipped artifact/file/modification to obligations; obtain legal review before distribution.
- **Test environments:** Planned Windows installer/update and source-distribution channels.
- **Expected result:** Approved compliance matrix, notice bundle, source availability procedure, and prohibited combinations if any.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Inability to distribute, takedown, or forced redesign.
- **Blocks phase:** Phase 2
- **Required decision:** Go/no-go for distribution model and modification strategy.
- **Required patch:** Compliance packaging/process changes; code changes only if required.
- **Regression test:** Automated license/SBOM/notice check in release pipeline plus periodic legal review.
- **Owner:** Unassigned; legal counsel required
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** This item records engineering due diligence, not legal advice.

### AUD-016 — Core download, checksum, and signature verification

- **Category:** Supply-chain security
- **Question:** What authenticated metadata and signatures are available for Camoufox core artifacts, and how can the updater establish provenance and prevent substitution/downgrade?
- **Why it matters:** The application executes downloaded browser binaries with access to sensitive profile data.
- **Current hypothesis:** Checksums may be available but the complete trust/signature model is unknown.
- **Known evidence:** No release-channel or verification audit accepted.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Official release publishing workflow, release metadata/assets, signing keys/procedures, checksums, updater/launcher download code, and hosting controls.
- **Test procedure:** Verify known artifacts, tamper metadata/artifacts, replay/downgrade versions, rotate keys, and test offline/failed verification behavior.
- **Test environments:** Controlled update server fixtures plus actual pinned official release channel.
- **Expected result:** Documented trust roots, verified metadata chain, fail-closed behavior, and recovery/key-rotation plan.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Arbitrary code execution or malicious downgrade.
- **Blocks phase:** Phase 2 for initial artifact trust; Phase 4 for automated update
- **Required decision:** Select artifact source and verification policy or require separately provisioned cores.
- **Required patch:** Updater/verifier implementation or upstream release-process improvement.
- **Regression test:** Tampered, stale, replayed, and valid artifact fixtures.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** A checksum fetched from the same unauthenticated source is not independent trust.

### AUD-017 — Windows Defender, SmartScreen, and antivirus compatibility

- **Category:** Windows distribution
- **Question:** How do packaged application, sidecar, Camoufox processes, updates, and profile operations behave under Defender, SmartScreen, and representative antivirus tools?
- **Why it matters:** Quarantine or reputation warnings can break launches, updates, and data consistency.
- **Current hypothesis:** Unsigned/unfamiliar browser and sidecar binaries may receive warnings or quarantine.
- **Known evidence:** No accepted compatibility evidence.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Planned packaging/signing design, vendor guidance, exact artifact reputation/signature metadata, and upstream reports.
- **Test procedure:** Install, launch, update, snapshot, restore, uninstall, and scan signed candidate builds; record detections and file actions.
- **Test environments:** Clean supported Windows VMs with current Defender/SmartScreen and a documented representative AV set.
- **Expected result:** No unexplained detection; documented signing, reputation, exclusions support, and recovery behavior.
- **Observed result:** Not observed.
- **Severity:** High
- **Probability:** Unknown
- **Impact:** Failed installation/launch, deleted binaries, or profile damage.
- **Blocks phase:** Phase 5 release
- **Required decision:** Approve signing/distribution/reputation plan.
- **Required patch:** Packaging, signing, update, or process behavior changes as evidence requires.
- **Regression test:** Pre-release clean-VM security-tool matrix.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Do not recommend disabling security products as the product solution.

### AUD-018 — Local automation endpoint exposure and authentication

- **Category:** API security
- **Question:** Can another website, user, or local process discover or misuse the local automation API or sidecar endpoints?
- **Why it matters:** Automation authority can expose sessions and control browser profiles.
- **Current hypothesis:** Loopback binding alone is insufficient; token, origin, scope, and local-process threats remain.
- **Known evidence:** Security design hypothesis only; no endpoint exists yet.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Planned API/transport design, relevant framework defaults, Windows local IPC security, and browser request behavior.
- **Test procedure:** Attempt unauthenticated, cross-origin/DNS-rebinding, token replay, privilege/scope escalation, port race, brute-force, and local-process attacks.
- **Test environments:** Supported Windows users/sessions, browsers, hostile local/web fixtures, and firewall configurations.
- **Expected result:** Loopback-only default, strong scoped token, explicit enablement, robust validation, and auditable denial.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Unauthorized profile/session control.
- **Blocks phase:** Phase 4
- **Required decision:** Approve API threat model, transport, token lifecycle, and exposure UX.
- **Required patch:** API authentication/authorization and binding hardening.
- **Regression test:** Automated API abuse suite.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Sidecar transport security is also covered by `AUD-024`.

### AUD-019 — Fingerprint probe completeness

- **Category:** Verification
- **Question:** Does the probe inventory cover every identity field, important correlated surface, execution context, and host-dependent observation needed for preflight and migration?
- **Why it matters:** A preflight can pass while missing the surface that drifted.
- **Current hypothesis:** A naive browser-page probe will miss native, worker, network, timing, font, media, and GPU correlations.
- **Known evidence:** No approved inventory or coverage map.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Camoufox configuration/patch surface inventory, Browser/Firefox APIs, probe code references, and detection research limited to reproducible technical surfaces.
- **Test procedure:** Map each manifest/config field and patch to one or more observations; mutation-test the probe by deliberately altering each controllable input.
- **Test environments:** Supported Windows/core/context matrix with controlled mutations.
- **Expected result:** Versioned coverage map, known blind spots, normalization rules, and mandatory/optional observations.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** High
- **Impact:** False-green starts and unsafe migrations.
- **Blocks phase:** Phase 2
- **Required decision:** Approve minimum preflight and full qualification probe sets.
- **Required patch:** Add probes or declare unsupported assurance where observation is impossible.
- **Regression test:** Probe mutation/coverage suite.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Probe behavior itself must avoid materially changing the profile.

### AUD-020 — Core rollback without profile corruption

- **Category:** Migration and recovery
- **Question:** Can a profile opened by a newer Camoufox core be safely reopened by the retained older core, and under what data/schema constraints?
- **Why it matters:** Binary rollback is not useful if the newer browser irreversibly migrates profile data.
- **Current hypothesis:** Some browser profile changes may be backward-incompatible, requiring snapshot restore rather than direct reopen.
- **Known evidence:** No accepted two-core rollback evidence.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Firefox/Camoufox profile migrations for exact versions, launcher behavior, storage schemas, and upstream rollback guidance/tests.
- **Test procedure:** Snapshot, open with new core, exercise representative state, stop, attempt direct old-core reopen, then test snapshot-based rollback and compare integrity.
- **Test environments:** Supported Windows matrix and each proposed adjacent core pair.
- **Expected result:** Explicit direct-rollback or restore-required classification with no silent corruption.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Irrecoverable profile state after failed migration.
- **Blocks phase:** Phase 4; informs Phase 2 core pinning
- **Required decision:** Select rollback mechanism and retention requirements per core pair.
- **Required patch:** Migration isolation, snapshot restore, or version guard as required.
- **Regression test:** Forward-use/backward-restore matrix for every update.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Never test valuable user profiles first.

### AUD-021 — Same-OS import/export identity preservation

- **Category:** Portability
- **Question:** Does encrypted export/import on the same supported OS preserve intended identity and selected browser state without hidden host/path dependencies?
- **Why it matters:** Backup and transfer are the local-first alternative to cloud profile sharing.
- **Current hypothesis:** Same-OS portability is more feasible than cross-hardware portability but may still depend on paths, keychain data, permissions, or machine state.
- **Known evidence:** No accepted round-trip evidence.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** `AUD-005` inventory, identity/storage layout, launcher path assumptions, keychain model, and export design.
- **Test procedure:** Round-trip each mode with path/user changes, compare manifest, browser state, baselines, exclusions, and preflight results.
- **Test environments:** Same Windows host under new path and clean compatible Windows host; non-production fixtures.
- **Expected result:** Mode-specific fidelity matrix and explicit exclusions; no secret/plaintext leakage.
- **Observed result:** Not observed.
- **Severity:** High
- **Probability:** Unknown
- **Impact:** Backups that cannot restore or transfers that change identity.
- **Blocks phase:** Phase 3
- **Required decision:** Approve supported same-OS backup/transfer envelope.
- **Required patch:** Container, path rebasing, compatibility, or key-handling changes.
- **Regression test:** Encrypted round-trip suite for all three modes.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Duplicate-as-new is expected to change identity.

### AUD-022 — Uncontrolled host-dependent fingerprint surfaces

- **Category:** Identity assurance
- **Question:** Which observable surfaces remain dependent on host OS, hardware, drivers, fonts, clocks, media devices, or environment despite Camoufox configuration?
- **Why it matters:** The product must bound its consistency promise and block incoherent presets.
- **Current hypothesis:** Some host dependence is unavoidable and must be discovered by source mapping and cross-host tests.
- **Known evidence:** No accepted comprehensive inventory.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Full patch/config coverage, Firefox platform integrations, launcher inputs, and probe inventory.
- **Test procedure:** Hold identity constant while varying one host factor at a time; correlate source coverage with observed diffs across contexts.
- **Test environments:** Diverse Windows hardware, drivers, displays/DPI, fonts, locale, timezone, audio/media devices, and power modes.
- **Expected result:** Controlled/uncontrolled inventory, compatibility constraints, and preflight detection rules.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** High
- **Impact:** False device-stability guarantee and transfer drift.
- **Blocks phase:** Phase 2
- **Required decision:** Bound supported host configurations and identity guarantee.
- **Required patch:** Host compatibility gates, preset constraints, or engine patches as feasible.
- **Regression test:** Host-variance matrix and preflight mutation checks.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Umbrella item informed by `AUD-006`, `AUD-007`, and `AUD-010`.

### AUD-023 — Upstream maintenance and fork sustainability

- **Category:** Project sustainability
- **Question:** Is Camoufox maintained with sufficient release, review, build, patch-rebase, security, and issue-response practices, and can this project sustain a fork if needed?
- **Why it matters:** A browser fork is a continuous security and compatibility obligation, not a one-time dependency.
- **Current hypothesis:** Upstream may be active yet still impose material single-maintainer, beta, rebase, or release risk.
- **Known evidence:** No current repository-health audit accepted in this project.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Repository history, maintainers, releases, CI, build instructions, security policy, issue/PR cadence, Firefox rebase process, funding/governance, and dependency ownership.
- **Test procedure:** Reproduce a pinned build/release verification where permitted, analyze maintenance metrics qualitatively, and estimate fork staffing/rebase work.
- **Test environments:** Clean documented build environment and repository history snapshot.
- **Expected result:** Maintenance-risk assessment, upstream contribution plan, pinning policy, and fork/no-fork contingency.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Unpatched security flaws, stalled releases, or unsustainable product.
- **Blocks phase:** Phase 2 go/no-go; re-evaluate in Phase 5
- **Required decision:** Accept dependency risk, fund/contribute upstream, maintain fork, or reject engine.
- **Required patch:** Process/governance action; source changes only when justified.
- **Regression test:** Scheduled upstream-health and patch-rebase review per release cycle.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Popularity metrics alone are insufficient.

### AUD-024 — Sidecar protocol and crash recovery

- **Category:** Inter-process architecture
- **Question:** Which local transport, framing, authentication, version negotiation, idempotency, secret delivery, timeout, cancellation, event, and reconciliation semantics safely connect Rust and the sidecar?
- **Why it matters:** Process ambiguity can duplicate launches, leak authority, or lose lifecycle state.
- **Current hypothesis:** A request/response protocol needs explicit uncertain-outcome and process-adoption semantics; transport choice remains open.
- **Known evidence:** Architectural requirements only; no protocol spike or threat test.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Candidate Windows IPC transports/libraries, launcher event models, Playwright lifecycle, OS access controls, and relevant threat guidance.
- **Test procedure:** Prototype candidates; inject lost responses, duplicate requests, sidecar/core/browser crashes, stale endpoints, unauthorized clients, oversized frames, and version mismatch.
- **Test environments:** Supported Windows versions, multiple users/sessions where relevant, normal and crash/restart conditions.
- **Expected result:** Selected transport and versioned protocol with authenticated instance, typed errors, idempotency, deadlines, and deterministic reconciliation.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** High
- **Impact:** Duplicate browsers, unauthorized control, stuck locks, or false lifecycle state.
- **Blocks phase:** Phase 2
- **Required decision:** Accept protocol/transport and recovery state machine.
- **Required patch:** Implement the approved boundary in Phase 2; upstream launcher changes if required.
- **Regression test:** Protocol conformance, fuzz/property, authorization, and crash matrix.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Must stay language-neutral under ADR-0006.

### AUD-025 — Future Chromium adapter feasibility

- **Category:** Engine extensibility
- **Question:** Can a maintainable, distributable Chromium-family engine implement the common contract without weakening identity, isolation, security, or update guarantees?
- **Why it matters:** Engine neutrality is an architectural goal, but a premature abstraction or unsuitable binary would create false confidence.
- **Current hypothesis:** The architecture can host another adapter, but no Chromium implementation is selected or proven.
- **Known evidence:** The shared conversation discussed candidates, but no current source/test evidence is accepted here.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Candidate source, patches, build/release provenance, licenses, launcher/API, tests, maintenance, and fingerprint surface coverage at the future audit date.
- **Test procedure:** Apply the same source audit, engine contract, determinism, isolation, proxy, crash, resource, migration, and licensing suite used for Camoufox.
- **Test environments:** Future supported Windows matrix and candidate-specific build/runtime environments.
- **Expected result:** Separate go/no-go ADR and capability matrix; no in-place Camoufox profile conversion.
- **Observed result:** Not observed.
- **Severity:** Medium
- **Probability:** Unknown
- **Impact:** Rework or permanent Firefox-only product if abstractions are unsound.
- **Blocks phase:** Phase 5 Chromium spike, not Camoufox MVP
- **Required decision:** Select/reject candidate and validate contract changes without engine-name policy leaks.
- **Required patch:** Future adapter or contract refinement backed by two-engine evidence.
- **Regression test:** Shared engine contract suite plus Chromium-specific qualification.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** Reassess candidates at audit time; do not rely on stale repository rankings.

## Register maintenance

When work starts, update `Owner`, `Status`, dates, and evidence references. Store large raw artifacts outside this document and link them with hashes. New uncertainty receives a new stable ID; closed items are not renumbered or deleted.

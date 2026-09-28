# Audit Register

## Evidence policy

This register is the authority for technical uncertainty. The shared design conversation is a source of hypotheses and decisions, not accepted Camoufox source/test evidence. No Camoufox source was audited and no runtime experiment was executed while creating this baseline.

Allowed statuses: `NOT_STARTED`, `RESEARCHING`, `TEST_READY`, `BLOCKED`, `CONFIRMED`, `PATCH_REQUIRED`, `RESOLVED`, `ACCEPTED_RISK`, `REJECTED`.

Evidence quality: `NONE`, `HYPOTHESIS`, `DOCUMENTED`, `SOURCE_CONFIRMED`, `TEST_CONFIRMED`, `MULTI_ENV_CONFIRMED`.

An item may become `CONFIRMED` only when its question has a supported answer. `RESOLVED` additionally requires the required decision/patch and regression coverage. Evidence records must identify exact source revisions or test artifacts. New work uses the report conventions in [docs/audit](audit/README.md), the execution plan in [research/camoufox](../research/camoufox/README.md), and the evidence-record policy in [research/camoufox/evidence](../research/camoufox/evidence/README.md).

## Phase 2 blocking summary

Phase 2 is blocked by: `AUD-001`, `AUD-002`, `AUD-003`, `AUD-004`, `AUD-005`, `AUD-006`, `AUD-007`, `AUD-008`, `AUD-012`, `AUD-013`, `AUD-014`, `AUD-015`, `AUD-016`, `AUD-019`, `AUD-022`, `AUD-023`, `AUD-024`, and the newly explicit surface/security scopes `AUD-027`–`AUD-034`. A go/no-go review may explicitly reject an engine or accept a bounded documented risk, but may not treat missing evidence as confirmation. Where an item requires packaged Phase 2 code for final testing, Phase 1 must at minimum approve the testable design, fixtures, and fail-closed gate; the item remains open until its evidence threshold is met.

Phase 3 portability additionally requires an evidence-backed decision for `AUD-010`, `AUD-021`, and `AUD-026`; relevant `AUD-005`, `AUD-011`, and `AUD-022` constraints must be reflected in the supported data/host matrix.

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

### AUD-015 — Project and third-party distribution obligations

- **Category:** Licensing and distribution
- **Question:** Which project license will be selected, and what distinct obligations apply to this project, Camoufox, Firefox/MPL-covered components, launcher/dependencies, modifications, and binary distribution?
- **Why it matters:** The product cannot ship legally without a compliant source, notice, and relinking/distribution plan where applicable.
- **Current hypothesis:** Multiple licenses and binary/source-offer obligations may apply; exact conclusions require qualified review.
- **Known evidence:** No license inventory or legal conclusion accepted in this repository.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** The project-license decision, [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md), exact upstream license files/notices, dependency manifests, binary contents, patch history, distribution terms, and official license texts.
- **Test procedure:** Build a software bill of materials and map each shipped artifact/file/modification to obligations; obtain legal review before distribution.
- **Test environments:** Planned Windows installer/update and source-distribution channels.
- **Expected result:** Approved compliance matrix, notice bundle, source availability procedure, and prohibited combinations if any.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Inability to distribute, takedown, or forced redesign.
- **Blocks phase:** Phase 2
- **Required decision:** Select the project license separately from approving the third-party compliance and binary-distribution model; obtain qualified legal review before distribution.
- **Required patch:** Compliance packaging/process changes; code changes only if required.
- **Regression test:** Automated license/SBOM/notice check in release pipeline plus periodic legal review.
- **Owner:** Unassigned; legal counsel required
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-27
- **Last updated date:** 2026-09-27
- **Notes:** This item records engineering due diligence, not legal advice. A public repository is not evidence that downstream use or redistribution is licensed.

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

### AUD-024 — Sidecar topology, protocol, process ownership, and crash recovery

- **Category:** Inter-process architecture
- **Question:** Which topology—per-profile sidecar, shared multi-profile sidecar, or shared supervisor with isolated worker per profile—and which transport, framing, authentication, version negotiation, idempotency, secret delivery, timeout, cancellation, event, Windows process-containment, ownership-proof, and reconciliation semantics safely connect Rust, sidecar workers, and browser trees?
- **Why it matters:** Process ambiguity can duplicate launches, leak authority, or lose lifecycle state.
- **Current hypothesis:** The Rust supervisor can remain the durable tree authority while the sidecar invokes the launcher, but this requires explicit uncertain-outcome semantics, PID-reuse-resistant ownership evidence, and tested asymmetric-crash rules; transport and Windows primitives remain open.
- **Known evidence:** Architectural requirements only; no protocol spike or threat test.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** [SIDECAR_PROCESS_MODEL.md](SIDECAR_PROCESS_MODEL.md), [ADR-0016](adr/0016-sidecar-topology.md), candidate Windows IPC and process/job containment APIs/libraries, launcher event/process models, Playwright lifecycle, OS access controls, and relevant threat guidance.
- **Test procedure:** Prototype all three topology candidates; measure process/startup/steady resource cost and isolation; inject lost responses, duplicate requests, sidecar/core/browser crashes in every asymmetric combination, PID reuse/stale ownership records, stale endpoints, unauthorized clients, oversized frames, mixed versions, and version mismatch. Verify blast radius and that adopt/terminate behavior never launches twice or targets an unowned process.
- **Test environments:** Supported Windows versions, multiple users/sessions where relevant, normal and crash/restart conditions.
- **Expected result:** Evidence-backed topology plus selected transport and Windows ownership mechanism with isolated authenticated instances, bounded resource cost/blast radius, explicit compatibility, typed errors, idempotency, deadlines, verified tree identity, and deterministic reconciliation for core-dead, supervisor-dead, worker-dead, and browser-dead cases.
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

### AUD-026 — Credential and authenticated-session boundary in browser state

- **Category:** Portability and secret handling
- **Question:** Which Camoufox/Firefox profile files, databases, key stores, OS-bound keys, and related metadata contain or enable recovery of saved credentials, authenticated sessions, tokens, or other account-bearing state, and can they be excluded selectively without corrupting supported restore semantics?
- **Why it matters:** A raw user data directory may couple cookies, logins, encryption keys, preferences, and storage. The product must not promise both full-state fidelity and credential/session exclusion when those properties are incompatible.
- **Current hypothesis:** Separately managed application/proxy credentials can be excluded reliably, but some browser-owned session or credential state may be opaque, interdependent, or protected by host-bound keys.
- **Known evidence:** No accepted Camoufox/Firefox file inventory, key-linkage analysis, or sanitized/full-state round-trip evidence.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Pinned Camoufox/Firefox profile layout and credential/session storage code/docs, NSS/key databases, cookie/login/session/local-storage/extension storage, launcher copy logic, `AUD-005` inventory, and portability design.
- **Test procedure:** Populate disposable profiles with uniquely tagged saved logins, cookies, authenticated sessions, local/IndexedDB/service-worker storage, extension credentials, and protected keys; inventory changed files and dependencies; test candidate sanitized and full-state exports, wrong-host/key conditions, omission failures, residual-secret scanning, and application usability after restore.
- **Test environments:** Supported Windows versions, same host/different path and clean compatible host where allowed; disposable accounts and controlled services only.
- **Expected result:** Evidence-backed per-data-type classification, key-dependency graph, safe exclusion/include rules, user-visible sensitivity labels, compatibility limits, and a decision to approve sanitized mode, explicitly sensitive full-state mode, both, or neither.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** High
- **Impact:** Secret/session leakage, misleading backup claims, broken restores, or accidental account duplication.
- **Blocks phase:** Phase 3 portability implementation; does not block Phase 2 MVP
- **Required decision:** Approve exact Backup/Transfer/Duplicate data inventories and sensitivity UX; reject any mode whose safety and fidelity cannot both meet policy.
- **Required patch:** Container filters, key-handling rules, explicit sensitive-mode design, or exclusion of unsupported browser-state classes.
- **Regression test:** Seeded-sensitive-data round trip, exclusion, residual scan, wrong-key/host, and restored-usability matrix for every portability release.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-28
- **Last updated date:** 2026-09-28
- **Notes:** This item refines `AUD-005` and `AUD-021`; it does not assume selective exclusion is feasible.

### AUD-027 — TLS, HTTP, and request-header coherence

- **Category:** Network fingerprint
- **Question:** Which TLS, HTTP/2 or later, protocol, and request-header surfaces are controlled by the pinned browser/launcher, and are they coherent with the declared browser identity and proxy path?
- **Why it matters:** Script-visible identity can disagree with network-visible behavior.
- **Current hypothesis:** Core version, proxy implementation, and launcher settings may alter observable network signatures.
- **Known evidence:** No pinned-source inventory or controlled network capture accepted.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Pinned core networking source/configuration, launcher arguments, proxy implementation, and protocol defaults.
- **Test procedure:** Capture controlled requests for direct and supported proxy modes; compare TLS/client hello, negotiated protocols, HTTP settings, headers, redirects, service workers, and subresources against the identity manifest and baseline policy.
- **Test environments:** Supported environment/proxy matrix with owned capture endpoints.
- **Expected result:** Versioned surface catalogue, coherence rules, known uncontrollable fields, and fail-closed policy for required mismatches.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Cross-layer fingerprint inconsistency or network leakage.
- **Blocks phase:** Phase 2 engine approval
- **Required decision:** Approve the supported network-surface matrix or reject the candidate.
- **Required patch:** TBD from evidence; adapter validation or upstream change.
- **Regression test:** Pinned network-capture and semantic-diff suite.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-28
- **Last updated date:** 2026-09-28
- **Notes:** Coordinate with `AUD-008`, `AUD-019`, and `AUD-028`.

### AUD-028 — Locale, timezone, geolocation, and proxy coherence

- **Category:** Cross-surface identity coherence
- **Question:** Can configured locale, language, timezone, geolocation permissions/values, DNS/network region, and proxy exit be made internally coherent without hidden random fallback?
- **Why it matters:** Conflicting regional signals are observable across browser and network surfaces.
- **Current hypothesis:** Some values are configurable while host or proxy-derived values may remain outside launcher control.
- **Known evidence:** No pinned-source mapping or cross-region test accepted.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Locale/timezone/geolocation configuration consumers, permission paths, DNS/WebRTC behavior, proxy semantics, and OS locale inputs.
- **Test procedure:** Run a region/locale/timezone/proxy matrix; probe main frame, workers, network headers, DNS/WebRTC, permissions, and navigation changes.
- **Test environments:** Proposed supported locales, language packs, timezones, and proxy modes.
- **Expected result:** Coherence constraints, supported combinations, revalidation triggers, and typed rejection for impossible combinations.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Identity inconsistency, location leakage, or false configuration claims.
- **Blocks phase:** Phase 2 identity/proxy approval
- **Required decision:** Select supported combinations and failure behavior.
- **Required patch:** TBD; adapter validation or upstream fix.
- **Regression test:** Cross-context regional-coherence matrix.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-28
- **Last updated date:** 2026-09-28
- **Notes:** Proxy assignment remains mutable runtime configuration.

### AUD-029 — Display, DPI, multi-monitor, and zoom behavior

- **Category:** Render and host dependence
- **Question:** How do Windows display scaling, multiple monitors, window movement, zoom, remote sessions, and display hot-plug affect configured and observed identity surfaces?
- **Why it matters:** Display changes can create drift after preflight or expose host geometry.
- **Current hypothesis:** Some observations are host/render-derived and may change while a profile is running.
- **Known evidence:** No controlled display matrix accepted.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Screen/window/media-query configuration paths, Firefox display handling, launcher window configuration, and Windows DPI behavior.
- **Test procedure:** Probe before and after scaling, zoom, monitor moves/hot-plug, sleep/resume, and remote-session transitions; compare all contexts.
- **Test environments:** Single/multiple monitors, proposed DPI values, GPU families, and Windows versions.
- **Expected result:** Supported display envelope, host-dependent classifications, runtime revalidation triggers, and navigation containment on invalidation.
- **Observed result:** Not observed.
- **Severity:** High
- **Probability:** Unknown
- **Impact:** Runtime fingerprint drift or unusable profiles.
- **Blocks phase:** Phase 2 supported-environment decision
- **Required decision:** Approve supported display configurations and drift response.
- **Required patch:** TBD; validation, relaunch requirement, or upstream patch.
- **Regression test:** Display-transition semantic-diff suite.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-28
- **Last updated date:** 2026-09-28
- **Notes:** Inputs belong in the environment descriptor, not immutable profile identity by default.

### AUD-030 — Media devices and permission surfaces

- **Category:** Identity and privacy
- **Question:** How are media device enumeration, labels, stable IDs, capabilities, permissions, and device changes exposed across contexts and restarts?
- **Why it matters:** Real or synthetic device surfaces can leak host identity or drift.
- **Current hypothesis:** Permission state and installed hardware may affect visibility independently of configured presets.
- **Known evidence:** No source trace or controlled device/permission matrix accepted.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Media-device configuration and ID derivation, permission storage, browser profile files, WebRTC paths, and host enumeration.
- **Test procedure:** Probe before/after permission decisions, restart, device add/remove, workers/iframes, restore/import, and different profiles.
- **Test environments:** No-device, common camera/microphone combinations, and virtual-device fixtures where controlled.
- **Expected result:** Surface ownership map, deterministic/persistent fields, privacy constraints, and supported permission behavior.
- **Observed result:** Not observed.
- **Severity:** High
- **Probability:** Unknown
- **Impact:** Host leakage, cross-profile correlation, or broken sites.
- **Blocks phase:** Phase 2 identity-surface decision
- **Required decision:** Approve supported media-device policy or disable unsupported claims.
- **Required patch:** TBD from evidence.
- **Regression test:** Media permission/device lifecycle matrix.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-28
- **Last updated date:** 2026-09-28
- **Notes:** Coordinate with `AUD-006`, `AUD-019`, and `AUD-022`.

### AUD-031 — Windows binary, process, and path hardening

- **Category:** Platform security
- **Question:** Can the application, sidecar, browser artifacts, working directories, DLL search, environment, handles, and process creation be hardened against substitution and path redirection on supported Windows systems?
- **Why it matters:** The application executes sensitive binaries and processes attacker-controlled browser data.
- **Current hypothesis:** Default process/path behavior is insufficient without explicit validation and ACL policy.
- **Known evidence:** No packaged-binary or adversarial path test accepted.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Planned packaging/process adapter, Windows process/DLL/path APIs, artifact layout, ACL design, upstream binary loading, and reparse handling.
- **Test procedure:** Attempt DLL/path substitution, writable-parent execution, environment injection, handle inheritance, junction/reparse escape, alternate data streams, long/UNC paths, and executable replacement.
- **Test environments:** Supported Windows/filesystem/security-tool matrix with standard-user installs.
- **Expected result:** Canonical-path and artifact verification, safe process creation, explicit DLL policy, minimal inherited state, ACL requirements, and fail-closed errors.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Local code execution, profile compromise, or cross-profile data access.
- **Blocks phase:** Phase 2 process/storage design; final packaged proof in Phase 5
- **Required decision:** Approve Windows hardening baseline and unsupported path/install conditions.
- **Required patch:** Application/sidecar hardening; upstream patch if browser loading cannot be bounded.
- **Regression test:** Adversarial Windows path/process harness.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-28
- **Last updated date:** 2026-09-28
- **Notes:** Coordinate with `AUD-016`, `AUD-017`, and `SEC-004`.

### AUD-032 — Preflight TOCTOU and revalidation triggers

- **Category:** Lifecycle assurance
- **Question:** Which events can invalidate preflight after observation, how quickly can they occur, and what containment/revalidation action is reliable?
- **Why it matters:** A valid preflight can become stale before or during external navigation.
- **Current hypothesis:** Core migration, proxy/display/monitor/extension changes, GPU restart, sleep/resume, import/recovery, and browser restart may invalidate some observations.
- **Known evidence:** Design requirements only; no trigger or race experiment accepted.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Browser lifecycle/events, GPU/display/network changes, extension and session restore behavior, launcher events, and [FINGERPRINT_SPEC.md](FINGERPRINT_SPEC.md).
- **Test procedure:** Inject each trigger before, during, and after probes and navigation admission; test event loss, rapid changes, stale results, cancellation, and candidate-baseline behavior.
- **Test environments:** Supported environment matrix with controlled proxy/display/GPU/sleep fixtures.
- **Expected result:** Trigger catalogue, validity token/generation rule, race-free navigation and lease gate, timeout behavior, and explicit revalidation policy.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** High
- **Impact:** Unverified identity escapes containment or drift is auto-accepted.
- **Blocks phase:** Phase 2 preflight design and launch gate
- **Required decision:** Approve validity-generation and containment semantics.
- **Required patch:** Lifecycle/adapter integration after Phase 1 design approval.
- **Regression test:** Trigger/race/fault-injection suite.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-28
- **Last updated date:** 2026-09-28
- **Notes:** Baseline replacement is never an automatic revalidation response.

### AUD-033 — Tauri/WebView IPC and renderer hardening

- **Category:** Desktop application security
- **Question:** Which Tauri/WebView IPC exposure, content policy, navigation, deep-link, updater, plugin, serialization, and capability settings keep renderer compromise from reaching filesystem, database, process, or secret authority?
- **Why it matters:** Browser-rendered UI content is outside the trusted core boundary.
- **Current hypothesis:** A narrow command allowlist and schema validation are required; exact framework-version controls remain unselected.
- **Known evidence:** Architecture requirements only; Tauri is not scaffolded and no configuration was tested.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Selected Tauri/WebView versions and official security guidance, planned IPC bindings, CSP/navigation configuration, plugin permissions, and updater design.
- **Test procedure:** Threat-model and test malicious renderer payloads, navigation, oversized/malformed messages, command confusion, deep links, plugin abuse, secret reflection, and update IPC.
- **Test environments:** Selected packaged Phase 2 stack on supported Windows versions.
- **Expected result:** Version-pinned IPC threat model, allowlist, schema/size validation, capability separation, CSP/navigation policy, and negative tests.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Trusted-core compromise, arbitrary process/filesystem access, or secret disclosure.
- **Blocks phase:** Phase 2 scaffold design; runtime closure before Phase 2 exit
- **Required decision:** Approve IPC surface and framework security baseline.
- **Required patch:** Phase 2 shell/binding configuration and tests.
- **Regression test:** Renderer-to-core authorization and fuzz/negative suite.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-28
- **Last updated date:** 2026-09-28
- **Notes:** This audit does not authorize scaffolding during Phase 1 documentation work.

### AUD-034 — Protected secrets and same-user local threat limits

- **Category:** Secret storage and local trust
- **Question:** Which Windows protected-storage mechanism, ACL, unlock/recovery behavior, and local-channel controls are achievable, and what attacks remain possible from another process running as the same user?
- **Why it matters:** Local-only does not make secrets or IPC safe from same-user malware, debuggers, dumps, or process inspection.
- **Current hypothesis:** OS protection can reduce accidental disclosure and at-rest theft but cannot fully defend against a compromised same-user session.
- **Known evidence:** No keychain implementation, threat test, or recovery decision accepted.
- **Evidence quality:** `HYPOTHESIS`
- **Source files/documents to inspect:** Windows credential/data-protection facilities, selected libraries, crash dump/logging behavior, named-pipe/local transport ACLs, backup/recovery requirements, and diagnostic tooling.
- **Test procedure:** Test at-rest copying, wrong-user/session access, same-user client impersonation, dump/log/env/argv leakage, credential rotation, OS reinstall/migration, backup recovery, and endpoint ACL bypass attempts.
- **Test environments:** Standard-user and multiple-user Windows test environments with documented security context.
- **Expected result:** Approved protected-store boundary, explicit same-user limitations, recovery/portability behavior, ACL/authentication policy, and user-facing risk statement.
- **Observed result:** Not observed.
- **Severity:** Critical
- **Probability:** Unknown
- **Impact:** Identity, proxy, API, or export-key disclosure and unauthorized local control.
- **Blocks phase:** Phase 2 secret/IPC design; portability specifics block Phase 3
- **Required decision:** Select protected store and accept/document residual same-user risk.
- **Required patch:** Phase 2 protected-store and channel controls.
- **Regression test:** Seeded-secret leakage and unauthorized-client matrix.
- **Owner:** Unassigned
- **Status:** `NOT_STARTED`
- **Created date:** 2026-09-28
- **Last updated date:** 2026-09-28
- **Notes:** Coordinate with `AUD-018`, `AUD-024`, `AUD-026`, and the [Threat Model](THREAT_MODEL.md).

## Register maintenance

When work starts, update `Owner`, `Status`, dates, and evidence references. Store large raw artifacts outside this document and link them with hashes. New uncertainty receives a new stable ID; closed items are not renumbered or deleted.

# Glossary

| Term | Definition |
|---|---|
| Browser core | A versioned browser binary distribution plus the files required to launch it. |
| Browser driver sidecar | A separately supervised process that translates the engine contract into launcher and Playwright operations. Its implementation language is not yet selected. |
| Browser state | Mutable data such as cookies, local storage, IndexedDB, history, extension data, and preferences. Exact persistence is subject to `AUD-005`. |
| Capability | A versioned engine feature explicitly reported by an adapter, rather than inferred from engine name. |
| Compatibility record | Immutable output of a launch, migration, restore, or import compatibility evaluation; it is evidence for a decision, not identity truth. |
| Device identity | The coherent set of identity inputs and policies assigned to one profile. |
| Engine adapter | Infrastructure implementation of the browser-engine contract for one engine family. |
| Fingerprint baseline | Versioned normalized observations for one profile/core/probe/environment tuple, used for semantic comparison. |
| Fingerprint preflight | A probe and semantic comparison performed before a profile is considered safely running. |
| `LAUNCHED_UNVERIFIED` | Contained lifecycle state after browser launch but before preflight passes; no external navigation, restored external tabs, or automation lease is allowed. |
| Identity manifest | Integrity-protected record of immutable profile identity inputs and derivation metadata; it excludes mutable core/proxy choices and observed baselines. |
| Migration | Controlled transition of a profile from one browser-core version to another within the same engine. |
| Portability container | Encrypted, authenticated export format used for backup, transfer, or duplication. |
| Profile | Aggregate that binds one immutable ID and engine to identity, browser state, proxy policy, and lifecycle metadata. |
| Profile lock | Exclusive local lease preventing unsupported concurrent mutation or launch of the same profile. |
| Profile secret | Random secret created once per profile and used as input to deterministic seed derivation. |
| Quarantine | Lifecycle condition in which a profile is prevented from normal launch because integrity, preflight, or recovery checks failed. |
| Runtime configuration | Mutable operational choices such as proxy assignment, approved extensions, startup URLs, and non-identity launch preferences. The profile aggregate is the proposed authority for `activeCoreId`. |
| Semantic fingerprint diff | Policy-based comparison that classifies expected, reviewable, and forbidden changes rather than requiring byte equality. |
| Snapshot | Point-in-time recovery artifact created only after a safe checkpoint. |
| Snapshot recovery | Replace an existing profile's state from a verified snapshot while preserving that profile identity. |
| Backup recovery | Import an authenticated Backup container either as the absent preserved identity or as an explicit same-profile staged replacement. |
| Trash restoration | Return a soft-deleted catalogue record from trash; it does not replace browser data. |
| Authoritative record | The single record whose committed value decides application state; caches, indexes, and projections are not authorities. |
| Activation generation | Monotonic value proposed to bind `activeCoreId` and `acceptedBaselineId` to one committed activation unit. |
| Supervised process tree | The sidecar/browser process group whose ownership and lifecycle are authoritatively tracked by the process supervisor. |
| Technical spike | Time-bounded experiment that produces reproducible evidence, not production code. |
| User data directory | Engine-owned on-disk directory dedicated to one profile. Its exact contents are engine-specific and audited. |

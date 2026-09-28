# Glossary

| Term | Definition |
|---|---|
| Browser core | A versioned browser binary distribution plus the files required to launch it. |
| Browser driver sidecar | A separately supervised process that translates the engine contract into launcher and Playwright operations. Its implementation language is not yet selected. |
| Browser state | Mutable data such as cookies, local storage, IndexedDB, history, extension data, and preferences. Exact persistence is subject to `AUD-005`. |
| Capability | A versioned engine feature explicitly reported by an adapter, rather than inferred from engine name. |
| Device identity | The coherent set of identity inputs and policies assigned to one profile. |
| Engine adapter | Infrastructure implementation of the browser-engine contract for one engine family. |
| Fingerprint baseline | A versioned set of probe observations accepted for a profile and browser-core version. |
| Fingerprint preflight | A probe and semantic comparison performed before a profile is considered safely running. |
| Identity manifest | Canonical, integrity-protected record of immutable, version-derived, and render-derived identity fields. |
| Migration | Controlled transition of a profile from one browser-core version to another within the same engine. |
| Portability container | Encrypted, authenticated export format used for backup, transfer, or duplication. |
| Profile | Aggregate that binds one immutable ID and engine to identity, browser state, proxy policy, and lifecycle metadata. |
| Profile lock | Exclusive local lease preventing unsupported concurrent mutation or launch of the same profile. |
| Profile secret | Random secret created once per profile and used as input to deterministic seed derivation. |
| Quarantine | Lifecycle condition in which a profile is prevented from normal launch because integrity, preflight, or recovery checks failed. |
| Semantic fingerprint diff | Policy-based comparison that classifies expected, reviewable, and forbidden changes rather than requiring byte equality. |
| Snapshot | Point-in-time recovery artifact created only after a safe checkpoint. |
| Technical spike | Time-bounded experiment that produces reproducible evidence, not production code. |
| User data directory | Engine-owned on-disk directory dedicated to one profile. Its exact contents are engine-specific and audited. |


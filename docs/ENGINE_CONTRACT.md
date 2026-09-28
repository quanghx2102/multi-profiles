# Browser Engine Contract

## Purpose

The engine contract prevents product policy from being coupled to Camoufox. It describes required behavior and typed failure semantics; concrete wire and language bindings are deferred to `AUD-024`.

The machine-readable files under [contracts/schemas](../contracts/schemas/) are `Proposed` interoperability drafts. Their existence is not Camoufox capability evidence and does not imply that a sidecar transport or language has been selected.

## Contract principles

- Version every request, result, capability, identity schema, probe schema, and error envelope.
- Negotiate capabilities before use; never branch on engine name in domain logic.
- Make operations idempotent where feasible and include an `operationId` for reconciliation.
- Treat timeouts as uncertain outcomes until process and storage state are reconciled.
- Pass secret handles or protected input channels, never secrets in command-line arguments.
- Return structured errors; do not require callers to parse log text.

## Conceptual operations

| Operation | Required behavior | Principal failures |
|---|---|---|
| `reportCapabilities` | Return supported contract versions, launch modes, proxy types, probe contexts, persistence, and migration features | incompatible protocol, unavailable runtime |
| `validateCoreCandidate` | Inspect an already staged, provenance-authorized candidate for engine-specific layout, version, compatibility, and launch prerequisites without installing it | invalid layout, unsupported platform/version, missing prerequisite |
| `validateInstallation` | Verify expected files, version, hash/signature status, and launch prerequisites | tampering, incomplete install, unsupported version |
| `createIdentity` | Translate an approved device preset and deterministic inputs into engine configuration | unsupported field, nondeterministic fallback, invalid combination |
| `validateIdentity` | Confirm manifest/config completeness and compatibility without mutating it | schema mismatch, missing seed, incompatible core |
| `startProfile` | Through the supervised sidecar session, invoke the launcher once for the requested core, isolated data directory, and identity, then report process/session evidence | already running, lock mismatch, launch failure, uncertain timeout |
| `stopProfile` | Request graceful shutdown, report flush/checkpoint status, and escalate only under caller policy | timeout, crash, incomplete flush |
| `probeFingerprint` | Collect versioned observations from requested supported contexts | context unsupported, probe failure, partial result |
| `validateMigration` | Run compatibility checks and produce a semantic diff without committing | incompatible storage, forbidden drift, crash |

Exact Camoufox support for these behaviors is not assumed (`AUD-001`–`AUD-012`, `AUD-019`, `AUD-020`, `AUD-022`).

## Capability model

The extended network, regional-coherence, display, media, and TOCTOU scopes remain unverified in `AUD-027` through `AUD-032`.

Capabilities must be granular and may carry constraints, for example:

- persistent context lifecycle;
- deterministic surface configuration by named surface;
- probe contexts: main frame, iframe, dedicated/shared worker, service worker, worklet;
- proxy schemes and authentication modes;
- graceful storage checkpoint;
- extension installation/management;
- core migration and downgrade compatibility;
- cookie import/export fidelity;
- headful/headless support;
- automation features.

Absence of a required capability causes a typed rejection. It must not trigger a best-effort random fallback.

## Request envelope

Every sidecar request is expected to carry:

- protocol version;
- operation ID and correlation ID;
- operation type and typed payload;
- profile and engine identifiers where applicable;
- deadline and cancellation policy;
- capability assumptions declared by the caller;
- non-secret references to core, data directory, manifest, and credential handles.

## Result envelope

Every result distinguishes success, rejected-before-effect, failed-after-partial-effect, and outcome-unknown. It includes structured diagnostics safe for normal logs, process identifiers where relevant, capability/version metadata, and reconciliation hints.

## Start postconditions

A successful engine start means only that the authorized sidecar invoked the adapter launcher and can communicate with the browser. The process supervisor, not the adapter, is authoritative for the resulting process tree. The application may mark the profile `RUNNING` only after supervision evidence is recorded and fingerprint preflight passes. If launch succeeds but the response is lost, reconciliation must find and adopt or terminate the exact verified process tree according to `AUD-024`; a second launch is forbidden.

## Stop postconditions

A successful stop reports both the sidecar's graceful-close result and the supervisor's observation that the owned process tree exited, plus any storage-checkpoint evidence. Snapshot creation is an application decision after this result. Forced termination is supervisor policy and must produce a recovery-required journal event.

## Core installation ownership

The engine contract does not download, authorize, or finalize core artifacts. `core-updater` stages and verifies provenance, asks the adapter to validate engine-specific candidate/installed layouts, and alone commits an immutable installation to the core store. This prevents an engine adapter from bypassing supply-chain or retention policy.

## Contract testing

Every adapter must pass the same engine contract suite described in [TEST_STRATEGY.md](TEST_STRATEGY.md). Engine-specific tests may add coverage but cannot weaken common invariants.

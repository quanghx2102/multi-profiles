# Architecture

## Status and evidence boundary

This is the target architecture agreed for planning. It does not assert that Camoufox can yet satisfy the engine contract. All Camoufox-specific feasibility questions remain open in the [Audit Register](AUDIT_REGISTER.md).

## Architectural style

The application uses a modular ports-and-adapters architecture. Domain and application policies sit inside the system boundary; desktop UI, persistence, keychain, filesystem, browser engines, automation libraries, and operating-system facilities are replaceable adapters.

```text
Desktop UI (React/TypeScript, planned)
             |
       validated Tauri IPC
             |
Application use cases ---- Domain model
       |       |               |
       |       +---- ports ----+
       |
       +-- Profile/storage adapters (SQLite + filesystem, planned)
       +-- Security adapters (OS keychain + crypto, planned)
       +-- Process supervisor
       +-- BrowserEngine contract
                    |
             Camoufox adapter
                    |
       versioned local sidecar protocol
                    |
       Browser-driver sidecar + Playwright
                    |
             Camoufox process
```

The named technologies are planned choices recorded in ADRs; they are not scaffolded in Phase 1.

## Dependency rule

Dependencies point inward:

- `domain` depends on no UI, storage, framework, automation, engine, or filesystem implementation.
- `application` depends on domain types and abstract ports.
- adapters implement ports and may depend on external technology.
- composition roots may know concrete implementations; feature modules may not bypass contracts.

The domain must never branch on `camoufox` or `chromium`. Differences are represented by declared capabilities and typed failure results.

## Primary runtime boundaries

| Boundary | Data crossing it | Control |
|---|---|---|
| WebView → Rust Core | Validated commands and presentation-safe results | Allowlisted Tauri commands; schema validation; no raw SQL or shell |
| Rust Core → sidecar | Versioned requests, non-secret handles, lifecycle context | Authenticated local channel, protocol negotiation, correlation IDs |
| Rust Core → keychain | Secret values and stable lookup identifiers | Least privilege; values never returned to UI |
| Rust Core → storage | Domain records, manifests, journals, snapshot metadata | Repository ports and transactions |
| Sidecar → browser | Launch configuration and automation commands | No secrets in argv; one process tree per profile |
| Local API → application | Authenticated automation requests | Loopback by default, scoped token, rate/operation controls |
| Updater → core store | Versioned artifacts and provenance metadata | Checksum/signature verification and anti-downgrade policy |

Protocol transport, sidecar language, and Camoufox launch semantics are deliberately unresolved (`AUD-012`, `AUD-024`).

## Aggregates and ownership

- **Profile aggregate:** identity references, engine binding, state, proxy assignment, active core, lock state, and lifecycle rules.
- **Identity manifest:** canonical identity inputs and versioned baselines; mutated only through explicit identity/migration use cases.
- **Browser-core installation:** immutable installed artifact plus verification and compatibility status.
- **Snapshot:** immutable recovery point linked to a profile checkpoint.
- **Operation:** correlated durable record for long-running start, stop, migration, import, export, and recovery work.

Detailed ownership is in [MODULE_BOUNDARIES.md](MODULE_BOUNDARIES.md); persistence is in [STORAGE_MODEL.md](STORAGE_MODEL.md).

## Key invariants

- `profileId`, `engineId`, and `profileSecret` never change for an existing profile.
- A profile has exactly one dedicated user data directory and may have at most one active process tree.
- A successful stop/start does not regenerate identity seeds.
- No two profiles share mutable browser state or secret-derived seed material.
- An engine operation is allowed only when the adapter reports the required capabilities.
- A profile becomes `RUNNING` only after lock acquisition, integrity checks, successful launch, and fingerprint preflight.
- A failed preflight never silently accepts a new baseline.
- A browser-core migration is transactional at the application level and retains a rollback target.
- Snapshots are created only at a verified checkpoint.
- Sensitive values never cross into UI models, command-line arguments, normal logs, or diagnostic bundles.

## Failure model

Every cross-process request has an operation ID, deadline, cancellation behavior, and typed result. Uncertain outcomes are not treated as success. After a timeout or crash, the supervisor reconciles process state, the application consults the event journal, and the profile remains locked or quarantined until safety is established.

Failures are classified as:

- validation or policy rejection;
- capability unavailable;
- integrity or provenance failure;
- transient process/IO failure;
- uncertain commit requiring reconciliation;
- fingerprint incompatibility;
- security boundary violation.

## Extensibility

A future Chromium adapter must implement the same behavioral contract but may expose a different capability set. An engine change creates a new profile. Only explicitly portable data may be copied; the existing identity is not reinterpreted as another engine's identity. See [ADR-0003](adr/0003-browser-engine-adapter.md) and [ADR-0007](adr/0007-immutable-engine-binding.md).

## Planned technologies

- Desktop shell: Tauri.
- System/core layer: Rust.
- UI: React, TypeScript, and Vite.
- Metadata: SQLite accessed only through Rust-side storage ports.
- Secrets: OS keychain and Rust-side cryptography.
- Automation: Playwright behind the browser-driver sidecar.
- First adapter: Camoufox, conditional on Phase 1 evidence.

Selection of TypeScript or Python for the sidecar is deferred to `AUD-012`; transport and recovery semantics are deferred to `AUD-024`.


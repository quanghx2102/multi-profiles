# Module Boundaries

## Rules

Modules communicate only through public contracts. No module deep-imports another module's implementation. The application composition root is the only place that selects concrete adapters. The ownership statements below are normative.

## Module catalogue

### `domain`

- **Owns:** entities, value objects, state transitions, invariants, domain errors, and capability requirements.
- **Public concepts:** `Profile`, `IdentityManifest`, `BrowserCoreRef`, `ProxyPolicy`, `SnapshotRef`, lifecycle states, semantic diff policy.
- **Depends on:** nothing outside the domain.
- **Does not own:** persistence, processes, UI, cryptography implementations, engine calls, or filesystem layout.

### `application`

- **Owns:** use-case orchestration, transaction boundaries, authorization policy, retries, reconciliation, and port definitions not owned by the domain.
- **Public operations:** create/start/stop/recover profile; snapshot/restore; import/export; install/migrate/rollback core; bulk commands.
- **Depends on:** `domain` and abstract ports.
- **Does not own:** framework handlers, SQL, Playwright calls, or engine-specific configuration.

### `engine-contract`

- **Owns:** versioned capability vocabulary, engine request/result schemas, compatibility rules, and contract-test requirements.
- **Public operations:** install, validate installation, create/validate identity, start, stop, probe fingerprint, validate migration, report capabilities.
- **Depends on:** stable shared domain identifiers and protocol primitives only.
- **Does not own:** any Camoufox/Chromium implementation or profile business policy.

### `engine-camoufox`

- **Owns:** translation between engine-contract requests and verified Camoufox launcher/configuration behavior.
- **Depends on:** `engine-contract`, sidecar client, verified core catalogue.
- **Does not own:** profile state transitions, migration approval, general process policy, storage, or UI.
- **Audit gate:** `AUD-001` through `AUD-012`, `AUD-019`, `AUD-022`.

### `engine-chromium` (future placeholder)

- **Owns:** no runtime behavior until a future spike accepts a Chromium implementation.
- **Depends on:** `engine-contract` only when implemented.
- **Does not own:** reuse or reinterpretation of Camoufox identity manifests.
- **Audit gate:** `AUD-025`.

### `profile-manager`

- **Owns:** profile aggregate coordination, lifecycle commands, lock intent, and user-visible profile policy.
- **Depends on:** application ports for identity, storage, engine, proxy, snapshots, and supervision.
- **Does not own:** direct SQL, seed algorithms, raw process spawning, or engine configuration.

### `identity-manager`

- **Owns:** creation of `profileSecret`, deterministic derivation policy, manifest validation, integrity hashes, schema migration, and baseline references.
- **Depends on:** cryptographic and manifest repositories through ports.
- **Does not own:** UI, process state, browser data directories, or acceptance of an unexpected probe result.

### `process-supervisor`

- **Owns:** child process trees, lifecycle deadlines, exit information, orphan detection, kill escalation, and resource observation.
- **Depends on:** OS process adapter and sidecar protocol.
- **Does not own:** identity mutation, fingerprint acceptance, snapshot content, or profile business transitions.

### `fingerprint-probe`

- **Owns:** probe schema, collection across supported execution contexts, normalization, and semantic diff production.
- **Depends on:** browser automation port and baseline store.
- **Does not own:** migration commit, baseline auto-acceptance, or identity generation.

### `profile-storage`

- **Owns:** metadata repositories, transaction implementation, filesystem layout adapter, atomic writes, and checkpoint primitives.
- **Depends on:** SQLite/filesystem implementations when selected.
- **Does not own:** lifecycle or migration decisions, secret derivation, process control, or snapshot policy.

### `proxy-manager`

- **Owns:** proxy configuration validation, credential handles, connectivity tests, assignment metadata, and leak-test orchestration.
- **Depends on:** keychain, network probe, engine capability port.
- **Does not own:** a proxy network, proxy reputation, or fingerprint identity.

### `snapshot-manager`

- **Owns:** safe-checkpoint verification, snapshot creation, retention metadata, integrity verification, and restore mechanics.
- **Depends on:** storage/checkpoint ports and encryption where required.
- **Does not own:** deciding that an unsafe running profile may be copied, or changing identity during restore.

### `import-export`

- **Owns:** portability schema, Backup/Transfer/Duplicate workflows, streaming authenticated encryption, compatibility report, and import staging.
- **Depends on:** identity, snapshot, storage, keychain/crypto, and compatibility ports.
- **Does not own:** plaintext temporary archives, distributed locks, or silent compatibility coercion.

### `core-updater`

- **Owns:** artifact catalogue, download staging, provenance verification, multi-core installation, canary coordination, and rollback retention.
- **Depends on:** artifact transport, verifier, engine contract, migration and storage ports.
- **Does not own:** arbitrary identity changes or deletion of the rollback target before policy permits.

### `automation-api`

- **Owns:** loopback API presentation, authentication, request validation, operation status, quotas, and cancellation exposure.
- **Depends on:** application use cases only.
- **Does not own:** raw Playwright access, database access, or process spawning.

### `security`

- **Owns:** secret handles, cryptographic policy, keychain integration, redaction policy, binary trust policy, and secure deletion requirements.
- **Depends on:** OS and crypto adapters.
- **Does not own:** product lifecycle decisions or UI state.

### `diagnostics/observability`

- **Owns:** structured event schema, correlation IDs, lifecycle journal format, semantic diff reports, process exit records, and redacted diagnostic bundles.
- **Depends on:** event sinks through ports.
- **Does not own:** secrets, raw cookie values, automatic recovery decisions, or acceptance of risk.

### `desktop-ui`

- **Owns:** presentation state, validated user intent, progress and recovery UX, and display-safe diagnostics.
- **Depends on:** typed Tauri/application facade.
- **Does not own:** SQL, filesystem access, browser processes, shell execution, secrets, or domain policy.

### `browser-driver-sidecar`

- **Owns:** launcher invocation, Playwright session, browser commands, browser events, fingerprint probe execution, and cookie operations authorized by the contract.
- **Depends on:** selected launcher, Playwright, protocol implementation.
- **Does not own:** durable profile policy, database writes, identity generation, migration commit, or secret logging.
- **Audit gate:** `AUD-012`, `AUD-024`.

## Forbidden dependency examples

- UI → SQLite or filesystem.
- UI → process spawn or shell.
- Domain/application → Camoufox, Chromium, Playwright, Tauri, or concrete database packages.
- Camoufox adapter → profile repository implementation.
- Process supervisor → identity manifest writer.
- Storage adapter → migration decision.
- Sidecar → OS keychain values except via narrowly scoped, explicit secret-delivery design approved by security review.


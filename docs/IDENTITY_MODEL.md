# Identity Model

## Objective

Each profile receives identity material once and reloads it on later starts. The model intentionally separates configured identity from observed fingerprint behavior; Camoufox persistence and propagation remain audit questions.

## Data classification

Identity is not a synonym for every profile setting. The following classes have different authorities and mutation rules.

| Class | Examples | Mutation rule | Authority |
|---|---|---|---|
| Immutable identity material | `profileId`, `engineId`, protected `profileSecret`, lineage, derivation namespace | Never changes for an existing profile | Identity manifest plus secret store |
| Version-derived identity configuration | Adapter/core-specific rendered config, deterministic surface seeds, dataset/schema version | Re-rendered only by a recorded deterministic migration | Identity renderer output linked from the manifest |
| Render-derived observations | Canvas/WebGL/audio results, headers and display probes | Append-only candidates; accepted only by explicit baseline workflow | Fingerprint baseline repository |
| Mutable profile runtime configuration | Startup URLs, automation policy, approved extensions, runtime preferences | User/operation controlled; cannot rewrite identity | Profile runtime configuration repository |
| Proxy assignment and credentials | Proxy reference, mode, endpoint metadata, protected credential handle | Mutable; a change triggers applicable preflight | Proxy repository and protected secret store |
| User-editable metadata | Name, notes, tags, archive flag | Mutable; never used as identity evidence | Profile metadata repository |

See [Data Authority](DATA_AUTHORITY.md) for the complete ownership table. In particular, proxy assignment is runtime configuration, not immutable identity.

## Canonical immutable manifest

The identity manifest contains at least:

- `profileId` and immutable `engineId`;
- a reference to the protected `profileSecret`, never the plaintext secret in ordinary metadata;
- `identitySchemaVersion` and `devicePresetVersion`;
- OS/device preset, screen, CPU/RAM class, GPU/WebGL preset, fonts, and media-device configuration;
- identity-bearing locale/timezone inputs;
- Canvas, Audio, WebGL-noise, and ClientRects seeds;
- manifest integrity hash;
- dedicated `user_data_dir` reference.

Whether Camoufox consumes every listed seed and propagates it consistently is explicitly unverified (`AUD-001`, `AUD-002`, `AUD-003`, `AUD-006`, `AUD-007`, `AUD-022`).

The manifest does not contain the mutable active-core pointer, proxy assignment, extension selection, accepted fingerprint baselines, or compatibility results. It may record immutable creation-time and version-baseline associations needed to interpret lineage, but those are not activation pointers. Separate records under [ADR-0014](adr/0014-separate-identity-runtime-and-observation-records.md) hold:

- profile metadata/runtime configuration holds mutable activation, proxy, approved extension, and non-identity launch choices; the proposed single owner for `activeCoreId` is the profile aggregate in [ADR-0015](adr/0015-profile-owned-active-core-pointer.md);
- fingerprint baselines hold normalized observations for a core/probe/environment tuple;
- compatibility records hold immutable preflight, migration, restore, or import decisions.

The profile aggregate coordinates references to these records without turning mutable runtime state into identity truth.

## Field classes

### Immutable identity fields

`profileId`, `engineId`, `profileSecret`, initial identity lineage, derivation namespace, and semantic identity inputs never change. Changing engine or intentionally changing an identity-bearing preset creates a new profile. A schema migration may change representation only when it preserves the same identity semantics.

### Version-derived fields

Engine configuration material may be re-rendered for a specific identity-schema, device-dataset, adapter, or browser-core version. Derivation must remain deterministic and recorded. A migration may add a field, but may not silently replace the secret or reinterpret a missing required seed as random.

### Render-derived fields

Observed values may legitimately differ because of core behavior or host rendering. They are stored as versioned baselines and evaluated by semantic policy. Acceptable ranges require test evidence; they are not inferred in this phase.

## Seed derivation policy

Under [ADR-0010](adr/0010-deterministic-identity-derivation.md), the planned design creates `profileSecret` once using a cryptographically secure generator, stores it through a protected secret mechanism, and derives named, versioned, domain-separated surface seeds. The exact KDF, salt/info labels, lengths, rotation rules, and recovery representation require a later cryptographic design review.

Required properties:

- domain separation between surfaces and schema versions;
- deterministic re-derivation from the same protected input;
- no cross-profile reuse;
- no secret or seed in logs;
- explicit failure when a required seed cannot be represented by an engine;
- integrity verification before use.

## Mutable runtime configuration

Runtime changes do not create a new identity unless a requested change would alter an immutable semantic input. Proxy changes, extension changes, display/monitor changes, resume events, core migrations, imports, and browser/GPU restarts can invalidate observations and therefore trigger the revalidation policy in [Fingerprint Specification](FINGERPRINT_SPEC.md). They never authorize automatic baseline replacement.

## Baselines

A baseline belongs to a tuple of profile, engine, core version, probe schema, and environment descriptor. It records normalized observations and evidence metadata. Under [ADR-0011](adr/0011-semantic-fingerprint-comparison.md), comparisons use evidence-backed field classes and normalization rather than raw byte equality. Baselines move through candidate, accepted, rejected, and superseded states as specified by [Fingerprint Specification](FINGERPRINT_SPEC.md). A failed start, runtime drift, or migration cannot overwrite the accepted baseline.

## Identity integrity failure

Missing secret, hash mismatch, incompatible schema, missing required field, or unexpected derivation result moves the profile to `QUARANTINED`. Recovery restores a verified manifest/secret pair or requires a deliberate duplicate-as-new workflow; it never generates replacement identity material for the existing profile.

## Host dependence and portability

The degree to which hardware, drivers, installed fonts, and OS state affect observed identity is unknown. Cross-machine preservation is gated by `AUD-010` and `AUD-022`. Export metadata therefore records OS and compatibility requirements and never guarantees portability merely because files decrypted successfully.

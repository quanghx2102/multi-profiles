# Identity Model

## Objective

Each profile receives identity material once and reloads it on later starts. The model intentionally separates configured identity from observed fingerprint behavior; Camoufox persistence and propagation remain audit questions.

## Canonical manifest

The identity manifest contains at least:

- `profileId` and immutable `engineId`;
- a reference to the protected `profileSecret`, never the plaintext secret in ordinary metadata;
- `identitySchemaVersion` and `devicePresetVersion`;
- active and compatible `browserCoreVersion` references;
- OS/device preset, screen, CPU/RAM class, GPU/WebGL preset, fonts, and media-device configuration;
- locale/timezone policy and proxy assignment reference;
- Canvas, Audio, WebGL-noise, and ClientRects seeds;
- manifest integrity hash;
- fingerprint baseline references per browser-core version;
- dedicated `user_data_dir` reference.

Whether Camoufox consumes every listed seed and propagates it consistently is explicitly unverified (`AUD-001`, `AUD-002`, `AUD-003`, `AUD-006`, `AUD-007`, `AUD-022`).

## Field classes

### Immutable identity fields

`profileId`, `engineId`, `profileSecret`, initial identity lineage, and derivation namespace never change. Changing engine or intentionally creating a different identity creates a new profile.

### Version-derived fields

Engine configuration material may be re-rendered for a specific identity-schema, device-dataset, adapter, or browser-core version. Derivation must remain deterministic and recorded. A migration may add a field, but may not silently replace the secret or reinterpret a missing required seed as random.

### Render-derived fields

Observed values may legitimately differ because of core behavior or host rendering. They are stored as versioned baselines and evaluated by semantic policy. Acceptable ranges require test evidence; they are not inferred in this phase.

## Seed derivation policy

The planned design creates `profileSecret` once using a cryptographically secure generator, stores it through a protected secret mechanism, and derives named, versioned surface seeds with a KDF such as HKDF. The exact algorithm, salt/info labels, lengths, rotation rules, and recovery representation require a later cryptographic design review.

Required properties:

- domain separation between surfaces and schema versions;
- deterministic re-derivation from the same protected input;
- no cross-profile reuse;
- no secret or seed in logs;
- explicit failure when a required seed cannot be represented by an engine;
- integrity verification before use.

## Baselines

A baseline belongs to a tuple of profile, engine, core version, probe schema, and environment descriptor. It records normalized observations and evidence metadata. Baselines are created only after an explicit verification workflow. A failed start or migration cannot overwrite the accepted baseline.

## Identity integrity failure

Missing secret, hash mismatch, incompatible schema, missing required field, or unexpected derivation result moves the profile to `QUARANTINED`. Recovery restores a verified manifest/secret pair or requires a deliberate duplicate-as-new workflow; it never generates replacement identity material for the existing profile.

## Host dependence and portability

The degree to which hardware, drivers, installed fonts, and OS state affect observed identity is unknown. Cross-machine preservation is gated by `AUD-010` and `AUD-022`. Export metadata therefore records OS and compatibility requirements and never guarantees portability merely because files decrypted successfully.


# Storage Model

## Scope

This document defines logical ownership and consistency requirements. It does not freeze a physical SQL schema or filesystem layout.

## Storage classes

| Class | Examples | Authority |
|---|---|---|
| Profile metadata | profile record, lifecycle state, user metadata, activation generation | Profile repository port |
| Identity | immutable manifest, schema/derivation metadata, seed references, integrity hash | Identity repository plus protected secret store |
| Runtime configuration | proxy assignment reference, approved extensions, startup and non-identity launch choices | Runtime-configuration repository |
| Observations | fingerprint baselines and compatibility records | Baseline/compatibility repositories |
| Browser state | dedicated user data directory | Browser engine; exact contents audited in `AUD-005` |
| Recovery | snapshots, snapshot-recovery points, migration checkpoints | Snapshot manager |
| Operations | lifecycle journal, operation outcomes, process exit records | Diagnostics/operation repository |
| Core artifacts | immutable versioned browser installations and provenance | Core updater/core store |
| Secrets | profile secret, proxy credentials, API token, export key material | OS keychain or approved protected store; exact mechanism remains `AUD-034` |

The authoritative-owner table, including the current/proposed distinction for `activeCoreId`, is in [Data Authority](DATA_AUTHORITY.md). SQLite and filesystem choices are implementation adapters, not domain authorities.

## Required records

The logical model includes profiles, immutable identity manifests, runtime configurations, core installations, fingerprint baselines, compatibility records, proxy assignments, snapshots, lifecycle operations, event journal entries, export/import jobs, and schema migrations. Foreign references use stable IDs; secrets are represented by opaque handles. `profileId` is the unique catalogue identity; Backup restore does not introduce a second local instance ID.

## Consistency rules

- Metadata commits cannot imply a process stopped, snapshot succeeded, or migration committed unless the corresponding durable evidence exists.
- Identity manifest writes use atomic replace plus integrity verification.
- Mutable core/proxy/extension choices never rewrite the immutable identity manifest.
- Browser data is never shared by path between profiles.
- Core directories are immutable after verification; a new build/hash gets a distinct installation identity.
- Snapshots are immutable and content/integrity addressed after completion.
- Subject to approval of [ADR-0015](adr/0015-profile-owned-active-core-pointer.md), the profile aggregate owns the only mutable `activeCoreId`; the identity manifest contains no competing activation pointer.
- The active-core pointer, accepted-baseline pointer, and activation generation transition as one journaled application-level activation unit.
- Destructive cleanup is delayed until retention and rollback policy permits it.

## Crash strategy

Long operations use the prepare/effect/commit protocol in [Operations Model](OPERATIONS_MODEL.md). On startup, the application reconciles incomplete operations against process, filesystem, and database reality. It must represent `OUTCOME_UNKNOWN`; it must not manufacture a successful commit from the requested intent.

SQLite durability settings, filesystem atomicity on supported Windows filesystems, and browser checkpoint semantics require implementation-time tests (`AUD-013`).

## Schema evolution

- Database, identity manifest, baseline, snapshot, and export container have independent version numbers.
- Migrations are forward-described, backed up, journaled, and idempotent where possible.
- An application/database migration must not silently perform a browser-core migration.
- Unknown future fields are preserved when safe or rejected explicitly; they are never discarded silently from identity-bearing formats.

## Backup boundary

Backups include authoritative state required for the selected mode and omit reproducible caches. Separately managed proxy credentials, API tokens, and application credentials are excluded by default. Saved-password and authenticated-session exclusion from opaque browser state is a policy target, not a proven capability; `AUD-026` must establish the file/key inventory and safe mode boundaries before implementation. See [IMPORT_EXPORT.md](IMPORT_EXPORT.md).

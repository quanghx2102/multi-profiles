# Storage Model

## Scope

This document defines logical ownership and consistency requirements. It does not freeze a physical SQL schema or filesystem layout.

## Storage classes

| Class | Examples | Authority |
|---|---|---|
| Metadata | profile record, state, engine/core refs, proxy ref, timestamps | SQLite through Rust-side repository ports |
| Identity | manifest, schema version, seed references, integrity hash, baselines | Identity repository plus protected secret store |
| Browser state | dedicated user data directory | Browser engine; exact contents audited in `AUD-005` |
| Recovery | snapshots, restore points, migration checkpoints | Snapshot manager |
| Operations | lifecycle journal, operation outcomes, process exit records | Diagnostics/operation repository |
| Core artifacts | immutable versioned browser installations and provenance | Core updater/core store |
| Secrets | profile secret, proxy credentials, API token, export key material | OS keychain or approved protected store |

## Required records

The logical model includes profiles, identity manifests, core installations, fingerprint baselines, proxy assignments, snapshots, lifecycle operations, event journal entries, export/import jobs, and schema migrations. Foreign references use stable IDs; secrets are represented by opaque handles.

## Consistency rules

- Metadata commits cannot imply a process stopped, snapshot succeeded, or migration committed unless the corresponding durable evidence exists.
- Identity manifest writes use atomic replace plus integrity verification.
- Browser data is never shared by path between profiles.
- Core directories are immutable after verification; a new build/hash gets a distinct installation identity.
- Snapshots are immutable and content/integrity addressed after completion.
- The active-core pointer and accepted baseline transition together at application level.
- Destructive cleanup is delayed until retention and rollback policy permits it.

## Crash strategy

Long operations use prepare/effect/commit journal stages. On startup, the application reconciles incomplete operations against process, filesystem, and database reality. It must represent `outcome unknown`; it must not manufacture a successful commit from the requested intent.

SQLite durability settings, filesystem atomicity on supported Windows filesystems, and browser checkpoint semantics require implementation-time tests (`AUD-013`).

## Schema evolution

- Database, identity manifest, baseline, snapshot, and export container have independent version numbers.
- Migrations are forward-described, backed up, journaled, and idempotent where possible.
- An application/database migration must not silently perform a browser-core migration.
- Unknown future fields are preserved when safe or rejected explicitly; they are never discarded silently from identity-bearing formats.

## Backup boundary

Backups include authoritative state required for the selected mode and omit reproducible caches. Saved passwords, proxy credentials, and authenticated sessions are excluded by default unless a later explicit policy approves them. See [IMPORT_EXPORT.md](IMPORT_EXPORT.md).


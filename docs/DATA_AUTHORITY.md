# Data Authority

- Status: Proposed where noted; otherwise restates Accepted boundaries
- Owner: Architecture and storage
- Last reviewed: 2026-09-28
- Review trigger: Approval/rejection of ADR-0015 or any persistence-boundary change

## Rule

Every durable fact has one authoritative owner. Caches, indexes, UI models, generated configuration, probe output, and compatibility projections are disposable or reproducible views; they never become a competing source of truth.

## Authority table

| Data | Authoritative owner | Durable source of truth | Derived/cache examples | Notes |
|---|---|---|---|---|
| Profile ID, engine binding, lifecycle state | Profile aggregate | Profile metadata repository | UI catalogue rows | `profileId` and `engineId` are immutable |
| User-editable name, tags, notes, folders | Profile aggregate | Profile metadata repository | Search index | Never identity material |
| Identity lineage and derivation inputs | Identity manager | Integrity-protected identity manifest + secret handle | Engine-rendered config | Manifest contains no active proxy or active-core pointer |
| `activeCoreId` | **Proposed:** Profile aggregate | Profile metadata repository | Launcher request, UI core label | ADR-0015; current ADR-0014 places it in runtime configuration until accepted |
| Accepted baseline pointer | **Proposed:** Profile aggregate | Profile metadata repository | Preflight comparison input | Changes atomically with `activeCoreId` during migration |
| Fingerprint baseline content/status | Fingerprint probe/baseline repository | Immutable versioned baseline records | Normalized comparison indexes | Baseline record associates profile, engine, core, probe schema, and environment |
| Proxy assignment | Profile runtime configuration | Runtime configuration repository | Resolved launcher config | Mutable; not identity material, though it affects coherence checks |
| Proxy credentials | Security/proxy manager | OS protected store | Opaque credential handle | Plaintext never enters ordinary metadata/UI |
| Profile secret | Identity manager/security | OS protected store | Opaque secret handle; derived seeds in controlled memory | Never regenerated for an existing profile |
| Browser data-directory binding | Profile aggregate/profile storage | Profile metadata repository | Validated concrete path resolved by filesystem adapter | Logical binding is unique per profile; physical relocation is a journaled recovery/import operation, not an identity change |
| Browser state | Browser engine | Dedicated user data directory | Reproducible caches | Exact ownership and safe-copy rules require `AUD-005`/`AUD-026` |
| Operation state | Operations service | Append/durable operation journal + committed metadata | Progress UI | Requested intent is not committed outcome |
| Snapshot | Snapshot manager | Immutable verified snapshot + metadata | Snapshot catalogue projection | Only from a verified checkpoint |
| Import/export job | Import/export service | Operation record + container/staging metadata | Progress UI | Container is not committed profile state until finalization |
| Core installation | Core updater | Immutable core catalogue and artifact store | Download cache | Adapter validates; updater authorizes/finalizes |
| Capability/qualification record | Qualification service | Immutable signed/hashed qualification record | Capability registry projection | Capability claims require evidence reference |
| Audit status/evidence quality | Audit Register | `docs/AUDIT_REGISTER.md` until migration completes | `RESULTS_INDEX.md` | Research notes do not change status automatically |

## Active-core authority analysis

The current documents no longer place `activeCoreId` in the identity manifest, but ADR-0014 lists it inside runtime configuration while update/lifecycle documents treat the profile aggregate as the transaction coordinator. Dual storage would permit a core pointer and accepted baseline to disagree.

[ADR-0015](adr/0015-profile-owned-active-core-pointer.md) therefore recommends one authoritative pair in profile metadata:

```text
(activeCoreId, acceptedBaselineId, activationGeneration)
```

The identity manifest may retain immutable identity lineage and compatibility constraints. Baseline records carry their own core association. Neither the manifest nor generated engine configuration duplicates the mutable active pointer.

Until ADR-0015 is Accepted, ADR-0014 remains authoritative. Implementers must not create both placements; Phase 2 remains blocked on the decision.

## Core/baseline activation transaction

1. Acquire the exclusive profile lock and create an operation record with the old authoritative pair.
2. Validate the candidate installation, identity compatibility, recovery point, and candidate baseline without changing active pointers.
3. Launch only in `LAUNCHED_UNVERIFIED`, run the required probe, and persist an immutable candidate baseline/diff.
4. On approval, one metadata transaction commits `activeCoreId`, `acceptedBaselineId`, `activationGeneration`, candidate status `ACCEPTED`, prior active baseline status `SUPERSEDED`, and the operation outcome.
5. Only after that transaction commits may navigation/automation admission use the new activation unit; projections update from the new generation.
6. On failure, leave the old pair unchanged, terminate/reconcile the candidate tree, and mark the candidate baseline `REJECTED` or retain it as diagnostic evidence.

If the outcome is unknown, reconciliation reads the operation journal and authoritative pair. A mixed pair, missing referenced record, or browser tree inconsistent with the pair quarantines the profile. Reconciliation never infers activation from files in a browser directory or from a successful launch alone.

## Projection rule

Every projection records its source generation/version. A stale projection may be rebuilt; it cannot repair or overwrite its authoritative record. UI edits always invoke an application use case against the authority, never mutate a projection directly.

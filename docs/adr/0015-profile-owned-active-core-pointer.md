# ADR-0015: Profile-Owned Active Core and Baseline Pointer

- Status: Proposed
- Date: 2026-09-28
- Decision owner: Pending user approval (`DEC-DATA-001`)

## Context

ADR-0014 separates identity, runtime configuration, observations, and compatibility records, and currently places active-core selection in runtime configuration. Core migration is nevertheless a profile aggregate transition that must commit the active core and accepted baseline together. A duplicated or indirectly authoritative pointer risks mixed core/baseline state.

## Proposed decision

Make profile metadata the single authority for `(activeCoreId, acceptedBaselineId, activationGeneration)`. The identity manifest contains immutable lineage/derivation inputs and compatibility constraints, never the mutable active pointer. Baseline records carry their own core association. Runtime configuration contains proxy, extensions, startup preferences, and other mutable non-core choices.

Activation uses the prepare/effect/commit and reconciliation flow in [DATA_AUTHORITY.md](../DATA_AUTHORITY.md). No adapter, manifest, generated engine configuration, or UI projection may duplicate the authoritative pointer.

## Alternatives

- Keep active core in runtime configuration under ADR-0014 and make the profile aggregate coordinate that record.
- Store it in both profile metadata and runtime configuration with reconciliation; rejected as a recommendation because it creates two authorities.

## Consequences

Core/baseline transactions and queries become direct aggregate operations, but accepting this ADR changes the storage placement described by ADR-0014 and requires schema/version migration planning. Until acceptance, ADR-0014 remains authoritative and Phase 2 must not implement dual storage.


# ADR-0013: Identity-Preserving Restore Collision Policy

- Status: Accepted; fidelity pending portability audits
- Date: 2026-09-28

## Context

A Backup preserves `profileId` and identity material. Importing it as a second row in the same local catalogue would collide with the stable identifier and would permit two locally managed instances of one identity to run concurrently.

## Decision

`profileId` remains the unique catalogue identifier and no second local instance identifier is introduced. When a Backup or Transfer identity is absent from the target catalogue, import may create that identity after compatibility checks. When the same `profileId` already exists, import is rejected unless the user explicitly chooses the same-profile recovery/replace workflow. That workflow locks the existing profile, stages and verifies the incoming data, retains the current recoverable state, and atomically commits or rolls back; it never creates a second runnable catalogue entry.

Creating another locally runnable profile always uses Duplicate-as-new, with a new `profileId`, `profileSecret`, identity lineage, and data directory. An exported container outside the catalogue cannot be globally revoked, so warnings and local locks do not constitute distributed exclusivity.

## Consequences

Primary-key and identity semantics stay aligned, and same-catalogue concurrent identity duplication is prevented. Restore UX must distinguish new-catalogue import from replacement recovery. Cross-host fidelity and state behavior remain gated by `AUD-010`, `AUD-021`, `AUD-022`, and `AUD-026`.


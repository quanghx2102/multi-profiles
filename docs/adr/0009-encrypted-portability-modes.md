# ADR-0009: Encrypted Portability with Three Explicit Modes

- Status: Accepted; fidelity pending audit
- Date: 2026-09-27

## Context

Backup, identity transfer, and creation of a separate profile have different identity and security semantics. A generic clone/export command would make accidental identity duplication likely.

## Decision

Expose Backup, Transfer, and Duplicate as new profile as separate workflows. Containers use authenticated encryption, versioned schemas, integrity checks, and streaming operation without plaintext ZIP staging. Separately managed credentials are excluded by default. Opaque browser state is treated as potentially session/credential-bearing until `AUD-026` establishes what can be safely excluded. Same-identity catalogue collisions follow [ADR-0013](0013-identity-preserving-restore-collision-policy.md).

## Consequences

The UI and import validator must preserve mode and collision semantics. Local-only transfer cannot enforce a distributed lock. Fidelity, sensitive-state classification, and host dependence remain gated by `AUD-010`, `AUD-021`, `AUD-022`, and `AUD-026`.

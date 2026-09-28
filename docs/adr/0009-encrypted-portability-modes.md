# ADR-0009: Encrypted Portability with Three Explicit Modes

- Status: Accepted; fidelity pending audit
- Date: 2026-09-27

## Context

Backup, identity transfer, and creation of a separate profile have different identity and security semantics. A generic clone/export command would make accidental identity duplication likely.

## Decision

Expose Backup, Transfer, and Duplicate as new profile as separate workflows. Containers use authenticated encryption, versioned schemas, integrity checks, and streaming operation without plaintext ZIP staging. Credentials and authenticated sessions are excluded by default.

## Consequences

The UI and import validator must preserve mode semantics. Local-only transfer cannot enforce a distributed lock. Fidelity and host dependence remain gated by `AUD-010`, `AUD-021`, and `AUD-022`.


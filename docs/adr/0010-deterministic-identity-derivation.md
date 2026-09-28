# ADR-0010: Deterministic, Domain-Separated Identity Derivation

- Status: Accepted; algorithm parameters pending security review
- Date: 2026-09-28

## Context

A profile must retain the same configured identity across ordinary stop/start, crash recovery, and qualified core migration. Persisting unrelated random values independently makes completeness, recovery, and accidental regeneration difficult to verify.

## Decision

Create one cryptographically random `profileSecret` per new profile and keep it behind an opaque protected-store handle. Derive every deterministic identity surface from that secret using named, versioned, domain-separated inputs. The derivation namespace and identity schema are immutable identity metadata. Missing required derivation material fails closed; an existing profile never receives replacement randomness.

The concrete KDF, labels, salt rules, output lengths, recovery representation, and approved cryptographic library require a security design review before implementation. Camoufox consumption and propagation of derived values remain evidence questions in `AUD-001`, `AUD-002`, `AUD-003`, `AUD-006`, `AUD-007`, and `AUD-022`.

## Consequences

The same protected input can reproduce required configured values without storing plaintext seed material throughout the system. Schema evolution must define deterministic, reviewed derivation rules and cannot silently reinterpret old labels. Loss of the protected secret is a recovery failure, not permission to regenerate the identity.


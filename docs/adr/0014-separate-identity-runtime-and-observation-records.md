# ADR-0014: Separate Identity, Runtime Configuration, and Observations

- Status: Accepted
- Date: 2026-09-28

## Context

Browser core selection, proxy assignment, observations, and compatibility results change over time. Keeping them inside the canonical identity manifest would either make identity appear mutable or create competing sources of truth with the profile aggregate.

## Decision

Store four distinct record classes:

- the identity manifest holds immutable identity inputs, protected-secret reference, derivation metadata, and integrity information;
- runtime configuration holds mutable operational choices such as active core, proxy assignment, approved extensions, and non-identity launch preferences;
- fingerprint baselines hold normalized observations for a specific engine/core/probe/environment tuple;
- compatibility records are immutable operation outputs describing whether a proposed launch, migration, restore, or import is allowed.

The profile aggregate owns references and transition rules across these records. A manifest schema migration may change representation only when it preserves the same identity semantics; a semantic identity change creates a new profile.

## Consequences

There is one authority for each class of fact. Core or proxy changes no longer rewrite identity data. Transactions that activate a core also move the corresponding accepted baseline reference, while compatibility reports remain evidence rather than mutable profile truth.


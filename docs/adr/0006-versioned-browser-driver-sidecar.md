# ADR-0006: Language-Neutral, Versioned Browser-Driver Sidecar

- Status: Accepted; language and transport pending audit
- Date: 2026-09-27

## Context

Camoufox launch and Playwright integration may be more reliable in TypeScript or Python. Binding the Rust Core to one launcher language would make engine integration and recovery policy fragile.

## Decision

Run browser integration in a separately supervised sidecar behind a typed, versioned, testable protocol. Prefer TypeScript only if its launcher passes parity and persistent-lifecycle audit; otherwise use Python. Rust application policy remains independent of this choice.

## Consequences

Cross-process failure and protocol negotiation become explicit. Secrets cannot be passed via argv or ordinary logs. `AUD-012` selects the initial implementation language; `AUD-024` validates transport, authentication, idempotency, and crash recovery.


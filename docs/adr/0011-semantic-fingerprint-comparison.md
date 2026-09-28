# ADR-0011: Semantic Fingerprint Comparison

- Status: Accepted; comparison policy pending audit evidence
- Date: 2026-09-28

## Context

Raw byte equality across browser cores, hosts, and probe versions would reject harmless representation changes, while accepting every change would hide identity drift. Some observations may be stable categorical values, some normalized sets, and some host-dependent measurements.

## Decision

Compare versioned, normalized fingerprint observations using a reviewed semantic policy. Each probe field is classified as invariant, allowed-set/range, environment-qualified, informational, or forbidden-to-change. A baseline is bound to profile, engine, core, probe schema, and environment descriptor. Missing mandatory observations, cross-context contradictions, and unexplained changes to immutable identity are hard failures.

No tolerance, normalization, or field classification is approved merely by this ADR. `AUD-019` and `AUD-022`, supported by the surface-specific audits, must provide the evidence.

## Consequences

Core qualification and profile preflight produce explainable field-level diffs instead of a single opaque hash result. Baselines cannot be silently rewritten after a failed check. The probe schema, normalization rules, and comparison policy become versioned compatibility inputs and require regression coverage.


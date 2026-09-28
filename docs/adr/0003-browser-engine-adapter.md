# ADR-0003: Capability-Based Browser Engine Adapters

- Status: Accepted
- Date: 2026-09-27

## Context

Camoufox is the first candidate but binds behavior to Firefox/Gecko. A future Chromium engine should not require rewriting profile, storage, security, or lifecycle policy.

## Decision

All browser engines implement a versioned, capability-based `BrowserEngine` contract. Domain and application code do not depend on Camoufox, Chromium, Playwright, or launcher-specific types. Camoufox is the first adapter only after its Phase 1 go decision.

## Consequences

Capabilities can differ without engine-name conditionals in the domain. The common contract must stay behavioral and avoid lowest-common-denominator leakage. A future Chromium adapter still requires an independent spike (`AUD-025`).


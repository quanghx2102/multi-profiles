# ADR-0007: Immutable Profile Engine Binding

- Status: Accepted
- Date: 2026-09-27

## Context

Firefox- and Chromium-family identities and browser data are not equivalent. Reinterpreting a profile in place could create incoherent fingerprints and corrupt engine-specific state.

## Decision

`engineId` is immutable. Moving to another engine creates a new profile with a new `profileId`, `profileSecret`, and identity. Only explicitly compatible data such as bookmarks, selected cookies, notes/tags, extensions/configuration where supported, and proxy configuration may be copied.

## Consequences

There is no one-click engine switch that claims identity continuity. Cross-engine copying requires an explicit compatibility report and excludes opaque engine state by default.


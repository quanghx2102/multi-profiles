# ADR-0004: One Browser Process Tree per Running Profile

- Status: Accepted, feasibility audit pending
- Date: 2026-09-27

## Context

Profile isolation requires separate mutable browser state and controlled failure domains. Sharing a browser process or persistent context could introduce cross-profile state and lifecycle coupling.

## Decision

Each running profile owns one separately supervised Camoufox process tree, dedicated user data directory, exclusive profile lock, and sidecar session. No mutable cookie, storage, extension, or identity state is shared.

## Consequences

Isolation and crash attribution improve, while memory/CPU/GPU and process-management costs rise. Camoufox multi-instance interference and the supported concurrency envelope must be demonstrated by `AUD-004` and `AUD-014`.


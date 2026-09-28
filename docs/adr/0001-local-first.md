# ADR-0001: Local-First, Single-User Product

- Status: Accepted
- Date: 2026-09-27

## Context

The intended user operates profiles on one computer and does not need team collaboration or continuous cross-device synchronization. Cloud infrastructure would expand authentication, privacy, distributed consistency, and operations scope before the browser/profile risks are understood.

## Decision

Version 1 is a Windows-first, local-only, single-user desktop product. Authoritative profile data remains local. Portability is provided through encrypted import/export.

## Consequences

The design is smaller and secrets need not be sent to a service. It cannot provide distributed locks, real-time sync, centralized team policy, or prevent a transferred identity from running elsewhere. Those limitations must be explicit.


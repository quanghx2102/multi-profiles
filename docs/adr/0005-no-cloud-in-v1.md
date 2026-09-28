# ADR-0005: No Cloud Sync or Team Workspace in Version 1

- Status: Accepted
- Date: 2026-09-27

## Context

Cloud sync is not required for the personal, one-machine use case. Occasional backup or handoff can be handled through portability containers.

## Decision

Do not build cloud sync, remote profile execution, team/workspace features, or a distributed lock service in Version 1. Provide encrypted Backup, Transfer, and Duplicate-as-new workflows instead.

## Consequences

The product cannot guarantee single execution after an export leaves the host and must warn about identity duplication. A future cloud design would require a separate ADR and threat model rather than extending the local lock implicitly.


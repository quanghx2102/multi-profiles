# ADR-0008: Side-by-Side, Staged Browser-Core Updates

- Status: Accepted; engine feasibility pending audit
- Date: 2026-09-27

## Context

Keeping an old browser forever creates security and compatibility problems, while immediate fleet-wide updates can change fingerprint behavior or profile storage.

## Decision

Install cores side by side and migrate profiles through verification, compatibility checks, canaries, semantic fingerprint diff, and commit-or-rollback. Support Stable Automatic, Manual Approval, and Pinned policies. Retain the old core through the rollback window.

## Consequences

Disk use and migration complexity increase. Byte-identical fingerprints are not required across versions, but immutable identity drift and unexplained cross-context changes are forbidden. `AUD-009`, `AUD-016`, and `AUD-020` must establish feasibility.


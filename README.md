# Local-First Browser Profile Manager

This repository currently contains the Phase 1 architecture and audit baseline for a Windows-first, single-user desktop application that manages isolated browser profiles. Camoufox/Firefox is the first intended browser engine, but it is treated as an adapter behind an engine-neutral contract.

No production application has been scaffolded. No runtime dependency has been installed or version-pinned during Phase 1; planned technology choices are recorded as architecture decisions only.

## Product intent

The product manages a set of local browser profiles. Each profile represents a durable device identity and owns an isolated browser data directory, proxy assignment, identity manifest, lifecycle journal, and recovery history. Stopping and starting a profile must not silently regenerate identity material or mix browser state with another profile.

The product promises browser-level isolation and measured fingerprint consistency. It does **not** promise that a site cannot correlate accounts or that the browser is "undetectable". Network reputation, account behavior, payment data, and server-side graphs remain outside this guarantee.

## Phase 1 status

Phase 1 is documentation and evidence planning only. Camoufox behavior remains unverified until the source and experiments named in the [Audit Register](docs/AUDIT_REGISTER.md) are completed.

Start with:

- [Documentation Governance](docs/DOCUMENTATION_GOVERNANCE.md)
- [Product Scope](docs/PRODUCT_SCOPE.md)
- [Requirement Catalogue](docs/REQUIREMENTS.md)
- [Feature Disposition Matrix](docs/FEATURE_MATRIX.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Development Phases](docs/DEVELOPMENT_PHASES.md)
- [Detailed Phase Specifications](docs/phases/README.md)
- [Audit Register](docs/AUDIT_REGISTER.md)
- [Audit Evidence Templates](docs/audit/README.md)
- [Camoufox Audit Workspace](research/camoufox/README.md)
- [Draft Contract Schemas](contracts/README.md)
- [Data Authority](docs/DATA_AUTHORITY.md)
- [Decisions Requiring Approval](docs/DECISIONS_REQUIRED.md)
- [Test Strategy](docs/TEST_STRATEGY.md)
- [Decision and Requirement Traceability](docs/TRACEABILITY.md)
- [Architecture Decision Records](docs/adr/)

## Documentation authority

When documents appear to conflict, follow [Documentation Governance](docs/DOCUMENTATION_GOVERNANCE.md). Accepted ADRs govern architectural choices, the audit register governs evidence status, the requirement catalogue governs stable requirement IDs, and the product scope plus feature matrix govern feature boundaries. Terms have the meanings defined in the [Glossary](docs/GLOSSARY.md).

Run the dependency-free documentation check with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/docs-check.ps1
```

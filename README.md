# Local-First Browser Profile Manager

This repository currently contains the Phase 1 architecture and audit baseline for a Windows-first, single-user desktop application that manages isolated browser profiles. Camoufox/Firefox is the first intended browser engine, but it is treated as an adapter behind an engine-neutral contract.

No production application has been scaffolded. A disposable external Python environment and Camoufox browser cache were created for the authorized Phase 1 spike; candidate versions/hashes and reviewed evidence are recorded under `research/camoufox`, not added as product dependencies.

## Product intent

The product manages a set of local browser profiles. Each profile represents a durable device identity and owns an isolated browser data directory, proxy assignment, identity manifest, lifecycle journal, and recovery history. Stopping and starting a profile must not silently regenerate identity material or mix browser state with another profile.

The product promises browser-level isolation and measured fingerprint consistency. It does **not** promise that a site cannot correlate accounts or that the browser is "undetectable". Network reputation, account behavior, payment data, and server-side graphs remain outside this guarantee.

## Phase 1 status

Phase 1 audit work is active. Initial beta.31 source/runtime evidence exists, but no audit is confirmed or resolved; the current official Windows artifact is on distribution hold under `AUD-015` because of its bundled-font notice. See the [Audit Register](docs/AUDIT_REGISTER.md) and [Results Index](research/camoufox/RESULTS_INDEX.md).

Start with:

- [Documentation Governance](docs/DOCUMENTATION_GOVERNANCE.md)
- [Product Scope](docs/PRODUCT_SCOPE.md)
- [Requirement Catalogue](docs/REQUIREMENTS.md)
- [Feature Disposition Matrix](docs/FEATURE_MATRIX.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Development Phases](docs/DEVELOPMENT_PHASES.md)
- [Phase Work Breakdown and Progress](docs/WORK_BREAKDOWN.md)
- [Detailed Phase Specifications](docs/phases/README.md)
- [Audit Register](docs/AUDIT_REGISTER.md)
- [Audit Evidence Templates](docs/audit/README.md)
- [Camoufox Audit Workspace](research/camoufox/README.md)
- [Draft Contract Schemas](contracts/README.md)
- [Data Authority](docs/DATA_AUTHORITY.md)
- [Decisions Requiring Approval](docs/DECISIONS_REQUIRED.md)
- [Test Strategy](docs/TEST_STRATEGY.md)
- [Decision and Requirement Traceability](docs/TRACEABILITY.md)
- [Documentation Review and Rationalization](docs/DOCUMENTATION_REVIEW.md)
- [Windows Security Boundary Proposal](docs/WINDOWS_SECURITY_BOUNDARIES.md)
- [Physical Schema, API, and Binding Readiness](docs/PHYSICAL_SCHEMA_API_BINDINGS.md)
- [Architecture Decision Records](docs/adr/)

## Documentation authority

When documents appear to conflict, follow [Documentation Governance](docs/DOCUMENTATION_GOVERNANCE.md). Accepted ADRs govern architectural choices, the audit register governs evidence status, the requirement catalogue governs stable requirement IDs, and the product scope plus feature matrix govern feature boundaries. Terms have the meanings defined in the [Glossary](docs/GLOSSARY.md).

Run the dependency-free documentation check with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/docs-check.ps1
```

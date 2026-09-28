# Repository Instructions

These instructions preserve the Phase 1 decisions for future coding agents.

## Current phase

- The repository is in Phase 1: audit and technical documentation.
- Do not add production code, scaffold Tauri/Rust/React, install dependencies, clone or modify Camoufox, or build a browser unless a later user request explicitly starts the relevant implementation or audit work.
- Treat every unverified Camoufox claim as a hypothesis and link it to an `AUD-*` item in `docs/AUDIT_REGISTER.md`.
- Do not change an audit item to `CONFIRMED` or `RESOLVED` without recorded source or test evidence at the required quality.

## Required workflow

1. Identify the current phase and its entry/exit gate.
2. Read [documentation governance](docs/DOCUMENTATION_GOVERNANCE.md), the relevant authority document, and [decisions required](docs/DECISIONS_REQUIRED.md).
3. Name the applicable `REQ-*`/`SEC-*`/`INV-*`, `AUD-*`, and ADR IDs before changing behavior.
4. Record runtime uncertainty in the Audit Register; never close it by assumption.
5. Record an architecture change in a new superseding ADR; do not overwrite an Accepted decision.
6. Update the canonical schema and generated bindings together once binding generation exists.
7. Never edit a file marked generated; update its source and regenerate it.
8. Do not promote audit status without evidence meeting the documented threshold.
9. Run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/docs-check.ps1` for documentation/schema changes and the applicable tests for implementation changes.
10. Report unresolved or blocked decisions explicitly.
11. Preserve user changes and inspect Git status before and after work.
12. Do not use destructive Git commands or push/merge without explicit authorization.

## Durable rules

- Domain and application logic must remain independent of Tauri, SQLite, Playwright, Camoufox, Chromium, and concrete filesystem implementations.
- Browser engines are accessed through the capability-based engine contract.
- A profile's `engineId`, `profileId`, and `profileSecret` are immutable after creation.
- The UI must not access the database, spawn a browser, execute arbitrary shell commands, or handle plaintext secrets directly.
- Do not put secrets in command-line arguments, logs, diagnostics, or export staging files.
- Keep module APIs explicit; do not deep-import another module's implementation.
- Architecture changes require an ADR. Runtime uncertainty requires an audit item or an update to an existing one.

## Documentation conventions

- Repository documentation is written in English.
- Avoid duplicating long requirements; cross-link to the owning document.
- State failure behavior for lifecycle operations and contracts.
- For each module, state what it owns and what it explicitly does not own.
- Use the terminology in `docs/GLOSSARY.md`.
- Keep requirements in `docs/REQUIREMENTS.md`, evidence status in `docs/AUDIT_REGISTER.md`, and phase documents limited to sequencing, deliverables, gates, and handoff.

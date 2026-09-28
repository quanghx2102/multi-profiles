# Camoufox Phase 1 Research Workspace

- Status: Ready for authorized audit work; no audit executed
- Owner: Phase 1 audit team
- Last reviewed: 2026-09-28

This workspace receives reproducible Camoufox source and runtime evidence after the user authorizes audit execution. It contains no Camoufox clone, browser binary, real user profile, credential, or completed result.

## Entry points

- [UPSTREAM_LOCK.json](UPSTREAM_LOCK.json): immutable input selection; currently `UNSELECTED`.
- [AUDIT_PLAN.md](AUDIT_PLAN.md): fail-fast execution order and audit mapping.
- [PATCH_REGISTER.md](PATCH_REGISTER.md): local/upstream patch inventory template.
- [RESULTS_INDEX.md](RESULTS_INDEX.md): evidence/report index; currently empty.
- [evidence/README.md](evidence/README.md): evidence record and retention policy.
- [probes/README.md](probes/README.md): probe ownership and promotion rules.
- [fixtures/README.md](fixtures/README.md): synthetic/disposable fixture policy.
- [experiments/README.md](experiments/README.md): pre-registration and run layout.

## Rules

1. Pin exact source/artifact/dependency inputs before inspecting or running them.
2. Pre-register expected result, environment, command/config, redaction, and stop conditions.
3. Keep source evidence, runtime evidence, inference, and decision separate.
4. Use only synthetic/disposable profiles and controlled accounts.
5. Commit reports/manifests and small reviewed evidence only. Large or sensitive artifacts use the approved external store with stable locator, hash, access, and retention metadata.
6. Do not commit browser binaries, source clones, raw profile directories, cookie/login/key databases, crash dumps, credentials, tokens, or secrets.
7. A research result does not change an audit status until reviewed and linked from `docs/AUDIT_REGISTER.md`.


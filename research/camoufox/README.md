# Camoufox Phase 1 Research Workspace

- Status: Phase 1 audit active; initial candidate/source/runtime evidence recorded
- Owner: Phase 1 audit team
- Last reviewed: 2026-09-28

This workspace contains reviewed, reproducible Phase 1 source/runtime evidence. Camoufox source clones, browser binaries, disposable profile directories, and Python environments remain outside the repository; no real user profile or credential is used.

## Entry points

- [UPSTREAM_LOCK.json](UPSTREAM_LOCK.json): beta.31 candidate lock; partially verified and not approved for distribution.
- [AUDIT_PLAN.md](AUDIT_PLAN.md): fail-fast execution order and audit mapping.
- [PATCH_REGISTER.md](PATCH_REGISTER.md): local/upstream patch inventory template.
- [RESULTS_INDEX.md](RESULTS_INDEX.md): evidence/report index.
- [FINGERPRINT_SURFACE_CATALOG.md](FINGERPRINT_SURFACE_CATALOG.md): source-declared beta.31 surface groups and unaccepted tolerance candidates.
- [BROWSER_STATE_CHECKPOINT_MATRIX.md](BROWSER_STATE_CHECKPOINT_MATRIX.md): observed clean-close state and checkpoint/portability gaps.
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

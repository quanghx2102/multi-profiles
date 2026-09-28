# Audit Evidence Workspace

## Purpose

This directory defines how Phase 1 research and technical-spike evidence will be recorded. It contains templates only; their presence is not evidence and does not change any `AUD-*` status.

## Proposed artifact layout

Create an item directory only when work on that audit is authorized:

```text
docs/audit/AUD-NNN/
  REPORT.md
  evidence/
    manifest.md
    source/
    runs/
    logs/
    screenshots/
  fixtures/
```

Large or sensitive raw artifacts may be stored in an approved external evidence location. `REPORT.md` must then record the stable locator, access constraints, size, cryptographic hash, and retention policy. Secrets, cookies, tokens, credential databases, and unredacted profile data must not be committed.

## Workflow

1. Copy [AUDIT_REPORT_TEMPLATE.md](AUDIT_REPORT_TEMPLATE.md) to the item's `REPORT.md`.
2. Pin source revisions, artifact hashes, host/environment, procedure, expected result, and redaction rules before the run.
3. Use [EVIDENCE_MANIFEST_TEMPLATE.md](EVIDENCE_MANIFEST_TEMPLATE.md) to inventory every retained artifact.
4. Keep raw observations distinct from interpretation and from the eventual decision.
5. Link exact source paths/lines or symbols and every reproducible command without embedding secrets.
6. Review redaction and hashes before commit.
7. Update [AUDIT_REGISTER.md](../AUDIT_REGISTER.md) only after the evidence bundle is reviewable.

## Naming and integrity

- Use UTC timestamps in `YYYYMMDDTHHMMSSZ` form for run directories.
- Keep original raw output immutable; create separately named redacted derivatives.
- Record SHA-256 for retained files and identify the tool used to compute it.
- Identify fixtures as synthetic/disposable and never reuse real user profiles.
- A changed procedure or pinned version creates a new run; it does not overwrite the prior run.

## Evidence quality

The [Audit Register](../AUDIT_REGISTER.md) remains authoritative for quality and status. A report must explicitly distinguish source evidence, runtime evidence, and inference. One passing host or an upstream claim alone does not establish cross-environment behavior.


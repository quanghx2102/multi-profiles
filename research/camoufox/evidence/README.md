# Evidence Records

This directory may contain only small, reviewed, redacted evidence and manifests. Large or sensitive raw artifacts must use the approved external location from `DEC-EVIDENCE-001` and be referenced by stable locator and SHA-256.

## Required evidence record

| Field | Requirement |
|---|---|
| Evidence ID | Stable `EVD-AUD-NNN-NNN` identifier |
| Audit ID | Existing `AUD-NNN` |
| Evidence kind | `SOURCE`, `RUNTIME`, `ARTIFACT`, `LEGAL_REVIEW`, or `INFERENCE` |
| Source revision | Exact upstream-lock revision(s); no floating branch |
| Artifact hash | SHA-256 for every retained input/output artifact, or reason not applicable |
| Environment ID | Defined environment plus exact run deviations |
| Command/config | Exact reproducible command/config with secret redaction; never include plaintext secrets |
| Expected result | Pre-registered before execution |
| Observed result | Raw observation distinguished from interpretation |
| Confounders | Known uncontrolled variables, failures, and limitations |
| Reproduction steps | Setup, inputs, sequence, cleanup, and expected artifact list |
| Evidence quality | Register enum: `NONE`, `HYPOTHESIS`, `DOCUMENTED`, `SOURCE_CONFIRMED`, `TEST_CONFIRMED`, `MULTI_ENV_CONFIRMED` |
| Reviewer | Named reviewer and review disposition |
| Timestamp | UTC ISO-8601 capture/review timestamps |

## Prohibited content

Do not commit browser binaries/source clones, real profile directories, `cookies.sqlite`, `logins.json`, `key4.db`, raw crash dumps, private keys, access tokens, proxy credentials, authenticated URLs, or unredacted environment dumps. Synthetic fixture values must be visibly marked and nonfunctional outside the controlled test.


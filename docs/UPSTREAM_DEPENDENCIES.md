# Upstream Dependencies and Pinning Policy

- Status: Draft / beta.31 candidate partially verified
- Owner: Phase 1 provenance workstream
- Last reviewed: 2026-09-28
- Review trigger: Any upstream-lock selection or update proposal

## Evidence boundary

The beta.31 candidate is pinned in `research/camoufox/UPSTREAM_LOCK.json`. It is not an accepted distribution or Phase 2 input: transitive/source mapping, signature/reproducible-build evidence, and legal review remain incomplete, and `AUD-015` records a bundled-font distribution blocker.

## Dependency inventory

| Dependency | Candidate official locator | Purpose | Pinning unit | License/status | Audit |
|---|---|---|---|---|---|
| Camoufox browser/build/launcher repository | <https://github.com/daijro/camoufox> | Firefox-derived candidate engine, patches/build inputs, launcher packages | Full immutable commit plus selected release/artifact hashes | beta.31 candidate pinned; distribution held by `AUD-015` | `AUD-015`, `AUD-016`, `AUD-023` |
| Camoufox documentation | <https://camoufox.com/> | Discovery of intended configuration/launcher behavior | Documentation snapshot date and source revision where available | Claims remain hypotheses until source/test evidence | Relevant behavioral audits |
| BrowserForge | <https://github.com/daijro/browserforge> | Candidate fingerprint/header generator dependency if present in selected launcher | Immutable commit and resolved package artifact | `1.2.4` artifact pinned; source mapping review pending | `AUD-001`, `AUD-012`, `AUD-015` |
| Firefox base | Locator derived from selected Camoufox build inputs | Upstream browser source | Exact Firefox revision/source archive hash | `152.0.4` source/hash pinned; checksum signature not verified | `AUD-015`, `AUD-020`, `AUD-023` |
| Playwright | Locator/manifests derived from selected launcher | Candidate automation transport/library | Exact resolved package version/artifact hash | Python `1.62.0` Windows artifact pinned; source mapping pending | `AUD-012`, `AUD-024` |
| Other generator/runtime dependencies | Discovered from pinned manifests | Identity generation, build, packaging, or runtime support | Lockfile-resolved commit/version/artifact | `UNSELECTED` | `AUD-001`, `AUD-015`, `AUD-016` |

## Selection procedure

1. Verify repository ownership/official status from multiple upstream-controlled references.
2. Select a candidate release for a documented audit objective; never use a floating branch as the input.
3. Resolve the release to an immutable commit and capture tag/signature metadata without treating a tag name as integrity proof.
4. Inventory submodules, vendored code, package manifests/lockfiles, build downloads, Firefox base, launcher, and generator dependencies.
5. Obtain platform artifacts only from the approved source, record size and SHA-256, and record available signature/provenance metadata independently.
6. Snapshot exact license/notice files for source and every shipped artifact; record `UNKNOWN` rather than infer obligations.
7. Review maintenance/security state and select/reject the candidate through the relevant audits.
8. Write the approved values atomically to `UPSTREAM_LOCK.json`; require review for every change.

## Update review

An upstream change creates a new candidate lock. It does not mutate existing evidence. Review release/source diffs, patch/config schema, generator data, dependencies, licenses, artifacts/signatures, known security issues, launcher parity, qualification impact, and rollback compatibility. A floating `main`, `latest`, `stable`, unpinned package range, or URL without a recorded immutable digest is forbidden in an audit/build input.

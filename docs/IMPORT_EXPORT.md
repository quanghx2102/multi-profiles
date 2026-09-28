# Import and Export

## Modes

### Backup

- Preserves `profileId`, identity lineage, `profileSecret`, compatible browser state, and recovery metadata.
- Leaves the source profile active and valid.
- Restoring creates another local copy of the same identity; the UX warns against concurrent use.

### Transfer

- Preserves identity and selected browser state.
- Archives or marks the source as transferred after a successful destination acknowledgement when both operations are locally coordinated.
- Warns that a local-only product cannot enforce a distributed lock after the container leaves the machine.

### Duplicate as new profile

- Creates a new `profileId`, `profileSecret`, seeds, and fingerprint identity.
- May copy non-identity configuration such as bookmarks, allowed extensions, notes/tags, and proxy settings.
- Does not copy saved passwords or authenticated sessions by default.

These modes must be explicit; a generic "clone" action is not permitted.

## Container requirements

The portability container has a magic/version header, authenticated manifest, encrypted payload records, integrity-protected index, required OS/platform, engine and core compatibility metadata, identity/export mode, binary hash references, content inventory, and KDF/AEAD parameters. Exact algorithms require security design review.

Required behavior:

- authenticated encryption;
- streaming creation and extraction without a plaintext ZIP staging file;
- schema and format versions independent of application version;
- integrity check before committing imported data;
- no reproducible cache by default;
- no saved passwords, proxy credentials, API tokens, or other credentials by default;
- collision-safe staging and atomic finalization;
- import compatibility report before mutation.

## Import workflow

1. Read only the bounded public header.
2. Validate format, size limits, mode, platform, and cryptographic parameters.
3. Acquire/decrypt key material through the approved secret flow.
4. Stream-decrypt into a private staging location while authenticating every record.
5. Validate manifest integrity, paths, engine/core requirements, and data inventory.
6. Run compatibility and identity checks.
7. Present or apply the mode-specific plan.
8. Commit metadata and move staged data atomically where possible.
9. Run fingerprint preflight before the imported profile becomes `READY`.
10. Remove staging according to secure cleanup policy and journal the result.

Path traversal, symlinks/reparse points, oversized records, duplicate IDs, unknown critical fields, and partially authenticated data are rejected.

## Portability limits

Successful decryption does not prove identity portability. Same-OS import preservation is gated by `AUD-021`; cross-hardware Windows behavior by `AUD-010` and `AUD-022`; extension and saved-state behavior by `AUD-005` and `AUD-011`.

## Failure handling

An import never modifies an existing profile in place. A failed export leaves no usable partial container and does not alter the source. A failed transfer does not archive the source unless destination commit is positively established by the supported local workflow.


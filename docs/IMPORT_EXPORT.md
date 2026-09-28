# Import and Export

## Modes

### Backup

- Preserves `profileId`, identity lineage, `profileSecret`, compatible browser state, and recovery metadata.
- Leaves the source profile active and valid.
- When the target catalogue does not contain `profileId`, restore may create that identity after compatibility checks.
- When the same `profileId` exists, restore is only an explicit same-profile staged replace/recovery; it cannot create a second runnable catalogue entry.

### Transfer

- Preserves identity and selected browser state.
- Archives or marks the source as transferred after a successful destination acknowledgement when both operations are locally coordinated.
- Warns that a local-only product cannot enforce a distributed lock after the container leaves the machine.

### Duplicate as new profile

- Creates a new `profileId`, `profileSecret`, seeds, and fingerprint identity.
- May copy non-identity configuration such as bookmarks, allowed extensions, notes/tags, and proxy settings.
- Does not intentionally copy saved passwords or authenticated sessions by default; safe selective handling is gated by `AUD-026`.

These modes must be explicit; a generic "clone" action is not permitted.

## Data inclusion policy matrix

`Include` means the product intends to carry the datum. `Exclude` means it must not be present. `Decision required` is not an implementation default. Any selective handling of opaque browser state remains blocked by `AUD-005` and `AUD-026`.

| Data type | Backup | Transfer | Duplicate as new | Decision status / rationale |
|---|---|---|---|---|
| Cookies | Decision required | Decision required | Exclude by default | Proposed; authenticated-session sensitivity and separability unverified |
| LocalStorage | Decision required | Decision required | Exclude by default | Proposed; can contain authentication tokens |
| IndexedDB | Decision required | Decision required | Exclude by default | Proposed; origin data may be identity/session bearing |
| Cache | Exclude | Exclude | Exclude | Accepted; reproducible, high-volume state |
| History | Include | Include | Decision required | Proposed; useful fidelity but privacy-sensitive |
| Session restore | Decision required | Decision required | Exclude | Proposed; cannot launch restored external tabs before preflight |
| Saved passwords | Exclude unless an explicit sensitive full-state mode is approved | Same as Backup | Exclude | Decision required; safe exclusion from opaque state is unverified |
| Form data | Decision required | Decision required | Exclude by default | Proposed; may contain secrets or personal data |
| Extension files/state | Include only for qualified compatible extensions | Same as Backup | Copy only allowlisted non-identity extension state | Proposed; gated by `AUD-011`, `AUD-026` |
| Proxy configuration | Include endpoint/mode reference where portable | Include endpoint/mode reference where portable | Copy only by explicit user choice | Proposed; proxy is mutable runtime configuration |
| Proxy credentials | Exclude by default | Exclude by default | Exclude | Accepted default; use separate protected enrollment |
| Profile secret | Include in protected payload | Include in protected payload | Exclude and generate a new secret | Accepted identity semantics; cryptographic format remains design review |
| Fingerprint baselines | Include compatible accepted/history records | Include compatible accepted/history records | Exclude and create new candidates | Proposed; preservation must not bypass destination preflight |
| Recovery history | Include bounded verified recovery metadata | Include only what destination recovery requires | Exclude | Proposed; retention and privacy policy pending |

The defaults requiring approval are tracked as `DEC-PORTABILITY-001` in [Decisions Required](DECISIONS_REQUIRED.md). A full-state container, if later approved, must be labelled sensitive rather than described as credential-free.

## Container requirements

The portability container has a magic/version header, authenticated manifest, encrypted payload records, integrity-protected index, required OS/platform, engine and core compatibility metadata, identity/export mode, binary hash references, content inventory, and KDF/AEAD parameters. Exact algorithms require security design review.

Required behavior:

- authenticated encryption;
- streaming creation and extraction without a plaintext ZIP staging file;
- schema and format versions independent of application version;
- integrity check before committing imported data;
- no reproducible cache by default;
- no proxy credentials, API tokens, or separately managed application credentials by default;
- no claim that opaque browser profile files exclude saved passwords or authenticated sessions until `AUD-026` proves a file/key-level policy;
- collision-safe staging and atomic finalization;
- import compatibility report before mutation.

## Import workflow

1. Read only the bounded public header.
2. Validate format, size limits, mode, platform, and cryptographic parameters.
3. Acquire/decrypt key material through the approved secret flow.
4. Stream-decrypt into a private staging location while authenticating every record.
5. Validate manifest integrity, paths, engine/core requirements, and data inventory.
6. Run compatibility and identity checks.
7. Present or apply the mode-specific plan, including same-profile collision handling.
8. Commit metadata and move staged data atomically where possible.
9. Launch only into `LAUNCHED_UNVERIFIED` and run fingerprint preflight before the imported profile becomes launchable (`READY` or `STOPPED`, pending [ADR-0017](adr/0017-launchable-steady-state.md)).
10. Remove staging according to secure cleanup policy and journal the result.

Path traversal, symlinks/reparse points, oversized records, unknown critical fields, and partially authenticated data are rejected. An existing `profileId` is also rejected unless the user chose the same-profile replace/recovery workflow defined by [ADR-0013](adr/0013-identity-preserving-restore-collision-policy.md).

## Portability limits

Successful decryption does not prove identity portability. Same-OS import preservation is gated by `AUD-021`; cross-hardware Windows behavior by `AUD-010` and `AUD-022`; extension and saved-state behavior by `AUD-005`, `AUD-011`, and `AUD-026`.

The product must not advertise a raw user-data-directory export as both full-fidelity and credential/session-free without evidence. Until `AUD-026` is decided, opaque browser state is classified as potentially containing authenticated session and credential material. A later design may approve a bounded sanitized mode, an explicitly sensitive full-state mode, or rejection of state types that cannot be separated safely.

## Failure handling

An import never partially overwrites an existing profile. Same-profile recovery stages and verifies a complete replacement, retains a rollback point, and commits atomically where supported. A failed export leaves no usable partial container and does not alter the source. A failed transfer does not archive the source unless destination commit is positively established by the supported local workflow.

# Security Model

## Security objectives

- Protect profile secrets, credentials, session data, and export key material from UI and logs.
- Prevent an untrusted renderer or local caller from gaining arbitrary database, filesystem, shell, or browser control.
- Reject tampered browser cores, manifests, snapshots, and portability containers.
- Contain compromise or crash of the browser-driver sidecar and browser process.
- Produce useful diagnostics without disclosing sensitive content.

## Trust boundaries

### Desktop renderer to Rust Core

The renderer is not trusted with secrets or ambient filesystem/process authority. It invokes an allowlist of typed commands. Rust validates structure, length, enum values, state preconditions, identifiers, and authorization before reaching application use cases. There is no generic SQL, path, URL-fetch, or shell command bridge.

### Rust Core to sidecar

The sidecar is less trusted than the core. The local channel requires protocol negotiation and instance authentication. Requests are scoped to an operation/profile, paths are resolved by the core, and secrets are not placed in argv, environment inherited broadly, or logs. The concrete secure transport and secret-delivery mechanism are open in `AUD-024`.

### Sidecar to browser/content

Web content is hostile. Automation results, page strings, downloaded files, and browser events are untrusted input. Browser process permissions and filesystem access are restricted to the assigned profile/core paths where the platform permits.

### Local automation API

The API binds loopback only by default, requires a high-entropy scoped authentication token, validates Origin where applicable, and must not rely on loopback as authentication. Exposure and authentication are tested under `AUD-018`.

### Artifact and import boundary

Browser binaries, update metadata, extensions, diagnostic inputs, and export containers are untrusted until verified. Archive entries cannot choose arbitrary destination paths.

## Secret inventory and placement

| Secret | Intended location | Never present in |
|---|---|---|
| Profile secret | OS keychain/protected core store | UI model, logs, argv, diagnostics |
| Proxy credential | OS keychain via opaque handle | manifest, argv, logs |
| Local API token | OS keychain/protected core store | URL query, normal logs |
| Export passphrase/key | short-lived protected memory/keychain flow | plaintext staging, logs |
| Cookies/session tokens | engine data directory; explicit protected export only | normal logs, diagnostics |

Implementation details and memory-zeroization guarantees are deferred to implementation security review.

## Required controls

- UI cannot read the database directly or spawn a process.
- IPC and sidecar inputs are schema validated and size bounded.
- Browser binaries are verified before execution (`AUD-016`).
- Manifest, snapshot, and export integrity is authenticated.
- Snapshot creation requires a confirmed checkpoint.
- Update policy prevents unauthorized downgrade or substitution.
- No arbitrary shell command facility is exposed to UI or local API.
- Logs redact cookies, tokens, credentials, `profileSecret`, seed material, and sensitive headers.
- Diagnostic bundles use an allowlist, not a denylist, for included data.
- File operations reject traversal and unsafe reparse/symlink behavior.
- Profile locks and local API tokens are not treated as distributed security controls.

## Threats requiring validation

Sidecar endpoint hijacking, token theft by another local process, browser escape, malicious extension behavior, antivirus quarantine, update-channel compromise, downgrade, export tampering, archive traversal, lock bypass, secret leakage in crash dumps, and proxy/DNS/WebRTC leakage require dedicated tests or later threat-model review. Relevant initial audits are `AUD-008`, `AUD-011`, `AUD-015`–`AUD-018`, and `AUD-024`.

## Diagnostics policy

Structured logs include timestamp, severity, module, event, operation/correlation ID, non-secret profile ID, engine/core identifiers, state transition, duration, and typed error code. They exclude page content by default. Process exit information and semantic fingerprint diffs are normalized and redacted. A diagnostic bundle contains a manifest of included files and applied redactions.


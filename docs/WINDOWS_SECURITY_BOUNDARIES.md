# Windows Process, Protected-Secret, and IPC Design

- Status: Proposed; primitive feasibility tested, integration not qualified
- Owner: Security and process-supervisor workstreams
- Last reviewed: 2026-09-29
- Review trigger: `AUD-024`, `AUD-031`, `AUD-033`, or `AUD-034` evidence/decision change

## Scope and evidence boundary

This document makes the Windows mechanisms concrete enough for Phase 1 testing. It does not authorize production adapters before the Phase 1 gate. The controlling requirements are `SEC-001`, `SEC-002`, and `SEC-004`; relevant audits are `AUD-024`, `AUD-031`, `AUD-033`, and `AUD-034`; topology remains `DEC-SIDECAR-001`.

The 2026-09-29 feasibility run proved only that a synthetic process created suspended can be assigned to a Job Object and terminated by closing a `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` job, and that DPAPI CurrentUser can protect/unprotect synthetic bytes with purpose entropy. It did not test a Camoufox tree, supervisor restart, a different Windows user, hostile same-user code, or packaged Tauri IPC.

## Process containment contract

The Rust `process-supervisor` is the sole creator and owner of each sidecar Job Object. The intended sequence is:

1. Resolve the sidecar executable and working directory from trusted installation IDs, reject reparse/path escape, verify the approved artifact identity, and construct a minimal environment block.
2. Create an unnamed Job Object and set `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`. Do not enable breakaway. Resource limits and UI restrictions remain opt-in only after browser compatibility tests.
3. Create the sidecar with `CreateProcessW`, `CREATE_SUSPENDED`, `CREATE_UNICODE_ENVIRONMENT`, no shell, no user-controlled command line, and no broad handle inheritance.
4. Assign the suspended sidecar to the Job Object before `ResumeThread`. Browser descendants must remain in the same job through normal job inheritance.
5. Use an I/O completion port or equivalent job notifications plus retained process handles for lifecycle evidence. A PID alone never proves ownership.
6. On a clean stop, request sidecar/browser shutdown, wait for the owned job to empty, record checkpoint evidence, then close handles. On forced stop or core loss, closing the final job handle terminates the owned tree.

Production process creation must use `STARTUPINFOEX` with `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` when a bootstrap handle is inherited. `bInheritHandles=TRUE` without an explicit handle list is forbidden. `CREATE_BREAKAWAY_FROM_JOB`, shell launch, PATH lookup, and arbitrary environment inheritance are forbidden.

`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` improves containment but does not prove state flush, block all browser exploits, or make PID adoption safe. Starting with Windows 8, nested jobs are supported, but actual Camoufox/Playwright behavior inside the selected job policy remains an `AUD-024` integration test. See Microsoft [Job Objects](https://learn.microsoft.com/windows/win32/procthread/job-objects) and [Process Creation Flags](https://learn.microsoft.com/windows/win32/procthread/process-creation-flags).

## Protected-secret store

The Phase 2 candidate is a `ProtectedSecretStore` adapter backed by DPAPI CurrentUser:

- use `CryptProtectData`/`CryptUnprotectData` without `CRYPTPROTECT_LOCAL_MACHINE`;
- use the non-interactive path and reject any UI-dependent protection flow;
- bind ciphertext to a versioned purpose string as optional entropy, such as `multi-profiles/profile-secret/v1`;
- persist only a versioned envelope containing algorithm/provider version, secret kind, created time, ciphertext, and integrity-safe metadata;
- store the envelope under a private, canonical, non-reparse application path with an explicit current-user/system ACL and atomic replace;
- return opaque secret handles to application modules; only the narrow consuming adapter may request plaintext;
- keep plaintext out of renderer models, SQLite fields, argv, environment, logs, crash diagnostics, and portability staging;
- make loss, wrong-user access, damaged ciphertext, and OS migration typed failures rather than regeneration.

DPAPI CurrentUser ties decryption to the user credentials on the same machine; machine scope is rejected because Microsoft documents that any user on that computer can decrypt machine-scoped data. Purpose entropy separates uses but is not an independent recovery key. The selected approach does not defend against malware, debuggers, or injected code already running as the same user. See Microsoft [`CryptProtectData`](https://learn.microsoft.com/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata).

Backup/Transfer cannot assume DPAPI ciphertext is portable. Phase 3 must explicitly decrypt through the protected-store port and re-encrypt into the approved authenticated portability container, or reject the operation.

## Core-to-sidecar transport

The Windows candidate is one duplex named pipe per dedicated sidecar instance. The pipe name is random and non-secret; access control and session authentication are both mandatory.

### Endpoint creation

- The Rust core creates the server endpoint before resuming the sidecar.
- Use a non-default security descriptor restricted to the current logon SID and required service/system identity; deny remote/network access. The Windows default named-pipe DACL is forbidden because Microsoft documents broader read access for Everyone and anonymous identities.
- Limit the pipe to one server instance, local clients, overlapped I/O, bounded buffers, and a connection/handshake deadline.
- After connection, obtain the client PID and verify it is the spawned sidecar process in the expected Job Object. PID validation supplements, but does not replace, handle/lifetime evidence.

Microsoft documents that named pipes can be remote when the Server service is available and recommends denying `NT AUTHORITY\\NETWORK` for local-only use; it also recommends a logon SID to exclude other terminal sessions. See [Named Pipes](https://learn.microsoft.com/windows/win32/ipc/named-pipes) and [Named Pipe Security and Access Rights](https://learn.microsoft.com/windows/win32/ipc/named-pipe-security-and-access-rights).

### Bootstrap and authentication

The core generates a 256-bit session token and delivers it once through an inherited anonymous-pipe read handle listed explicitly in `PROC_THREAD_ATTRIBUTE_HANDLE_LIST`. The token is never placed in argv, a normal environment variable, a named file, or a log.

The named-pipe handshake is challenge-response HMAC-SHA-256 over protocol version, a 256-bit core nonce, `sidecarInstanceId`, and `profileId`. Authentication failure closes the pipe and the owned job. The bootstrap token is zeroed/closed after negotiation and rotated for every sidecar instance. This authenticates possession; it does not provide confidentiality from a process already able to inspect the same-user process memory.

### Framing and protocol rules

- Four-byte big-endian unsigned length followed by one UTF-8 JSON object.
- Maximum frame size is 1 MiB initially; zero, oversized, truncated, malformed, and non-object frames fail closed.
- Negotiate protocol and capability versions before any effectful request.
- Every request carries a unique request ID, operation ID, profile ID, deadline, and operation-specific schema version.
- Mutations require idempotency handling and produce explicit `SUCCEEDED`, `FAILED`, `CANCELLED`, or `OUTCOME_UNKNOWN` results.
- Events carry a monotonic session sequence; gaps force reconciliation.
- Backpressure is bounded; unbounded queues and silent event dropping are forbidden.
- Payload schemas may carry opaque credential handles but never plaintext secrets.

The research framing/HMAC probe is intentionally transport-independent. Named-pipe ACLs, client identity, explicit handle inheritance, disconnect races, crash permutations, and Camoufox process-tree integration still require runtime evidence.

## Renderer-to-core Tauri IPC

The renderer uses only named application commands, never the sidecar pipe. The Phase 2 Tauri candidate must:

- explicitly enable only reviewed capabilities in `tauri.conf.json`;
- bind permissions to exact window/webview labels, local bundled origins only, with no wildcard remote URLs;
- expose no shell, generic filesystem, generic HTTP, SQL, process, or keychain command;
- validate generated request types plus total size, string length, enum, identifier, state, and authorization limits in Rust;
- return typed/redacted errors and operation references rather than raw logs or secret-bearing objects;
- treat renderer events as presentation hints, never lifecycle truth.

Tauri documents that capabilities constrain which windows/webviews may reach core commands, but they do not protect against insecure Rust command implementations. Therefore, capability configuration and application authorization tests are both required. See Tauri [Capabilities](https://v2.tauri.app/security/capabilities/) and [Runtime Authority](https://v2.tauri.app/security/runtime-authority/).

## Required integration tests before acceptance

| Boundary | Required proof | Current result |
|---|---|---|
| Job Object | Actual sidecar + full Camoufox descendant tree; clean/forced/core crash; no breakaway/orphan | Synthetic child only; researching |
| Binary/path | Reparse, writable parent, DLL search, replacement, long/UNC path, inherited handle/env | Not tested |
| DPAPI | Correct user, different user, damaged blob, reinstall/migration, ACL and seeded-log scan | Current-user synthetic round trip only |
| Named pipe | DACL/logon SID/remote denial, wrong client/PID/token, replay, frame fuzz, disconnect/backpressure | Framing and HMAC unit tests only |
| Tauri IPC | Exact pinned Tauri/WebView build, capability negative tests, malformed/oversized inputs, navigation/CSP | Not scaffolded; blocked by Phase 1 gate |

## Residual risk

No local design can promise confidentiality or control against a fully compromised same-user Windows session. Administrators, debuggers, injected code, memory dumps, accessibility/desktop capture, and browser vulnerabilities remain relevant. These limits must be explicit in the threat model and product claims; they cannot be converted into `CONFIRMED` controls by passing the primitive probes.

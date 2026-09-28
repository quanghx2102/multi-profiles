# Product Scope

## Purpose

Build a local-first desktop application with the core browser-profile management behavior expected from products such as GoLogin, using Camoufox/Firefox as the first engine. The application is for one person operating profiles on one Windows machine.

This document owns product boundaries. Architecture details belong in [ARCHITECTURE.md](ARCHITECTURE.md), stable normative IDs in [REQUIREMENTS.md](REQUIREMENTS.md), detailed inclusion/defer/reject decisions in [FEATURE_MATRIX.md](FEATURE_MATRIX.md), and claims requiring Camoufox evidence in [AUDIT_REGISTER.md](AUDIT_REGISTER.md).

## Goals

- Create, inspect, start, stop, archive/unarchive, move to/restore from trash, purge, snapshot-recover, back up, transfer, duplicate, import, and export browser profiles with distinct verbs and safeguards.
- Represent each profile as a durable device identity with stable identity inputs across ordinary stop/start cycles.
- Run one separately supervised Camoufox process per running profile.
- Isolate cookies, browser storage, extension state, data directories, and identity seeds between profiles.
- Assign and validate a third-party proxy per profile.
- Protect local data with snapshots, recovery procedures, encrypted portability, and OS-backed secret storage.
- Evolve the browser core through staged migration, semantic fingerprint preflight, canaries, and rollback.
- Add local automation and bulk operations in later phases.
- Preserve an engine-neutral design so a future Chromium adapter can be evaluated without rewriting the domain.

## Initial platform boundary

| Area | Version 1 decision |
|---|---|
| Host OS | Windows-first |
| Deployment | Local desktop only |
| Tenancy | Single user |
| First engine | Camoufox/Firefox, subject to Phase 1 go/no-go audit |
| Cloud sync | Out of scope |
| Teams/workspaces | Out of scope |
| Mobile | Out of scope; Android and iOS would be separate products |
| Sharing | Encrypted import/export, not cloud profile sharing |
| Proxy service | Third-party proxy support; no owned proxy network |

## Product capabilities by maturity

The complete product direction includes profile lifecycle, persistent identities, proxy management, snapshot recovery, backup recovery, extension and cookie operations, core updates, local automation, bulk actions, resource scheduling, and diagnostics. Delivery is staged as specified in [DEVELOPMENT_PHASES.md](DEVELOPMENT_PHASES.md).

## Explicit non-goals and non-claims

- No claim of being undetectable, unlinkable, or guaranteed to bypass anti-bot systems.
- No guarantee against correlation based on IP reputation, account history, user behavior, payment/device graphs, or other server-side data.
- No direct in-place conversion of a profile between browser engines.
- No cloud control plane, distributed lock, remote team collaboration, or mobile runtime in the initial product.
- No bundled proxy marketplace or proxy network.
- No silent fallback to random identity values when an engine cannot apply a required field.
- No promise that every raw fingerprint hash remains byte-identical across a browser-core migration; migrations are evaluated semantically.

## Core user journeys

1. Create a profile and receive a verified, persistent identity.
2. Start and stop it repeatedly without regenerating identity material or losing browser state.
3. Run multiple profiles concurrently without cross-profile state or process interference.
4. Assign a proxy and receive an explicit network-leak validation result.
5. Recover a profile after an application or browser crash without inventing a new identity.
6. Back up, transfer, or duplicate a profile using mode-specific safeguards.
7. Adopt a tested browser-core update with a migration report and automatic rollback path.
8. Diagnose a failure without exposing secrets in logs or support bundles.

## Functional coverage baseline

The agreed product is more than a Camoufox launcher. The following capability map defines intended coverage and prevents accidental claims of full GoLogin parity.

| Capability group | Intended local product scope | Boundary or gate |
|---|---|---|
| Profile catalogue | Create/edit/archive/unarchive/trash/trash-restore/purge; search, sort, filter; folders, tags, notes, status, and configurable presentation | Phase 2; exact lifecycle defaults await `DEC-PROFILE-001` |
| Bulk operations | Start/stop, move, tag, rename, proxy assignment, and other safe batch commands with per-profile outcomes | Phase 4; no all-or-nothing claim across browser processes |
| Identity | Coherent presets, persistent identity inputs, baselines, and preflight | Camoufox feasibility gated by `AUD-001`–`AUD-003`, `AUD-006`, `AUD-007`, `AUD-019`, `AUD-022` |
| Proxy manager | Third-party HTTP/HTTPS/SOCKS inventory, assignment, encrypted credentials, health and leak tests | `AUD-008`; no owned proxy network, traffic billing, or phone proxy device |
| Cookies and storage | Isolated state plus supported import/export/view/delete workflows | Exact formats and fidelity follow `AUD-005`; never edit live browser databases unsafely |
| Recovery | Safe snapshots and snapshot recovery, backup recovery, retention, and crash reconciliation as distinct operations | `AUD-013`; snapshot only after checkpoint |
| Extensions | Per-profile Firefox-compatible extensions | `AUD-011`; no promise of Chrome Web Store or Chrome-only API compatibility |
| Automation | Local authenticated API and Playwright-oriented automation | Phase 4 and `AUD-018`; no promised Puppeteer/CDP parity |
| Cookie Bot | Basic scheduled browsing workflow with per-profile result and resource controls | Phase 4; no claim that generated behavior is human or unlinkable |
| Human typing | Unicode/IME-aware typing behavior through approved automation/UI mechanisms | Phase 4; implementation behavior must be tested |
| Run with Sync | Optional semantic leader/follower prototype using navigation intent and locators, with divergence/2FA/CAPTCHA stops | Phase 4 prototype; raw coordinate mirroring is not the design |
| Core lifecycle | Side-by-side installation, qualification, canary, semantic migration, rollback | `AUD-009`, `AUD-016`, `AUD-020` |
| Portability | Encrypted Backup, Transfer, and Duplicate-as-new | `AUD-010`, `AUD-021`, `AUD-022`, `AUD-026`; same-catalogue collision follows ADR-0013 |

Cloud Browser, cloud synchronization, team/workspace/RBAC, a proxy network, Android execution, and phone-based proxy devices are separate backend/mobile products and are not hidden requirements of this roadmap. Named comparison features such as clone, bookmarks, SDKs, Selenium, templates, start pages, CSV exchange, and default extensions have explicit dispositions in the [Feature Matrix](FEATURE_MATRIX.md).

## Success boundaries

Phase 1 ends with evidence-backed go/no-go criteria, not a working application. Phase 2 may begin only after its blocking audit items in [AUDIT_REGISTER.md](AUDIT_REGISTER.md) meet their required decisions.

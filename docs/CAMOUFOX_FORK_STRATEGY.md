# Camoufox Contribution and Fork Strategy

- Status: Proposed; no fork commitment has been made
- Owner: Upstream maintenance
- Last reviewed: 2026-09-28
- Review trigger: `AUD-023` evidence, required local patch, upstream governance/security change

## Policy direction

Prefer configuration, adapter behavior, and upstream contribution over a permanent private fork. A local patch is justified only when a required invariant cannot be achieved safely through supported configuration/adapter behavior and the patch has a named owner, evidence, regression coverage, rebase plan, and distribution/license review.

This document does not conclude that the project can or should maintain a Camoufox fork.

## Patch levels

| Level | Description | Default disposition |
|---|---|---|
| 0 | No engine change; use qualified upstream artifact | Preferred |
| 1 | Application/adapter validation or fail-closed constraint | Preferred when sufficient |
| 2 | Upstreamable launcher/configuration patch | Contribute upstream first |
| 3 | Upstreamable engine patch carried temporarily | Requires `PATCH_REGISTER.md`, owner, tests, legal review |
| 4 | Long-lived divergent fork | Requires explicit Accepted ADR, staffing/budget and security response plan |

## Local patch requirements

Every patch record identifies upstream base commit, files/symbols, rationale, related audits, security/fingerprint impact, upstream issue/PR, rebase state, regression tests, owner, and status. Patch source and binary provenance must remain reproducible. “Works locally” is not acceptance evidence.

## Rebase and security intake

- Rebase onto each candidate upstream lock in isolation; never rewrite old patch evidence.
- Classify conflicts as mechanical, behavioral, fingerprint-affecting, security-affecting, or no-longer-needed.
- Re-run source-to-probe coverage and every related regression after rebase.
- Monitor Firefox and Camoufox security/release channels selected during `AUD-023`.
- Define supported-core retirement and emergency update behavior before distribution.
- Critical security fixes may shorten normal qualification but never bypass provenance, integrity, minimal regression, or rollback preparation.

## Fork trigger criteria

A fork proposal requires evidence that upstream cannot/will not accept or deliver a critical requirement in the needed window, plus:

- sustainable ownership for Firefox/Camoufox rebase, build, release, security triage, and support;
- measured patch volume/conflict rate and release cadence;
- reproducible build/artifact/signing and license-compliance plan;
- vulnerability intake and emergency release service levels;
- costed contingency for maintainer loss;
- explicit exit criteria and migration path.

The decision is a new ADR and may be `GO`, `CONDITIONAL GO`, `HOLD`, or `NO-GO`. `AUD-023` remains the evidence gate.

## Exit strategy

If upstream stalls or the project cannot maintain required security/compatibility work, freeze new profile creation on unsafe cores as policy permits, retain recoverable user data, publish limits, evaluate a newly audited engine adapter, and avoid in-place reinterpretation of Camoufox identities. Existing profiles are not silently converted to Chromium.


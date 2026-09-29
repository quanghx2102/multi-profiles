# Camoufox beta.31 Fingerprint Surface and Tolerance Catalogue

- Status: Source inventory started; runtime coverage incomplete
- Upstream lock: `v152.0.4-beta.31` / peeled commit `eb5dc3bc5b917d1e6c71d9cacfecdddb55fbfc4a`
- Audits: `AUD-001`, `AUD-003`, `AUD-006`, `AUD-007`, `AUD-019`, `AUD-022`, `AUD-027`–`AUD-030`
- Last reviewed: 2026-09-29

## Evidence boundary

`settings/properties.json` declares configuration keys accepted by the pinned browser build. A declared key is not proof that every consumer/context is patched correctly. The first runtime probe covers only a subset in one main frame and one dedicated worker on `ENV-WIN10-SMOKE-01`.

## Source-declared groups

| Group | Declared keys/shape | Source-linked patch families | Runtime status |
|---|---|---|---|
| Navigator | UA, DNT, app fields, OS CPU, language(s), platform, concurrency, product fields, touch, cookie/GPC/build/online | fingerprint injection, touch spoofing, locale | UA/platform/language/concurrency/touch/webdriver observed in main; four fields observed in worker |
| Screen/window/document | screen/available geometry, offsets, scroll bounds, inner/outer sizes, position, history length, DPR, body client box | fingerprint injection, browser init | width/height/available/inner/outer/DPR/depth observed in main only |
| Network-visible | User-Agent, Accept-Language, Accept-Encoding headers; WebRTC public/local v4/v6 | fingerprint injection, WebRTC IP spoofing | Not captured at a controlled network observer |
| Fonts/noise seeds | font list, font-spacing seed, audio seed, canvas seed | font list/hijacker/system font, audio manager, anti-font fingerprinting | Canvas output hash observed once; seed-to-output mutation untested |
| Region | geolocation lat/lon/accuracy, timezone, locale language/region/script/all | locale/timezone spoofing | Timezone and navigator locale observed once; geolocation/header coherence untested |
| Audio | sample rate, output latency, maximum channels plus audio seed | audio context/fingerprint manager | Not observed |
| WebGL | vendor/renderer, WebGL1/2 extensions, parameters, precision formats, context attributes, block-if-undefined flags | WebGL spoofing | WebGL1 vendor/renderer/extensions observed once; parameters/WebGL2/precision untested |
| Canvas rasterization | seed, AA offset/cap offset | anti-font/canvas-related patches | One deterministic-input relationship not established |
| Speech | voices, undefined policy, fake completion and rate | fingerprint injection/config consumers | Not observed |
| Media | microphone/webcam/speaker counts, enable flag, codec spoofing | media-device/media-codec spoofing | Not observed |
| Volatile/runtime | PDF viewer, battery state/times/level, online, history length, humanize timing/cursor | multiple runtime consumers | Not identity-qualified; mostly unobserved |
| Privileged/behavioral | world isolation, addon new-tab, scope access, theming/animation/memory saver, addons/certificates/debug | config and launcher behavior | Security/capability inputs, not fingerprint acceptance by default |

## Proposed comparison policy

These are comparison classes to test, not accepted tolerances:

| Surface type | Normalization | Candidate rule within same core + approved environment | Current confidence |
|---|---|---|---|
| Identity strings/enums | Unicode normalization only where semantics permit; case remains meaningful unless source says otherwise | Exact equality | Proposed |
| Ordered language/voice preference | Preserve order and duplicates unless API semantics prove set behavior | Exact ordered equality | Proposed |
| WebGL extension support | Deduplicate and sort only if browser ordering is proven non-semantic | Set equality plus explicit missing/extra diff | Proposed; ordering not yet justified |
| Integer identity values/seeds | Canonical unsigned integer | Exact equality | Source supports seed control; runtime mutation pending |
| Screen/viewport geometry | Canonical integer pixels plus environment/DPI generation | Exact configured relations; runtime-derived inner chrome may use evidence-backed relation, not arbitrary ±pixels | Unmeasured |
| DPR/geolocation/audio floats | Canonical finite decimal representation and units | Exact configured value or a measured serialization/quantization interval tied to API/core | Unmeasured; no numeric epsilon approved |
| Canvas/audio rendered output | Hash normalized probe procedure and retain semantic metadata | Exact only for same probe/core/environment after 50-run evidence; otherwise `REVIEW_REQUIRED`/`UNKNOWN` | One canvas sample only |
| WebGL vendor/renderer/parameters | Canonical strings/maps and numeric representation | Exact for a locked environment descriptor; cross-driver/core changes require a qualified rule | One observation only |
| Battery, online, timing, window position, history length | Type/range validation | Informational unless a later audit promotes a field | Proposed |
| Network/WebRTC/header coherence | Canonical endpoint/header/list representation | Exact policy match and no unapproved candidate/address/route | Untested |

No blanket percentage, Levenshtein distance, or aggregate hash tolerance is approved. Missing mandatory fields, contradictions between contexts, unrecognized changes, and changes to immutable identity inputs default to `UNKNOWN` or `FORBIDDEN`, not “close enough”.

## Source-confirmed randomness

The pinned Python launcher assigns random 32-bit non-zero values per launch to:

- `fonts:spacing_seed`;
- `audio:seed`;
- `canvas:seed`.

The source also generates/selects broader fingerprints and font/voice/WebGL data. The three confirmed seed assignments alone are sufficient to reject default launcher generation as a persistent product identity. The product must derive/store explicit versioned inputs, pass them through the adapter, and prove through mutation tests that each intended input reaches every required context.

## Coverage gaps before tolerance acceptance

- same-origin and cross-origin iframe;
- shared worker, service worker, audio/paint worklet where applicable;
- network observer for headers/TLS/HTTP/DNS/WebRTC;
- AudioContext, WebGL2/parameters/precision, font metrics/list, speech voices, media devices/permissions;
- repeated 50-launch stability with fixed explicit inputs;
- one-input-at-a-time mutation sensitivity and unrelated-field stability;
- Windows 11 plus GPU/font/display/DPI/locale matrices;
- clean stop, forced browser exit, sidecar exit, sleep/resume, GPU restart, and profile restore.

Until these exist, `docs/FINGERPRINT_SPEC.md` remains proposed and numeric tolerances remain intentionally unset.

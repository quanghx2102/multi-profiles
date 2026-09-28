# Supported Environment Matrix

- Status: Proposed / Unverified
- Owner: Phase 1 audit
- Last reviewed: 2026-09-28
- Review trigger: Upstream lock selection or new environment evidence

## Rule

No row below is supported merely because it is listed. `UNSELECTED` means the exact build/device has not been pinned. A row becomes `QUALIFIED` only through linked audit evidence and a Phase 1 decision. Marketing and runtime validation must distinguish candidate, tested, qualified, limited, and rejected environments.

## Environment IDs

| Environment ID | Purpose | Windows build | CPU architecture | GPU/driver | Display/DPI | Locale/timezone/fonts | Security tools | Status |
|---|---|---|---|---|---|---|---|---|
| `ENV-WIN-BASE-01` | Clean baseline | `UNSELECTED` Windows 11 build | `x86_64` candidate | Software/basic candidate | Single monitor, 100% candidate | `UNSELECTED` | Defender/SmartScreen state recorded | `UNVERIFIED` |
| `ENV-WIN-INTEL-01` | Integrated GPU | `UNSELECTED` | `x86_64` candidate | Intel family/driver `UNSELECTED` | Single + multi-monitor candidates | `UNSELECTED` | `UNSELECTED` | `UNVERIFIED` |
| `ENV-WIN-AMD-01` | AMD GPU | `UNSELECTED` | `x86_64` candidate | AMD family/driver `UNSELECTED` | Mixed-DPI candidate | `UNSELECTED` | `UNSELECTED` | `UNVERIFIED` |
| `ENV-WIN-NVIDIA-01` | NVIDIA GPU | `UNSELECTED` | `x86_64` candidate | NVIDIA family/driver `UNSELECTED` | Mixed-DPI candidate | `UNSELECTED` | `UNSELECTED` | `UNVERIFIED` |
| `ENV-WIN-LOCALE-01` | Locale/font variance | `UNSELECTED` | `x86_64` candidate | `UNSELECTED` | `UNSELECTED` | Non-default language pack/timezone/font inventory `UNSELECTED` | `UNSELECTED` | `UNVERIFIED` |
| `ENV-WIN-SECURITY-01` | Security-tool compatibility | `UNSELECTED` | `x86_64` candidate | `UNSELECTED` | `UNSELECTED` | `UNSELECTED` | Representative AV product/version `UNSELECTED` | `UNVERIFIED` |

Windows 10, Windows on ARM64, virtual machines, Remote Desktop, headless sessions, and server editions are not implied. They require explicit candidate rows and evidence.

## Dimension matrices

| Dimension | Candidates to select | Required observations | Audit |
|---|---|---|---|
| Windows version/build | Exact supported build set | process/filesystem/IPC, rendering, install/security behavior | `AUD-013`, `AUD-017`, `AUD-031` |
| CPU architecture | x86_64; ARM64 only if selected | artifact availability, launch, performance, process model | `AUD-014`, `AUD-016` |
| GPU/driver | Intel/AMD/NVIDIA exact families and driver versions | WebGL, GPU crashes/restarts, semantic drift | `AUD-007`, `AUD-022`, `AUD-029` |
| Display | single/multi-monitor, 100/125/150/200%, zoom, monitor move | screen/viewport/devicePixelRatio stability and revalidation | `AUD-029`, `AUD-032` |
| Locale/timezone | selected locales, language packs, timezone/DST transitions | navigator/Intl/header/geolocation/proxy coherence | `AUD-028` |
| Fonts | captured inventory per environment | enumeration, fallback, metrics, rendering | `AUD-006`, `AUD-022` |
| Proxy | HTTP, HTTPS, SOCKS candidates with/without auth | DNS/WebRTC/TLS/header routing and failure policy | `AUD-008`, `AUD-027`, `AUD-028` |
| Media | no-device and selected microphone/camera/speaker configurations | enumeration, permission, labels/IDs, hot-plug behavior | `AUD-030` |
| Security tools | Defender, SmartScreen, representative AV selected later | install/launch/update/quarantine/recovery | `AUD-017`, `AUD-031` |

## Evidence record requirements

Every test run records environment ID plus exact OS build, updates, hardware identifiers at the approved redaction level, driver versions, displays/DPI/zoom, locale/language/timezone, font inventory hash, proxy topology, media devices, security tools, power/sleep state, and deviations from the environment definition.


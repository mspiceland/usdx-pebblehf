# Changelog

All notable changes to Pebble HF firmware will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and version numbers follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html), matching
the firmware's own `VERSION` string and this project's existing git tags.

Entries below are transcribed from the per-version tables already published in this project's
[GitHub Release notes](https://github.com/mspiceland/usdx-pebblehf/releases) — this file collects
that same history in the conventional location, so it's discoverable without opening each release.
Pre-1.0.0 prototype history (before the "new versioning scheme" noted at 1.0.0, back when the
project was still called PCKT20) isn't included here.

---

## [Unreleased]

## [1.0.7] — 2026-06-03

### Fixed

- **Critical CW RX image bug.** The 1.0.3 CW sidetone-offset-direction change had flipped the RX
  local oscillator to `freq - cw_offset` while keeping the original LSB I/Q phasing, placing the
  wanted signal on the rejected-image side. Strong signals became weak or inaudible, with a loud
  image appearing about 1.2 kHz above. Reverted RX to `freq + cw_offset` (CW-R/LSB) and TX to
  `-cw_offset`, matching the original, proven configuration. Configurable CW tone is retained.

## [1.0.6] — 2026-04-26

### Fixed

- **Audible "thump" between CW dits/dahs**, caused by RX audio switching on suddenly after each CW
  TX→RX transition. RX audio now fades in briefly instead. No change to the RF envelope or
  sidetone.

## [1.0.5]

### Changed

- **Noise Gate now only applies in VOX mode** — voice PTT uses an optimal low threshold
  automatically instead.

## [1.0.4]

### Fixed

- **Spurious VOX transmit caused by sound card DC bias** on the Tip/DIT pin — the hardware PTT
  check is now skipped when VOX is enabled.

## [1.0.3]

### Fixed

- **CW sidetone offset direction** — changing the sidetone frequency now shifts the received pitch
  in the same direction. (This fix introduced the RX image regression later fixed in 1.0.7.)

## [1.0.2]

### Added

- Configurable CW tone menu option (300–900 Hz).

### Changed

- Encoder startup cleanup.

## [1.0.1] — 2026-03-24

### Changed

- Decoupled the EEPROM version ID from the firmware version string; menu version label updated.

## [1.0.0]

### Changed

- **Forked from upstream uSDX 1.02x** — new versioning scheme adopted; version display now
  includes the compile date.

---

*Versions 1.0.0 through 1.0.5 weren't individually tagged in git — this history is transcribed
from the cumulative table published in the v1.0.6 and v1.0.7-test release notes. Only 1.0.1, 1.0.6,
and 1.0.7 have their own [GitHub Releases](https://github.com/mspiceland/usdx-pebblehf/releases)
with downloadable `.hex` files.*

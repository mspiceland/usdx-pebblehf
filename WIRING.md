# Connector and Wiring Reference

A general reference for every external connector on the Pebble HF board — antenna, power, key/mic,
and audio. For the audio-jack wiring specific to digital modes (FT8, JS8Call, etc.), see
[TROUBLESHOOTING.md](TROUBLESHOOTING.md#q-what-is-the-setup-for-digital-modes); for the separate
6-pin ISP programming header, see [PROGRAMMING.md](PROGRAMMING.md).

![Pebble HF connector layout](top.png)

*Left to right: DC power input, built-in speaker, board (display, tuning knob, MENU/SELECT
buttons), antenna connector, key/mic jack with hand mic attached.*

## Antenna

A coaxial connector for a 50Ω antenna or dummy load (visible on the right in the photo above).
Always have an antenna or dummy load connected before transmitting — the board includes diode
protection against poor SWR and accidental transmission with no antenna, but this is not a
substitute for using one (see [TROUBLESHOOTING.md](TROUBLESHOOTING.md#protection)).

## DC Power

A barrel-style power connector (visible top-left in the photo above). Nominal input is 12–13.8V;
see [TROUBLESHOOTING.md](TROUBLESHOOTING.md#expected-performance) for the efficiency/output-power
figures measured at 13.8V. Reverse-polarity and connector-size specifics aren't documented in this
repository — check [pebblehf.com](https://pebblehf.com) or measure your own board directly before
assuming a value not stated here.

## Key / Mic Jack

A single shared jack handles both an external key/paddle and an external microphone:

- **Plugging anything in disables the built-in microphone** (see [README.md](README.md#operation)).
- **For CW keying**: tip = DIT, ring = DAH by default; the **Keyer Swap** setting reverses this if
  your paddle is wired the other way round, or if you prefer to key left-handed (see
  [OPERATING_MANUAL.md, § 2.7](OPERATING_MANUAL.md#27-keyer-swap)).
- **Straight key mode** (the default, and the correct mode for the built-in key) treats the key
  input as a simple on/off switch (see
  [OPERATING_MANUAL.md, § 2.6](OPERATING_MANUAL.md#26-keyer-mode)).
- **Iambic A/B modes require a paddle to be physically connected** — with nothing plugged in, the
  onboard microphone can falsely trigger the keyer and cause unintended transmissions (see
  [OPERATING_MANUAL.md, § 2.6](OPERATING_MANUAL.md#26-keyer-mode) and
  [README.md](README.md#operation)).

The jack's physical size (e.g. 3.5mm vs. 2.5mm) isn't specified anywhere in this repository —
check [pebblehf.com](https://pebblehf.com) or measure your own board before buying a cable or
adapter.

## Speaker / Headphone Output

A separate audio output jack drives the built-in speaker or a set of headphones. This is the same
jack an external USB sound card's output connects to for digital modes — see
[TROUBLESHOOTING.md](TROUBLESHOOTING.md#connections) for that specific wiring table.

## Internal Signal Reference

For anyone working from the schematic rather than the physical board, the DIT/DAH/PTT and
microphone signal paths are visible in [usdx.png](usdx.png) (bottom-left: key jack, tip/ring/DIT/
DAH labelled; bottom-right: electret mic input) and the overall RX/TX signal flow — including
where the key input and microphone enter the firmware's mode logic — is in
[block.png](block.png) (`DIT DAH PTT` and `electret mic` inputs, right-hand side).

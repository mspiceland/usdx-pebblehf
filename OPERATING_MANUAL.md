# Pebble HF Operating Manual

**Firmware Version 1.0.1**

![Pebble HF](https://pebblehf.com/images/Pebble%20HF.jpg)

## Introduction

Pebble HF is an ultra-affordable, ultra-portable QRP transceiver for the 20-meter band (14.000–14.350 MHz). It supports CW (morse code), SSB voice (USB/LSB), and digital modes such as FT8, JS8, and FT4. Based on the open source uSDX software-defined radio design, Pebble HF packs a full-featured SDR transceiver into a tiny, power-efficient package.

**Key specs at a glance:**

- **Band:** 20 meters (14.000–14.350 MHz)
- **Modes:** USB, LSB, CW
- **Output power:** ~5W PEP on 7–14V, ~1W on USB-C (5V)
- **Weight:** Less than 4.7 oz (132g)
- **Power consumption:** ~80mA RX, 500–600mA TX @ 12V
- **Built-in:** CW straight key, microphone, 1602 LCD display

For more information, visit [pebblehf.com](https://pebblehf.com).

---

## Controls

Pebble HF has three controls:

- **Tuning Knob (Rotary Encoder)** — The main knob on the right side. Turn to tune frequency. Press and turn to adjust volume. Press to change tuning step size.
- **MENU Button (Left)** — Short press enters the menu system. Used to navigate and select menu parameters.
- **SELECT Button (Right)** — Used to exit menus, cycle filter bandwidth (double-click), and toggle VFO/RIT (long press).

---

## Basic Operation

### Tuning

Turn the rotary encoder to change frequency. The radio is locked to the 20-meter band (14.000–14.350 MHz).

### Tuning Step Size

Short press the encoder to increase the tuning step size. Long press the encoder to decrease it. Available step sizes: 10M, 1M, 0.5M, 100k, 10k, 1k, 0.5k, 100, 10, 1 Hz.

### Volume

Press and hold the encoder while turning to adjust volume (0–16). Turning the volume below 0 will power off the radio.

### Filter Bandwidth

Double-click the SELECT (right) button to cycle through receiver filter bandwidths. In SSB mode: Full, 3000, 2400, 1800 Hz. In CW mode: 500, 200, 100, 50 Hz. The filter also controls SSB transmit bandwidth.

### VFO A/B and RIT

Long press the SELECT (right) button to toggle RIT (Receive Incremental Tuning). A second long press swaps between VFO A and VFO B.

### Power Off

Press and hold the encoder while turning the volume below 0. The radio will display "Power-off 73 :-)" and enter a low-power sleep state.

### Factory Reset

Hold the encoder button down during power-up to reset all settings to factory defaults.

---

## Menu System

Press the MENU (left) button to enter the menu. Turn the encoder to scroll through menu items. Press the MENU button again to select a parameter for editing, then turn the encoder to change the value. Press the SELECT (right) button to save and go back, or press it again to exit the menu entirely.

**Quick menu access:** Hold the MENU (left) button while turning the encoder to quickly navigate to a parameter. Release the button and turn the encoder to immediately change the value.

---

## Menu Reference — Summary

| # | Menu Item | Values | Description |
|---|-----------|--------|-------------|
| 1.1 | Volume | -1 (off) to 16 | Audio output level; below 0 powers off the radio |
| 1.2 | Mode | LSB, USB, CW | Modulation mode |
| 1.3 | Filter BW | Full, 3000, 2400, 1800, 500, 200, 100, 50 Hz | Receiver/transmitter audio passband filter |
| 1.5 | Tune Rate | 10M, 1M, 0.5M, 100k, 10k, 1k, 0.5k, 100, 10, 1 | Tuning step size per encoder click |
| 1.6 | VFO Mode | A, B | Select VFO A or VFO B |
| 1.7 | RIT | OFF, ON | Receive Incremental Tuning |
| 1.8 | AGC | OFF, ON | Automatic Gain Control |
| 1.9 | NR | 0–8 | Noise reduction level |
| 1.10 | ATT | 0, -13, -20, -33, -40, -53, -60, -73 dB | Analog front-end attenuator |
| 1.11 | ATT2 | 0–16 (6 dB steps) | Digital attenuator in CIC stage |
| 1.12 | S-meter | OFF, dBm, S, S-bar, wpm | Signal meter display format |
| 2.1 | CW Decoder | OFF, ON | On-screen CW decoder |
| 2.2 | CW Tone | 300–900 Hz | CW sidetone frequency |
| 2.3 | CW Side Vol | -1 (mute) to 16 | CW sidetone volume (independent of main volume) |
| 2.4 | Semi QSK | OFF, ON | Mutes RX briefly after keying for semi break-in |
| 2.5 | Keyer Speed | 1–60 WPM | CW keyer speed in words per minute |
| 2.6 | Keyer Mode | Iambic A, Iambic B, Straight | Type of CW keyer |
| 2.7 | Keyer Swap | OFF, ON | Swap DIT/DAH paddle inputs |
| 2.8 | Practice | OFF, ON | Disables transmit for CW practice |
| 3.1 | VOX | OFF, ON | Voice-operated transmit |
| 3.2 | Noise Gate | 0–255 | Audio threshold for VOX and SSB TX |
| 3.3 | TX Drive | 0–8 | Transmit audio gain (6 dB steps) |
| 8.1 | PA Bias min | 0–255 | PA PWM level for 0% RF output |
| 8.2 | PA Bias max | 0–255 | PA PWM level for 100% RF output |
| 8.3 | Ref freq | 14000000–28000000 | SI5351 crystal frequency calibration |
| 8.4 | IQ Phase | 0–180° | RX I/Q phase correction |
| 10.1 | Version | (read only) | Firmware version and compile date |

---

## Menu Reference — Detailed

### 1.1 Volume

**Values:** -1 (off) through 16

Controls the main audio output level of the receiver. Setting 0 is very quiet; 16 is maximum volume. Turning the volume below 0 (to -1) will power off the radio into a low-power sleep state. Volume can be adjusted at any time by pressing and holding the encoder knob while turning it — you do not need to enter the menu.

---

### 1.2 Mode

**Values:** LSB, USB, CW

Selects the modulation mode.

- **LSB** — Lower Sideband, used for voice on bands below 10 MHz (not typical for 20m, but available).
- **USB** — Upper Sideband, the standard voice mode for the 20-meter band.
- **CW** — Continuous Wave (morse code). When CW mode is selected, the filter automatically narrows and the tuning step size adjusts for CW operation.

---

### 1.3 Filter BW

**Values:** Full, 3000, 2400, 1800, 500, 200, 100, 50 Hz

Sets the DSP audio passband filter width for both receive and transmit.

- **Full** — No filtering, full audio bandwidth.
- **3000 Hz** — Wide SSB filter (300–3000 Hz passband).
- **2400 Hz** — Standard SSB filter (300–2400 Hz passband).
- **1800 Hz** — Narrow SSB filter (300–1800 Hz passband).
- **500 Hz** — Wide CW filter, good for general CW operation.
- **200 Hz** — Medium CW filter, helps isolate a single signal.
- **100 Hz** — Narrow CW filter for crowded band conditions.
- **50 Hz** — Ultra-narrow CW filter for extreme selectivity.

**Quick access:** Double-click the SELECT (right) button to cycle through filters without entering the menu. In SSB mode, it cycles through Full/3000/2400/1800. In CW mode, it cycles through 500/200/100/50.

---

### 1.5 Tune Rate

**Values:** 10M, 1M, 0.5M, 100k, 10k, 1k, 0.5k, 100, 10, 1

Sets how much the frequency changes per click of the encoder. For quick tuning across the band, use 1k or 10k. For fine-tuning a CW signal, use 100, 10, or 1 Hz.

**Quick access:** Short press the encoder to increase the step size. Long press the encoder to decrease it.

---

### 1.6 VFO Mode

**Values:** A, B

Selects which VFO (Variable Frequency Oscillator) memory is active. Each VFO stores its own frequency and mode. This allows you to quickly switch between two frequencies.

**Quick access:** Long press the SELECT (right) button to toggle RIT, then long press again to swap VFOs.

---

### 1.7 RIT

**Values:** OFF, ON

Receive Incremental Tuning allows you to offset the receive frequency from the transmit frequency. When RIT is enabled, the tuning step automatically changes to 10 Hz for fine adjustment. This is useful for tuning in a station that is slightly off your transmit frequency without moving your transmit frequency.

**Quick access:** Long press the SELECT (right) button to toggle RIT on or off.

---

### 1.8 AGC

**Values:** OFF, ON

Automatic Gain Control automatically adjusts the receiver volume to keep signals at a consistent level — boosting weak signals and reducing strong ones. AGC is disabled by default.

- **OFF** — Manual volume control only. Quieter but requires more manual adjustment.
- **ON** — Automatic level control. Good for SSB but can be distracting during CW.

---

### 1.9 NR

**Values:** 0–8

Noise Reduction applies a low-pass smoothing filter to reduce background noise. Higher values apply more aggressive noise reduction. A setting of 0 disables noise reduction. Start with low values (1–3) and increase as needed. NR is reset to 0 when switching to CW mode.

---

### 1.10 ATT

**Values:** 0dB, -13dB, -20dB, -33dB, -40dB, -53dB, -60dB, -73dB

Analog front-end attenuator. Reduces the signal level entering the receiver. Use this when strong signals are overloading the receiver or to reduce atmospheric noise. On the 20-meter band, a small amount of attenuation (e.g., -13dB) can improve reception by lowering the noise floor relative to signals.

---

### 1.11 ATT2

**Values:** 0–16 (each step is approximately 6 dB)

Digital attenuator applied in the CIC (Cascaded Integrator-Comb) filter stage of the DSP receiver. Provides additional signal level control in the digital domain. Use in combination with ATT for fine-tuning the receiver's dynamic range.

---

### 1.12 S-meter

**Values:** OFF, dBm, S, S-bar, wpm

Controls what is displayed on the signal meter area of the LCD.

- **OFF** — No signal meter displayed.
- **dBm** — Shows received signal strength in dBm.
- **S** — Shows signal strength as an S-unit value (S1–S9, S9+).
- **S-bar** — Shows signal strength as a visual bar graph.
- **wpm** — Shows decoded CW speed in words per minute (useful with CW Decoder enabled).

---

### 2.1 CW Decoder

**Values:** OFF, ON

Enables or disables the built-in CW decoder. When enabled, received CW signals are decoded and the characters are displayed on the LCD screen. Works best with a narrow CW filter (200 Hz or less) and a clean signal.

---

### 2.2 CW Tone

**Values:** 300–900 Hz

Sets the CW sidetone frequency in Hertz. This is the pitch of the tone you hear when keying CW, and it also sets the CW offset used for transmit. Choose a pitch that is comfortable for your ear. Common values are 500–700 Hz. Default is 600 Hz.

---

### 2.3 CW Side Vol

**Values:** -1 (mute) through 16

Sets the CW sidetone volume independently from the main receiver volume. This allows you to have a comfortable sidetone level while keeping the receiver volume at a different level. A value of -1 mutes the sidetone entirely. Default is 12.

---

### 2.4 Semi QSK

**Values:** OFF, ON

Semi QSK (semi break-in) mutes the receiver for a short period after each CW element (dit or dah) and during word spaces. This prevents you from hearing your own transmitted signal between elements while still allowing you to hear the band during longer pauses. Useful for comfortable CW ragchewing.

---

### 2.5 Keyer Speed

**Values:** 1–60 WPM

Sets the speed of the built-in CW keyer in words per minute (Paris standard). This setting applies to Iambic A and Iambic B modes. In Straight key mode, speed is determined by your manual keying. Default is 15 WPM.

---

### 2.6 Keyer Mode

**Values:** Iambic A, Iambic B, Straight

Selects the type of CW keyer.

- **Iambic A** — Iambic keyer mode A. Alternating dits and dahs are produced when both paddles are squeezed. Releasing the paddles stops keying immediately.
- **Iambic B** — Iambic keyer mode B. Similar to Iambic A, but an additional dit or dah is inserted after releasing the paddles if the opposite paddle was held.
- **Straight** — Straight key mode. The key input is used as a simple on/off switch. This is the default and is the correct mode for the built-in key button.

> **Important:** If you select Iambic A or Iambic B mode, you **must** have a paddle connected to the key/mic jack. If nothing is plugged in, the built-in microphone can falsely trigger the keyer and cause unintended transmissions.

---

### 2.7 Keyer Swap

**Values:** OFF, ON

Swaps the DIT and DAH paddle inputs. Use this if your paddle is wired in reverse, or if you prefer to key left-handed. OFF is normal (tip = DIT, ring = DAH). ON swaps them.

---

### 2.8 Practice

**Values:** OFF, ON

When enabled, the transmitter is disabled for CW practice purposes. You will hear the sidetone in your speaker but no RF is transmitted. This is useful for practicing your keying without going on the air.

---

### 3.1 VOX

**Values:** OFF, ON

Voice-Operated Transmit automatically switches the radio to transmit when audio is detected from the microphone. The sensitivity is controlled by the Noise Gate setting (3.2). VOX is also used for digital mode operation — the audio from your computer triggers the transmitter.

When VOX is enabled, a "V" appears on the right side of the display instead of "R" (receive).

> **Note:** VOX is always disabled on power-up for safety, regardless of the saved setting.

---

### 3.2 Noise Gate

**Values:** 0–255

Sets the audio threshold level for VOX activation and SSB transmit. Audio below this level will not trigger transmission. Higher values require louder audio to trigger transmit. Lower values make VOX more sensitive.

- For VOX voice operation, start around 40–50 and adjust based on your environment.
- For digital modes, adjust so that your computer's audio reliably triggers transmit without false triggers from noise.

Default is 50.

---

### 3.3 TX Drive

**Values:** 0–8

Controls the transmit audio gain in approximately 6 dB steps. Higher values increase the modulation depth and transmit power.

- **0** — Minimum drive.
- **8** — Maximum / constant amplitude (useful for CW or digital modes).
- **2–4** — Typical range for SSB voice.

Adjust while monitoring your signal or based on signal reports. Default is 4 (set during initialization).

---

### 8.1 PA Bias min

**Values:** 0 to (PA Bias max - 1)

Sets the PWM (Pulse Width Modulation) level that represents 0% RF output from the power amplifier. This is a calibration parameter. **Do not change this unless you understand PA biasing.** Incorrect values can damage the PA transistors.

---

### 8.2 PA Bias max

**Values:** (PA Bias min) to 255

Sets the PWM level that represents 100% RF output from the power amplifier. This is a calibration parameter. **Do not change this unless you understand PA biasing.** Default is 128.

---

### 8.3 Ref freq

**Values:** 14000000–28000000

The actual crystal oscillator frequency of the SI5351 PLL. Used for frequency calibration. The Pebble HF uses a 26 MHz TCXO, so this should be close to 26000000. If your displayed frequency does not match a known reference signal, adjust this value until it does.

---

### 8.4 IQ Phase

**Values:** 0–180°

Adjusts the I/Q phase offset for the SDR receiver in degrees. This calibration parameter affects sideband suppression. The optimal value cancels out the unwanted sideband. Adjust while listening to a signal and minimize the opposite sideband bleed-through.

---

### 10.1 Version

**Read only**

Displays the firmware version number and compile date. Useful for verifying which firmware is installed on your radio.

---

## Button Quick Reference

| Action | How | Context |
|--------|-----|---------|
| Tune frequency | Turn encoder | Main screen |
| Adjust volume | Press + turn encoder | Any time |
| Change tuning step (up) | Short press encoder | Main screen |
| Change tuning step (down) | Long press encoder | Main screen |
| Cycle filter bandwidth | Double-click SELECT (right) | Main screen |
| Toggle RIT / Swap VFO | Long press SELECT (right) | Main screen |
| Enter menu | Short press MENU (left) | Main screen |
| Quick menu access | Hold MENU (left) + turn encoder | Main screen |
| Select menu item | Short press MENU (left) | In menu |
| Save and exit to menu | Short press SELECT (right) | Editing value |
| Exit menu | Short press SELECT (right) | In menu |
| Power off | Press + turn encoder below 0 | Any time |
| Factory reset | Hold encoder during power-up | Power-up |

---

## Startup Self-Test

On power-up, the radio performs a hardware self-test (diagnostics). It checks supply voltages, bias levels, I2C communications, and processing performance. If any check fails, an error message is displayed. Normal startup shows the splash screen "PEBBLE" followed by the version number, then proceeds to normal operation.

---

## Credits

- **Pebble HF Project:** Mike N4FFF — Firmware modifications and project maintenance
- **Original uSDX Firmware:** Guido PE1NNZ
- **Hardware Design:** Barbaros Asuroglu, WB2CBA

This is an open source project. For more information, visit [pebblehf.com](https://pebblehf.com).

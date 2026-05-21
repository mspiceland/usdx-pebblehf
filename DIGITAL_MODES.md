# Pebble HF — Digital Modes Guide

This guide covers operating Pebble HF with FT8, FT4, JS8Call, and WSPR on the 20-meter band.

---

## How Digital Modes Work on Pebble HF

Pebble HF uses **VOX (Voice-Operated Transmit)** for PTT. When your software sends audio, the radio switches to transmit automatically — no CAT interface, no PTT cable, and no extra hardware required. This makes Pebble HF an excellent choice for portable digital operation from a phone, tablet, or laptop.

The radio's built-in USB audio codec appears on your host device as a standard **USB Audio Device**. No driver installation is required on any supported operating system (Windows, macOS, Linux, Android, iOS).

---

## Equipment and Connections

- **Computer, phone, or tablet** — any device with a USB port
- **USB cable** — the same cable used to power the radio
- **Android/iOS** — a USB OTG adapter is required (USB-A to USB-C, or Lightning Camera Connection Kit)
- **Antenna** — a resonant 20m antenna connected to the SMA connector

A separate USB power supply is **not** needed when connected to a computer — the radio is powered from the same USB connection that carries audio.

> **Power note:** On USB-C (5V), Pebble HF produces approximately 1W of RF output. On a 7–14V battery, output rises to approximately 5W. For SOTA and POTA activations requiring more power, connect a separate battery to the power input and use USB for audio only.

---

## Radio Settings for Digital Modes

Before launching your digital mode software, configure the radio as follows:

| Setting | Value | Menu |
|---------|-------|------|
| Mode | USB | 1.2 |
| Filter BW | Full or 3000 Hz | 1.3 |
| VOX | ON | 3.1 |
| Noise Gate | 40–80 | 3.2 |
| TX Drive | 4–6 | 3.3 |
| AGC | OFF | 1.8 |
| NR | 0 | 1.9 |

**VOX** must be enabled for the radio to transmit. It is reset to OFF on every power-up — remember to turn it on each session.

**Noise Gate** controls how much audio is needed to trigger transmit. Start at 50 and adjust: higher values require louder audio; lower values make VOX more sensitive. A value that is too low will cause false triggers from background noise.

**TX Drive** controls transmit power. Values of 4–6 are appropriate for digital modes. During an FT8 exchange the radio typically alternates between 15-second TX and RX slots, so sustained periods at high drive are possible — avoid running higher than needed, as the PA generates heat.

**Filter BW** should be wide (Full or 3000 Hz) so the full audio spectrum from the software reaches the transmitter without being cut off. Narrow CW filters will distort or block the digital audio.

**AGC and NR** should both be off — digital mode decoders work best on the unprocessed received audio.

---

## Frequencies

Tune the radio VFO to the standard dial frequency for each mode. Since Pebble HF does not have CAT control, you set the frequency manually on the radio before launching your software.

| Mode | Dial Frequency (USB) | Audio range | Notes |
|------|---------------------|-------------|-------|
| FT8 | 14.074 MHz | 1000–3000 Hz | Set WSJT-X dial to 14.074.000 |
| FT4 | 14.080 MHz | 1000–3000 Hz | Set WSJT-X dial to 14.080.000 |
| JS8Call | 14.078 MHz | 500–2500 Hz | Standard JS8 sub-band |
| WSPR | 14.0956 MHz | 1400–1600 Hz | See note below |

> **WSPR note:** WSPR uses 2-minute TX windows and requires your clock to be accurate to within a few seconds of UTC. Use low TX Drive (1–2) — WSPR signals are narrow and stations will decode you at very low power. Start with a long listening session before transmitting.

---

## Computer Time Synchronisation

FT8 and FT4 transmissions are tightly slotted: FT8 uses 15-second slots, FT4 uses 7.5-second slots. **Your computer clock must be accurate to within approximately 1 second of UTC.** If your clock is out of sync, your transmissions will not be decoded.

Enable automatic time synchronisation on your computer (NTP/internet time) before operating. On Windows: Settings → Time → Sync now. On macOS: System Preferences → Date & Time → Set automatically.

---

## WSJT-X (Windows, macOS, Linux)

WSJT-X is the standard software for FT8 and FT4.

1. Connect Pebble HF to your computer via USB.
2. Open WSJT-X and go to **File → Settings**.
3. **Audio tab:**
   - Input: **USB Audio Device** (Pebble HF)
   - Output: **USB Audio Device** (Pebble HF)
4. **Radio tab:**
   - Rig: **None**
   - PTT is handled by the radio's own VOX — no PTT setting is needed here.
5. Click **OK**.
6. Set the radio's VFO to **14.074.000 MHz** for FT8, or **14.080.000 MHz** for FT4.
7. On the radio, enable VOX (menu 3.1).
8. In WSJT-X, select **FT8** (or **FT4**) from the Mode menu.

The waterfall should show received signals immediately. FT8 decodes appear at the start of each 15-second slot. When WSJT-X transmits, the audio it sends will trigger VOX and the radio will switch to TX automatically.

> **Tip:** Adjust your computer's audio output volume so that the radio's TX LED lights consistently when WSJT-X is transmitting, but does not stay on when WSJT-X is receiving. If the TX LED stays on during RX, lower the output volume or increase the Noise Gate setting on the radio.

---

## JS8Call (Windows, macOS, Linux)

JS8Call is a keyboard-to-keyboard digital mode based on FT8 with longer, conversational messages.

1. Connect Pebble HF to your computer via USB.
2. Open JS8Call and go to **File → Settings → Audio**.
   - Input: **USB Audio Device** (Pebble HF)
   - Output: **USB Audio Device** (Pebble HF)
3. Under **Radio**, set Rig to **None**. PTT is handled by the radio's own VOX.
4. Set the radio VFO to **14.078 MHz** and enable VOX (menu 3.1).
5. In JS8Call, select **Normal** speed (default) for standard operation.

JS8Call transmissions are 15 seconds per frame at Normal speed. The same VOX behaviour applies as for WSJT-X.

---

## TrailDigi (Android)

[TrailDigi](https://codeberg.org/traildigi/traildigi) is a SOTA/POTA-optimised Android FT8/FT4 app, purpose-built for portable HF operation with radios like Pebble HF.

1. Connect Pebble HF to your Android phone or tablet using a USB OTG adapter.
2. Open TrailDigi and go to **Settings → Audio**.
3. Select **USB Audio Device** (Pebble HF) as both audio input and output.
4. Enable VOX on the radio (menu 3.1).
5. Set the radio VFO to the desired frequency (14.074 MHz for FT8).

TrailDigi handles timing, decoding, and logging automatically. No separate PTT or CAT connection is required.

---

## FT8TW (Android)

[FT8TW](https://github.com/N0BOT/FT8TW) is the upstream Android app from which TrailDigi is derived. Configuration is identical to TrailDigi above.

---

## IFTX (iOS)

1. Connect Pebble HF to your iPhone or iPad using a USB Lightning/USB-C to USB-A adapter (Camera Connection Kit or equivalent).
2. Open IFTX and select **USB Audio Device** (Pebble HF) as the audio input and output.
3. Enable VOX on the radio (menu 3.1).
4. Set the radio VFO to the desired frequency.

IFTX: https://apps.apple.com/us/app/iftx/id6446093115

---

## Troubleshooting

**Radio does not transmit when software sends audio:**
- Check that VOX is enabled (menu 3.1 → ON). VOX resets to OFF on every power-up.
- Check that the audio output of your computer/phone is turned up.
- Try lowering the Noise Gate (menu 3.2) — it may be set too high.
- Confirm the correct USB Audio Device is selected in your software.

**Radio transmits continuously and does not return to receive:**
- The Noise Gate is too low — background noise is triggering VOX. Increase it (menu 3.2).
- Lower the computer audio output level.

**Transmissions are not decoded by other stations:**
- Check your computer clock is synchronised to within 1 second of UTC.
- Confirm the radio is in USB mode (menu 1.2).
- Check the Filter BW is set to Full or 3000 Hz (menu 1.3) — narrow filters distort the digital audio.
- Reduce TX Drive (menu 3.3) if you are overdriving the PA.

**Received signals look weak or noisy on the waterfall:**
- Confirm AGC is off (menu 1.8) and NR is 0 (menu 1.9).
- Try increasing the computer audio input (microphone) level.
- Check your antenna connection.

**Audio device not detected on Android:**
- Try a different USB OTG adapter or cable — Android USB audio support varies by device.
- Pebble HF is USB class-compliant and does not require a driver.

---

## Further Reading

- [README.md](README.md) — project overview and features
- [OPERATING_MANUAL.md](OPERATING_MANUAL.md) — full radio operating guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — hardware and firmware troubleshooting

# Pebble HF: An Ultra-Affordable HF Radio for Everyone


Pebble HF is an experimental QRP radio designed to get more people into HF radio with a General class amateur radio license and outdoor radio operation. It is an ultra-inexpensive 20-meter single-band transceiver built for accessibility and simplicity.

![Pebble HF](https://pebblehf.com/images/Pebble%20HF.jpg)
**For more information, visit [pebblehf.com](https://pebblehf.com)**

## Credits

This project is built on the shoulders of giants from the open source [uSDX project](https://github.com/threeme3/usdx):

- **Hardware Design**: [Barbaros Asuroglu, WB2CBA](https://github.com/WB2CBA/PEBBLE-20m-HF-TRANSCEIVER)
- **Pebble HF Firmware & Project**: Mike N4FFF
- **Original uSDX Firmware**: Guido PE1NNZ (pe1nnz@qsl.net)

The Pebble HF firmware is a modified version of the uSDX firmware, optimized for the Pebble HF hardware platform.

## About the Radio

Amateur radio is a fantastic hobby for learning, connection, and adventure — and small, portable radios are perfect for getting on HF, connecting with people around the world, and outdoor radio adventures like POTA and SOTA.

Pebble HF was purpose-designed to be ultra-affordable and easy to build. It is a single-band 20-meter QRP transceiver that supports CW (morse code), SSB voice (USB/LSB), and digital modes such as FT8, JS8, and FT4. The hardware was designed from the ground up by Barb WB2CBA with cost and kit-friendliness in mind — nearly all parts are pre-soldered surface mount, leaving only 14 easy through-hole parts for the builder. Most people complete the build in under an hour.

Despite its simplicity, Pebble HF is a capable software-defined radio. Both the transmitter and receiver run on a single ATMEGA328P microcontroller. The transmitter uses an efficient Class-E power amplifier driven entirely by digital signal processing, and the receiver implements DSP filtering, AGC, noise reduction, and more — all in software. This keeps the parts count low, the design simple, and the radio highly power-efficient.

- **~5W output** on 7–14V battery power, **~1W on USB-C** (5V) — get on the air even without a dedicated battery
- **Weighs less than 4.7 oz (132g)** — perfect for portable operation
- **Built-in CW key and microphone** — nothing extra needed to start making contacts
- **Open source hardware and firmware** — hack it, improve it, share it

Our mission is simple: get more people into HF ham radio and outdoor radio!

## List of Features

- **Simple, fun and versatile QRP SSB HF transceiver** with embedded **DSP and SDR functions**
- **20-meter single-band** operation (14.000 - 14.350 MHz)
- **EER Class-E** driven SSB transmit-stage
- Approximately **5W PEP SSB output** from 13.8V supply
- **Mode support: USB, LSB, CW**
- **DSP filters: Full, 3000, 2400, 1800, 500, 200, 100, 50 Hz passband**
- **DSP features: Automatic Gain Control (AGC), Noise-reduction (NR), Voice-triggered Xmit (VOX), RX Attenuators (ATT), TX noise gate, TX drive control, Volume control, dBm/S-meter**
- SSB opposite side-band/carrier suppression **Transmit: better than -45dBc, IMD3 (two-tone) -33dBc, Receive: better than -50dBc**
- **Open source** firmware, built with Arduino IDE; allows experimentation, new features can be added, contributions can be shared via Github, software-complexity: 2000 lines of code
- Software-based **VOX** that can be used as **fast Full Break-In** (QSK and semi-QSK operation) or assist in RX/TX switching for operating digital modes (no CAT or PTT interface required), external PTT output/PA control with **TX-delay**
- **Lightweight and low-cost transceiver design**: because of the EER-transmitter class-E stage it is **highly power-efficient** (no bulky heatsinks required), and has a **simple design** (no complex balanced linear power amplifier required)
- **Fully digital and software-based SSB transmit-stage**: samples microphone-input and reconstruct a SSB-signal by controlling the phase of the SI5351 PLL (through tiny frequency changes over 800kbits/s I2C) and the amplitude of the PA (through PWM of the PA key-shaping circuit)
- **Fully digital and software-based SDR receiver-stages (optionally)**: samples I/Q (complex) signal from Quadrature Sampling Detector digital mixer, and performs a 90-degree phase-shift mathematically in software (Hilbert-transform) and cancels out one side-band by adding them
- **CW decoder**, Straight/Iambic-A/B **keyer**
- **VFO A/B + RIT**, and corresponding relay band-filter switching via I2C
- Probably the most **cost effective** and **easy** to build standalone SDR/SSB transceiver that you can find. Very much **simplified** circuit and **versatile** in use.


## Hardware

The Pebble HF hardware is designed by [Barbaros Asuroglu, WB2CBA](https://github.com/WB2CBA/PEBBLE-20m-HF-TRANSCEIVER). For hardware schematics, bill of materials, and build information, see [Barb's hardware repository on GitHub](https://github.com/WB2CBA/PEBBLE-20m-HF-TRANSCEIVER). For general project information, visit [pebblehf.com](https://pebblehf.com).

This project is based on the original uSDX design. For other uSDX hardware variants, see the [uSDX Forum].

## Operation

Pebble HF has three controls: a **tuning knob** (rotary encoder), a **MENU button** (left), and a **SELECT button** (right).

- **Tune:** Turn the encoder to change frequency (locked to 14.000–14.350 MHz).
- **Volume:** Press and hold the encoder while turning. Turning below 0 powers off the radio.
- **Step size:** Short press encoder to increase, long press to decrease.
- **Filter:** Double-click SELECT (right) to cycle through DSP filter bandwidths.
- **VFO/RIT:** Long press SELECT (right) to toggle RIT, then again to swap VFO A/B.
- **Menu:** Short press MENU (left) to enter. Turn encoder to browse, press MENU to edit a value, press SELECT to save/exit.
- **Factory reset:** Hold encoder button during power-up.

Pebble HF has a built-in straight key and microphone. An external key or mic can be connected to the key/mic jack. Plugging something into the jack disables the built-in mic. **Always have a paddle plugged in when using Iambic A/B keyer mode** — otherwise the onboard mic may falsely trigger the keyer.

> **For the full operating manual including all menu options, see [OPERATING_MANUAL.md](OPERATING_MANUAL.md).**

## Firmware

The radio comes pre-programmed. At this stage, custom programming is not encouraged, but here is what is being used during development:

### Programming Hardware

- **AVR Programmer**: [Pocket AVR Programmer](https://www.sparkfun.com/pocket-avr-programmer.html)
- **Pogo Pins** (to program without soldering a header): [Spring Loaded Pogo Pins](https://www.amazon.com/dp/B075Q25BK3)

### Programming Commands

Program the firmware:
```
avrdude -c usbtiny -p m328p -U flash:w:usdx.ino.hex
```

Set the fuses:
```
avrdude -c usbtiny -p m328p \
  -U lfuse:w:0xFF:m \
  -U hfuse:w:0xD6:m \
  -U efuse:w:0xFD:m
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Credits

**Pebble HF Project**: Mike N4FFF - Firmware modifications and project maintenance

**Original uSDX Project**: The uSDX was originally announced in the [QRPLabs Forum] as a SSB modification for a [QCX]. The [uSDX] transmitter and receiver stage both running on a ATMEGA328P, including its multiband front-end and direct PA biasing/envelope-generation technique; its concept, circuit, code are a design by _Guido (PE1NNZ)_; the software-based SSB transmit stage is a derivate of earlier experiments with a [digital SSB generation technique] on a Raspberry Pi.

**Hardware Design**: [Barbaros Asuroglu (WB2CBA)](https://github.com/WB2CBA/PEBBLE-20m-HF-TRANSCEIVER) - Pebble HF hardware design

Many thanks to all contributors to the open source uSDX project, without whose work the Pebble HF would not be possible.

<!-- Link references -->
[uSDX]: https://github.com/threeme3/usdx
[uSDX Forum]: https://groups.io/g/ucx
[QRPLabs Forum]: https://groups.io/g/QRPLabs/topic/29572792
[QCX]: https://qrp-labs.com/qcx.html
[digital SSB generation technique]: http://pe1nnz.nl.eu.org/2013/05/direct-ssb-generation-on-pll.html


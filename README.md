# Pebble HF: An Ultra-Affordable HF Radio for Everyone


Pebble HF is an experimental QRP radio designed to get more people into HF radio with a General class amateur radio license and outdoor radio operation. It is an ultra-inexpensive 20-meter single-band transceiver built for accessibility and simplicity.

![Pebble HF](https://pebblehf.com/images/Pebble%20HF.jpg)
**For more information, visit [pebblehf.com](https://pebblehf.com)**

## Credits

This project is built on the shoulders of giants from the open source [uSDX project](https://github.com/threeme3/usdx):

- **Hardware Design**: Barbaros Asuroglu, WB2CBA
- **Pebble HF Firmware & Project**: Mike N4FFF
- **Original uSDX Firmware**: Guido PE1NNZ (pe1nnz@qsl.net)

The Pebble HF firmware is a modified version of the uSDX firmware, optimized for the Pebble HF hardware platform.

## About the Radio

Pebble HF is a simple and experimental (Class-E driven) SSB and CW SDR transceiver based on the uSDX design. It operates on the 20-meter band (14 MHz) and can be used for QRP SSB/CW contacts or digital modes such as FT8, JS8, and FT4.

The SSB transmit-stage is implemented entirely in digital and software-based manner: at the heart the ATMEGA328P is sampling the input-audio and reconstructing a SSB-signal by controlling the SI5351 PLL phase (through tiny frequency changes over 800kbit/s I2C) and controlling the PA Power (through PWM on the key-shaping circuit). This results in a highly power-efficient class-E driven SSB-signal that keeps the transceiver simple, tiny, cool, power-efficient and low-cost.

For the receiver, most parts are implemented in software: the ATMEGA328P implements a 90 degree phase shift circuit, the (CW/SSB) filter circuit and the audio amplifier circuit (class-D amplifier). This simplifies the circuit significantly and provides adjustable IF DSP filters for CW and SSB, AGC, noise-reduction, and multiple attenuator options.

## List of Features

- **Simple, fun and versatile QRP SSB HF transceiver** with embedded **DSP and SDR functions**
- **20-meter single-band** operation (14.000 - 14.350 MHz)
- **EER Class-E** driven SSB transmit-stage
- Approximately **5W PEP SSB output** from 13.8V supply
- **Mode support: USB, LSB, CW**
- **DSP filters: 4000, 2500, 1700, 500, 200, 100, 50 Hz passband**
- **DSP features: Automatic Gain Control (AGC), Noise-reduction (NR), Voice-triggered Xmit (VOX), RX Attenuators (ATT), TX noise gate, TX drive control, Volume control, dBm/S-meter**
- SSB opposite side-band/carrier suppression **Transmit: better than -45dBc, IMD3 (two-tone) -33dBc, Receive: better than -50dBc**
- **Open source** firmware, built with Arduino IDE; allows experimentation, new features can be added, contributions can be shared via Github, software-complexity: 2000 lines of code
- Software-based **VOX** that can be used as **fast Full Break-In** (QSK and semi-QSK operation) or assist in RX/TX switching for operating digital modes (no CAT or PTT interface required), external PTT output/PA control with **TX-delay**
- **Lightweight and low-cost transceiver design**: because of the EER-transmitter class-E stage it is **highly power-efficient** (no bulky heatsinks required), and has a **simple design** (no complex balanced linear power amplifier required)
- **Fully digital and software-based SSB transmit-stage**: samples microphone-input and reconstruct a SSB-signal by controlling the phase of the SI5351 PLL (through tiny frequency changes over 800kbits/s I2C) and the amplitude of the PA (through PWM of the PA key-shaping circuit)
- **Fully digital and software-based SDR receiver-stages (optionally)**: samples I/Q (complex) signal from Quadrature Sampling Detector digital mixer, and performs a 90-degree phase-shift mathematically in software (Hilbert-transform) and cancels out one side-band by adding them
- **CW decoder**, Straight/Iambic-A/B **keyer**
- **VFO A/B + RIT and Split**, and corresponding relay band-filter switching via I2C
- Probably the most **cost effective** and **easy** to build standalone SDR/SSB transceiver that you can find. Very much **simplified** circuit and **versatile** in use.


## Hardware

The Pebble HF hardware is designed by Barbaros Asuroglu, WB2CBA. For hardware schematics and build information, visit [pebblehf.com](https://pebblehf.com).

This project is based on the original uSDX design. For other uSDX hardware variants, see the [uSDX Forum].

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


## Operation:

There is a main tuning knob and a MENU (R) and SELECT (L) button.  For basic operation, the tuning knob is used to change the frequency.  Pressing the MENU button will bring up a menu of options.  Turning the knob with the menu open will allow you to select and change the options.


| Menu Item           | Function                                     | Button |
| ------------------- | -------------------------------------------- | ------ |
| 1.1 Volume          | Audio level (0..16) & power-off/on (turn left) | **E +turn** |
| 1.2 Mode            | Modulation (LSB, USB, CW) | (via menu) |
| 1.3 Filter BW       | Audio passband (Full, 300..3000, 300..2400, 300..1800, 500, 200, 100, 50 Hz), this also controls the SSB TX BW. | **R double** |
| 1.5 Tuning Rate     | Tuning step size 10M, 1M, 0.5M, 100k, 10k, 1k, 0.5k, 100, 10, 1 | **E or E long** |
| 1.6 VFO Mode        | Selects different VFO, or RX/TX split-VFO (A, B, Split) | **R long** |
| 1.7 RIT             | RX in transit (ON, OFF) | **R long** |
| 1.8 AGC             | Automatic Gain Control (ON, OFF) | |
| 1.9 NR              | Noise-reduction level (0-8), low-pass & smooth | |
| 1.10 ATT            | Analog Attenuator (0, -13, -20, -33, -40, -53, -60, -73 dB) | |
| 1.11 ATT2           | Digital Attenuator in CIC-stage (0-16) in steps of 6dB | |
| 1.12 S-meter        | Type of S-Meter (OFF, dBm, S, S-bar) | |
| 2.1 CW Decoder      | Enable/disable CW Decoder (ON, OFF) | |
| 2.2 CW Tone         | CW sidetone frequency (300-900 Hz) | |
| 2.3 CW Side Vol     | CW sidetone volume (0-16), independent of main volume | |
| 2.4 Semi QSK        | On TX silences RX on CW sign and word spaces | | 
| 2.5 Keyer speed     | CW Keyer speed in Paris-WPM (1..60) | |
| 2.6 Keyer mode      | Type of keyer (Iambic-A, -B, Straight) | |
| 2.7 Keyer swap      | Swap keyer DIT, DAH inputs (ON, OFF) | |
| 2.8 Practice        | Disable TX for practice purposes (ON, OFF) | |
| 3.1 VOX             | Voice Operated Xmit (ON, OFF) | |
| 3.2 Noise Gate      | Audio threshold for SSB TX and VOX (0-255) | |
| 3.3 TX Drive        | Transmit audio gain (0-8) in steps of 6dB, 8=constant amplitude for SSB | |
| 8.1 PA Bias min     | PA amplitude PWM level (0-255) for representing 0% RF output | |
| 8.2 PA Bias max     | PA amplitude PWM level (0-255) for representing 100% RF output | |
| 8.3 Ref freq        | Actual SI5351 crystal frequency, used for frequency-calibration | |
| 8.4 IQ Phase        | RX I/Q phase offset in degrees (0..180 degrees) | |
| 10.1 Version        | Display firmware version and compile date | |
| power-up            | Reset to factory settings | **E long** |
| main                | Tune frequency (20kHz..99MHz) | **turn** |
| main                | Quick menu | **L +turn** |
| main                | Menu enter | **L** |
| RIT                 | RIT back | **R** |
| menu                | Menu back | **R** |


Operating Instructions:

Tuning can be done by turning the rotary encoder. Its step size can be decreased or increased by a short or long press. A double press on the right button narrows the receiver filter bandwidth. The volume is changed by turning the rotary encoder while pressed.

There is a menu available that can be accessed by a short left press. With the encoder it is possible to navigate through this menu. When you want to change a menu parameter, a press with left button allows you to change the parameter with the encoder. With the right button it is possible to exit the menu any time. A fast access to the menu and parameter can be achieved by pressing the left button while turning the encoder, once you lift the left button you can immediately change the parameter by turning the encoder.

For receive, by default an AGC is disabled but can be enabled in the menu. This increases the volume when there are weak signals and decreases for strong signals. This is good for SSB signals but can be annoying for CW operation. The AGC can be turned off in the menu, this makes the receiver less noisy but require more manual volume change. To further reduce the noise, a noise-reduction function can be enabled in the menu with the NR parameter. To use the available dynamic range optimally, you can attenuate incoming signal by enabling a front-end attenuator with "ATT" parameter. Especially on frequencies 3.5-7 MHz the atmospheric noise levels are much higher, so you can increase the receiver performance by adding attenuation (e.g 13dB) such that the noise-floor is still audible. 

For SSB voice operation, connect a microphone to the paddle jack, a PTT or onboard "key" press will bring the transceiver into transmit. With the "TX Drive" parameter, it is possible to set the modulation depth or PA drive. Setting menu item "VOX" to ON enters the transceiver in Voice-On-Xmit operation (TX mode as soon as audio is detected), the VOX sensitivity can be configured with the "Noise Gate" parameter.

For FT8 (and any other digital) operation, tune to the FT8 frequency (14.074 MHz), connect the headphone jack to sound card microphone jack, sound card speaker jack to microphone jack, and enable VOX mode in the menu. Adjust the volume to a minimum and start your favorite FT8 application (JTDX, WSJT-X, etc.). The sensitivity of the VOX can be set in the "Noise Gate" parameter. 

On startup, the transceiver is performing a self-test (when DIAG option is enabled). It is checking the supply and bias voltages, I2C communications and algorithmic performance. In case of deviations, the display will report an error during startup. It also discovers the capabilties of the transceiver depending on the mods made.


## Credits

**Pebble HF Project**: Mike N4FFF - Firmware modifications and project maintenance

**Original uSDX Project**: The uSDX was originally announced in the [QRPLabs Forum] as a SSB modification for a [QCX]. The [uSDX] transmitter and receiver stage both running on a ATMEGA328P, including its multiband front-end and direct PA biasing/envelope-generation technique; its concept, circuit, code are a design by _Guido (PE1NNZ)_; the software-based SSB transmit stage is a derivate of earlier experiments with a [digital SSB generation technique] on a Raspberry Pi.

**Hardware Design**: Barbaros Asuroglu (WB2CBA) - Pebble HF hardware design

Many thanks to all contributors to the open source uSDX project, without whose work the Pebble HF would not be possible.

<!-- Link references -->
[uSDX]: https://github.com/threeme3/usdx
[uSDX Forum]: https://groups.io/g/ucx
[QRPLabs Forum]: https://groups.io/g/QRPLabs/topic/29572792
[QCX]: https://qrp-labs.com/qcx.html
[digital SSB generation technique]: http://pe1nnz.nl.eu.org/2013/05/direct-ssb-generation-on-pll.html


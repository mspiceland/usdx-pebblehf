# Troubleshooting and FAQ

## Toroid Winding

Winding the toroids correctly is critical for getting the most out of your Pebble HF and for protecting your finals (RF transmitting transistors).

The Pebble HF uses a **Class E PA design**. This high-efficiency design is what allows the Pebble HF to operate without a heatsink. However, this efficiency depends on well-wound toroids.

### Winding Tips

- **Pull each turn tight** — loose windings reduce efficiency
- **Space turns evenly** — consistent spacing improves performance
- **Inspect your work** — poor windings are the most common cause of issues

### Expected Performance

With proper toroid winding and 13.8V input:

| Efficiency | Output Power | Notes |
|------------|--------------|-------|
| 75–79% | 4.5–5.5 W | Normal, healthy operation |
| Below 50% | Reduced | Excessive heat generated |

> **Warning:** If efficiency drops below 50%, the PA will generate considerable heat. This will eventually cause the BS170 transistors to fail after extended TX periods.

### Protection

The Pebble HF includes diode protection against poor SWR and accidental transmission with no antenna connected. **The most likely cause of failed transistors is improper toroid winding**, not SWR issues.

---

## Frequently Asked Questions

### Q: What is the setup for digital modes?

For digital modes (FT8, JS8Call, etc.), you will need an external USB sound card.

#### Connections

| Sound Card Jack | Connects To |
|-----------------|-------------|
| Input (red) | Pebble HF headphone output |
| Output (green) | Pebble HF mic/key input |

#### Recommended Settings

1. **Firmware**: Use v1.0.4 or later (fixes sound card compatibility issues)
2. **VOX**: Set to **ON**
3. **Noise Gate**: Set to **50** (increase if you experience unexpected TX)
4. **Practice Mode**: Start with **ON** to verify timing before transmitting

#### Setup Procedure

1. Connect the sound card as shown above
2. Set **Practice Mode** to **ON**
3. Configure your digital mode software (WSJT-X, JS8Call, etc.) to use VOX for the radio
4. Verify the radio keys at the correct times
5. Set **Practice Mode** to **OFF** to transmit for real

#### Sound Card Compatibility Note

Starting with firmware v1.0.4, when VOX mode is enabled, the Tip conductor from the TRS (tip-ring-sleeve) audio cable is ignored. Some sound cards have impedance characteristics that would cause the radio to transmit as if the PTT button was pressed. This change improves compatibility with a wider range of external sound cards.

---

### Q: How do I report issues?

For community support, please join the **Discord channel** listed on the quickstart guide that came with your Pebble HF.

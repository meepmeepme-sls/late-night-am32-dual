# Late Night AM32 Dual

A bulletproof, high-backvoltage **Dual 40 A AM32 Combat Robot ESC** engineered for 2S–6S LiHV (`6.0 V – 26.1 V`) drive systems, featuring an overbuilt **100 V-rated 5 V receiver BEC**, **85 V high-avalanche MOSFETs**, **3000 W surge clamping**, and **100% stock `AM32_RR_ROBOT_DUAL_ESC_F421` firmware compatibility** (no custom mixer firmware; mix on transmitter).

## Repository Contents

- [`DESIGN_SPEC.md`](DESIGN_SPEC.md) — Full hardware specification, visual teardown comparison (Repeat Robotics Dual AM32 vs. JCR SNIPE Dual 40A v1.0/v2.0), high-backvoltage failure analysis, MCU pinout (`AT32F421G8U7`), 4-stage 100 V BEC architecture, and PCB layout rules.
- [`bom_jlcpcb.csv`](bom_jlcpcb.csv) — JLCPCB-ready Bill of Materials with verified LCSC part numbers.
- [`verify_calculations.py`](verify_calculations.py) — Python verification script for voltage breakdown margins, BEMF/ADC divider clamping, shunt heat, MOSFET conduction losses, and BEC holdup calculations.
- [`reference_images/`](reference_images/) — Product photos and zoomed IC marking crops (`crops/`) used for the component teardown.

## Quick Verification

```bash
python3 verify_calculations.py
```

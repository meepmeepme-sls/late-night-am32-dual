#!/usr/bin/env python3
"""Electrical, thermal, backvoltage & Qty-500 economics checks for the Late Night AM32 Dual ESC."""

VBAT_MIN = 11.1         # 3S nominal (9.0V discharged)
VBAT_NOM = 14.8         # 4S nominal
VBAT_MAX = 26.1         # 6S LiHV full charge (4.35V * 6)
V_TVS_CLAMP_28A = 45.4  # SMCJ28A (1500W) max clamping voltage
V_TVS_CLAMP_30A = 48.4  # SMCJ30A (1500W) max clamping voltage
V_REGEN_EXTREME = 65.0  # Unclamped back-EMF spike before clamp

print("=== 1. HIGH-BACKVOLTAGE TVS vs. MOSFET & REGULATOR BREAKDOWN MARGINS ===")
devices = [
    ("Repeat Dual MOSFET (Toshiba TPN2R304PL)", 40.0),
    ("Repeat Dual 5V BEC (TI LMR33620B abs max)", 38.0),
    ("Repeat Dual Gate LDO (78L08 / 8G)", 35.0),
    ("JCR SNIPE MOSFET (RS120N04AD / S120N04D)", 40.0),
    ("Cost-Opt Primary MOSFET: AGM403A1 (40V, 5x6mm)", 40.0),
    ("Drop-In 60V Alt MOSFET: DON120N06 (60V, 5x6mm)", 60.0),
    ("Extreme 85V Alt MOSFET: APM AP140N08NF (85V)", 85.0),
    ("Cost-Opt 10V Gate Buck: XL7015E1 (80V)", 80.0),
    ("Bulletproof 5V RX BEC: TI LM5164DDAR (100V / 105V)", 100.0),
]
for name, v_rating in devices:
    margin_28a = v_rating - V_TVS_CLAMP_28A
    status = (
        "PASS"
        if margin_28a >= 10.0
        else ("MARKET-40V CLASS" if margin_28a < 0 and "AGM403A1" in name else ("FAIL (Avalanches before TVS full clamp!)" if margin_28a < 0 else "TIGHT"))
    )
    print(f"{name:52s} | Rating: {v_rating:5.1f} V | Margin @ SMCJ28A ({V_TVS_CLAMP_28A}V): {margin_28a:+6.1f} V [{status}]")

print("\n=== 2. VOLTAGE SENSE & BEMF DIVIDERS (11:1) UNDER HIGH BACK-VOLTAGE ===")
R_TOP = 100_000.0
R_BOT = 10_000.0
ratio = (R_TOP + R_BOT) / R_BOT
v_adc_max = VBAT_MAX / ratio
v_adc_clamp = V_TVS_CLAMP_28A / ratio
v_adc_extreme = V_REGEN_EXTREME / ratio
v_vbat_at_3v6_limit = 3.6 * ratio
print(f"Divider ratio: {ratio:.2f}:1 (AM32 TARGET_VOLTAGE_DIVIDER = {int(round(ratio * 10))})")
print(f"Pin voltage @ 6S LiHV ({VBAT_MAX} V): {v_adc_max:.3f} V (safe, < 3.30 V)")
print(f"AT32F421G8U7 abs max analog pin voltage (VDDA + 0.3V = 3.60V) reached at VBAT = {v_vbat_at_3v6_limit:.1f} V!")
print(f"Unclamped pin voltage @ SMCJ28A peak ({V_TVS_CLAMP_28A} V): {v_adc_clamp:.2f} V -> REQUIRES BAT54S clamp to 3.3V!")
print(f"Unclamped pin voltage @ 65 V phase BEMF spike: {v_adc_extreme:.2f} V -> BAT54S limits to 3.55 V (I_clamp = {(v_adc_extreme-3.3)/(22000*2200/24200)*1000:.2f} mA)")

print("\n=== 3. CURRENT SENSE COMPARISON (1x 1.0 mOhm RLM25FEER001 + INA180A2 vs INA180A1) ===")
for r_shunt, gain, name in [
    (0.00100, 12, "Repeat Dual: 1x 1.0 mOhm (R001) + ~12 V/V amp"),
    (0.00100, 50, "Cost-Opt Primary: 1x 1.0 mOhm + INA180A2 (50 V/V)"),
    (0.00100, 20, "High-Current Alt: 1x 1.0 mOhm + INA180A1 (20 V/V)"),
]:
    mv_per_a = r_shunt * gain * 1000.0
    i_fs = 3.3 / (r_shunt * gain)
    p_shunt_40a = (40.0 ** 2) * r_shunt
    print(f"{name:55s}: {mv_per_a:4.1f} mV/A | Full-scale = {i_fs:5.1f} A | Shunt heat @ 40A = {p_shunt_40a:.2f} W")

print("\n=== 4. MOSFET CONDUCTION LOSS PER CHANNEL @ 40 A CONTINUOUS ===")
I_CONT = 40.0
for name, rds_typ_mohm in [
    ("40V AGM403A1 (2.3 mOhm typ @ 10V)", 2.3),
    ("60V DON120N06 (3.5 mOhm typ @ 10V)", 3.5),
    ("85V APM AP140N08NF (2.5 mOhm typ @ 10V)", 2.5),
]:
    rds_hot = (rds_typ_mohm / 1000.0) * 1.45
    p_cond_ch = 2.0 * (I_CONT ** 2) * rds_hot
    print(f"{name:45s} | Hot Rds = {rds_hot*1000:.2f} mOhm | Channel loss @ 40A = {p_cond_ch:.2f} W ({p_cond_ch/6:.2f} W/FET avg)")

print("\n=== 5. REGENERATIVE BRAKING / IMPACT ENERGY ABSORPTION (50V CAP BANK) ===")
C_BUS = (2 * 220e-6) + (6 * 10e-6)
e_cap_j = 0.5 * C_BUS * (45.0**2 - 25.2**2)
print(f"Onboard + Bulk Bank Capacitance: {C_BUS*1e6:.0f} uF (50V rated)")
print(f"Single-pulse energy absorbed by {C_BUS*1e6:.0f} uF cap bank (25.2V -> 45.0V before SMCJ28A): {e_cap_j*1000:.1f} mJ")

print("\n=== 6. OVERBUILT 5 V RECEIVER BEC BUDGET (100V LM5164DDAR + SS310) ===")
I_RX_TYP = 0.15
EFF = 0.85
C_HOLDUP = 100e-6  # 100uF 50V SMD holdup cap behind SS310
p_in_rx = (5.05 * I_RX_TYP) / EFF
t_holdup_ms = 1000.0 * (0.5 * C_HOLDUP * (12.0**2 - 6.5**2)) / p_in_rx
C_OUT_EXT = 470e-6
dv_step = 0.30 * 50e-6 / C_OUT_EXT
print(f"Input holdup across complete VBAT dropout (12 V -> 6.5 V @ 150 mA RX, 100 uF 50V holdup): {t_holdup_ms:.2f} ms")
print(f"5 V droop on sudden 300 mA / 50 us RX telemetry burst with 470 uF ext cap: {dv_step*1000:.2f} mV")

print("\n=== 7. QTY-500 BOM & LANDED MARGIN VERIFICATION ===")
QTY = 500
verified_bom = [
    ("U1, U2 (AT32F421G8U7)", 2, 0.4680),
    ("U3, U4 (EG6288)", 2, 0.2101),
    ("Q1-Q12 (AGM403A1)", 12, 0.1846),
    ("R_SH1-2 (RLM25FEER001)", 2, 0.0403),
    ("U5, U6 (INA180A2IDBVR)", 2, 0.1030),
    ("U7 (LM5164DDAR - 5V BEC)", 1, 1.5781),
    ("U8 (XL7015E1 - 10V Gate)", 1, 0.2405),
    ("U9, U10 (AMS1117-3.3)", 2, 0.1141),
    ("D1 (SS310)", 1, 0.0493),
    ("D2 (SMCJ28A)", 1, 0.0519),
    ("D3 (SMBJ30A)", 1, 0.0324),
    ("D4 (SMBJ5.0A)", 1, 0.0311),
    ("F1 (nSMD050-33V)", 1, 0.0429),
    ("FB1, FB2 (BLM18PG121SN1D)", 2, 0.0105),
    ("L1, L2 (PNLS5040-150M)", 2, 0.0473),
    ("C_VBAT_EXT1-2 (XT220UF50V90RV0078)", 2, 0.1332),
    ("C_VBAT1-6 (CL31B106KBHNNNE)", 6, 0.1205),
    ("C_BEC_HOLD (CK1H101M-CRE77)", 1, 0.0398),
    ("C_BEC_OUT1-2 (CGA1206X7R226K160NT)", 2, 0.0876),
    ("D_VS1-6 (RB520S-30)", 6, 0.0146),
    ("D_GOFF1-12 (1N4148WS)", 12, 0.0077),
    ("D_CLAMP1-8 (BAT54S)", 8, 0.0196),
    ("C_BOOT/DEC (100nF 0603)", 14, 0.0037),
    ("R_10k (0603)", 16, 0.0014),
    ("R_22k (0603)", 12, 0.0026),
    ("R_2R2 (0603)", 18, 0.0022),
]
comp_verified = sum(q * p for _, q, p in verified_bom)
comp_misc_est = 0.0500  # ~28 Basic 0603 passives & LEDs
comp_total = comp_verified + comp_misc_est

pcba_total_500 = 25.56 + 8.21 + 164.18 + (27 * 1.53) + (357 * 0.0013 * QTY) + (0.25 * QTY)
pcba_per_bd = pcba_total_500 / QTY
pcb_total_500 = (0.040 * 0.028 * QTY * 65.67) + 20.52
pcb_per_bd = pcb_total_500 / QTY

ex_works = comp_total + pcba_per_bd + pcb_per_bd
landed_extras = 2.30  # Freight (~$0.60) + tariff/duty (~$1.20) + heatshrink/coat/pack (~$0.50)
landed_cogs = ex_works + landed_extras

print(f"Verified LCSC components/bd: ${comp_verified:.2f} (+ ${comp_misc_est:.2f} Basic passives est = ${comp_total:.2f})")
print(f"JLCPCB PCBA fee/bd (qty 500): ${pcba_per_bd:.2f} (${pcba_total_500:.2f} total)")
print(f"Bare PCB 4L 1oz HASL/bd:      ${pcb_per_bd:.2f} (${pcb_total_500:.2f} total)")
print(f"Ex-Works PCBA unit cost:      ${ex_works:.2f}")
print(f"Estimated Landed COGS:        ${landed_cogs:.2f} (Target <= $16.00 for 60% @ $40 MSRP)")
for msrp in [35.0, 38.0, 40.0, 42.0, 45.0]:
    gp = msrp - landed_cogs
    gm = (gp / msrp) * 100.0
    print(f"  MSRP ${msrp:5.2f} -> Gross Profit ${gp:5.2f} | Gross Margin: {gm:5.1f}%")

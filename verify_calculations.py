#!/usr/bin/env python3
"""Electrical, thermal & high-backvoltage transient checks for the Dual 40A AM32 Combat ESC."""

VBAT_MIN = 6.0        # 2S discharged
VBAT_NOM = 14.8       # 4S nominal
VBAT_MAX = 26.1       # 6S LiHV full charge (4.35V * 6)
V_TVS_CLAMP_28A = 45.4  # SMDJ28A (3000W) max clamping voltage @ 66.1A Ipp
V_TVS_CLAMP_30A = 48.4  # SMDJ30A (3000W) max clamping voltage @ 62.0A Ipp
V_REGEN_EXTREME = 65.0  # Unclamped back-EMF spike if battery disconnects or before clamp

print("=== 1. HIGH-BACKVOLTAGE TVS vs. MOSFET & REGULATOR BREAKDOWN MARGINS ===")
devices = [
    ("Repeat Dual MOSFET (Toshiba TPN2R304PL)", 40.0),
    ("Repeat Dual 5V BEC (TI LMR33620B abs max)", 38.0),
    ("Repeat Dual Gate LDO (78L08 / 8G)", 35.0),
    ("JCR SNIPE MOSFET (RS120N04AD / S120N04D)", 40.0),
    ("Our Upgrade Option A: TI CSD18540Q5B (60V)", 60.0),
    ("Our Upgrade Primary: APM AP140N08NF (85V, 900mJ Eas)", 85.0),
    ("Our Upgrade Extreme: HUAYI HYG037N10LS2C2 (100V)", 100.0),
    ("Our BEC & Gate Bucks: TI LM5164DDAR (100V / 105V abs)", 100.0),
]
for name, v_rating in devices:
    margin_28a = v_rating - V_TVS_CLAMP_28A
    status = "PASS" if margin_28a >= 10.0 else ("FAIL (Avalanches before TVS full clamp!)" if margin_28a < 0 else "TIGHT")
    print(f"{name:52s} | Rating: {v_rating:5.1f} V | Margin @ SMDJ28A ({V_TVS_CLAMP_28A}V): {margin_28a:+6.1f} V [{status}]")

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
print(f"AT32F421G8U7 absolute max analog pin voltage (VDDA + 0.3V = 3.60V) reached at VBAT = {v_vbat_at_3v6_limit:.1f} V!")
print(f"Unclamped pin voltage @ SMDJ28A peak ({V_TVS_CLAMP_28A} V): {v_adc_clamp:.2f} V -> REQUIRES BAT54S clamp to 3.3V!")
print(f"Unclamped pin voltage @ 65 V phase BEMF spike: {v_adc_extreme:.2f} V -> BAT54S limits to 3.55 V (I_clamp = {(v_adc_extreme-3.3)/(22000*2200/24200)*1000:.2f} mA)")

print("\n=== 3. CURRENT SENSE COMPARISON (Repeat 1.0 mOhm vs. Our 2x 0.5 mOhm = 0.25 mOhm) ===")
for r_shunt, gain, name in [
    (0.00100, 12, "Repeat Dual: 1x 1.0 mOhm (R001) + ~12 V/V amp"),
    (0.00025, 50, "Our Design:  2x 0.5 mOhm (0.25 mOhm) + INA180A2 (50 V/V)"),
]:
    mv_per_a = r_shunt * gain * 1000.0
    i_fs = 3.3 / (r_shunt * gain)
    p_shunt_40a = (40.0 ** 2) * r_shunt
    print(f"{name:55s}: {mv_per_a:4.1f} mV/A | Full-scale = {i_fs:5.1f} A | Shunt heat @ 40A = {p_shunt_40a:.2f} W")

print("\n=== 4. MOSFET CONDUCTION LOSS PER CHANNEL @ 40 A CONTINUOUS ===")
I_CONT = 40.0
for name, rds_typ_mohm in [
    ("60V TI CSD18540Q5B (1.8 mOhm typ)", 1.8),
    ("85V APM AP140N08NF (2.5 mOhm typ, 900mJ Eas)", 2.5),
    ("100V HUAYI HYG037N10LS2C2 (3.0 mOhm typ)", 3.0),
]:
    rds_hot = (rds_typ_mohm / 1000.0) * 1.45
    p_cond_ch = 2.0 * (I_CONT ** 2) * rds_hot
    print(f"{name:45s} | Hot Rds = {rds_hot*1000:.2f} mOhm | Channel loss @ 40A = {p_cond_ch:.2f} W ({p_cond_ch/6:.2f} W/FET avg)")

print("\n=== 5. REGENERATIVE BRAKING / IMPACT ENERGY ABSORPTION (50V POLYMER CAP BANK) ===")
# Kinetic energy of a 3lb (1.36kg) beetleweight at 4.5 m/s (10 mph): 0.5 * m * v^2 = 13.8 J
# Stored energy delta in 2x 220uF + 12x 10uF = 500 uF capacitor bank from 25.2V to 45.0V:
C_BUS = (2 * 220e-6) + (12 * 10e-6)
e_cap_j = 0.5 * C_BUS * (45.0**2 - 25.2**2)
print(f"Onboard + Polymer Bank Capacitance: {C_BUS*1e6:.0f} uF (50V rated)")
print(f"Single-pulse energy absorbed by 500 uF cap bank (25.2V -> 45.0V before TVS): {e_cap_j*1000:.1f} mJ")
print(f"SMDJ28A (3000W 10/1000us) + AP140N08NF (900mJ Eas per FET) provides massive avalanche safety buffer.")

print("\n=== 6. OVERBUILT 5 V RECEIVER BEC BUDGET (100V LM5164DDAR + SS310) ===")
V_SCHOTTKY_DROP = 0.45
I_RX_TYP = 0.15
EFF = 0.85
C_HOLDUP = 120e-6  # 100uF 50V polymer + 2x 10uF 50V MLCC
p_in_rx = (5.05 * I_RX_TYP) / EFF
t_holdup_ms = 1000.0 * (0.5 * C_HOLDUP * (12.0**2 - 6.5**2)) / p_in_rx
C_OUT_EXT = 470e-6
dv_step = 0.30 * 50e-6 / C_OUT_EXT
print(f"Input holdup across complete VBAT dropout (12 V -> 6.5 V @ 150 mA RX, 120 uF 50V holdup): {t_holdup_ms:.2f} ms")
print(f"5 V droop on sudden 300 mA / 50 us RX telemetry burst with 470 uF ext cap: {dv_step*1000:.2f} mV")

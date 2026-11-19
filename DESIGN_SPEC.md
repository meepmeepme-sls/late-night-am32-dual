# Dual 40 A AM32 Combat ESC — High-Backvoltage Hardware Design Specification

**Baseline:** Combines the active current limiting, double-sided battery passthrough, and `AT32F421G8U7` stock firmware compatibility of the **Repeat Robotics Dual AM32 ESC** with the 40 A continuous rating, plated through-hole wire tabs, and `50 V` bulk capacitor bank of the **Just 'Cuz Robotics SNIPE Dual 40A (v2.0)** — **without custom mixer firmware** (two independent channels, mix on radio) and engineered for **3S–6S LiHV (`26.1 V` max) combat robotics** with an **overbuilt 100 V-rated `5 V` Receiver BEC**.

> [!IMPORTANT]
> **Project Economics & Costed BOM (Qty 500 Target):**
> See [`BOM_ECONOMICS.md`](file:///home/antigravity/meepmeepme-sls/late-night-am32-dual/BOM_ECONOMICS.md) and [`bom_jlcpcb.csv`](file:///home/antigravity/meepmeepme-sls/late-night-am32-dual/bom_jlcpcb.csv) for full itemized LCSC/JLCPCB Qty-500 pricing, PCBA fee breakdown, and margin sensitivity.
> - **Components (Qty 500):** `$7.96/board` | **Ex-Works PCBA (4L 1 oz HASL, Single-Sided SMT):** `$9.26/unit` | **Est. Landed COGS:** **`$11.56/unit`**
> - **Margin @ `$40.00` MSRP:** **`71.1%` Gross Margin** (`$28.44` gross profit/unit), exceeding the `60%` target (`≤$16.00` COGS) with `$4.44/unit` headroom.

---

## 1. Visual Teardown Comparison (From High-Res Product Photos)

All product photos and zoomed IC marking crops are saved in [`reference_images/`](file:///home/antigravity/dual-am32-esc/reference_images/) and [`reference_images/crops/`](file:///home/antigravity/dual-am32-esc/reference_images/crops/).

| Subsystem | Repeat Robotics Dual AM32 (`28 × 20 mm`) | JCR / cb-technology SNIPE Dual 40A (`32 × 20 mm`, v1.0 & v2.0) | Late Night AM32 Dual (`~40 × 28 mm`, Cost-Optimized 3S–6S LiHV) |
| :--- | :--- | :--- | :--- |
| **Main MCUs (`2×`)** | **Artery `AT32F421G8U7`** (`QFN-28 4×4 mm`, LCSC `C2765098`), 1 Front / 1 Back | **Artery `AT32F421G8U7`** (`QFN-28 4×4 mm`, LCSC `C2765098`), both on Back (v2.0) | **Artery `AT32F421G8U7`** (`QFN-28 4×4 mm`, LCSC `C2765098`) — flashes stock `AM32_RR_ROBOT_DUAL_ESC_F421` |
| **Aux Mixer MCU** | None (`S1`/`S2` independent) | **3rd QFN-20 (3×3 mm) MCU** between the two `AT32F421` ICs for mixing/CRSF | **None** (eliminates 3rd MCU failure/firmware point; mix on radio) |
| **Gate Drivers (`2×`)** | **Fortior `FD6288Q`** (`QFN-24 4×4 mm`, LCSC `C328453`), 1 Front / 1 Back | **Fortior `FD6288Q`** (`QFN-24 4×4 mm`, LCSC `C328453`), both on Back (v2.0) | **`EG6288`** (`TSSOP-20`, LCSC `C54102120`, `220 V`, `+1.8 A/-2.3 A`, internal boot diodes) + **6× `RB520S-30` Negative-`VS` Schottkys** |
| **MOSFETs (`12×`)** | **Toshiba `TPN2R304PL`** (`2R304 PL`, LCSC `C5802634`): **40 V**, `1.8 mΩ` typ, `3.3 × 3.3 mm` | **`RS120N04AD` / `S120N04D`** (LCSC `C47665714`): **40 V**, `<3.5 mΩ`, `3.3 × 3.3 mm` | **`AGM403A1`** (`C5184861`): **40 V, `2.3 mΩ` @ 10 V, 120 A**, `5 × 6 mm` PDFN-8 *(drop-in 60 V alt: `DON120N06` `C41384268`; 85 V alt: `AP140N08NF`)* |
| **Current Sensing** | **Yes:** `1× 1.0 mΩ` (`R001`) 2512 shunt per ch + SOT-23-5 amp (`1639`) | **None** (no current shunts on v1.0 or v2.0) | **Yes:** `1× 1.0 mΩ` `RLM25FEER001` (`C316227`) per ch + `INA180A2` (`C192764`, `50 V/V` = `50 mV/A`; or `INA180A1` `20 mV/A`) |
| **5 V Receiver BEC** | **TI `LMR33620B`** (**36 V max / 38 V abs max**) + `4R7` inductor | Tiny **SOT-23-6 buck** + miniature `0805` chip inductor (**250 mA max**) | **TI `LM5164DDAR`** (**100 V / 105 V abs max**, `1 A`, `C477928`) + `SS310` `100 V` diode + `100 µF 50 V` holdup + `500 mA` PTC |
| **Gate Drive Supply (`VCC`)** | **SOT-89-3 `78L08` (`8G`) 8 V Linear LDO** (**30–35 V max input**) | **SOT-89-3 Linear Regulator** (`L78Lxx`) + 2nd SOT-23-6 step-down | **`XL7015E1`** (`TO-252-5`, `C73013`, **80 V, 0.8 A Buck**) set to **full `10.0 V`** (zero linear heat, `$0.24` vs `$1.58`) |
| **3.3 V MCU LDO** | Single SOT-23-5 LDO (`AG5R`) on Back | Single SOT-23-5 LDO (`WB33` on v1.0) | **2× Independent `AMS1117-3.3` LDOs** (`C6186`, Basic) fed from `10.0 V` buck rail (complete channel fault isolation) |
| **Onboard TVS Clamp** | **None!** (`0 W` onboard TVS) | **1× `400 W` SMA (`DO-214AC`) TVS** | **1× `1500 W` SMC (`DO-214AB`) `SMCJ28A`** (`C20883365`, `45.4 V` max) + `SMBJ30A` (`C3009993`) on `BEC_VIN` |
| **External Bus Caps** | `1× 35 V` radial electrolytic cap on battery leads | **v2.0:** **`2× 220 µF 50 V` Conductive Polymer Hybrid Caps** | **`2× 220 µF 50 V` SMD Caps** (`XT220UF50V90RV0078`, `C2992609`) + **`6× 10 µF 50 V` X7R MLCCs** (`C89632`) |
| **Analog BEMF / ADC Clamps** | None (unclamped `11:1` dividers fail above `VBAT = 39.6 V`) | None (unclamped `11:1` dividers fail above `VBAT = 39.6 V`) | **8× `BAT54S` Dual Series Schottky Clamps to `3.3 V`/`GND`** (`C699095`) on `VBAT_ADC` and `BEMF_A/B/C` + **6× Phase `RC` Snubbers** |
| **Wire Termination** | Surface-mount corner pads + double-sided `VBAT`/`GND` weapon passthrough | **Plated Through-Hole Edge Solder Tabs** (`A B C BATT GND A B C`) | **Both:** Plated through-hole wire tabs (100G pull resistance) **plus** double-sided `VBAT`/`GND` weapon ESC passthrough |

---

## 2. Why Commercial 6S ESCs Die in High Back-Voltage Combat — & How We Solve It

In combat robotics, drive motors experience four simultaneous high-voltage surge mechanisms:
1. **Synchronous Active Braking & Full-Stick Reversals:** AM32 uses complementary PWM (damped light / active freewheeling). Sudden deceleration turns the motor inductance and rotor inertia ($\frac{1}{2} J \omega^2$) into a boost converter pumping energy back into `VBAT`.
2. **Back-Driven Impacts from Opponent Weapons:** When a horizontal/vertical spinner launches your robot across the box, the drive wheels are mechanically forced faster than their no-load Kv speed, generating `45 V – 80 V` back-EMF across the bridge.
3. **Master Switch / Removable Link Contact Bounce or BMS Trip:** If a master switch bounces open for even `100 µs` during active braking, the battery disappears as a current sink and `VBAT` skyrockets immediately.
4. **Inductive Cable Whip ($V = L \frac{dI}{dt}$):** Interrupting `40 A – 100 A` across battery leads creates sharp voltage spikes.

### The Fatal Flaw in Repeat Dual & JCR SNIPE (`40 V` Parts vs. `45.4 V` 6S TVS Clamping)
On a 6S LiHV (`26.1 V`) battery, a TVS diode must have a standoff voltage $V_{RWM} \ge 28\text{ V}$ so it does not conduct and burn up during normal operation. However, a `28 V` TVS (`SMBJ28A` / `SMDJ28A`) does not reach its full clamping current until **`45.4 V`** (`48.4 V` for a `30 V` TVS).
- **Repeat Dual** uses **`40 V` MOSFETs (`TPN2R304PL`)**, a **`36 V` BEC (`LMR33620B`, `38 V` abs max)**, and a **`30–35 V` linear gate regulator (`78L08`)** — with **no onboard TVS**.
- **JCR SNIPE** uses **`40 V` MOSFETs (`RS120N04AD`)**.
- **Result:** On both commercial boards, **the MOSFETs (`40 V`) and regulators (`35 V–38 V`) break down and enter avalanche BEFORE a 6S TVS diode can even finish clamping at `45.4 V`!** Even worse, above `39.6 V`, the `11:1` BEMF and `VBAT_ADC` resistor dividers push `>3.60 V` (`VDDA + 0.3 V`) directly into the `AT32F421G8U7` analog pins!

### Our Cost-Optimized High-Reliability Architecture (3S–6S LiHV)
1. **`40 V` `5×6 mm` MOSFETs (`AGM403A1`, `C5184861`) — With Drop-In `60 V` / `85 V` Upgrade Path:**
   - Rated for **`40 V` $V_{DS}$**, **`2.3 mΩ` typical** at $V_{GS} = 10\text{ V}$, **120 A**, `Qg = 20 nC` in a `5 × 6 mm` PDFN-8 package (`2.75×` the thermal contact area of the `3.3 × 3.3 mm` FETs on Repeat and SNIPE), matching the market-accepted `40 V` class at **`$0.1846/ea`**.
   - *(Footprint-compatible `PDFN5×6-8L` upgrades: **`60 V` `DON120N06`** `C41384268` at `3.5 mΩ` typ for **`$0.1846/ea`** — +14.6 V margin above `SMCJ28A` — or **`85 V` `AP140N08NF`** `C56142574` for extreme 8S/high-surge builds).*
2. **`1500 W` SMC Surge Clamp (`SMCJ28A`, `C20883365`) + Optional Active Regen Bleed Pads:**
   - Replaces Repeat's `0 W` TVS and SNIPE's `400 W` SMA TVS with a **1500 W `SMCJ28A` (`DO-214AB` SMC)** unidirectional TVS across `VBAT`/`GND` (`28 V` standoff, `31.1 V` breakdown, `45.4 V` max clamp, **3.75× SNIPE's TVS rating** at `$0.0519/board`).
   - **Optional Active Regen Brake Shunt Pad (`Q_DUMP` + `R_DUMP`, DNP by default):** Unpopulated footprint for heavy-wheel 12 lb / 30 lb drive systems or bots prone to master-switch bounce.
3. **100 V `5 V` Receiver BEC (`LM5164DDAR`, `C477928`) + 80 V `10 V` Gate Buck (`XL7015E1`, `C73013`):**
   - **Zero compromise on the `5 V` RX BEC:** Uses TI's **100 V (`105 V` abs max) `LM5164DDAR`** + **100 V, 3 A `SS310` Schottky (`C330484`)** — more than **2.2×** the peak TVS clamping voltage.
   - **Cost-optimized `10.0 V` Gate Rail:** Uses **`XL7015E1` (`80 V`, `0.8 A` buck, `C73013`)** at `$0.2405` instead of a second `$1.58` `LM5164DDAR`, while still vastly outperforming Repeat's `35 V` `78L08` linear LDO.
4. **`50 V` Capacitor Bank (`2× 220 µF 50 V` SMD + `6× 10 µF 50 V` X7R MLCCs):**
   - Adopts SNIPE v2.0's `2× 220 µF 50 V` bulk upgrade using SMD `XT220UF50V90RV0078` (`C2992609`, `$0.1332/ea`), backed by **`6× 10 µF 50 V` X7R `1206` MLCCs** (`C89632`, `3` per channel directly across the half-bridges).
5. **Negative-`VS` Undershoot Clamping & Asymmetric Fast-Turn-Off Gate Drive (`EG6288` Hardening):**
   - Uses **`EG6288` (`TSSOP-20`, `C54102120`, `220 V`, `+1.8 A / -2.3 A`, `200 ns` deadtime, integrated bootstrap diodes)** — saves `~$4.32/board` over `FD6288Q` and eliminates `6×` external bootstrap diodes.
   - Retains **6× `RB520S-30` (`C7502701`)** negative-`VS` clamp Schottkys, **asymmetric gate networks** (`10 Ω` turn-on / `1N4148WS` + `2.2 Ω` turn-off + `10 kΩ` pull-downs), and **6× `RC` phase snubbers (`2.2 Ω` + `1 nF 100 V`)**.
6. **`BAT54S` Analog BEMF & `VBAT_ADC` Input Clamping (Protects the MCUs Above `39.6 V`):**
   - Retains **8× `BAT54S` dual series Schottky clamp arrays (`C699095`)** on `VBAT_ADC` and `BEMF_A/B/C` tied between `GND` and `3V3_CHx`, shunting any spike above `39.6 V` safely at `≤3.55 V`.

---

## 3. Exact MCU Pin Map (Per Channel × 2: `U1` and `U2`)

Both `U1` (Channel A) and `U2` (Channel B) use **`AT32F421G8U7`** (`QFN-28 4×4 mm`, LCSC **`C2765098`** — the exact package verified in our photo teardown of both Repeat Dual and SNIPE v2.0) wired identically to AM32's **`RR_ROBOT_DUAL_ESC_F421`** target (`HARDWARE_GROUP_AT_C` + `HARDWARE_GROUP_AT_045`):

| `AT32F421G8U7` Pin (QFN-28) | Port / Net Name | AM32 Function | Connection / High-Backvoltage Protection |
| :---: | :--- | :--- | :--- |
| `Pin 9` | `PA2` (`SIG_IN`) | `TMR15_CH1` Input | `S1` (Ch A) or `S2` (Ch B) via `220 Ω` series resistor + `10 kΩ` pull-down + `3.3 V` ESD diode |
| `Pin 20` | `PA10` (`PHASE_A_HI`) | `TIM1_CH3` | `EG6288` `HIN1` |
| `Pin 15` | `PB1` (`PHASE_A_LO`) | `TIM1_CH3N` | `EG6288` `LIN1` |
| `Pin 19` | `PA9` (`PHASE_B_HI`) | `TIM1_CH2` | `EG6288` `HIN2` |
| `Pin 14` | `PB0` (`PHASE_B_LO`) | `TIM1_CH2N` | `EG6288` `LIN2` |
| `Pin 18` | `PA8` (`PHASE_C_HI`) | `TIM1_CH1` | `EG6288` `HIN3` |
| `Pin 13` | `PA7` (`PHASE_C_LO`) | `TIM1_CH1N` | `EG6288` `LIN3` |
| `Pin 7` | `PA0` (`BEMF_A`) | `COMP_INM` | Phase A divider (`22 kΩ` `0603` / `2.2 kΩ`) + **`BAT54S` clamp to `3.3 V`/`GND`** |
| `Pin 11` | `PA4` (`BEMF_B`) | `COMP_INM` | Phase B divider (`22 kΩ` `0603` / `2.2 kΩ`) + **`BAT54S` clamp to `3.3 V`/`GND`** |
| `Pin 12` | `PA5` (`BEMF_C`) | `COMP_INM` | Phase C divider (`22 kΩ` `0603` / `2.2 kΩ`) + **`BAT54S` clamp to `3.3 V`/`GND`** |
| `Pin 8` | `PA1` (`BEMF_NEUTRAL`) | `COMP_INP` | Virtual neutral star: `3× 22 kΩ` from Phases A/B/C + `2.2 kΩ` to `GND` |
| `Pin 10` | `PA3` (`VBAT_ADC`) | `ADC_IN3` | `100 kΩ` to `VBAT`, `10 kΩ` to `GND` + `100 pF` filter + **`BAT54S` clamp (`TARGET_VOLTAGE_DIVIDER = 110`)** |
| `Pin 12/13*` (`PA6`) | `PA6` (`CURR_ADC`) | `ADC_IN6` | `INA180A2` output (`50 V/V` × `1.0 mΩ` = `50 mV/A`, `MILLIVOLT_PER_AMP = 50`; or `INA180A1` for `20 mV/A`) via `100 Ω` + `1 nF` RC filter |
| `Pin 22` | `PB6` (`TLM_TX`) | `USART1_TX` | Exposed telemetry test pad |
| `Pin 23 / 24` | `PA13` / `PA14` | `SWDIO` / `SWCLK` | Exposed 4-pad SWD programming header (`3V3, SWDIO, SWCLK, GND`) per channel |
| `VDD / VDDA` | `3V3_CHx` | Logic & Analog Power | Dedicated `AMS1117-3.3` per channel fed from `10.0 V` buck rail (`100 nF` + `4.7 µF` X7R + `10 Ω` `VDDA` RC filter) |

*(Note: Verify exact QFN-28 pin numbers against the official Artery `AT32F421G8U7` datasheet symbol in EasyEDA/KiCad when placing `C2765098`).*

---

## 4. Overbuilt 100 V-Rated 5 V Receiver BEC Architecture (4-Stage Protection)

```text
VBAT ──┬──► [D2: SMCJ28A 1500W SMC TVS] + [2× 220µF 50V SMD Caps] + [6× 10µF 50V MLCC]
       │
       └──► [D1: SS310 100V 3A Schottky] ──► [FB1: 120Ω Bead] ──┬──► [D3: SMBJ30A 600W TVS]
                                                                ├──► [2× 10µF 50V X7R MLCC]
                                                                └──► [C_BEC_HOLD: 100µF 50V SMD Cap]
                                                                                │
                                                                    [U7: LM5164DDAR (100V, 1A Buck)]
                                                                                │  (5.05 V + Type-3 Ripple Network)
                                                                      ┌─────────┴─────────┐
                                                             [2× 22µF 16V X7R]            │
                                                                      │           [FB2: Low-DCR Bead]
                                                                      │                   │
                                                                     GND          [F1: 500mA PTC Fuse]
                                                                                          │
                                                                                  [D4: SMBJ5.0A Clamp TVS]
                                                                                          │
                                                                       5V_RX ◄──── [External 470µF–1000µF 16V Polymer Cap Pads]
```

### Why This BEC Cannot Be Killed by High Back-Voltage or Brownouts
1. **100 V Input Survivability (`LM5164DDAR` `C477928` + `SS310` `C330484`):** Whereas Repeat's `LMR33620B` has a `38 V` absolute max rating (below the `45.4 V` clamping ceiling of a 6S TVS!), our `LM5164DDAR` and `SS310` input diode are rated to **100 V (`105 V` abs max)** — more than **2.2×** the peak TVS clamping voltage.
2. **6.85 ms Complete-Dropout Brownout Holdup (`D1` `SS310` + `100 µF 50 V` Holdup Reservoir):** If a weapon spin-up or drive stall drags `VBAT` to `0 V` for several milliseconds, `D1` prevents the motor bridges from discharging the BEC's `50 V` holdup island, maintaining uninterrupted `5.05 V` receiver power for **`~6.85 ms`** at `150 mA` load.
3. **Stable External `470 µF – 1000 µF` Receiver Capacitance:** `FB2` decouples the `LM5164`'s local `2× 22 µF` ceramic output caps (with Type-3 ripple injection) from the external `470 µF – 1000 µF 16 V` polymer reservoir cap, giving `<32 mV` droop on sudden `300 mA` ELRS telemetry bursts with zero control-loop oscillation.
4. **Isolated `10.0 V` Gate Drive Supply (`U8` `XL7015E1` `80 V` Buck):** `U8` (`XL7015E1`, `C73013`, `$0.2405`) generates a dedicated **`10.0 V` Gate Drive & Logic Rail** (replacing Repeat's `35 V`-limited `78L08` `8 V` linear regulator). Driving `AGM403A1` MOSFETs at a full `10.0 V` instead of `8.0 V` minimizes $R_{DS(on)}$ (`2.3 mΩ`) and eliminates linear regulator heating on 6S.

---

## 5. Combat-Hardened Mechanical & Cost-Optimized PCB Construction

1. **Plated Through-Hole Edge Solder Tabs + Double-Sided Weapon Passthrough:**
   - Borrow SNIPE v2.0's **gold-plated through-hole edge tabs** (`A, B, C, VBAT, GND, A, B, C`) so `14–18 AWG` silicone wires thread **through** the plated hole before soldering (preventing 100G arena impacts from peeling surface-mount copper pads off the FR-4 laminate).
   - Retain Repeat Dual's **unmasked top & bottom `VBAT`/`GND` passthrough zones** so a weapon ESC and the main battery lead can solder to opposite sides of the same high-current busbar.
2. **Single-Sided SMT Assembly (`~40 × 28 mm`, 4-Layer `1 oz` HASL):**
   - Placing all SMD components on **`L1 (Top)`** cuts JLCPCB Standard PCBA assembly costs (single stencil, single reflow pass, `$1.19/board` PCBA fee) and keeps bare 4-layer `1 oz` HASL PCB cost to **`$0.11/board`** at Qty 500 (see [`BOM_ECONOMICS.md`](file:///home/antigravity/meepmeepme-sls/late-night-am32-dual/BOM_ECONOMICS.md)).
   - `L1 (Top)`: All `12×` `5×6 mm` MOSFETs (`Q1–Q12`), `2×` `RLM25FEER001` shunts, `U1/U2` MCUs, `U3/U4` `EG6288` drivers, `SMCJ28A` TVS, `U7` `LM5164DDAR` (`5 V` BEC), `U8` `XL7015E1` (`10 V` buck), and `2× 220 µF 50 V` SMD bulk caps.
   - `L2 (Inner 1)`: **Unbroken solid `GND` plane** + dedicated Kelvin star ground tie for `INA180A2` and `U7`/`U8`.
   - `L3 (Inner 2)`: Solid `VBAT` bus plane + `10V_DRV` and `5V_SW` routing + stitched phase copper polygons.
   - `L4 (Bottom)`: High-current copper pours (thermal vias under MOSFETs), unmasked `VBAT`/`GND` passthrough zones, and SWD/telemetry test pads.
3. **Conformal Coating & Strain Relief:**
   - Apply acrylic or silicone conformal coating (`MG Chemicals 419D` or `422C`) across all QFN/TSSOP/0603 logic sections after SWD bootloader flashing, and secure the `2× 220 µF 50 V` SMD bulk caps with Neutral-Cure Electronics Silicone before heatshrinking.

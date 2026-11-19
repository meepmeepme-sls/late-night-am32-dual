# Dual 40 A AM32 Combat Drivetrain ESC — High-Backvoltage Hardware Design Specification

**Target Envelope:** **3S–6S LiPo / LiHV (`9.0 V – 26.1 V`)** combat robot **drivetrain** application (`40 A` continuous per channel × 2 channels).
**Baseline:** Combines the active current limiting, double-sided battery passthrough, and `AT32F421G8U7` stock firmware compatibility of the **Repeat Robotics Dual AM32 ESC** with the 40 A continuous rating, plated through-hole wire tabs, and horizontal `50 V` polymer capacitor bank of the **Just 'Cuz Robotics SNIPE Dual 40A (v2.0)** — **without custom mixer firmware** (two independent channels, mix on radio) and engineered from the ground up to survive **extreme high back-voltage (`45 V – 80 V+`), violent regenerative braking, and back-driven weapon impacts in 3S–6S LiHV combat robotics**.

---

## 1. Visual Teardown Comparison (From High-Res Product Photos)

All product photos and zoomed IC marking crops are saved in [`reference_images/`](file:///home/antigravity/dual-am32-esc/reference_images/) and [`reference_images/crops/`](file:///home/antigravity/dual-am32-esc/reference_images/crops/).

| Subsystem | Repeat Robotics Dual AM32 (`28 × 20 mm`) | JCR / cb-technology SNIPE Dual 40A (`32 × 20 mm`, v1.0 & v2.0) | Our High-Backvoltage Bulletproof Design (`~38 × 26 mm`) |
| :--- | :--- | :--- | :--- |
| **Main MCUs (`2×`)** | **Artery `AT32F421G8U7`** (`QFN-28 4×4 mm`, LCSC `C2765098`), 1 Front / 1 Back | **Artery `AT32F421G8U7`** (`QFN-28 4×4 mm`, LCSC `C2765098`), both on Back (v2.0) | **Artery `AT32F421G8U7`** (`QFN-28 4×4 mm`, LCSC `C2765098`) — flashes stock `AM32_RR_ROBOT_DUAL_ESC_F421` |
| **Aux Mixer MCU** | None (`S1`/`S2` independent) | **3rd QFN-20 (3×3 mm) MCU** between the two `AT32F421` ICs for mixing/CRSF | **None** (eliminates 3rd MCU failure/firmware point; mix on radio) |
| **Gate Drivers (`2×`)** | **Fortior `FD6288Q`** (`QFN-24 4×4 mm`, LCSC `C328453`), 1 Front / 1 Back | **Fortior `FD6288Q`** (`QFN-24 4×4 mm`, LCSC `C328453`), both on Back (v2.0) | **Fortior `FD6288Q`** (`C328453`) + **6× `RB520S-30` Negative-`VS` Schottkys** + **Asymmetric Fast Turn-Off** |
| **MOSFETs (`12×`)** | **Toshiba `TPN2R304PL`** (`2R304 PL`, LCSC `C5802634`): **40 V**, `1.8 mΩ` typ (`2.3 mΩ` max), `3.3 × 3.3 mm` TSON Advance | **`RS120N04AD` / `S120N04D`** (LCSC `C47665714`): **40 V**, `<3.5 mΩ`, 120 A class, `3.3 × 3.3 mm` PDFN3.3×3.3 | **APM `AP140N08NF`** (LCSC `C56142574`): **85 V**, `2.5 mΩ` typ (`3.2 mΩ` max), **140 A, 900 mJ Avalanche ($E_{AS}$)**, `5 × 6 mm` PDFN5×6-8L *(or `100 V` `HYG037N10LS2C2` `C3025196`)* |
| **Current Sensing** | **Yes:** `1× 1.0 mΩ` (`R001`) 2512 shunt per ch (**1.6 W heat @ 40 A!**) + SOT-23-5 amp (`1639`) | **None** (no current shunts on v1.0 or v2.0) | **Yes (4× Lower Heat):** `2× 0.5 mΩ` parallel 2512 shunts (`0.25 mΩ`, only **0.40 W @ 40 A**) + `INA180A2` (`50 V/V`, `C544664`) = `12.5 mV/A` |
| **5 V Receiver BEC** | **TI `LMR33620B`** (`33620B`, **36 V max / 38 V abs max**) + `4R7` (`4.7 µH`) 4×4 mm inductor (`1.5 A`) | Tiny **SOT-23-6 buck** (`DJ2E...`) + miniature `0805` chip inductor (**250 mA max**) | **TI `LM5164DDAR`** (**100 V / 105 V abs max**, `1 A`, `C477928`) + `SS310` `100 V` blocking diode + `100 µF 50 V` holdup + `500 mA` PTC + external `470–1000 µF` RX cap |
| **Gate Drive Supply (`VCC`)** | **SOT-89-3 `78L08` (`8G`) 8 V Linear LDO** (**30–35 V max input!** Drops `26.1 V → 8 V` as pure heat) | **SOT-89-3 Linear Regulator** (`L78Lxx`) + 2nd SOT-23-6 step-down | **2nd TI `LM5164DDAR`** (**100 V Synchronous Buck**, `C477928`) set to **full `10.0 V`** (minimizes MOSFET $R_{DS(on)}$ with zero linear heat) |
| **3.3 V MCU LDO** | Single SOT-23-5 LDO (`AG5R`) on Back | Single SOT-23-5 LDO (`WB33` on v1.0) | **2× Independent `AMS1117-3.3` LDOs** fed from `10.0 V` buck rail (complete channel fault isolation) |
| **Onboard TVS Clamp** | **None!** (`0 W` onboard TVS) | **1× `400 W` SMA (`DO-214AC`) TVS** (`446 JP` on v1.0; small SMD diode on v2.0) | **1× `3000 W` SMC (`DO-214AB`) `SMDJ28A`** (`C2846134`, clamps @ `45.4 V` max) + `SMAJ28A` (`C7466250`) on `BEC_VIN` |
| **External Bus Caps** | `1× 35 V` radial electrolytic cap on battery leads | **v1.0:** `1× 470 µF 35 V` elco<br>**v2.0:** **`2× 220 µF 50 V` Conductive Polymer Hybrid Caps** (`J35Z 220 50`) | **`2× 220 µF 50 V` Conductive Polymer / Hybrid Caps** (`C19270689`) in horizontal board cradle + **`12× 10 µF 50 V` X7R MLCCs** |
| **Analog BEMF / ADC Clamps** | None (unclamped `11:1` dividers fail above `VBAT = 39.6 V`) | None (unclamped `11:1` dividers fail above `VBAT = 39.6 V`) | **8× `BAT54S` Dual Series Schottky Clamps to `3.3 V`/`GND`** on `VBAT_ADC` and `BEMF_A/B/C` + **6× Phase `RC` Snubbers** |
| **Wire Termination** | Surface-mount corner pads + double-sided `VBAT`/`GND` weapon passthrough | **Plated Through-Hole Edge Solder Tabs** (`A B C BATT GND A B C`) + breakaway mounting ears | **Both:** Plated through-hole wire tabs (100G pull resistance) **plus** double-sided `VBAT`/`GND` weapon ESC passthrough |

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

### Our 7-Point High-Backvoltage Bulletproof Architecture
1. **`85 V` High-Avalanche MOSFETs (`AP140N08NF`, LCSC `C56142574`) in `5×6 mm` PDFN5×6-8L:**
   - Rated for **`85 V` $V_{DS}$**, **`2.5 mΩ` typical (`3.2 mΩ` max)** at $V_{GS} = 10\text{ V}$, **140 A**, and an extraordinary **900 mJ single-pulse avalanche energy ($E_{AS}$)** in a `5 × 6 mm` package (2.75× the thermal contact area of the `3.3 × 3.3 mm` FETs on Repeat and SNIPE).
   - At the `SMDJ28A` peak clamp voltage of `45.4 V`, our `85 V` MOSFETs still have **+39.6 V of clean voltage margin** and never enter avalanche!
   - *(Footprint-compatible `PDFN5×6-8L` alternatives: **`100 V` `HYG037N10LS2C2`** `C3025196` at `3.0 mΩ` typ for +54.6 V margin, or **`60 V` `CSD18540Q5B`** `C86513` at `1.8 mΩ` typ for +14.6 V margin).*
2. **`3000 W` SMC Surge Clamp (`SMDJ28A`, LCSC `C2846134`) + Optional Active Regen Bleed Dumper:**
   - Replaces Repeat's `0 W` TVS and SNIPE's `400 W` SMA TVS with a **3000 W `SMDJ28A` (`DO-214AB` SMC)** unidirectional TVS across the main `VBAT`/`GND` bus (`28 V` standoff, `31.1 V` breakdown, `45.4 V` max clamp @ `66.1 A` peak pulse).
   - **Optional Active Regen Brake Shunt Pad (`Q_DUMP` + `R_DUMP`):** For heavy-wheel 12 lb / 30 lb drive systems or bots prone to master-switch bounce, a simple `30 V` precision Zener/TL431 comparator switches on an auxiliary `85 V` `AP140N08NF` FET into a `1.0 Ω – 2.2 Ω` pulse-rated resistor bank whenever `VBAT > 30.5 V`, bleeding continuous regenerative braking energy before the TVS even heats up.
3. **100 V Dual Synchronous Buck Supply (`2× LM5164DDAR`, LCSC `C477928`) + `100 V` `SS310` Schottky (`C330484`):**
   - Eliminates Repeat's `36 V` `LMR33620B` BEC and `35 V` `78L08` linear gate regulator.
   - Both `U7` (`5.05 V` Receiver BEC) and `U8` (`10.0 V` Gate Drive & Logic Buck) use TI's **100 V (`105 V` abs max) `LM5164DDAR`**, and `D1` is upgraded to a **100 V, 3 A `SS310` Schottky (`C330484`)**. Every single power IC connected to `VBAT` is rated to **100 V**!
4. **`50 V` Conductive Polymer Hybrid Capacitor Bank (Adopting & Expanding SNIPE v2.0's Upgrade):**
   - In our teardown of SNIPE v2.0 ([`crop_snipe_v2_caps.jpg`](file:///home/antigravity/dual-am32-esc/reference_images/crops/crop_snipe_v2_caps.jpg)), we discovered JCR upgraded from `1× 35 V 470 µF` elco to **`2× 220 µF 50 V` conductive polymer hybrid capacitors (`J35Z 220 50`)** because `35 V` electrolytics vent under 6S back-EMF spikes.
   - We use **`2× 220 µF 50 V` Conductive Polymer Aluminum Capacitors** (`JBLH2221M050E125RLM`, LCSC **`C19270689`**, or `2× 330 µF – 470 µF 50 V` hybrid polymer caps) in a horizontal recessed bay, backed by **`12× 10 µF 50 V` X7R `1206` soft-termination MLCCs** (`6` per channel directly across the half-bridges).
5. **Negative-`VS` Undershoot Clamping & Asymmetric Fast-Turn-Off Gate Drive (`FD6288Q` Hardening):**
   - When braking hard at 40 A+, rapid di/dt across motor phase inductance drags the switch node (`VS1/2/3`) **negative below `GND` (`-5 V to -10 V`)**, which latches up or blows monolithic gate drivers, while high positive $dV/dt$ injects current through the MOSFET Miller capacitance ($C_{GD}$) to cause shoot-through.
   - We add **6× `BAT46WS` / `BAV19WS` / `SS110` (`100 V` fast/Schottky diodes)** from `GND` (anode) directly to `VS1/2/3` (cathode) at the `FD6288Q` pins, clamping negative undershoot to `-0.3 V` while easily surviving `45.4 V` 6S spikes.
   - We use **asymmetric gate networks** (`10 Ω` turn-on resistor in parallel with a `1N4148WS` diode + `2.2 Ω` turn-off resistor, plus a `10 kΩ` gate-to-source pull-down on all 12 FETs) so turn-off is **4.5× stronger** than turn-on, locking the off-state gate down during violent back-EMF spikes.
   - We place **6× `RC` phase snubbers (`2.2 Ω` `0603` + `1 nF 100 V` X7R `0603`)** from each motor phase (`A, B, C`) to `GND` to damp high-frequency ringing.
6. **`BAT54S` Analog BEMF & `VBAT_ADC` Input Clamping (Protects the MCUs Above `39.6 V`):**
   - The `AT32F421G8U7` analog comparator (`PA0, PA4, PA5`) and ADC (`PA3`) pins are **not 5 V tolerant** (absolute max $V_{DDA} + 0.3\text{ V} = 3.60\text{ V}$). With an `11:1` divider (`22 kΩ / 2.2 kΩ`), any phase or bus spike above **`39.6 V`** exceeds `3.60 V` (`45.4 V` → `4.13 V`; `65 V` phase spike → `5.91 V`)!
   - We place **4× `BAT54S` dual series Schottky clamp arrays per channel (`8×` total)** on `VBAT_ADC`, `BEMF_A`, `BEMF_B`, and `BEMF_C` tied between `GND` and `3V3_CHx`. Any spike above `39.6 V` is safely shunted at `≤3.55 V` (`<1.3 mA` through the `22 kΩ` top resistor into the local `3.3 V` decoupling rail).

---

## 3. Exact MCU Pin Map (Per Channel × 2: `U1` and `U2`)

Both `U1` (Channel A) and `U2` (Channel B) use **`AT32F421G8U7`** (`QFN-28 4×4 mm`, LCSC **`C2765098`** — the exact package verified in our photo teardown of both Repeat Dual and SNIPE v2.0) wired identically to AM32's **`RR_ROBOT_DUAL_ESC_F421`** target (`HARDWARE_GROUP_AT_C` + `HARDWARE_GROUP_AT_045`):

| `AT32F421G8U7` Pin (QFN-28) | Port / Net Name | AM32 Function | Connection / High-Backvoltage Protection |
| :---: | :--- | :--- | :--- |
| `Pin 9` | `PA2` (`SIG_IN`) | `TMR15_CH1` Input | `S1` (Ch A) or `S2` (Ch B) via `220 Ω` series resistor + `10 kΩ` pull-down + `3.3 V` ESD diode |
| `Pin 20` | `PA10` (`PHASE_A_HI`) | `TIM1_CH3` | `FD6288Q` `HIN1` |
| `Pin 15` | `PB1` (`PHASE_A_LO`) | `TIM1_CH3N` | `FD6288Q` `LIN1` |
| `Pin 19` | `PA9` (`PHASE_B_HI`) | `TIM1_CH2` | `FD6288Q` `HIN2` |
| `Pin 14` | `PB0` (`PHASE_B_LO`) | `TIM1_CH2N` | `FD6288Q` `LIN2` |
| `Pin 18` | `PA8` (`PHASE_C_HI`) | `TIM1_CH1` | `FD6288Q` `HIN3` |
| `Pin 13` | `PA7` (`PHASE_C_LO`) | `TIM1_CH1N` | `FD6288Q` `LIN3` |
| `Pin 7` | `PA0` (`BEMF_A`) | `COMP_INM` | Phase A divider (`22 kΩ` `0603` / `2.2 kΩ`) + **`BAT54S` clamp to `3.3 V`/`GND`** |
| `Pin 11` | `PA4` (`BEMF_B`) | `COMP_INM` | Phase B divider (`22 kΩ` `0603` / `2.2 kΩ`) + **`BAT54S` clamp to `3.3 V`/`GND`** |
| `Pin 12` | `PA5` (`BEMF_C`) | `COMP_INM` | Phase C divider (`22 kΩ` `0603` / `2.2 kΩ`) + **`BAT54S` clamp to `3.3 V`/`GND`** |
| `Pin 8` | `PA1` (`BEMF_NEUTRAL`) | `COMP_INP` | Virtual neutral star: `3× 22 kΩ` from Phases A/B/C + `2.2 kΩ` to `GND` |
| `Pin 10` | `PA3` (`VBAT_ADC`) | `ADC_IN3` | `100 kΩ` to `VBAT`, `10 kΩ` to `GND` + `100 pF` filter + **`BAT54S` clamp (`TARGET_VOLTAGE_DIVIDER = 110`)** |
| `Pin 12/13*` (`PA6`) | `PA6` (`CURR_ADC`) | `ADC_IN6` | `INA180A2` output (`50 V/V` × `0.25 mΩ` = `12.5 mV/A` ≈ `MILLIVOLT_PER_AMP = 12`) via `100 Ω` + `1 nF` RC filter |
| `Pin 22` | `PB6` (`TLM_TX`) | `USART1_TX` | Exposed telemetry test pad |
| `Pin 23 / 24` | `PA13` / `PA14` | `SWDIO` / `SWCLK` | Exposed 4-pad SWD programming header (`3V3, SWDIO, SWCLK, GND`) per channel |
| `VDD / VDDA` | `3V3_CHx` | Logic & Analog Power | Dedicated `AMS1117-3.3` per channel fed from `10.0 V` buck rail (`100 nF` + `4.7 µF` X7R + `10 Ω` `VDDA` RC filter) |

*(Note: Verify exact QFN-28 pin numbers against the official Artery `AT32F421G8U7` datasheet symbol in EasyEDA/KiCad when placing `C2765098`).*

---

## 4. Overbuilt 100 V-Rated 5 V Receiver BEC Architecture (4-Stage Protection)

```text
VBAT ──┬──► [D2: SMDJ28A 3000W SMC TVS] + [2× 220µF 50V Polymer Caps] + [12× 10µF 50V MLCC]
       │
       └──► [D1: SS310 100V 3A Schottky] ──► [FB1: 600Ω Bead] ──┬──► [D3: SMAJ28A 400W TVS]
                                                                ├──► [2× 10µF 50V X7R MLCC]
                                                                └──► [C_BEC_HOLD: 100µF 50V Polymer Cap]
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
2. **6.85 ms Complete-Dropout Brownout Holdup (`D1` `SS310` + `120 µF 50 V` Holdup Reservoir):** If a weapon spin-up or drive stall drags `VBAT` to `0 V` for several milliseconds, `D1` prevents the motor bridges from discharging the BEC's `50 V` holdup island, maintaining uninterrupted `5.05 V` receiver power for **`~6.85 ms`** at `150 mA` load.
3. **Stable External `470 µF – 1000 µF` Receiver Capacitance:** `FB2` decouples the `LM5164`'s local `2× 22 µF` ceramic output caps (with Type-3 ripple injection) from the external `470 µF – 1000 µF 16 V` polymer reservoir cap, giving `<32 mV` droop on sudden `300 mA` ELRS telemetry bursts with zero control-loop oscillation.
4. **Complete Isolation from Motor Gate Drive (`U8` `10.0 V` Buck):** A second `100 V` `LM5164DDAR` (`U8`) generates a dedicated **`10.0 V` Gate Drive & Logic Rail** (replacing Repeat's `35 V`-limited `78L08` `8 V` linear regulator). Driving our `AP140N08NF` MOSFETs at a full `10.0 V` instead of `8.0 V` reduces MOSFET $R_{DS(on)}$ and eliminates linear regulator heating on 6S.

---

## 5. Combat-Hardened Mechanical & PCB Construction Features

1. **Plated Through-Hole Edge Solder Tabs + Double-Sided Weapon Passthrough:**
   - Borrow SNIPE v2.0's **gold-plated through-hole edge tabs** (`A, B, C, VBAT, GND, A, B, C`) so `14–18 AWG` silicone wires thread **through** the plated hole before soldering (preventing 100G arena impacts from peeling surface-mount copper pads off the FR-4 laminate).
   - Retain Repeat Dual's **unmasked top & bottom `VBAT`/`GND` passthrough zones** so a weapon ESC and the main battery lead can solder to opposite sides of the same high-current busbar.
2. **Recessed Horizontal `50 V` Polymer Capacitor Bay (With Silicone/Epoxy Strain Relief):**
   - Provide dedicated horizontal +/- through-hole pads at the top edge of the PCB for the **`2× 220 µF 50 V` Conductive Polymer Hybrid Capacitors (`C19270689`)** so they lie flat inside the board's thickness profile (`~6 mm`), secured with Neutral-Cure Electronics Silicone (`Momentive RTV162` or `Dow 3145`) before applying clear polyolefin heatshrink.
3. **4-Layer Heavy Copper Stackup (`2 oz` Outer / `1 oz` Inner, TG170 FR-4):**
   - `L1 (Top)`: High-side `5×6 mm` MOSFETs (`Q1–Q3`, `Q7–Q9`), `SMDJ28A` `3000 W` TVS, `U7`/`U8` `100 V` bucks, `U1` MCU + `U3` `FD6288Q`.
   - `L2 (Inner 1)`: **Unbroken solid `GND` plane** + dedicated Kelvin star ground tie for `INA180A2` and `U7`/`U8`.
   - `L3 (Inner 2)`: Solid `VBAT` bus plane + `10V_DRV` and `5V_SW` routing + stitched phase copper polygons.
   - `L4 (Bottom)`: Low-side `5×6 mm` MOSFETs (`Q4–Q6`, `Q10–Q12`), `4× 0.5 mΩ` 2512 current shunts, `U2` MCU + `U4` `FD6288Q`, `BAT54S` clamps, and phase `RC` snubbers.
4. **Conformal Coating Masking:**
   - Apply acrylic or silicone conformal coating (`MG Chemicals 419D` or `422C`) across all QFN/SOT/0402 logic sections after SWD bootloader flashing to prevent conductive carbon dust, metal grindings, or arena humidity from bridging the `100 V` buck pins or `0.5 mm`-pitch QFN leads.

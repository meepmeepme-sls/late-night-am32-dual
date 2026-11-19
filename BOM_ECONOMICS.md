# Late Night AM32 Dual — Qty-500 Costed BOM & Unit Economics

**Target:** Match the **~$40.00 MSRP** of the JCR SNIPE Dual 40A at **500-unit production volume** while achieving **≥ 60% landed gross margin** (**≤ $16.00 landed COGS**), **without compromising the 100 V-rated 5 V Receiver BEC**.

> [!NOTE]
> **Pricing Basis:** Component unit prices and stock counts below were verified directly against JLCPCB/LCSC part pages at **Qty 500-board** volume breaks (`500×` to `6,000×` parts depending on per-board quantity). Bare PCB, JLCPCB Standard PCBA assembly fees, and logistics/tariffs/packaging are modeled transparently and labeled where estimated.

---

## 1. Executive Economics Summary (Qty = 500 Units)

| Cost / Margin Metric | Per-Unit ($) | 500-Unit Total ($) | Notes |
| :--- | :---: | :---: | :--- |
| **Verified LCSC Components (26 line items)** | `$7.91` | `$3,957.10` | Exact LCSC/JLCPCB Qty-500 tier pricing |
| **Misc. Basic 0603 Passives & LEDs (est.)** | `$0.05` | `$25.00` | ~28 Basic 0603 parts (`10 Ω`, `2.2 kΩ`, `100 kΩ`, `1 nF`, LEDs) |
| **Total BOM Components** | **`$7.96`** | **`$3,982.10`** | Down from >$48+/board in initial 85 V/FD6288Q spec |
| **JLCPCB Standard PCBA Assembly Fees** | `$1.19` | `$596.31` | Single-sided SMT, setup, stencil, fixture, feeders, joints, X-ray |
| **Bare PCB (4-Layer, 1 oz HASL, 40 × 28 mm)** | `$0.11` | `$57.30` | `$65.67/m²` + `$20.52` engineering fee (`0.00112 m²/board`) |
| **Ex-Works PCBA Unit Cost** | **`$9.26`** | **`$4,635.71`** | Ready for flash/test/finish |
| **Estimated Landed Extras** *(est.)* | `$2.30` | `$1,150.00` | Air freight (`~$0.60`), tariff/duty (`~$1.20`), heatshrink/coat/pack (`~$0.50`) |
| **Total Estimated Landed COGS** | **`$11.56`** | **`$5,785.71`** | **`$4.44/unit` headroom** below `$16.00` (60% margin ceiling) |
| **Gross Profit @ `$40.00` MSRP** | **`$28.44`** | **`$14,214.29`** | **71.1% Gross Margin** (exceeds 60% target by +11.1 pts) |

---

## 2. Where We Cost-Optimized vs. What We Refused to Cut

The combat robotics market already accepts the 6S drivetrain performance of the **Repeat Dual** (`40 V` FETs) and **JCR SNIPE** (`40 V` FETs, no current sensing, `400 W` SMA TVS) — *except* for their weak `36 V` / `250 mA` `5 V` receiver BECs. We therefore kept the **bulletproof 100 V `5 V` RX BEC** intact and cut cost everywhere else:

### A. Justified Cost-Downs ("Inferior" to Overbuilt 85V Spec, Still ≥ Market)
1. **MOSFETs (`12×`): `85 V` `AP140N08NF` → `40 V` `AGM403A1` (`$0.1846/ea`, `$2.22/board`)**
   - Saves **~$35+/board** vs. high-cost `TI CSD18540Q5B` (`$3.27/ea`) or unstocked `AP140N08NF`.
   - Matches the `40 V` voltage class used by Repeat Dual and JCR SNIPE, **but retains the larger `5 × 6 mm` PDFN-8 package** (`2.3 mΩ` typ @ `10 V`, `2.75×` larger thermal pad than their `3.3 × 3.3 mm` FETs).
   - *Drop-in `60 V` upgrade:* **`DON120N06`** (`C41384268`, `60 V`, `3.5 mΩ`, **`$0.1846/ea` @ 1,000+**) — identical per-unit cost if `60 V` margin above `SMCJ28A` is preferred over `2.3 mΩ` vs. `3.5 mΩ` $R_{DS(on)}$.
2. **Gate Drivers (`2×`): `FD6288Q` (`$2.37/ea`, OOS) → `EG6288` (`$0.2101/ea`, `$0.42/board`)**
   - Saves **~$4.32/board** and eliminates QFN-24 stockouts/X-ray.
   - Verified `EG6288` specs: `220 V`, 3-phase, `+1.8 A / -2.3 A` drive, `200 ns` deadtime, `5–20 V` `VCC`, `2.5 V` logic high, **integrated bootstrap diodes** (eliminating `6×` external bootstrap diodes), leaded `TSSOP-20`.
3. **10 V Gate Rail (`U8`): 2nd `LM5164DDAR` (`$1.58`) → `XL7015E1` (`$0.2405`)**
   - Saves **$1.34/board**. `XL7015E1` (`TO-252-5`) is an **`80 V`, `0.8 A` buck** — vastly superior to Repeat's `35 V` `78L08` linear LDO (`$0.023`), while costing 6.5× less than a second `LM5164DDAR`.
4. **Main VBAT TVS (`D2`): `3000 W` `SMDJ28A` (OOS) → `1500 W` `SMCJ28A` (`$0.0519`)**
   - Still **3.75× larger** than JCR SNIPE's `400 W` SMA TVS and infinity larger than Repeat's `0 W` (none).
5. **Current Shunts (`2×` total vs. `4×`): `2× 0.5 mΩ` parallel/ch → `1× 1.0 mΩ` `RLM25FEER001` (`$0.0403/ea`)**
   - Halves shunt count and cost (`$0.08/board` total). With `INA180A2` (`50 V/V`), `1 mΩ × 50 = 50 mV/A` (`66 A` full-scale @ `3.3 V` ADC; set AM32 `MILLIVOLT_PER_AMP = 50`, or swap to `INA180A1` `20 V/V` for `20 mV/A` / `165 A` full-scale).
6. **Bus MLCCs (`12×` → `6×`): `6× 10 µF 50 V` `1206` X7R (`$0.1205/ea`)**
   - Saves **$0.72/board** while keeping `3× 10 µF` ceramic decoupling right across each channel's half-bridges, backed by `2× 220 µF 50 V` SMD polymer caps.
7. **Single-Sided SMT + 4-Layer `1 oz` HASL PCB**
   - Eliminates double-sided PCBA fixture/reflow costs and `2 oz` copper surcharges (`$0.11/board` bare PCB vs. `>$0.60/board` for `2 oz`).

### B. What We Refused to Cut (The Bulletproof `5 V` Receiver BEC)
- **`U7`: TI `LM5164DDAR`** (`C477928`, **`$1.5781`**) — `100 V` (`105 V` abs max), `1 A` synchronous buck.
- **`D1`: `SS310`** (`C330484`, **`$0.0493`**) — `100 V`, `3 A` holdup isolation Schottky.
- **`C_BEC_HOLD`: `CK1H101M-CRE77`** (`C42389919`, **`$0.0398`**) — `100 µF 50 V` SMD polymer holdup cap (`~6.85 ms` complete-dropout holdup).
- **`F1`: `nSMD050-33V`** (`C70077`, **`$0.0429`**) + **`D4`: `SMBJ5.0A`** (`C2758500`, **`$0.0311`**) — `500 mA` PTC short-circuit protection + `5.0 V` output clamp.
- **`D_CLAMP1-8`: `8× BAT54S`** (`C699095`) + **`D_VS1-6`: `6× RB520S-30`** (`C7502701`) — keeps MCU analog pins and gate drivers alive during back-EMF hits.

---

## 3. Itemized Verified BOM (500-Board Production Run)

| Designator | Qty/Bd | Total (500 bds) | MPN | LCSC # | Type | Stock Observed | Unit ($) | Ext/Bd ($) | 500-Bd ($) |
| :--- | :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| `U1, U2` | 2 | 1,000 | `AT32F421G8U7` | `C2765098` | Ext | 8,292 | `$0.4680` | `$0.9360` | `$468.00` |
| `U3, U4` | 2 | 1,000 | `EG6288` | `C54102120` | Ext | 3,985 | `$0.2101` | `$0.4202` | `$210.10` |
| `Q1–Q12` | 12 | 6,000 | `AGM403A1` *(Note 1)* | `C5184861` | Ext | 4,580 | `$0.1846` | `$2.2152` | `$1,107.60` |
| `R_SH1, R_SH2` | 2 | 1,000 | `RLM25FEER001` | `C316227` | Ext | 4,824 | `$0.0403` | `$0.0806` | `$40.30` |
| `U5, U6` | 2 | 1,000 | `INA180A2IDBVR` | `C192764` | Ext | 99,735 | `$0.1030` | `$0.2060` | `$103.00` |
| `U7` | 1 | 500 | `LM5164DDAR` | `C477928` | Ext | In stock | `$1.5781` | `$1.5781` | `$789.05` |
| `U8` | 1 | 500 | `XL7015E1` | `C73013` | Ext | 52,380 | `$0.2405` | `$0.2405` | `$120.25` |
| `U9, U10` | 2 | 1,000 | `AMS1117-3.3` | `C6186` | **Basic** | 1,415,767 | `$0.1141` | `$0.2282` | `$114.10` |
| `D1` | 1 | 500 | `SS310` | `C330484` | Ext | In stock | `$0.0493` | `$0.0493` | `$24.65` |
| `D2` | 1 | 500 | `SMCJ28A` | `C20883365` | Ext | 3,291 | `$0.0519` | `$0.0519` | `$25.95` |
| `D3` | 1 | 500 | `SMBJ30A` *(Note 2)* | `C3009993` | Ext | 248 | `$0.0324` | `$0.0324` | `$16.20` |
| `D4` | 1 | 500 | `SMBJ5.0A` | `C2758500` | Ext | 46,134 | `$0.0311` | `$0.0311` | `$15.55` |
| `F1` | 1 | 500 | `nSMD050-33V` | `C70077` | Ext | 130,259 | `$0.0429` | `$0.0429` | `$21.45` |
| `FB1, FB2` | 2 | 1,000 | `BLM18PG121SN1D` | `C14709` | **Basic** | 1,678,698 | `$0.0105` | `$0.0210` | `$10.50` |
| `L1, L2` | 2 | 1,000 | `PNLS5040-150M` | `C2849502` | Ext | 1,828 | `$0.0473` | `$0.0946` | `$47.30` |
| `C_VBAT_EXT1–2` | 2 | 1,000 | `XT220UF50V90RV0078` | `C2992609` | Ext | 26,753 | `$0.1332` | `$0.2664` | `$133.20` |
| `C_VBAT1–6` | 6 | 3,000 | `CL31B106KBHNNNE` | `C89632` | Ext | 648,123 | `$0.1205` | `$0.7230` | `$361.50` |
| `C_BEC_HOLD` | 1 | 500 | `CK1H101M-CRE77` | `C42389919` | Ext | 4,946 | `$0.0398` | `$0.0398` | `$19.90` |
| `C_BEC_OUT1–2` | 2 | 1,000 | `CGA1206X7R226K160NT` | `C6119995` | Ext | 3,831 | `$0.0876` | `$0.1752` | `$87.60` |
| `D_VS1–6` | 6 | 3,000 | `RB520S-30` | `C7502701` | Ext | 19,190 | `$0.0146` | `$0.0876` | `$43.80` |
| `D_GOFF1–12` | 12 | 6,000 | `1N4148WS` | `C2128` | **Basic** | 4,061,545 | `$0.0077` | `$0.0924` | `$46.20` |
| `D_CLAMP1–8` | 8 | 4,000 | `BAT54S` | `C699095` | Ext | In stock | `$0.0196` | `$0.1568` | `$78.40` |
| `C_BOOT/DEC` | 14 | 7,000 | `CC0603KRX7R9BB104` | `C14663` | **Basic** | 34.6M | `$0.0037` | `$0.0518` | `$25.90` |
| `R_10k` | 16 | 8,000 | `0603WAF1002T5E` | `C25804` | **Basic** | 44.8M | `$0.0014` | `$0.0224` | `$11.20` |
| `R_22k` | 12 | 6,000 | `0603WAF2202T5E` | `C31850` | **Basic** | In stock | `$0.0026` | `$0.0312` | `$15.60` |
| `R_2R2` | 18 | 9,000 | `0603WAF220KT5E` | `C22939` | **Basic** | In stock | `$0.0022` | `$0.0396` | `$19.80` |
| *Misc. Basic 0603* | ~28 | ~14,000 | `10Ω`, `2.2kΩ`, `100kΩ`, `1nF`, LEDs | Basic | **Basic** | — | `~$0.0018` | `~$0.0500` | `~$25.00` |
| **TOTAL** | **~158** | **~79,000** | — | — | — | — | — | **`$7.96`** | **`$3,982.10`** |

> [!IMPORTANT]
> **Stock & Pre-Order Notes:**
> 1. **`AGM403A1` (`C5184861`)**: `4,580` in stock vs. `6,000` required for 500 boards. Pre-order/reel restock via JLCPCB Parts Manager, or split/substitute with `60 V` **`DON120N06`** (`C41384268`, `3,554` in stock, identical `$0.1846` price).
> 2. **`SMBJ30A` (`C3009993`)**: `248` in stock vs. `500` required; restock or swap to stocked `SMBJ28A` / `SMCJ30A` (`C408374`, `7,098` in stock, `$0.1077`).

---

## 4. JLCPCB Bare PCB + Standard PCBA Fee Breakdown (Qty = 500)

| Fee Category | Formula / Basis | 500-Unit Total ($) | Per-Board ($) |
| :--- | :--- | :---: | :---: |
| **Bare PCB (4-Layer, 1 oz, HASL)** | `40 × 28 mm` (`0.00112 m²/bd` × 500 = `0.56 m²`) @ `$65.67/m²` + `$20.52` eng | `$57.30` | `$0.1146` |
| **PCBA Setup Fee** | Standard PCBA fixed setup | `$25.56` | `$0.0511` |
| **SMT Stencil** | Single-sided stainless stencil | `$8.21` | `$0.0164` |
| **Fixture / Jig** | Panelized assembly tooling | `$164.18` | `$0.3284` |
| **Feeder / Reel Loading** | `27` unique parts × `$1.53` (conservative; Basic parts often `$0`) | `$41.31` | `$0.0826` |
| **SMT Solder Joints** | `~357` joints/bd × 500 × `$0.0013/joint` | `$232.05` | `$0.4641` |
| **QFN/DFN X-Ray Inspection** | `500` boards × `$0.25/board` | `$125.00` | `$0.2500` |
| **Total PCB + PCBA Processing** | — | **`$653.61`** | **`$1.3072`** |

---

## 5. MSRP & Gross Margin Sensitivity (Target ≥ 60%)

At **Landed COGS = `$11.56/unit`** (`$9.26` ex-works + `$2.30` est. freight/tariff/packaging):

| Target MSRP | Gross Profit / Unit | Gross Margin (%) | vs. 60% Target | Positioning |
| :---: | :---: | :---: | :---: | :--- |
| **`$35.00`** | `$23.44` | `67.0%` | **+7.0 pts** | Undercuts SNIPE by `$5` |
| **`$38.00`** | `$26.44` | `69.6%` | **+9.6 pts** | Aggressive combat-bot pricing |
| **`$40.00`** | **`$28.44`** | **`71.1%`** | **+11.1 pts** | **Target MSRP (Matches JCR SNIPE)** |
| **`$42.00`** | `$30.44` | `72.5%` | **+12.5 pts** | Premium BEC positioning |
| **`$45.00`** | `$33.44` | `74.3%` | **+14.3 pts** | High-margin buffer |

### Optional Further Cost-Downs (If Needed)
- **Drop Current Sensing (`R_SH1-2` + `U5-6`)**: Matches JCR SNIPE (which has no current shunts) and saves **`~$0.30/board`** (`$150` per 500).
- **Eliminate QFN/DFN X-Ray (`-$0.25/board`)**: Swap `AT32F421G8U7` (`QFN-28`) → **`AT32F421K8T7`** (`C3029575`, `LQFP-32 7×7 mm`, `$0.4696` @ 1,000+) and `AGM403A1` (`PDFN-8`) → **`LWN4007A4`** (`C54221215`, `TO-252`, `40 V`, `3.7 mΩ`, `$0.1404` @ 5,000+) or **`AP90N04K`** (`C5198074`, `TO-252`, `$0.1126` @ 5,000+) — saves `~$0.78–$1.11/board` in FET + X-ray cost at the expense of a slightly larger PCB.

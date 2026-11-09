# Reference Schematic/BOM — v0.1 (v1.4-style, UNVERIFIED)

**Status:** Working reference for design capture. **NOT verified against official Fulltone documentation.** Values/refdes below are derived from cross-checking opened sources (primarily S3 zadvitsky walkthrough; topology S1/S2). **Do not fabricate missing values** — confirm before netlist generation (D001 gate).

## Deviations from typical OCD reference
- Supply: **5–18V DC** (C002, D002 risk) — reference designs commonly 9V/9–18V.
- Unbranded v0.1 (C001).
- **D003 (most-available default):** versatile clipping pads; default option may use **BAT46-class Schottky** (or other common) in place of/alongside selected Ge; Ge optional. *Character differs from 1N34A — document/measure.* Floating-Vref topology preserved.

## Block-level BOM (values confirmed from S3 text where stated; others TBD)

| Ref (S3 naming where given) | Block | Value / Part | Source/note | Verified? |
|---|---|---|---|---|
| D1 | Reverse polarity | diode (type TBD) | S3 mentions protection diode | no |
| C1 | Power bulk filter | electrolytic TBD | S3 | no |
| C2 | Power HF filter | film/small TBD (parallel to C1) | S3 | no |
| R1, R2 | Vref divider | equal values TBD (example 100k/100k = C008 calc only) | S3 | no |
| C? (Vref filter) | Vref bypass | TBD (S2 mentions R4,R7,C5 in their analysis) | S2/S3 naming differs | no |
| C5 | Input coupling | TBD | S3 | no |
| R5 | Input reference to ground | TBD | S3 | no |
| R3 | Op-amp input series | TBD | S3 | no |
| R4 | Bias to Vref | TBD | S3 | no |
| U1A | Gain stage 1 | TL082 (1/2) | S1–S3; D002 risk at 5V | part ID yes, pinout no |
| Drive pot | Variable gain | 1M (S3 example for v1.4-era gain calc context) | S3: "gain pot (1M)+R8 and R5..." / "Drive pot (1M)+R8" in S2 text; verify revision | no |
| R6/R7/R17 (S3 naming) | Gain feedback | S3 states max gain k=1+(R6+R7)/R17 = 1+(1M+18k)/2.2k = 464 (~53dB) | S3 | **values stated in S3 but full refdes map unverified** |
| C6 | HF stability | TBD | S3 | no |
| C4 | Bass limit in gain path | TBD (varies by revision) | S3/S4 | no |
| C7 | Coupling/bass role | TBD (varies) | S3 | no |
| R8 | Clipping series resistor (to Vref network) | TBD | S3/S2 critical role | no |
| Q1, Q2 | Clipping devices (body diodes) | **2N7000** (common, D003) | S1–S3 | part type yes, package/pinout no |
| D2 | Asymmetric Ge element | **1N34A-class selected Ge OPTIONAL** (D003); default most-available may use **BAT46-class Schottky** on versatile pads | S3: "Germanium diode D2 is present not in all versions of OCD" (v1.4 has Ge character per S4) | **default choice needs your confirmation** |
| U1B | Gain stage 2 | TL082 (2/2), fixed gain ~5 (S3: R10/R11) | S3 | part yes, values no |
| R10, R11 | Stage 2 gain | gives ~5x (S3) — exact values TBD | S3 | no |
| C11 | Output coupling | "high value" (S3); Nichicon MUSE mentioned in some analyses | S3 | no |
| R12, R13, C12, R14, Tone pot | Tone + HP/LP | passive treble cut; HP/LP parallels resistors (S3) | S3/S2 | no |
| Volume pot | Output level | log in v1.4 per S4 (verify) | S4 | no |
| SW_HP/LP | Voicing switch | SPDT/DPDT TBD | S3 | no |
| 3PDT | True bypass | standard wiring TBD (Q5) | C002 | no |
| Jacks/DC jack | I/O/power | 1/4" TS, 2.1mm center-neg | standard | type yes, wiring no |

## Required to lock this BOM
1. Confirm/choose a **single traceable schematic source** and paste or authorize extraction (blocker).
2. Confirm **D003 default clipping option**: `BAT46-class Schottky default, Ge optional` (recommended) OR `1N4148 default, Ge optional`.
3. Resolve D002 after S007/S008 datasheet extraction + SPICE @ 5/9/18V.

## Circuit-design-skill readiness
- ngspice available locally. TL082/2N7000 **not in model_fetch catalog**; TI **SLOJ070** PSpice model noted (S007) — ingest with provenance when file/source obtained. 2N7002 in catalog is **not** a drop-in for 2N7000 body-diode clipping context without verification.

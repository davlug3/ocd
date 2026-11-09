# Schematic — v0.1 Working Reference (v1.4-style, UNVERIFIED cross-check)

**Project:** unbranded OCD-style overdrive clone v0.1  
**Date:** 2026-11-09  
**Status:** Working schematic/BOM created per user authorization. **UNVERIFIED** — synthesized from S2 (Analog Is Not Dead, text; schematic image not machine-extracted) and S3 (zadvitsky, partial values). **Refdes in this document are PROJECT refdes**, not claimed to match S2/S3/original. Do not treat as a verified clone without traceable schematic confirmation and datasheet pinout checks.

## Scope / deviations
- Supply: **8–18V DC, center-negative** (C022, reconciled 2026-11-09; 5V dropped). *8V is the minimum and still requires D002 TL082 validation (C023/S007).*
- **True bypass** (C002/A2).
- **D003 (most-available default):** versatile clipping pads; **default = BAT46-class Schottky** (project assumption), selected Ge (1N34A-class) optional, 1N4148 optional. Preserves **floating-Vref clipping topology** (C003). **No identical tone claim.**
- Anchors: hybrid **S002+S003** cross-checked with **S001/S013** (provenance-labeled; not a verified Fulltone netlist).

## Block signal flow
```
J2(IN) -> C4 -> [input ref/bias R3,R4,R5] -> U1A (Gain 1, Drive RV1)
      -> R8 -> [CLIP to VREF: Q1 body diode path || (Q2 body diode + D2 asym element)]
      -> U1B (Gain 2) -> tone/HP-LP (RV2,C7,R11,R12,SW1) -> C8 -> RV3 -> J3(OUT)
                               VREF (~VCC/2) biases U1 and clipping reference
SW2 3PDT provides true bypass (dry J2->J3 when off)
J1/VCC -> D1(reverse prot., proposed) -> C1||C2 -> VCC rail; R1/R2/C3 -> VREF
```

## Stage details (with provenance/status)

### 1) Power / Vref (project R1,R2,C3,D1,C1,C2)
- **VCC:** 8–18V DC center-neg via J1 (C022). Proposed reverse protection D1 (S3 mentions protection diode; type/value TBD). C1 bulk + C2 HF decoupling (S2: R1/C2/C3 filter concept; values TBD).
- **VREF:** resistive divider to ~Vcc/2 + filter cap (S2: R4,R7,C5 in their naming; S3: R1,R2). Ideal example: 100k/100k @ 9V = 4.5V, Rth ~50k (C008, `circuit_calc.py divider`); 4V @ 8V, 9V @ 18V. **Proposed 100k/100k/10uF** pending locked schematic.
- **D002 note:** Vref at 8V = 4V. TI S007 (opened 2026-11-09) shows TL082 min supply 7V and CM headroom to V− typ 3V — *typical* margin exists at 8V, but swing/headroom are condition-dependent and **unverified** (C023). Historical 5V risk (C011) is superseded by the 8–18V spec change.

### 2) Input / Gain 1 (U1A TL082, RV1 Drive)
- Input coupling + reference/bias network (S2: C1,R2 1M,R3,R6 to Vref; S3: C5,R5,R3,R4). **Exact values TBD**; project proposes C4 22nF–100nF, R3 1M, R4 1k–10k, R5 1M (UNVERIFIED placeholders).
- Non-inverting gain with Drive. **S3 states max gain:** `k = 1 + (R6 + R7) / R17 = 1 + (1M + 18k) / 2.2k = 464 (~53 dB)` (accessed 2026-11-09, S003). **Project mapping (provisional):** R6=2.2k (Rg), R7=18k (fixed), RV1=1M (Drive) — **refdes mapping uncertain**; confirm before netlist.
- HF stability cap (S2: C6) and bass/gain-path shaping (S2: C4, S3: C7 varies) — **TBD**.
- **Risk:** Max gain 464 => GBW-limited bandwidth with TL082 GBW~3MHz typ (`circuit_calc.py opamp --gain 464 --gbw 3000000` shows BW margin concern); also noise/oscillation risk. **8V headroom/swing/CM must be validated (D002/C023).**

### 3) Clipping to Vref (R8, Q1, Q2, D2) — key topology
- Amplified signal through **series resistor R8** into clipping network referenced to **VREF** (S1–S3, C003). **Not ground-referenced** in the defining topology.
- **Typical v1.4 character (S1–S4):** 2N7000 MOSFET body-diode paths + 1N34A Ge in one branch => asymmetric clipping. S2 text: "2N7000 in parallel with another 2N7000 and a 1N34A germanium diode"; **exact node orientation must be confirmed** (S2 comment notes other references show different wiring — conflict flag).
- **D003 versatile/most-available implementation:** pads/footprint options for Q1,Q2,D2. **Default D2 = BAT46-class Schottky** (project assumption); **1N34A-class selected Ge optional**; 1N4148 optional. Document Vf/orientation per option. **No identical tone claim.**
- **Pinouts unverified:** 2N7000 pinout/manufacturer-specific (C012/S008).

### 4) Gain 2 (U1B TL082)
- S3: "Resistors R10 and R11 gives us amplification factor a bit smaller then 5". **Project proposes** R9=4.7k, R10=22k => gain ~5.68 (non-inverting) — **TBD, adjust to verified values**.

### 5) Tone / HP-LP / Volume / Output
- Passive treble-cut tone, HP/LP voicing switch (S2/S3; refdes/values differ). S2: treble through 10k pot X4 and cap C11 to ground; HP/LP parallels R14,R15. S3: R12/R13/C12/R14 and HP/LP parallels R12,R13. **TBD pending locked schematic.**
- Output coupling C8 high-value film proposed (S3: C11 high value). Volume RV3 100k log proposed (S4/practice, verify).

### 6) True bypass (SW2)
- 3PDT mechanical bypass, dry signal J2->J3 when off (A2/C002). LED indicator optional (Q5).

## Datasheet/pinout verification required before netlist/PCB
| Part | Datasheet/source | What to verify |
|---|---|---|
| TL082 (exact variant) | TI SLOS081O Rev O (S007) | Pinout (DIP/SOIC), supply min/recommended, VICR/VOM vs Vcc=5/9/18V & load, single-supply biasing |
| 2N7000 (exact mfr/pkg) | onsemi NDS7002A / chosen mfr (S008, C012) | Pinout/orientation (TO-92/SOT-23), body diode, ratings |
| BAT46 / 1N4148 / selected Ge | Mfr datasheets / measured Ge | Vf/leakage, polarity, footprint |
| Pots/switch/jacks | Mfr/measured | Pinout, taper, mechanical |

## Circuit-design-skill next steps (once values locked/authorized)
1. Extract S007/S008 limits; ingest provenance-tracked SPICE models (TL082 TI PSpice SLOJ070 noted; 2N7000/diodes as available with provenance).
2. Build `circuit/base-spec.json` with normalized project refdes/nets + test-point map.
3. `audio_handoff.py` merge + `generate.py` + `verify.py --require models,design`.
4. ngspice @ 8V/9V/18V (D002/A1) with provenance-tracked models: Vref, DC ops, clean swing, clipping waveform, AC under stated conditions. Record in research log.

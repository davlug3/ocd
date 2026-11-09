# ocd_textsch_s002_9v_v0p1_draft

OCD-style overdrive draft from user-provided text schematic + node connections reported from schematic image (S002-based: https://www.analogisnotdead.com/article34/circuit-analysis-fulltone-s-ocd, accessed 2026-11-09). 9V ONLY. UNVERIFIED: op-amp feedback/pin wiring assumed Vref-biased single-supply; M1/M2/D1 types unknown (APPROX sim-only); X2/X5 pot wiring modeled at 50%; Switch1/R14/R15/C11/X4 omitted/simplified. Not a verified Fulltone netlist. Do not fabricate.

- Topology: `ocd_textsch_s002_9v`
- Ground: `GND`
- Generated: 2026-11-09
- Simulation status: **vendor models supplied**

## Supplies

- `VCC` = 9.0 V

## Design record

Vref-biased single-supply 9V: input bias -> X1 gain -> R9/R10/R12/C7/M1/M2/D1 clip network -> X3 gain/filter -> simplified output volume. Switch1/X4 omitted.

**Blocks:** power_ref; input_bias; x1_gain; clip_network; x3_gain; output_simplified

**Interfaces:** IN; OUT 100k; VCC 9V; GND

**Test points:** VREF; X1_OUT; CLIP_A; CLIP_B; X3_OUT; OUT

| Budget | Value |
| --- | --- |
| vref | ~4.5V |

### Requirements

| ID | Requirement | Acceptance | Source |
| --- | --- | --- | --- |
| R1 | 9V DC operation with Vref ~4.5V | op/bench TBD | user text + S002 |
| R2 | Two TL082 gain stages + MOSFET/diode nonlinear stage (user-reported connections) | sim/bench TBD | user-provided 2026-11-09 |
| R3 | Adjustable gain and volume (simplified in sim) | pots TBD | user text |

### Decisions

| ID | Decision | Alternatives | Rationale | Sources |
| --- | --- | --- | --- | --- |
| D_V1 | 9V only | 8-18V (prior C022) | user selected 1=yes 9V only 2026-11-09 | user 2026-11-09 |
| D_CLIP_V1 | Implement user-reported M1/M2/D1/R9/R10/R12/C7 connections from schematic image (S002-based) | prior provisional draft wiring | user provided explicit node table 2026-11-09 | user-reported from schematic image, 2026-11-09, S002 https://www.analogisnotdead.com/article34/circuit-analysis-fulltone-s-ocd accessed 2026-11-09 |
| D_POTS | X2 gain pot 1M per S002 retrieved text (mapping to X2 assumed); X5 volume 100k placeholder (not found in retrieved S002 text); X4/Switch1 omitted for sim | ask user for exact pot values/wiring | user asked to find likely values from academic/available sources; S002 states 'gain pot (1M)' and '10k pot X4'; volume not explicit in retrieval | S002 accessed 2026-11-09 (curl extract), placeholder for X5 |
| D_DEV | TL082.301 sim-only; M1/M2 APPROX_2N7000, D1 APPROX_BAT46 placeholders (user: D1 any of those) | APPROX_1N34A, sourced models | exact parts unknown; simulation-only | TI SLOJ070 TL082.301, local APPROX models |
| D_BIAS_FIX | Provisional: R2 to VREF (was GND per text) to fix DC bias in sim; D1=APPROX_1N4148 (user-selected placeholder) per 2026-11-09 | keep R2 to GND and revise feedback topology, verify S002 image | OP showed IN_B~3V/X1_OUT saturated low with R2-GND + R6-VREF ratio; single-supply bias fix applied for simulatable OP | ngspice OP debug 2026-11-09, user selection 2026-11-09 |

### Risks

| ID | Risk | Severity | Mitigation | Verification |
| --- | --- | --- | --- | --- |
| K1 | Op-amp feedback and input pin wiring assumed (text functional, not pin-net explicit) | high | verify against actual S002 schematic | schematic compare + sim |
| K2 | M1/M2/D1 types/pinouts unknown; APPROX models unverified | high | identify parts from schematic/BOM | datasheets + sourced models |
| K3 | X2/X5 values/wiring/placement uncertain; X5 is placeholder | medium | confirm from S002 schematic image/BOM | source check |
| K4 | Switch1/R14/R15/C11/X4 omitted; output/tone not representative | high | add after confirming topology | schematic compare |
| K5 | User-reported node extraction from image; no image in repo | high | record provenance; verify against S002 | manual check |

### Sources

| Title | Document / URL | Revision | Accessed |
| --- | --- | --- | --- |
| Circuit Analysis: Fulltone's OCD | https://www.analogisnotdead.com/article34/circuit-analysis-fulltone-s-ocd | n/a | 2026-11-09 |
| User-provided text schematic + node connections | local:conversation/2026-11-09 | n/a | 2026-11-09 |

## Components

| Ref | Type | Value | Pins | Notes |
| --- | --- | --- | --- | --- |
| V1 | V | 9 V | 1=VCC, 2=GND | 9V only (D_V1) |
| V_IN | V | SIN source | 1=IN, 2=GND |  |
| R1 | R | 100 | 1=VCC, 2=VCC_F | supply feed/filter node |
| C2 | C | 10u | 1=VCC_F, 2=GND |  |
| C3 | C | 100n | 1=VCC_F, 2=GND |  |
| R4 | R | 10k | 1=VCC_F, 2=VREF |  |
| R7 | R | 10k | 1=VREF, 2=GND |  |
| C5 | C | 10u | 1=VREF, 2=GND |  |
| C1 | C | 22n | 1=IN, 2=IN_B | input coupling |
| R2 | R | 1Meg | 1=IN_B, 2=VREF | PROVISIONAL BIAS FIX (2026-11-09): changed from GND to VREF to bias IN_B near Vref in single-supply sim; S002 text states R2 to ground (unverified mapping) - verify against schematic |
| R6 | R | 470k | 1=IN_B, 2=VREF | bias to Vref |
| R3 | R | 10k | 1=IN_B, 2=X1_P | limits current to X1+ |
| X1A | OPAMP | TL082 | 1=X1_P, 2=X1_FB, 3=VCC_F, 4=GND, 5=X1_OUT | TL082 section 1; wiring assumed |
| R5 | R | 2.2k | 1=X1_FB, 2=VREF | gain ref to Vref assumed |
| R8 | R | 18k | 1=X1_FB, 2=X2_W | gain network; placement assumed |
| R_X2POT | R | 500k | 1=X2_W, 2=X1_OUT | Drive/gain pot modeled 50% of 1M (S002 gain pot 1M; mapping/wiring assumed) |
| C4 | C | 100n | 1=X1_FB, 2=VREF | LF response; assumed placement |
| C6 | C | 220p | 1=X1_OUT, 2=X1_FB | HF/stability; assumed |
| R9 | R | 10k | 1=X1_OUT, 2=CLIP_A | user-reported |
| C7 | C | 10n | 1=VREF, 2=CLIP_A | user-reported VREF-CLIP_A |
| R10 | R | 10k | 1=CLIP_A, 2=CLIP_B | user-reported |
| R12 | R | 220k | 1=VREF, 2=CLIP_B | user-reported bias to CLIP_B |
| M1 | NMOS | APPROX_2N7000 | 1=VREF, 2=VREF, 3=CLIP_A | user-reported from schematic image; exact part unknown; APPROX sim-only |
| M2 | NMOS | APPROX_2N7000 | 1=VREF, 2=M2_D1_NODE, 3=M2_D1_NODE | user-reported; exact part unknown |
| D1 | D | APPROX_1N4148 | 1=CLIP_A, 2=M2_D1_NODE | user-reported polarity A=CLIP_A K=M2_D1_NODE; exact type unknown (user selected 1N4148 Si APPROX placeholder); APPROX sim-only |
| X3A | OPAMP | TL082 | 1=CLIP_B, 2=X3_FB, 3=VCC_F, 4=GND, 5=X3_OUT | non-inv input CLIP_B per user node table; wiring assumed |
| R11 | R | 39k | 1=X3_FB, 2=VREF | assumed gain ref |
| R13 | R | 150k | 1=X3_FB, 2=X3_OUT | feedback; assumed placement |
| C8 | C | 100n | 1=X3_FB, 2=VREF | LF; assumed |
| C9 | C | 220p | 1=X3_OUT, 2=X3_FB | HF; assumed |
| C10 | C | 10u | 1=X3_OUT, 2=OUT_A | output coupling |
| R_VOL5A | R | 50k | 1=OUT_A, 2=OUT | Volume pot 100k placeholder modeled at 50% (NOT found in retrieved S002 text); Switch1/R14/R15/C11/X4 omitted |
| R_VOL5B | R | 50k | 1=OUT, 2=GND | volume lower leg placeholder |
| R_LOAD | R | 100k | 1=OUT, 2=GND |  |

## Bill of materials

| Refs | Qty | Type | Value | Footprint |
| --- | --- | --- | --- | --- |
| C1 | 1 | Capacitor | 22n |  |
| C10 | 1 | Capacitor | 10u |  |
| C2 C5 | 2 | Capacitor | 10u |  |
| C3 | 1 | Capacitor | 100n |  |
| C4 | 1 | Capacitor | 100n |  |
| C6 | 1 | Capacitor | 220p |  |
| C7 | 1 | Capacitor | 10n |  |
| C8 | 1 | Capacitor | 100n |  |
| C9 | 1 | Capacitor | 220p |  |
| D1 | 1 | Diode | APPROX_1N4148 |  |
| M1 | 1 | N-MOSFET | APPROX_2N7000 |  |
| M2 | 1 | N-MOSFET | APPROX_2N7000 |  |
| R1 | 1 | Resistor | 100 |  |
| R11 | 1 | Resistor | 39k |  |
| R12 | 1 | Resistor | 220k |  |
| R13 | 1 | Resistor | 150k |  |
| R2 | 1 | Resistor | 1Meg |  |
| R3 | 1 | Resistor | 10k |  |
| R4 R7 | 2 | Resistor | 10k |  |
| R5 | 1 | Resistor | 2.2k |  |
| R6 | 1 | Resistor | 470k |  |
| R8 | 1 | Resistor | 18k |  |
| R9 R10 | 2 | Resistor | 10k |  |
| R_LOAD | 1 | Resistor | 100k |  |
| R_VOL5A | 1 | Resistor | 50k |  |
| R_VOL5B | 1 | Resistor | 50k |  |
| R_X2POT | 1 | Resistor | 500k |  |
| V1 | 1 | Voltage source | 9 V |  |
| V_IN | 1 | Voltage source | SIN source |  |
| X1A | 1 | Op-amp | TL082 |  |
| X3A | 1 | Op-amp | TL082 |  |

## Device models

| Ref | Type | Model | Kind | Vendor | Part | SHA256 |
| --- | --- | --- | --- | --- | --- | --- |
| X1A | OPAMP | `TL082` | vendor | Texas Instruments | TL082 (macromodel) | `adad2e131f728610` |
| M1 | NMOS | `APPROX_2N7000` | vendor | project approximation | 2N7000 APPROX sim-only | `081054dff4a75cb5` |
| M2 | NMOS | `APPROX_2N7000` | vendor | project approximation | 2N7000 APPROX sim-only | `081054dff4a75cb5` |
| D1 | D | `APPROX_1N4148` | vendor | project approximation | 1N4148 APPROX sim-only (user selected) | `bfa7e99c8627cad9` |
| X3A | OPAMP | `TL082` | vendor | Texas Instruments | TL082 (macromodel) | `adad2e131f728610` |

## Analyses

- `op`
- `tran` (stop=0.03, step=1e-05)
- `ac` (start=20, stop=20000, points=100)

## Assumptions

- 9V only. All wiring beyond user-reported clip node table is assumed/provisional.
- Op-amp feedback networks (X1/X3) are standard Vref-biased assumptions from component values; not pin-verified against S002 schematic.
- X2 modeled as 500k (50% of 1M). S002 states 'gain pot (1M)' (accessed 2026-11-09) - mapping/wiring to X2 assumed.
- X5 modeled as 50% of 100k placeholder - volume value NOT found in retrieved S002 text; unverified.
- M1/M2/D1 exact part numbers unknown. APPROX_2N7000/APPROX_BAT46 are simulation-only, unverified.
- Switch1, R14, R15, C11, X4 omitted/simplified for initial sim.
- Provenance: user-provided text + node connections reported from schematic image (S002-based), 2026-11-09, unverified.
- PROVISIONAL BIAS FIX: R2 connected to VREF (not GND) to achieve ~Vref bias in simulation; conflicts with S002 text snippet stating R2 to ground - VERIFY.

## Verification

Status: **PASS**

- [PASS] spec: valid spec with 34 components, 0 warning(s)
- [PASS] models: vendor models supplied
- [PASS] design: 3 requirements, 5 decisions, 5 risks, 2 sources
- [PASS] spice_netlist: 34 devices, node lists match the spec
- [PASS] ltspice_asc: 34 symbols; every pin has a matching net flag
- [PASS] kicad_netlist: 17 nets match the spec exactly
- [SKIP] kicad_schematic: kiutils is not installed; schematic geometry not parsed (set PYTHONPATH to a kiutils checkout)
- [SKIP] pcb_handoff: not generated (add "pcb" to deliverables)
- [SKIP] mna_linear: circuit contains nonlinear element(s) M1, M2, D1; MNA only solves linear circuits
- [PASS] ngspice: ngspice ran 3 analysis plot(s): AC Analysis, Operating Point, Transient Analysis; V(vcc)=9, V(in)=0, V(vcc_f)=8.15877, V(vref)=4.07938, V(in_b)=4.07937, V(x1_p)=4.07937, V(xx1a.11)=0.345441, V(xx1a.12)=0.345453, V(xx1a.6)=7.80968e-09, V(xx1a.7)=4.07933, V(x1_out)=4.07933, V(xx1a.53)=5.95877, V(xx1a.54)=2.2, V(xx1a.90)=-2.67625e-07, V(xx1a.91)=25, V(xx1a.92)=-25, V(xx1a.99)=4.07939, V(xx1a.10)=3.68079, V(x1_fb)=4.07938, V(xx1a.9)=0, V(xx1a.8)=4.07933, V(x2_w)=4.07938, V(clip_a)=4.07933, V(clip_b)=4.07933, V(m2_d1_node)=4.07935, V(xx3a.11)=0.345441, V(xx3a.12)=0.345453, V(xx3a.6)=2.37909e-08, V(xx3a.7)=4.07922, V(x3_out)=4.07922, V(xx3a.53)=5.95877, V(xx3a.54)=2.2, V(xx3a.90)=-8.47424e-07, V(xx3a.91)=25, V(xx3a.92)=-25, V(xx3a.99)=4.07939, V(xx3a.10)=3.68075, V(x3_fb)=4.07935, V(xx3a.9)=0, V(xx3a.8)=4.07922, V(out_a)=0, V(out)=0

## Files

- `spice`: `ocd_textsch_s002_9v_v0p1_draft.cir`
- `models`: `ocd_textsch_s002_9v_v0p1_draft.models`
- `ltspice_asc`: `ocd_textsch_s002_9v_v0p1_draft.asc`
- `kicad_net`: `ocd_textsch_s002_9v_v0p1_draft.net`
- `kicad_sch`: `ocd_textsch_s002_9v_v0p1_draft.kicad_sch`
- `bom`: `ocd_textsch_s002_9v_v0p1_draft-bom.csv`

> The generated SPICE netlist is the electrical source of truth. The schematics are drawn from the same component list and use net labels at every pin instead of routed wires.

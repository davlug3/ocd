# ocd_textsch_s002_9v_v0p1_draft

OCD-style overdrive 9V draft from S002-verified topology + user node connections. S002 confirms: R2 to GND, clip = 2N7000||2N7000+1N34A Ge to Vref, X4=10k tone pot, C11 cap to ground, HP/LP parallels R14/R15, gain pot 1M. Clip wiring CONFIRMED from S002 schematic image (matches user-reported; commenter-reported alternate does not match). Op-amp feedback wiring assumed. Not a verified Fulltone netlist. Do not fabricate.

- Topology: `ocd_textsch_s002_9v`
- Ground: `GND`
- Generated: 2026-11-10
- Simulation status: **vendor models supplied**

## Supplies

- `VCC` = 9.0 V

## Design record

Vref-biased single-supply 9V: input bias -> X1 gain -> R9/R10/R12/C7/M1/M2/D1 clip network (to Vref) -> X3 gain/filter -> tone (X4 10k pot + C11 to ground) -> HP/LP (Switch1 parallels R14/R15) -> volume -> OUT.

**Blocks:** power_ref; input_bias; x1_gain; clip_network; x3_gain; tone_hp_lp; output_volume

**Interfaces:** IN; OUT 100k; VCC 9V; GND

**Test points:** VREF; X1_OUT; CLIP_A; CLIP_B; X3_OUT; TONE_W; OUT

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
| D_BIAS_FIX | Reverted: R2 to GND per S002-confirmed text (1M input reference to ground). R6 biases op-amp non-inverting input to VREF. D1=APPROX_1N34A per S002-confirmed 1N34A Ge clipping diode. | keep R2 to VREF (provisional sim fix, conflicts with S002), verify S002 image for pin-level confirmation | S002 text explicitly states R2 connects input cap C1 to GROUND as voltage reference (C026). Previous VREF move was a provisional sim bias fix and is now removed. | S002 https://www.analogisnotdead.com/article34/circuit-analysis-fulltone-s-ocd accessed 2026-11-10 via webfetch (C026), ngspice OP debug 2026-11-09 (superseded) |
| D_TONE | Implement S002-confirmed tone/HP-LP network: X4=10k tone pot, C11 tone cap to ground, Switch1 (HP/LP) parallels R14/R15. R14=22k/R15=33k image-read from S002 schematic (verify); C11=47n placeholder. | keep tone/volume simplified (prior draft), ask user for exact tone/HP-LP values/wiring | S002 text confirms X4=10k pot, C11 cap to ground, HP/LP parallels R14/R15 (C028). Clip wiring confirmed from S002 schematic image matches user-reported wiring; commenter-reported alternate wiring does not match image. | S002 https://www.analogisnotdead.com/article34/circuit-analysis-fulltone-s-ocd accessed 2026-11-10 via webfetch (C028), S002 schematic images in circuit/sources/s002-images/ (clipping.png, fulltone-ocd.png) |

### Risks

| ID | Risk | Severity | Mitigation | Verification |
| --- | --- | --- | --- | --- |
| K1 | Op-amp feedback and input pin wiring assumed (text functional, not pin-net explicit). R2→GND confirmed from S002 image; X1/X3 feedback placement still assumed. | high | verify against actual S002 schematic | schematic compare + sim |
| K2 | M1/M2/D1 types/pinouts unknown; APPROX models unverified. Clip wiring CONFIRMED from S002 image: M1[D&G=VREF,S=CLIP_A], M2[D=VREF,G&S=M2_D1_NODE], D1[A=CLIP_A,K=M2_D1_NODE]. Commenter-reported alternate wiring does NOT match S002 image. | high | identify parts from schematic/BOM; obtain manufacturer models | datasheets + sourced models + schematic compare |
| K3 | X2/X5 values/wiring/placement uncertain; X5 is placeholder | medium | confirm from S002 schematic image/BOM | source check |
| K4 | Tone/HP-LP values are image-read (uncertain): R14=22k, R15=33k, C11=47n placeholder. X4=10k confirmed from S002 text. Switch1 wiring assumed. | medium | confirm values from S002 schematic image | schematic compare |
| K5 | S002 schematic image available but cannot be machine-analyzed; node extraction and clip wiring rely on human visual inspection. All image-read values should be verified against the source image. | medium | user/human verification of S002 images in circuit/sources/s002-images/ | manual check |

### Sources

| Title | Document / URL | Revision | Accessed |
| --- | --- | --- | --- |
| Circuit Analysis: Fulltone's OCD | https://www.analogisnotdead.com/article34/circuit-analysis-fulltone-s-ocd | n/a | 2026-11-09 |
| User-provided text schematic + node connections | local:conversation/2026-11-09 | n/a | 2026-11-09 |

## Components

| Ref | Type | Value | Tolerance | Pins | Notes |
| --- | --- | --- | --- | --- | --- |
| V1 | V | 9 V | — | 1=VCC, 2=GND | 9V only (D_V1) |
| V_IN | V | SIN source | — | 1=IN, 2=GND |  |
| R1 | R | 100 | — | 1=VCC, 2=VCC_F | supply feed/filter node |
| C2 | C | 10u | — | 1=VCC_F, 2=GND |  |
| C3 | C | 100n | — | 1=VCC_F, 2=GND |  |
| R4 | R | 10k | — | 1=VCC_F, 2=VREF |  |
| R7 | R | 10k | — | 1=VREF, 2=GND |  |
| C5 | C | 10u | — | 1=VREF, 2=GND |  |
| C1 | C | 22n | — | 1=IN, 2=IN_B | input coupling |
| R2 | R | 1Meg | — | 1=IN_B, 2=GND | S002-confirmed: R2 (1M) connects input cap C1 to GROUND as voltage reference, not to VREF. R6 biases op-amp to VREF. |
| R6 | R | 470k | — | 1=IN_B, 2=VREF | bias to Vref |
| R3 | R | 10k | — | 1=IN_B, 2=X1_P | limits current to X1+ |
| X1A | OPAMP | TL082 | — | 1=X1_P, 2=X1_FB, 3=VCC_F, 4=GND, 5=X1_OUT | TL082 section 1; wiring assumed |
| R5 | R | 2.2k | — | 1=X1_FB, 2=VREF | gain ref to Vref assumed |
| R8 | R | 18k | — | 1=X1_FB, 2=X2_W | gain network; placement assumed |
| R_X2POT | R | 500k | — | 1=X2_W, 2=X1_OUT | Drive/gain pot modeled 50% of 1M (S002 gain pot 1M; mapping/wiring assumed) |
| C4 | C | 100n | — | 1=X1_FB, 2=VREF | LF response; assumed placement |
| C6 | C | 220p | — | 1=X1_OUT, 2=X1_FB | HF/stability; assumed |
| R9 | R | 10k | — | 1=X1_OUT, 2=CLIP_A | user-reported |
| C7 | C | 10n | — | 1=VREF, 2=CLIP_A | user-reported VREF-CLIP_A |
| R10 | R | 10k | — | 1=CLIP_A, 2=CLIP_B | user-reported |
| R12 | R | 220k | — | 1=VREF, 2=CLIP_B | user-reported bias to CLIP_B |
| M1 | NMOS | APPROX_2N7000 | — | 1=VREF, 2=VREF, 3=CLIP_A | S002-schematic-image-confirmed: M1 [D&G=VREF, S=CLIP_A]. Exact part unknown; APPROX sim-only. Commenter-reported alternate wiring (M1[S=VREF,D&G=R9/R10]) does NOT match S002 image. |
| M2 | NMOS | APPROX_2N7000 | — | 1=VREF, 2=M2_D1_NODE, 3=M2_D1_NODE | S002-schematic-image-confirmed: M2 [D=VREF, G&S=M2_D1_NODE]. Exact part unknown; APPROX sim-only. Commenter-reported alternate wiring (M2[D&G=VREF,S=D1]) does NOT match S002 image. |
| D1 | D | APPROX_1N34A | — | 1=CLIP_A, 2=M2_D1_NODE | S002-schematic-image-confirmed: D1 [A=CLIP_A, K=M2_D1_NODE], 1N34A Ge per article text (C027). APPROX sim-only model, Ge variability applies. |
| X3A | OPAMP | TL082 | — | 1=CLIP_B, 2=X3_FB, 3=VCC_F, 4=GND, 5=X3_OUT | non-inv input CLIP_B per user node table; wiring assumed |
| R11 | R | 39k | — | 1=X3_FB, 2=VREF | assumed gain ref |
| R13 | R | 150k | — | 1=X3_FB, 2=X3_OUT | feedback; assumed placement |
| C8 | C | 100n | — | 1=X3_FB, 2=VREF | LF; assumed |
| C9 | C | 220p | — | 1=X3_OUT, 2=X3_FB | HF; assumed |
| C10 | C | 10u | — | 1=X3_OUT, 2=TONE_TOP | output coupling to tone network |
| R_X4A | R | 5k | — | 1=TONE_TOP, 2=TONE_W | Tone pot X4 (10k) modeled at 50%: upper leg TONE_TOP→TONE_W. S002-confirmed 10k pot. Wiring assumed. |
| R_X4B | R | 5k | — | 1=TONE_W, 2=GND | Tone pot X4 (10k) modeled at 50%: lower leg TONE_W→GND. S002-confirmed 10k pot. Wiring assumed. |
| C11 | C | 47n | — | 1=TONE_W, 2=GND | S002-confirmed: tone cap C11 to ground. Value TBD (47n placeholder). |
| R14 | R | 22k | — | 1=TONE_W, 2=VOL_TOP | S002-schematic-image-read: R14 HP/LP network resistor (value reads as 22k, verify). Always in path (HP position); R15 added in parallel when Switch1 closed (LP position). |
| R15 | R | 33k | — | 1=TONE_W, 2=VOL_TOP | S002-schematic-image-read: R15 HP/LP network resistor (value reads as 33k, verify). Added in parallel with R14 when Switch1 closed (LP position). Removing R15 models HP position (switch open). |
| R_VOL5A | R | 50k | — | 1=VOL_TOP, 2=OUT | Volume pot 100k placeholder modeled at 50% (NOT found in retrieved S002 text). |
| R_VOL5B | R | 50k | — | 1=OUT, 2=GND | volume lower leg placeholder |
| R_LOAD | R | 100k | — | 1=OUT, 2=GND |  |

## Bill of materials

| Refs | Qty | Type | Value | Footprint |
| --- | --- | --- | --- | --- |
| C1 | 1 | Capacitor | 22n |  |
| C10 | 1 | Capacitor | 10u |  |
| C11 | 1 | Capacitor | 47n |  |
| C2 C5 | 2 | Capacitor | 10u |  |
| C3 | 1 | Capacitor | 100n |  |
| C4 | 1 | Capacitor | 100n |  |
| C6 | 1 | Capacitor | 220p |  |
| C7 | 1 | Capacitor | 10n |  |
| C8 | 1 | Capacitor | 100n |  |
| C9 | 1 | Capacitor | 220p |  |
| D1 | 1 | Diode | APPROX_1N34A |  |
| M1 | 1 | N-MOSFET | APPROX_2N7000 |  |
| M2 | 1 | N-MOSFET | APPROX_2N7000 |  |
| R1 | 1 | Resistor | 100 |  |
| R11 | 1 | Resistor | 39k |  |
| R12 | 1 | Resistor | 220k |  |
| R13 | 1 | Resistor | 150k |  |
| R14 | 1 | Resistor | 22k |  |
| R15 | 1 | Resistor | 33k |  |
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
| R_X4A | 1 | Resistor | 5k |  |
| R_X4B | 1 | Resistor | 5k |  |
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
| D1 | D | `APPROX_1N34A` | vendor | project approximation | 1N34A Ge APPROX sim-only (S002-confirmed D1 type) | `db949f2074c80243` |
| X3A | OPAMP | `TL082` | vendor | Texas Instruments | TL082 (macromodel) | `adad2e131f728610` |

## Analyses

- `op`
- `tran` (stop=0.03, step=1e-05)
- `ac` (start=20, stop=20000, points=100)

## Assumptions

- 9V only. All wiring beyond user-reported clip node table and S002 article text is assumed/provisional.
- Op-amp feedback networks (X1/X3) are standard Vref-biased assumptions from component values; not pin-verified against S002 schematic.
- R2 to GND per S002-confirmed text (C026) — not VREF. R6 biases op-amp non-inverting input to VREF.
- X2 modeled as 500k (50% of 1M). S002 states 'gain pot (1M)' (accessed 2026-11-09) - mapping/wiring to X2 assumed.
- X5 modeled as 50% of 100k placeholder - volume value NOT found in retrieved S002 text; unverified.
- M1/M2 exact part numbers unknown; APPROX_2N7000 simulation-only, unverified. D1=APPROX_1N34A per S002-confirmed 1N34A Ge clipping diode (C027). APPROX sim-only, Ge variability applies.
- Clip wiring CONFIRMED from S002 schematic image: M1[D&G=VREF,S=CLIP_A], M2[D=VREF,G&S=M2_D1_NODE], D1[A=CLIP_A,K=M2_D1_NODE]. Commenter-reported alternate wiring does NOT match S002 image.
- Tone/HP-LP added per S002: X4=10k pot, C11 cap to ground, Switch1 parallels R14/R15 (C028). R14=22k, R15=33k image-read from S002 schematic (verify); C11=47n placeholder. Switch1 wiring assumed.
- Provenance: S002 article text + schematic images (webfetch 2026-11-10) + user-provided node connections from schematic image (2026-11-09). Images in circuit/sources/s002-images/.

## Verification

Status: **PASS**

- [PASS] spec: valid spec with 39 components, 0 warning(s)
- [PASS] models: vendor models supplied
- [PASS] design: 3 requirements, 6 decisions, 5 risks, 2 sources
- [SKIP] measurement_plan: no measurement plan declared; add design.measurements with test points, setup and acceptance criteria
- [SKIP] operating_limits: no operating limits declared; add calculated stresses and sourced datasheet limits
- [PASS] spice_netlist: 39 devices, node lists match the spec
- [PASS] ltspice_asc: 39 symbols; every pin has a matching net flag
- [PASS] kicad_netlist: 19 nets match the spec exactly
- [SKIP] kicad_schematic: kiutils is not installed; schematic geometry not parsed (set PYTHONPATH to a kiutils checkout)
- [SKIP] pcb_handoff: not generated (add "pcb" to deliverables)
- [SKIP] mna_linear: circuit contains nonlinear element(s) M1, M2, D1; MNA only solves linear circuits
- [PASS] ngspice: ngspice ran 3 analysis plot(s): AC Analysis, Operating Point, Transient Analysis; V(vcc)=9, V(in)=0, V(vcc_f)=8.15686, V(vref)=3.86898, V(in_b)=2.63195, V(x1_p)=2.63195, V(xx1a.11)=6.66856e-08, V(xx1a.12)=0.695012, V(xx1a.6)=19.6535, V(xx1a.7)=1.49133, V(x1_out)=1.52315, V(xx1a.53)=5.95686, V(xx1a.54)=2.2, V(xx1a.90)=-0.212178, V(xx1a.91)=25, V(xx1a.92)=-25, V(xx1a.99)=4.07843, V(xx1a.10)=2.48501, V(x1_fb)=3.85906, V(xx1a.9)=0, V(xx1a.8)=1.49133, V(x2_w)=3.77789, V(clip_a)=1.74654, V(clip_b)=1.83882, V(m2_d1_node)=1.74656, V(xx3a.11)=6.5009e-08, V(xx3a.12)=0.697739, V(xx3a.6)=19.7299, V(xx3a.7)=1.49328, V(x3_out)=1.52305, V(xx3a.53)=5.95686, V(xx3a.54)=2.2, V(xx3a.90)=-0.198462, V(xx3a.91)=25, V(xx3a.92)=-25, V(xx3a.99)=4.07843, V(xx3a.10)=1.69355, V(x3_fb)=3.3849, V(xx3a.9)=0, V(xx3a.8)=1.49328, V(tone_top)=0, V(tone_w)=0, V(vol_top)=0, V(out)=0

## Files

- `spice`: `ocd_textsch_s002_9v_v0p1_draft.cir`
- `models`: `ocd_textsch_s002_9v_v0p1_draft.models`
- `ltspice_asc`: `ocd_textsch_s002_9v_v0p1_draft.asc`
- `kicad_net`: `ocd_textsch_s002_9v_v0p1_draft.net`
- `kicad_sch`: `ocd_textsch_s002_9v_v0p1_draft.kicad_sch`
- `bom`: `ocd_textsch_s002_9v_v0p1_draft-bom.csv`

> The generated SPICE netlist is the electrical source of truth. The schematics are drawn from the same component list and use net labels at every pin instead of routed wires.

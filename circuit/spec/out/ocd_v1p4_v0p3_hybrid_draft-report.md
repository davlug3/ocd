# ocd_v1p4_v0p3_hybrid_draft

OCD-style overdrive v0.1 (unbranded), v1.4-style hybrid draft (S002+S003 cross-checked with S001/S013). 8-18V DC. TRUE BYPASS external. SIMULATION-ONLY/UNVERIFIED: provisional values, clipping wiring TBD/conflict, APPROX models. DC-op debug pass applied (bias/Vref stiffness/clipping DC-safe placeholders) - still provisional, do not fabricate.

- Topology: `ocd_style_overdrive_hybrid_v1p4`
- Ground: `GND`
- Generated: 2026-11-09
- Simulation status: **vendor models supplied**

## Supplies

- `VCC` = 9.0 V

## Design record

Vref-biased TL082 2-stage gain, provisional asymmetric MOSFET/diode clipping referenced to Vref, simplified tone/volume placeholders, 100k load. True bypass external.

**Blocks:** input; vref; gain1_drive; clip_vref_provisional; gain2; tone_volume_placeholder; output

**Interfaces:** IN_SIG AC; VOUT into 100k; VCC 8-18V; GND

**Test points:** VREF; G1_OUT; CLIP_NODE; G2_OUT; VOUT

| Budget | Value |
| --- | --- |
| supply | 8-18V DC |
| load | 100k |
| gain1_mid_approx | ~236x (Drive 50%, S003-based) |
| gain2 | ~4.9x placeholder |

### Requirements

| ID | Requirement | Acceptance | Source |
| --- | --- | --- | --- |
| A1 | Operate 8-18V DC center-negative (no damage/oscillation; functional audio at 8/9/18V into 100k, conditions TBD) | Bench/sim sweep 8/9/18V, 1kHz, 100k; D002 TL082 validation required | S009/C022 |
| A2 | True bypass (external to effect core) | Dry signal when off; 3PDT wiring verified separately | S009/C022 |
| A3 | Asymmetric OCD-style clipping character to Vref with tone/HP-LP voicing | Qualitative + sim waveform/spectrum under stated conditions; not a verified Fulltone clone claim | S001/S002/C003 |
| A4 | Vref bias tracks Vcc/2 | Within TBD tolerance across 8-18V | S002/C008 |

### Decisions

| ID | Decision | Alternatives | Rationale | Sources |
| --- | --- | --- | --- | --- |
| D001 | v1.4-style hybrid working reference, not verified Fulltone netlist | verified single schematic (blocked), v2-only | user lock C022; sources conflict/incomplete | S002 opened 2026-11-09, S003 opened 2026-11-09, S001/S013 cross-check |
| D002 | Validate TL082 at 8-18V; TL082.301 simulation-only | TL082H, OPA2197 | min supply 7V and directional sim favorable (C023/C024); not closed | S007 TI TL082 page opened 2026-11-09, circuit/models/TL082.301, C024 |
| D003 | Most-available/versatile clipping; default BAT46 in this draft, options noted | 1N34A default, 1N4148 | user lock C022; Ge variability C009 | S009/C022, S010-S012 context |
| D_CLIP_WIRE | PROVISIONAL clipping wiring follows S002 text topology assumption; M1/M2/D_ASYM orientation is TBD/conflict | S002 2026 comment alternate wiring, hold for traceable schematic | user selected provisional S002 text; exact node orientation not verified | S002 opened 2026-11-09, S002 page comment 2026-05-20 (conflict noted) |
| D_VALUES | Hybrid labeled: S003 explicit gain values + placeholders for simulatable completeness | S003 partial only (incomplete sim), S001 v2 baseline labeled non-v1.4 | user selected hybrid labeled/propose table confirmed | S003 opened 2026-11-09, S001 context labeled non-v1.4 |
| D_DC_DEBUG | DC-op debug fix: stiffer Vref (10k/10k), IN_A biased to Vref, CLIP/ASYM nodes DC-referenced to Vref, HF cap to Vref; provisional | leave broken bias, buffer Vref (not added) | generated ngspice .op showed Vref pulled to ~2.23V and wrong input bias due to loading/provisional wiring | local ngspice .op debug 2026-11-09 |

### Risks

| ID | Risk | Severity | Mitigation | Verification |
| --- | --- | --- | --- | --- |
| K1 | TL082 CM/swing/headroom at 8V condition-dependent | high | SLOS081O + full-topology SPICE/bench at 8/9/18V (D002 open) | A1/C024 follow-up |
| K2 | Clipping wiring/orientation wrong (S002 comment conflict) | high | Mark PROVISIONAL; verify against traceable schematic before fabrication; do not trust sim tone | schematic trace + bench |
| K3 | Many values are placeholders (tone/HP-LP/G2/coupling/caps) | high | Label TBD/proposed; replace with traceable values | source review |
| K4 | APPROX discrete models unverified | high | Simulation-only; obtain manufacturer models for verification | model provenance |
| K5 | Ge/diode/MOSFET behavior varies; asymmetry/tone not guaranteed | medium | D003 options, selection/measurement | A3 sim/listening |
| K6 | DC debug fixes are provisional and may not match real OCD bias topology | medium | verify bias/coupling against traceable schematic; sim/bench | op/DC sweep |

### Sources

| Title | Document / URL | Revision | Accessed |
| --- | --- | --- | --- |
| Circuit Analysis: Fulltone's OCD | https://www.analogisnotdead.com/article34/circuit-analysis-fulltone-s-ocd | n/a | 2026-11-09 |
| OCD overdrive clone (my very first pedal) | http://zadvitsky.com/index.php/projects/pedals/ocd-overdrive-diy.html | n/a | 2026-11-09 |
| TL082 product/datasheet (SLOS081O) | https://www.ti.com/product/TL082 | SLOS081O Rev O | 2026-11-09 |
| Explicit WDF Model of Fulltone OCD (OCD v2 context) | https://dafx.de/paper-archive/2026/papers/DAFx26_paper_24.pdf | 2026 | 2026-11-09 |
| User reconciliation lock | local:conversation/2026-11-09 | n/a | 2026-11-09 |

## Components

| Ref | Type | Value | Pins | Notes |
| --- | --- | --- | --- | --- |
| V1 | V | 9 V | 1=VCC, 2=GND | Nominal 9V; design range 8-18V (C022) |
| V_IN | V | SIN source | 1=IN_SIG, 2=GND | Test input; SIN for tran (AC mag may need manual netlist tweak if AC sim required) |
| R_V1 | R | 10k | 1=VCC, 2=VREF | Vref divider stiffened for draft (10k/10k=5k Thevenin); value proposed |
| R_V2 | R | 10k | 1=VREF, 2=GND | Vref divider stiffened for draft |
| C_VREF | C | 10u | 1=VREF, 2=GND | Vref filter proposed |
| C_IN | C | 22n | 1=IN_SIG, 2=IN_A | Input coupling provisional (S003 role) |
| R_IN_BIAS | R | 1Meg | 1=IN_A, 2=VREF | Bias non-inv input to Vref (provisional single-supply bias); R_INREF-to-GND removed in DC debug |
| U1A | OPAMP | TL082 | 1=IN_A, 2=G1_FB, 3=VCC, 4=GND, 5=G1_OUT | Gain 1, TL082 candidate (D002/C024) |
| R_G1 | R | 2.2k | 1=G1_FB, 2=VREF | S003 gain formula: Rg=2.2k (refdes mapping provisional) |
| R_G1F | R | 18k | 1=G1_FB, 2=DRV_W | S003 gain formula: fixed 18k (provisional mapping) |
| R_DRV_MID | R | 500k | 1=DRV_W, 2=G1_OUT | Drive pot modeled at 50% (1M pot => 500k); variable in real circuit. S003 uses 1M in max gain. |
| C_G1HF | C | 220p | 1=G1_OUT, 2=G1_FB | HF stability cap proposed (S002 C6 role) |
| R_CLIP | R | 10k | 1=G1_OUT, 2=CLIP_NODE | Series into clipping (S002 R9 role); value TBD |
| C_CLIP_HF | C | 100n | 1=CLIP_NODE, 2=VREF | HF placeholder referenced to VREF (DC debug); placement/value TBD |
| R_CLIP_BIAS | R | 100k | 1=CLIP_NODE, 2=VREF | DC debug: bias clip node to VREF (provisional) |
| Q1 | NMOS | APPROX_2N7000 | 1=CLIP_NODE, 2=CLIP_NODE, 3=VREF | PROVISIONAL WIRING (S002 text assumed; S002 comment conflict). D-G tied as diode-like element; uses APPROX subckt body diode path. VERIFY orientation. |
| Q2 | NMOS | APPROX_2N7000 | 1=VREF, 2=VREF, 3=ASYM_NODE | PROVISIONAL WIRING (conflict). VERIFY orientation. |
| D_ASYM | D | APPROX_BAT46 | 1=ASYM_NODE, 2=CLIP_NODE | PROVISIONAL asymmetry element (D003 default BAT46; Ge/1N4148 options). VERIFY orientation/polarity with chosen wiring. |
| R_ASYM | R | 1Meg | 1=ASYM_NODE, 2=VREF | DC debug: reference asym node to VREF, avoid float (provisional) |
| U1B | OPAMP | TL082 | 1=CLIP_NODE, 2=G2_FB, 3=VCC, 4=GND, 5=G2_OUT | Gain 2 recovery placeholder; direct connection from clip node is simplified/provisional |
| R_G2 | R | 10k | 1=G2_FB, 2=VREF | Gain 2 placeholder |
| R_G2F | R | 39k | 1=G2_FB, 2=G2_OUT | Gain 2 ~4.9x placeholder (TBD) |
| R_TONE | R | 10k | 1=G2_OUT, 2=TONE_NODE | Simplified tone placeholder (HP/LP omitted/TBD) |
| C_TONE | C | 47n | 1=TONE_NODE, 2=GND | Simplified tone placeholder |
| C_OUT | C | 1u | 1=TONE_NODE, 2=VOL_TOP | Output coupling placeholder |
| R_VOL | R | 50k | 1=VOL_TOP, 2=VOUT | Volume modeled at 50% (100k pot placeholder) |
| R_VOLG | R | 50k | 1=VOUT, 2=GND | Volume lower leg placeholder |
| R_LOAD | R | 100k | 1=VOUT, 2=GND | Handoff load condition |

## Bill of materials

| Refs | Qty | Type | Value | Footprint |
| --- | --- | --- | --- | --- |
| C_CLIP_HF | 1 | Capacitor | 100n |  |
| C_G1HF | 1 | Capacitor | 220p |  |
| C_IN | 1 | Capacitor | 22n |  |
| C_OUT | 1 | Capacitor | 1u |  |
| C_TONE | 1 | Capacitor | 47n |  |
| C_VREF | 1 | Capacitor | 10u |  |
| D_ASYM | 1 | Diode | APPROX_BAT46 |  |
| Q1 | 1 | N-MOSFET | APPROX_2N7000 |  |
| Q2 | 1 | N-MOSFET | APPROX_2N7000 |  |
| R_ASYM | 1 | Resistor | 1Meg |  |
| R_CLIP | 1 | Resistor | 10k |  |
| R_CLIP_BIAS | 1 | Resistor | 100k |  |
| R_DRV_MID | 1 | Resistor | 500k |  |
| R_G1 | 1 | Resistor | 2.2k |  |
| R_G1F | 1 | Resistor | 18k |  |
| R_G2 | 1 | Resistor | 10k |  |
| R_G2F | 1 | Resistor | 39k |  |
| R_IN_BIAS | 1 | Resistor | 1Meg |  |
| R_LOAD | 1 | Resistor | 100k |  |
| R_TONE | 1 | Resistor | 10k |  |
| R_V1 | 1 | Resistor | 10k |  |
| R_V2 | 1 | Resistor | 10k |  |
| R_VOL | 1 | Resistor | 50k |  |
| R_VOLG | 1 | Resistor | 50k |  |
| U1A | 1 | Op-amp | TL082 |  |
| U1B | 1 | Op-amp | TL082 |  |
| V1 | 1 | Voltage source | 9 V |  |
| V_IN | 1 | Voltage source | SIN source |  |

## Device models

| Ref | Type | Model | Kind | Vendor | Part | SHA256 |
| --- | --- | --- | --- | --- | --- | --- |
| U1A | OPAMP | `TL082` | vendor | Texas Instruments | TL082 (macromodel) | `adad2e131f728610` |
| Q1 | NMOS | `APPROX_2N7000` | vendor | project approximation | 2N7000 (APPROX, exploration only) | `081054dff4a75cb5` |
| Q2 | NMOS | `APPROX_2N7000` | vendor | project approximation | 2N7000 (APPROX, exploration only) | `081054dff4a75cb5` |
| D_ASYM | D | `APPROX_BAT46` | vendor | project approximation | BAT46-class (APPROX, exploration only) | `7b617c80cc7481ad` |
| U1B | OPAMP | `TL082` | vendor | Texas Instruments | TL082 (macromodel) | `adad2e131f728610` |

## Analyses

- `op`
- `dc` (source=V1, start=8, stop=18, step=1)
- `tran` (stop=0.02, step=1e-05)
- `ac` (start=20, stop=20000, points=100)

## Assumptions

- UNVERIFIED hybrid draft - not a Fulltone/OCD clone netlist
- Clipping wiring is PROVISIONAL (S002 text assumed); S002 2026 comment reports alternate M1/M2 wiring - VERIFY before fabrication
- Values are hybrid labeled: S003 explicit gain formula parts + placeholders for completeness
- Drive/Tone/Volume modeled as fixed mid positions for simulation
- HP/LP switch omitted/simplified in this draft
- True bypass is external to SPICE core
- Models: TL082.301 (TI SLOJ070, +/-15V characterized, extrapolative at 8-18V single supply) + APPROX_2N7000/APPROX_BAT46 (unverified) - SIMULATION ONLY
- 8-18V DC supply range (C022); D002 not closed
- DC-op debug pass: Vref 10k/10k, IN_A biased to Vref, CLIP_NODE/ASYM_NODE DC-referenced to Vref, C_CLIP_HF to VREF. Provisional fixes, not verified topology.

## Verification

Status: **PASS**

- [PASS] spec: valid spec with 28 components, 0 warning(s)
- [PASS] models: vendor models supplied
- [PASS] design: 4 requirements, 6 decisions, 6 risks, 5 sources
- [PASS] spice_netlist: 28 devices, node lists match the spec
- [PASS] ltspice_asc: 28 symbols; every pin has a matching net flag
- [PASS] kicad_netlist: 15 nets match the spec exactly
- [SKIP] kicad_schematic: kiutils is not installed; schematic geometry not parsed (set PYTHONPATH to a kiutils checkout)
- [SKIP] pcb_handoff: not generated (add "pcb" to deliverables)
- [SKIP] mna_linear: circuit contains nonlinear element(s) Q1, Q2, D_ASYM; MNA only solves linear circuits
- [PASS] ngspice: ngspice ran 4 analysis plot(s): AC Analysis, DC transfer characteristic, Operating Point, Transient Analysis; V(vcc)=9, V(in_sig)=0, V(vref)=4.49719, V(in_a)=4.49715, V(xu1a.11)=0.345445, V(xu1a.12)=0.345458, V(xu1a.6)=1.184e-06, V(xu1a.7)=4.49165, V(g1_out)=4.49166, V(xu1a.53)=6.8, V(xu1a.54)=2.2, V(xu1a.90)=-6.46255e-05, V(xu1a.91)=25, V(xu1a.92)=-25, V(xu1a.99)=4.5, V(xu1a.10)=4.09857, V(g1_fb)=4.49716, V(xu1a.9)=0, V(xu1a.8)=4.49165, V(drv_w)=4.49697, V(clip_node)=4.4922, V(asym_node)=4.49327, V(xu1b.11)=0.345454, V(xu1b.12)=0.345467, V(xu1b.6)=3.87331e-06, V(xu1b.7)=4.47272, V(g2_out)=4.4728, V(xu1b.53)=6.8, V(xu1b.54)=2.2, V(xu1b.90)=-0.000497758, V(xu1b.91)=25, V(xu1b.92)=-25, V(xu1b.99)=4.5, V(xu1b.10)=4.09363, V(g2_fb)=4.49221, V(xu1b.9)=0, V(xu1b.8)=4.47272, V(tone_node)=4.4728, V(vol_top)=0, V(vout)=0

## Files

- `spice`: `ocd_v1p4_v0p3_hybrid_draft.cir`
- `models`: `ocd_v1p4_v0p3_hybrid_draft.models`
- `ltspice_asc`: `ocd_v1p4_v0p3_hybrid_draft.asc`
- `kicad_net`: `ocd_v1p4_v0p3_hybrid_draft.net`
- `kicad_sch`: `ocd_v1p4_v0p3_hybrid_draft.kicad_sch`
- `bom`: `ocd_v1p4_v0p3_hybrid_draft-bom.csv`

> The generated SPICE netlist is the electrical source of truth. The schematics are drawn from the same component list and use net labels at every pin instead of routed wires.

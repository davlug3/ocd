# ocd_v0p4_8v18v

OCD-style overdrive v0.4: S002-verified topology + user node connections; 8-18V DC center-negative, 9V nominal. D_FB_FIX moves C4/C8 in series with R5/R11 (the prior parallel placement saturated both op-amps). Adds 1N5819 protection, status LED, 9V battery/DC-jack provision, and an explicit HP/LP SW1. Not a verified Fulltone netlist; 2N7000/1N34A/1N5819 models are approximations.

- Topology: `ocd_v0p4_8v18v`
- Ground: `GND`
- Generated: 2026-11-11
- Simulation status: **declared models (no vendor provenance)**

## Supplies

- `VCC_JACK` = 9.0 V

## Design record

VCC_JACK -> D_PWR(1N5819) -> VCC -> R1/C2/C3 -> VCC_F; Vref divider; input C1/R2/R6/R3; X1 gain (R5+C4 series, R8/Drive, C6); clip R9/C7/R10/R12/M1/M2/D1; X3 gain (R11+C8 series, R13, C9); tone/HP-LP (R14/R15/SW1); volume; LED; true bypass.

**Blocks:** power_entry; protection; power_filter; vref; input_bias; gain1; clip_vref; gain2; tone_hplp; volume; led; bypass

**Interfaces:** IN; OUT; VCC_JACK; VBAT; GND

**Test points:** VCC_JACK; VCC; VCC_F; VREF; IN_B; X1_FB; X1_OUT; CLIP_A; CLIP_B; X3_FB; X3_OUT; TONE_W; VOL_TOP; OUT; LED_A

| Budget | Value |
| --- | --- |
| vref | VCC_F/2 +/-5% |
| headroom | +/-2.09V at 8V, +/-2.54V at 9V, +/-6.45V at 18V (TL082 typ 1.5V rail headroom; model VCC_F) |
| supply_current | TL082 model 8.4mA at 9V, 16.6mA at 18V; datasheet 2.8mA typ |

### Requirements

| ID | Requirement | Acceptance | Source |
| --- | --- | --- | --- |
| E1 | Operate from 8-18V DC center-negative at the jack with series reverse-polarity protection; the protected/filtered rail VCC_F must keep the TL082 within its 7-30V total-supply range. | At 8V jack, VCC_F >= 7.0V; at 18V jack, VCC_F <= 30V; reverse polarity draws no current and causes no damage (current-limited test). | S007, S009 |
| E2 | Vref = VCC_F/2 within +/-5% at 8/9/18V and stable under signal. | Measured VREF 3.59/4.04/7.95V nominal at 8/9/18V, +/-5%; no shift or oscillation under drive. | S002, S007 |
| E3 | Both TL082 stages have unity DC gain and no quiescent saturation. | X1_OUT ~= X1_P and X3_OUT ~= X3_P; neither output at a rail at 8/9/18V. | S002, simulation |
| E4 | SW1 selects R14 only (LP, darker) or R14 in parallel with R15 (HP, brighter). | Repeatable HP/LP frequency-response difference at 1kHz with Drive/Tone/Volume fixed; no oscillation. Parallel position is brighter per S003. | S002, S003 |
| E5 | Status LED with series resistor from VCC_F to GND, 1-5mA at 8-18V. | LED on; measured current 1-5mA. | S009 |
| E6 | 9V battery option with a switching DC jack and input-jack battery disconnect. | Battery disconnects when the DC plug is inserted; no battery drain when the input jack is unplugged. | S009 |
| E7 | True bypass with a 3PDT; dry signal passes when off. | Continuity/audio check; active circuit isolated when off. | S009 |
| E8 | PCB-mounted 1/4-inch TS jacks and 3PDT; 1590B enclosure, 108 x 58mm board, through-hole (Phase C). | Test fit in 1590B; jack/switch alignment and board dimensions verified (Phase C). | S009 |
| A1 | Operate from 8-18V DC center-negative | No damage/oscillation; functional audio at 8V, 9V, and 18V into 100k load under stated conditions (50mVpk, 1kHz; 20Hz-20kHz) | S009 |
| A2 | True bypass | Dry signal passed when off; active circuit isolated per implementation | S009 |
| A3 | Asymmetric OCD-style clipping character with HP/LP voicing | Qualitative + simulation waveform/spectrum under stated conditions (exploratory); not a verified Fulltone clone claim | S001 |
| A4 | Stable bias with no low-frequency instability (hum, motorboating, or oscillation) at 8/9/18V | Audible/measured: no hum, motorboating, or oscillation at 8/9/18V; bias stable under signal. Circuit-level VREF = VCC_F/2 is verified under E2. | S002 |
| A5 | Drive/Volume control range and output level | Measure gain at 1kHz and output level at Drive/Volume extremes; exploratory pending a verified reference | S002 |
| A6 | HP/LP voicing is selectable and audibly different | Repeatable frequency-response difference between HP and LP at the same Drive/Tone/Volume; no oscillation | S002 |

### Decisions

| ID | Decision | Alternatives | Rationale | Sources |
| --- | --- | --- | --- | --- |
| D_V1 | 8-18V DC center-negative at the jack; 9V nominal test. |  | User intake; TL082 total-supply maximum is 30V (S007). | S009, S007 |
| D_CLIP_V1 | Clip network M1/M2/D1 wiring per the S002 schematic image. |  | The image confirms M1[D&G=VREF,S=CLIP_A], M2[D=VREF,G&S=M2_D1_NODE], D1[A=CLIP_A,K=M2_D1_NODE]. | S002 |
| D_POTS | X2 Drive 1M audio, X5 Volume 100k audio provisional, X4 Tone 10k audio wired as a rheostat in series with C11 to ground; 50% linear snapshot in simulation. |  | S002 gives the pot values and confirms X4 sends treble through the 10k pot and C11 to ground. Tapers and the X5 value are unverified. | S002, S003 |
| D_DEV | TL082 vendor model; 2N7000/1N34A project approximations; 1N5819/LED/SW ideal models. |  | Only the TL082 has a vendor macromodel; the rest are simulation-only approximations and the models gate is SKIP. | S007, S002 |
| D_BIAS_FIX | Keep R2 to GND, R6 to VREF, and D1 as 1N34A; do not add a second Ge diode. |  | S002 text and image confirm this bias arrangement. | S002 |
| D_TONE | Tone/HP-LP: R14 22k always in path; R15 33k in parallel only when SW1 is closed (HP); SW1 open = LP. |  | S002 confirms R14/R15 values. S003 states the switch-on position parallels R12/R13 (R14/R15 here) reducing high-frequency loss, i.e. brighter; AGENTS.md defines HP as brighter/more presence. So HP=closed/parallel, LP=open. Reverses the provisional D_TONE label. | S002, S003 |
| D_FB_FIX | Move C4 in series with R5 (X1_FB -> X1_RG -> VREF) and C8 in series with R11 (X3_FB -> X3_RG -> VREF). |  | The prior parallel placement gave zero DC feedback and saturated both op-amps. Series placement gives unity DC gain and the intended AC bass limit. 8/9/18V OP after the fix: VREF 3.588/4.039/7.947V; X1_OUT 2.441/2.747/5.406V; X3_OUT 2.538/2.857/5.905V. | S002, simulation |
| D_PROT | 1N5819 series Schottky reverse-polarity protection; P-FET fallback if the 8V margin fails. |  | Simple and low-drop. At 8V jack the TL082 sees about 7.7V real (about 7.25V with the pessimistic model), leaving roughly 0.7V above the 7V minimum; bench gate. | S007, S014 |
| D_LED | LED + 4.7k from VCC_F to GND; always-on in simulation; physically switched by the 3PDT. |  | Status indicator at 1.35mA/9V and about 3mA/18V. | S009 |
| D_BAT | 9V battery via a switching DC jack and input-jack battery disconnect. |  | User requirement; prevents battery drain when unplugged. | S009 |
| D_AC_SRC | Split V_IN (SIN) and V_AC (AC 1V) in series because the generator drops AC when a waveform is present. |  | AC metrics need excitation while transient needs a sine. Verified AC gain at 1kHz/9V after the fix: OUT 37.2dB, X1_OUT 43.1dB, X3_OUT 54.5dB. | simulation |
| D_MODEL_LIMITS | Use datasheet TL082 limits for headroom and the vendor model for AC/clipping shape; model supply current is not trustworthy. |  | The TL082 model draws 8.4mA at 9V and 16.6mA at 18V vs about 2.8mA real, inflating the R1 drop. | S007 |
| D_PCB_MECH | 1590B enclosure, 108 x 58mm board, through-hole, PCB-mounted I/O jacks and 3PDT (Phase C). |  | User decision; PCB work is deferred. | S009 |
| D_PRIOR_SIM | Prior AC/THD/Vref results are superseded. |  | The old netlist had C4/C8 in parallel (saturated bias) and V_IN without an AC magnitude (zero AC excitation). | simulation |

### Risks

| ID | Risk | Severity | Mitigation | Verification |
| --- | --- | --- | --- | --- |
| K1 | TL082 CM/swing/headroom may be insufficient at 8V single supply (condition/process/temperature dependent) |  | Verify SLOS081O limits (S007) + provenance-tracked SPICE/bench at 8/9/18V; substitute only with datasheet/SPICE provenance and a recorded decision (D002) | A1, E1-E3, DC/transient sim, bench |
| K2 | 1N34A Ge diode variability shifts clipping symmetry/threshold |  | Select/measure diodes or design for tolerance; D003 allows BAT46/1N4148 options with provenance | A3 sim/listening |
| K3 | Exact schematic values/orientation not a verified Fulltone netlist |  | Hybrid working reference S002+S003 cross-checked with S001/S013; label unverified items; confirm pin-level values/orientation against traceable schematic+datasheets before fabrication | design review |
| K4 | 1N5819 drop plus the TL082 7V minimum leaves only about 0.7V at an 8V jack |  | Bench-gate 8V operation; fall back to a P-FET reverse-polarity circuit if the margin fails | E1, 8V bench, DC sweep |
| K5 | The TL082 model supply current is about 3-6x the datasheet value, so simulated VCC_F/headroom is pessimistic |  | Use datasheet limits for headroom decisions; record the model artifact | S007 comparison |
| K6 | PCB-mounted 3PDT/jack mechanical alignment and the SW1 physical SPDT mapping are unproven |  | Phase C mechanical fit check in a 1590B; confirm footprint pad positions and switch mapping before fabrication | E8, Phase C |
| K7 | X2/X5 values, wiring and tapers are unverified. | medium | Confirm against a traceable schematic/photo; mark the 50% linear simulation snapshot. | E4, A5 |
| K8 | The voltage-controlled SW1 model has four nodes but the physical HP/LP switch is a three-terminal SPDT. | high | Define the physical pad mapping in Phase C; keep the control pins simulation-only. | E4, Phase C |
| K9 | AC/THD/noise metrics are exploratory; there is no verified reference target. | medium | Record conditions and model provenance; do not claim a verified clone performance. | A3/A5 metrics, bench |

### Sources

| Title | Document / URL | Revision | Accessed |
| --- | --- | --- | --- |
| DAFx26 OCD Wave Digital Model (cross-check; OCD v2 context) | https://dafx.de/paper-archive/2026/papers/DAFx26_paper_24.pdf |  | 2026-11-09 |
| Analog Is Not Dead - OCD analysis (opened this session) | https://www.analogisnotdead.com/article34/circuit-analysis-fulltone-s-ocd |  | 2026-11-09 |
| zadvitsky OCD overdrive clone (opened this session, partial values) | http://zadvitsky.com/index.php/projects/pedals/ocd-overdrive-diy.html |  | 2026-11-09 |
| TI TL082 datasheet/product (SLOS081O, opened this session) | https://www.ti.com/lit/gpn/TL082 |  | 2026-11-11 |
| User intake/reconciliation v0.1 | local:conversation/2026-11-09 |  | 2026-11-09 |
| PCB Guitar Mania TOC (OCD) v2.1 build docs (authorized, cross-check) | https://pcbguitarmania.com/wp-content/uploads/2018/02/TOC-2v1-Building-Docs.pdf |  | 2026-11-09 |
| Vishay 1N5817/1N5818/1N5819 Schottky datasheet | https://www.vishay.com/docs/88525/1n5817.pdf |  | 2026-11-11 |

## Components

| Ref | Type | Value | Tolerance | Pins | Notes |
| --- | --- | --- | --- | --- | --- |
| V1 | V | 9 V | — | 1=VCC_JACK, 2=GND | 9V nominal test at the DC jack; design range 8-18V DC center-negative (C022). D_PWR and R1 drop before the op-amp rail. |
| V_IN | V | SIN source | — | 1=IN, 2=IN_SRC | Transient excitation 50mVpk/1kHz. AC excitation is V_AC because the generator drops AC when a waveform is present. |
| V_AC | V | 0 V | — | 1=IN_SRC, 2=GND | AC excitation 1V for .ac/.noise. Simulation-only; in series with V_IN. Workaround for the generator dropping AC on a waveform source. |
| D_PWR | D | APPROX_1N5819 | — | 1=VCC_JACK, 2=VCC | Series Schottky reverse-polarity protection; 1N5819 default. APPROX model; Vf ~0.25-0.3V. 8V-jack margin to the TL082 7V minimum is a bench gate (D_PROT). |
| R1 | R | 100 | — | 1=VCC, 2=VCC_F | S002-schematic-image-confirmed: supply feed/filter node (R1=100ohm), now after D_PWR protection. |
| C2 | C | 10u | — | 1=VCC_F, 2=GND | S002-schematic-image-confirmed: power bulk filter (C2=10µF). |
| C3 | C | 100n | — | 1=VCC_F, 2=GND | S002-schematic-image-confirmed: power HF decoupling (C3=100nF). |
| R4 | R | 10k | — | 1=VCC_F, 2=VREF | S002-schematic-image-confirmed: Vref divider upper (R4=10k). |
| R7 | R | 10k | — | 1=VREF, 2=GND | S002-schematic-image-confirmed: Vref divider lower (R7=10k). |
| C5 | C | 10u | — | 1=VREF, 2=GND | S002-schematic-image-confirmed: Vref filter cap (C5=10µF). |
| C1 | C | 22n | — | 1=IN, 2=IN_B | S002-schematic-image-confirmed: input coupling cap (C1=22nF). |
| R2 | R | 1Meg | — | 1=IN_B, 2=GND | S002-schematic-image-confirmed: R2 (1M) connects input cap C1 to GROUND as voltage reference, not to VREF. R6 biases op-amp to VREF. |
| R6 | R | 470k | — | 1=IN_B, 2=VREF | S002-schematic-image-confirmed: biases op-amp non-inverting input to VREF (R6=470k). |
| R3 | R | 10k | — | 1=IN_B, 2=X1_P | S002-schematic-image-confirmed: limits current to op-amp input (R3=10k). |
| X1A | OPAMP | TL082 | — | 1=X1_P, 2=X1_FB, 3=VCC_F, 4=GND, 5=X1_OUT | TL082 section 1; wiring assumed |
| R5 | R | 2.2k | — | 1=X1_FB, 2=X1_RG | S002-confirmed value R5=2.2k. D_FB_FIX: R5 is in series with C4 to VREF so the stage has unity DC gain and an AC bass limit. |
| R8 | R | 18k | — | 1=X1_FB, 2=X2_W | S002-schematic-image-confirmed: gain network (R8=18k). |
| R_X2POT | R | 500k | — | 1=X2_W, 2=X1_OUT | Drive/gain pot modeled 50% of 1M (S002 states gain pot 1M; mapping/wiring assumed). |
| C4 | C | 100n | — | 1=X1_RG, 2=VREF | S002-confirmed C4=100nF. D_FB_FIX: C4 is in series with R5, not in parallel with it; the parallel placement had zero DC feedback and saturated X1. |
| C6 | C | 220p | — | 1=X1_OUT, 2=X1_FB | S002-schematic-image-confirmed: HF stability cap (C6=220pF). |
| R9 | R | 10k | — | 1=X1_OUT, 2=CLIP_A | S002-schematic-image-confirmed: series into clipping (R9=10k). |
| C7 | C | 10n | — | 1=VREF, 2=CLIP_A | S002-schematic-image-confirmed: VREF-CLIP_A cap (C7=10nF). |
| R10 | R | 10k | — | 1=CLIP_A, 2=CLIP_B | S002-schematic-image-confirmed: clip network resistor (R10=10k). |
| R12 | R | 220k | — | 1=VREF, 2=CLIP_B | S002-schematic-image-confirmed: bias to CLIP_B (R12=220k). |
| M1 | NMOS | APPROX_2N7000 | — | 1=VREF, 2=VREF, 3=CLIP_A | S002-schematic-image-confirmed: M1 [D&G=VREF, S=CLIP_A]. Exact part unknown; APPROX sim-only. Commenter-reported alternate wiring (M1[S=VREF,D&G=R9/R10]) does NOT match S002 image. |
| M2 | NMOS | APPROX_2N7000 | — | 1=VREF, 2=M2_D1_NODE, 3=M2_D1_NODE | S002-schematic-image-confirmed: M2 [D=VREF, G&S=M2_D1_NODE]. Exact part unknown; APPROX sim-only. Commenter-reported alternate wiring (M2[D&G=VREF,S=D1]) does NOT match S002 image. |
| D1 | D | APPROX_1N34A | — | 1=CLIP_A, 2=M2_D1_NODE | S002-schematic-image-confirmed: D1 [A=CLIP_A, K=M2_D1_NODE], 1N34A Ge per article text (C027). APPROX sim-only model, Ge variability applies. |
| X3A | OPAMP | TL082 | — | 1=CLIP_B, 2=X3_FB, 3=VCC_F, 4=GND, 5=X3_OUT | S002-schematic-image-confirmed: TL082 section 2; non-inv input CLIP_B; wiring assumed. |
| R11 | R | 39k | — | 1=X3_FB, 2=X3_RG | S002-confirmed R11=39k. D_FB_FIX: R11 is in series with C8 to VREF so the stage has unity DC gain. |
| R13 | R | 150k | — | 1=X3_FB, 2=X3_OUT | S002-schematic-image-confirmed: feedback (R13=150k). |
| C8 | C | 100n | — | 1=X3_RG, 2=VREF | S002-confirmed C8=100nF. D_FB_FIX: C8 is in series with R11, not in parallel with it; the parallel placement had zero DC feedback and saturated X3. |
| C9 | C | 220p | — | 1=X3_OUT, 2=X3_FB | S002-schematic-image-confirmed: HF stability (C9=220pF). |
| C10 | C | 10u | — | 1=X3_OUT, 2=TONE_TOP | S002-schematic-image-confirmed: output coupling cap (C10=10µF). |
| R_X4 | R | 5k | — | 1=TONE_TOP, 2=TONE_W | S002 tone pot X4=10k wired as a rheostat in series with C11 to ground (treble passes through X4 then C11). 50% snapshot=5k; BOM part is a 10k pot. |
| C11 | C | 47n | — | 1=TONE_W, 2=GND | S002-schematic-image-confirmed: tone cap C11 to ground (C11=47nF). |
| R14 | R | 22k | — | 1=TONE_TOP, 2=VOL_TOP | S002-confirmed R14=22k. Main signal path from TONE_TOP (after C10) to VOL_TOP; always in circuit (LP=open, darker). |
| R15 | R | 33k | — | 1=TONE_TOP, 2=SW1_1 | S002-confirmed R15=33k. Switched in parallel with R14 via SW1 from TONE_TOP to VOL_TOP; HP=closed/parallel=brighter (S003), LP=open/darker. |
| SW1 | SW | SW1MODEL | — | 1=SW1_1, 2=VOL_TOP, 3=HP_CTRL, 4=GND | HP/LP toggle modeled as a voltage-controlled switch. HP = closed (V_HP=5V) -> R15 parallel with R14 (brighter); LP = open (V_HP=0V) -> R14 only (darker). Physical part is an SPDT; PCB pad mapping is Phase C. |
| V_HP | V | 5 V | — | 1=HP_CTRL, 2=GND | Simulation-only switch control. 5V = HP (SW1 closed, parallel, brighter); change to 0V for the LP variant. |
| R_VOL5A | R | 50k | — | 1=VOL_TOP, 2=OUT | Volume pot 100k modeled at 50% (X5 value not found in retrieved S002 text; 100k is placeholder). |
| R_VOL5B | R | 50k | — | 1=OUT, 2=GND | Volume pot lower leg modeled at 50% (X5 value not found in retrieved S002 text; 100k is placeholder). |
| R_LOAD | R | 100k | — | 1=OUT, 2=GND |  |
| R_LED | R | 4.7k | — | 1=VCC_F, 2=LED_A | Status LED series resistor; 1.35mA at 9V, ~3mA at 18V (Vf 1.8V). Physical LED switching is via the 3PDT (D_LED). |
| D_LED | LED | LED_RED | — | 1=LED_A, 2=GND | Status LED, 1.8V red generic model. Always-on in simulation; physically switched by the 3PDT. |

## Bill of materials

| Refs | Qty | Type | Value | Footprint |
| --- | --- | --- | --- | --- |
| C1 | 1 | Capacitor | 22n |  |
| C10 | 1 | Capacitor | 10u |  |
| C11 | 1 | Capacitor | 47n |  |
| C2 | 1 | Capacitor | 10u |  |
| C3 | 1 | Capacitor | 100n |  |
| C4 | 1 | Capacitor | 100n |  |
| C5 | 1 | Capacitor | 10u |  |
| C6 | 1 | Capacitor | 220p |  |
| C7 | 1 | Capacitor | 10n |  |
| C8 | 1 | Capacitor | 100n |  |
| C9 | 1 | Capacitor | 220p |  |
| D1 | 1 | Diode | APPROX_1N34A |  |
| D_LED | 1 | LED | LED_RED |  |
| D_PWR | 1 | Diode | APPROX_1N5819 |  |
| M1 | 1 | N-MOSFET | APPROX_2N7000 |  |
| M2 | 1 | N-MOSFET | APPROX_2N7000 |  |
| R1 | 1 | Resistor | 100 |  |
| R10 | 1 | Resistor | 10k |  |
| R11 | 1 | Resistor | 39k |  |
| R12 | 1 | Resistor | 220k |  |
| R13 | 1 | Resistor | 150k |  |
| R14 | 1 | Resistor | 22k |  |
| R15 | 1 | Resistor | 33k |  |
| R2 | 1 | Resistor | 1Meg |  |
| R3 | 1 | Resistor | 10k |  |
| R4 | 1 | Resistor | 10k |  |
| R5 | 1 | Resistor | 2.2k |  |
| R6 | 1 | Resistor | 470k |  |
| R7 | 1 | Resistor | 10k |  |
| R8 | 1 | Resistor | 18k |  |
| R9 | 1 | Resistor | 10k |  |
| R_LED | 1 | Resistor | 4.7k |  |
| R_LOAD | 1 | Resistor | 100k |  |
| R_VOL5A | 1 | Resistor | 50k |  |
| R_VOL5B | 1 | Resistor | 50k |  |
| R_X2POT | 1 | Resistor | 500k |  |
| R_X4 | 1 | Resistor | 5k |  |
| SW1 | 1 | Analog switch | SW1MODEL |  |
| V1 | 1 | Voltage source | 9 V |  |
| V_AC | 1 | Voltage source | 0 V |  |
| V_HP | 1 | Voltage source | 5 V |  |
| V_IN | 1 | Voltage source | SIN source |  |
| X1A | 1 | Op-amp | TL082 |  |
| X3A | 1 | Op-amp | TL082 |  |

## Device models

| Ref | Type | Model | Kind | Vendor | Part | SHA256 |
| --- | --- | --- | --- | --- | --- | --- |
| D_PWR | D | `APPROX_1N5819` | declared |  |  | `` |
| X1A | OPAMP | `TL082` | vendor | Texas Instruments | TL082 (macromodel) | `adad2e131f728610` |
| M1 | NMOS | `APPROX_2N7000` | declared |  | 2N7000 APPROX sim-only | `081054dff4a75cb5` |
| M2 | NMOS | `APPROX_2N7000` | declared |  | 2N7000 APPROX sim-only | `081054dff4a75cb5` |
| D1 | D | `APPROX_1N34A` | declared |  | 1N34A Ge APPROX sim-only (S002-confirmed D1 type) | `db949f2074c80243` |
| X3A | OPAMP | `TL082` | vendor | Texas Instruments | TL082 (macromodel) | `adad2e131f728610` |
| SW1 | SW | `SW1MODEL` | declared |  |  | `` |
| D_LED | LED | `LED_RED` | declared |  |  | `` |

## Analyses

- `op`
- `dc` (source=V1, start=8.0, stop=18.0, step=1.0)
- `tran` (step=1e-05, stop=0.03)
- `fourier` (fundamental=1000.0, output=v(out))
- `ac` (start=20.0, stop=20000.0, points=200)
- `noise` (output=OUT, source=V_AC, start=20.0, stop=20000.0, points=100)

## Assumptions

- S002 topology; S003 cross-check; S001/S013 context; not a verified Fulltone netlist.
- TL082 vendor model; 2N7000/1N34A/1N5819/LED/SW models are approximations or ideal. The models gate is SKIP.
- Pots are modeled as 50% linear snapshots; actual tapers/values are unverified.
- HP/LP is modeled as a voltage-controlled SW1; the physical part is an SPDT and PCB mapping is Phase C.
- Battery/DC-jack/3PDT wiring is not simulated; it is bench/PCB Phase C.
- AC excitation is split into V_IN and V_AC; THD/noise are exploratory.

## Warnings

- model 'APPROX_2N7000' has no vendor/part/source provenance; the report will call it declared, not vendor
- model 'APPROX_1N34A' has no vendor/part/source provenance; the report will call it declared, not vendor
- metrics.metrics[0]: exploratory=true ignores the target or limit
- metrics.metrics[1]: exploratory=true ignores the target or limit
- metrics.metrics[2]: exploratory=true ignores the target or limit
- metrics.metrics[3]: exploratory=true ignores the target or limit
- metrics.metrics[4]: exploratory=true ignores the target or limit
- D_PWR (D) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R1 (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- C2 (C) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- C3 (C) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R4 (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R7 (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- C5 (C) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- C1 (C) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R2 (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R6 (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R3 (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- X1A (OPAMP) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R5 (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R8 (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R_X2POT (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- C4 (C) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- C6 (C) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R9 (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- C7 (C) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R10 (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R12 (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- M1 (NMOS) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- M2 (NMOS) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- D1 (D) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- X3A (OPAMP) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R11 (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R13 (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- C8 (C) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- C9 (C) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- C10 (C) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R_X4 (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- C11 (C) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R14 (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R15 (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R_VOL5A (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R_VOL5B (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R_LED (R) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- D_LED (LED) has no footprint; the PCB pipeline will ask for one or fail with --no-ask
- R_LOAD is a boardable part but was explicitly excluded; the PCB will not contain it
- X1A (OPAMP) has no pcb.pin_map entry; the PCB pipeline will ask for a package pinout
- M1 (NMOS) has no pcb.pin_map entry; the PCB pipeline will ask for a package pinout
- M2 (NMOS) has no pcb.pin_map entry; the PCB pipeline will ask for a package pinout
- X3A (OPAMP) has no pcb.pin_map entry; the PCB pipeline will ask for a package pinout

## Verification

Status: **PASS**

- [PASS] spec: valid spec with 44 components, 50 warning(s)
- [SKIP] models: declared models (no vendor provenance); models are declared inline but have no vendor/part/source; record provenance to call them vendor models
- [PASS] design: 14 requirements, 14 decisions, 9 risks, 7 sources
- [PASS] measurement_plan: 8 actionable measurements trace to declared requirements
- [PASS] operating_limits: 5 calculated stresses are within their declared sourced limits
- [PASS] spice_netlist: 44 devices, node lists match the spec
- [PASS] ltspice_asc: 44 symbols; every pin has a matching net flag
- [PASS] kicad_netlist: 26 nets match the spec exactly
- [SKIP] kicad_schematic: kiutils is not installed; schematic geometry not parsed (set PYTHONPATH to a kiutils checkout)
- [SKIP] pcb_handoff: not generated (add "pcb" to deliverables)
- [SKIP] mna_linear: circuit contains nonlinear element(s) D_PWR, M1, M2, D1, SW1, D_LED; MNA only solves linear circuits
- [PASS] ngspice: ngspice ran 6 analysis plot(s): AC Analysis, DC transfer characteristic, Operating Point, Transient Analysis, Noise Spectral Density Curves, Integrated Noise; V(vcc_jack)=9, V(in)=0, V(in_src)=0, V(vcc)=8.75112, V(vcc_f)=7.81275, V(vref)=3.86748, V(in_b)=2.63093, V(x1_p)=2.63093, V(xx1a.11)=0.347612, V(xx1a.12)=0.347671, V(xx1a.6)=0.000180826, V(xx1a.7)=2.6302, V(x1_out)=2.631, V(xx1a.53)=5.61275, V(xx1a.54)=2.2, V(xx1a.90)=-0.00530625, V(xx1a.91)=25, V(xx1a.92)=-25, V(xx1a.99)=3.90638, V(xx1a.10)=2.23428, V(x1_fb)=2.63098, V(xx1a.9)=0, V(xx1a.8)=2.6302, V(x1_rg)=2.63098, V(x2_w)=2.63098, V(clip_a)=2.68406, V(clip_b)=2.73551, V(m2_d1_node)=2.68408, V(xx3a.11)=0.347434, V(xx3a.12)=0.347489, V(xx3a.6)=0.000165792, V(xx3a.7)=2.73557, V(x3_out)=2.73557, V(xx3a.53)=5.61275, V(xx3a.54)=2.2, V(xx3a.90)=3.04378e-08, V(xx3a.91)=25, V(xx3a.92)=-25, V(xx3a.99)=3.90638, V(xx3a.10)=2.3387, V(x3_fb)=2.73556, V(xx3a.9)=0, V(xx3a.8)=2.73557, V(x3_rg)=2.73556, V(tone_top)=0, V(tone_w)=0, V(vol_top)=0, V(sw1_1)=0, V(hp_ctrl)=5, V(out)=0, V(led_a)=1.66634
- [PASS] metrics: M1: gain_db=44.5706 dB (INFO; exploratory); M2: bandwidth_width_hz=1368.55 Hz (INFO; exploratory); M3: thd_percent=66.3437 % (INFO; exploratory); M4: noise_uv=141.417 uV (INFO; exploratory); M5: output_vrms=0.69027 V (INFO; exploratory)
- [SKIP] kicad_pcb_drc: actual PCB file not found (ocd_v0p4_8v18v.kicad_pcb); PCB handoff is not a board
- [PASS] required:design: stage 'design' required and passed (design)
- [PASS] required:limits: stage 'limits' required and passed (operating_limits)
- [PASS] required:measurements: stage 'measurements' required and passed (measurement_plan)
- [PASS] required:simulate: stage 'simulate' required and passed (ngspice)

## Files

- `spice`: `ocd_v0p4_8v18v.cir`
- `models`: `ocd_v0p4_8v18v.models`
- `ltspice_asc`: `ocd_v0p4_8v18v.asc`
- `kicad_net`: `ocd_v0p4_8v18v.net`
- `kicad_sch`: `ocd_v0p4_8v18v.kicad_sch`
- `bom`: `ocd_v0p4_8v18v-bom.csv`
- `test_plan`: `ocd_v0p4_8v18v-test-plan.md`

> The generated SPICE netlist is the electrical source of truth. The schematics are drawn from the same component list and use net labels at every pin instead of routed wires.

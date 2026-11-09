# AGENTS.md — Fulltone OCD Clone (Descriptive Design Guide)

## Project purpose
Design and build a **faithful electrical clone** of the Fulltone OCD (Obsessive Compulsive Drive) overdrive pedal. This document is the project’s working guide: it explains the **physical, electronic, musical, and audio** concepts behind the circuit, records what is **verified vs. unverified**, and defines how to move from idea to schematic, simulation, and PCB using the local skills.

> **Scope boundary:** This is an engineering/design guide. It is not legal advice about trademarks, trade dress, or branding. A clone should avoid copying protected branding/artwork and should be described honestly (e.g., “OCD-style overdrive”).

## Skills available (in `~/.agents/skills/`)
Use these skills in order; each owns a different layer of truth.

| Skill | Owns | Key outputs |
|---|---|---|
| `audio-engineering-skill` | Audio targets, conditions, budgets, measurement/listening plans, evidence, handoff contract | `audio-requirements.md`, budgets, `handoff.json` |
| `circuit-design-skill` | Electrical implementation: parts, sizing, netlist, LTspice/KiCad schematics, SPICE models, simulation, verification | design spec, `.cir`, `.asc`, `.kicad_sch`, BOM, verification report |
| `pcb-design-skill` | Physical board: footprints, placement, routing, stackup/rules, DRC/DFM, fabrication outputs | `.kicad_pcb`, Gerbers/drill, DRC/DFM report |

**Non-overlap rule:** Do not invent audio targets in the circuit skill, and do not claim PCB manufacturability or measured performance without the corresponding skill’s checks/evidence.

## Target revision (lock before schematic capture)
- **Primary target:** OCD v1.4 / v1.7 topology (widely documented, commonly cloned).
- **Optional variant:** v2/v2.01-style front end (JFET input buffer) + selectable True/Enhanced Bypass.
- **Why lock this:** Component values, buffering, and construction (through-hole vs. SMT) vary across revisions. “OCD” is not one fixed schematic.

## Physical concepts (mechanics, enclosure, controls, interfaces)

### Enclosure and form factor
A typical OCD-style pedal is a small stompbox enclosure (commonly a “1590B/125B-class” footprint in clones) housing:
- **Top panel controls:** 3 knobs (Volume, Drive, Tone) and 1 toggle (HP/LP).
- **Footswitch:** momentary or latching switch implementing bypass (true bypass or buffered/bypass-selectable depending on revision).
- **Jacks:** 1/4" TS input and output (instrument-level, unbalanced).
- **Power:** 9V DC center-negative barrel jack (Boss-style). Some versions tolerate up to 18V.
- **Optional battery:** 9V battery compartment (earlier/through-hole layouts).

**Physical design constraints that affect electronics/audio:**
- **Knob/switch placement** determines wiring length and noise pickup risk.
- **Jack isolation** (insulated vs. chassis-grounded) affects ground loops and hum.
- **Enclosure shielding** (metal enclosure tied to circuit ground strategy) affects RF/EMI pickup.
- **Footswitch wiring** (true bypass) routes the full instrument signal; poor wiring/layout can add noise or pops.
- **Thermal/mechanical**: op-amps and regulators (if present) dissipate little in a typical 9V overdrive, but cramped layouts can still couple noise.

### User interface (what the player physically manipulates)
| Control | Physical action | Electrical effect | Musical/audible effect |
|---|---|---|---|
| **Volume** | Rotates pot | Sets output level (post-clipping/tone network, implementation-dependent) | Overall loudness; can push an amp harder |
| **Drive** | Rotates pot | Sets first-stage gain/feedback ratio | Clean → edge-of-breakup → saturated overdrive |
| **Tone** | Rotates pot | Passive treble attenuation (treble-bleed style) | Darker/warmer ↔ brighter/cutting |
| **HP/LP** | Toggles switch | Changes HF/voicing network resistance/capacitance interaction | HP = more presence/upper-mid bite and perceived openness; LP = flatter/more transparent |
| **Footswitch** | Press | Engages/bypasses effect | On-demand grit/dynamics |

### Signal path as a physical journey
An unbalanced guitar signal enters the **input jack**, travels through wiring/PCB traces to the **input buffer or first gain stage**, is amplified and clipped, shaped by tone controls, buffered/attenuated to the **output jack**, and returns through the amp cable. Every physical connection (jack, switch lug, pot wiper, solder joint) is also a potential failure point, noise source, or impedance discontinuity.

## Electronic concepts (how the circuit works)

### 1) Power supply, ground, and the virtual reference (Vref)
Most OCD-style clones run from a **single 9V supply** (battery or DC adapter). Op-amps need a way to handle AC audio signals that swing above and below a reference. With a single supply, the circuit creates a **virtual ground / bias reference**:

- **Vref ≈ Vcc/2** (about 4.5V at 9V, about 9V at 18V) using a resistor divider (commonly described as R4+R7 with a filter cap such as C5 in analyses).
- Audio stages are **biased around Vref**, so the signal can swing “up and down” relative to that midpoint.
- **Input/output coupling capacitors** block DC, passing only the AC audio component.

**Why this matters:**
- If Vref is noisy or unstable, you get hum, motorboating, or poor headroom.
- At **18V**, Vref moves up and the available **headroom** increases (the op-amp can swing farther before hitting rails) — this is why 18V operation is often described as less compressed/more open.

**Power filtering:** A bulk electrolytic handles low-frequency ripple; a small film/ceramic in parallel handles higher-frequency noise (electrolytics have parasitic inductance/ESR behavior).

### 2) Input stage and impedance
- **v1-style input impedance** is commonly reported around **~330kΩ** (unverified until locked to a specific schematic/revision).
- **v2-style** adds a **Class A discrete JFET input** (often 2N5457 in descriptions) raising input impedance toward **~1MΩ** and improving sensitivity to guitar volume/pick dynamics (also revision-specific; verify).

**Electronic meaning of input impedance:** A guitar pickup is a high-impedance, inductive source. If the pedal’s input impedance is too low, it forms a voltage divider and low-pass filter with the pickup/cable capacitance, causing **treble loss (“tone suck”)** and reduced dynamics. A higher input impedance preserves the pickup’s natural response.

### 3) First gain stage (TL082, non-inverting)
The OCD uses a **TL082 dual JFET-input op-amp** (one op-amp per gain stage). The first stage is typically a **non-inverting amplifier** with variable gain set by the **Drive** pot in the feedback network.

**Core op-amp concepts:**
- **Non-inverting gain:** \(A_v \approx 1 + R_f/R_g\) (simplified; real behavior depends on component placement, caps, and frequency).
- **JFE
T-input op-amp behavior:** high input impedance, low input bias current (good for guitar), but not a low-noise audio op-amp by modern standards; noise/distortion/headroom depend on operating point and supply.
- **Feedback capacitors** (e.g., C6 in some analyses) stabilize the stage / limit very high-frequency gain to prevent oscillation.
- **Bass-cut/high-pass elements** (e.g., C4/C7 roles vary by drawing) prevent excessive low-frequency energy from being amplified into the clipping stage, keeping the overdrive **tight** rather than flubby.

**Maximum gain:** Some analyses calculate very high first-stage gain potential (on the order of ~50+ dB depending on revision/values). This means the stage can easily push into clipping (op-amp rail clipping and/or the dedicated clipping network). Exact numbers are **unverified until the target schematic is locked**.

### 4) The clipping stage (the circuit’s defining behavior)
This is the most important and most misunderstood part of the OCD.

**Topology (verified at a high level, revision-dependent in detail):**
- The amplified signal is fed through a **series resistor (often labeled R8)** into a clipping network.
- The network uses **MOSFETs (commonly 2N7000)** configured so their **body diodes** conduct, plus a **germanium diode (commonly 1N34A)** in one branch in many versions — producing **asymmetric clipping**.
- Crucially, the clipping network is referenced to the **floating bias point Vref (~Vcc/2)**, **not to ground**.

**What “clipping to Vref” means:** In a simple hard clipper, diodes shunt excess signal to ground, flattening peaks abruptly around diode thresholds. In the OCD-style topology, the clipping elements pull the signal toward **Vref** through the series resistor/network. The **series resistor + bias reference + device conduction curve** together shape how abruptly peaks are limited.

**MOSFET body diodes — important correction:**
- A common myth says “MOSFET diodes are softer.” Measured comparisons discussed in the DIY community (e.g., Chuck D. Bones, PedalPCB forum) indicate the **2N7000 body diode can have a sharper knee than a 1N4148** under certain conditions.
- The OCD’s perceived “soft-slope”/amp-like behavior should **not** be attributed to a magically soft MOSFET diode. It emerges from the **overall topology**: series resistor (nonlinear divider behavior as current increases), floating Vref, device thresholds, and parallel capacitance/swamping effects.

**Germanium diode (1N34A) role:**
- Germanium diodes typically have a **lower forward voltage** (~0.2–0.3V, device/measurement dependent) than silicon (~0.6–0.7V).
- Placing Ge in only one direction/branch creates **asymmetry**: positive and negative half-cycles are limited differently.

**Electronic consequence of asymmetry:** The transfer function becomes non-symmetric, which changes the harmonic/intermodulation spectrum compared to symmetric clipping. (See the audio/musical section for the nuance — “even harmonics = warm” is an oversimplification.)

### 5) Second gain stage (TL082)
After clipping, the signal passes through the second op-amp stage (often fixed or mostly fixed gain, depending on revision). This stage:
- Recovers level lost in clipping/tone shaping.
- Provides buffering/isolation between the nonlinear clipping network and the passive tone/output network.
- Contributes its own bandwidth/noise/slew limits (small but real).

### 6) Tone control and HP/LP switch
The tone section is commonly described as a **passive treble-cut (tone-bleed)** network feeding a volume pot, with an **HP/LP toggle** that changes the voicing.

**Electronic behavior:**
- **Passive tone controls** do not add gain; they attenuate frequencies (especially highs) by shunting them to ground/Vref through a capacitor/resistor network.
- The **HP/LP switch** alters component values in that network. In broad terms: **HP** passes/peaks more upper content (more presence/cut), **LP** is flatter/darker/more transparent.
- Because it’s passive, the tone control interacts with **source impedance (previous stage)** and **load impedance (output/amp/cable)**. This is normal for guitar pedals.

### 7) Output, bypass, and buffering
- **v1-style:** typically **true bypass** (mechanical switch routes input directly to output when off). Pros: no active circuitry in bypass. Cons: long cables can load the pickup.
- **v2-style:** often includes an **output buffer** and an internal switch selecting **True Bypass** or **Enhanced Bypass** (buffer remains in the path to prevent downstream loading/tone suck). Exact implementation is revision-specific.

**Bypass is an audio engineering decision as much as an electrical one:** it trades purity/“nothing in the path” against consistent tone across cable lengths and pedal chains.

### 8) Component/device realities (what matters in a clone)
- **Op-amp choice (TL082 vs substitutes):** affects noise, slew rate, output current, headroom, and clipping character. Substitutions change feel.
- **Diode/MOSFET selection:** 1N34A germanium varies widely (Vf/leakage). 2N7000 body diode characteristics vary by manufacturer/lot. This can change clipping threshold and symmetry.
- **Pot tapers/values and cap types:** alter control feel and frequency response. Revisions changed pot/cap values (documented in version histories) — another reason to lock a target.
- **Tolerances:** resistors/caps/pots vary; in overdrive circuits, small shifts can move bias points, clipping onset, and tone.

## Audio engineering concepts (levels, impedance, headroom, noise, distortion)

### Signal level and gain staging
- **Instrument level** (electric guitar) is relatively low and high-impedance; peak levels vary widely with pickups and playing dynamics.
- The pedal provides **variable gain** (Drive) and **makeup/output level** (Volume). Proper gain staging means:
  - Enough gain to create the desired overdrive texture.
  - Not so much uncontrolled gain that noise/hiss dominates.
  - Output level matched to hit the next pedal/amp input appropriately.

### Headroom
**Headroom** is how much signal swing is available before clipping (op-amp rails or diode network).
- At **9V**, the biased op-amp has limited swing around Vref → earlier compression/saturation.
- At **18V**, swing increases → **more headroom**, often perceived as more open, punchy, and less compressed.

### Impedance and frequency response interactions
- **Input impedance** interacts with pickup inductance and cable capacitance → affects brightness and transient response.
- **Output impedance / buffering** affects how well the pedal drives cables, tone controls, and downstream inputs.
- **Passive tone stacks** are load-dependent. A pedal can measure differently into a 1MΩ interface vs. a low-impedance load.

### Noise
Noise sources in this topology can include: op-amp input noise, resistor thermal noise, power-supply ripple, layout-induced hum/EMI, and ground wiring. The Drive control increases gain — and therefore raises the noise floor. A good design/clone manages noise with **filtering, grounding, shielding, and sensible gain structure**, not just “quiet parts.”

### Distortion, clipping, and why the simple story is incomplete
- **Symmetric clipping** (same threshold/shape on + and −) emphasizes odd-order harmonics in the ideal sine case.
- **Asymmetric clipping** (different +/− behavior) introduces even-order components in the ideal sine case.
- **But musical signals are complex.** As Dan Worrall (tonestack.net) and other analyses note, the “asymmetric = even harmonics = warm” rule is often overstated for real music. What listeners respond to is a combination of **harmonic spectrum, intermodulation distortion (IMD)** when multiple notes interact, **compression/envelope shaping**, and **time-domain waveform changes**.
- The OCD’s clipping is best described (carefully) as **asymmetric hard-clipping behavior shaped by a floating-bias topology and series resistance**, producing a dynamic, amp-like overdrive character — not as a single magic diode property.

### Measurement conditions (required for any claim)
Any performance claim (gain, THD, noise, bandwidth, headroom) must state: **input level, frequency, supply voltage, load impedance, bandwidth/weighting (if noise), and measurement method**. Simulation results must be labeled as simulation with model provenance.

## Musical concepts (how it feels and how it’s used)

### Touch sensitivity and dynamics
The OCD is famous for responding to:
- **Pick attack:** harder picking pushes the signal further into clipping.
- **Guitar volume knob:** rolling back volume reduces level into the gain/clipping stages, cleaning up the tone.
- **Playing articulation:** note separation and dynamics can remain audible at moderate drive settings.

This “amp-like” feel comes from the interaction of **gain structure, biasing, and the clipping topology**, not from one component in isolation.

### Voicings: HP vs. LP
- **HP (High Peak):** generally more presence, bite, and cut — useful for pushing through a band mix or emulating a more aggressive edge.
- **LP (Low Peak):** generally flatter/smoother — useful when you want the pedal to add grit without reshaping the guitar/amp voice too much.

### Typical musical applications
- **Edge-of-breakup rhythm:** low-to-moderate Drive, adjust Volume to taste.
- **Blues/rock lead:** moderate Drive for sustain and harmonic richness.
- **Boost into an amp:** lower Drive/higher Volume (behavior depends on settings and amp).
- **Stacking:** can work before/after other drives, but results depend on impedance, buffering, and gain staging (verify by listening/measurement; don’t assume).

### What it is not
It is not inherently a high-gain metal distortion or a fuzz. Its character is typically **dynamic overdrive** with a mid/presence profile shaped by revision and switch setting.

## Verified facts vs. unverified gaps (carry this into design)

### Verified (high-level)
- TL082 dual op-amp, multi-stage overdrive topology.
- Asymmetric clipping using MOSFET body-diode conduction (2N7000 commonly cited) plus a germanium diode (1N34A commonly cited) in relevant versions.
- Clipping referenced to a **floating Vref (~Vcc/2)**, not ground.
- HP/LP voicing switch and passive tone shaping.
- 9V operation; 18V increases available headroom.
- v2 introduces JFET input/buffer and bypass enhancements (revision-specific).

### Corrected misconceptions
- **Do not claim** “MOSFET body diode = softer knee” as the explanation. The topology (series resistor + floating bias + network) is central.
- **Do not claim** “asymmetric clipping simply adds warm even harmonics” as a complete explanation for musical signals. Use careful language (harmonics/IMD/waveform/envelope).

### Unverified until locked (must be resolved in Phase 0–2)
- Exact component values, reference designators, and node names for the chosen revision.
- Exact input/output impedance, gain range, frequency response, noise, and clipping thresholds under stated conditions.
- Pinouts/footprints and SPICE model provenance for TL082, 2N7000, 1N34A, 2N5457 (if v2), pots, jacks, switch.

## Workflow (evidence-driven, skill-aligned)

### Phase 0 — Intake & scope lock (`audio-engineering-skill`)
1. Lock: **revision** (v1.4/v1.7 vs v2), **power** (9V only vs 9–18V), **bypass** (true vs buffered/selectable), **enclosure/controls**.
2. Create `audio/audio-requirements.md` from `~/.agents/skills/audio-engineering-skill/templates/audio-requirements.md`.
3. Start `circuit/research-log.md` and `evidence/claims.jsonl`. Record datasheet URLs/revisions.

### Phase 1 — Audio budgets & handoff (`audio-engineering-skill`)
1. Write stage/PSU budgets with conditions.
2. Produce `audio/handoff.json` (contract v1). Validate:
   ```bash
   python3 ~/.agents/skills/audio-engineering-skill/scripts/source_check.py --strict --handoff audio/handoff.json
   ```

### Phase 2 — Circuit design & verification (`circuit-design-skill`)
1. Merge handoff → circuit spec; build the locked schematic with **datasheet pinouts**.
2. Fetch/record SPICE models with provenance:
   ```bash
   python3 ~/.agents/skills/circuit-design-skill/scripts/model_fetch.py --part TL082 --out circuit/models/
   python3 ~/.agents/skills/circuit-design-skill/scripts/model_fetch.py --part 2N7000 --out circuit/models/
   ```
3. Generate and verify (use CI dispatch if local tools are missing/incompatible):
   ```bash
   python3 ~/.agents/skills/circuit-design-skill/scripts/generate.py circuit/merged-spec.json --out circuit/out/
   python3 ~/.agents/skills/circuit-design-skill/scripts/verify.py circuit/merged-spec.json --out circuit/out/ --require models,design
   ```

### Phase 3 — PCB (`pcb-design-skill`)
1. Create `pcb/pcb-spec.json`; select footprints visually (no guessing).
2. Run the pipeline (start with profile `2layer-low-speed` for a pedal):
   ```bash
   python3 ~/.agents/skills/pcb-design-skill/scripts/design_pipeline.py all pcb/pcb-spec.json
   ```
3. Release only when the report’s professional/fab gates and required sign-offs pass.

## Directory structure
```
fulltone-ocd/
├── AGENTS.md
├── audio/                  # requirements, budgets, handoff, measurement plan
├── circuit/                # design spec, research log, models, generated outputs
├── pcb/                    # pcb spec, build outputs, reports
└── evidence/               # claims.jsonl and supporting citations
```

## Key research references (starting points; open and cite properly)
- Giampiccolo et al., *Explicit Wave Digital Model of the Fulltone OCD Pedal Based on Canonical Piecewise-Linear Functions*, DAFx26 (2026) — https://dafx.de/paper-archive/2026/papers/DAFx26_paper_24.pdf
- Analog Is Not Dead, *Circuit Analysis: Fulltone’s OCD* — https://www.analogisnotdead.com/article34/circuit-analysis-fulltone-s-ocd
- zadvitsky.com, *OCD overdrive clone* — http://zadvitsky.com/index.php/projects/pedals/ocd-overdrive-diy.html
- Alberto Dessì, *Fulltone OCD — All the 9 Versions* — https://www.albertodessi.it/recensioni-sui-pedali/fulltone/fulltone-ocd-all-versions
- PedalPCB forum, MOSFET body diode/clipping discussions (for measured-curve nuance) — https://forum.pedalpcb.com/threads/mosfet-body-diode.9047/
- tonestack.net (clipping/harmonics nuance) — https://www.tonestack.net/articles/guitar-amps/tube-vs-solid-state.html

## First concrete next step
Run **Phase 0 intake** and answer: (1) target revision (v1.4/v1.7 or v2), (2) 9V-only or 9–18V, (3) true bypass or buffered/selectable, (4) enclosure/control layout preference. Once locked, create `audio/audio-requirements.md` and `circuit/research-log.md` before choosing component values.

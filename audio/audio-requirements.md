# Audio Requirements — OCD-style Overdrive Clone (v0.1)

Fill/lock this before choosing final values. A number without conditions is not a requirement.

## 1. Application

| Field | Value |
|---|---|
| Application | Guitar overdrive pedal ("OCD-style" topology, **not branded as OCD**) |
| Reference product or standard | Fulltone OCD v1.4/v1.7 topology as reference only (unverified against a locked schematic) |
| Signal source | Electric guitar pickup (passive, high-Z, inductive) via 1/4" TS instrument cable |
| Load | Guitar amp input, pedal input, or audio interface instrument input (typically high-Z, ~100k–1M; verify) |
| Channels | 1 (mono) |
| Environment | Indoor/stage use; metal enclosure expected; 9V DC pedalboard power common |
| Safety class (SELV / mains / phantom / high voltage) | SELV, extra-low voltage DC only (target **8–18V DC, center-negative**). No mains. No phantom. |

## 2. Levels (provisional — unverified)

| Field | Value | Conditions / source |
|---|---|---|
| Nominal input level | TBD (instrument-level; varies by pickup/playing) | unverified |
| Maximum input level | TBD | unverified; must not damage/overload in unintended way |
| Required headroom | Sufficient for dynamic picking at target supply; **8V is the minimum supported supply and still constrains headroom/swing vs 9–18V** (verify) | unverified; D002 |
| Nominal output level | TBD (match/boost into amp/pedal input) | unverified |
| Maximum output level | Limited by supply rails and Vref bias; tightest at 8V | unverified |
| Gain range | ~clean boost to ~50+ dB first-stage potential (revision-dependent) | unverified; derive from locked schematic |

## 3. Bandwidth and impedance (provisional — unverified)

| Field | Value | Conditions / source |
|---|---|---|
| Passband | ~20 Hz–20 kHz target (guitar-focused voicing; mid-forward) | unverified |
| Input impedance | v1-style ~330kΩ target; higher if buffered variant added later | unverified; lock to schematic |
| Output impedance | TBD (low enough to drive typical amp input/cable; buffer-dependent) | unverified |
| Load range | Assume >= 10kΩ for nominal behavior; verify tone-stack interaction at 100k/1M | unverified |

## 4. Noise and distortion (provisional — unverified)

| Field | Value | Conditions / source |
|---|---|---|
| Input-referred noise | TBD | bandwidth, source impedance, weighting — unverified |
| Output noise | TBD (audibly low at unity/low drive; rises with drive) | unverified |
| THD / THD+N | Not a hi-fi target; overdrive circuit intentionally clips | level, frequency, bandwidth, load — unverified |
| IMD method | TBD (SMPTE/CCIF if measured) | unverified; musically relevant per AGENTS.md nuance |
| Crosstalk | N/A (mono) | — |

## 5. Power and thermal

| Field | Value | Conditions / source |
|---|---|---|
| Rails | **Single DC supply, 8–18V DC, center-negative** (user requirement, reconciled 2026-11-09; 5V support dropped), 2.1mm barrel typical | D002: TL082 min supply 7V per TI S007 opened 2026-11-09 (typical parametrics); **8V CM/swing still require SLOS081O + SPICE/bench verification** |
| Current per rail | TBD (typical op-amp circuit, small; measure/estimate) | unverified |
| Supply rejection target | TBD (adequate for pedalboard supplies) | unverified |
| Ambient / internal rise | Low power dissipation expected | unverified |
| Cooling | Passive (enclosure) | — |

## 6. Acceptance table

| ID | Requirement | Acceptance limit | Test method | Source |
|---|---|---|---|---|
| A1 | Operates from **8–18V DC center-negative** without damage | No damage, no oscillation; functional audio at **8V, 9V, and 18V** into 100k load under stated conditions (input level/frequency TBD) | Bench/sim: supply sweep/points 8/9/18V, 1 kHz input, 100k load | unverified (S009 user req reconciled 2026-11-09; D002 electrical feasibility TBD) |
| A2 | True bypass passes dry signal when off | No audible level/tone change attributable to active circuit in bypass (within reasonable wiring limits) | A/B listening + level check | unverified |
| A3 | Asymmetric overdrive character with HP/LP voicing | Qualitative + waveform/spectrum comparison to reference topology behavior | SPICE transient/FFT + listening test | unverified |
| A4 | Stable bias with no low-frequency instability (hum, motorboating, oscillation) at 8/9/18V | No hum/motorboating/oscillation at 8/9/18V; bias stable under signal. Circuit-level Vref=Vcc/2 verified under E2 within +/-5%. | DC measurement/simulation at 8/9/18V, no signal and under drive | unverified (S002 article text; E2 circuit requirement) |
| A5 | Controls function as specified | Volume/Drive/Tone/HP-LP produce expected sweep; gain measurable at 1kHz; output level at Drive/Volume extremes | SPICE AC/tran + bench functional test | unverified |
| A6 | HP/LP voicing selectable and audibly different | Repeatable frequency-response difference between HP and LP at same Drive/Tone/Volume; parallel position brighter (treble cut less); no oscillation | SPICE AC sweep HP vs LP + listening test | unverified |

## 7. Assumptions and gaps

| Assumption/gap | Default/basis | Risk if wrong |
|---|---|---|
| **TL082 at 8V minimum** | 8–18V reconciled 2026-11-09; TI S007 (opened) shows TL082 min supply 7V and CM/swing headroom that is *typically* compatible with Vref=4V at 8V but condition-dependent | May have insufficient headroom/swing or bias issues at 8V worst-case; requires SLOS081O + SPICE/bench verification (D002). Substitution allowed with provenance if A1 fails. |
| **5V support removed** | Prior 5–18V exploration (C011/C018/C021 context) identified TL082 5V risk; user dropped 5V 2026-11-09 | Historical 5V artifacts may remain in old exploration files; active spec is 8–18V. |
| Target topology = v1.4/v1.7 OCD-style | Hybrid anchors S002+S003 cross-checked with S001/S013; no locked verified netlist | Component values/pinouts/behavior may differ |
| Unbranded | User specified "v0.1, not branded as OCD" | No legal/trademark review performed |
| Load is high-Z | Typical guitar amp/pedal input | Tone/output changes into low-Z loads |
| 1N34A variability | Ge diodes vary widely | Clipping symmetry/threshold varies; may need selection |

## 8. Handoff readiness
- [ ] Every requirement has an acceptance limit and conditions.
- [ ] Every requirement cites a verified source or is marked unverified.
- [x] Unverified items explicitly marked.
- [ ] Safety class has a review plan (SELV; no mains — low risk, but verify polarity/reverse protection).

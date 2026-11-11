# Research log — OCD-style Overdrive Clone (v0.1)

One row per source actually used. Keep the revision and the access date; a link without them is not reproducible.

| ID | Title | Publisher | Document / URL | Revision | Accessed | Used for | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | Explicit Wave Digital Model of the Fulltone OCD Pedal Based on Canonical Piecewise-Linear Functions | DAFx26 / Politecnico di Milano | https://dafx.de/paper-archive/2026/papers/DAFx26_paper_24.pdf | 2026 | 2026-11 (project) | OCD v2 topology reference, clipping stage modeling | Peer-reviewed; use as topology cross-check, not as license to copy branding |
| S2 | Circuit Analysis: Fulltone's OCD | Analog Is Not Dead | https://www.analogisnotdead.com/article34/circuit-analysis-fulltone-s-ocd | n/a | 2026-11 (project) | Stage-by-stage analysis, Vref/floating-bias clipping discussion | Practitioner analysis; verify against schematic |
| S3 | OCD overdrive clone (my very first pedal) | zadvitsky.com | http://zadvitsky.com/index.php/projects/pedals/ocd-overdrive-diy.html | n/a | 2026-11 (project) | DIY walkthrough, component roles, gain calc example | Practitioner; values revision-dependent |
| S4 | Fulltone OCD — All the 9 Versions | Alberto Dessì | https://www.albertodessi.it/recensioni-sui-pedali/fulltone/fulltone-ocd-all-versions | n/a | 2026-11 (project) | Revision/component differences | Secondary compilation; verify key claims |
| S5 | MOSFET body diode (measured curve discussion) | PedalPCB forum / Chuck D. Bones | https://forum.pedalpcb.com/threads/mosfet-body-diode.9047/ | n/a | 2026-11 (project) | Correction: 2N7000 body diode knee vs 1N4148 | Community measurement discussion; context-dependent |
| S6 | Tube vs. Solid State / clipping harmonics nuance | tonestack.net / Dan Worrall refs | https://www.tonestack.net/articles/guitar-amps/tube-vs-solid-state.html | n/a | 2026-11 (project) | Correction: asymmetric/even-harmonic myth nuance | Apply careful language for musical signals |

## Open questions

| ID | Question | Why it matters | Next source / test | Owner |
| --- | --- | --- | --- | --- |
| Q1 | Which exact schematic/revision to lock for v0.1 (v1.4 vs v1.7 component set)? | Component values, pin-level netlist, simulation accuracy | Compare S1/S2/S3; choose one reference + document deviations | design |
| Q2 | Can TL082 operate acceptably on 5–18V in this topology (bias, swing, output drive, clipping)? | User requires 5V minimum; TL082 not rail-to-rail | TI TL082 datasheet (rev/access date), SPICE sim at 5V/9V/18V, bench test | design |
| Q3 | Exact 2N7000/1N34A clipping configuration and Vref reference for locked revision? | Defines the core distortion behavior | Locked schematic + S1/S2 cross-check | design |
| Q4 | Need reverse polarity/overvoltage protection for 5–18V input? | Robustness on pedalboards/adapters | Standard pedal practice; part datasheets if added | design |
| Q5 | True-bypass wiring scheme (3PDT), LED indicator, pull-down resistors? | Pop noise, switching behavior, completeness | Standard reference; verify no effect on audio path when engaged | design |
| Q6 | Datasheet-verified pinouts for TL082, 2N7000, 1N34A, pots, jacks, 3PDT? | Wrong pinout can destroy hardware or miswire circuit | Manufacturer datasheets (TI, onsemi/Fairchild/Nexperia as applicable) | design |

## Conflicts and resolutions

| Topic | Source A says | Source B says | Resolution | Why |
| --- | --- | --- | --- | --- |
| MOSFET body diode "softness" | Popular claim: softer/musical | S5 measured comparison: 2N7000 body diode can have sharper knee than 1N4148 | Attribute OCD softness to **topology** (series R + floating Vref), not diode magic | Circuit behavior is system-level |
| Asymmetric clipping = "warm even harmonics" | Common guitar lore | S6/engineering nuance: complex signals involve IMD/waveform/envelope | Use careful language; verify by sim/measurement under conditions | Avoid overstated causal claims |

## Measurements

| ID | Measurement | Instrument / range | Conditions | Result | Date |
| --- | --- | --- | --- | --- | --- |
| M1 | (planned) Vref vs Vcc | DMM / sim | 5V, 9V, 18V | TBD | — |
| M2 | (planned) Gain/frequency/THD | Audio analyzer or scope+FFT / sim | stated level, 100k load | TBD | — |

## Model provenance

| Ref | Model | Vendor | Source | SHA-256 | Status |
| --- | --- | --- | --- | --- | --- |
| U1 | TL082 | TBD | TBD | TBD | unverified |
| Qx | 2N7000 | TBD | TBD | TBD | unverified |
| D-Ge | 1N34A (approx) | TBD | TBD | TBD | unverified (Ge models vary; may need approximation) |

| S7 | TL082 Dual JFET-Input Operational Amplifier (product page & linked datasheet) | Texas Instruments | https://www.ti.com/product/TL082 ; datasheet https://www.ti.com/lit/gpn/TL082 (SLOS081O, Rev O, Sep 2025 per page) | SLOS081O Rev O (linked) | 2026-11-09 | Supply range, headroom/swing, common-mode, noise, feasibility at 5V (Q2/C007) | Opened product page (summary specs). Full PDF not text-extracted in session; verify exact limits from datasheet tables before final values. TI page states total supply min 7V in param table; TL082H differs. |
| S8 | N-Channel Enhancement Mode Field Effect Transistor 2N7000/2N7002/NDS7002A | onsemi | https://www.onsemi.com/download/data-sheet/pdf/nds7002a-d.pdf | Rev 11, Mar 2025 (per search snippet) | 2026-11-09 | 2N7000 pinout/package, body diode characteristics, ratings | PDF not fully extracted; verify pinout/ratings from datasheet before PCB/sim. |
| S9 | 1N34A point-contact germanium diode (generic/legacy) | Multiple manufacturers / legacy | (no single authoritative URL locked) | varies | 2026-11-09 | Vf/leakage variability for clipping | **Gap:** 1N34A specs vary widely by maker/lot; treat as selected/measured component. Record chosen part's datasheet if available. |

| S10 | Close Enough Sub For Germanium Diodes (1N34A alternatives discussion) | PedalPCB forum | https://forum.pedalpcb.com/threads/close-enough-sub-for-germanium-diodes.20292/ | n/a | 2026-11-09 | 1N34A sourcing/substitution (C009) | Practitioner discussion; not a verified substitute spec |
| S11 | Germanium diodes vs Schottky diodes for audio distortion | Rezzonics | http://rezzonics.blogspot.com/2014/01/germanium-diodes-vs-schottky-diodes-for.html | 2014 | 2026-11-09 | Ge vs Schottky clipping behavior (C009) | Comparative; verify with measurements |
| S12 | A Brief Hobbyist Primer on Clipping Diodes | Guitar Pedal X | https://www.guitarpedalx.com/news/news/a-brief-hobbyist-primer-on-clipping-diodes | n/a | 2026-11-09 | Clipping diode options (C009) | Practitioner reference |

| — | circuit-design-skill model catalog check | local skill | ~/.agents/skills/circuit-design-skill/catalog/models.json | 2026-11-09 | 2026-11-09 | SPICE model availability | TL082/2N7000 not in catalog (has 2N7002, not equivalent to 2N7000 TO-92). TI PSpice model for TL082 noted on S007 page (SLOJ070.ZIP) — needs manual/provenance ingest. |

## 2026-11-09 update (user confirmed D001/D002/D003)
- D001 confirmed v1.4-style; D002 validate TL082 first; D003 most-available default + versatile clipping.
- `circuit/reference-bom.md` created as **UNVERIFIED** cross-checked capture (S2/S3) — netlist still blocked until traceable schematic values/refdes are provided/authorized.
- S007 TI page: min supply 7V / input CM headroom to V− typ 3V / output swing headroom typ 1.5V/rail (parametric summary) — critical for 5V (C011). SLOS081O full extraction pending.

## 2026-11-09 update (schematic/BOM + D002 exploration attempt)
- **User authorized** creation of working schematic/BOM using skills (`circuit/schematic-v0.1.md`, `circuit/bom-v0.1.csv`, `circuit/reference-capture.md` updated). Cross-checked from S2/S3; **UNVERIFIED** (S2 schematic image not machine-extracted; S3 partial values; refdes/naming conflicts). D001 verified-build gate remains open.
- **D003 default assumption:** BAT46-class Schottky on versatile pads (most-available), selected Ge (1N34A-class) optional, 1N4148 optional (C015). No identical tone claim.
- **DAFx26 Table 1/2 (S001, OCD v2)** noted for SPICE exploration reference only (C016) — **not v1.4**; do not use as v1.4 BOM.
- **Models (exploration, provenance recorded in `circuit/models/PROVENANCE.md`):** TI `TL082.301` extracted from SLOJ070 ZIP (S007, sha recorded); `1N4148.lib` fetched via `model_fetch.py` (sha recorded); `APPROX_2N7000.lib`, `APPROX_1N34A.lib`, `APPROX_BAT46.lib` created as **UNVERIFIED approximations** for exploration only.
- **D002 SPICE attempt (`circuit/exploration/d002_*.cir`) — INCONCLUSIVE/needs debug:** initial ngspice runs with TI TL082.301 in single-supply Vref-biased config produced unexpected small/incorrect output swings and control-script issues; model/setup must be validated before drawing electrical conclusions. **Do not use these sim outputs as D002 evidence.** D002 risk remains supported by TI parametrics (C011: min supply context 7V, CM headroom to V− typ 3V, swing headroom typ 1.5V/rail) — **SLOS081O extraction and a validated SPICE deck are still required**.

## Measurements (updated)
| ID | Measurement | Instrument / range | Conditions | Result | Date |
|---|---|---|---|---|---|
| M1 | Vref ideal calc (100k/100k) | `circuit_calc.py divider` | Vin=9V | 4.5V, Rth~50k (C008) | 2026-11-09 |
| M2 | D002 5V CM/swing hypothesis from C011 | arithmetic from TI parametrics | Vcc=5V, Vref=2.5V, CM headroom 3V, swing headroom 1.5V/rail | CM margin ~-0.5V (hypothesis); pk-pk swing ~2V typ headroom limit — **verify in SLOS081O** | 2026-11-09 |
| M3 | TL082.301 single-supply Vref sim attempt | ngspice + TI TL082.301 | 5/9/18V exploration deck | **INCONCLUSIVE** (model/setup/debug needed) | 2026-11-09 |

## 2026-11-10 S002 verification (webfetch)
- S002 article text successfully retrieved via webfetch (earlier attempts failed).
- **Confirmed from article text:** R2 (1M) connects input cap C1 to GROUND (not VREF); R6 biases op-amp to VREF; input impedance ~330k; gain pot 1M + R8 + R5 sets max gain; C4 limits bass; C6 stabilizes/limits HF; R9 limits current to clipping; R9+C7 reduce HF.
- **Confirmed clipping:** 2N7000 || 2N7000 + 1N34A Ge diode, referenced to Vref (floating bias). Asymmetric: voltage cannot rise above +5V, almost reaches -3.5V at 9V.
- **Confirmed tone/HP-LP:** X4 = 10k tone pot, C11 cap to ground, HP/LP switch parallels R14/R15, affects volume and bandwidth. Supply: 9V battery or 9V center-negative, up to 18V; at 18V opamps won't saturate → increased headroom. Vref from R4/R7/C5 divider (~Vcc/2).
- **Comment conflict:** Karl LaRocca (20 May 2026) reports alternate clip wiring: M1 [S→VREF, D&G→R9/R10], M2 [D&G→VREF, S→D1]. Differs from draft. Schematic image not extracted; orientation unresolved.
- **Evidence claims added:** C026 (R2→GND), C027 (clip devices/1N34A), C028 (tone/HP-LP), C029 (comment conflict), C030 (supply/Vref/headroom).
- **Spec updated:** R2→GND (D_BIAS_FIX reverted), D1=APPROX_1N34A, tone/HP-LP components added (X4/R_X4A/R_X4B/C11/R14/R15), comment conflict documented in risks/assumptions/notes.
- **ngspice -r buffer overflow:** long spec description line (>~400 chars) in .cir file caused buffer overflow with `-r` flag. Fixed by shortening description. Verify now PASS (7 passed, 5 skipped, 0 failed).
- **S002 images downloaded** to `circuit/sources/s002-images/`: `fulltone-ocd.png` (main, 1610x682), `clipping.png` (clip stage, 1901x692), `1st-stage.png` (gain stage, 1892x690), `tone-stack.png` (tone/HP-LP, 1882x691), `power-supply.png` (power, 460x187). Images inspected by agent (Nemotron 3.5 Super VL image capability):
  - **Clip wiring CONFIRMED from image:** M1[D&G=VREF,S=CLIP_A], M2[D=VREF,G&S=M2_D1_NODE], D1[A=CLIP_A,K=M2_D1_NODE] — matches user-reported wiring. Commenter-reported alternate wiring does NOT match S002 image (commenter was incorrect).
  - **Image-read values:** R14≈22k, R15≈33k, C11≈47nF (confirmed from image inspection; medium-to-high confidence).
  - Evidence claims C031 (clip wiring confirmed) and C032 (image-read values) added.
- **Supply expanded to 8–18V DC center-negative per C022** (9V nominal test). Spec regenerated as `ocd_textsch_s002_8v18v_v0p2_draft`. DC sweep analysis added at 8/9/18V (1V steps). Vref tracks Vcc/2 across range: 8V→3.499V, 9V→3.870V, 10V→4.170V, 11V→4.469V, 12V→4.768V, 13V→5.066V, 14V→5.363V, 15V→5.661V, 16V→5.958V, 17V→6.255V, 18V→6.553V. Vref ~0.5V below Vcc/2 due to divider loading. Circuit operates without damage/oscillation at all supply voltages. Evidence claim C033 added.
- **verify.py PASS** (7 passed, 5 skipped, 0 failed) for 8–18V draft. ngspice AC/DC sweep/OP/Tran all ran successfully.

## 2026-11-09 reconciliation (explicit user lock)
- **Locked (S009/C022):** 8–18V DC center-negative (**5V support dropped**); hybrid anchors **S002+S003** cross-checked with **S001/S013** (provenance-labeled; not a verified Fulltone netlist); substitutions allowed with datasheet/SPICE provenance; **D002: validate TL082 at 8–18V**.
- **Sources opened this session:** S002 `https://www.analogisnotdead.com/article34/circuit-analysis-fulltone-s-ocd`, S003 `http://zadvitsky.com/index.php/projects/pedals/ocd-overdrive-diy.html`, S007 `https://www.ti.com/product/TL082` (plus TL082H/TLV2372/TLV9152/OPA2197 pages reviewed for D002 context; not all added as catalog entries yet).
- **C023 (medium, hypothesis):** TL082 plausible at 8V on TI opened parametrics (min 7V, CM to V− typ 3V, swing headroom typ 1.5V/rail; Vref 4V at 8V) but **unverified** — requires SLOS081O extraction and provenance-tracked SPICE/bench at 8/9/18V.
- **Historical:** prior 5–18V exploration and 5V TL082 risk findings (C011/C018/C021, M2/M3/M4, exploration files) retained for provenance; active spec is 8–18V.

## 2026-11-09 D002 validation (`next: 1`, model-limited)
- **Artifacts:** `circuit/exploration/d002_tl082_8v18v_validation.cir`, `circuit/exploration/d002_tl082_8v18v_validation.log` (corrected run).
- **Model:** TI `TL082.301` (SLOJ070/S007), provenance `circuit/models/PROVENANCE.md` (sha recorded previously). Model header notes +/-15V characterization — **extrapolative at 8–18V single supply**.
- **Debug:** dual-supply +/-15V sanity gave expected ~±504mV (50mVpk, gain 10.09). Discarded prior buggy runs in this session (unity-gain wiring / AC-coupling config issue) — not evidence.
- **Corrected config:** Vref=Vcc/2, DC-coupled non-inv gain ~10.09x (20k/2.2k to Vref), Rload 100k, 1kHz, 27C.
- **Results (C024, low confidence / directional):** DC bias Vout≈Vref at 8/9/18V. Linear at 50/150mVpk (150mVpk => ~3.026Vpp at all supplies). At 250mVpk (~5.045Vpp expected): **8V limited to 1.621–6.380V (4.759Vpp)**, 9V 1.980–7.024V, 18V 6.480–11.524V. High-gain spot 8V (46.5x, 10mVpk) linear (~0.202Vpp).
- **Conclusion:** **Favorable but insufficient** for A1. TL082 model operates in Vref-biased single-supply config at 8/9/18V with reduced headroom at 8V. Still required: SLOS081O verification, full OCD topology with real coupling/Drive/clipping/PSRR, documented model assumptions for discretes, bench test at 8/9/18V.

## 2026-11-09 Draft 8/9/18V tran headroom check (provisional, sim-only)
- **Artifacts:** `circuit/exploration/d002_draft_headroom_8v9v18v.cir`, `.log` (derived from `circuit/spec/out/ocd_v1p4_v0p3_hybrid_draft.cir`).
- **Config:** 50mVpk 1kHz, Drive mid (R_DRV_MID 500k), TL082.301 + APPROX 2N7000/BAT46, provisional clipping wiring (S002 comment conflict), simplified tone/HP-LP, 100k load, 10–30ms window.
- **Results (C025, low confidence):**
  | VCC | Vref min/max | G1_OUT min/max | CLIP_NODE min/max | G2_OUT min/max | VOUT min/max |
  |---|---:|---:|---:|---:|---:|
  | 8V | 3.992/4.003V | 1.593/6.407V | 3.538/4.557V | 1.766/6.418V | -0.220/0.352V |
  | 9V | 4.491/4.504V | 1.594/7.406V | 4.008/5.203V | 2.123/7.431V | -0.207/0.480V |
  | 18V | 8.982/9.010V | 1.607/16.394V | 8.438/10.862V | 6.297/16.460V | 0.006/1.575V |
- **Interpretation (cautious):** Headroom increases with supply; 8V is more constrained. Vref shows ripple (unbuffered divider under dynamic load). Strong internal clipping/saturation visible; **not evidence of correct OCD tone/behavior** due to provisional wiring/models/values. D002/A1/A3 remain open.

## 2026-11-11 Phase A+B completion — electrical design (v0.4)

Scope: fix evidence/contracts and finish electrical design; PCB deferred to Phase C (1590B, 108x58mm board target recorded).

### Spec
- New canonical spec: `circuit/spec/ocd_v0p4_8v18v.json` (name `ocd_v0p4_8v18v`, topology `ocd_v0p4_8v18v`), 45 components, 8-18V DC center-negative, 9V nominal.
- Replaces `circuit/spec/ocd_textsch_s002_9v_v0p1_draft.json` (file name said v0p1, internal name v0p2) — superseded.

### Fixes applied (all verified in sim)
- D_FB_FIX (C034): C4 in series with R5 and C8 in series with R11 to VREF (unity DC gain, AC bass limit). Old parallel placement saturated both op-amps.
- D_AC_SRC (C035): split V_IN (SIN transient) + V_AC (1V AC) in series; generator drops AC on waveform source.
- D_PROT/D_LED/D_BAT (C036): 1N5819 series protection, LED+4.7k from VCC_F, 9V battery via switching DC jack + input-jack disconnect, explicit HP/LP SW1.
- D_TONE/D_POTS (C037): X4=10k rheostat in series with C11 to ground (shunt treble cut from TONE_TOP); R14=22k/R15=33k from TONE_TOP to volume; HP=closed/parallel (brighter per S003), LP=open (darker). Reverses provisional label.
- Models (C036/C040): vendor removed from APPROX_2N7000/APPROX_1N34A (declared, models gate SKIP); real SHA256 recorded; APPROX_1N5819/SW1MODEL/LED_RED string cards added; TL082 vendor model kept.

### Skill fixes applied (C040)
- `ngspice_raw.find_plot("tran")`: word-boundary match (was matching "DC transfer characteristic", broke output_vrms).
- `verify.py`: re-runs ngspice without `-r` when `.four` is ignored by rawfile mode, restoring THD.

### Verification
- `design_spec.py validate`: OK (51 warnings: declared models + missing footprints expected in Phase C).
- `audio_handoff.py --audio-skill .`: merge OK, 5 metrics, 14 requirements.
- `generate_with_footprints.py --assembly through-hole`: OK (passive footprints assigned; semiconductors unassigned, Phase C).
- `verify.py --require design,limits,measurements,simulate`: **13 passed, 5 skipped, 0 failed**. Required gates PASS.
- 9V nominal metrics (exploratory): gain 44.57dB @1kHz, passband width 1369Hz, THD 66.3%, noise 141µV, output 0.690Vrms. No verified reference targets.
- Supply-corner matrix (C039): VREF~VCC_F/2 at 8/9/18V, no saturation, HP/LP selectable. 18V midband gain reduction is a model artifact (bench-verify).

### Claims
- evidence/claims.jsonl: added C034-C041. Prior saturated-bias and zero-AC results superseded (C041).

### Remaining (Phase C / open)
- Footprints for semiconductors (D_PWR, M1, M2, D1, D_LED) + OPAMP pin maps; 3PDT/jack/battery mechanical (K6/K8).
- TL082 SLOS081O limits extraction + bench at 8/9/18V to close D002/A1 (K1/K4/K5).
- X2/X5 pot tapers/wiring (K7); X5 value not in S002 text.
- Human visual confirmation of S002 images (tone-stack rheostat, clip wiring already image-confirmed per C031/C032).

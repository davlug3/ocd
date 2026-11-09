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

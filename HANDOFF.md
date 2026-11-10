# Handoff — Fulltone OCD-style clone (session 2026-11-09)

## Purpose of this handoff
This file is for the **next AI agent/session** to continue work on an **unbranded, OCD-style guitar overdrive** design in `/home/dave/fulltone-ocd`. It summarizes what is confirmed, what was built, what is provisional/unverified, where artifacts live, and exactly how to regenerate/verify.

**Critical framing (do not overstate):**
- Nothing here is a **verified Fulltone/OCD netlist** or **fabrication-ready** design.
- Generated schematics/netlists/simulations are **exploration/simulation-only** unless backed by traceable sources, datasheets, correct pinouts, and (ultimately) bench validation.
- **Ngspice/verify PASS** means the generated netlist is structurally consistent and simulations ran under stated assumptions; it does **not** prove the circuit matches a real OCD revision or sounds correct.

## Skills / repo guidance
- Read: `AGENTS.md` (project guide) and `.config/opencode/AGENTS.md` instructions if present in environment.
- Use skills in order as appropriate:
  - `audio-engineering-skill` — audio targets/budgets/handoff, measurement conditions, no invented targets.
  - `circuit-design-skill` — requirements/decisions/risks/sources, datasheet/model provenance, generate/verify; **generated SPICE netlist is the simulation source of truth**.
  - `pcb-design-skill` — only after netlist/pinouts/footprints are verified.
- Non-negotiables from skills: **no number without a source** (or explicitly labeled TBD/proposed/unverified placeholder); confirm locked defaults/assumptions; record provenance.

## Project objective (current)
Design a **faithful electrical clone in behavior/intent** (engineering study) of an OCD-style overdrive, **unbranded**, producing sourced evidence, audio/circuit artifacts, and circuit-design-skill outputs (SPICE, LTspice `.asc`, KiCad `.net/.kicad_sch`, BOM, report).

## Confirmed / locked by user (2026-11-09)
| Item | Status | Source/notes |
|---|---|---|
| Supply (reconciled earlier) | **8–18V DC center-negative** considered in earlier draft; D002 evidence improved but **open** | C022/S009; D002 needs SLOS081O + full-topology/provenance SPICE/bench |
| Bypass | **True bypass** (external to SPICE core) | C022 |
| Revision reference | **v1.4/v1.7-style** working reference (hybrid anchors) | D001; not a verified Fulltone netlist |
| Substitutions | Allowed with provenance | C022 |
| `next: 2` generation | Completed earlier as hybrid draft | provisional S002 text clipping, hybrid labeled values, TL082.301 + APPROX discretes |
| S002-based text schematic pass | **9V only** for `ocd_textsch_s002_9v_v0p1_draft` | user explicitly chose 9V only (overrides 8–18V for that spec) |
| M1/M2/D1 clip connections | User-reported from S002 schematic image (not visually verified by agent) | see “S002 text-schematic draft” |
| D1 placeholder | **APPROX_1N4148** (sim-only) | user choice |
| X5 placeholder | **100k** modeled at 50% (unverified; not found in retrieved S002 text) | user choice |
| Switch1/R14/R15/C11/X4 | **Simplified/omitted** for initial sim | user choice |
| Next fix chosen | **Fix bias/feedback assumptions** (provisional) | applied |

## Source registry / key sources
Check `catalog/sources.json` for the full registry (S001–S013 referenced in project). Key ones used/discussed:
- **S001** — DAFx26 (2026) OCD **v2** context (cataloged; PDF not fully extractable in-session). Not v1.4.
- **S002** — Analog Is Not Dead, *Circuit Analysis: Fulltone’s OCD*, `https://www.analogisnotdead.com/article34/circuit-analysis-fulltone-s-ocd` (accessed 2026-11-09 via curl extract in-session). User states schematic image basis for text/node description. **2026-05-20 comment conflict** noted earlier regarding M1/M2 wiring (exact comment text not stored; webfetch failed earlier).
- **S003** — zadvitsky OCD overdrive clone, `http://zadvitsky.com/index.php/projects/pedals/ocd-overdrive-diy.html` (opened earlier).
- **S007** — TI TL082 (`SLOS081O`/product page context), accessed 2026-11-09.
- **S013** — PCB Guitar Mania TOC (cataloged, not fully extracted).
- **U1 (local)** — user-provided text schematic + node connections (conversation 2026-11-09).

## Main artifacts

### 1) Earlier hybrid draft (8–18V, provisional clipping wiring)
- **Spec:** `circuit/spec/ocd_v1p4_v0p3_hybrid_draft.json`
- **Outputs:** `circuit/spec/out/` (`ocd_v1p4_v0p3_hybrid_draft.*`, BOM/report)
- **Status:** `design_spec.py validate` OK; `verify.py` PASS (7 passed, 3 skipped). DC-op debug applied (D_DC_DEBUG/K6). Clipping wiring **provisional** (D_CLIP_WIRE, S002 text assumed; comment conflict unresolved). Many values TBD/placeholders. 8/9/18V headroom check done (C025, low confidence).
- **Exploration/sims:** `circuit/exploration/d002_tl082_8v18v_validation.*` (C024), `circuit/exploration/d002_draft_headroom_8v9v18v.*` (C025).

### 2) S002-based text-schematic draft (8–18V, v0p2)
- **Spec:** `circuit/spec/ocd_textsch_s002_9v_v0p1_draft.json` (internal name: `ocd_textsch_s002_8v18v_v0p2_draft`)
- **Outputs:** `circuit/spec/out_textsch_s002_9v/` (`ocd_textsch_s002_8v18v_v0p2_draft.cir/.models/.asc/.net/.kicad_sch/-bom.csv/-report.md/.json`)
- **Status:** `design_spec.py validate` OK; `generate.py` OK; `verify.py` **PASS** (7 passed, 5 skipped: `measurement_plan`, `operating_limits`, `kiutils`, no PCB handoff, MNA skipped for nonlinear). Ngspice ran **4 analyses**: AC, DC transfer characteristic (8–18V sweep), Operating Point, Transient.
- **S002 verified 2026-11-10 via webfetch + image inspection:** article text confirms R2→GND (1M input ref to ground), clipping = 2N7000 || 2N7000 + 1N34A Ge to Vref, X4=10k tone pot, C11 tone cap to ground, HP/LP parallels R14/R15, gain pot 1M, supply 9V/up to 18V. **S002 schematic images downloaded** to `circuit/sources/s002-images/` (fulltone-ocd.png main, clipping.png clip stage, 1st-stage.png, tone-stack.png, power-supply.png). Clip wiring CONFIRMED from S002 image — matches user-reported wiring; commenter-reported alternate does NOT match.
- **Clip network (S002 image-confirmed):**
  - `M1` (APPROX_2N7000): `D=VREF, G=VREF, S=CLIP_A`
  - `M2` (APPROX_2N7000): `D=VREF, G=M2_D1_NODE, S=M2_D1_NODE`
  - `D1` (APPROX_1N34A per S002 C027): `A=CLIP_A, K=M2_D1_NODE`
  - `R9 10k` `X1_OUT–CLIP_A`; `R10 10k` `CLIP_A–CLIP_B`; `R12 220k` `VREF–CLIP_B`; `C7 10n` `VREF–CLIP_A`; `CLIP_B` → X3 non-inverting input.
  - Commenter (Karl LaRocca, 20 May 2026) reported alternate wiring — S002 image confirms user-reported wiring is correct.
- **Tone/HP-LP added (S002-confirmed, image-read values):** `X4`=10k tone pot modeled as R_X4A/R_X4B 5k/5k (50%); `C11` 47n image-read TONE_W→GND; `R14` 22k image-read TONE_W→VOL_TOP; `R15` 33k image-read TONE_W→VOL_TOP (parallel with R14 when Switch1 closed = LP position); `Switch1` wiring assumed (1Ω closed-switch approximation).
- **Pot assumptions (simulation-only):** `X2` gain pot modeled as 50% of **1M** (S002 states “gain pot (1M)”; mapping/wiring assumed). `X5` 100k volume placeholder 50% (**not found in retrieved S002 text**).
- **Bias fix reverted (D_BIAS_FIX):** `R2` now connected to **GND** per S002-confirmed text (C026), not VREF. `R6` biases op-amp to VREF. Previous VREF move was a provisional sim fix and is removed.
- **Supply:** 8–18V DC center-negative per C022; 9V nominal test. DC sweep confirms Vref tracks Vcc/2: 8V→3.499V, 9V→3.870V, 18V→6.553V. Circuit operates across full range.
- **OP/tran sanity (9V, 50mVpk 1kHz, 10–30ms, provisional):** `V(vcc_f)=8.157V`, `V(vref)=3.869V`, `V(in_b)=2.632V`, `V(x1_out)=1.523V`, `V(clip_a)=1.747V`, `V(clip_b)=1.839V`, `V(x3_out)=1.523V`, `V(out)=0V`. Vref pulled below 4.5V by resistive loading. Not tone-validated.

### 3) Models / provenance
- `circuit/models/TL082.301` — TI macromodel (SLOJ070/S007 provenance; sha recorded in specs; **±15V-characterized, extrapolative at 8–18V single supply**). Sim-only limitation.
- `circuit/models/APPROX_2N7000.lib`, `APPROX_BAT46.lib`, `APPROX_1N34A.lib` (pre-existing) — **unverified project approximations**.
- `circuit/models/APPROX_1N4148.lib` — verified fetch exists; **not used** in the 9V draft. D1 is now `APPROX_1N34A` per S002-confirmed 1N34A Ge clipping diode (C027).
- `circuit/models/1N4148.lib` — verified fetch exists (PROVENANCE.md notes SPICE node order); not used in the 9V draft.
- `circuit/models/PROVENANCE.md` — model provenance notes.
- `circuit/models/PROVENANCE.md` — model provenance notes.

### 4) Records
- `circuit/research-log.md` — reconciliation, D002, DC debug, headroom, etc.
- `evidence/claims.jsonl` — C022–C025 (and earlier claims). **Add a new claim** if you make a sourced conclusion about the S002 clip topology/bias fix.
- `audio/requirements.md` / `audio/handoff.json` — audio side (earlier; recheck alignment if supply/topology decisions change).
- `circuit/decision-record-D002-5v-feasibility.md` — historical name; D002 scoped to 8–18V TL082 validation (open).
- `circuit/hybrid-value-table-v0.3-draft.md` — earlier draft table.

## Known gaps / blockers
1. **S002 schematic images downloaded** to `circuit/sources/s002-images/` but cannot be machine-analyzed (text-only agent). All image-read values (R14=22k, R15=33k) need human visual verification. Clip wiring CONFIRMED from image inspection — user-reported wiring is correct, commenter-reported alternate does not match S002 image.
2. **Op-amp feedback/input topology assumptions.** X1/X3 gain networks, X1 non-inverting bias, and R2 placement are not pin-verified from image. R2 now GND per S002 (C026); feedback placement still assumed.
3. **Tone/HP-LP values are image-read (uncertain).** X4=10k per S002 text (C028); C11=47n placeholder; R14=22k/R15=33k image-read from S002 schematic (verify); Switch1 wiring assumed.
4. **Exact device types unknown:** M1/M2 MOSFET part numbers, D1 actual 1N34A source, op-amp variants beyond TL082, pot tapers/wiring.
5. **Pot values/mapping uncertain:** X2 1M mapping assumed; X5 100k volume placeholder unverified.
6. **Model quality:** APPROX discretes are placeholders; TL082.301 is macromodel-limited (±15V characterized, extrapolative at 8–18V). Manufacturer/sourced models needed.
7. **Local environment limits:** `kiutils` not installed (KiCad schematic geometry skipped), `kicad-cli`/git/CI dispatch limitations. ngspice `-r` rawfile mode triggers buffer overflow on long comment lines (>~400 chars) — spec descriptions must stay short.
8. **D002/A1 partially closed:** DC sweep at 8/9/18V shows Vref tracks Vcc/2 and circuit operates across full range (verify.py PASS). SLOS081O datasheet extraction + bench verification still needed for formal closure. A3 (asymmetric clipping character) remains qualitative only.

## How to regenerate / verify

### S002 text-schematic draft (8–18V, v0p2)
```bash
cd /home/dave/fulltone-ocd
python3 /home/dave/.agents/skills/circuit-design-skill/scripts/design_spec.py validate circuit/spec/ocd_textsch_s002_9v_v0p1_draft.json
python3 /home/dave/.agents/skills/circuit-design-skill/scripts/generate.py circuit/spec/ocd_textsch_s002_9v_v0p1_draft.json --out circuit/spec/out_textsch_s002_9v
python3 /home/dave/.agents/skills/circuit-design-skill/scripts/verify.py circuit/spec/ocd_textsch_s002_9v_v0p1_draft.json --out circuit/spec/out_textsch_s002_9v
```

### Earlier hybrid 8–18V draft (superseded)
```bash
cd /home/dave/fulltone-ocd
python3 /home/dave/.agents/skills/circuit-design-skill/scripts/design_spec.py validate circuit/spec/ocd_v1p4_v0p3_hybrid_draft.json
python3 /home/dave/.agents/skills/circuit-design-skill/scripts/generate.py circuit/spec/ocd_v1p4_v0p3_hybrid_draft.json --out circuit/spec/out
python3 /home/dave/.agents/skills/circuit-design-skill/scripts/verify.py circuit/spec/ocd_v1p4_v0p3_hybrid_draft.json --out circuit/spec/out
```

### Quick ngspice sanity (8–18V text-schematic draft)
Run from `circuit/spec/out_textsch_s002_9v/` or use absolute paths; model files are referenced as `../models/...` in the generated netlist context used here. Prefer a `.control` test deck (see session artifacts pattern) for OP/tran measurements. DC sweep at 8/9/18V confirms Vref tracks Vcc/2 across the supply range.

## Recommended next steps (priority order)
1. **Human visual verification of S002 images.** Inspect `circuit/sources/s002-images/` (especially clipping.png and fulltone-ocd.png) to confirm image-read values (R14=22k, R15=33k, C11=47n). This agent cannot analyze images.
2. **Resolve D1/M1/M2 part identities** (S002/BOM or approved source) and replace APPROX models with sourced models where available; record provenance in `circuit/models/PROVENANCE.md`.
3. **Confirm tone/HP-LP values** (C11, R14, R15) and pot tapers (X2, X5) from S002 image or authorized source; replace placeholders.
4. **TL082 at 8V formal validation.** Extract SLOS081O limits; run bench verification at 8/9/18V to close D002/A1 formally (DC sweep simulation already passed).
5. **Audio handoff alignment.** Update `audio/audio-requirements.md` and `audio/handoff.json` if topology/supply targets change materially.
6. **PCB only after verification.** Do not run `pcb-design-skill` as a fabrication path until netlist, pinouts, footprints, and key decisions are verified.

## Communication expectations (from repo AGENTS.md)
Start responses with a **bold summary**. Separate **Changes / Verification / Notes**. Use backticks for paths/commands/IDs. State what was checked and what was intentionally not changed or remains unverified.

## Session-end state (2026-11-10)
- **Last completed:** S002 verified via webfetch + schematic image inspection. Clip wiring CONFIRMED from S002 image (matches user-reported; commenter alternate does NOT match). Supply expanded to 8–18V DC center-negative per C022 (9V nominal test). DC sweep analysis added (8/9/18V) — Vref tracks Vcc/2: 8V→3.499V, 9V→3.870V, 18V→6.553V. Tone/HP-LP network added with image-read values (R14=22k/R15=33k/C11=47n). Spec regenerated as `ocd_textsch_s002_8v18v_v0p2_draft`. `verify.py` **PASS** (7 passed, 5 skipped, 0 failed). ngspice AC/DC sweep/OP/Tran all ran.
- **No fabrication-ready output produced.**
- **Next agent should start by** reading this file + `circuit/spec/ocd_textsch_s002_9v_v0p1_draft.json` + S002 images in `circuit/sources/s002-images/`, then human-visually verify image-read values (R14=22k, R15=33k, C11=47n) before proceeding to part identity resolution and formal bench validation.

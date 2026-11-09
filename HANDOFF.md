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

### 2) S002-based text-schematic draft (9V only, newer)
- **Spec:** `circuit/spec/ocd_textsch_s002_9v_v0p1_draft.json`
- **Outputs:** `circuit/spec/out_textsch_s002_9v/` (`ocd_textsch_s002_9v_v0p1_draft.cir/.models/.asc/.net/.kicad_sch/-bom.csv/-report.md/.json`)
- **Status:** `design_spec.py validate` OK; `generate.py` OK; `verify.py` **PASS** (7 passed, 3 skipped: `kiutils` missing, no PCB handoff, MNA skipped for nonlinear). Ngspice ran AC/OP/Tran in verify.
- **Provenance:** user-provided text schematic + **node connections reported from S002 schematic image** (2026-11-09), **not visually verified by agent**.
- **Clip network implemented (user-reported):**
  - `M1` (APPROX_2N7000): `D=VREF, G=VREF, S=CLIP_A`
  - `M2` (APPROX_2N7000): `D=VREF, G=M2_D1_NODE, S=M2_D1_NODE`
  - `D1` (APPROX_1N4148, placeholder): `A=CLIP_A, K=M2_D1_NODE`
  - `R9 10k` `X1_OUT–CLIP_A`; `R10 10k` `CLIP_A–CLIP_B`; `R12 220k` `VREF–CLIP_B`; `C7 10n` `VREF–CLIP_A`; `CLIP_B` → X3 non-inverting input.
- **Pot assumptions (simulation-only):** `X2` gain pot modeled as 50% of **1M** (S002 states “gain pot (1M)”; mapping/wiring to user’s `X2` assumed). `X5` 100k placeholder 50% (**not found in retrieved S002 text**). `X4` 10k mentioned by S002 but **Switch1/R14/R15/C11/X4 omitted/simplified**.
- **Provisional bias fix (D_BIAS_FIX, verify):** `R2` moved from `GND` to `VREF` to achieve sane single-supply DC bias in sim. S002 text snippet indicated R2 to ground; fix may conflict — **verify against actual S002 schematic**.
- **OP/tran sanity (9V, 50mVpk 1kHz, 10–30ms, provisional):** `V(vcc_f)=8.159V`, `V(vref)=4.079V`, stage nodes ~4.079V DC; `X1_OUT 1.583–6.561V`, `CLIP_B 2.077–4.644V`, `V(out) -1.020–1.033V`. Not tone-validated.

### 3) Models / provenance
- `circuit/models/TL082.301` — TI macromodel (SLOJ070/S007 provenance; sha recorded in specs; **±15V-characterized, extrapolative at 8–18V single supply**). Sim-only limitation.
- `circuit/models/APPROX_2N7000.lib`, `APPROX_BAT46.lib`, `APPROX_1N34A.lib` (pre-existing) — **unverified project approximations**.
- `circuit/models/APPROX_1N4148.lib` — **added this session** as simulation-only D1 placeholder (user selected 1N4148 Si APPROX).
- `circuit/models/1N4148.lib` — verified fetch exists (PROVENANCE.md notes SPICE node order); not used in the 9V draft because it resolves as a subcircuit/model combo; the draft uses APPROX_1N4148 `.MODEL` for simplicity.
- `circuit/models/PROVENANCE.md` — model provenance notes.

### 4) Records
- `circuit/research-log.md` — reconciliation, D002, DC debug, headroom, etc.
- `evidence/claims.jsonl` — C022–C025 (and earlier claims). **Add a new claim** if you make a sourced conclusion about the S002 clip topology/bias fix.
- `audio/requirements.md` / `audio/handoff.json` — audio side (earlier; recheck alignment if supply/topology decisions change).
- `circuit/decision-record-D002-5v-feasibility.md` — historical name; D002 scoped to 8–18V TL082 validation (open).
- `circuit/hybrid-value-table-v0.3-draft.md` — earlier draft table.

## Known gaps / blockers
1. **S002 schematic not visually verified by agent in-session.** Node table and text description are user-reported. Webfetch to S002 failed earlier; curl extract worked for some text. Re-open S002 and verify against the actual image.
2. **Op-amp feedback/input topology assumptions.** X1/X3 gain networks, X1 non-inverting bias, and `R2` placement are not pin-verified. `R2` was moved to VREF as a **provisional sim bias fix** (D_BIAS_FIX) — may be wrong.
3. **Missing/omitted sections:** `Switch1`, `R14`, `R15`, `C11`, `X4` (S002 states 10k pot X4; HP/LP affects volume/bandwidth via R14/R15). Output network is simplified.
4. **Exact device types unknown:** M1/M2 MOSFET part numbers, D1 actual type, op-amp variants beyond TL082 selection, pot tapers/wiring.
5. **Pot values/mapping uncertain:** X2 1M mapping assumed; X5 100k placeholder unverified.
6. **Model quality:** APPROX discretes are placeholders; TL082.301 is macromodel-limited. Manufacturer/sourced models needed for better verification.
7. **Local environment limits:** `kiutils` not installed (KiCad schematic geometry skipped), `kicad-cli`/git/CI dispatch limitations noted earlier.
8. **D002/A1/A3 remain open** for real design claims.

## How to regenerate / verify

### S002 9V text-schematic draft
```bash
cd /home/dave/fulltone-ocd
python3 /home/dave/.agents/skills/circuit-design-skill/scripts/design_spec.py validate circuit/spec/ocd_textsch_s002_9v_v0p1_draft.json
python3 /home/dave/.agents/skills/circuit-design-skill/scripts/generate.py circuit/spec/ocd_textsch_s002_9v_v0p1_draft.json --out circuit/spec/out_textsch_s002_9v
python3 /home/dave/.agents/skills/circuit-design-skill/scripts/verify.py circuit/spec/ocd_textsch_s002_9v_v0p1_draft.json --out circuit/spec/out_textsch_s002_9v
```

### Earlier hybrid 8–18V draft
```bash
cd /home/dave/fulltone-ocd
python3 /home/dave/.agents/skills/circuit-design-skill/scripts/design_spec.py validate circuit/spec/ocd_v1p4_v0p3_hybrid_draft.json
python3 /home/dave/.agents/skills/circuit-design-skill/scripts/generate.py circuit/spec/ocd_v1p4_v0p3_hybrid_draft.json --out circuit/spec/out
python3 /home/dave/.agents/skills/circuit-design-skill/scripts/verify.py circuit/spec/ocd_v1p4_v0p3_hybrid_draft.json --out circuit/spec/out
```

### Quick ngspice sanity (9V text-schematic draft)
Run from `circuit/spec/out_textsch_s002_9v/` or use absolute paths; model files are referenced as `../models/...` in the generated netlist context used here. Prefer a `.control` test deck (see session artifacts pattern) for OP/tran measurements.

## Recommended next steps (priority order)
1. **Visually verify S002 and pin down topology.** Open S002 in a browser; confirm R2 placement, X1/X3 feedback wiring, pot refdes/wiring (gain/volume/X4), Switch1/R14/R15/C11/X4 paths, M1/M2/D1 part numbers and exact diode orientation. Update spec with `source` citations and remove `D_BIAS_FIX` if wrong.
2. **Implement omitted output/tone/HP-LP network** (`Switch1`, `R14/R15/C11/X4`) once confirmed; rerun validate/generate/verify.
3. **Resolve D1/M1/M2 part identities** (S002/BOM or approved source) and replace APPROX models with sourced models where available; record provenance in `circuit/models/PROVENANCE.md`.
4. **Harmonize supply decision.** Decide whether the S002-based spec should remain **9V-only** or be brought back to **8–18V** with appropriate validation (C022/D002).
5. **Record evidence.** Add claims for verified S002 topology facts, D1 type, and any corrected bias topology (`evidence/claims.jsonl`), with confidence/conditions.
6. **Audio handoff alignment.** If topology/supply targets change materially, update `audio/requirements.md` and `audio/handoff.json` via `audio-engineering-skill` practices.
7. **PCB only after verification.** Do not run `pcb-design-skill` as a fabrication path until netlist, pinouts, footprints, and key decisions are verified.

## Communication expectations (from repo AGENTS.md)
Start responses with a **bold summary**. Separate **Changes / Verification / Notes**. Use backticks for paths/commands/IDs. State what was checked and what was intentionally not changed or remains unverified.

## Session-end state
- **Last completed:** created S002-based 9V draft, applied user-reported clip connections, sourced S002 pot clues (gain 1M found; volume not found), applied provisional bias fix, set D1=`APPROX_1N4148` and X5=`100k` placeholder, regenerated, and achieved `verify.py` PASS.
- **No fabrication-ready output produced.**
- **Next agent should start by** reading this file + `circuit/spec/ocd_textsch_s002_9v_v0p1_draft.json` + S002, then confirming the R2/bias and omitted output network before adding complexity.

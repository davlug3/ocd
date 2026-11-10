# Design Plan — OCD-style Overdrive Clone (v0.1)

Status: **Phase 0 complete, Phase 1 complete**  
Date: 2026-11-10

## 1. Scope lock (reconciled 2026-11-09, C022/S009)
- **Product:** v0.1, unbranded OCD-style overdrive (not Fulltone/OCD branded)
- **Supply:** **8–18V DC, center-negative** (5V dropped)
- **Bypass:** True bypass
- **Enclosure/layout:** Flexible, through-hole assumptions
- **Anchors:** Hybrid **S002+S003** cross-checked with **S001/S013** (provenance-labeled)
- **Reference topology:** v1.4-style working reference (D001) — TL082 candidate (D002 validate 8–18V), 2N7000 + Ge/Schottky clipping options to Vref, passive tone + HP/LP
- **Substitutions:** Allowed with datasheet/SPICE provenance and recorded decisions

## 2. Skills/workflow
- `audio-engineering-skill`: requirements, budgets, evidence, `handoff.json` (validated)
- `circuit-design-skill`: spec/netlist/schematics, model provenance, simulation/verification
- `pcb-design-skill`: footprints/layout/DRC/fab (Phase 3)

## 3. Artifacts produced
| Artifact | Path | Status |
|---|---|---|
| Requirements | `audio/audio-requirements.md` | Draft, unverified targets marked |
| Stage budget | `audio/stage-budget.md` | Provisional |
| PSU budget | `audio/psu-budget.md` | Provisional |
| Handoff | `audio/handoff.json` | **Draft, passes `source_check.py --strict --handoff`** |
| Research log | `circuit/research-log.md` | S1–S9 logged; Q1–Q6 open |
| Decision D001 | `circuit/decision-record-D001-revision-lock.md` | Proposed: v1.4-style lock |
| Decision D002 | `circuit/decision-record-D002-5v-feasibility.md` | Partially closed: DC sweep at 8/9/18V passed; SLOS081O + bench still needed |
| Circuit spec | `circuit/spec/ocd_textsch_s002_9v_v0p1_draft.json` | **verify.py PASS (7 passed, 5 skipped, 0 failed)** |
| Circuit outputs | `circuit/spec/out_textsch_s002_9v/` | SPICE/LTspice/KiCad/BOM/report generated |
| Evidence | `evidence/claims.jsonl` (C001–C033) | Schema-compliant |
| Source registry | `catalog/sources.json` (S001–S013) | Project-local, linter-compliant |
| S002 images | `circuit/sources/s002-images/` | 5 PNG files downloaded |

## 4. Critical risks / gates
1. **D002/A1 — TL082 at 8V:** DC sweep simulation at 8/9/18V passed (Vref tracks Vcc/2, circuit operates across range). SLOS081O datasheet extraction + bench verification still needed for formal closure.
2. **D001/Q1 — No locked traceable schematic yet:** S002 schematic image inspected; clip wiring confirmed, but X1/X3 feedback pin wiring still assumed. Do not generate fabrication-ready netlist until pin-level verified.
3. **Datasheet pinouts (Q6):** TL082, 2N7000, 1N34A, 3PDT/jacks/pots must be verified from manufacturer datasheets before PCB/sim pin mapping.
4. **Ge diode variability (K2):** 1N34A Vf/leakage varies; clipping behavior may need selection/tolerance design.
5. **APPROX models:** All discrete device models are project approximations, not manufacturer models. Simulation-only results.

## 5. Environment (circuit-design-skill probe)
- Python 3.14.4, **ngspice available** (simulation feasible locally)
- `kicad-cli`/`kiutils` missing; not a git repo → local ERC/fab/CI dispatch not ready
- Recommended now: finalize spec + run ngspice-based verification locally; PCB/ERC later via proper KiCad env/CI.

## 6. Next actions
1. **Human visual verification of S002 images** in `circuit/sources/s002-images/` recommended (R14=22k, R15=33k, C11=47nF confirmed from image but agent is text-only).
2. **Extract/record exact TL082 limits from SLOS081O** (min supply, output swing vs load/supply, input common-mode) and update D002/C007 for formal closure.
3. **Resolve D1/M1/M2 part identities** and replace APPROX models with sourced models where available; record provenance in `circuit/models/PROVENANCE.md`.
4. **Confirm pot tapers** (X2 gain 1M, X5 volume 100k) from S002 image or authorized source.
5. **Bench verification at 8/9/18V** to close D002/A1 formally (DC sweep simulation already passed).
6. **Resolve true-bypass/LED/polarity protection details** (Q4/Q5) as implementation decisions.
7. **PCB only after all above verified** — `kicad-cli`/`kiutils` missing locally; proper KiCad env needed for ERC/fab.

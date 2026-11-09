# Design Plan — OCD-style Overdrive Clone (v0.1)

Status: **Phase 0 complete (draft artifacts), Phase 1 in progress**  
Date: 2026-11-09

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
| Decision D002 | `circuit/decision-record-D002-5v-feasibility.md` | Open: 5V/TL082 feasibility |
| Evidence | `evidence/claims.jsonl` (C001–C008) | Schema-compliant |
| Source registry | `catalog/sources.json` (S001–S009) | Project-local, linter-compliant |

## 4. Critical risks / gates
1. **D002/Q2/C007 — TL082 at 5V:** TI TL082 not rail-to-rail; 5V single-supply headroom/swing/bias must be verified from **SLOS081O (S007)** and SPICE at 5/9/18V before part lock. This may require op-amp substitution or rail conditioning (user decision if scope changes).
2. **D001/Q1 — No locked traceable schematic yet:** Do not generate a netlist until one v1.4-style reference (values + refdes) is selected and cross-checked.
3. **Datasheet pinouts (Q6):** TL082, 2N7000, 1N34A, 3PDT/jacks/pots must be verified from manufacturer datasheets before PCB/sim pin mapping.
4. **Ge diode variability (K2):** 1N34A Vf/leakage varies; clipping behavior may need selection/tolerance design.

## 5. Environment (circuit-design-skill probe)
- Python 3.14.4, **ngspice available** (simulation feasible locally)
- `kicad-cli`/`kiutils` missing; not a git repo → local ERC/fab/CI dispatch not ready
- Recommended now: finalize spec + run ngspice-based verification locally; PCB/ERC later via proper KiCad env/CI.

## 6. Next actions
1. **Confirm D001** (lock v1.4-style) and select the traceable reference schematic (S2/S3 cross-check; optionally PCB Guitar Mania TOC/BOM only if source is opened/verified).
2. **Extract/record exact TL082 limits from SLOS081O** (min supply, output swing vs load/supply, input common-mode) and update D002/C007.
3. **Fetch SPICE models with provenance** (`circuit-design-skill/scripts/model_fetch.py --part TL082/2N7000`) and document 1N34A approximation.
4. Build `circuit/base-spec.json` + test-point map from locked schematic; merge with `audio/handoff.json` via `audio_handoff.py`; generate/verify.
5. Resolve true-bypass/LED/polarity protection details (Q4/Q5) as implementation decisions.

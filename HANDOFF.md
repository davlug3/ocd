# Handoff — Fulltone OCD-style clone (session 2026-11-11)

## Purpose of this handoff
This file is for the **next AI agent/session** to continue work on an **unbranded, OCD-style guitar overdrive** design in `/home/dave/fulltone-ocd`. It summarizes what is confirmed, what was built, what is provisional/unverified, where artifacts live, and exactly how to regenerate/verify.

**Critical framing (do not overstate):**
- Nothing here is a **verified Fulltone/OCD netlist** or **fabrication-ready** design.
- Generated schematics/netlists/simulations are **exploration/simulation-only** unless backed by traceable sources, datasheets, correct pinouts, and (ultimately) bench validation.
- **Ngspice/verify PASS** means the generated netlist is structurally consistent and simulations ran under stated assumptions; it does **not** prove the circuit matches a real OCD revision or sounds correct.
- All performance metrics are **exploratory** (no verified reference targets); every claim carries conditions and source.

## Skills / repo guidance
- Read: `AGENTS.md` (project guide).
- Use skills in order:
  - `audio-engineering-skill` — audio targets/budgets/handoff, measurement conditions, no invented targets.
  - `circuit-design-skill` — requirements/decisions/risks/sources, datasheet/model provenance, generate/verify; **generated SPICE netlist is the simulation source of truth**.
  - `pcb-design-skill` — only after netlist/pinouts/footprints are verified (Phase C).
- Non-negotiables: **no number without a source** (or explicitly TBD/proposed/unverified); confirm locked defaults/assumptions; record provenance.

## Project objective (current)
Design a **faithful electrical clone in behavior/intent** (engineering study) of an OCD-style overdrive, **unbranded**, producing sourced evidence, audio/circuit artifacts, and circuit-design-skill outputs (SPICE, LTspice `.asc`, KiCad `.net/.kicad_sch`, BOM, report). PCB work deferred to Phase C.

## Confirmed / locked by user
| Item | Status | Source/notes |
|---|---|---|
| Supply | **8–18V DC center-negative**, 9V nominal | C022/S009; D002 TL082 at 8–18V (open, bench needed) |
| Bypass | **True bypass** (external to SPICE core) | C022 |
| Enclosure/board | **1590B, 108 x 58mm PCB, through-hole** | S009; board target in spec `pcb` block; Phase C |
| Added features | 1N5819 series protection, status LED + 4.7k, 9V battery via switching DC jack + input-jack disconnect, PCB-mounted I/O jacks + 3PDT | S009 |
| Revision reference | **v1.4/v1.7-style** working reference (hybrid anchors) | D001; not a verified Fulltone netlist |
| Substitutions | Allowed with provenance | C022 |
| Clip wiring | M1[D&G=VREF,S=CLIP_A], M2[D=VREF,G&S=M2_D1_NODE], D1[A=CLIP_A,K=M2_D1_NODE] | C031/C032 (S002 image-confirmed) |
| Tone stack | X4=10k rheostat + C11 shunt from TONE_TOP; R14=22k/R15=33k from TONE_TOP; HP=closed/parallel (brighter), LP=open (darker) | C037 (S002+S003) |
| X5 volume | 100k placeholder, 50% sim snapshot, value/taper unverified | K7 |

## Source registry / key sources
Check `catalog/sources.json` for the full registry (S001–S013 referenced in project).
- **S001** — DAFx26 (2026) OCD v2 context (not v1.4).
- **S002** — Analog Is Not Dead, *Circuit Analysis: Fulltone's OCD*, https://www.analogisnotdead.com/article34/circuit-analysis-fulltone-s-ocd (accessed 2026-11-10).
- **S003** — zadvitsky OCD clone, http://zadvitsky.com/index.php/projects/pedals/ocd-overdrive-diy.html (accessed 2026-11-09).
- **S007** — TI TL082 (SLOS081O/product), accessed 2026-11-11.
- **S009** — User intake/reconciliation (local:conversation/2026-11-09).
- **S013** — PCB Guitar Mania TOC (OCD) v2.1 (cataloged).
- **S014** — Vishay 1N5817/18/19 datasheet (accessed 2026-11-11; used for 1N5819 Vr=40V limit).

## Main artifacts

### Current spec (v0.4)
- **Spec (base):** `circuit/spec/ocd_v0p4_8v18v.json` — 45 components, validates OK.
- **Spec (merged):** `circuit/spec/ocd_v0p4_8v18v_merged.json` — audio handoff merged; 5 metrics, 14 requirements (E1–E8 + A1–A6).
- **Metric map:** `circuit/spec/ocd_v0p4_metrics-map.json` — gain_db (A5), bandwidth_width_hz (A5), thd_percent (A3), noise_uv, output_vrms (A5); all exploratory.
- **Outputs:** `circuit/spec/out_ocd_v0p4_8v18v/` — `.cir`, `.asc`, `.net`, `.kicad_sch`, `-bom.csv`, `-report.md`, `-report.json`, `-verification.json`, `-test-plan.md`.
- **Superseded:** `circuit/spec/ocd_textsch_s002_9v_v0p1_draft.json` (old v0p1/v0p2 draft) and `circuit/spec/out_textsch_s002_9v/`.

### Verification (latest)
`python3 <skill>/circuit-design-skill/scripts/verify.py circuit/spec/ocd_v0p4_8v18v_merged.json --out circuit/spec/out_ocd_v0p4_8v18v --require design,limits,measurements,simulate`
- **Result: 13 passed, 5 skipped, 0 failed.** Required gates `design`, `limits`, `measurements`, `simulate` all PASS.
- 9V nominal (Drive/Tone/Volume 50%, LP, 100k load, exploratory): gain 44.57dB @1kHz, passband width 1369Hz, THD 66.3%, output noise 141µV, output 0.690Vrms.
- Supply-corner matrix (8/9/18V): VREF~VCC_F/2 at all corners, no op-amp saturation, HP/LP selectable.

### Models / provenance
- `circuit/models/TL082.301` — TI macromodel (vendor, provenance recorded).
- `circuit/models/APPROX_2N7000.lib`, `APPROX_1N34A.lib` — declared project approximations (vendor removed; models gate SKIP); SHA256 recorded.
- `circuit/models/APPROX_1N5819`, `SW1MODEL`, `LED_RED` — declared inline string cards.
- `circuit/models/PROVENANCE.md` — model provenance notes.

## Known gaps / blockers
1. **Footprints for semiconductors** (D_PWR, M1, M2, D1, D_LED) + OPAMP pin maps; `pcb` block expects them (Phase C).
2. **3PDT/jack/battery mechanical:** PCB-mounted jacks + 3PDT fit in 1590B; SW1 physical SPDT pad mapping (K6/K8).
3. **TL082 SLOS081O limits extraction** + bench at 8/9/18V to close D002/A1 (K1/K4/K5).
4. **Pot tapers/values** (X2 1M, X5 100k placeholder) — unverified (K7).
5. **Local environment:** `kiutils`/`kicad-cli` missing; KiCad schematic geometry and PCB DRC/fab deferred. Disk space constrained (~700M avail) — clean `ocd_matrix_*`/`ocd_lean_*` temp dirs after matrix runs.
6. **18V midband gain reduction** is an exploratory model artifact (K5) — bench-verify, do not claim.

## How to regenerate / verify
```bash
cd /home/dave/fulltone-ocd
# 1) Validate base spec
python3 /home/dave/.agents/skills/circuit-design-skill/scripts/design_spec.py validate circuit/spec/ocd_v0p4_8v18v.json
# 2) Merge audio handoff into circuit spec
python3 /home/dave/.agents/skills/circuit-design-skill/scripts/audio_handoff.py \
  --handoff audio/handoff.json --base circuit/spec/ocd_v0p4_8v18v.json \
  --map circuit/spec/ocd_v0p4_metrics-map.json --out circuit/spec/ocd_v0p4_8v18v_merged.json \
  --audio-skill .
# 3) Generate outputs (through-hole passive footprints)
python3 /home/dave/.agents/skills/circuit-design-skill/scripts/generate_with_footprints.py \
  circuit/spec/ocd_v0p4_8v18v_merged.json --out circuit/spec/out_ocd_v0p4_8v18v --assembly through-hole
# 4) Verify (required gates: design, limits, measurements, simulate)
python3 /home/dave/.agents/skills/circuit-design-skill/scripts/verify.py \
  circuit/spec/ocd_v0p4_8v18v_merged.json --out circuit/spec/out_ocd_v0p4_8v18v \
  --require design,limits,measurements,simulate
# 5) Audio handoff strict source check
python3 /home/dave/.agents/skills/audio-engineering-skill/scripts/source_check.py --strict --handoff audio/handoff.json
```

## Recommended next steps (priority order)
1. **Close D002/A1:** TL082 SLOS081O limits extraction + bench verification at 8/9/18V.
2. **Human visual verification of S002 images** (tone-stack rheostat, X5 value/taper).
3. **Resolve D1/M1/M2 part identities**; replace APPROX models with sourced models; record provenance.
4. **Confirm pot tapers/values** (X2, X5).
5. **Footprints + pin maps; 3PDT/jack/battery mechanical fit** (Phase C).
6. **PCB only after all above verified.**

## Communication expectations (from repo AGENTS.md)
Start responses with a **bold summary**. Separate **Changes / Verification / Notes**. Use backticks for paths/commands/IDs. State what was checked and what was intentionally not changed or remains unverified.

## Session-end state (2026-11-11)
- **Last completed:** Phase A+B electrical design (v0.4): C4/C8 series feedback fix, V_IN/V_AC AC-source split, 1N5819 protection, LED, 9V battery/DC-jack, HP/LP SW1, tone-stack rheostat + HP/LP correction, models cleaned (vendor removed from APPROX), verify.py clean (13 passed, 5 skipped, 0 failed), supply-corner matrix done.
- **No fabrication-ready output produced.** PCB deferred to Phase C.
- **Next agent should start by** reading this file + `circuit/design-plan.md` + `circuit/research-log.md`, then close D002/A1 (TL082 bench at 8/9/18V) and resolve semiconductor footprints/pin maps for Phase C.

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
Check `catalog/sources.json` for the full registry (S001–S019 referenced in project).
- **S001** — DAFx26 (2026) OCD v2 context (not v1.4).
- **S002** — Analog Is Not Dead, *Circuit Analysis: Fulltone's OCD*, https://www.analogisnotdead.com/article34/circuit-analysis-fulltone-s-ocd (accessed 2026-11-10).
- **S003** — zadvitsky OCD clone, http://zadvitsky.com/index.php/projects/pedals/ocd-overdrive-diy.html (accessed 2026-11-09).
- **S007** — TI TL082 (SLOS081O/product), accessed 2026-11-11.
- **S009** — User intake/reconciliation (local:conversation/2026-11-09).
- **S013** — PCB Guitar Mania TOC (OCD) v2.1 (cataloged).
- **S014** — Vishay 1N5817/18/19 datasheet, https://www.vishay.com/docs/88525/1n5817.pdf (accessed 2026-11-11; HTTP 200, Last-Modified 2026-04-03, sha256 `4465c825...`; registered in `catalog/sources.json`; used for 1N5819 Vr=40V limit).

## Main artifacts

### Current spec (v0.4)
- **Spec (base):** `circuit/spec/ocd_v0p4_8v18v.json` — 45 components, validates OK.
- **Spec (merged):** `circuit/spec/ocd_v0p4_8v18v_merged.json` — audio handoff merged; 5 metrics, 14 requirements (E1–E8 + A1–A6).
- **Metric map:** `circuit/spec/ocd_v0p4_metrics-map.json` — gain_db (A5), bandwidth_width_hz (A5), thd_percent (A3), noise_uv, output_vrms (A5); all exploratory.
- **Outputs:** `circuit/spec/out_ocd_v0p4_8v18v/` — `.cir`, `.asc`, `.net`, `.kicad_sch`, `-bom.csv`, `-report.md`, `-report.json`, `-verification.json`, `-test-plan.md`.
- **Master BOM:** `circuit/bom-v0.4.csv` — 51 orderable line items (44 electrical + 7 board-level: jacks, DC jack, headers, mounting holes); every non-simulation ref reconciled; sim-only refs (V1, V_IN, V_AC, V_HP, R_LOAD) excluded. Pot values/tapers for X2/X4/X5 flagged TBD/unverified.
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

## Phase C — PCB (routed prototype, gates passed)

Board spec: `circuit/spec/ocd_v0p4_8v18v.json` → `pcb` block. Generated handoff:
`pcb/handoff/` (overlay, pin map, node aliases, `.cir`). Board notes and wiring
tables: `pcb/README.md`. Released artifacts: `pcb/board/` (board, Gerbers,
drill, position, STEP, IPC-D-356, `fabrication.zip`, DRC report, gate report).

- **Board:** 108 × 58 mm, 2-layer, 1.6 mm, 1 oz, THT, `2layer-low-speed`.
- **Placed parts:** 46 = 42 electrical + 4 M3 mounting holes.
- **U1 (DIP-8 TL082)** merges `X1A` + `X3A`; both sections are excluded from
  the LTspice import.
- **Pots:** `X2` (1 M Drive), `X4` (10 k Tone), `X5` (100 k Volume) replace the
  fixed simulation placeholders `R_X2POT`, `R_X4`, `R_VOL5A/B`; the placeholders
  are excluded. Rheostat wiring ties the unused end to the wiper.
- **Jacks:** `J_IN` Neutrik NMJ6HFD2 (stereo, ring = `BAT_NEG` battery
  disconnect), `J_OUT` NMJ4HFD2 (mono).
- **Power:** `J_PWR` CUI/Same Sky PJ-102AH center-negative switched jack
  (pad 1 = GND, pad 2 = `VCC_JACK`, pad 3 = `BAT_POS`), `BT1` 1×02 battery
  snap header.
- **Switches:** `SW_FS` 2×05 header (wire header pin *n* to 3PDT pin *n*),
  `SW_HP` 1×03 header (short 1–2 for HP).
- **Pin maps:** 2N7000 TO-92 `d=3, g=2, s=1, b=1` (S008); KiCad diodes/LED
  anode→pad 2, cathode→pad 1 (S019); TL082 DIP-8 standard (S007).
- **Deviation:** the LED is always-on in the electrical model. On the board,
  3PDT pole 3 shorts `LED_A` to `GND` in bypass, so the physical LED is on only
  when the effect is engaged. This is a board-level behavior, not a schematic
  change.
- **Gate result:** CI run 43059805373 — structural 0, DRC 0, unconnected 0,
  DFM 0, netlist parity 0, stackup 0, impedance 0, length match 0, fab 0.
  46 footprints, 29 nets, 261 track segments, 2 vias, 2 GND zones, 1270.7 mm
  track length. Report: `pcb/board/design-report.md`.
- **Not closed:** panel fit to a specific 1590B drilling; 3PDT PCB footprint;
  pot CW/CCW end assignment (C046); pot tapers/values (K7); bench behavior of
  the real 2N7000/1N34A (K2). The board is a **routed prototype with the
  automated release gates passed**, not a panel-verified assembly.

CI backend: `davlug3/pcb-design-skill` branch `ocd-v0p4`, workflow
`Design pipeline`, staged under `specs/ocd-v0p4/`. Transient artifacts download
to `pcb/build/`; the tracked release copy is `pcb/board/`.

## Known gaps / blockers
1. **Footprints for semiconductors** (D_PWR, M1, M2, D1, D_LED) + OPAMP pin maps; `pcb` block expects them (Phase C).
2. **3PDT/jack/battery mechanical:** PCB-mounted jacks + 3PDT fit in 1590B; SW1 physical SPDT pad mapping (K6/K8).
3. **TL082 SLOS081O limits extraction** + bench at 8/9/18V to close D002/A1 (K1/K4/K5).
4. **Pot tapers/values** (X2 1M, X5 100k placeholder) — unverified (K7).
5. **Local environment:** `kiutils`/`kicad-cli` missing; KiCad schematic geometry and PCB DRC/fab deferred. Disk space constrained (~700M avail) — clean `ocd_matrix_*`/`ocd_lean_*` temp dirs after matrix runs.
6. **18V clip-bias/threshold (C042):** the 18V gain drop is a clip-network threshold effect (M1 `Vgs = VREF - CLIP_A` crosses the 2N7000 `Vgs(th)`), not an op-amp artifact. VTO=2.1 gives 22.2 dB at 18V; VTO>=2.5 gives 44.6 dB. Bench-verify with the selected 2N7000 (K2), do not claim 18V performance.

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
1. **Close Phase C mechanical:** panel-fit the prototype board to the chosen
   1590B drilling; fix pot/jack/3PDT heights and positions (the jacks are at
   different heights to clear the corner holes); confirm the pot CW/CCW end
   assignment on hardware (C046).
2. **Close D002/A1:** TL082 SLOS081O limits extraction + bench verification at
   8/9/18V.
3. **Human visual verification of S002 images** (tone-stack rheostat, X5
   value/taper).
4. **Resolve D1/M1/M2 part identities**; replace APPROX models with sourced
   models; record provenance; bench the 18V clip-bias threshold (K2).
5. **Confirm pot tapers/values** (X2, X5).
6. **Release the PCB only after the gate report and required sign-offs pass.**

## Communication expectations (from repo AGENTS.md)
Start responses with a **bold summary**. Separate **Changes / Verification / Notes**. Use backticks for paths/commands/IDs. State what was checked and what was intentionally not changed or remains unverified.

## Session-end state (2026-11-11)
- **Phase A+B electrical design (v0.4):** C4/C8 series feedback fix,
  V_IN/V_AC AC-source split, 1N5819 protection, LED, 9V battery/DC-jack,
  HP/LP SW1, tone-stack rheostat + HP/LP correction, models cleaned (vendor
  removed from APPROX), verify.py clean (13 passed, 5 skipped, 0 failed),
  supply-corner matrix done. Follow-up: S014 added/verified, master BOM
  `circuit/bom-v0.4.csv` built and reconciled, `PROVENANCE.md` updated, 18V
  anomaly root-caused (C042: clip-bias/threshold, not op-amp).
- **Phase C PCB prototype:** `pcb` block, footprints, pin maps, extra board
  parts and mounting holes added; handoff regenerated; LTspice import resolves
  46 parts with 0 validation errors. Board built/routed by the
  `pcb-design-skill` CI backend (KiCad 9 + Freerouting). **Not panel-fitted and
  not released.** See `pcb/README.md` and `pcb/build/design-report/`.
- **No fabrication-ready output produced.** The board is an electrically
  resolved prototype; mechanical fit and bench verification remain open.
- **Next agent should start by** reading this file + `pcb/README.md` +
  `circuit/design-plan.md` + `circuit/research-log.md`, then close the Phase C
  mechanical fit and D002/A1 bench items.

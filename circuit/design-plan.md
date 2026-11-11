# Design Plan — OCD-style Overdrive Clone (v0.4)

Status: **Phase 0 complete, Phase 1 complete, Phase A+B complete (electrical design), Phase C routed prototype (automated release gates passed).**
Date: 2026-11-11

## 1. Scope lock (reconciled 2026-11-09, C022/S009)
- **Product:** v0.4, unbranded OCD-style overdrive (not branded as Fulltone/OCD)
- **Supply:** **8–18V DC, center-negative** (5V dropped), 9V nominal test
- **Bypass:** True bypass (external to SPICE core; 3PDT physical switching Phase C)
- **Enclosure/layout:** **1590B enclosure, 108 x 58 mm PCB, through-hole** (board target recorded in spec `pcb` block; PCB work Phase C)
- **Added features:** 1N5819 series reverse-polarity protection, status LED + 4.7k, 9V battery via switching DC jack + input-jack battery disconnect, PCB-mounted I/O jacks + 3PDT
- **Anchors:** Hybrid **S002+S003** cross-checked with **S001/S013** (provenance-labeled)
- **Reference topology:** v1.4/v1.7-style working reference — TL082 candidate (D002 validate 8–18V), 2N7000 + Ge (1N34A) asymmetric clipping to floating Vref, passive tone + HP/LP
- **Substitutions:** Allowed with datasheet/SPICE provenance and recorded decisions

## 2. Skills/workflow
- `audio-engineering-skill`: requirements, budgets, evidence, `handoff.json` (validated via `source_check.py --strict`)
- `circuit-design-skill`: spec/netlist/schematics, model provenance, simulation/verification
- `pcb-design-skill`: footprints/layout/DRC/fab (Phase C — deferred, no kicad-cli/kiutils locally)

## 3. Artifacts produced (current)
| Artifact | Path | Status |
|---|---|---|
| Requirements | `audio/audio-requirements.md` | Draft; A4 rewritten as audio-observable bias stability; A5/A6 added |
| Handoff | `audio/handoff.json` | Passes `source_check.py --strict`; A1–A6 + 5 exploratory metrics |
| Research log | `circuit/research-log.md` | S1–S9 + 2026-11-11 v0.4 update; Q1–Q6 open |
| Circuit spec (base) | `circuit/spec/ocd_v0p4_8v18v.json` | `design_spec.py validate` OK |
| Circuit spec (merged) | `circuit/spec/ocd_v0p4_8v18v_merged.json` | `audio_handoff.py` merge OK; 5 metrics, 14 requirements |
| Metric map | `circuit/spec/ocd_v0p4_metrics-map.json` | gain_db, bandwidth_width_hz, thd_percent, noise_uv, output_vrms |
| Circuit outputs | `circuit/spec/out_ocd_v0p4_8v18v/` | SPICE/LTspice/KiCad/BOM/report generated (through-hole passive footprints) |
| Verification | `circuit/spec/out_ocd_v0p4_8v18v/ocd_v0p4_8v18v-verification.json` | **verify.py: 13 passed, 5 skipped, 0 failed**; required design/limits/measurements/simulate PASS |
| Master BOM | `circuit/bom-v0.4.csv` | 51 line items (44 electrical + 7 board-level); every non-sim ref reconciled; sim-only refs excluded |
| Evidence | `evidence/claims.jsonl` (C001–C048) | C034–C042 electrical; C043–C048 PCB pinouts and overlay |
| Source registry | `catalog/sources.json` (S001–S019) | S014–S019 added and URL-verified 2026-11-11 |
| S002 images | `circuit/sources/s002-images/` | 5 PNG files downloaded |
| Models | `circuit/models/` | TL082.301 vendor; APPROX_2N7000/1N34A/1N5819/SW1MODEL/LED_RED declared; `PROVENANCE.md` v0.4 |
| PCB handoff | `pcb/handoff/` | Overlay, pin map, node aliases, `.cir`; 46 parts (42 electrical + 4 holes) |
| PCB notes | `pcb/README.md` | Board, pin maps, wiring, deviations, open items |
| PCB build | `pcb/board/` + `pcb/build/` | `pcb/board/` is the tracked release (board, Gerbers, drill, zip, DRC, gate report); `pcb/build/` is the transient CI download |

### Phase C — PCB (routed prototype, gates passed)

- **Board:** 108 × 58 mm, 2-layer, 1.6 mm, 1 oz, THT, `2layer-low-speed`.
- **Anchored:** 4 × M3 holes, the DIP-8 `U1`, the three pots and the two
  jacks; auto-placement handles the DC jack, headers, battery header and small
  parts. The placement engine now uses each footprint's real bounding-box
  offset (`pcb-design-skill` commit `8f60198`) and its text-free mechanical
  box, so the jack noses sit on the side edges. The jacks are at different
  heights (in `y=25`, out `y=33`) to clear the corner holes; panel fit is
  still open.
- **Pin maps:** 2N7000 TO-92 `d=3, g=2, s=1, b=1` (S008); KiCad diodes/LED
  anode→pad 2, cathode→pad 1 (S019); TL082 DIP-8 standard (S007).
- **Deviation:** the LED is always-on in the electrical model; 3PDT pole 3
  switches it on the board.
- **Gate result:** CI run 43059805373 — structural 0, DRC 0, unconnected 0,
  DFM 0, netlist parity 0, stackup 0, impedance 0, length match 0, fab 0.
  46 footprints, 29 nets, 261 track segments, 2 vias, 1270.7 mm track length.
  Release copy: `pcb/board/`; report: `pcb/board/design-report.md`.
- **Open:** panel fit, pot CW/CCW, pot tapers/values, real-device bench (K2/K7).
- **Status:** routed prototype with the automated release gates passed; not a
  panel-verified assembly.

## 4. Critical risks / gates (from spec `design.risks`)
1. **K1/K4 — TL082 at 8V:** DC sweep/OP at 8/9/18V shows Vref~VCC_F/2, no saturation. SLOS081O extraction + bench verification still needed for formal closure (8V margin ~0.7V with 1N5819; P-FET fallback).
2. **K3/Q1 — No locked traceable schematic:** S002 schematic image inspected; clip wiring confirmed (C031/C032), X1/X3 feedback pin wiring assumed from S002 text. Not fabrication-ready until pin-level verified.
3. **K6/K8 — 3PDT/jack/battery mechanical:** PCB-mounted jacks + 3PDT mechanical alignment and SW1 physical SPDT pad mapping unproven (Phase C).
4. **K2 — Ge diode variability:** 1N34A Vf/leakage varies; clipping behavior may need selection/tolerance.
5. **K5 — Model artifact (headroom):** TL082 model supply current (~3-6x datasheet) makes simulated VCC_F/headroom pessimistic; use datasheet limits for headroom decisions.
6. **K7 — Pot values/tapers:** X2 (1M) mapping assumed; X5 (100k) placeholder not in S002 text; tapers unverified.
7. **APPROX models:** All discrete device models are project approximations, not manufacturer models. Simulation-only results.
8. **18V clip-bias/threshold (C042):** the 18V gain drop is caused by M1's ratiometric gate bias (`Vgs = VREF - CLIP_A`) crossing the 2N7000 `Vgs(th)`; VTO=2.1 gives 22.2 dB at 18V, VTO>=2.5 gives 44.6 dB. Real behavior depends on the selected 2N7000 and exact bias — bench-verify, do not claim 18V performance.

## 5. Environment
- Python 3.14.4, ngspice available (simulation feasible locally)
- `kicad-cli`/`kiutils` missing locally; PCB build/routing/DRC/fab run in the `pcb-design-skill` CI backend (KiCad 9 + Freerouting)
- Disk space constrained in temp dir (~700M available) — clean `ocd_matrix_*` temp dirs after matrix runs

## 6. Next actions (priority order)
1. **Close Phase C mechanical fit:** panel-fit the routed board to a specific
   1590B drilling; verify pot/jack/3PDT heights and the pot CW/CCW end
   assignment on hardware (C046).
2. **Close D002/A1 + 18V behavior:** Extract TL082 SLOS081O limits (min supply, output swing vs load/supply, input common-mode); bench-verify at 8/9/18V (DC sweep simulation already passed). Also bench the 18V clip-bias threshold with the selected 2N7000 (C042/K2).
3. **Human visual verification of S002 images** in `circuit/sources/s002-images/` (tone-stack rheostat wiring, X5 value/taper).
4. **Resolve D1/M1/M2 part identities** and replace APPROX models with sourced models where available; record provenance in `circuit/models/PROVENANCE.md`.
5. **Confirm pot tapers/values** (X2 gain 1M, X5 volume 100k) from S002 image or authorized source.
6. **Audio handoff alignment:** `audio/audio-requirements.md` and `audio/handoff.json` already aligned to v0.4 (A4/A6).
7. **Panel-fit and sign off the released board.** The automated gates passed
   (CI run 43059805373); `pcb/board/` holds the board, Gerbers, drill, STEP,
   IPC-D-356, `fabrication.zip` and the gate report. Local
   `kicad-cli`/`kiutils` are still missing, so rebuilds go through the
   `pcb-design-skill` CI backend (KiCad 9 + Freerouting).

# Schematic — v0.2 Hybrid Working Reference (EXPLORATION / MERGE DRAFT)

**Status:** Draft merge (2026-11-09). **Not a verified pin-level netlist.** User authorized S013 (PCB Guitar Mania TOC v2.1), S001 (DAFx26), S002 (Analog Is Not Dead) and requested merging best features; not tied to a particular version (C018).

## Confirmed defaults
- True-bypass core, **no buffer by default** (S013 buffers Q3/Q4/SW2/SW3 excluded).
- **5–18V DC center-negative** (D002 critical at 5V).
- Most-available parts (D003): **BAT46-class Schottky default** on versatile clipping pads; selected 1N34A-class Ge optional; 1N4148 optional. **Floating VREF clipping topology preserved** (C003/C004). No identical-tone claim.
- TL082 validated first (D002).

## Source merge
| Layer | Primary reference | Secondary/cross-check | Status |
|---|---|---|---|
| Topology/behavior | S002, S001 | S013 | Core blocks clear; pin-level wiring incomplete |
| Numeric baseline (exploration) | S001 DAFx26 v2 Table 1/2 (C020) | S013 version deltas, S002 | **Exploration only** (v2-derived; verify table against PDF before build) |
| Practical BOM/options | S013 | D003 | Extracted (p.2-5); schematic image not extracted |
| 5V feasibility | S007, D002, C011, C021 | exploration sims | **Unresolved** |

## Core block flow (normalized)
`IN -> input/bias -> TL082 gain1 (Drive) -> series R -> CLIP to VREF (2N7000 paths + D3 option, D003) -> TL082 gain2 -> HP/LP + Tone -> Volume -> OUT`; `3PDT` true bypass. `VCC(5-18V) -> protection/decoupling -> rail; divider/filter -> VREF(~VCC/2)`.

## S013 buffer exclusion (default)
PCB Mania TOC includes `Q3 2N5088, Q4 2N5457, SW2, SW3, R16-R22,R26-R30,C13,D4 (per extracted BOM context)` for selectable buffers. **Excluded from v0.2 default**; may be added as a separate variant only with a verified netlist and its own decision record.

## Verified-netlist gap (blocking fabrication)
1. S013 schematic (p.6) is an image — **connections/pin wiring not extracted**.
2. S002 schematic is an image.
3. S001 provides v2 values but full node wiring must be taken from the verified DAFx26 schematic for any DAFx26-based sim; I used search-extracted Table 1/2 only.
4. TL082/2N7000 pinouts must come from datasheets for chosen packages.

## Next concrete implementation steps
1. Lock node-level netlist: either (a) user pastes key S013/authorized schematic connections, or (b) implement from DAFx26 full schematic text/table verification (explicitly labeled v2-exploration baseline adapted to v0.2 defaults).
2. Build `circuit/base-spec.json` (circuit-design-skill schema) + validated ngspice 5/9/18V (D002) with provenance-tracked models.
3. Run `audio_handoff.py` merge, `generate.py`, `verify.py`; record results.
4. Resolve D002 (SLOS081O + validated sim). If TL082 fails at 5V, open substitution decision.

# Decision Record D001 — Hybrid reference (v0.2)

## Status
**Active** — 2026-11-09 (supersedes strict v1.4-only lock for baseline). User authorized: PCB Guitar Mania TOC (OCD) v2.1 (S013), DAFx26 (S001), Analog Is Not Dead (S002). User stated: **not tied to a particular version; merge best features**.

## Confirmed baseline (v0.1/v0.2)
- Unbranded OCD-style overdrive (C001).
- **5–18V DC, center-negative** (C002, D002).
- **True bypass core**; no input/output buffer by default (user confirmed).
- **Most-available parts + versatile clipping** (D003): **BAT46-class Schottky default** on versatile pads; selected 1N34A-class Ge optional; 1N4148 optional. **Floating VREF (~VCC/2) clipping topology preserved** (C003/C004). No identical-tone claim.
- TL082 validated first for 5V (D002); substitute only if A1 fails.

## Source roles
| Source | Role | Limitation |
|---|---|---|
| S013 PCB Mania TOC v2.1 | Practical BOM/version deltas, part availability, multi-version options; confirms TL082/2N7000/1N34A option/controls | Third-party multi-version PCB; includes buffers not in default; schematic image not extracted here; version-column mapping to Fulltone revisions needs care |
| S001 DAFx26 (OCD v2) | Complete numeric/structural exploration baseline (Table 1/2) | OCD **v2** model, not v1.4; values used for exploration/spec scaffolding only until verified |
| S002 Analog Is Not Dead | Topology/behavior, Vref, 18V headroom, clipping-to-Vref explanation, conflict flag on clipping wiring | Schematic image; incomplete verified BOM |

## Merge rules
1. Cite per-item provenance. 2. Resolve conflicts by explicit decision. 3. Mark unextracted/unverified wiring/pinouts as `TBD/unverified`. 4. Keep default build simple (no buffer).

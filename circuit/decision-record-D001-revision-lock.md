# Decision Record D001 — Reference revision lock (v0.1)

## Status
**Confirmed (v1.4-style) + working reference authorized** — 2026-11-09. User instructed: create schematic/BOM using `audio-engineering-skill`/`circuit-design-skill`/`pcb-design-skill`. Assistant produced a **working cross-check** from S2/S3 (`circuit/schematic-v0.1.md`, `circuit/bom-v0.1.csv`).

## Decision
Lock **v1.4-style OCD topology** as the primary reference. Use a **project-normalized working schematic/BOM** synthesized from S2+S3 with full provenance labeling for v0.1 design/simulation, with deviations: **8–18V DC center-negative** (D002, reconciled 2026-11-09; 5V dropped by explicit user decision), **true bypass** (C002), **most-available parts / versatile clipping** (D003). Anchors: hybrid **S002+S003** cross-checked with **S001/S013** (provenance-labeled; not a verified Fulltone netlist).

## Verification gate
- **For simulation/design iteration:** working artifacts are traceable to S2/S3 and may proceed with all unverified items labeled.
- **For fabrication/verified clone netlist:** confirm all values, refdes mapping, node wiring (especially clipping orientation per S2 comment conflict), and pinouts against a traceable schematic and manufacturer datasheets. Do not claim verified equivalence to any Fulltone revision.

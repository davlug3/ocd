# v0.1 Reference capture (v1.4-style, UNVERIFIED working synthesis)

**Status:** Working reference for design capture. **Not a verified clone netlist.** Cross-checked from **S002** (Analog Is Not Dead, opened 2026-11-09) and **S003** (zadvitsky, opened 2026-11-09), with cross-check context from **S001/S013** (cataloged; PDFs not fully extracted in this session). Values/net mapping are provisional; confirm against a traceable schematic/BOM and datasheets before fabrication (D001 verification gate).

## Locked decisions (reconciled 2026-11-09, C022/S009)
- **Supply:** 8–18V DC center-negative (**5V dropped**).
- **Anchors:** hybrid **S002+S003** cross-checked with **S001/S013** (provenance-labeled).
- **D001:** v1.4-style reference as primary working topology.
- **D002:** Validate TL082 for **8–18V** first; substitute only with datasheet/SPICE provenance and recorded decision if A1 fails.
- **D003:** Most-available default BOM/versatile clipping; **default BAT46-class Schottky** (assumption), selected Ge (1N34A-class) optional, 1N4148 optional — preserving floating-Vref topology (C003). **No identical OCD tone claim**.
- **Bypass/scope:** unbranded v0.1, true bypass (C002).

## Cross-checked topology blocks (S1–S3 context)
| Block | Function | Notes |
|---|---|---|
| Power input/filter | 2.1mm center-neg DC jack, reverse protection (proposed), bulk+HF decoupling | S2: R1/C2/C3 filter; S3: D1 protection, C1/C2. 8–18V range (C022). |
| Vref | ~Vcc/2 bias for single-supply op-amps/clipping reference | S2: R4,R7,C5; values vary by source/rev. Ideal 100k/100k: 4V @ 8V, 4.5V @ 9V, 9V @ 18V (C008 method). |
| Input | Coupling, pull/reference, series limit, bias to Vref | S2: C1,R2(1M),R3,R6; S3: C5,R5,R3,R4. **Refdes differ between sources.** |
| Gain 1 | TL082A non-inverting candidate, variable Drive | S3: k=1+(1M+18k)/2.2k=464 max (~53dB) stated; refdes mapping uncertain. **8V CM/swing/headroom risk (D002/C023).** |
| Clipping | Series R into asymmetric network referenced to **VREF** (not ground): 2N7000 body-diode paths + Ge/asymmetric element in v1.4 character | S1–S3. Floating-Vref topology key (C003/C004). **S2 comment notes possible wiring/orientation conflict vs other references** — resolve before fabrication. D003 adds versatile options. |
| Gain 2 | TL082B recovery/buffer gain | Exact values TBD from traceable schematic. |
| Tone/HP-LP/Volume | Passive treble cut, HP/LP voicing, output level | S2/S3 naming differs; load-dependent. |
| True bypass | 3PDT mechanical bypass | C002/A2. |

## D001 gate status
- Working artifacts exist (`circuit/schematic-v0.1.md`, `circuit/bom-v0.1.csv`, etc.) and are **provisional**.
- **Verified-build gate open:** confirm all values/refdes/pinouts/orientation against a traceable schematic and datasheets before PCB/fabrication.

## TL082 8V feasibility (D002, C023)
- TI TL082 page (S007, opened 2026-11-09): **min supply 7V**, **CM headroom to V− typ 3V**, **output swing headroom typ 1.5V/rail**. At **Vcc=8V, Vref=4V**, typical CM margin exists but swing/headroom are condition-dependent — **plausible, unverified**. Requires SLOS081O extraction + provenance-tracked SPICE/bench at **8/9/18V**. *Validate TL082 first; substitute only with provenance/decision if A1 fails.* Historical 5V risk retained in D002/research log.

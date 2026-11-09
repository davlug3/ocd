# Authorized source extracts (v0.2 hybrid, 2026-11-09)

User authorization (2026-11-09): "authorize PCB Guitar Mania, AND DAFx26 OCD Model AND Analog is not Dead. not tied to a particular version; merge the best features of each one."  
**Original defaults (superseded in part):** true-bypass core, 5–18V, most-available parts, BAT46 default clipping with Ge/1N4148 options, no buffer by default.  
**Reconciliation (2026-11-09, C022/S009):** **8–18V DC center-negative** (5V dropped); hybrid anchors **S002+S003** cross-checked with **S001/S013**; substitutions allowed with provenance; **D002 validate TL082 at 8–18V**. Other defaults unchanged unless noted.

## 1) PCB Guitar Mania TOC (OCD) v2.1 Build Docs
- **File provided by user:** `/mnt/c/Users/iHOMS-DAVE/Downloads/TOC-2v1-Building-Docs.pdf` (also `/tmp/opencode/TOC-2v1-Building-Docs.pdf`)
- **Source URL (from PDF metadata/strings):** https://www.musikding.de/PCB-Guitar-Mania_2 (link) / PCB Guitar Mania build doc "TOC (OCD) by PCB Guitar Mania", Document version 2.1v, 13th April 2022
- **Accessed/extracted:** 2026-11-09 via pypdf.
- **Nature:** Third-party multi-version PCB design. Includes core OCD-style circuit plus **optional input/output buffers** (`Q3 2N5088`, `Q4 2N5457`, `SW2/SW3`, associated R/C/D4 parts). **v0.1 default excludes buffer** (user confirmed).
- **BOM (version 3 base, p.3):** R1 1M, R2 10K, R3 1M, R4* 2K2, R6 18K, R7 10K, R8 10K, R9 39K, R10 150K, R11 22K, R12 33K, R14 1K, R16 510K, R17 10K, R18 100r, R19 47K, R20 27r, R21 10K, R22 10K, R26 10K, R27 10K, R28 1K, R29 27K, R30 10K. C1 22n, C2* 68n, C3 220p, C4 1n, C5 100n, C6 220p, C7 1u, C8* 47n, C9 100n, C10 1u. C11/C12 220u, C13 10u. Q1/Q2 2N7000, Q3 2N5088, Q4 2N5457. IC1 TL082. Pots: TONE B10K, VOL A100K, DRIVE A1M. SW1 SPDT, SW2 SPDT, SW3 SPDT, 3PDT stomp. D1 Jumper*, D2 1N5817, D3 3mm red LED, D4 9.1V zener.
- **Version table (p.5):** V1-V4/JHS/PCB MANIA differences — R4* (2k2/2k2/2k2/2k2/4k7/3k3), C2* (68n/68n/68n/68n/100n/100n), C8* (47n/47n/47n/47n/47n/22n), D1* (Jumper/Jumper/Jumper/1N34a/Jumper/Jumper), DRIVE (A500K/A500K/A1M/A1M/A1M/A1M), TONE (A25K/A25K/B10K/B10K/B10K/B10K), VOL (B100k/B500k/B500k/A500k/A500k/A100k).
- **Schematic (p.6):** image in PDF; text not extracted. **Pin-level connections/wiring not fully extractable here** — requires manual schematic reading or pasted netlist for verified netlist.
- **Use in v0.2:** practical BOM/version-delta reference, part availability context, confirms TL082/2N7000/1N34A option/HP-LP-style controls. **Not used as sole verified netlist** due to buffer/variant complexity and unextracted schematic.

## 2) DAFx26 (S001)
- **URL:** https://dafx.de/paper-archive/2026/papers/DAFx26_paper_24.pdf
- **Title:** Explicit Wave Digital Model of the Fulltone OCD Pedal Based on Canonical Piecewise-Linear Functions (Giampiccolo et al., DAFx26, 2026)
- **Accessed:** 2026-11 (project); table text observed via web search 2026-11-09.
- **Nature:** Peer-reviewed **OCD v2** model (not v1.4). Provides complete component parameter set useful for traceable exploration.
- **Table 1 (search-extracted, verify against PDF):** R1 10k, R2 1M, R3 470k, R4 18k, R5 500k, R6 2.2k, R7 10k, R8 220k, R9 10k, R10 150k, R11 39k, R12 33k, R13 22k, R14 10k, R15 500k, C1 22nF, C2 220pF, C3 100nF, C4 10nF, C5 220pF, C6 100nF, C7 10µF, C8 47nF, Vb 4.5V.
- **Table 2 (search-extracted):** 1N34A Is 2.58µA, n 1.61, Vt 25.8mV, Rs 1n, Rp 1T. 2N7000 kn 0.025 A/V^2, Vth 2.1V, lambda 0.02.
- **Use in v0.2:** **numeric baseline for SPICE exploration / draft spec structure**, clearly labeled as OCD v2-derived baseline adapted to v0.1 requirements (**8–18V** after C022 reconciliation, true bypass, D003). Not a claim of v1.4 equivalence.

## 3) Analog Is Not Dead (S002)
- **URL:** https://www.analogisnotdead.com/article34/circuit-analysis-fulltone-s-ocd
- **Accessed:** 2026-11 (project); 2026-11-09.
- **Nature:** Practitioner stage-by-stage analysis. Key topology facts extracted in text: 9V (up to 18V) supply; R1/C2/C3 filter; R4,R7,C5 form Vref ≈ Vcc/2 (4.5V at 9V); TL082 dual op-amp non-inverting stages; 2N7000/1N34A clipping stage between gain stages; passive treble bleed + HP/LP switch parallels R14/R15; input ~330k noted; MOSFETs described as diode-like clipping in that topology. Schematic image not machine-extracted. Comment notes other references show clipping wired differently.
- **Use in v0.2:** topology/behavior explanation, Vref concept, 18V headroom rationale, and conflict flag on clipping wiring. Not a complete verified BOM.

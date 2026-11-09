# SPICE model provenance (v0.1 exploration)

| File | Part | Source | Accessed | SHA256 | Status |
|---|---|---|---|---|---|
| `TL082.301` | TL082 (macromodel) | TI SLOJ070 ZIP https://www.ti.com/lit/zip/sloj070 (TL082.301 inside) | 2026-11-09 | `adad2e131f728610963e0797670ea34d2857c0b26b3f49c6ce356a3213d89011` (file) / zip `4f27e17a7c...` | TI-sourced file; subckt pin order per header: 1=non-inv,2=inv,3=V+,4=V-,5=out. Verify suitability/terms for your use. Exploration only. |
| `1N4148.lib` | 1N4148 | NXP via PySpice/KiCad mirror (model_fetch.py) | 2026-11-09 | `db2ee7a8...` (see .sha256) | Verified fetch; SPICE node 1=anode,2=cathode (SOD-27 PCB pin order differs). |
| `APPROX_2N7000.lib` | 2N7000 | **Approximation** authored for exploration; NOT a manufacturer model | 2026-11-09 | (computed on write) | **UNVERIFIED/APPROX.** Level-1 NMOS + body diode placeholders; do not use for fabrication decisions. |
| `APPROX_1N34A.lib` | 1N34A Ge | **Approximation** from DAFx26-style params (S001/C016 context) | 2026-11-09 | (computed on write) | **UNVERIFIED/APPROX.** Ge diodes vary widely (C009/S009). |
| `APPROX_BAT46.lib` | BAT46-class Schottky | **Approximation** for D003 exploration | 2026-11-09 | (computed on write) | **UNVERIFIED/APPROX.** Use manufacturer model when selected. |

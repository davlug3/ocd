# SPICE model provenance (v0.4)

Status: project exploration. **No discrete device model here is a manufacturer
model unless the row says vendor.** Simulation results are only as good as these
models; treat APPROX/declared models as exploratory and bench-verify before any
fabrication or performance claim.

## Model files

| File | Part | Source | Accessed | SHA256 | Status |
|---|---|---|---|---|---|
| `TL082.301` | TL082 (macromodel) | TI SLOJ070 ZIP https://www.ti.com/lit/zip/sloj070 (TL082.301 inside); S007 | 2026-11-09 | `adad2e131f728610963e0797670ea34d2857c0b26b3f49c6ce356a3213d89011` | **Vendor** (TI). Subckt pin order per header: 1=non-inv, 2=inv, 3=V+, 4=V-, 5=out. Verify terms/suitability. |
| `1N4148.lib` | 1N4148 | NXP via PySpice/KiCad mirror (`model_fetch.py`) | 2026-11-09 | `db2ee7a82fd6398c2abb233b03e27f76fa2df1aca33a252adc24696b8764f8a7` | Verified fetch; SPICE node 1=anode, 2=cathode (SOD-27 PCB pin order differs). Not used in v0.4 netlist. |
| `APPROX_2N7000.lib` | 2N7000 | **Approximation authored for exploration; NOT a manufacturer model** | 2026-11-09 | `081054dff4a75cb511fef93cd2e8c4310a685018b570eb92f2f241bc9b992a55` | **Declared/APPROX.** Level-1 NMOS + body-diode placeholder. No vendor field (models gate = SKIP). |
| `APPROX_1N34A.lib` | 1N34A Ge | **Approximation from DAFx26-style params (S001/C016)** | 2026-11-09 | `db949f2074c80243651fc2ab6c003f27fecc0fba127df704fcdba44427450aaa` | **Declared/APPROX.** Ge diodes vary widely (C009/S009). No vendor field (models gate = SKIP). |
| `APPROX_1N4148.lib` | 1N4148 | **Approximation** | 2026-11-09 | `bfa7e99c8627cad9b8f3d58bc8479b9e075bded3914e9da9fdd52fee30596daa` | **Declared/APPROX.** Not used in v0.4 netlist. |
| `APPROX_BAT46.lib` | BAT46-class Schottky | **Approximation for D003 exploration** | 2026-11-09 | `7b617c80cc7481ad33ce728db7e09b1860f1bb6143f9c8701b954c6616e295b3` | **Declared/APPROX.** Not used in v0.4 netlist. |

## Inline model cards (declared in the spec `models` block)

| Name | Card | Part | Status |
|---|---|---|---|
| `APPROX_1N5819` | `.model APPROX_1N5819 D(Is=1e-6 N=1.05 Rs=0.05)` | 1N5819 Schottky (D_PWR) | **Declared/APPROX.** Forward drop ~0.25-0.3 V. Real part is Vishay 1N5819 (S014, Vr=40 V). |
| `SW1MODEL` | `.model SW1MODEL SW(Ron=0.05 Roff=1e6 Vt=2.5 Vh=0.1)` | HP/LP switch (SW1) | **Declared/ideal.** Voltage-controlled switch stand-in; physical part is an SPDT. |
| `LED_RED` | `.model LED_RED D(Is=4.3e-19 N=1.8 Rs=5)` | Red status LED (D_LED) | **Declared/APPROX.** Generic 1.8 V-class red LED. |

## Notes

- Vendor provenance was intentionally removed from `APPROX_2N7000` and
  `APPROX_1N34A`; calling them vendor models would overclaim. The verification
  `models` gate therefore reports SKIP (declared, not vendor).
- **K5 model artifact:** the TL082 macromodel draws far more supply current than
  the datasheet (~8.4 mA at 9 V and ~16.6 mA at 18 V vs ~2.8 mA real), which
  inflates the R1 drop and makes simulated headroom/VCC_F pessimistic. Use
  datasheet limits (S007) for headroom decisions.
- **Not a TL082 artifact:** the 18 V AC-gain drop is a clip-network threshold
  effect (M1 `Vgs = VREF - CLIP_A` crosses the 2N7000 `Vgs(th)`), confirmed by a
  VTO sweep (C042). It depends on the selected 2N7000; bench-verify.
- To replace an APPROX model: fetch a manufacturer model, record the URL, revision
  and SHA256 here, update the spec `models` entry with `vendor`/`part`/`source`,
  regenerate, and re-verify.

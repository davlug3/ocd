# Decision Record D002 — Supply range / TL082 feasibility (8–18V)

## Status
**Open (evidence improved, not closed)** — user confirmed 2026-11-09: **8–18V DC center-negative** (5V dropped). TL082 validated *by model-limited simulation* at 8/9/18V in a simplified gain stage (2026-11-09); **SLOS081O datasheet confirmation + full-topology/provenance SPICE/bench still required** before closing A1/D002.

## Reconciliation (2026-11-09)
- Prior 5–18V exploration identified TL082 5V risk (C011/C021). **5V support removed by explicit user decision** (S009/C022).
- Active requirement: **8–18V DC center-negative** (A1 revised).

## TL082 datasheet parametrics (opened source — verify against full SLOS081O tables/graphs)
TI TL082 product page (S007, opened 2026-11-09, https://www.ti.com/product/TL082): **min supply 7V**, max 30V; **input CM headroom to V− typ 3V**; **output swing headroom to V− typ 1.5V, to V+ typ -1.5V**; "In to V+", JFET input. Datasheet: **SLOS081O Rev O** (https://www.ti.com/lit/gpn/TL082). At 8V/Vref=4V this gives *typical* CM margin; swing/headroom are condition-dependent.

## Model-limited SPICE validation (2026-11-09, C024)
- **Artifact:** `circuit/exploration/d002_tl082_8v18v_validation.cir` + `.log`
- **Model:** TI `TL082.301` from SLOJ070 (S007), `circuit/models/TL082.301`, provenance in `circuit/models/PROVENANCE.md`. **Model header states +/-15V characterization; 8–18V single-supply use is extrapolative/model-limited.**
- **Config:** Vref=Vcc/2, DC-coupled non-inverting gain **~10.09x** (Rf=20k, Rg=2.2k to Vref), **Rload=100k**, 1kHz, 27C. Corrected after debug: dual-supply +/-15V sanity gave ~±504mV for 50mVpk in (expected); initial AC-coupled/unity-gain test-script bugs were discarded (not evidence).
- **Results (steady 2–12ms):**
  - DC bias: Vout ≈ Vref at 8/9/18V (e.g., 4.000V/4.500V/9.000V).
  - 50mVpk in (~1.009Vpp expected): **8V** 3.496–4.505V (1.009Vpp), **9V** 3.996–5.005V, **18V** 8.496–9.505V — linear.
  - 150mVpk in (~3.027Vpp expected): **8V** 2.488–5.514V (3.026Vpp), **9V** 2.988–6.014V, **18V** 7.488–10.514V — linear in this test.
  - 250mVpk in (~5.045Vpp expected): **8V** 1.621–6.380V (**4.759Vpp, limiting/clipping**), **9V** 1.980–7.024V (5.044Vpp), **18V** 6.480–11.524V (5.044Vpp).
  - High-gain spot (8V, Rf=100k, 10mVpk, ~46.5x): 3.900–4.101V (~0.202Vpp) — linear at that level.
- **Interpretation (cautious):** The model supports Vref-biased operation and linear gain at 8/9/18V into 100k for moderate swings; **8V has reduced headroom and clips earlier at large signal** (consistent with reduced rail margin). This is **favorable but not sufficient** evidence for A1.

## Historical 5V finding (superseded, retained for provenance)
At 5V/Vref=2.5V, TL082 CM/swing headroom (S007 typ parametrics) indicated high risk (C011). 5V dropped by spec change.

## Required next steps
1. Extract/confirm **SLOS081O** limits for 8V single-supply use (VICR/VOM vs supply/load/temperature, recommended conditions).
2. Run **full-topology, provenance-tracked SPICE** at 8/9/18V (real coupling, Drive settings, clipping network with documented models/assumptions, PSRR/ripple) under stated handoff conditions.
3. **Bench verification** at 8/9/18V (A1). Substitute op-amp only with datasheet/SPICE provenance and a recorded decision if A1 fails.

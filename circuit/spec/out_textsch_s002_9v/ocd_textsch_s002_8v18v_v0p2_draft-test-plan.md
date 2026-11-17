# ocd_textsch_s002_8v18v_v0p2_draft — Test and measurement plan

This plan defines bench evidence. Simulation results do not replace these measurements.

| ID | Requirement | Test point | Quantity | Method | Equipment | Conditions | Acceptance | Safety / notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M1 | A1 | TP_VCC | Supply voltage | DC voltmeter at barrel jack | DMM, adjustable DC supply | 8V, 9V, 18V, 25C, no signal | Within ±5% of set voltage, no oscillation | SELV DC only Verify reverse polarity protection if installed |
| M2 | A4 | TP_VREF | Vref bias voltage | DC voltmeter at VREF node | DMM | 8V, 9V, 18V supply, no signal, idle | Vref = Vcc/2 ± 2% across 8-18V | SELV DC only Vref loaded by feedback networks; measure under idle conditions |
| M3 | A1 | TP_GAIN1 | Gain stage 1 DC bias and swing | Oscilloscope at X1_OUT | Oscilloscope, function generator | 9V supply, 1kHz sine, 50mVpk input, Drive at 50% | DC bias near Vref, no clipping at moderate input levels | SELV DC only Verify linear operation before clipping threshold |
| M4 | A3 | TP_CLIP | Clipping threshold and symmetry | Oscilloscope at CLIP_A/CLIP_B, function generator, FFT | Oscilloscope with FFT, function generator | 9V supply, 1kHz sine, 50mVpk input, Drive at 50% | Asymmetric clipping: positive peak ~+5V, negative ~-3.5V relative to Vref | SELV DC only Compare against S002 voltage transfer curve (mosfet-1n34a-voltage-saturation-curve.png) |
| M5 | A1 | TP_OUT | Output swing and headroom | Oscilloscope at OUT, function generator | Oscilloscope, function generator | 8V, 9V, 18V supply, 1kHz sine, 50mVpk input, 100k load | No clipping distortion at unity gain; headroom increases with supply voltage | SELV DC only Verify 18V gives measurably more headroom than 9V |
| M6 | A5 | TP_TONE_W | Tone/HP-LP voicing sweep | Oscilloscope at TONE_W, function generator, FFT | Oscilloscope with FFT, function generator | 9V supply, 1kHz sine, 50mVpk input, Drive at 50%, Tone pot sweep, HP/LP toggle | HP position: more high-frequency content; LP position: flatter/darker response | SELV DC only Compare against S002 tone-stack frequency response (tone-stack.png) |

## Requirement traceability

- **R1:** 9V DC operation with Vref ~4.5V — measurements: not covered
- **R2:** Two TL082 gain stages + MOSFET/diode nonlinear stage (user-reported connections) — measurements: not covered
- **R3:** Adjustable gain and volume (simplified in sim) — measurements: not covered
- **A1:** Operate from 8-18V DC center-negative without damage — measurements: M1, M3, M5
- **A4:** Vref bias tracks Vcc/2 — measurements: M2
- **A3:** Asymmetric OCD-style clipping character with HP/LP voicing — measurements: M4
- **A5:** Controls function as specified — measurements: M6

## Execution record

Record actual measured values, instrument identifiers/calibration status, date, operator, deviations and pass/fail against the acceptance criteria before release.

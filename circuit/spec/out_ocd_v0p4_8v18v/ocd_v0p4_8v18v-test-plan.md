# ocd_v0p4_8v18v — Test and measurement plan

This plan defines bench evidence. Simulation results do not replace these measurements.

| ID | Requirement | Test point | Quantity | Method | Equipment | Conditions | Acceptance | Safety / notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M_E1 | E1 | VCC_JACK, VCC_F | DC voltage and reverse-polarity current | DMM at 8/9/18V; current-limited reverse-polarity test | bench supply, DMM | no signal, 25C, 100k load | VCC_F >= 7.0V at 8V jack; no damage; reverse polarity draws no current |  |
| M_E2 | E2 | VREF | DC voltage | DMM at 8/9/18V | DMM | no signal, 25C | VREF = VCC_F/2 +/-5% at 8/9/18V |  |
| M_E3 | E3 | X1_P, X1_OUT, X3_FB, X3_OUT | DC voltage | DMM/scope at 9V | DMM, oscilloscope | no signal, 25C | X1_OUT ~= X1_P; X3_OUT ~= X3_FB; neither at a rail |  |
| M_E4 | E4 | OUT | frequency response | sweep 20Hz-20kHz in LP and HP positions | audio analyzer or scope | Drive/Tone/Volume fixed; 50mVpk input | Repeatable LP/HP difference at 1kHz; no oscillation |  |
| M_E5 | E5 | LED_A | LED current and forward voltage | DMM at 8/9/18V | DMM | LED on, 25C | 1-5mA; LED on |  |
| M_E6 | E6 | VBAT, VCC_JACK | DC voltage and continuity | DMM with battery and DC plug; input jack inserted/removed | DMM, bench supply | battery only; DC plug in/out; input jack in/out | Battery disconnects with DC plug; no drain when input unplugged |  |
| M_E7 | E7 | IN, OUT | continuity/audio | true-bypass check | DMM, audio source | pedal off | Dry signal passes; circuit isolated when off |  |
| M_E8 | E8 | PCB mechanical | mechanical fit | test fit in 1590B; caliper check | 1590B enclosure, calipers | THT board, PCB-mounted jacks/3PDT | Fits 108 x 58mm; jacks/switch align (Phase C) |  |

## Requirement traceability

- **E1:** Operate from 8-18V DC center-negative at the jack with series reverse-polarity protection; the protected/filtered rail VCC_F must keep the TL082 within its 7-30V total-supply range. — measurements: M_E1
- **E2:** Vref = VCC_F/2 within +/-5% at 8/9/18V and stable under signal. — measurements: M_E2
- **E3:** Both TL082 stages have unity DC gain and no quiescent saturation. — measurements: M_E3
- **E4:** SW1 selects R14 only (LP, darker) or R14 in parallel with R15 (HP, brighter). — measurements: M_E4
- **E5:** Status LED with series resistor from VCC_F to GND, 1-5mA at 8-18V. — measurements: M_E5
- **E6:** 9V battery option with a switching DC jack and input-jack battery disconnect. — measurements: M_E6
- **E7:** True bypass with a 3PDT; dry signal passes when off. — measurements: M_E7
- **E8:** PCB-mounted 1/4-inch TS jacks and 3PDT; 1590B enclosure, 108 x 58mm board, through-hole (Phase C). — measurements: M_E8
- **A1:** Operate from 8-18V DC center-negative — measurements: not covered
- **A2:** True bypass — measurements: not covered
- **A3:** Asymmetric OCD-style clipping character with HP/LP voicing — measurements: not covered
- **A4:** Stable bias with no low-frequency instability (hum, motorboating, or oscillation) at 8/9/18V — measurements: not covered
- **A5:** Drive/Volume control range and output level — measurements: not covered
- **A6:** HP/LP voicing is selectable and audibly different — measurements: not covered

## Execution record

Record actual measured values, instrument identifiers/calibration status, date, operator, deviations and pass/fail against the acceptance criteria before release.

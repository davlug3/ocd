# Stage Budget — v0.1 (provisional, unverified)

## Conditions
| Field | Value |
|---|---|
| Bandwidth | 20 Hz – 20 kHz (target, unverified) |
| Source impedance | Guitar pickup + cable (high-Z, reactive; simplified as TBD for calc) |
| Load | >= 10 kΩ nominal assumption; verify at 100 kΩ / 1 MΩ (unverified) |
| Temperature | 25 °C assumed |
| Supply rails | Single DC 5–18V, Vref ≈ Vcc/2 (user req C002; 5V feasibility unverified C007) |

## Stages (topology-level; component values TBD after schematic lock D001)
| Stage | Gain (dB) | Input level | Output level | Headroom | Input Z | Output Z | Noise contribution | Bandwidth | Source |
|---|---|---|---|---|---|---|---|---|---|
| Input/coupling | ~0 | instrument (TBD) | TBD | TBD | ~330k target v1-style (unverified) | TBD | TBD | TBD | S2–S4, C003 |
| Gain stage 1 (TL082 non-inv, Drive) | variable, up to ~50+ dB potential (unverified) | TBD | limited by Vref/rails | **critical at 5V** | high (op-amp) | low-mid | op-amp + resistors (TBD) | set by feedback caps (TBD) | S2,S3,C003,C007 |
| Clipping (2N7000+1N34A to Vref) | loss/limiting (nonlinear) | TBD | clipped around Vref | set by thresholds + Vref | via series R (TBD) | TBD | N/A (distortion mechanism) | cap-dependent (TBD) | S1–S3,C003,C004 |
| Gain stage 2 (TL082) | fixed/modest (TBD) | clipped | TBD | rail-limited | TBD | buffered-ish | TBD | TBD | S2,S3 |
| Tone (passive) + HP/LP + Volume | attenuation | TBD | user-set | N/A | load-dependent | load-dependent | minimal (passive) | voicing-dependent | S2–S4 |
| True bypass path | 0 | instrument | instrument | N/A | direct | direct | wiring only | cable-dependent | C002 |

## Totals
| Quantity | Value | Limit | Margin | Source |
|---|---|---|---|---|
| Total gain | TBD | TBD | TBD | unverified |
| Input-referred noise | TBD | TBD | TBD | unverified |
| Headroom | TBD; worst at 5V | must pass A1 | unknown | C002,C007 |
| Bandwidth | TBD | 20 Hz–20 kHz target | TBD | unverified |
| THD budget | intentional overdrive (not hi-fi) | characterize, not minimize | N/A | AGENTS.md |
| Power per rail | TBD | supply-dependent | TBD | unverified |

## Notes
- Values become meaningful only after D001 locks a schematic and D002 resolves 5V feasibility.
- Vref divider example (ideal): 100k/100k at 9V → 4.5V, Thevenin ~50k (`circuit_calc.py divider`, verified locally 2026-11-09). Actual divider values TBD per locked schematic.

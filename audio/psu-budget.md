# Power Supply Budget — v0.1 (provisional)

## Rails
| Rail | Nominal | Tolerance | Max load current | Quiescent current | Ripple limit | Source |
|---|---|---|---|---|---|---|
| Vcc (single) | 8–18V DC (user, reconciled 2026-11-09) | TBD (adapter dependent) | TBD | TBD (TL082 + any LED/buffer) | TBD | C022 |
| Vref (derived) | Vcc/2 | TBD (divider tolerance) | bias only | n/a | must be well filtered | S2,C003 |

## Source and rectification
| Item | Value | Conditions / source |
|---|---|---|
| Input | External DC adapter or 9V battery (optional) | C002; battery at 5V not typical |
| Reverse polarity protection | TBD (recommended) | Q4 |
| Filtering | Bulk + small HF cap (topology TBD) | S2 |

## Regulation
No onboard regulator assumed in reference topology; circuit runs from Vcc with Vref divider. Re-evaluate if D002 selects rail conditioning.

## Grounding and safety
| Item | Value | Conditions / source |
|---|---|---|
| Domain | SELV DC only, no mains | C002 |
| True bypass | Mechanical path; ground/jack wiring must avoid hum/ground loops | Q5 |
| Enclosure | Metal enclosure typical; bonding/shielding strategy TBD | intake "anything" |

## Notes
- 5V adapters vary in regulation/noise; test with representative supplies.
- No mains safety review required for SELV DC pedal, but polarity/reverse/overvoltage protection should be considered (Q4).

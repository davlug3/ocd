# Hybrid labeled value/conflict table — v0.3 DRAFT (confirmed for generation)

**Confirmed:** 2026-11-09, `next: 2`, `clipping: provisional S002 text`, `values: hybrid labeled`, `models: existing TL082.301 + APPROX discretes simulation-only` (user: "yes").
**Status:** Working draft for `circuit-design-skill` spec generation. **Not a verified Fulltone/OCD netlist. Do not fabricate.**
**Anchors:** S002 (opened 2026-11-09), S003 (opened 2026-11-09); cross-check context S001 (OCD v2, cataloged), S013 (cataloged).
**Locked:** 8–18V DC center-negative, true bypass, v1.4/v1.7-style reference, substitutions with provenance (C022). D002 directionally favorable but open (C024).
**Clipping conflict:** S002 text topology assumed provisionally; 2026 S002 comment reports different M1/M2 wiring. **M1/M2/D_ASYM node orientation in generated spec is PROVISIONAL and must be verified before fabrication.**

## Working values (simulatable draft)
| Block | Ref | Value/part | Provenance | Status |
|---|---|---|---|---|
| VCC | V1 | 9V nominal test source (spec supports 8–18V) | C022 | test condition |
| Vref | R_V1,R_V2,C_VREF | 100k,100k,10u | C008 method; S002 concept | proposed |
| Input | C_IN,R_INREF,R_IN_BIAS | 22n,1M,1M | S002/S003 roles | provisional |
| Gain 1 | U1A,R_G1,R_G1F,RV_DRIVE,C_G1HF | TL082,2.2k,18k,1M,220p | S003 explicit gain formula; others proposed | provisional |
| Clip series | R_CLIP,C_CLIP_HF | 10k,100n (placeholder) | S002 role; values TBD | TBD/proposed |
| Clipping | Q1,Q2,D_ASYM | APPROX_2N7000 x2, APPROX_BAT46 default (D3 option) | D003/C022; wiring PROVISIONAL | unverified |
| Gain 2 | U1B,R_G2A,R_G2B | TL082,10k,39k (~4.9x, placeholder) | role per S002/S003; values TBD | proposed |
| Tone/HP-LP | RV_TONE,C_TONE,R_HP,R_LP,SW_HP | 10k,47n,10k,22k,SPDT (simplified placeholders) | S002 roles; implementation simplified | TBD/proposed |
| Volume/out | C_OUT,RV_VOL | 1u,100k | proposed | TBD/proposed |
| Load | R_LOAD | 100k | handoff condition | condition |
| Bypass | SW_BYP | noted, not in SPICE core path | C022 | external |

All unverified. Simulation uses TL082.301 + APPROX discretes (simulation-only).

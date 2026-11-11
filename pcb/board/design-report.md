# ocd_v0p4_8v18v rev v0.4

**Status: PROFESSIONAL - RELEASE GATES PASSED**

- Profile: `2layer-low-speed` (full)
- Backend: `local` (ci)
- Failures: none
- Required human sign-off: none
- Completed sign-off: none

## Automated gates

| Gate | Result |
|---|---|
| spec | {"errors": 0, "ok": true, "warnings": 8} |
| structural | 0 |
| drc | 0 |
| unconnected | 0 |
| dfm | 0 |
| netlist_parity | 0 |
| stackup | 0 |
| impedance | 0 |
| length_match | 0 |
| fab | 0 |
| thermal | reported |
| emc | not_verified |

## DRC

- Errors: 0
- Unconnected: 0
- Report: `build/pcb/check/ocd_v0p4_8v18v.drc.rpt`

## Routing quality metrics

- Track copper length: 1270.673 mm
- Track segments: 261
- Vias: 2
- Via layer-transition locations: 2
- Unconnected items: 0
- Clearance violations: 0
- Metrics JSON: `build/pcb/route-metrics.json`

These are routing measurements, not electrical, thermal, SI/PI, EMC, or safety sign-off.

## Routed lengths

- BAT_NEG: 25.658 mm
- BAT_POS: 24.942 mm
- CLIP_A: 87.389 mm
- CLIP_B: 10.194 mm
- GND: 191.579 mm
- IN: 19.293 mm
- IN_B: 59.49 mm
- J_IN_TIP: 39.455 mm
- J_OUT_TIP: 53.509 mm
- LED_A: 49.937 mm
- M2_D1_NODE: 28.522 mm
- OUT: 20.257 mm
- SW1_1: 9.458 mm
- TONE_TOP: 51.956 mm
- TONE_W: 12.857 mm
- VCC: 5.908 mm
- VCC_F: 97.347 mm
- VCC_JACK: 7.696 mm
- VOL_TOP: 23.543 mm
- VREF: 105.9 mm
- X1_FB: 99.83 mm
- X1_OUT: 68.349 mm
- X1_P: 33.77 mm
- X1_RG: 6.658 mm
- X2_W: 8.578 mm
- X3_FB: 47.008 mm
- X3_OUT: 62.668 mm
- X3_RG: 18.922 mm

## Warnings

- `components.ref_format` reference 'D_PWR' does not look like a standard designator
- `components.ref_format` reference 'R_LED' does not look like a standard designator
- `components.ref_format` reference 'D_LED' does not look like a standard designator
- `components.ref_format` reference 'J_IN' does not look like a standard designator
- `components.ref_format` reference 'J_OUT' does not look like a standard designator
- `components.ref_format` reference 'J_PWR' does not look like a standard designator
- `components.ref_format` reference 'SW_FS' does not look like a standard designator
- `components.ref_format` reference 'SW_HP' does not look like a standard designator

## Assumptions

- X1A and X3A are two sections of one TL082 dual op-amp; they are merged into a single DIP-8 U1 on the board.
- The Drive, Tone and Volume pots replace the fixed simulation resistors R_X2POT, R_X4 and R_VOL5A/B; the SPICE netlist remains the electrical source of truth.
- The 3PDT and HP/LP toggle are panel-mounted and wired to headers; a PCB-mounted 3PDT footprint needs a verified switch datasheet.
- The input jack is a TRS part used as mono: the ring carries the battery negative and completes it only when a mono plug is inserted.
- The DC jack is center-negative; its normally-closed switch (pads 2-3) disconnects the battery when a DC plug is inserted.
- Mechanical placement relative to the 1590B enclosure drilling is a follow-up; this board is electrically routed but not yet panel-fitted.
- The PCB overlay is generated from the circuit spec; the SPICE netlist is the electrical source of truth.
- Logical SPICE pin numbers are not physical footprint pads; pin maps must come from the real package datasheet.
- The pcb-design-skill DRC, DFM and unconnected gates, not this handoff, decide whether the board is manufacturable.
- Ideal switches and simulation sources are excluded from the board.

## Fabrication package

- Archive: `build/pcb/fab/ocd_v0p4_8v18v-fabrication.zip`
- Gerbers: `build/pcb/fab/gerbers`
- Drill: `build/pcb/fab/drill`
- Position: `build/pcb/fab/ocd_v0p4_8v18v-pos.csv`
- STEP: `build/pcb/fab/ocd_v0p4_8v18v.step`
- IPC-D-356: `build/pcb/fab/ocd_v0p4_8v18v-ipc356.net`
- Required outputs: drill, gerbers, ipc356, pos, step

---

A professional claim means the automated gates listed in this report passed and the required human sign-offs are recorded. It does not certify performance that the pipeline cannot measure (RF, EMC, thermal, safety, flex fatigue).

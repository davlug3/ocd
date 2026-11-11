# Phase C — OCD v0.4 PCB (1590B, through-hole)

Electrical source of truth: `circuit/spec/out_ocd_v0p4_8v18v/ocd_v0p4_8v18v.cir`
(copied to `pcb/handoff/ocd_v0p4_8v18v.cir`). The PCB overlay adds board
mechanics, footprints and pin maps; it does not change the schematic.

> **Status: routed, release gates passed (prototype).** The `pcb-design-skill`
> CI pipeline built, routed and checked the board: DRC 0, unconnected 0,
> DFM 0, netlist parity 0 and fab 0 (run 43059805373). See
> `pcb/board/design-report.md`. It is **not** panel-fitted to a specific
> 1590B drilling; that remains the main open mechanical item.

## Board

| Item | Value |
|---|---|
| Size | 108 × 58 mm |
| Layers / thickness / copper | 2 / 1.6 mm / 1 oz |
| Material / finish | FR4 / HASL-LF |
| Assembly | Through-hole (THT) |
| Profile | `2layer-low-speed` |
| Mounting | 4 × M3 non-plated holes, 3.2 mm, at (7,7), (101,7), (7,51), (101,51) mm |

## What is on the board

46 placed parts: 42 electrical + 4 mounting holes.

- **Core circuit:** R1–R15, C1–C11, D1, D_PWR, D_LED, R_LED, M1, M2
  (the SPICE netlist decides connectivity).
- **U1 (DIP-8):** one TL082 package. The SPICE sections `X1A` and `X3A` are
  merged here; they are excluded from the LTspice import.
- **X2 / X4 / X5:** Drive, Tone and Volume pots. They replace the fixed
  simulation placeholders `R_X2POT`, `R_X4`, `R_VOL5A/B`, which are excluded.
- **J_IN / J_OUT:** PCB-mounted 1/4" jacks (Neutrik NMJ6HFD2 stereo in,
  NMJ4HFD2 mono out).
- **J_PWR:** 9 V DC jack, center-negative, switched (CUI/Same Sky PJ-102AH).
- **BT1:** 2-pin header for an off-board 9 V battery snap.
- **SW_FS:** 2×05 header for a panel-mounted 3PDT true-bypass switch.
- **SW_HP:** 1×03 header for the panel-mounted HP/LP toggle.

## Footprint verification

Footprint names and pad numbers were read from the official KiCad library
(S019) and cross-checked against the part datasheets (S007, S008, S016–S018).
They were **not** previewed in the KiCad footprint picker locally because the
Termux environment has no KiCad; the CI build resolves the installed KiCad 9
library and is the compatibility gate. A missing or renamed footprint will
fail the CI build rather than be silently substituted.

## Pin maps that matter

| Part | Footprint | Map | Evidence |
|---|---|---|---|
| M1, M2 (2N7000) | `Package_TO_SOT_THT:TO-92_Inline` | `d=3, g=2, s=1, b=1` | S008 (onsemi NDS7002A): TO-92 1=S, 2=G, 3=D |
| D_PWR, D1, D_LED | KiCad `Diode_THT` / `LED_THT` | anode→pad 2, cathode→pad 1 | S019: KiCad `Device:D`/`LED` pin 1=K, 2=A |
| U1 (TL082) | `Package_DIP:DIP-8_W7.62mm` | 1=X1_OUT, 2=X1_FB, 3=X1_P, 4=GND, 5=CLIP_B, 6=X3_FB, 7=X3_OUT, 8=VCC_F | S007 TL082 DIP-8 pinout |
| X2 (Drive, 1 M) | Alpha RD901F vertical | 1=X1_OUT, 2=X2_W, 3=X2_W | S017 + build check |
| X4 (Tone, 10 k) | Alpha RD901F vertical | 1=TONE_TOP, 2=TONE_W, 3=TONE_W | S002/S017 + build check |
| X5 (Volume, 100 k) | Alpha RD901F vertical | 1=GND, 2=OUT, 3=VOL_TOP | S017 + build check |
| J_IN | Neutrik NMJ6HFD2 | T=J_IN_TIP, S=GND, R=BAT_NEG | S018/S019 |
| J_OUT | Neutrik NMJ4HFD2 | T=J_OUT_TIP, S=GND | S018/S019 |
| J_PWR | PJ-102AH | 1=GND (center), 2=VCC_JACK (sleeve), 3=BAT_POS (switch) | S016 |
| BT1 | 1×02 header | 1=BAT_POS, 2=BAT_NEG | project wiring |
| SW_HP | 1×03 header | 1=SW1_1, 2=VOL_TOP | S002 |

### Pot wiring

The pots are wired as **rheostats**: the unused end is tied to the wiper.

- **Drive:** CW increases the resistance from `X1_OUT` to `X2_W` → more gain.
- **Tone:** CW increases the resistance from `TONE_TOP` to `TONE_W` → brighter.
- **Volume:** CW moves the wiper from `GND` toward `VOL_TOP` → louder.

`S017` confirms pins 1 and 3 are the fixed ends and pin 2 is the wiper, but the
extracted datasheet text does **not** say which end is CW. The board assumes
**pin 1 = CCW, pin 3 = CW**; confirm on the built hardware (C046).

### 3PDT true bypass (SW_FS)

Wire header pin *n* to 3PDT pin *n* 1:1:

| Header | 3PDT pin | Net | Role |
|---|---|---|---|
| 1 | 1 | `J_IN_TIP` | pole 1 throw |
| 2 | 2 | `IN` | pole 1 common → effect input |
| 3 | 3 | `J_OUT_TIP` | pole 1 throw → bypass |
| 4 | 4 | `J_OUT_TIP` | pole 2 throw → effect output |
| 5 | 5 | `OUT` | pole 2 common |
| 6 | 6 | `GND` | pole 2 throw → mute effect output in bypass |
| 7 | 7 | *(open)* | pole 3 throw |
| 8 | 8 | `LED_A` | pole 3 common |
| 9 | 9 | `GND` | pole 3 throw → LED off in bypass |

The LED is **always on** in the electrical model (D_LED from `LED_A` to `GND`).
On the board, 3PDT pole 3 shorts `LED_A` to `GND` in the bypass position, so
the physical LED is on only when the effect is engaged. This is a board-level
deviation from the simulation, not a schematic change. If the switch throws
are reversed, swap header pins 1↔3, 4↔6 or 7↔9 as needed.

### Battery and DC jack

- **DC present:** center pin (pad 1) = `GND`, sleeve (pad 2) = `VCC_JACK`.
  The normally-closed switch (pads 2–3) opens, disconnecting `BAT_POS`.
- **No DC:** pads 2–3 are closed, so `BAT_POS` feeds `VCC_JACK` through the
  same reverse-polarity diode path.
- **Battery negative:** returns through the input jack ring `R` (`BAT_NEG`).
  A mono TS plug shorts the ring to the plug sleeve, completing the battery
  circuit only while a cable is inserted.
- **Polarity:** center-negative, as required by the v0.4 circuit spec.

This relies on the PJ-102AH switch being closed between pads 2–3 with no plug
(S016, distributor description). Bench-check the actual jack before trusting
the battery/DC handover (C045).

## Deviations and open items

1. **Mechanical fit is not closed.** U1, the three pots, the two jacks and the
   four mounting holes are anchored; the DC jack, headers, battery header and
   small parts are auto-placed. The jack noses now sit at the side edges: the
   placement engine was fixed to use each footprint's real bounding-box offset
   (`pcb-design-skill` commit `8f60198`) and to use the text-free mechanical
   bounding box instead of the text-inflated one (`dca3320`, with the F.CrtYd
   courtyard as fallback). The two jacks are at
   different heights (input `y=25`, output `y=33`) to clear the corner mounting
   holes; pot/jack/3PDT heights, panel hole positions and knob clearance still
   need a mechanical drawing and a panel-fit check.
2. **3PDT is panel-mounted.** No verified KiCad 3PDT footprint was found; the
   board exposes a 2×05 header instead.
3. **Pot CW/CCW end assignment** is assumed (C046).
4. **Pot values/tapers** (X2 1 M, X5 100 k) remain unverified from S002 (K7).
5. **D1/M1/M2 are still approximation models** in simulation; the board uses
   real 1N34A/2N7000 packages, but bench behavior must be confirmed (K2).
6. **No performance claim.** Routing/DRC/DFM say the copper is manufacturable
   at the stated rules; they do not certify the audio performance.

## Pipeline notes

- Placement uses a 0.8 mm courtyard-to-courtyard clearance and a 1.27 mm
  search grid. The board is dense enough that 1.0 mm left no room for C9;
  0.8 mm is still well above the 0.2 mm routing clearance.
- Freerouting can emit neckdown tracks below the netclass minimum (observed
  0.1874 mm against 0.2 mm). The route stage clamps SES widths to
  `rules.min_track_width_mm` before import, so the DRC gate sees the board's
  declared minimum.
- The GND zone on B.Cu uses solid pad connections. Thermal relief left SW_FS
  pad 6 starved (one spoke) and pad 9 unconnected; solid connections remove
  that failure mode on a low-power pedal board. Isolated zone islands are
  removed by the fill.
- GND is poured on both layers. A B.Cu-only pour left an isolated island
  around U1/SW_FS that KiCad reported as unconnected; the F.Cu pour stitches
  the layers through the through-hole GND pads. The Specctra export drops the
  pours so Freerouting routes GND as a normal net; the pours are re-added and
  filled after the SES import, and the router's GND vias stitch the layers.
  The Specctra boundary is inset by the edge clearance plus 0.1 mm so the
  router cannot lay copper flush to the board edge.
- A post-placement pass keeps the fixed-part reference text inside the board
  silk margin and pushes overlapping references apart. Placement itself
  ignores text, so edge parts can otherwise clip their reference. Auto-placed
  passives have their silk reference hidden; the reference stays on F.Fab and
  in the position file.
- The connectors, headers, pots, op-amp and mounting holes are marked
  `board_only` because they are not in the SPICE netlist. That is what the
  structural checker's "pad has no net; confirm it is mechanical" warning is
  about.

## Regenerate

```bash
cd /data/data/com.termux/files/home/ocd

# 1) validate the circuit spec (includes the pcb block)
python3 ~/.agents/skills/circuit-design-skill/scripts/design_spec.py \
  validate circuit/spec/ocd_v0p4_8v18v.json

# 2) regenerate the PCB handoff
python3 ~/.agents/skills/circuit-design-skill/scripts/pcb_handoff.py \
  circuit/spec/ocd_v0p4_8v18v.json --out pcb/handoff

# 3) run the PCB pipeline (needs KiCad 9 + Java + Freerouting;
#    the local Termux environment does not have them, so use CI)
python3 ~/.agents/skills/pcb-design-skill/scripts/design_pipeline.py all \
  pcb/handoff/ocd_v0p4_8v18v-pcb.json \
  --ltspice pcb/handoff/ocd_v0p4_8v18v.cir \
  --pin-map pcb/handoff/ocd_v0p4_8v18v-pinmap.json \
  --node-aliases pcb/handoff/ocd_v0p4_8v18v-node-aliases.json \
  --no-ask
```

The CI path used here stages the same files under
`specs/ocd-v0p4/` on the `davlug3/pcb-design-skill` branch `ocd-v0p4` and
dispatches the `Design pipeline` workflow.

## Previews

- `pcb/preview/ocd_v0p4_8v18v_top.png` / `.svg` and `..._bottom.png` / `.svg`:
  quick top/bottom views of the routed board (copper, pads, silkscreen,
  outline). Generated locally from the `.kicad_pcb`; see `pcb/preview/README.md`.
- `circuit/preview/ocd_v0p4_8v18v.svg` / `.png`: v0.4 schematic preview from
  the generated `.kicad_sch` (symbol grid + global labels, no wires). See
  `circuit/preview/README.md`.
- `pcb/board/fab/ocd_v0p4_8v18v.step`: 3D STEP model for a mechanical viewer.
- Gerbers in `pcb/board/fab/gerbers/` open in any Gerber viewer.

## Evidence

- `pcb/board/`: tracked release copy — `ocd_v0p4_8v18v.kicad_pcb`,
  `.kicad_pro`, Gerbers, drill, position file, STEP, IPC-D-356,
  `ocd_v0p4_8v18v-fabrication.zip`, DRC report, route metrics and
  `design-report.md` from CI run 43059805373.
- Gate summary: 46 footprints, 29 nets, 261 track segments, 2 vias, 2 GND
  zones, 1270.7 mm total track length, 0 DRC violations, 0 unconnected,
  0 DFM failures, clean netlist parity.
- `catalog/sources.json`: S016 (PJ-102AH), S017 (Alpha RD901F), S018 (Neutrik
  jacks), S019 (KiCad footprints); S007/S008 for the TL082/2N7000.
- `evidence/claims.jsonl`: C043–C048.
- `pcb/handoff/ocd_v0p4_8v18v-pcb-handoff.md`: generated handoff and warnings.
- `pcb/build/`: transient CI download (gitignored); `pcb/board/` is the
  tracked release copy.

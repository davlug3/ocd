# Board previews — OCD v0.4

These images are generated from the routed board
`pcb/board/ocd_v0p4_8v18v.kicad_pcb` for quick visual inspection on a phone or
laptop. They are **not** manufacturing drawings.

| File | View |
|---|---|
| `ocd_v0p4_8v18v_top.png` / `.svg` | Top copper, through-hole pads, silkscreen, outline |
| `ocd_v0p4_8v18v_bottom.png` / `.svg` | Bottom copper, pads, silkscreen (X-mirrored as seen from below) |

## Regenerate

```bash
python3 pcb/preview/render_board.py \
  --board pcb/board/ocd_v0p4_8v18v.kicad_pcb \
  --out-dir pcb/preview
```

Optional: `--scale 20` for a larger PNG, `--prefix NAME`.

## What it draws

- `Edge.Cuts` outline and the 108 × 58 mm board rectangle.
- `F.Cu` / `B.Cu` track segments and vias.
- Through-hole and SMD pads with drills.
- Footprint silkscreen (`F.SilkS` / `B.SilkS`) and reference labels.
- GND zones as a translucent copper underlay.

## Caveats

- **Preview only.** The authoritative geometry is the Gerber set and the DRC
  report in `pcb/board/`; this renderer does not run DRC or check clearances.
- Zone fills are drawn as filled polygons from `filled_polygon`; keepouts and
  thermal spokes are not modelled.
- The renderer is a local fallback for hosts without KiCad, Freerouting or an
  SVG rasteriser. It is not a replacement for `kicad-cli pcb render` or a
  Gerber viewer.
- Use the `.svg` files when zooming: the PNG is a fixed-resolution raster.
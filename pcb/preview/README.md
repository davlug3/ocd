# Board previews — OCD v0.4

These images are generated from the routed board
`pcb/board/ocd_v0p4_8v18v.kicad_pcb` for quick visual inspection on a phone or
laptop. They are **not** manufacturing drawings.

| File | View |
|---|---|
| `ocd_v0p4_8v18v_top.png` / `.svg` | Top copper, through-hole pads, silkscreen, outline |
| `ocd_v0p4_8v18v_bottom.png` / `.svg` | Bottom copper, pads, silkscreen (X-mirrored as seen from below) |
| `ocd_v0p4_8v18v-3d-top.png` / `-3d-bottom.png` | Raytraced 3D renders from KiCad 9 |
| `ocd_v0p4_8v18v.glb` | Binary glTF of the full assembly (42 parts) |
| `ocd_v0p4_8v18v-components.step` | STEP including component bodies |
| `viewer.html` | Self-contained interactive 3D viewer (open directly) |

## 3D preview

Open `viewer.html` in a browser (double-click, or `termux-open viewer.html`).
It embeds the GLB as a base64 data URI so it works from `file://`; the
model-viewer runtime is loaded from a CDN, so the first open needs network
access.

The GLB contains the board and all 42 electrical parts. The four M3 mounting
holes are holes in the board, so they have no 3D node. The official KiCad
library has no model for the Neutrik switched jacks, CUI PJ-102AH jack or Alpha
RD901F pot; the preview substitutes the closest official models (CUI PJ-063AH
jack and Bourns 3266W pot) so the part envelopes still show. Substitutions are
visual only and are not manufacturer geometry.

## Regenerate

### 2D board previews

```bash
python3 pcb/preview/render_board.py \
  --board pcb/board/ocd_v0p4_8v18v.kicad_pcb \
  --out-dir pcb/preview
```

Optional: `--scale 20` for a larger PNG, `--prefix NAME`.

### 3D previews

The local Termux host has no KiCad. The 3D export runs in the
`kicad/kicad:9.0` container via the `3D preview` GitHub Actions workflow:

```bash
gh workflow run preview-3d.yml --ref main
gh run watch <run-id>
gh run download <run-id> -n ocd-3d-preview -D /tmp/ocd-3d
cp /tmp/ocd-3d/* pcb/preview/
python3 pcb/preview/make_viewer.py \
  --glb pcb/preview/ocd_v0p4_8v18v.glb \
  --out pcb/preview/viewer.html
```

`build_3d.py` downloads only the 15 models the board references, substitutes
the four missing ones, and exports GLB, component STEP and raytraced stills.

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
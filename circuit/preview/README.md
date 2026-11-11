# Schematic previews — OCD v0.4

| File | Content |
|---|---|
| `ocd_v0p4_8v18v.svg` / `.png` | v0.4 schematic rendered from `circuit/spec/out_ocd_v0p4_8v18v/ocd_v0p4_8v18v.kicad_sch` |

## What this is

The circuit-design-skill generator emits a deterministic **symbol grid**: every
part is a placed symbol with absolute `Reference`/`Value` properties, and each
pin is tied to a global label. It does **not** emit wire segments. The preview
draws exactly that: symbols, pin stubs, reference/value text and global net
labels.

That is why the image is tall and sparse rather than a hand-drawn schematic.
It is faithful to the `.kicad_sch`; it is not a re-layout.

## Regenerate

```bash
python3 circuit/preview/render_schematic.py \
  --sch circuit/spec/out_ocd_v0p4_8v18v/ocd_v0p4_8v18v.kicad_sch \
  --out-dir circuit/preview
```

Optional: `--scale 12` for a larger PNG.

## Related files

- `circuit/spec/out_textsch_s002_9v/ocd_textsch_s002_8v18v_v0p2_draft.png` /
  `.svg`: an **older v0.2 text-schematic draft** (39 symbols). Superseded by
  the v0.4 render here; kept for history.
- `circuit/spec/out_ocd_v0p4_8v18v/ocd_v0p4_8v18v.kicad_sch`: the source file.
- `circuit/spec/out_ocd_v0p4_8v18v/ocd_v0p4_8v18v.cir`: the SPICE netlist used
  for simulation.

## Caveats

- **Preview only.** It does not replace `kicad-cli sch export` or an ERC run;
  it does not prove connectivity beyond what the global labels encode.
- The generated schematic has no wire geometry, so the preview intentionally
  shows pin stubs and labels rather than routed wires.
- The authoritative electrical source of truth is the `.cir` netlist plus
  `verify.py` results, not this image.
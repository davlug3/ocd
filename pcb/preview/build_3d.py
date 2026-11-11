#!/usr/bin/env python3
"""Build a 3D preview (GLB + optional STEP/PNG) from the routed KiCad board.

The board's footprints reference KiCad's official 3D model library through
``${KICAD9_3DMODEL_DIR}``. The KiCad Docker image does not ship that library
(it is multi-gigabyte), so this script downloads only the models the board
needs, then runs ``kicad-cli`` to export:

* ``<name>.glb``  — binary glTF for an interactive browser viewer
* ``<name>-components.step`` — STEP including component bodies
* ``<name>-3d-top.png`` / ``-3d-bottom.png`` — raytraced stills (best effort)

Missing models are reported and skipped; KiCad will omit those components from
the 3D output. This is a preview tool, not a fabrication output.

Usage (inside the KiCad 9 container):
    python3 pcb/preview/build_3d.py \
        --board pcb/board/ocd_v0p4_8v18v.kicad_pcb \
        --out-dir pcb/preview
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

GITHUB_RAW = "https://raw.githubusercontent.com/KiCad/kicad-packages3D/master"
MODEL_RE = re.compile(r'\(model "\$\{KICAD9_3DMODEL_DIR\}/([^"]+)"')

# The official library has no model for a few of the selected footprints
# (Neutrik switched jacks, CUI PJ-102AH, Alpha RD901F 9 mm pot). Substitute
# simple VRML stand-ins so the 3D preview shows the part envelope instead of
# omitting the component. These are previews, not manufacturer geometry.
def _mesh(points: list[tuple[float, float, float]],
          triangles: list[tuple[int, int, int]],
          color: str = "0.10 0.10 0.11") -> str:
    """Minimal VRML2 IndexedFaceSet mesh in the structure KiCad emits."""
    pts = ",\n".join(f"{x:.4f} {y:.4f} {z:.4f}" for x, y, z in points)
    idx = ",\n".join(f"{a}, {b}, {c}, -1" for a, b, c in triangles)
    return f"""#VRML V2.0 utf8
Shape {{
  appearance Appearance {{ material DEF MAT Material {{
    ambientIntensity 0.2
    diffuseColor {color}
    specularColor 0.25 0.25 0.25
    emissiveColor 0.0 0.0 0.0
    transparency 0.0
    shininess 0.35
  }} }}
}}
Shape {{
  geometry IndexedFaceSet {{
    creaseAngle 0.50
    coordIndex [
      {idx}
    ]
    coord Coordinate {{ point [
      {pts}
    ] }}
  }}
  appearance Appearance {{ material USE MAT }}
}}
"""


def _box(x: float, y: float, z: float, sx: float, sy: float, sz: float) -> str:
    x0, x1 = x - sx / 2, x + sx / 2
    y0, y1 = y - sy / 2, y + sy / 2
    z0, z1 = z - sz / 2, z + sz / 2
    pts = [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
    ]
    tris = [
        (0, 2, 1), (0, 3, 2),
        (4, 5, 6), (4, 6, 7),
        (0, 1, 5), (0, 5, 4),
        (1, 2, 6), (1, 6, 5),
        (2, 3, 7), (2, 7, 6),
        (3, 0, 4), (3, 4, 7),
    ]
    return _mesh(pts, tris)


def _cylinder(x: float, y: float, z0: float, z1: float, r: float,
              segments: int = 16) -> str:
    import math

    pts: list[tuple[float, float, float]] = []
    for z in (z0, z1):
        for i in range(segments):
            a = 2 * math.pi * i / segments
            pts.append((x + r * math.cos(a), y + r * math.sin(a), z))
    cb = len(pts)
    pts.append((x, y, z0))
    ct = len(pts)
    pts.append((x, y, z1))

    tris: list[tuple[int, int, int]] = []
    for i in range(segments):
        j = (i + 1) % segments
        b0, b1 = i, j
        t0, t1 = segments + i, segments + j
        tris.append((b0, b1, t1))
        tris.append((b0, t1, t0))
        tris.append((cb, b1, b0))
        tris.append((ct, t0, t1))
    return _mesh(pts, tris, "0.55 0.55 0.58")


def _pot(x: float, y: float) -> str:
    return _box(x, y, 3.0, 9.0, 9.0, 6.0) + _cylinder(x, y, 6.0, 16.0, 3.0)


SUBSTITUTES: dict[str, str] = {
    "Connector_Audio.3dshapes/Jack_6.35mm_Neutrik_NMJ4HFD2_Horizontal.step":
        _box(6.35, 8.1, 6.0, 14.0, 16.0, 12.0),
    "Connector_Audio.3dshapes/Jack_6.35mm_Neutrik_NMJ6HFD2_Horizontal.step":
        _box(6.35, 8.1, 6.0, 14.0, 16.0, 12.0),
    "Connector_BarrelJack.3dshapes/BarrelJack_CUI_PJ-102AH_Horizontal.step":
        _box(2.35, 3.0, 5.5, 9.0, 11.0, 11.0),
    "Potentiometer_THT.3dshapes/Potentiometer_Alpha_RD901F-40-00D_Single_Vertical.step":
        _pot(3.75, 2.5),
}


def download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return True
    req = urllib.request.Request(url, headers={"User-Agent": "ocd-preview/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
            shutil.copyfileobj(r, f)
        return True
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
        print(f"  ! {dest.relative_to(dest.parents[2]) if len(dest.parents) > 2 else dest}: {exc}")
        if dest.exists():
            dest.unlink()
        return False


def run(cmd: list[str]) -> int:
    print("+", " ".join(cmd))
    try:
        return subprocess.call(cmd)
    except OSError as exc:
        print(f"  ! cannot run {cmd[0]}: {exc}")
        return 127


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--board", required=True, type=Path)
    ap.add_argument("--out-dir", default=Path("pcb/preview"), type=Path)
    ap.add_argument("--models-dir", default=None, type=Path)
    ap.add_argument("--kicad-cli", default="kicad-cli")
    ap.add_argument("--skip-render", action="store_true")
    args = ap.parse_args()

    board = args.board.resolve()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    models_dir = (args.models_dir or (out_dir / "models")).resolve()
    models_dir.mkdir(parents=True, exist_ok=True)

    text = board.read_text()
    rels = sorted(set(MODEL_RE.findall(text)))
    print(f"board: {board}")
    print(f"models needed: {len(rels)}")

    missing: list[str] = []
    replacements: dict[str, str] = {}
    for rel in rels:
        dest = models_dir / rel
        ok = download(f"{GITHUB_RAW}/{rel}", dest)
        if not ok and rel in SUBSTITUTES:
            wrl_rel = rel[:-5] + ".wrl" if rel.endswith(".step") else rel + ".wrl"
            wrl_path = models_dir / wrl_rel
            wrl_path.parent.mkdir(parents=True, exist_ok=True)
            wrl_path.write_text(SUBSTITUTES[rel])
            replacements[rel] = wrl_rel
            print(f"  SUB {rel} -> {wrl_rel}")
            continue
        print(f"  {'ok ' if ok else 'MISS'} {rel}")
        if not ok:
            missing.append(rel)

    cli = shutil.which(args.kicad_cli)
    if not cli:
        print(f"! {args.kicad_cli} not found; downloaded models only", file=sys.stderr)
        return 2

    name = board.stem
    glb = out_dir / f"{name}.glb"
    step = out_dir / f"{name}-components.step"

    preview_text = text
    for old, new in replacements.items():
        preview_text = preview_text.replace(
            "${KICAD9_3DMODEL_DIR}/" + old,
            "${KICAD9_3DMODEL_DIR}/" + new,
        )
    preview_board = out_dir / f"{name}-preview.kicad_pcb"
    preview_board.write_text(preview_text)

    rc = run([
        cli, "pcb", "export", "glb",
        "-o", str(glb), "-f", "--subst-models",
        "-D", f"KICAD9_3DMODEL_DIR={models_dir}",
        str(preview_board),
    ])
    if rc != 0:
        return rc

    run([
        cli, "pcb", "export", "step",
        "-o", str(step), "-f", "--subst-models",
        "-D", f"KICAD9_3DMODEL_DIR={models_dir}",
        str(preview_board),
    ])

    if not args.skip_render:
        for side in ("top", "bottom"):
            png = out_dir / f"{name}-3d-{side}.png"
            rc = run([
                cli, "pcb", "render",
                "-o", str(png),
                "--side", side,
                "--quality", "high",
                "--perspective",
                "--rotate", "-45,0,45",
                "--background", "opaque",
                "-D", f"KICAD9_3DMODEL_DIR={models_dir}",
                str(preview_board),
            ])
            if rc != 0:
                print(f"  ! {side} render failed (continuing)")

    preview_board.unlink(missing_ok=True)

    print(f"\nwrote {glb}")
    if step.exists():
        print(f"wrote {step} ({step.stat().st_size} bytes)")
    if replacements:
        print(f"\n{len(replacements)} model(s) replaced by simple VRML envelopes:")
        for rel in replacements:
            print(f"  - {rel}")
    if missing:
        print(f"\n{len(missing)} model(s) not in the official library; those parts are omitted:")
        for rel in missing:
            print(f"  - {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
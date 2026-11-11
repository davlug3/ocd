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
    for rel in rels:
        dest = models_dir / rel
        ok = download(f"{GITHUB_RAW}/{rel}", dest)
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

    rc = run([
        cli, "pcb", "export", "glb",
        "-o", str(glb), "-f", "--subst-models",
        "-D", f"KICAD9_3DMODEL_DIR={models_dir}",
        str(board),
    ])
    if rc != 0:
        return rc

    run([
        cli, "pcb", "export", "step",
        "-o", str(step), "-f", "--subst-models",
        "-D", f"KICAD9_3DMODEL_DIR={models_dir}",
        str(board),
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
                str(board),
            ])
            if rc != 0:
                print(f"  ! {side} render failed (continuing)")

    print(f"\nwrote {glb}")
    if step.exists():
        print(f"wrote {step} ({step.stat().st_size} bytes)")
    if missing:
        print(f"\n{len(missing)} model(s) not in the official library; those parts are omitted:")
        for rel in missing:
            print(f"  - {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
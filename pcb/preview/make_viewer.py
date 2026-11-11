#!/usr/bin/env python3
"""Build a self-contained model-viewer HTML from the exported GLB.

The GLB is embedded as a base64 data URI so the page works when opened
directly from disk (``file://``) on a phone or laptop. The model-viewer
runtime is loaded from a CDN, so the first open needs network access.

Usage:
    python3 pcb/preview/make_viewer.py \
        --glb pcb/preview/ocd_v0p4_8v18v.glb \
        --out pcb/preview/viewer.html
"""

from __future__ import annotations

import argparse
import base64
from pathlib import Path

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  html, body {{ margin: 0; height: 100%; background: #0b0f14; overflow: hidden; }}
  model-viewer {{ width: 100%; height: 100%; background: #0b0f14; }}
  .hud {{
    position: fixed; left: 12px; bottom: 12px; z-index: 2;
    color: #cbd5e1; font: 12px/1.45 ui-monospace, SFMono-Regular, Menlo, monospace;
    background: rgba(11,15,20,.72); border: 1px solid #1f2937;
    border-radius: 8px; padding: 8px 10px; max-width: min(92vw, 520px);
    pointer-events: none;
  }}
  .hud b {{ color: #f8fafc; }}
</style>
<script type="module"
  src="https://cdn.jsdelivr.net/npm/@google/model-viewer@4.0.0/dist/model-viewer.min.js"></script>
</head>
<body>
<model-viewer
  src="data:model/gltf-binary;base64,{b64}"
  alt="{alt}"
  camera-controls
  auto-rotate
  rotation-per-second="18deg"
  camera-orbit="35deg 62deg 105%"
  field-of-view="32deg"
  environment-image="neutral"
  exposure="1.0"
  shadow-intensity="1.0"
  shadow-softness="0.8"
  touch-action="pan-y"
  loading="eager">
</model-viewer>
<div class="hud">
  <b>{title}</b><br>
  drag to orbit · pinch/scroll to zoom · double-tap to reset<br>
  preview only — not a manufacturing model
</div>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--glb", required=True, type=Path)
    ap.add_argument("--out", default=Path("pcb/preview/viewer.html"), type=Path)
    ap.add_argument("--title", default="OCD v0.4 — 3D board preview")
    args = ap.parse_args()

    data = args.glb.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    html = TEMPLATE.format(
        title=args.title,
        alt=args.title,
        b64=b64,
    )
    args.out.write_text(html)
    print(f"wrote {args.out} ({args.out.stat().st_size} bytes) from {args.glb} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
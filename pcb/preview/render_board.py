#!/usr/bin/env python3
"""Render a routed KiCad 9 board to top/bottom PNG + SVG previews.

This is a dependency-light fallback for hosts without KiCad, Freerouting or an
SVG rasteriser. It parses the s-expression ``.kicad_pcb`` directly and draws:

* the Edge.Cuts outline,
* F.Cu/B.Cu tracks and vias,
* through-hole and SMD pads (with drills),
* silkscreen lines/rects/circles and footprint reference labels,
* GND zone fills as a translucent underlay.

It is a *preview*, not a manufacturing drawing: it does not claim DRC-clean
geometry. The authoritative outputs remain the Gerbers/DRC reports from the
``pcb-design-skill`` pipeline.

Usage:
    python3 pcb/preview/render_board.py \
        --board pcb/board/ocd_v0p4_8v18v.kicad_pcb \
        --out-dir pcb/preview
"""

from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover - optional
    Image = None
    ImageDraw = None
    ImageFont = None


# ---------------------------------------------------------------------------
# s-expression parsing
# ---------------------------------------------------------------------------

TOKEN_RE = re.compile(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+')


def parse_sexpr(text: str) -> list[Any]:
    tokens = TOKEN_RE.findall(text)
    pos = 0

    def parse() -> Any:
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError("unexpected end of input")
        tok = tokens[pos]
        if tok == "(":
            pos += 1
            items: list[Any] = []
            while pos < len(tokens) and tokens[pos] != ")":
                items.append(parse())
            if pos >= len(tokens):
                raise ValueError("unclosed parenthesis")
            pos += 1
            return items
        if tok == ")":
            raise ValueError("unexpected )")
        pos += 1
        if tok.startswith('"'):
            return tok[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        return tok

    result = parse()
    if pos != len(tokens):
        raise ValueError(f"trailing tokens at {pos}")
    return result  # type: ignore[return-value]


def head(node: Any) -> str:
    return node[0] if isinstance(node, list) and node else ""


def children(node: Any, name: str) -> list[list[Any]]:
    return [c for c in node if isinstance(c, list) and head(c) == name]


def child(node: Any, name: str) -> list[Any] | None:
    for c in node:
        if isinstance(c, list) and head(c) == name:
            return c
    return None


def fnum(node: Any, default: float = 0.0) -> float:
    if not isinstance(node, list):
        return default
    for item in node[1:]:
        try:
            return float(item)
        except (TypeError, ValueError):
            continue
    return default


def fpair(node: Any) -> tuple[float, float]:
    if not isinstance(node, list):
        return (0.0, 0.0)
    nums: list[float] = []
    for item in node[1:]:
        try:
            nums.append(float(item))
        except (TypeError, ValueError):
            pass
    if len(nums) >= 2:
        return (nums[0], nums[1])
    return (0.0, 0.0)


# ---------------------------------------------------------------------------
# Board model
# ---------------------------------------------------------------------------


@dataclass
class Pad:
    number: str
    shape: str
    x: float
    y: float
    angle: float
    w: float
    h: float
    drill: float
    layers: list[str]
    net: str


@dataclass
class Footprint:
    name: str
    ref: str
    x: float
    y: float
    angle: float
    pads: list[Pad] = field(default_factory=list)
    lines: list[tuple[tuple[float, float], tuple[float, float], float, str]] = field(
        default_factory=list
    )
    rects: list[tuple[tuple[float, float], tuple[float, float], float, str]] = field(
        default_factory=list
    )
    circles: list[tuple[tuple[float, float], float, float, str]] = field(default_factory=list)


@dataclass
class Board:
    width: float
    height: float
    footprints: list[Footprint]
    segments: list[dict[str, Any]]
    vias: list[dict[str, Any]]
    zones: list[dict[str, Any]]
    outline: list[tuple[tuple[float, float], tuple[float, float]]]


def load_board(path: Path) -> Board:
    root = parse_sexpr(path.read_text())

    def find_layer(node: Any) -> str:
        lay = child(node, "layer")
        return lay[1] if lay and len(lay) > 1 else ""

    def find_at(node: Any) -> tuple[float, float, float]:
        at = child(node, "at")
        if not at:
            return (0.0, 0.0, 0.0)
        nums: list[float] = []
        for item in at[1:]:
            try:
                nums.append(float(item))
            except (TypeError, ValueError):
                pass
        x = nums[0] if len(nums) > 0 else 0.0
        y = nums[1] if len(nums) > 1 else 0.0
        a = nums[2] if len(nums) > 2 else 0.0
        return (x, y, a)

    def stroke_width(node: Any) -> float:
        st = child(node, "stroke")
        return fnum(child(st, "width")) if st else 0.0

    footprints: list[Footprint] = []
    for fp_node in children(root, "footprint"):
        name = fp_node[1] if len(fp_node) > 1 else ""
        x, y, angle = find_at(fp_node)
        ref = ""
        for prop in children(fp_node, "property"):
            if len(prop) > 2 and prop[1] == "Reference":
                ref = prop[2]
        fp = Footprint(name=name, ref=ref, x=x, y=y, angle=angle)

        for pad_node in children(fp_node, "pad"):
            if len(pad_node) < 4:
                continue
            number = pad_node[1]
            shape = pad_node[3] if isinstance(pad_node[3], str) else "circle"
            px, py, pa = find_at(pad_node)
            size = child(pad_node, "size")
            w, h = fpair(size) if size else (0.0, 0.0)
            drill_node = child(pad_node, "drill")
            drill = fnum(drill_node) if drill_node else 0.0
            layers_node = child(pad_node, "layers")
            layers = [str(v) for v in layers_node[1:]] if layers_node else []
            net = ""
            net_node = child(pad_node, "net")
            if net_node and len(net_node) > 2:
                net = str(net_node[2])
            fp.pads.append(
                Pad(number, shape, px, py, pa, w, h, drill, layers, net)
            )

        for ln in children(fp_node, "fp_line"):
            start = fpair(child(ln, "start"))
            end = fpair(child(ln, "end"))
            fp.lines.append((start, end, stroke_width(ln), find_layer(ln)))
        for rc in children(fp_node, "fp_rect"):
            start = fpair(child(rc, "start"))
            end = fpair(child(rc, "end"))
            fp.rects.append((start, end, stroke_width(rc), find_layer(rc)))
        for ci in children(fp_node, "fp_circle"):
            center = fpair(child(ci, "center"))
            end = fpair(child(ci, "end"))
            r = math.dist(center, end)
            fp.circles.append((center, r, stroke_width(ci), find_layer(ci)))
        footprints.append(fp)

    segments: list[dict[str, Any]] = []
    for seg in children(root, "segment"):
        segments.append(
            {
                "start": fpair(child(seg, "start")),
                "end": fpair(child(seg, "end")),
                "width": fnum(child(seg, "width")),
                "layer": find_layer(seg),
                "net": str(child(seg, "net")[1]) if child(seg, "net") else "",
            }
        )

    vias: list[dict[str, Any]] = []
    for via in children(root, "via"):
        vias.append(
            {
                "at": fpair(child(via, "at")),
                "size": fnum(child(via, "size")),
                "drill": fnum(child(via, "drill")),
                "layers": [str(v) for v in (child(via, "layers")[1:] if child(via, "layers") else [])],
                "net": str(child(via, "net")[1]) if child(via, "net") else "",
            }
        )

    zones: list[dict[str, Any]] = []
    for zone in children(root, "zone"):
        polys: list[list[tuple[float, float]]] = []
        for fp_poly in children(zone, "filled_polygon"):
            pts_node = child(fp_poly, "pts")
            if pts_node:
                polys.append([fpair(p) for p in children(pts_node, "xy")])
        if not polys:
            poly = child(zone, "polygon")
            pts_node = child(poly, "pts") if poly else None
            if pts_node:
                polys.append([fpair(p) for p in children(pts_node, "xy")])
        zones.append(
            {
                "net": str(child(zone, "net")[1]) if child(zone, "net") else "",
                "layer": find_layer(zone),
                "polys": polys,
            }
        )

    outline: list[tuple[tuple[float, float], tuple[float, float]]] = []
    for ln in children(root, "gr_line"):
        if find_layer(ln) == "Edge.Cuts":
            outline.append((fpair(child(ln, "start")), fpair(child(ln, "end"))))
    for rc in children(root, "gr_rect"):
        if find_layer(rc) == "Edge.Cuts":
            a = fpair(child(rc, "start"))
            b = fpair(child(rc, "end"))
            outline.extend(
                [
                    (a, (b[0], a[1])),
                    ((b[0], a[1]), b),
                    (b, (a[0], b[1])),
                    ((a[0], b[1]), a),
                ]
            )

    xs = [p[0] for seg in outline for p in seg]
    ys = [p[1] for seg in outline for p in seg]
    width = max(xs) - min(xs) if xs else 100.0
    height = max(ys) - min(ys) if ys else 80.0
    return Board(width, height, footprints, segments, vias, zones, outline)


# ---------------------------------------------------------------------------
# Rendering primitives
# ---------------------------------------------------------------------------


@dataclass
class Prim:
    kind: str
    points: list[tuple[float, float]]
    width: float
    color: str
    fill: bool = False
    text: str = ""
    size: float = 0.0


class Canvas:
    def __init__(self, board: Board, scale: float, margin_mm: float, flip: bool = False):
        self.board = board
        self.scale = scale
        self.flip = flip
        self.margin = margin_mm * scale
        self.w_px = int(round(board.width * scale + 2 * margin_mm * scale))
        self.h_px = int(round(board.height * scale + 2 * margin_mm * scale))
        self.prims: list[Prim] = []

    def pt(self, x: float, y: float) -> tuple[float, float]:
        if self.flip:
            x = self.board.width - x
        return (
            self.margin + x * self.scale,
            self.margin + y * self.scale,
        )

    def line(self, a: tuple[float, float], b: tuple[float, float], width_mm: float, color: str):
        self.prims.append(Prim("line", [self.pt(*a), self.pt(*b)], width_mm, color))

    def circle(self, c: tuple[float, float], d_mm: float, color: str):
        self.prims.append(Prim("circle", [self.pt(*c)], d_mm, color))

    def rect(self, a: tuple[float, float], b: tuple[float, float], width_mm: float, color: str):
        p1 = self.pt(*a)
        p2 = self.pt(*b)
        pts = [p1, (p2[0], p1[1]), p2, (p1[0], p2[1])]
        self.prims.append(Prim("poly", pts, width_mm, color, fill=False))

    def polygon(self, pts: Iterable[tuple[float, float]], color: str, alpha_fill: bool = False):
        p = [self.pt(*q) for q in pts]
        self.prims.append(Prim("polygon", p, 0.0, color, fill=True))

    def text(self, at: tuple[float, float], s: str, size_mm: float, color: str):
        self.prims.append(
            Prim("text", [self.pt(*at)], 0.0, color, text=s, size=size_mm)
        )


def transform(x: float, y: float, ox: float, oy: float, angle: float) -> tuple[float, float]:
    """Rotate a local footprint point into board coordinates.

    KiCad stores Y downward; a positive angle is counter-clockwise as displayed.
    """
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    return (ox + x * ca + y * sa, oy - x * sa + y * ca)


def pad_polygon(pad: Pad, fp: Footprint) -> tuple[str, list[tuple[float, float]]]:
    """Return (shape kind, points) for a pad in board coordinates."""
    total = fp.angle + pad.angle
    cx, cy = transform(pad.x, pad.y, fp.x, fp.y, fp.angle)
    if pad.shape == "circle":
        return ("circle", [(cx, cy)])
    if pad.shape == "rect":
        a = math.radians(total)
        ca, sa = math.cos(a), math.sin(a)
        hw, hh = pad.w / 2.0, pad.h / 2.0
        corners = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
        pts = [
            (cx + lx * ca + ly * sa, cy - lx * sa + ly * ca)
            for lx, ly in corners
        ]
        return ("poly", pts)
    # oval / roundrect / trapezoid: approximate with an oriented rectangle
    a = math.radians(total)
    ca, sa = math.cos(a), math.sin(a)
    hw, hh = pad.w / 2.0, pad.h / 2.0
    corners = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
    pts = [
        (cx + lx * ca + ly * sa, cy - lx * sa + ly * ca)
        for lx, ly in corners
    ]
    return ("poly", pts)


def visible(layers: list[str], view: str) -> bool:
    want = "F.Cu" if view == "top" else "B.Cu"
    return any(l in (want, "*.Cu") for l in layers)


def render(board: Board, view: str, scale: float) -> Canvas:
    flip = view == "bottom"
    cv = Canvas(board, scale, margin_mm=6.0, flip=flip)
    copper = "#E0A040" if view == "top" else "#4FA3D1"
    copper_dim = "#8A6428" if view == "top" else "#2E5F7A"
    silk = "#F4F1E8"
    outline = "#FFFFFF"

    # zones first (translucent copper underlay)
    for z in board.zones:
        if z["layer"] != ("F.Cu" if view == "top" else "B.Cu"):
            continue
        for poly in z["polys"]:
            cv.prims.append(
                Prim("polygon", [cv.pt(*p) for p in poly], 0.0, copper_dim, fill=True)
            )

    # tracks
    for seg in board.segments:
        if seg["layer"] != ("F.Cu" if view == "top" else "B.Cu"):
            continue
        cv.line(seg["start"], seg["end"], seg["width"], copper)

    # vias
    for via in board.vias:
        if not visible(via["layers"], view):
            continue
        d = via["size"]
        cv.circle(via["at"], d, copper)
        cv.circle(via["at"], via["drill"], "#0B0F14")

    # footprints
    for fp in board.footprints:
        silk_layer = "F.SilkS" if view == "top" else "B.SilkS"
        for a, b, w, layer in fp.lines:
            if layer != silk_layer:
                continue
            pa = transform(a[0], a[1], fp.x, fp.y, fp.angle)
            pb = transform(b[0], b[1], fp.x, fp.y, fp.angle)
            cv.line(pa, pb, max(w, 0.12), silk)
        for a, b, w, layer in fp.rects:
            if layer != silk_layer:
                continue
            pa = transform(a[0], a[1], fp.x, fp.y, fp.angle)
            pb = transform(b[0], b[1], fp.x, fp.y, fp.angle)
            # approximate a rotated rectangle by its four transformed corners
            lo_x, lo_y = a
            hi_x, hi_y = b
            corners = [
                (lo_x, lo_y),
                (hi_x, lo_y),
                (hi_x, hi_y),
                (lo_x, hi_y),
            ]
            pts = [transform(x, y, fp.x, fp.y, fp.angle) for x, y in corners]
            cv.prims.append(Prim("poly", [cv.pt(*p) for p in pts], max(w, 0.12), silk))
        for center, r, w, layer in fp.circles:
            if layer != silk_layer:
                continue
            pc = transform(center[0], center[1], fp.x, fp.y, fp.angle)
            cv.circle(pc, 2 * r, silk)

        for pad in fp.pads:
            if not visible(pad.layers, view):
                continue
            kind, pts = pad_polygon(pad, fp)
            if kind == "circle":
                cv.circle(pts[0], max(pad.w, pad.h), copper)
            else:
                cv.prims.append(Prim("polygon", [cv.pt(*p) for p in pts], 0.0, copper, fill=True))
            if pad.drill > 0:
                cx, cy = transform(pad.x, pad.y, fp.x, fp.y, fp.angle)
                cv.circle((cx, cy), pad.drill, "#0B0F14")

        if fp.ref:
            rx, ry = transform(0.0, 0.0, fp.x, fp.y, fp.angle)
            cv.text((rx, ry - 1.2), fp.ref, 1.6, silk)

    # outline last
    for a, b in board.outline:
        cv.line(a, b, 0.15, outline)

    return cv


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def _svg_poly(points: list[tuple[float, float]]) -> str:
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in points)


def write_svg(cv: Canvas, path: Path, title: str) -> None:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{cv.w_px}" height="{cv.h_px}" '
        f'viewBox="0 0 {cv.w_px} {cv.h_px}">',
        f"<title>{title}</title>",
        f'<rect width="100%" height="100%" fill="#0B0F14"/>',
        f'<rect x="{cv.margin:.2f}" y="{cv.margin:.2f}" '
        f'width="{cv.board.width * cv.scale:.2f}" height="{cv.board.height * cv.scale:.2f}" '
        f'fill="#123B2A" stroke="none"/>',
    ]
    for p in cv.prims:
        if p.kind == "line":
            (x1, y1), (x2, y2) = p.points
            parts.append(
                f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                f'stroke="{p.color}" stroke-width="{max(p.width * cv.scale, 0.6):.2f}" '
                f'stroke-linecap="round"/>'
            )
        elif p.kind == "circle":
            (x, y) = p.points[0]
            parts.append(
                f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{p.width * cv.scale / 2:.2f}" '
                f'fill="{p.color}"/>'
            )
        elif p.kind == "polygon":
            fill = p.color if p.fill else "none"
            parts.append(
                f'<polygon points="{_svg_poly(p.points)}" fill="{fill}" '
                f'stroke="{p.color if not p.fill else "none"}" '
                f'stroke-width="{max(p.width * cv.scale, 0.6):.2f}"/>'
            )
        elif p.kind == "text":
            (x, y) = p.points[0]
            parts.append(
                f'<text x="{x:.2f}" y="{y:.2f}" fill="{p.color}" '
                f'font-family="monospace" font-size="{p.size * cv.scale:.2f}" '
                f'text-anchor="middle">{p.text}</text>'
            )
    parts.append("</svg>")
    path.write_text("\n".join(parts))


def write_png(cv: Canvas, path: Path, title: str) -> None:
    if Image is None:  # pragma: no cover
        raise RuntimeError("Pillow is required for PNG output")
    img = Image.new("RGB", (cv.w_px, cv.h_px), "#0B0F14")
    draw = ImageDraw.Draw(img)
    draw.rectangle(
        [
            cv.margin,
            cv.margin,
            cv.margin + cv.board.width * cv.scale,
            cv.margin + cv.board.height * cv.scale,
        ],
        fill="#123B2A",
    )

    for p in cv.prims:
        color = p.color
        if p.kind == "line":
            (x1, y1), (x2, y2) = p.points
            draw.line(
                [(x1, y1), (x2, y2)],
                fill=color,
                width=max(int(round(p.width * cv.scale)), 1),
            )
        elif p.kind == "circle":
            (x, y) = p.points[0]
            r = p.width * cv.scale / 2
            draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
        elif p.kind == "polygon":
            if p.fill:
                draw.polygon(p.points, fill=color)
            else:
                draw.line(p.points + [p.points[0]], fill=color, width=2)
        elif p.kind == "text":
            (x, y) = p.points[0]
            size = max(int(p.size * cv.scale), 8)
            try:
                font = ImageFont.truetype("DejaVuSansMono.ttf", size)
            except OSError:
                font = ImageFont.load_default()
            draw.text((x, y), p.text, fill=color, font=font, anchor="mm")

    img.save(path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--board", required=True, type=Path)
    ap.add_argument("--out-dir", default=Path("pcb/preview"), type=Path)
    ap.add_argument("--scale", type=float, default=16.0, help="pixels per mm")
    ap.add_argument("--prefix", default=None)
    args = ap.parse_args()

    board = load_board(args.board)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.prefix or args.board.stem

    for view in ("top", "bottom"):
        cv = render(board, view, args.scale)
        stem = f"{prefix}_{view}"
        write_svg(cv, args.out_dir / f"{stem}.svg", f"{prefix} {view}")
        write_png(cv, args.out_dir / f"{stem}.png", f"{prefix} {view}")
        print(f"wrote {args.out_dir / stem}.svg and .png ({cv.w_px}x{cv.h_px})")

    print(
        f"board {board.width:.2f} x {board.height:.2f} mm, "
        f"{len(board.footprints)} footprints, "
        f"{len(board.segments)} tracks, {len(board.vias)} vias"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
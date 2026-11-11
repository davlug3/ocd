#!/usr/bin/env python3
"""Render the generated KiCad 9 schematic to a top-level PNG + SVG preview.

The circuit-design-skill emits a deterministic *symbol grid*: each part is a
symbol instance with absolute Reference/Value properties, and every pin is
tied to a global label (the generator does not emit wire geometry). This
renderer draws exactly what the ``.kicad_sch`` contains, so the preview is
faithful to the file rather than a re-drawn approximation.

It is a preview only: it is not an ERC/DRC result and does not replace
``kicad-cli sch export``.

Usage:
    python3 circuit/preview/render_schematic.py \
        --sch circuit/spec/out_ocd_v0p4_8v18v/ocd_v0p4_8v18v.kicad_sch \
        --out-dir circuit/preview
"""

from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    Image = None
    ImageDraw = None
    ImageFont = None


# ---------------------------------------------------------------------------
# s-expression parsing (kept local so this script has no dependencies)
# ---------------------------------------------------------------------------

TOKEN_RE = re.compile(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+')


def parse(text: str) -> list[Any]:
    toks = TOKEN_RE.findall(text)
    i = 0

    def one() -> Any:
        nonlocal i
        t = toks[i]
        if t == "(":
            i += 1
            out: list[Any] = []
            while toks[i] != ")":
                out.append(one())
            i += 1
            return out
        i += 1
        if t.startswith('"'):
            return t[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        return t

    root = one()
    if i != len(toks):
        raise ValueError("trailing tokens")
    return root  # type: ignore[return-value]


def head(n: Any) -> str:
    return n[0] if isinstance(n, list) and n else ""


def kids(n: Any, name: str) -> list[list[Any]]:
    return [c for c in n if isinstance(c, list) and head(c) == name]


def kid(n: Any, name: str) -> list[Any] | None:
    for c in n:
        if isinstance(c, list) and head(c) == name:
            return c
    return None


def nums(node: Any) -> list[float]:
    if not isinstance(node, list):
        return []
    out: list[float] = []
    for x in node[1:]:
        try:
            out.append(float(x))
        except (TypeError, ValueError):
            pass
    return out


def at(node: Any) -> tuple[float, float, float]:
    a = kid(node, "at")
    v = nums(a) if a else []
    return (v[0] if len(v) > 0 else 0.0,
            v[1] if len(v) > 1 else 0.0,
            v[2] if len(v) > 2 else 0.0)


def stroke_width(node: Any) -> float:
    st = kid(node, "stroke")
    if not st:
        return 0.254
    w = kid(st, "width")
    return float(w[1]) if w and len(w) > 1 else 0.254


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------


@dataclass
class Prim:
    kind: str  # line | rect | circle | polyline | polygon | text
    pts: list[tuple[float, float]]  # schematic mm (Y up)
    width: float
    text: str = ""
    size: float = 1.27
    angle: float = 0.0
    anchor: str = "start"
    color: str = "#111111"


@dataclass
class Instance:
    lib_id: str
    x: float
    y: float
    angle: float
    mirror: str
    ref: str
    value: str
    ref_at: tuple[float, float, float]
    value_at: tuple[float, float, float]


def load(path: Path) -> tuple[dict[str, list[Prim]], list[Instance], list[Prim]]:
    root = parse(path.read_text())
    libs: dict[str, list[Prim]] = {}

    for sym in kids(kid(root, "lib_symbols") or [], "symbol"):
        name = str(sym[1])
        prims: list[Prim] = []
        for sub in kids(sym, "symbol"):
            # "R_0_1" common graphics + "R_1_1" unit graphics
            if not re.search(r"_0_1$|_1_1$", str(sub[1])):
                continue
            for rc in kids(sub, "rectangle"):
                a = nums(kid(rc, "start"))
                b = nums(kid(rc, "end"))
                if len(a) >= 2 and len(b) >= 2:
                    prims.append(Prim("rect", [(a[0], a[1]), (b[0], b[1])], stroke_width(rc)))
            for ci in kids(sub, "circle"):
                c = nums(kid(ci, "center"))
                r = nums(kid(ci, "radius"))
                if len(c) >= 2 and r:
                    prims.append(Prim("circle", [(c[0], c[1])], stroke_width(ci)))
                    prims[-1].size = float(r[0])
            for pl in kids(sub, "polyline"):
                pts = [tuple(nums(p)[:2]) for p in kids(kid(pl, "pts") or [], "xy")]
                pts = [p for p in pts if len(p) == 2]
                prims.append(Prim("polyline", pts, stroke_width(pl)))
            for pin in kids(sub, "pin"):
                p = nums(kid(pin, "at"))
                ln = nums(kid(pin, "length"))
                if len(p) < 3 or not ln:
                    continue
                ang = math.radians(p[2])
                L = float(ln[0])
                x0, y0 = p[0], p[1]
                x1, y1 = x0 + L * math.cos(ang), y0 + L * math.sin(ang)
                prims.append(Prim("line", [(x0, y0), (x1, y1)], 0.254))
        libs[name] = prims

    instances: list[Instance] = []
    for sym in kids(root, "symbol"):
        lib_node = kid(sym, "lib_id")
        if not lib_node:
            continue
        lib_id = str(lib_node[1])
        x, y, angle = at(sym)
        mirror_node = kid(sym, "mirror")
        mirror = str(mirror_node[1]) if mirror_node else ""
        ref = value = ""
        ref_at = value_at = (0.0, 0.0, 0.0)
        for prop in kids(sym, "property"):
            if len(prop) < 3:
                continue
            key = str(prop[1])
            val = str(prop[2])
            if key == "Reference":
                ref = val
                ref_at = at(prop)
            elif key == "Value":
                value = val
                value_at = at(prop)
        instances.append(
            Instance(lib_id, x, y, angle, mirror, ref, value, ref_at, value_at)
        )

    labels: list[Prim] = []
    for gl in kids(root, "global_label"):
        name = str(gl[1]) if len(gl) > 1 else ""
        x, y, angle = at(gl)
        if angle == 90:
            anchor = "start"
        elif angle == 270:
            anchor = "end"
        elif angle == 180:
            anchor = "end"
        else:
            anchor = "start"
        labels.append(Prim("text", [(x, y)], 0.0, text=name, size=1.27,
                           angle=angle, anchor=anchor, color="#0B4F8A"))
        # a small tick at the attachment point so the label reads as a pin tag
        labels.append(Prim("line", [(x, y), (x, y)], 0.2, color="#0B4F8A"))

    return libs, instances, labels


def instance_prims(lib: list[Prim], inst: Instance) -> list[Prim]:
    out: list[Prim] = []
    a = math.radians(inst.angle)
    ca, sa = math.cos(a), math.sin(a)

    def tr(x: float, y: float) -> tuple[float, float]:
        if "x" in inst.mirror:
            x = -x
        if "y" in inst.mirror:
            y = -y
        return (inst.x + x * ca - y * sa, inst.y + x * sa + y * ca)

    for p in lib:
        q = Prim(p.kind, [tr(x, y) for x, y in p.pts], p.width, p.text, p.size,
                 p.angle + inst.angle, p.anchor, p.color)
        out.append(q)
    for prop, txt in ((inst.ref_at, inst.ref), (inst.value_at, inst.value)):
        if not txt:
            continue
        out.append(Prim("text", [prop[:2]], 0.0, text=txt, size=1.27,
                        angle=prop[2], anchor="start", color="#111111"))
    return out


# ---------------------------------------------------------------------------
# Canvas
# ---------------------------------------------------------------------------


class Canvas:
    def __init__(self, prims: list[Prim], scale: float, margin_mm: float = 4.0):
        xs: list[float] = []
        ys: list[float] = []
        for p in prims:
            for x, y in p.pts:
                xs.append(x)
                ys.append(y)
        self.minx = min(xs) - margin_mm
        self.maxx = max(xs) + margin_mm
        self.miny = min(ys) - margin_mm
        self.maxy = max(ys) + margin_mm
        self.scale = scale
        self.w = int(round((self.maxx - self.minx) * scale))
        self.h = int(round((self.maxy - self.miny) * scale))
        self.prims = prims

    def pt(self, x: float, y: float) -> tuple[float, float]:
        return ((x - self.minx) * self.scale,
                (self.maxy - y) * self.scale)


def write_svg(cv: Canvas, path: Path, title: str) -> None:
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{cv.w}" height="{cv.h}" '
        f'viewBox="0 0 {cv.w} {cv.h}">',
        f"<title>{title}</title>",
        '<rect width="100%" height="100%" fill="#FFFFFF"/>',
    ]
    for p in cv.prims:
        color = p.color
        if p.kind == "line":
            (x1, y1), (x2, y2) = (cv.pt(*p.pts[0]), cv.pt(*p.pts[1]))
            out.append(
                f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                f'stroke="{color}" stroke-width="{max(p.width * cv.scale, 0.6):.2f}"/>'
            )
        elif p.kind == "polyline":
            pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in (cv.pt(*q) for q in p.pts))
            out.append(
                f'<polyline points="{pts}" fill="none" stroke="{color}" '
                f'stroke-width="{max(p.width * cv.scale, 0.6):.2f}" '
                f'stroke-linejoin="round" stroke-linecap="round"/>'
            )
        elif p.kind == "rect":
            (x1, y1) = cv.pt(*p.pts[0])
            (x2, y2) = cv.pt(*p.pts[1])
            out.append(
                f'<rect x="{min(x1, x2):.2f}" y="{min(y1, y2):.2f}" '
                f'width="{abs(x2 - x1):.2f}" height="{abs(y2 - y1):.2f}" '
                f'fill="none" stroke="{color}" '
                f'stroke-width="{max(p.width * cv.scale, 0.6):.2f}"/>'
            )
        elif p.kind == "circle":
            (x, y) = cv.pt(*p.pts[0])
            out.append(
                f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{p.size * cv.scale:.2f}" '
                f'fill="none" stroke="{color}" '
                f'stroke-width="{max(p.width * cv.scale, 0.6):.2f}"/>'
            )
        elif p.kind == "text":
            x, y = cv.pt(*p.pts[0])
            anchor = p.anchor
            rot = -p.angle if p.angle in (90, 270) else 0
            out.append(
                f'<text x="{x:.2f}" y="{y:.2f}" fill="{color}" '
                f'font-family="monospace" font-size="{p.size * cv.scale:.2f}" '
                f'text-anchor="{anchor}" transform="rotate({rot} {x:.2f} {y:.2f})">'
                f"{p.text}</text>"
            )
    out.append("</svg>")
    path.write_text("\n".join(out))


def _font(size: int):
    try:
        return ImageFont.truetype("DejaVuSansMono.ttf", size)
    except OSError:
        return ImageFont.load_default()


def write_png(cv: Canvas, path: Path, title: str) -> None:
    if Image is None:  # pragma: no cover
        raise RuntimeError("Pillow is required for PNG output")
    img = Image.new("RGB", (cv.w, cv.h), "#FFFFFF")
    d = ImageDraw.Draw(img)
    for p in cv.prims:
        color = p.color
        if p.kind == "line":
            (x1, y1) = cv.pt(*p.pts[0])
            (x2, y2) = cv.pt(*p.pts[1])
            d.line([(x1, y1), (x2, y2)], fill=color,
                   width=max(int(round(p.width * cv.scale)), 1))
        elif p.kind == "polyline":
            pts = [cv.pt(*q) for q in p.pts]
            if len(pts) > 1:
                d.line(pts, fill=color, width=max(int(round(p.width * cv.scale)), 1),
                       joint="curve")
        elif p.kind == "rect":
            (x1, y1) = cv.pt(*p.pts[0])
            (x2, y2) = cv.pt(*p.pts[1])
            d.rectangle([min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)],
                        outline=color, width=max(int(round(p.width * cv.scale)), 1))
        elif p.kind == "circle":
            (x, y) = cv.pt(*p.pts[0])
            r = p.size * cv.scale
            d.ellipse([x - r, y - r, x + r, y + r], outline=color,
                      width=max(int(round(p.width * cv.scale)), 1))
        elif p.kind == "text":
            x, y = cv.pt(*p.pts[0])
            size = max(int(round(p.size * cv.scale)), 6)
            font = _font(size)
            # measure to place rotated text by its anchor
            l, t, r, b = d.textbbox((0, 0), p.text, font=font)
            tw, th = r - l, b - t
            pad = 4
            tmp = Image.new("RGBA", (tw + 2 * pad, th + 2 * pad), (255, 255, 255, 0))
            td = ImageDraw.Draw(tmp)
            td.text((pad - l, pad - t), p.text, font=font, fill=color)
            rot = tmp.rotate(p.angle, expand=True, resample=Image.BICUBIC)
            if p.anchor == "end":
                ax = rot.width
            elif p.anchor == "middle":
                ax = rot.width / 2
            else:
                ax = 0
            img.paste(rot, (int(x - ax), int(y - rot.height / 2)), rot)
    img.save(path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sch", required=True, type=Path)
    ap.add_argument("--out-dir", default=Path("circuit/preview"), type=Path)
    ap.add_argument("--scale", type=float, default=9.0, help="pixels per mm")
    ap.add_argument("--prefix", default=None)
    args = ap.parse_args()

    libs, instances, labels = load(args.sch)
    prims: list[Prim] = []
    for inst in instances:
        prims.extend(instance_prims(libs.get(inst.lib_id, []), inst))
    prims.extend(labels)

    cv = Canvas(prims, args.scale)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    stem = args.prefix or args.sch.stem
    write_svg(cv, args.out_dir / f"{stem}.svg", stem)
    write_png(cv, args.out_dir / f"{stem}.png", stem)
    print(f"wrote {args.out_dir / stem}.svg and .png ({cv.w}x{cv.h})")
    print(f"{len(instances)} symbols, {len(libs)} library symbols, {len(labels)} label primitives")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
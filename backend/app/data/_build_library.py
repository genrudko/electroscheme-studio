#!/usr/bin/env python3
"""GOST/ESKD-compliant SVG builders for electrical scheme symbols.

Implements conditional graphic symbols (UGO) per:
  ГОСТ 2.701-2008, 2.709-89, 2.710-81, 2.721-74, 2.722-68,
  2.723-68, 2.728-74, 2.729-68, 2.742-68, 2.747-68, 2.755-87,
  2.759-82, 2.768-90

Module grid: d = 2.5 mm (ГОСТ 2.747-68)
Standard angles: 30°, 45°, 60°, 90°
"""
from __future__ import annotations

from typing import Any

SW = 0.8
SC = 0.35
BLACK = "black"

# ── SVG primitives ────────────────────────────────────────────────

def _s(tag: str, attrs: dict[str, Any], children: str = "") -> str:
    parts = [f'{k}="{v}"' for k, v in attrs.items()]
    a = " ".join(parts)
    if children:
        return f"<{tag} {a}>{children}</{tag}>"
    return f"<{tag} {a}/>"


def _line(x1: float, y1: float, x2: float, y2: float,
          sw: float = SW) -> str:
    return _s("line", {"x1": x1, "y1": y1, "x2": x2, "y2": y2,
                        "stroke": BLACK, "stroke-width": sw})


def _circle(cx: float, cy: float, r: float, sw: float = SC,
            fill: str = "none") -> str:
    return _s("circle", {"cx": cx, "cy": cy, "r": r,
                          "stroke": BLACK, "stroke-width": sw,
                          "fill": fill})


def _rect(x: float, y: float, w: float, h: float,
          sw: float = SC) -> str:
    return _s("rect", {"x": x, "y": y, "width": w, "height": h,
                        "stroke": BLACK, "stroke-width": sw,
                        "fill": "none"})


def _text(x: float, y: float, t: str, sz: float = 3.5) -> str:
    return _s("text", {
        "x": x, "y": y,
        "font-family": "Arial,Helvetica,sans-serif",
        "font-size": sz, "fill": BLACK,
        "text-anchor": "middle",
        "dominant-baseline": "central",
    }, t)


def _path(d: str, sw: float = SC) -> str:
    return _s("path", {"d": d, "stroke": BLACK,
                        "stroke-width": sw, "fill": "none"})


def _polyline(pts: str, sw: float = SW) -> str:
    return _s("polyline", {"points": pts, "stroke": BLACK,
                            "stroke-width": sw, "fill": "none"})


def _filled_circle(cx: float, cy: float, r: float) -> str:
    return _circle(cx, cy, r, sw=SC, fill=BLACK)


def _mk_svg(vb: str, *elements: str) -> str:
    inner = "".join(elements)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">'
        f'<g stroke="currentColor" fill="none" '
        f'stroke-width="{SW}" stroke-linecap="round" '
        f'stroke-linejoin="round">{inner}</g></svg>'
    )


# ── Symbol constructors ───────────────────────────────────────────

def _term(id_: str, rx: float, ry: float) -> dict:
    return {"id": id_, "rx": rx, "ry": ry}


def _sym(
    id_: str, type_: str, name: str, cat: str,
    gost: str, gost_ref: str,
    vw: str, dw: float, dh: float,
    terminals: list[dict], svg: str,
    letter: str = "",
    props: dict | None = None,
    interactive: bool = False,
    states: list[dict] | None = None,
    def_state: str = "normal",
    mw: float = 0, mh: float = 0,
) -> dict:
    s: dict[str, Any] = {
        "id": id_, "type": type_, "name": name,
        "category": cat,
        "gost": gost, "gost_ref": gost_ref,
        "viewBox": vw,
        "default_width": dw, "default_height": dh,
        "terminals": terminals,
        "default_properties": props or {},
        "svg": svg, "interactive": interactive,
        "default_state": def_state,
        "current_state": def_state,
        "states": states or [],
        "letter_designation": letter,
        "module_width": mw or dw,
        "module_height": mh or dh,
        "line_width_main": SW,
        "line_width_contour": SC,
    }
    return s


# ══════════════════════════════════════════════════════════════════
#  GOST-COMPLIANT SVG BUILDER FUNCTIONS
# ══════════════════════════════════════════════════════════════════

# ── CIRCUIT BREAKERS  (ГОСТ 2.755-87) ────────────────────────────
# Single-line: square/rectangle on bus line
# Normal: moving contact with fixed contacts

def svg_cb_sl_closed(vb: str = "0 0 100 60", y: float = 30,
                     bx: float = 32, bw: float = 24,
                     bh: float = 20) -> str:
    x0 = (100 - bw) / 2
    return _mk_svg(vb,
        _line(0, y, x0, y),
        _rect(x0, y - bh / 2, bw, bh, SW),
        _line(x0 + bw, y, 100, y),
    )


def svg_cb_sl_open(vb: str = "0 0 100 60", y: float = 30,
                   bx: float = 32, bw: float = 24,
                   bh: float = 20) -> str:
    x0 = (100 - bw) / 2
    return _mk_svg(vb,
        _line(0, y, x0, y),
        _rect(x0, y - bh / 2, bw, bh, SW),
        _line(x0 + bw, y, 100, y),
        _line(x0 + bw / 2, y - bh / 2, x0 + bw / 2, y - bh / 2 - 8),
    )


def svg_cb_normal_closed(
    vb: str = "0 0 80 60", y: float = 40,
) -> str:
    px, py = 15, y
    cx, cy = 65, y
    arm_len = 38
    import math
    ex = px + arm_len * math.cos(math.radians(35))
    ey = py - arm_len * math.sin(math.radians(35))
    return _mk_svg(vb,
        _filled_circle(px, py, 2.5),
        _filled_circle(cx, cy, 2.5),
        _line(px, py, cx, cy, SW),
    )


def svg_cb_normal_open(
    vb: str = "0 0 80 60", y: float = 40,
) -> str:
    px, py = 15, y
    cx, cy = 65, y
    arm_len = 38
    import math
    ex = px + arm_len * math.cos(math.radians(35))
    ey = py - arm_len * math.sin(math.radians(35))
    return _mk_svg(vb,
        _filled_circle(px, py, 2.5),
        _filled_circle(cx, cy, 2.5),
        _line(px, py, ex, ey, SW),
    )


def svg_cb_normal_blown(
    vb: str = "0 0 80 60", y: float = 40,
) -> str:
    px, py = 15, y
    cx, cy = 65, y
    return _mk_svg(vb,
        _filled_circle(px, py, 2.5),
        _filled_circle(cx, cy, 2.5),
        _line(px, py, 45, py - 18, SW),
        _line(45, py + 2, 45, py + 8, SC),
    )


# ── DISCONNECTORS  (ГОСТ 2.755-87) ──────────────────────────────
# Single-line: knife switch — pivot + diagonal arm + fixed contact

def svg_ds_sl_closed(
    vb: str = "0 0 100 60", y: float = 30,
) -> str:
    px, py = 30, y
    cx, cy = 70, y
    return _mk_svg(vb,
        _line(0, y, px, y),
        _filled_circle(px, py, 2),
        _line(px, py, cx, cy, SW),
        _line(cx, cy - 8, cx, cy + 8, SW),
        _line(cx, y, 100, y),
    )


def svg_ds_sl_open(
    vb: str = "0 0 100 60", y: float = 30,
) -> str:
    px, py = 30, y
    cx, cy = 70, y
    arm_len = 35
    import math
    ex = px + arm_len * math.cos(math.radians(60))
    ey = py - arm_len * math.sin(math.radians(60))
    return _mk_svg(vb,
        _line(0, y, px, y),
        _filled_circle(px, py, 2),
        _line(px, py, ex, ey, SW),
        _line(cx, cy - 8, cx, cy + 8, SW),
        _line(cx, y, 100, y),
    )


def svg_ds_normal_closed(
    vb: str = "0 0 80 60", y: float = 40,
) -> str:
    px, py = 15, y
    cx, cy = 65, y
    return _mk_svg(vb,
        _filled_circle(px, py, 2.5),
        _filled_circle(cx, cy, 2.5),
        _line(cx, cy - 8, cx, cy + 8, SW),
        _line(px, py, cx, cy, SW),
    )


def svg_ds_normal_open(
    vb: str = "0 0 80 60", y: float = 40,
) -> str:
    px, py = 15, y
    cx, cy = 65, y
    arm_len = 38
    import math
    ex = px + arm_len * math.cos(math.radians(35))
    ey = py - arm_len * math.sin(math.radians(35))
    return _mk_svg(vb,
        _filled_circle(px, py, 2.5),
        _filled_circle(cx, cy, 2.5),
        _line(cx, cy - 8, cx, cy + 8, SW),
        _line(px, py, ex, ey, SW),
    )


# ── GROUNDING SWITCH  (ГОСТ 2.755-87) ───────────────────────────

def svg_grounding_sl(
    vb: str = "0 0 100 80", y: float = 30,
) -> str:
    px, py = 30, y
    gx, gy = 70, y + 30
    return _mk_svg(vb,
        _line(0, y, px, y),
        _filled_circle(px, py, 2),
        _line(px, py, 70, y + 30, SW),
        _line(58, y + 30, 82, y + 30, SW),
        _line(63, y + 36, 77, y + 36, SC),
        _line(68, y + 42, 72, y + 42, SC),
    )


def svg_grounding_sl_open(
    vb: str = "0 0 100 80", y: float = 30,
) -> str:
    px, py = 30, y
    import math
    arm_len = 35
    ex = px + arm_len * math.cos(math.radians(60))
    ey = py + arm_len * math.sin(math.radians(60))
    return _mk_svg(vb,
        _line(0, y, px, y),
        _filled_circle(px, py, 2),
        _line(px, py, ex, ey, SW),
        _line(58, y + 30, 82, y + 30, SW),
        _line(63, y + 36, 77, y + 36, SC),
        _line(68, y + 42, 72, y + 42, SC),
    )


# ── FUSES  (ГОСТ 2.728-74 / ГОСТ 2.721-74) ────────────────────
# Rectangle with diagonal line through it

def svg_fuse_sl(
    vb: str = "0 0 100 60", y: float = 30,
    bw: float = 30, bh: float = 20,
) -> str:
    x0 = (100 - bw) / 2
    return _mk_svg(vb,
        _line(0, y, x0, y),
        _rect(x0, y - bh / 2, bw, bh, SW),
        _line(x0, y + bh / 2, x0 + bw, y - bh / 2, SC),
        _line(x0 + bw, y, 100, y),
    )


def svg_fuse_holders_sl(
    vb: str = "0 0 100 60", y: float = 30,
) -> str:
    return _mk_svg(vb,
        _line(0, y, 30, y),
        _rect(30, y - 12, 15, 24, SW),
        _rect(55, y - 12, 15, 24, SW),
        _line(30, y - 8, 45, y + 8, SC),
        _line(55, y + 8, 70, y - 8, SC),
        _line(70, y, 100, y),
    )


# ── ARRESTERS / ОПН  (ГОСТ 2.742-68) ────────────────────────────

def svg_spark_gap_sl(
    vb: str = "0 0 100 60", y: float = 30,
) -> str:
    return _mk_svg(vb,
        _line(0, y, 35, y),
        _line(35, y, 50, y - 10, SW),
        _line(50, y + 10, 65, y, SW),
        _line(65, y, 100, y),
    )


def svg_opn_sl(
    vb: str = "0 0 100 60", y: float = 30,
    bw: float = 24, bh: float = 20,
) -> str:
    x0 = (100 - bw) / 2
    return _mk_svg(vb,
        _line(0, y, x0, y),
        _rect(x0, y - bh / 2, bw, bh, SW),
        _line(x0 + 4, y - bh / 4, x0 + bw - 4, y + bh / 4, SC),
        _line(x0 + 4, y + bh / 4, x0 + bw - 4, y - bh / 4, SC),
        _line(x0 + bw, y, 100, y),
    )


def svg_surge_capacitor_sl(
    vb: str = "0 0 100 60", y: float = 30,
) -> str:
    return _mk_svg(vb,
        _line(0, y, 42, y),
        _line(42, y - 10, 42, y + 10, SW),
        _line(58, y - 10, 58, y + 10, SW),
        _line(58, y, 100, y),
        _line(42, y, 58, y, SC),
    )


# ── TRANSFORMERS  (ГОСТ 2.723-68) ───────────────────────────────
# Two-winding: two overlapping circles
# Three-winding: three overlapping circles

def svg_xfmr_2w(
    vb: str = "0 0 100 100",
) -> str:
    r = 18
    cx1, cx2 = 40, 60
    cy = 50
    return _mk_svg(vb,
        _line(50, 0, 50, cy - r),
        _circle(cx1, cy, r, SW),
        _circle(cx2, cy, r, SW),
        _line(50, cy + r, 50, 100),
    )


def svg_xfmr_3w(
    vb: str = "0 0 100 120",
) -> str:
    r = 15
    cx1, cx2, cx3 = 32, 50, 68
    cy = 60
    return _mk_svg(vb,
        _line(50, 0, 50, cy - r),
        _circle(cx1, cy, r, SW),
        _circle(cx2, cy, r, SW),
        _circle(cx3, cy, r, SW),
        _line(50, cy + r, 50, 120),
    )


def svg_xfmr_2w_delta_wye(
    vb: str = "0 0 100 110",
) -> str:
    r = 18
    cx1, cx2 = 38, 62
    cy = 55
    return _mk_svg(vb,
        _line(50, 0, 50, cy - r),
        _circle(cx1, cy, r, SW),
        _circle(cx2, cy, r, SW),
        _path(f"M{cx2 - 5},{cy + r - 2} L{cx2},{cy + r + 4} L{cx2 + 5},{cy + r - 2}Z", SC),
        _line(50, cy + r, 50, 110),
    )


def svg_xfmr_autotransformer(
    vb: str = "0 0 100 110",
) -> str:
    r = 20
    cy = 55
    return _mk_svg(vb,
        _line(30, 0, 30, cy - r),
        _circle(50, cy, r, SW),
        _line(30, cy - r, 50, cy - r, SC),
        _line(30, cy, 50, cy + r, SC),
        _line(70, cy + r, 70, 110),
    )


# ── CT / ТТ  (ГОСТ 2.723-68) ────────────────────────────────────
# Two small circles on the bus line

def svg_ct_sl(
    vb: str = "0 0 100 60", y: float = 30,
    r: float = 10,
) -> str:
    gap = 3
    cx1 = 50 - r - gap / 2
    cx2 = 50 + r + gap / 2
    return _mk_svg(vb,
        _line(0, y, cx1 - r, y),
        _circle(cx1, y, r, SW),
        _circle(cx2, y, r, SW),
        _line(cx2 + r, y, 100, y),
    )


def svg_ct_normal(
    vb: str = "0 0 80 60", y: float = 30,
) -> str:
    r = 12
    return _mk_svg(vb,
        _line(0, y, 50 - r, y),
        _circle(50, y, r, SW),
        _line(50 + r, y, 80, y),
        _line(50, y + r, 50, 60),
        _circle(50, y + r + 8, 5, SW),
    )


# ── VT / ТН  (ГОСТ 2.723-68) ────────────────────────────────────

def svg_vt_sl(
    vb: str = "0 0 100 80", y: float = 25,
    r: float = 12,
) -> str:
    bx = 50
    return _mk_svg(vb,
        _line(0, y, bx - r, y),
        _circle(bx, y + 15, r, SW),
        _line(bx, y, bx, y + 15 - r),
        _line(bx, y + 15 + r, bx, y + 45),
        _line(bx - 8, y + 45, bx + 8, y + 45, SW),
        _line(bx - 5, y + 50, bx + 5, y + 50, SC),
        _line(bx - 2, y + 55, bx + 2, y + 55, SC),
        _line(bx + r, y, 100, y),
    )


def svg_vt_normal(
    vb: str = "0 0 60 80", x: float = 30,
) -> str:
    r = 12
    return _mk_svg(vb,
        _line(x, 0, x, 20 - r),
        _circle(x, 20, r, SW),
        _line(x, 20 + r, x, 80),
    )


# ── REACTOR / ШУНТИРУЮЩИЙ РЕАКТОР  (ГОСТ 2.723-68) ─────────────

def svg_reactor(
    vb: str = "0 0 100 60", y: float = 30,
) -> str:
    arcs = []
    n = 3
    arc_r = 7
    start_x = 50 - n * arc_r
    for i in range(n):
        ax = start_x + i * arc_r * 2 + arc_r
        arcs.append(
            f'<path d="M{ax - arc_r},{y} A{arc_r},{arc_r} 0 0,1 {ax + arc_r},{y}" '
            f'stroke="{BLACK}" stroke-width="{SW}" fill="none"/>'
        )
    return _mk_svg(vb,
        _line(0, y, start_x, y),
        "".join(arcs),
        _line(start_x + n * arc_r * 2, y, 100, y),
        _line(start_x, y + 12, start_x + n * arc_r * 2, y + 12, SC),
    )


def svg_shunt_reactor(
    vb: str = "0 0 100 60", y: float = 30,
) -> str:
    return svg_reactor(vb, y)


# ── MOTOR / GENERATOR  (ГОСТ 2.722-68) ──────────────────────────

def svg_machine(
    letter: str, vb: str = "0 0 80 80",
    cx: float = 40, cy: float = 40, r: float = 25,
) -> str:
    return _mk_svg(vb,
        _line(cx, 0, cx, cy - r),
        _circle(cx, cy, r, SW),
        _text(cx, cy, letter, 16),
        _line(cx, cy + r, cx, 80),
    )


def svg_generator_excited(
    letter: str, vb: str = "0 0 80 90",
    cx: float = 40, cy: float = 45, r: float = 22,
) -> str:
    return _mk_svg(vb,
        _line(cx, 0, cx, cy - r),
        _circle(cx, cy, r, SW),
        _text(cx, cy - 3, letter, 14),
        _line(cx - 6, cy + 8, cx + 6, cy + 8, SC),
        _line(cx, cy + r, cx, 90),
    )


# ── PASSIVE COMPONENTS  (ГОСТ 2.728-74) ─────────────────────────

def svg_resistor(
    vb: str = "0 0 100 40", y: float = 20,
    bw: float = 40, bh: float = 14,
) -> str:
    x0 = (100 - bw) / 2
    return _mk_svg(vb,
        _line(0, y, x0, y),
        _rect(x0, y - bh / 2, bw, bh, SW),
        _line(x0 + bw, y, 100, y),
    )


def svg_rheostat(
    vb: str = "0 0 100 50", y: float = 25,
) -> str:
    x0, bw, bh = 30, 40, 14
    return _mk_svg(vb,
        _line(0, y, x0, y),
        _rect(x0, y - bh / 2, bw, bh, SW),
        _line(x0 + bw, y, 100, y),
        _line(50, y - bh / 2, 50, y - bh / 2 - 10, SC),
        _path(f"M45,{y - bh / 2 - 10} L50,{y - bh / 2 - 5} L55,{y - bh / 2 - 10}", SC),
    )


def svg_var_resistor(
    vb: str = "0 0 100 50", y: float = 25,
) -> str:
    x0, bw, bh = 30, 40, 14
    return _mk_svg(vb,
        _line(0, y, x0, y),
        _rect(x0, y - bh / 2, bw, bh, SW),
        _line(x0 + bw, y, 100, y),
        _line(25, y + bh / 2 + 5, 75, y - bh / 2 - 5, SC),
    )


def svg_capacitor(
    vb: str = "0 0 100 50", y: float = 25,
    gap: float = 8, ph: float = 16,
) -> str:
    cx = 50
    return _mk_svg(vb,
        _line(0, y, cx - gap / 2, y),
        _line(cx - gap / 2, y - ph, cx - gap / 2, y + ph, SW),
        _line(cx + gap / 2, y - ph, cx + gap / 2, y + ph, SW),
        _line(cx + gap / 2, y, 100, y),
    )


def svg_electrolytic_capacitor(
    vb: str = "0 0 100 55", y: float = 28,
) -> str:
    cx = 50
    return _mk_svg(vb,
        _line(0, y, cx - 5, y),
        _line(cx - 5, y - 14, cx - 5, y + 14, SW),
        _line(cx + 5, y - 14, cx + 5, y + 14, SW),
        _line(cx + 5, y, 100, y),
        _text(cx, y - 18, "+", 5),
    )


def svg_inductor(
    vb: str = "0 0 100 60", y: float = 30,
) -> str:
    arcs = []
    n = 3
    arc_r = 7
    start_x = 50 - n * arc_r
    for i in range(n):
        ax = start_x + i * arc_r * 2 + arc_r
        arcs.append(
            f'<path d="M{ax - arc_r},{y} A{arc_r},{arc_r} 0 0,0 {ax + arc_r},{y}" '
            f'stroke="{BLACK}" stroke-width="{SW}" fill="none"/>'
        )
    return _mk_svg(vb,
        _line(0, y, start_x, y),
        "".join(arcs),
        _line(start_x + n * arc_r * 2, y, 100, y),
    )


# ── MEASURING INSTRUMENTS  (ГОСТ 2.729-68) ─────────────────────

def svg_instrument(
    letter: str, vb: str = "0 0 100 60", y: float = 30,
    r: float = 14,
) -> str:
    cx = 50
    return _mk_svg(vb,
        _line(0, y, cx - r, y),
        _circle(cx, y, r, SW),
        _text(cx, y, letter, 10),
        _line(cx + r, y, 100, y),
    )


# ── BUS BAR  (ГОСТ 2.702-2011) ──────────────────────────────────

def svg_bus(
    vb: str = "0 0 100 20", y: float = 10,
    sw: float = 2.5,
) -> str:
    return _mk_svg(vb,
        _line(0, y, 100, y, sw),
    )


def svg_bus_tap(
    vb: str = "0 0 60 60", x: float = 30, y: float = 10,
    sw: float = 2.5,
) -> str:
    return _mk_svg(vb,
        _line(0, y, 60, y, sw),
        _line(x, y, x, 60, SW),
    )


def svg_bus_node(
    vb: str = "0 0 40 40", cx: float = 20, cy: float = 20,
) -> str:
    return _mk_svg(vb,
        _filled_circle(cx, cy, 3),
    )


# ── GROUND  (ГОСТ 2.756-76) ─────────────────────────────────────

def svg_ground(
    vb: str = "0 0 40 50", x: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(x, 0, x, 15),
        _line(6, 15, 34, 15, SW),
        _line(11, 22, 29, 22, SW),
        _line(16, 29, 24, 29, SW),
    )


def svg_frame_ground(
    vb: str = "0 0 40 50", x: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(x, 0, x, 15),
        _line(6, 15, 34, 15, SW),
        _line(15, 20, 25, 25, SC),
        _line(25, 20, 15, 25, SC),
    )


def svg_antenna_ground(
    vb: str = "0 0 40 55", x: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(x, 0, x, 15),
        _line(6, 15, 34, 15, SW),
        _line(10, 22, 30, 22, SW),
        _line(14, 29, 26, 29, SW),
        _line(18, 36, 22, 36, SW),
    )


# ── TERMINALS  (ГОСТ 2.721-74) ──────────────────────────────────

def svg_terminal(
    vb: str = "0 0 30 30", cx: float = 15, cy: float = 15,
) -> str:
    return _mk_svg(vb,
        _filled_circle(cx, cy, 3),
    )


def svg_terminal_board(
    vb: str = "0 0 100 30", y: float = 15,
) -> str:
    parts = ""
    for i in range(5):
        tx = 10 + i * 20
        parts += _filled_circle(tx, y, 3)
    return _mk_svg(vb, parts)


# ── CONTACTS  (ГОСТ 2.759-82 / ГОСТ 2.755-87) ──────────────────

def svg_no_contact_closed(
    vb: str = "0 0 80 60", y: float = 40,
) -> str:
    px, py = 15, y
    cx, cy = 65, y
    return _mk_svg(vb,
        _filled_circle(px, py, 2.5),
        _filled_circle(cx, cy, 2.5),
        _line(px, py, cx, cy, SW),
    )


def svg_no_contact_open(
    vb: str = "0 0 80 60", y: float = 40,
) -> str:
    px, py = 15, y
    cx, cy = 65, y
    arm_len = 38
    import math
    ex = px + arm_len * math.cos(math.radians(35))
    ey = py - arm_len * math.sin(math.radians(35))
    return _mk_svg(vb,
        _filled_circle(px, py, 2.5),
        _filled_circle(cx, cy, 2.5),
        _line(px, py, ex, ey, SW),
    )


def svg_nc_contact_closed(
    vb: str = "0 0 80 60", y: float = 40,
) -> str:
    px, py = 15, y
    cx, cy = 65, y
    import math
    arm_len = 38
    ex = px + arm_len * math.cos(math.radians(35))
    ey = py - arm_len * math.sin(math.radians(35))
    return _mk_svg(vb,
        _filled_circle(px, py, 2.5),
        _filled_circle(cx, cy, 2.5),
        _line(px, py, ex, ey, SW),
        _line(cx - 4, cy + 4, cx + 4, cy - 4, SC),
    )


def svg_nc_contact_open(
    vb: str = "0 0 80 60", y: float = 40,
) -> str:
    px, py = 15, y
    cx, cy = 65, y
    return _mk_svg(vb,
        _filled_circle(px, py, 2.5),
        _filled_circle(cx, cy, 2.5),
        _line(px, py, cx, cy, SW),
        _line(cx - 4, cy + 4, cx + 4, cy - 4, SC),
    )


def svg_changeover_closed(
    vb: str = "0 0 80 80", y1: float = 25, y2: float = 55,
    yc: float = 40,
) -> str:
    px, py = 15, yc
    cx1, cy1 = 65, y1
    cx2, cy2 = 65, y2
    return _mk_svg(vb,
        _filled_circle(px, py, 2.5),
        _filled_circle(cx1, cy1, 2.5),
        _filled_circle(cx2, cy2, 2.5),
        _line(px, py, cx1, cy1, SW),
        _line(px, py, 15, 0, SC),
        _line(cx1, cy1, 80, y1, SC),
        _line(cx2, cy2, 80, y2, SC),
    )


def svg_changeover_open(
    vb: str = "0 0 80 80", y1: float = 25, y2: float = 55,
    yc: float = 40,
) -> str:
    px, py = 15, yc
    cx1, cy1 = 65, y1
    cx2, cy2 = 65, y2
    arm_len = 38
    import math
    angle = math.atan2(y1 - yc, 65 - 15)
    ex = px + arm_len * math.cos(angle)
    ey = py + arm_len * math.sin(angle)
    return _mk_svg(vb,
        _filled_circle(px, py, 2.5),
        _filled_circle(cx1, cy1, 2.5),
        _filled_circle(cx2, cy2, 2.5),
        _line(px, py, ex, ey, SW),
        _line(px, py, 15, 0, SC),
        _line(cx1, cy1, 80, y1, SC),
        _line(cx2, cy2, 80, y2, SC),
    )


# ── RELAY / CONTACTOR COILS  (ГОСТ 2.759-82) ───────────────────

def svg_relay_coil(
    vb: str = "0 0 40 80", x: float = 20,
    bw: float = 20, bh: float = 40,
) -> str:
    return _mk_svg(vb,
        _line(x, 0, x, 20),
        _rect(x - bw / 2, 20, bw, bh, SW),
        _line(x, 20 + bh, x, 80),
    )


def svg_contactor_coil(
    vb: str = "0 0 40 80", x: float = 20,
    bw: float = 20, bh: float = 40,
) -> str:
    return svg_relay_coil(vb, x, bw, bh)


# ── OVERCURRENT RELAY  (ГОСТ 2.759-82) ──────────────────────────

def svg_relay_overcurrent(
    vb: str = "0 0 40 80", x: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(x, 0, x, 20),
        _rect(x - 10, 20, 20, 40, SW),
        _text(x, 40, "I>", 7),
        _line(x, 60, x, 80),
    )


def svg_relay_diff(
    vb: str = "0 0 40 80", x: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(x, 0, x, 20),
        _rect(x - 10, 20, 20, 40, SW),
        _text(x, 40, "ΔI", 7),
        _line(x, 60, x, 80),
    )


def svg_relay_distance(
    vb: str = "0 0 40 80", x: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(x, 0, x, 20),
        _rect(x - 10, 20, 20, 40, SW),
        _text(x, 40, "Z", 7),
        _line(x, 60, x, 80),
    )


def svg_relay_earth_fault(
    vb: str = "0 0 40 80", x: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(x, 0, x, 20),
        _rect(x - 10, 20, 20, 40, SW),
        _text(x, 40, "3I0", 6),
        _line(x, 60, x, 80),
    )


def svg_relay_thermal(
    vb: str = "0 0 40 80", x: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(x, 0, x, 20),
        _rect(x - 10, 20, 20, 40, SW),
        _text(x, 40, "T", 7),
        _line(x, 60, x, 80),
    )


def svg_relay_pressure(
    vb: str = "0 0 40 80", x: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(x, 0, x, 20),
        _rect(x - 10, 20, 20, 40, SW),
        _text(x, 40, "P", 7),
        _line(x, 60, x, 80),
    )


def svg_relay_overload(
    vb: str = "0 0 40 80", x: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(x, 0, x, 20),
        _rect(x - 10, 20, 20, 40, SW),
        _text(x, 40, "I>", 7),
        _line(x, 60, x, 80),
    )


def svg_relay_buchholz(
    vb: str = "0 0 40 80", x: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(x, 0, x, 20),
        _rect(x - 10, 20, 20, 40, SW),
        _text(x, 40, "B", 7),
        _line(x, 60, x, 80),
    )


def svg_relay_gas(
    vb: str = "0 0 40 80", x: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(x, 0, x, 20),
        _rect(x - 10, 20, 20, 40, SW),
        _text(x, 40, "G", 7),
        _line(x, 60, x, 80),
    )


# ── CABLE  (ГОСТ 2.721-74) ──────────────────────────────────────

def svg_cable(
    vb: str = "0 0 100 40", y: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(0, y, 100, y),
        _line(40, y - 8, 40, y + 8, SC),
        _line(50, y - 8, 50, y + 8, SC),
        _line(60, y - 8, 60, y + 8, SC),
    )


def svg_cable_pair(
    vb: str = "0 0 100 40", y: float = 15,
) -> str:
    return _mk_svg(vb,
        _line(0, y, 100, y),
        _line(0, y + 10, 100, y + 10),
        _line(45, y - 6, 45, y + 16, SC),
        _line(55, y - 6, 55, y + 16, SC),
    )


def svg_cable_shielded(
    vb: str = "0 0 100 50", y: float = 25,
) -> str:
    return _mk_svg(vb,
        _line(0, y, 100, y),
        _rect(30, y - 10, 40, 20, SC),
    )


def svg_cable_joint(
    vb: str = "0 0 100 40", y: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(0, y, 35, y),
        _rect(35, y - 8, 30, 16, SC),
        _line(65, y, 100, y),
    )


def svg_cable_terminal(
    vb: str = "0 0 60 40", y: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(0, y, 25, y),
        _rect(25, y - 6, 15, 12, SW),
        _filled_circle(50, y, 3),
    )


# ── ENCLOSURE  (ГОСТ 2.721-74) ──────────────────────────────────

def svg_enclosure(
    vb: str = "0 0 100 80",
) -> str:
    return _mk_svg(vb,
        _rect(5, 5, 90, 70, SC),
    )


def svg_switchgear_cell(
    vb: str = "0 0 100 120",
) -> str:
    return _mk_svg(vb,
        _rect(5, 5, 90, 110, SC),
        _line(5, 30, 95, 30, SC),
        _line(5, 60, 95, 60, SC),
        _line(5, 90, 95, 90, SC),
    )


def svg_withdrawable_element(
    vb: str = "0 0 100 80",
) -> str:
    return _mk_svg(vb,
        _rect(5, 5, 90, 70, SC),
        _line(10, 5, 10, 75, SC),
    )


# ── BATTERY  (ГОСТ 2.721-74) ────────────────────────────────────

def svg_battery(
    vb: str = "0 0 100 60", y: float = 30,
) -> str:
    return _mk_svg(vb,
        _line(0, y, 35, y),
        _line(35, y - 12, 35, y + 12, SW),
        _line(42, y - 6, 42, y + 6, SC),
        _line(49, y - 12, 49, y + 12, SW),
        _line(56, y - 6, 56, y + 6, SC),
        _line(63, y - 12, 63, y + 12, SW),
        _line(63, y, 100, y),
    )


def svg_battery_cell(
    vb: str = "0 0 60 60", y: float = 30,
) -> str:
    return _mk_svg(vb,
        _line(0, y, 22, y),
        _line(22, y - 10, 22, y + 10, SW),
        _line(30, y - 5, 30, y + 5, SC),
        _line(30, y, 60, y),
    )


def svg_accumulator(
    vb: str = "0 0 100 60", y: float = 30,
) -> str:
    return _mk_svg(vb,
        _line(0, y, 30, y),
        _line(30, y - 12, 30, y + 12, SW),
        _line(38, y - 6, 38, y + 6, SC),
        _line(46, y - 12, 46, y + 12, SW),
        _line(54, y - 6, 54, y + 6, SC),
        _line(62, y - 12, 62, y + 12, SW),
        _line(62, y, 100, y),
        _text(46, y - 18, "+", 6),
    )


# ── CABLE ACCESSORIES  ──────────────────────────────────────────

def svg_cable_gland(
    vb: str = "0 0 50 40", x: float = 25, y: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(0, y, 15, y),
        _rect(15, y - 8, 20, 16, SW),
        _line(35, y, 50, y),
    )


def svg_cable_duct(
    vb: str = "0 0 100 40", y: float = 20,
) -> str:
    return _mk_svg(vb,
        _line(0, y - 6, 100, y - 6, SC),
        _line(0, y + 6, 100, y + 6, SC),
        _line(0, y, 100, y),
    )


# ── LIGHTNING / EARTHING ────────────────────────────────────────

def svg_lightning_arrester(
    vb: str = "0 0 100 80", y: float = 25,
) -> str:
    return _mk_svg(vb,
        _line(0, y, 35, y),
        _line(35, y, 50, y - 12, SW),
        _line(50, y + 12, 65, y, SW),
        _line(65, y, 100, y),
        _line(50, y + 12, 50, 65),
        _line(38, 65, 62, 65, SW),
        _line(43, 71, 57, 71, SC),
    )


def svg_earthing_device(
    vb: str = "0 0 60 80", x: float = 30,
) -> str:
    return _mk_svg(vb,
        _line(x, 0, x, 20),
        _line(x - 10, 20, x + 10, 20, SW),
        _line(x, 20, x, 40),
        _line(x - 15, 40, x + 15, 40, SW),
        _line(x - 10, 47, x + 10, 47, SC),
        _line(x - 5, 54, x + 5, 54, SC),
    )


# ── SWITCHING DEVICE — STATE MAPS ────────────────────────────────

def _cb_states() -> list[dict]:
    return [
        {"id": "closed", "name": "Closed", "alternate_svg": svg_cb_normal_closed()},
        {"id": "open", "name": "Open", "alternate_svg": svg_cb_normal_open()},
        {"id": "blown", "name": "Blown", "alternate_svg": svg_cb_normal_blown()},
    ]


def _ds_states() -> list[dict]:
    return [
        {"id": "closed", "name": "Closed", "alternate_svg": svg_ds_normal_closed()},
        {"id": "open", "name": "Open", "alternate_svg": svg_ds_normal_open()},
    ]


def _no_contact_states() -> list[dict]:
    return [
        {"id": "open", "name": "Open", "alternate_svg": svg_no_contact_open()},
        {"id": "closed", "name": "Closed", "alternate_svg": svg_no_contact_closed()},
    ]


def _nc_contact_states() -> list[dict]:
    return [
        {"id": "closed", "name": "Closed", "alternate_svg": svg_nc_contact_closed()},
        {"id": "open", "name": "Open", "alternate_svg": svg_nc_contact_open()},
    ]


def _changeover_states() -> list[dict]:
    return [
        {"id": "pos1", "name": "Position 1", "alternate_svg": svg_changeover_closed()},
        {"id": "pos2", "name": "Position 2", "alternate_svg": svg_changeover_open()},
    ]


# ── CONVENIENCE BUILDERS  (imported by _build_symbols) ────────────

def _cb(sid: str, name: str, cat: str) -> dict:
    return _sym(
        sid, sid, name, cat,
        "ГОСТ 2.755-87", "fig.1",
        "0 0 100 60", 100, 60,
        [_term("t1", 0, 50), _term("t2", 100, 50)],
        svg_cb_sl_closed(),
        letter="QF",
        interactive=True,
        def_state="closed",
        states=_cb_states(),
    )


def _ds(sid: str, name: str, cat: str) -> dict:
    return _sym(
        sid, sid, name, cat,
        "ГОСТ 2.755-87", "fig.2",
        "0 0 100 60", 100, 60,
        [_term("t1", 0, 50), _term("t2", 100, 50)],
        svg_ds_sl_closed(),
        letter="QS",
        interactive=True,
        def_state="closed",
        states=_ds_states(),
    )


# ══════════════════════════════════════════════════════════════════
#  CATEGORY DEFINITIONS
# ══════════════════════════════════════════════════════════════════

CATEGORIES: list[dict] = [
    {"id": "switching", "name": "Switching devices (circuit breakers)",
     "gost": "ГОСТ 2.755-87", "description": "Автоматические выключатели",
     "svg_preview": svg_cb_sl_closed()},
    {"id": "disconnector", "name": "Disconnectors",
     "gost": "ГОСТ 2.755-87", "description": "Разъединители и заземляющие ножи",
     "svg_preview": svg_ds_sl_closed()},
    {"id": "contactor", "name": "Contactors",
     "gost": "ГОСТ 2.759-82", "description": "Контакторы и пускатели",
     "svg_preview": svg_contactor_coil()},
    {"id": "switch", "name": "Manual switches",
     "gost": "ГОСТ 2.755-87", "description": "Ручные коммутационные аппараты",
     "svg_preview": svg_ds_sl_closed()},
    {"id": "fuse", "name": "Fuses",
     "gost": "ГОСТ 2.728-74", "description": "Предохранители",
     "svg_preview": svg_fuse_sl()},
    {"id": "arrester", "name": "Arresters and surge arresters",
     "gost": "ГОСТ 2.742-68", "description": "Разрядники и ОПН",
     "svg_preview": svg_opn_sl()},
    {"id": "transformer", "name": "Transformers",
     "gost": "ГОСТ 2.723-68", "description": "Силовые трансформаторы и автотрансформаторы",
     "svg_preview": svg_xfmr_2w()},
    {"id": "ct_vt", "name": "Instrument transformers",
     "gost": "ГОСТ 2.723-68", "description": "Трансформаторы тока и напряжения",
     "svg_preview": svg_ct_sl()},
    {"id": "relay", "name": "Relay protection",
     "gost": "ГОСТ 2.759-82", "description": "Реле и устройства РЗА",
     "svg_preview": svg_relay_overcurrent()},
    {"id": "instruments", "name": "Measuring instruments",
     "gost": "ГОСТ 2.729-68", "description": "Измерительные приборы",
     "svg_preview": svg_instrument("A")},
    {"id": "machines", "name": "Electrical machines",
     "gost": "ГОСТ 2.722-68", "description": "Генераторы, двигатели",
     "svg_preview": svg_machine("M")},
    {"id": "passive", "name": "Passive components",
     "gost": "ГОСТ 2.728-74", "description": "Резисторы, конденсаторы, катушки",
     "svg_preview": svg_resistor()},
    {"id": "reactor", "name": "Reactors",
     "gost": "ГОСТ 2.723-68", "description": "Шунтирующие реакторы",
     "svg_preview": svg_reactor()},
    {"id": "bus_line", "name": "Bus bars and lines",
     "gost": "ГОСТ 2.702-2011", "description": "Шины и соединительные линии",
     "svg_preview": svg_bus()},
    {"id": "terminals", "name": "Terminals and connectors",
     "gost": "ГОСТ 2.721-74", "description": "Зажимы и клеммы",
     "svg_preview": svg_terminal()},
    {"id": "ground", "name": "Earthing",
     "gost": "ГОСТ 2.756-76", "description": "Заземление",
     "svg_preview": svg_ground()},
    {"id": "enclosure", "name": "Enclosures and switchgear",
     "gost": "ГОСТ 2.721-74", "description": "Корпуса и ячейки КРУ",
     "svg_preview": svg_enclosure()},
    {"id": "battery", "name": "Batteries and power supplies",
     "gost": "ГОСТ 2.721-74", "description": "Аккумуляторные батареи",
     "svg_preview": svg_battery()},
    {"id": "cable", "name": "Cables and wiring",
     "gost": "ГОСТ 2.721-74", "description": "Кабели и провода",
     "svg_preview": svg_cable()},
    {"id": "cable_accessories", "name": "Cable accessories",
     "gost": "ГОСТ 2.721-74", "description": "Кабельные муфты и вводы",
     "svg_preview": svg_cable_gland()},
    {"id": "lightning", "name": "Lightning and earthing protection",
     "gost": "ГОСТ 2.742-68", "description": "Молниезащита и заземляющие устройства",
     "svg_preview": svg_lightning_arrester()},
    {"id": "contact_types", "name": "Contact types",
     "gost": "ГОСТ 2.759-82", "description": "Контакты замыкающие, размыкающие, переключающие",
     "svg_preview": svg_no_contact_open()},
    {"id": "signaling", "name": "Signaling devices",
     "gost": "ГОСТ 2.727-68", "description": "Лампы, индикаторы, сигнализация",
     "svg_preview": svg_instrument("H")},
    {"id": "protection_devices", "name": "Protection devices",
     "gost": "ГОСТ 2.728-74", "description": "Устройства защиты",
     "svg_preview": svg_fuse_sl()},
    {"id": "motors", "name": "Motors and starters",
     "gost": "ГОСТ 2.722-68", "description": "Электродвигатели и пусковые устройства",
     "svg_preview": svg_machine("M")},
]
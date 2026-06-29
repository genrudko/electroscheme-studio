#!/usr/bin/env python3
"""Build a clean interactive review page for parametric busbars.

This page is for interaction, not static snapshot regression. It regenerates
busbar previews from the parametric model and places each preview into one
clean SVG coordinate system:

    grid == busbar == labels == guides == drag coordinates

This avoids nested snapshot offsets and makes guide positioning predictable.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ReviewCase:
    id: str
    title: str
    description: str
    params: dict[str, Any]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def repo_root_from_visual_dir(visual_dir: Path) -> Path:
    resolved = visual_dir.resolve()
    if resolved.name == "parametric_busbar" and resolved.parent.name == "visual_checks":
        return resolved.parent.parent
    return Path.cwd().resolve()


def load_backend(repo_root: Path) -> tuple[Any, Any]:
    backend_root = repo_root / "backend"
    if str(backend_root) not in sys.path:
        sys.path.insert(0, str(backend_root))

    from app.core.parametric_busbar import generate_busbar_preview
    from app.schemas.parametric_symbols import BusbarPreviewRequest

    return generate_busbar_preview, BusbarPreviewRequest


def review_cases() -> list[ReviewCase]:
    base: dict[str, Any] = {
        "id": "param_busbar",
        "name_ru": "1С 10 кВ",
        "voltage_kv": 10,
        "length": 260,
        "fit_length_to_slots": True,
        "thickness_mm": 12,
        "connection_spacing": 48,
        "end_slot_offset": 12,
        "slot_diameter": 8,
        "margin": 24,
        "bay_depth": 90,
        "bay_numbering_enabled": True,
        "bay_numbering_prefix": "Яч. ",
        "bay_numbering_style": "number_only",
        "bay_numbering_step": 1,
        "bay_label_offset": 16,
        "bay_label_both_side_separate_rows": True,
        "bay_label_default_rotation_deg": 0,
        "bay_label_overrides": {},
        "bus_label": "1С 10 кВ",
        "bus_label_position": "auto",
        "bus_label_gap": 34,
        "bus_label_offset_x": 0,
        "bus_label_offset_y": 0,
        "bus_label_rotation_mode": "auto",
        "bus_label_rotation_deg": 0,
    }

    def make(case_id: str, title: str, description: str, **overrides: Any) -> ReviewCase:
        params = dict(base)
        params.update(overrides)
        params["id"] = case_id
        return ReviewCase(case_id, title, description, params)

    return [
        make(
            "01_horizontal_bottom_numbered",
            "Horizontal busbar — bottom slots, numbered above",
            "Clean model canvas: bottom slots, bay numbers and bus caption share one coordinate system.",
            connection_count=8,
            connection_side="bottom",
            orientation="horizontal",
            bay_numbering_start=1,
        ),
        make(
            "02_horizontal_top_numbered",
            "Horizontal busbar — top slots, numbered above",
            "Checks top slots, grid alignment and guide alignment with labels 9–16.",
            connection_count=8,
            connection_side="top",
            orientation="horizontal",
            bay_numbering_start=9,
        ),
        make(
            "03_horizontal_both_sides",
            "Horizontal busbar — both sides",
            "Checks separate upper/lower number rows for both-side busbar.",
            connection_count=6,
            connection_side="both",
            orientation="horizontal",
            bay_numbering_start=21,
        ),
        make(
            "04_vertical_right_numbered",
            "Vertical busbar — right slots",
            "Checks vertical orientation with right-side slots and labels.",
            connection_count=7,
            connection_side="bottom",
            orientation="vertical",
            bay_numbering_start=1,
            bus_label_rotation_mode="manual",
            bus_label_rotation_deg=-90,
        ),
        make(
            "05_vertical_left_numbered",
            "Vertical busbar — left slots",
            "Checks vertical orientation with left-side slots and labels.",
            connection_count=7,
            connection_side="top",
            orientation="vertical",
            bay_numbering_start=1,
            bus_label_rotation_mode="manual",
            bus_label_rotation_deg=-90,
        ),
        make(
            "06_numbering_disabled",
            "Horizontal busbar — numbering disabled",
            "Checks that slots remain available without bay number labels.",
            connection_count=5,
            connection_side="bottom",
            orientation="horizontal",
            bay_numbering_enabled=False,
        ),
        make(
            "07_dense_16_slots",
            "Horizontal busbar — dense 16 slots",
            "Checks dense slot spacing and guide behavior on a crowded section.",
            connection_count=16,
            connection_side="bottom",
            orientation="horizontal",
            connection_spacing=24,
            bay_numbering_start=1,
            bus_label_gap=28,
        ),
    ]


def svg_card(case: ReviewCase, preview: Any) -> str:
    view_box = preview.viewBox
    width = float(view_box["width"])
    height = float(view_box["height"])
    grid_id = "grid_" + html.escape(case.id)
    title = html.escape(case.title)
    description = html.escape(case.description)
    labels = ", ".join(slot.label for slot in preview.bay_slots if slot.label)
    labels_html = html.escape(labels)

    svg = f"""
<svg
  class="review-svg"
  data-clean-canvas="true"
  data-case-id="{html.escape(case.id)}"
  viewBox="0 0 {width:.6g} {height:.6g}"
  role="img"
  aria-label="{title}"
>
  <defs>
    <pattern id="{grid_id}" width="6" height="6" patternUnits="userSpaceOnUse">
      <path d="M 6 0 L 0 0 0 6" fill="none" stroke="#e5e7eb" stroke-width="0.45" />
    </pattern>
  </defs>
  <rect class="grid-fill" x="0" y="0" width="{width:.6g}" height="{height:.6g}" fill="url(#{grid_id})" />
  <rect class="drawing-viewport" x="0.5" y="0.5" width="{max(width - 1, 1):.6g}" height="{max(height - 1, 1):.6g}" fill="none" stroke="#cbd5e1" stroke-width="1" rx="8" />
  <g class="drawing-layer">
{preview.svg_fragment}
  </g>
</svg>"""

    return f"""<article class="card" data-case-id="{html.escape(case.id)}">
  <header>
    <h2>{title}</h2>
    <p>{description}</p>
    <p class="meta">terminals={len(preview.terminals)}; bay_slots={len(preview.bay_slots)}; viewBox={width:.0f}x{height:.0f}; grid=6</p>
    <p class="labels">{labels_html}</p>
  </header>
  <div class="svg-wrap">{svg}</div>
  <p class="drag-status">Drag text. Blue guides use the same coordinate system as the grid and drawing.</p>
</article>"""


def page_html(cards_html: str) -> str:
    template = """<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>Clean interactive busbar review — ElectroScheme Studio</title>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; background: #f5f6f8; color: #111827; }
    header.page { position: sticky; top: 0; z-index: 10; background: #111827; color: white; padding: 16px 22px; box-shadow: 0 2px 12px rgba(0,0,0,.2); }
    header.page h1 { margin: 0 0 6px; font-size: 22px; }
    header.page p { margin: 0; color: #cbd5e1; }
    main { padding: 18px; display: grid; grid-template-columns: repeat(auto-fill, minmax(620px, 1fr)); gap: 16px; }
    .card { background: white; border: 1px solid #e5e7eb; border-radius: 14px; padding: 14px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
    .card h2 { margin: 0 0 6px; font-size: 17px; }
    .card p { margin: 6px 0; color: #4b5563; }
    .meta { font-size: 12px; font-weight: 700; }
    .labels { font-size: 12px; color: #1d4ed8; }
    .svg-wrap { width: 100%; min-height: 300px; border: 1px solid #e5e7eb; border-radius: 10px; background: #fff; overflow: auto; }
    .review-svg { width: 100%; height: auto; display: block; --busbar-color: #6d0ad6; --slot-stroke: #ffffff; --label-color: #111111; }
    [data-role="bus-label"], [data-role="bay-label"] { cursor: grab; user-select: none; }
    [data-role="bus-label"].selected, [data-role="bay-label"].selected {
      paint-order: stroke;
      stroke: rgba(37, 99, 235, 0.35);
      stroke-width: 3;
    }
    .drag-status { font-size: 12px; color: #64748b; }
    .toolbar {
      position: fixed;
      right: 18px;
      bottom: 18px;
      z-index: 100;
      width: 300px;
      padding: 12px;
      border-radius: 14px;
      background: #111827;
      color: white;
      box-shadow: 0 12px 28px rgba(0,0,0,.25);
    }
    .toolbar h2 { margin: 0 0 8px; font-size: 15px; }
    .toolbar p { margin: 0 0 10px; color: #cbd5e1; font-size: 12px; }
    .toolbar button {
      margin: 3px;
      padding: 6px 9px;
      border: 0;
      border-radius: 999px;
      background: #2563eb;
      color: white;
      font-weight: 700;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <header class="page">
    <h1>Clean interactive busbar review</h1>
    <p>One SVG coordinate system per card: grid, busbar, labels, guides and drag math are aligned.</p>
  </header>
  <main>
    __CARDS__
  </main>
  <aside class="toolbar">
    <h2>Text tools</h2>
    <p id="selectedText">Selected: none</p>
    <button data-rotate="0">0°</button>
    <button data-rotate="90">+90°</button>
    <button data-rotate="-90">-90°</button>
    <button data-rotate="180">180°</button>
  </aside>
  <script>
    let selectedText = null;
    const snapTolerance = 6;
    const gridStep = 6;

    function clientToSvgPoint(svg, event) {
      const point = svg.createSVGPoint();
      point.x = event.clientX;
      point.y = event.clientY;
      const ctm = svg.getScreenCTM();
      if (!ctm) return null;
      return point.matrixTransform(ctm.inverse());
    }

    function unique(values) {
      return [...new Set(values.map((value) => Math.round(value * 10) / 10))].sort((a, b) => a - b);
    }

    function bboxCenter(element) {
      const box = element.getBBox();
      return { x: box.x + box.width / 2, y: box.y + box.height / 2 };
    }

    function textAnchor(element) {
      return {
        x: Number(element.getAttribute('x') || '0') || 0,
        y: Number(element.getAttribute('y') || '0') || 0,
      };
    }

    function setTextPosition(target, x, y) {
      const rotation = Number(target.getAttribute('data-rotation') || '0') || 0;
      const rx = Math.round(x * 10) / 10;
      const ry = Math.round(y * 10) / 10;
      target.setAttribute('x', String(rx));
      target.setAttribute('y', String(ry));
      target.setAttribute('transform', `rotate(${rotation} ${rx} ${ry})`);
    }

    function selectTarget(target) {
      document.querySelectorAll('.selected').forEach((item) => item.classList.remove('selected'));
      selectedText = target;
      if (target) {
        target.classList.add('selected');
        const role = target.getAttribute('data-role') || 'text';
        const id = target.getAttribute('data-bay-slot-id') || role;
        document.getElementById('selectedText').textContent = `Selected: ${id}`;
      } else {
        document.getElementById('selectedText').textContent = 'Selected: none';
      }
    }

    function collectGuides(svg, target) {
      const vertical = [];
      const horizontal = [];
      const vb = svg.viewBox.baseVal;

      svg.querySelectorAll('circle').forEach((circle) => {
        const cx = Number(circle.getAttribute('cx'));
        const cy = Number(circle.getAttribute('cy'));
        if (Number.isFinite(cx)) vertical.push(cx);
        if (Number.isFinite(cy)) horizontal.push(cy);
      });

      svg.querySelectorAll('rect').forEach((rect) => {
        if (rect.classList.contains('grid-fill') || rect.classList.contains('drawing-viewport')) return;
        const x = Number(rect.getAttribute('x'));
        const y = Number(rect.getAttribute('y'));
        const width = Number(rect.getAttribute('width'));
        const height = Number(rect.getAttribute('height'));
        if (!Number.isFinite(x) || !Number.isFinite(y) || !Number.isFinite(width) || !Number.isFinite(height)) return;
        vertical.push(x, x + width / 2, x + width);
        horizontal.push(y, y + height / 2, y + height);
      });

      svg.querySelectorAll('text').forEach((text) => {
        if (text === target) return;
        const center = bboxCenter(text);
        vertical.push(center.x);
        horizontal.push(center.y);
      });

      for (let x = vb.x; x <= vb.x + vb.width; x += gridStep) vertical.push(x);
      for (let y = vb.y; y <= vb.y + vb.height; y += gridStep) horizontal.push(y);

      return { vertical: unique(vertical), horizontal: unique(horizontal) };
    }

    function snap(value, guides) {
      let best = null;
      let bestDistance = Infinity;
      for (const guide of guides) {
        const distance = Math.abs(value - guide);
        if (distance < bestDistance) {
          bestDistance = distance;
          best = guide;
        }
      }
      return best !== null && bestDistance <= snapTolerance ? { value: best, guide: best } : { value, guide: null };
    }

    function ensureGuideLayer(svg) {
      let layer = svg.querySelector('[data-role="alignment-guides"]');
      if (!layer) {
        layer = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        layer.setAttribute('data-role', 'alignment-guides');
        layer.setAttribute('pointer-events', 'none');
        svg.appendChild(layer);
      }
      return layer;
    }

    function addLine(layer, attrs) {
      const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      for (const [key, value] of Object.entries(attrs)) line.setAttribute(key, String(value));
      layer.appendChild(line);
    }

    function drawGuides(svg, x, y, snapX, snapY) {
      const layer = ensureGuideLayer(svg);
      layer.innerHTML = '';
      const vb = svg.viewBox.baseVal;
      const base = { stroke: '#64748b', 'stroke-width': '0.8', 'stroke-dasharray': '3 3', opacity: '0.55' };
      const highlight = { stroke: '#2563eb', 'stroke-width': '1.4', 'stroke-dasharray': 'none', opacity: '0.9' };
      addLine(layer, { x1: x, y1: vb.y, x2: x, y2: vb.y + vb.height, ...base });
      addLine(layer, { x1: vb.x, y1: y, x2: vb.x + vb.width, y2: y, ...base });
      if (snapX !== null) addLine(layer, { x1: snapX, y1: vb.y, x2: snapX, y2: vb.y + vb.height, ...highlight });
      if (snapY !== null) addLine(layer, { x1: vb.x, y1: snapY, x2: vb.x + vb.width, y2: snapY, ...highlight });
    }

    function clearGuides(svg) {
      svg.querySelector('[data-role="alignment-guides"]')?.remove();
    }

    document.querySelectorAll('.toolbar button[data-rotate]').forEach((button) => {
      button.addEventListener('click', () => {
        if (!selectedText) return;
        const rotation = Number(button.getAttribute('data-rotate') || '0') || 0;
        selectedText.setAttribute('data-rotation', String(rotation));
        const anchor = textAnchor(selectedText);
        selectedText.setAttribute('transform', `rotate(${rotation} ${anchor.x} ${anchor.y})`);
      });
    });

    document.addEventListener('pointerdown', (event) => {
      const target = event.target.closest('[data-role="bus-label"], [data-role="bay-label"]');
      if (!target) return;
      const svg = target.ownerSVGElement;
      if (!svg) return;

      event.preventDefault();
      selectTarget(target);

      const start = clientToSvgPoint(svg, event);
      if (!start) return;

      const baseAnchor = textAnchor(target);
      const baseCenter = bboxCenter(target);
      const guides = collectGuides(svg, target);
      const pointerId = event.pointerId;
      target.setPointerCapture?.(pointerId);

      const move = (moveEvent) => {
        if (moveEvent.pointerId !== pointerId) return;
        const current = clientToSvgPoint(svg, moveEvent);
        if (!current) return;

        const rawCenterX = baseCenter.x + current.x - start.x;
        const rawCenterY = baseCenter.y + current.y - start.y;
        const snappedX = snap(rawCenterX, guides.vertical);
        const snappedY = snap(rawCenterY, guides.horizontal);
        const dx = snappedX.value - baseCenter.x;
        const dy = snappedY.value - baseCenter.y;

        setTextPosition(target, baseAnchor.x + dx, baseAnchor.y + dy);
        drawGuides(svg, snappedX.value, snappedY.value, snappedX.guide, snappedY.guide);
      };

      const up = (upEvent) => {
        if (upEvent.pointerId !== pointerId) return;
        target.releasePointerCapture?.(pointerId);
        clearGuides(svg);
        window.removeEventListener('pointermove', move);
        window.removeEventListener('pointerup', up);
      };

      window.addEventListener('pointermove', move);
      window.addEventListener('pointerup', up);
    });
  </script>
</body>
</html>"""
    return template.replace("__CARDS__", cards_html)


def build_interactive_page(visual_dir: Path, out_path: Path) -> dict[str, Any]:
    repo_root = repo_root_from_visual_dir(visual_dir)
    generate_busbar_preview, BusbarPreviewRequest = load_backend(repo_root)

    rendered: list[str] = []
    manifest_cases: list[dict[str, Any]] = []

    for case in review_cases():
        request = BusbarPreviewRequest(**case.params)
        preview = generate_busbar_preview(request)
        rendered.append(svg_card(case, preview))
        manifest_cases.append(
            {
                "id": case.id,
                "title": case.title,
                "terminal_count": len(preview.terminals),
                "bay_slot_count": len(preview.bay_slots),
                "label_count": len([slot for slot in preview.bay_slots if slot.label]),
                "viewBox": preview.viewBox,
                "labels": [slot.label for slot in preview.bay_slots if slot.label],
            }
        )

    write_text(out_path, page_html("\n".join(rendered)))

    return {
        "interactive_page": str(out_path),
        "case_count": len(rendered),
        "coordinate_mode": "clean_model_canvas_single_svg_coordinate_system",
        "grid_step": 6,
        "cases": manifest_cases,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build clean interactive busbar review page.")
    parser.add_argument("--visual-dir", type=Path, default=Path("visual_checks/parametric_busbar"))
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    visual_dir = args.visual_dir.resolve()
    out = args.out.resolve() if args.out else visual_dir / "interactive.html"
    summary = build_interactive_page(visual_dir, out)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
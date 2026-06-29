#!/usr/bin/env python3
"""Build an interactive visual review page from generated SVG snapshots.

This builder is transform-aware. The visible review SVG can contain transformed
subgroups, so label coordinates must be converted between text-local and root
SVG coordinates during drag and snapping.
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_interactive_page(visual_dir: Path, out_path: Path) -> dict[str, Any]:
    manifest = read_json(visual_dir / "manifest.json")
    cards: list[str] = []

    for case in manifest.get("cases", []):
        svg_name = case["svg"]
        svg_path = visual_dir / svg_name
        svg = svg_path.read_text(encoding="utf-8")
        title = html.escape(case.get("title", case.get("id", svg_name)))
        description = html.escape(case.get("description", ""))
        labels = html.escape(", ".join(case.get("labels", [])[:16]))
        case_id = html.escape(case.get("id", ""))
        terminal_count = case.get("terminal_count")
        bay_slot_count = case.get("bay_slot_count")
        label_count = case.get("label_count")
        cards.append(
            f"""<article class="card" data-case-id="{case_id}">
  <header>
    <h2>{title}</h2>
    <p>{description}</p>
    <p class="meta">terminals={terminal_count}; bay_slots={bay_slot_count}; labels={label_count}</p>
    <p class="labels">{labels}</p>
  </header>
  <div class="svg-wrap">{svg}</div>
  <p class="drag-status">Click or drag bus captions/cell numbers. Use the floating toolbar for rotation presets.</p>
</article>"""
        )

    cards_html = "\n".join(cards)

    page = """<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>Interactive visual review - ElectroScheme Studio</title>
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
    .svg-wrap svg { width: 100%; height: auto; display: block; }
    [data-role="bus-label"], [data-role="bay-label"] { cursor: grab; user-select: none; }
    [data-role="bus-label"].selected, [data-role="bay-label"].selected { paint-order: stroke; stroke: rgba(37, 99, 235, 0.35); stroke-width: 3; }
    .drag-status { font-size: 12px; color: #64748b; }
    .toolbar { position: fixed; right: 18px; bottom: 18px; z-index: 100; width: 280px; padding: 12px; border-radius: 14px; background: #111827; color: white; box-shadow: 0 12px 28px rgba(0,0,0,.25); }
    .toolbar h2 { margin: 0 0 8px; font-size: 15px; }
    .toolbar p { margin: 0 0 10px; color: #cbd5e1; font-size: 12px; }
    .toolbar button { margin: 3px; padding: 6px 9px; border: 0; border-radius: 999px; background: #2563eb; color: white; font-weight: 700; cursor: pointer; }
  </style>
</head>
<body>
  <header class="page">
    <h1>Interactive visual review</h1>
    <p>Transform-aware dragging: labels, guides and snapping now use one root coordinate system.</p>
  </header>
  <main>
    __CARDS__
  </main>
  <aside class="toolbar">
    <h2>Text tools</h2>
    <p id="selectedText">Selected: none</p>
    <button data-rotate="0">0В°</button>
    <button data-rotate="90">+90В°</button>
    <button data-rotate="-90">-90В°</button>
    <button data-rotate="180">180В°</button>
  </aside>
  <script>
    let selectedText = null;
    const snapTolerance = 6;
    const gridStep = 6;

    function svgPoint(svg, x, y) { const p = svg.createSVGPoint(); p.x = x; p.y = y; return p; }
    function clientToRootPoint(svg, event) { const ctm = svg.getScreenCTM(); return ctm ? svgPoint(svg, event.clientX, event.clientY).matrixTransform(ctm.inverse()) : null; }
    function parentCtm(target) { const parent = target.parentElement; return parent && typeof parent.getCTM === 'function' ? parent.getCTM() : null; }
    function localToRoot(target, x, y) { const svg = target.ownerSVGElement; const ctm = parentCtm(target); return svg && ctm ? svgPoint(svg, x, y).matrixTransform(ctm) : null; }
    function rootToLocal(target, x, y) { const svg = target.ownerSVGElement; const ctm = parentCtm(target); return svg && ctm ? svgPoint(svg, x, y).matrixTransform(ctm.inverse()) : null; }
    function elementLocalToRoot(element, x, y) { const svg = element.ownerSVGElement; const ctm = element.getCTM(); return svg && ctm ? svgPoint(svg, x, y).matrixTransform(ctm) : null; }
    function textAnchorRoot(target) { const x = Number(target.getAttribute('x')); const y = Number(target.getAttribute('y')); return Number.isFinite(x) && Number.isFinite(y) ? localToRoot(target, x, y) : null; }

    function elementBoundsInRoot(element) {
      try {
        const b = element.getBBox();
        const pts = [elementLocalToRoot(element, b.x, b.y), elementLocalToRoot(element, b.x + b.width, b.y), elementLocalToRoot(element, b.x, b.y + b.height), elementLocalToRoot(element, b.x + b.width, b.y + b.height)].filter(Boolean);
        if (pts.length !== 4) return null;
        const xs = pts.map((p) => p.x); const ys = pts.map((p) => p.y);
        const minX = Math.min(...xs); const maxX = Math.max(...xs); const minY = Math.min(...ys); const maxY = Math.max(...ys);
        return { x: minX, y: minY, width: maxX - minX, height: maxY - minY };
      } catch { return null; }
    }

    function circleCenterInRoot(circle) { const cx = Number(circle.getAttribute('cx')); const cy = Number(circle.getAttribute('cy')); return Number.isFinite(cx) && Number.isFinite(cy) ? elementLocalToRoot(circle, cx, cy) : null; }

    function resolveGuideBounds(svg) {
      const vb = svg.viewBox.baseVal;
      const fallback = { x: vb.x, y: vb.y, width: vb.width, height: vb.height };
      let best = null; let bestArea = 0;
      svg.querySelectorAll('rect').forEach((rect) => {
        const box = elementBoundsInRoot(rect); if (!box) return;
        const area = box.width * box.height;
        const looksLikeDrawingViewport = box.width >= 160 && box.height >= 80;
        const fitsInsideRoot = box.x >= vb.x - 1 && box.y >= vb.y - 1 && box.x + box.width <= vb.x + vb.width + 1 && box.y + box.height <= vb.y + vb.height + 1;
        if (looksLikeDrawingViewport && fitsInsideRoot && area > bestArea) { best = box; bestArea = area; }
      });
      return best || fallback;
    }

    function isInsideBounds(x, y, bounds) { return x >= bounds.x - 0.5 && x <= bounds.x + bounds.width + 0.5 && y >= bounds.y - 0.5 && y <= bounds.y + bounds.height + 0.5; }
    function addGuideIfInside(values, value, min, max) { if (Number.isFinite(value) && value >= min - 0.5 && value <= max + 0.5) values.push(value); }
    function unique(values) { return [...new Set(values.map((v) => Math.round(v * 10) / 10))].sort((a, b) => a - b); }

    function collectGuides(svg, target) {
      const bounds = resolveGuideBounds(svg);
      const vertical = []; const horizontal = [];
      svg.querySelectorAll('circle').forEach((circle) => { const p = circleCenterInRoot(circle); if (!p || !isInsideBounds(p.x, p.y, bounds)) return; vertical.push(p.x); horizontal.push(p.y); });
      svg.querySelectorAll('rect').forEach((rect) => {
        const box = elementBoundsInRoot(rect); if (!box) return;
        const cx = box.x + box.width / 2; const cy = box.y + box.height / 2;
        if (!isInsideBounds(cx, cy, bounds)) return;
        addGuideIfInside(vertical, box.x, bounds.x, bounds.x + bounds.width); addGuideIfInside(vertical, cx, bounds.x, bounds.x + bounds.width); addGuideIfInside(vertical, box.x + box.width, bounds.x, bounds.x + bounds.width);
        addGuideIfInside(horizontal, box.y, bounds.y, bounds.y + bounds.height); addGuideIfInside(horizontal, cy, bounds.y, bounds.y + bounds.height); addGuideIfInside(horizontal, box.y + box.height, bounds.y, bounds.y + bounds.height);
      });
      svg.querySelectorAll('text').forEach((text) => { if (text === target) return; const p = textAnchorRoot(text); if (!p || !isInsideBounds(p.x, p.y, bounds)) return; vertical.push(p.x); horizontal.push(p.y); });
      for (let x = bounds.x; x <= bounds.x + bounds.width; x += gridStep) vertical.push(x);
      for (let y = bounds.y; y <= bounds.y + bounds.height; y += gridStep) horizontal.push(y);
      return { vertical: unique(vertical), horizontal: unique(horizontal) };
    }

    function snap(value, guides) { let best = null; let d = Infinity; for (const g of guides) { const nd = Math.abs(value - g); if (nd < d) { d = nd; best = g; } } return best !== null && d <= snapTolerance ? { value: best, guide: best } : { value, guide: null }; }
    function ensureGuideLayer(svg) { let layer = svg.querySelector('[data-role="alignment-guides"]'); if (!layer) { layer = document.createElementNS('http://www.w3.org/2000/svg', 'g'); layer.setAttribute('data-role', 'alignment-guides'); layer.setAttribute('pointer-events', 'none'); svg.appendChild(layer); } return layer; }
    function addLine(layer, attrs) { const line = document.createElementNS('http://www.w3.org/2000/svg', 'line'); for (const [k, v] of Object.entries(attrs)) line.setAttribute(k, String(v)); layer.appendChild(line); }

    function drawGuides(svg, x, y, snapX, snapY) {
      const layer = ensureGuideLayer(svg); layer.innerHTML = '';
      const b = resolveGuideBounds(svg);
      const cx = Math.min(Math.max(x, b.x), b.x + b.width); const cy = Math.min(Math.max(y, b.y), b.y + b.height);
      const base = { stroke: '#64748b', 'stroke-width': '0.8', 'stroke-dasharray': '3 3', opacity: '0.55' };
      const hi = { stroke: '#2563eb', 'stroke-width': '1.4', 'stroke-dasharray': 'none', opacity: '0.9' };
      addLine(layer, { x1: cx, y1: b.y, x2: cx, y2: b.y + b.height, ...base });
      addLine(layer, { x1: b.x, y1: cy, x2: b.x + b.width, y2: cy, ...base });
      if (snapX !== null) addLine(layer, { x1: snapX, y1: b.y, x2: snapX, y2: b.y + b.height, ...hi });
      if (snapY !== null) addLine(layer, { x1: b.x, y1: snapY, x2: b.x + b.width, y2: snapY, ...hi });
    }

    function clearGuides(svg) { svg.querySelector('[data-role="alignment-guides"]')?.remove(); }
    function setTextPositionLocal(target, x, y) { const r = Number(target.getAttribute('data-rotation') || '0') || 0; const rx = Math.round(x * 10) / 10; const ry = Math.round(y * 10) / 10; target.setAttribute('x', String(rx)); target.setAttribute('y', String(ry)); target.setAttribute('transform', `rotate(${r} ${rx} ${ry})`); }
    function selectTarget(target) { document.querySelectorAll('.selected').forEach((i) => i.classList.remove('selected')); selectedText = target; if (target) { target.classList.add('selected'); const role = target.getAttribute('data-role') || 'text'; const id = target.getAttribute('data-bay-slot-id') || role; document.getElementById('selectedText').textContent = `Selected: ${id}`; } else { document.getElementById('selectedText').textContent = 'Selected: none'; } }

    document.querySelectorAll('.toolbar button[data-rotate]').forEach((button) => {
      button.addEventListener('click', () => { if (!selectedText) return; const r = Number(button.getAttribute('data-rotate') || '0') || 0; const x = Number(selectedText.getAttribute('x') || '0') || 0; const y = Number(selectedText.getAttribute('y') || '0') || 0; selectedText.setAttribute('data-rotation', String(r)); selectedText.setAttribute('transform', `rotate(${r} ${x} ${y})`); });
    });

    document.addEventListener('pointerdown', (event) => {
      const target = event.target.closest('[data-role="bus-label"], [data-role="bay-label"]');
      if (!target) return;
      const svg = target.ownerSVGElement; if (!svg) return;
      event.preventDefault(); selectTarget(target);
      const startRoot = clientToRootPoint(svg, event); if (!startRoot) return;
      const baseLocalX = Number(target.getAttribute('x') || '0') || 0; const baseLocalY = Number(target.getAttribute('y') || '0') || 0;
      const baseRoot = localToRoot(target, baseLocalX, baseLocalY) || startRoot;
      const guides = collectGuides(svg, target); const pointerId = event.pointerId; target.setPointerCapture?.(pointerId);
      const move = (moveEvent) => {
        if (moveEvent.pointerId !== pointerId) return;
        const currentRoot = clientToRootPoint(svg, moveEvent); if (!currentRoot) return;
        const rawRootX = baseRoot.x + currentRoot.x - startRoot.x; const rawRootY = baseRoot.y + currentRoot.y - startRoot.y;
        const sx = snap(rawRootX, guides.vertical); const sy = snap(rawRootY, guides.horizontal);
        const nextLocal = rootToLocal(target, sx.value, sy.value); if (!nextLocal) return;
        setTextPositionLocal(target, nextLocal.x, nextLocal.y); drawGuides(svg, sx.value, sy.value, sx.guide, sy.guide);
      };
      const up = (upEvent) => { if (upEvent.pointerId !== pointerId) return; target.releasePointerCapture?.(pointerId); clearGuides(svg); window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up); };
      window.addEventListener('pointermove', move); window.addEventListener('pointerup', up);
    });
  </script>
</body>
</html>
"""
    page = page.replace("__CARDS__", cards_html)
    write_text(out_path, page)

    return {
        "interactive_page": str(out_path),
        "case_count": len(manifest.get("cases", [])),
        "source_manifest": str(visual_dir / "manifest.json"),
        "coordinate_mode": "transform_aware_root_guides_local_label_writeback",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build interactive visual review page.")
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
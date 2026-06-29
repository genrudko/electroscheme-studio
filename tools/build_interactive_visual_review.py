#!/usr/bin/env python3
"""Build an interactive visual review page from generated SVG snapshots."""

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
        cards.append(
            f"""<article class="card" data-case-id="{html.escape(case.get("id", ""))}">
  <header>
    <h2>{title}</h2>
    <p>{description}</p>
    <p class="meta">terminals={case.get("terminal_count")}; bay_slots={case.get("bay_slot_count")}; labels={case.get("label_count")}</p>
    <p class="labels">{labels}</p>
  </header>
  <div class="svg-wrap">{svg}</div>
  <p class="drag-status">Drag bus captions or cell-number labels. This is visual-only; it does not rewrite model JSON.</p>
</article>"""
        )

    page = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>Interactive visual review - ElectroScheme Studio</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f5f6f8; color: #111827; }}
    header.page {{ position: sticky; top: 0; z-index: 10; background: #111827; color: white; padding: 16px 22px; box-shadow: 0 2px 12px rgba(0,0,0,.2); }}
    header.page h1 {{ margin: 0 0 6px; font-size: 22px; }}
    header.page p {{ margin: 0; color: #cbd5e1; }}
    main {{ padding: 18px; display: grid; grid-template-columns: repeat(auto-fill, minmax(620px, 1fr)); gap: 16px; }}
    .card {{ background: white; border: 1px solid #e5e7eb; border-radius: 14px; padding: 14px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }}
    .card h2 {{ margin: 0 0 6px; font-size: 17px; }}
    .card p {{ margin: 6px 0; color: #4b5563; }}
    .meta {{ font-size: 12px; font-weight: 700; }}
    .labels {{ font-size: 12px; color: #1d4ed8; }}
    .svg-wrap {{ width: 100%; min-height: 300px; border: 1px solid #e5e7eb; border-radius: 10px; background: #fff; overflow: auto; }}
    .svg-wrap svg {{ width: 100%; height: auto; display: block; }}
    [data-role="bus-label"], [data-role="bay-label"] {{ cursor: grab; user-select: none; }}
    [data-role="bus-label"].dragging, [data-role="bay-label"].dragging {{ cursor: grabbing; }}
    .drag-status {{ font-size: 12px; color: #64748b; }}
  </style>
</head>
<body>
  <header class="page">
    <h1>Interactive visual review</h1>
    <p>Static snapshots are embedded inline. Bus captions and cell-number labels can be dragged visually.</p>
  </header>
  <main>
    {''.join(cards)}
  </main>
  <script>
    function clientToSvgPoint(svg, event) {{
      const point = svg.createSVGPoint();
      point.x = event.clientX;
      point.y = event.clientY;
      const ctm = svg.getScreenCTM();
      if (!ctm) return null;
      return point.matrixTransform(ctm.inverse());
    }}

    function setTextPosition(target, x, y) {{
      const rotation = Number(target.getAttribute('data-rotation') || '0') || 0;
      const rx = Math.round(x * 10) / 10;
      const ry = Math.round(y * 10) / 10;
      target.setAttribute('x', String(rx));
      target.setAttribute('y', String(ry));
      target.setAttribute('transform', `rotate(${{rotation}} ${{rx}} ${{ry}})`);
    }}

    document.addEventListener('pointerdown', (event) => {{
      const target = event.target.closest('[data-role="bus-label"], [data-role="bay-label"]');
      if (!target) return;
      const svg = target.ownerSVGElement;
      if (!svg) return;

      event.preventDefault();

      const start = clientToSvgPoint(svg, event);
      if (!start) return;

      const baseX = Number(target.getAttribute('x') || '0') || 0;
      const baseY = Number(target.getAttribute('y') || '0') || 0;
      const pointerId = event.pointerId;
      target.classList.add('dragging');
      target.setPointerCapture?.(pointerId);

      const move = (moveEvent) => {{
        if (moveEvent.pointerId !== pointerId) return;
        const current = clientToSvgPoint(svg, moveEvent);
        if (!current) return;
        setTextPosition(target, baseX + current.x - start.x, baseY + current.y - start.y);
      }};

      const up = (upEvent) => {{
        if (upEvent.pointerId !== pointerId) return;
        target.classList.remove('dragging');
        target.releasePointerCapture?.(pointerId);
        window.removeEventListener('pointermove', move);
        window.removeEventListener('pointerup', up);
      }};

      window.addEventListener('pointermove', move);
      window.addEventListener('pointerup', up);
    }});
  </script>
</body>
</html>
"""
    write_text(out_path, page)

    return {
        "interactive_page": str(out_path),
        "case_count": len(manifest.get("cases", [])),
        "source_manifest": str(visual_dir / "manifest.json"),
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
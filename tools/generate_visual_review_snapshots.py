#!/usr/bin/env python3
"""Generate local visual review snapshots for ElectroScheme Studio."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any


def ensure_backend_import(repo_root: Path) -> None:
    backend_root = repo_root / "backend"
    if str(backend_root) not in sys.path:
        sys.path.insert(0, str(backend_root))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def fmt(value: float) -> str:
    if abs(value) < 1e-9:
        value = 0.0
    return f"{value:.6g}"


def build_cases() -> list[dict[str, Any]]:
    base = {
        "voltage_kv": 35,
        "stroke_width": 4,
        "margin": 20,
        "lead_length": 28,
        "bay_depth": 90,
        "bay_numbering_enabled": True,
        "bay_numbering_prefix": "Яч. ",
        "bay_numbering_start": 1,
        "bay_numbering_step": 1,
        "bay_label_position": "above",
        "bay_label_offset": 12,
    }
    return [
        {
            "id": "01_horizontal_bottom_numbered",
            "title": "Horizontal busbar — bottom slots, numbered above",
            "description": "Default RU section case: cells under busbar, numbering above bay slots.",
            "request": {**base, "id": "visual_busbar_bottom", "name_ru": "1С-35", "length": 420, "connection_count": 8, "connection_side": "bottom", "orientation": "horizontal"},
        },
        {
            "id": "02_horizontal_top_numbered",
            "title": "Horizontal busbar — top slots, numbered above",
            "description": "Checks label clearance when equipment slots are above the busbar.",
            "request": {**base, "id": "visual_busbar_top", "name_ru": "2С-35", "length": 420, "connection_count": 8, "connection_side": "top", "orientation": "horizontal", "bay_numbering_start": 9},
        },
        {
            "id": "03_horizontal_both_sides",
            "title": "Horizontal busbar — both sides",
            "description": "Shows numbering sequence when slots are generated on both sides.",
            "request": {**base, "id": "visual_busbar_both", "name_ru": "3С-35", "length": 520, "connection_count": 6, "connection_side": "both", "orientation": "horizontal", "bay_numbering_start": 21, "bay_depth": 80},
        },
        {
            "id": "04_vertical_right_numbered",
            "title": "Vertical busbar — right slots",
            "description": "Checks vertical orientation, right-side bay slots and labels.",
            "request": {**base, "id": "visual_busbar_vertical_right", "name_ru": "Вертикальная шина", "length": 420, "connection_count": 7, "connection_side": "bottom", "orientation": "vertical", "bay_label_position": "right"},
        },
        {
            "id": "05_vertical_left_numbered",
            "title": "Vertical busbar — left slots",
            "description": "Checks vertical orientation, left-side bay slots and labels.",
            "request": {**base, "id": "visual_busbar_vertical_left", "name_ru": "Вертикальная шина Л", "length": 420, "connection_count": 7, "connection_side": "top", "orientation": "vertical", "bay_label_position": "left"},
        },
        {
            "id": "06_numbering_disabled",
            "title": "Horizontal busbar — numbering disabled",
            "description": "Checks clean geometry without cell labels.",
            "request": {**base, "id": "visual_busbar_no_numbering", "name_ru": "Шина без номеров", "length": 360, "connection_count": 5, "connection_side": "bottom", "orientation": "horizontal", "bay_numbering_enabled": False, "bay_depth": 80},
        },
        {
            "id": "07_dense_16_slots",
            "title": "Dense busbar — 16 numbered slots",
            "description": "Stress test for label overlap and slot spacing.",
            "request": {**base, "id": "visual_busbar_dense", "name_ru": "Плотная шина 16", "length": 680, "connection_count": 16, "connection_side": "bottom", "orientation": "horizontal", "lead_length": 24, "bay_depth": 70, "bay_label_offset": 10},
        },
    ]


def render_case_svg(title: str, description: str, preview: Any) -> str:
    vb = preview.viewBox
    width = float(vb.get("width", 100))
    height = float(vb.get("height", 100))
    canvas_w = max(width + 80, 620)
    canvas_h = height + 130
    tx = 40
    ty = 80
    fragment = preview.svg_fragment
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(canvas_w)}" height="{fmt(canvas_h)}" viewBox="0 0 {fmt(canvas_w)} {fmt(canvas_h)}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <defs><pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M 18 0 L 0 0 0 18" fill="none" stroke="#e5e7eb" stroke-width="1"/></pattern></defs>
  <text x="24" y="28" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="#111827">{html.escape(title)}</text>
  <text x="24" y="50" font-family="Arial, sans-serif" font-size="12" fill="#4b5563">{html.escape(description)}</text>
  <rect x="{fmt(tx - 12)}" y="{fmt(ty - 12)}" width="{fmt(width + 24)}" height="{fmt(height + 24)}" fill="url(#grid)" stroke="#cbd5e1" rx="10"/>
  <g transform="translate({fmt(tx)}, {fmt(ty)})" style="color:#4b5563;--voltage-color:#4b5563;--slot-color:#2563eb;--label-color:#111827">
{fragment}
  </g>
  <text x="24" y="{fmt(canvas_h - 28)}" font-family="Arial, sans-serif" font-size="11" fill="#64748b">terminals={len(preview.terminals)}; bay_slots={len(preview.bay_slots)}; viewBox={fmt(width)}x{fmt(height)}</text>
</svg>
"""


def render_index(manifest: dict[str, Any]) -> str:
    cards: list[str] = []
    for item in manifest["cases"]:
        labels = ", ".join(item["labels"][:12])
        cards.append(f"""
<article class="card">
  <h2>{html.escape(item['title'])}</h2>
  <p>{html.escape(item['description'])}</p>
  <p class="meta">terminals={item['terminal_count']}; bay_slots={item['bay_slot_count']}; labels={item['label_count']}</p>
  <p class="labels">{html.escape(labels)}</p>
  <object data="{html.escape(item['svg'])}" type="image/svg+xml" class="preview"></object>
  <p><a href="{html.escape(item['svg'])}" target="_blank" rel="noreferrer">Open SVG</a></p>
</article>""")
    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>ElectroScheme Studio — Visual review snapshots</title>
  <style>
    body {{ margin:0; font-family:Arial,sans-serif; background:#f5f6f8; color:#111827; }}
    header {{ position:sticky; top:0; z-index:10; background:#111827; color:white; padding:18px 24px; box-shadow:0 2px 12px rgba(0,0,0,.2); }}
    header h1 {{ margin:0 0 6px; font-size:22px; }}
    header p {{ margin:0; color:#cbd5e1; }}
    main {{ padding:18px; display:grid; grid-template-columns:repeat(auto-fill,minmax(560px,1fr)); gap:16px; }}
    .card {{ background:white; border:1px solid #e5e7eb; border-radius:14px; padding:14px; box-shadow:0 1px 4px rgba(0,0,0,.06); }}
    .card h2 {{ margin:0 0 6px; font-size:17px; }}
    .card p {{ margin:6px 0; color:#4b5563; }}
    .meta {{ font-size:12px; font-weight:700; }}
    .labels {{ font-size:12px; color:#1d4ed8; }}
    .preview {{ width:100%; min-height:280px; border:1px solid #e5e7eb; border-radius:10px; background:#fff; }}
    a {{ color:#2563eb; font-weight:700; }}
  </style>
</head>
<body>
  <header><h1>ElectroScheme Studio — Visual review snapshots</h1><p>Open this file locally and comment on geometry, label placement, slot spacing and readability.</p></header>
  <main>{''.join(cards)}</main>
</body>
</html>
"""


def generate(repo_root: Path, out_dir: Path) -> dict[str, Any]:
    ensure_backend_import(repo_root)
    from app.core.parametric_busbar import generate_busbar_preview
    from app.schemas.parametric_symbols import BusbarPreviewRequest

    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.svg"):
        old.unlink()

    cases_out: list[dict[str, Any]] = []
    for case in build_cases():
        preview = generate_busbar_preview(BusbarPreviewRequest(**case["request"]))
        svg_name = f"{case['id']}.svg"
        write_text(out_dir / svg_name, render_case_svg(case["title"], case["description"], preview))
        labels = [slot.label for slot in preview.bay_slots if slot.label]
        cases_out.append({
            "id": case["id"],
            "title": case["title"],
            "description": case["description"],
            "svg": svg_name,
            "request": case["request"],
            "terminal_count": len(preview.terminals),
            "bay_slot_count": len(preview.bay_slots),
            "label_count": len(labels),
            "labels": labels,
            "viewBox": preview.viewBox,
        })

    manifest = {
        "schema_version": "visual-review-snapshots-0.1",
        "feature": "parametric_busbar",
        "out_dir": str(out_dir),
        "index": str(out_dir / "index.html"),
        "case_count": len(cases_out),
        "cases": cases_out,
        "review_questions": [
            "Номера ячеек читаются и не перекрывают шину?",
            "Подписи расположены с нужной стороны?",
            "Bay slot markers не мешают восприятию схемы?",
            "Плотная шина с 16 присоединениями выглядит приемлемо?",
            "Нужны ли другие стили подписи: только число, Яч. N, N, N-35?",
        ],
    }
    write_json(out_dir / "manifest.json", manifest)
    write_text(out_dir / "index.html", render_index(manifest))
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate visual review snapshots.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path, default=Path("visual_checks/parametric_busbar"))
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    out_dir = args.out if args.out.is_absolute() else repo_root / args.out
    manifest = generate(repo_root, out_dir)
    print(json.dumps({
        "index": manifest["index"],
        "case_count": manifest["case_count"],
        "cases": [
            {
                "id": case["id"],
                "svg": case["svg"],
                "terminal_count": case["terminal_count"],
                "bay_slot_count": case["bay_slot_count"],
                "label_count": case["label_count"],
                "labels": case["labels"][:8],
            }
            for case in manifest["cases"]
        ],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
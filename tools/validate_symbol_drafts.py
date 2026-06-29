#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

REQUIRED = [
    "schema_version", "id", "name_ru", "category", "review_status",
    "source", "viewBox", "svg_fragment", "terminals", "capabilities", "conversion",
]

SWITCHING = {"circuit_breaker", "load_break_switch", "disconnector", "earthing_switch", "kru_trolley"}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def is_num(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def validate_one(path: Path, symbol: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    for key in REQUIRED:
        if key not in symbol:
            errors.append(f"missing required field: {key}")

    sid = str(symbol.get("id", ""))
    if not sid:
        errors.append("empty id")
    if sid and path.name != f"{sid}.symbol.json":
        warnings.append("filename does not match id")

    if symbol.get("review_status") != "needs_review":
        errors.append("review_status must remain needs_review")

    vb = symbol.get("viewBox", {})
    width = vb.get("width")
    height = vb.get("height")
    if not is_num(width) or float(width) <= 0:
        errors.append("viewBox.width must be positive")
    if not is_num(height) or float(height) <= 0:
        errors.append("viewBox.height must be positive")

    fragment = symbol.get("svg_fragment", "")
    if not isinstance(fragment, str) or not fragment.strip():
        errors.append("empty svg_fragment")
    if isinstance(fragment, str) and "<svg" in fragment.lower():
        warnings.append("svg_fragment contains nested <svg>")

    terminals = symbol.get("terminals", [])
    if not isinstance(terminals, list):
        errors.append("terminals must be array")
        terminals = []

    seen = set()
    coord_count = 0
    for t in terminals:
        if not isinstance(t, dict):
            errors.append("terminal is not object")
            continue
        tid = str(t.get("id", ""))
        if not tid:
            errors.append("terminal without id")
        elif tid in seen:
            errors.append(f"duplicate terminal id: {tid}")
        seen.add(tid)

        x = t.get("x")
        y = t.get("y")
        if is_num(x) and is_num(y):
            coord_count += 1
            if is_num(width) and is_num(height):
                if float(x) < -1e-6 or float(y) < -1e-6 or float(x) > float(width) + 1e-6 or float(y) > float(height) + 1e-6:
                    warnings.append(f"terminal outside viewBox: {tid}")
        else:
            warnings.append(f"terminal without numeric coordinates: {tid}")

    caps = symbol.get("capabilities", {})
    flags = caps.get("feature_flags", {}) if isinstance(caps, dict) else {}
    if not flags.get("colorizable_by_voltage_class", False):
        errors.append("missing voltage colorization flag")
    if not flags.get("rotatable", False):
        errors.append("missing rotatable flag")
    if not flags.get("requires_review", False):
        errors.append("missing requires_review flag")

    category = str(symbol.get("category", "unknown"))
    if category == "busbar" and not flags.get("busbar_configurable_connection_points", False):
        errors.append("busbar must have configurable connection points flag")

    states = caps.get("states", {}) if isinstance(caps, dict) else {}
    if category in SWITCHING and not states.get("enabled", False):
        errors.append("switching device must enable states")

    conv = symbol.get("conversion", {})
    conv_warnings = conv.get("warnings", []) if isinstance(conv, dict) else []
    for item in conv_warnings:
        warnings.append(f"converter: {item}")

    score = 100 - min(100, len(errors) * 25) - min(40, len(warnings) * 2)
    if coord_count == 0:
        score -= 10
    score = max(0, score)

    return {
        "id": sid,
        "name_ru": symbol.get("name_ru", ""),
        "category": category,
        "path": str(path),
        "terminal_count": len(terminals),
        "terminal_with_coordinates": coord_count,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "quality_score": score,
        "feature_flags": flags,
        "errors": errors,
        "warnings": warnings,
    }


def make_svg_preview(symbol: dict[str, Any]) -> str:
    vb = symbol.get("viewBox", {})
    width = float(vb.get("width") or 1)
    height = float(vb.get("height") or 1)
    fragment = symbol.get("svg_fragment", "")
    return (
        f'<svg class="symbol-preview" viewBox="0 0 {width:g} {height:g}" '
        'xmlns="http://www.w3.org/2000/svg">'
        f'{fragment}</svg>'
    )


def build_report(draft_dir: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    files = sorted(draft_dir.glob("*.symbol.json"))
    results: list[dict[str, Any]] = []
    symbols: dict[str, dict[str, Any]] = {}
    failures: list[dict[str, str]] = []

    seen_ids = set()
    duplicate_ids = []

    for path in files:
        try:
            symbol = read_json(path)
            result = validate_one(path, symbol)
        except Exception as exc:
            failures.append({"path": str(path), "error": str(exc)})
            continue

        sid = result["id"]
        if sid in seen_ids:
            result["errors"].append(f"duplicate id: {sid}")
            result["error_count"] += 1
            duplicate_ids.append(sid)
        seen_ids.add(sid)
        symbols[sid] = symbol
        results.append(result)

    by_category = Counter(item["category"] for item in results)
    with_terminals = sum(1 for item in results if item["terminal_count"] > 0)
    with_warnings = sum(1 for item in results if item["warning_count"] > 0)
    with_errors = sum(1 for item in results if item["error_count"] > 0)
    avg = round(sum(item["quality_score"] for item in results) / len(results), 2) if results else 0

    high_priority = [
        item for item in results
        if item["error_count"] > 0
        or item["terminal_count"] == 0
        or item["category"] in {"busbar", "circuit_breaker", "disconnector", "earthing_switch", "kru_trolley"}
    ]
    high_priority.sort(key=lambda item: (item["error_count"] == 0, item["quality_score"], item["id"]))

    report = {
        "schema_version": "symbol-draft-review-0.1",
        "draft_dir": str(draft_dir),
        "draft_count": len(files),
        "loaded_count": len(results),
        "load_failures": failures,
        "duplicate_ids": sorted(set(duplicate_ids)),
        "summary": {
            "with_terminals": with_terminals,
            "without_terminals": len(results) - with_terminals,
            "with_warnings": with_warnings,
            "without_warnings": len(results) - with_warnings,
            "with_errors": with_errors,
            "without_errors": len(results) - with_errors,
            "average_quality": avg,
            "by_category": dict(sorted(by_category.items())),
        },
        "review_policy": {
            "all_drafts_must_remain_needs_review": True,
            "promotion_to_core_requires_manual_review": True,
            "busbars_require_parameterization": True,
            "switching_devices_require_state_mapping": True,
            "rotation_snap_stretch_voltage_style_must_be_validated": True,
        },
        "high_priority_review": high_priority[:80],
        "symbols": results,
    }
    return report, symbols


def write_html(path: Path, report: dict[str, Any], symbols: dict[str, dict[str, Any]]) -> None:
    rows = []
    for item in report["symbols"]:
        symbol = symbols.get(item["id"], {})
        preview = make_svg_preview(symbol) if symbol else ""
        flags = item.get("feature_flags", {})
        badges = "".join(
            f'<span class="badge">{html.escape(key)}</span>'
            for key in ["colorizable_by_voltage_class", "multi_state_candidate", "busbar_configurable_connection_points", "stretchable_leads_candidate", "auto_layout_eligible"]
            if flags.get(key)
        )
        issues = "".join(f'<li class="error">{html.escape(x)}</li>' for x in item["errors"])
        issues += "".join(f'<li class="warning">{html.escape(x)}</li>' for x in item["warnings"][:8])
        if not issues:
            issues = '<li class="ok">No validator issues</li>'
        rows.append(f'''
<section class="card">
  <div class="preview">{preview}</div>
  <div class="meta">
    <h2>{html.escape(str(item["name_ru"]))}</h2>
    <p><code>{html.escape(str(item["id"]))}</code></p>
    <p>Category: <strong>{html.escape(str(item["category"]))}</strong></p>
    <p>Terminals: {item["terminal_count"]}; with coordinates: {item["terminal_with_coordinates"]}</p>
    <p>Quality: <strong>{item["quality_score"]}</strong>; errors: {item["error_count"]}; warnings: {item["warning_count"]}</p>
    <div>{badges}</div>
    <details><summary>Issues</summary><ul>{issues}</ul></details>
  </div>
</section>''')

    summary = report["summary"]
    text = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>ElectroScheme Studio — Visio Draft Symbol Review</title>
<style>
body{{margin:0;font-family:Arial,sans-serif;background:#f5f6f8;color:#1f2937}}
header{{position:sticky;top:0;z-index:5;background:#111827;color:white;padding:16px 24px;box-shadow:0 2px 8px rgba(0,0,0,.2)}}
h1{{margin:0 0 8px;font-size:22px}}
.stats{{display:flex;flex-wrap:wrap;gap:10px;font-size:13px}}
.stat{{background:rgba(255,255,255,.12);padding:6px 10px;border-radius:999px}}
main{{padding:18px;display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:14px}}
.card{{display:grid;grid-template-columns:150px 1fr;gap:12px;background:white;border:1px solid #e5e7eb;border-radius:12px;padding:12px;box-shadow:0 1px 2px rgba(0,0,0,.05)}}
.preview{{display:flex;align-items:center;justify-content:center;min-height:140px;border:1px solid #e5e7eb;border-radius:8px;overflow:hidden;color:#4b5563;--voltage-color:#4b5563}}
.symbol-preview{{max-width:135px;max-height:125px;width:135px;height:125px}}
.meta h2{{font-size:16px;margin:0 0 4px}}
.meta p{{margin:4px 0;font-size:13px}}
code{{font-size:12px;color:#374151}}
.badge{{display:inline-block;background:#e0f2fe;color:#075985;padding:3px 7px;border-radius:999px;margin:2px;font-size:11px}}
details{{margin-top:8px;font-size:12px}}
.error{{color:#b91c1c}}.warning{{color:#92400e}}.ok{{color:#047857}}
</style>
</head>
<body>
<header>
  <h1>ElectroScheme Studio — Visio Draft Symbol Review</h1>
  <div class="stats">
    <span class="stat">Drafts: {report["loaded_count"]}</span>
    <span class="stat">With terminals: {summary["with_terminals"]}</span>
    <span class="stat">Without terminals: {summary["without_terminals"]}</span>
    <span class="stat">Warnings: {summary["with_warnings"]}</span>
    <span class="stat">Errors: {summary["with_errors"]}</span>
    <span class="stat">Avg quality: {summary["average_quality"]}</span>
  </div>
</header>
<main>
{''.join(rows)}
</main>
</body>
</html>
'''
    write_text(path, text)


def write_md(path: Path, report: dict[str, Any]) -> None:
    summary = report["summary"]
    lines = [
        "# Visio draft symbol review summary",
        "",
        f"- Draft count: {report['draft_count']}",
        f"- Loaded count: {report['loaded_count']}",
        f"- With terminals: {summary['with_terminals']}",
        f"- Without terminals: {summary['without_terminals']}",
        f"- With warnings: {summary['with_warnings']}",
        f"- With errors: {summary['with_errors']}",
        f"- Average quality: {summary['average_quality']}",
        "",
        "## Categories",
        "",
        "| Category | Count |",
        "|---|---:|",
    ]
    for category, count in summary["by_category"].items():
        lines.append(f"| {category} | {count} |")
    lines += [
        "",
        "## High priority review",
        "",
        "| Symbol | Category | Score | Terminals | Errors | Warnings |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for item in report["high_priority_review"][:40]:
        lines.append(f"| `{item['id']}` {item['name_ru']} | {item['category']} | {item['quality_score']} | {item['terminal_count']} | {item['error_count']} | {item['warning_count']} |")
    lines += [
        "",
        "## Policy",
        "",
        "- Drafts stay in `needs_review`.",
        "- Core promotion requires manual review.",
        "- Busbars require parameterization.",
        "- Switching devices require state mapping.",
        "- Rotation/snap/stretch/voltage style must be validated.",
    ]
    write_text(path, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft-dir", type=Path, default=Path("symbols/imported/visio/needs_review"))
    parser.add_argument("--report-json", type=Path, default=Path("symbols/imported/visio/review_report.json"))
    parser.add_argument("--report-html", type=Path, default=Path("symbols/imported/visio/review_report.html"))
    parser.add_argument("--report-md", type=Path, default=Path("symbols/imported/visio/review_summary.md"))
    args = parser.parse_args()

    report, symbols = build_report(args.draft_dir)
    write_json(args.report_json, report)
    write_html(args.report_html, report, symbols)
    write_md(args.report_md, report)

    print(json.dumps({
        "draft_count": report["draft_count"],
        "loaded_count": report["loaded_count"],
        "summary": report["summary"],
        "report_json": str(args.report_json),
        "report_html": str(args.report_html),
        "report_md": str(args.report_md),
    }, ensure_ascii=False, indent=2))

    return 2 if report["load_failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
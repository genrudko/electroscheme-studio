#!/usr/bin/env python3
"""Initialize or refresh imported Visio symbol review status store."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ALLOWED_STATUSES = [
    "needs_review",
    "accepted",
    "rejected",
    "needs_geometry_review",
    "needs_manual_terminals",
    "needs_state_mapping",
    "needs_busbar_parameters",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_symbols(index_path: Path, report_path: Path) -> list[dict[str, Any]]:
    report = load_json(report_path, {})
    symbols = report.get("symbols")
    if isinstance(symbols, list) and symbols:
        return symbols

    index = load_json(index_path, {})
    indexed = index.get("symbols", [])
    return indexed if isinstance(indexed, list) else []


def infer_initial_status(symbol: dict[str, Any]) -> str:
    category = str(symbol.get("category", ""))
    terminal_count = int(symbol.get("terminal_count", 0) or 0)
    warning_count = int(symbol.get("warning_count", 0) or 0)

    if category == "busbar":
        return "needs_busbar_parameters"
    if category in {"circuit_breaker", "load_break_switch", "disconnector", "earthing_switch", "kru_trolley"}:
        return "needs_state_mapping"
    if terminal_count == 0:
        return "needs_manual_terminals"
    if warning_count > 0:
        return "needs_geometry_review"
    return "needs_review"


def build_status_store(index_path: Path, report_path: Path, status_path: Path) -> dict[str, Any]:
    now = utc_now()
    existing = load_json(status_path, {})
    existing_entries = existing.get("entries", {}) if isinstance(existing, dict) else {}
    symbols = load_symbols(index_path, report_path)

    entries: dict[str, Any] = {}
    for symbol in symbols:
        symbol_id = str(symbol.get("id", ""))
        if not symbol_id:
            continue

        old = existing_entries.get(symbol_id, {}) if isinstance(existing_entries, dict) else {}
        old_status = old.get("status")
        status = old_status if old_status in ALLOWED_STATUSES else infer_initial_status(symbol)

        entries[symbol_id] = {
            "symbol_id": symbol_id,
            "name_ru": symbol.get("name_ru", ""),
            "category": symbol.get("category", ""),
            "status": status,
            "note": old.get("note", ""),
            "updated_at": old.get("updated_at", now),
            "updated_by": old.get("updated_by", "system"),
            "source_quality_score": symbol.get("quality_score"),
            "terminal_count": symbol.get("terminal_count", 0),
            "warning_count": symbol.get("warning_count", 0),
            "error_count": symbol.get("error_count", 0),
        }

    store = {
        "schema_version": "symbol-review-status-0.1",
        "updated_at": now,
        "allowed_statuses": ALLOWED_STATUSES,
        "entries": entries,
        "summary": summarize(entries),
    }
    return store


def summarize(entries: dict[str, Any]) -> dict[str, int]:
    result = {status: 0 for status in ALLOWED_STATUSES}
    for entry in entries.values():
        status = entry.get("status", "needs_review")
        result[status] = result.get(status, 0) + 1
    result["total"] = len(entries)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize imported symbol review status store.")
    parser.add_argument("--index", type=Path, default=Path("symbols/imported/visio/index.json"))
    parser.add_argument("--review-report", type=Path, default=Path("symbols/imported/visio/review_report.json"))
    parser.add_argument("--status", type=Path, default=Path("symbols/imported/visio/review_status.json"))
    args = parser.parse_args()

    store = build_status_store(args.index, args.review_report, args.status)
    write_json(args.status, store)
    print(json.dumps({"status": str(args.status), "summary": store["summary"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
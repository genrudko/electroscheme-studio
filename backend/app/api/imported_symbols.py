from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


router = APIRouter(prefix="/api/imported-symbols", tags=["imported-symbols"])


ALLOWED_REVIEW_STATUSES = {
    "needs_review",
    "accepted",
    "rejected",
    "needs_geometry_review",
    "needs_manual_terminals",
    "needs_state_mapping",
    "needs_busbar_parameters",
}


class ReviewStatusUpdate(BaseModel):
    status: str = Field(..., min_length=1)
    note: str = ""
    updated_by: str = "local-user"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _repo_root() -> Path:
    # backend/app/api/imported_symbols.py -> repo root
    return Path(__file__).resolve().parents[3]


def _visio_root() -> Path:
    return _repo_root() / "symbols" / "imported" / "visio"


def _needs_review_dir() -> Path:
    return _visio_root() / "needs_review"


def _status_path() -> Path:
    return _visio_root() / "review_status.json"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {path.name}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in {path.name}: {exc}") from exc


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _symbol_exists(symbol_id: str) -> bool:
    return (_needs_review_dir() / f"{symbol_id}.symbol.json").exists()


def _default_status_store() -> dict[str, Any]:
    return {
        "schema_version": "symbol-review-status-0.1",
        "updated_at": _utc_now(),
        "allowed_statuses": sorted(ALLOWED_REVIEW_STATUSES),
        "entries": {},
        "summary": {},
    }


def _summarize_statuses(entries: dict[str, Any]) -> dict[str, int]:
    summary = {status: 0 for status in sorted(ALLOWED_REVIEW_STATUSES)}
    for entry in entries.values():
        status = str(entry.get("status", "needs_review"))
        summary[status] = summary.get(status, 0) + 1
    summary["total"] = len(entries)
    return summary


def _load_status_store() -> dict[str, Any]:
    path = _status_path()
    if not path.exists():
        return _default_status_store()
    store = _load_json(path)
    entries = store.get("entries")
    if not isinstance(entries, dict):
        store["entries"] = {}
    store["allowed_statuses"] = sorted(ALLOWED_REVIEW_STATUSES)
    store["summary"] = _summarize_statuses(store["entries"])
    return store


def _save_status_store(store: dict[str, Any]) -> dict[str, Any]:
    store["schema_version"] = "symbol-review-status-0.1"
    store["updated_at"] = _utc_now()
    store["allowed_statuses"] = sorted(ALLOWED_REVIEW_STATUSES)
    entries = store.get("entries")
    if not isinstance(entries, dict):
        entries = {}
        store["entries"] = entries
    store["summary"] = _summarize_statuses(entries)
    _write_json(_status_path(), store)
    return store


def _annotate_report_with_status(report: dict[str, Any], status_store: dict[str, Any]) -> dict[str, Any]:
    entries = status_store.get("entries", {})
    symbols = report.get("symbols", [])
    if isinstance(symbols, list):
        for symbol in symbols:
            if not isinstance(symbol, dict):
                continue
            symbol_id = str(symbol.get("id", ""))
            entry = entries.get(symbol_id, {})
            symbol["workflow_status"] = entry.get("status", "needs_review")
            symbol["workflow_note"] = entry.get("note", "")
            symbol["workflow_updated_at"] = entry.get("updated_at", "")
    report["workflow_summary"] = status_store.get("summary", {})
    return report


@router.get("")
def list_imported_symbols() -> dict[str, Any]:
    index_path = _visio_root() / "index.json"
    review_report_path = _visio_root() / "review_report.json"
    status_store = _load_status_store()

    index = _load_json(index_path) if index_path.exists() else {
        "schema_version": "draft-index-0.1",
        "review_status": "missing",
        "symbols": [],
        "failures": [],
    }

    review_report = _load_json(review_report_path) if review_report_path.exists() else None
    if review_report is not None:
        review_report = _annotate_report_with_status(review_report, status_store)

    return {
        "source": "symbols/imported/visio",
        "review_status": "needs_review",
        "index": index,
        "review_report": review_report,
        "review_status_store": status_store,
    }


@router.get("/review-status")
def get_review_status_store() -> dict[str, Any]:
    return _load_status_store()


@router.put("/{symbol_id}/review-status")
def update_review_status(symbol_id: str, update: ReviewStatusUpdate) -> dict[str, Any]:
    safe_id = symbol_id.strip()
    if not safe_id or "/" in safe_id or "\\" in safe_id or ".." in safe_id:
        raise HTTPException(status_code=400, detail="Invalid symbol id")

    if update.status not in ALLOWED_REVIEW_STATUSES:
        raise HTTPException(status_code=400, detail=f"Unsupported review status: {update.status}")

    if not _symbol_exists(safe_id):
        raise HTTPException(status_code=404, detail=f"Imported symbol not found: {safe_id}")

    store = _load_status_store()
    entries = store.setdefault("entries", {})
    current = entries.get(safe_id, {})
    entries[safe_id] = {
        **current,
        "symbol_id": safe_id,
        "status": update.status,
        "note": update.note,
        "updated_at": _utc_now(),
        "updated_by": update.updated_by or "local-user",
    }

    saved = _save_status_store(store)
    return {
        "symbol_id": safe_id,
        "entry": saved["entries"][safe_id],
        "summary": saved["summary"],
    }


@router.get("/{symbol_id}")
def get_imported_symbol(symbol_id: str) -> dict[str, Any]:
    safe_id = symbol_id.strip()
    if not safe_id or "/" in safe_id or "\\" in safe_id or ".." in safe_id:
        raise HTTPException(status_code=400, detail="Invalid symbol id")

    symbol_path = _needs_review_dir() / f"{safe_id}.symbol.json"
    symbol = _load_json(symbol_path)

    status_store = _load_status_store()
    entry = status_store.get("entries", {}).get(safe_id)
    symbol["workflow_status"] = entry.get("status", "needs_review") if isinstance(entry, dict) else "needs_review"
    symbol["workflow_note"] = entry.get("note", "") if isinstance(entry, dict) else ""
    symbol["workflow_updated_at"] = entry.get("updated_at", "") if isinstance(entry, dict) else ""
    return symbol
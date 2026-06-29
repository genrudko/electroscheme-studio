from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException


router = APIRouter(prefix="/api/imported-symbols", tags=["imported-symbols"])


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _visio_root() -> Path:
    return _repo_root() / "symbols" / "imported" / "visio"


def _needs_review_dir() -> Path:
    return _visio_root() / "needs_review"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {path.name}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in {path.name}: {exc}") from exc


@router.get("")
def list_imported_symbols() -> dict[str, Any]:
    index_path = _visio_root() / "index.json"
    review_report_path = _visio_root() / "review_report.json"

    index = _load_json(index_path) if index_path.exists() else {
        "schema_version": "draft-index-0.1",
        "review_status": "missing",
        "symbols": [],
        "failures": [],
    }
    review_report = _load_json(review_report_path) if review_report_path.exists() else None

    return {
        "source": "symbols/imported/visio",
        "review_status": "needs_review",
        "index": index,
        "review_report": review_report,
    }


@router.get("/{symbol_id}")
def get_imported_symbol(symbol_id: str) -> dict[str, Any]:
    safe_id = symbol_id.strip()
    if not safe_id or "/" in safe_id or "\\" in safe_id or ".." in safe_id:
        raise HTTPException(status_code=400, detail="Invalid symbol id")
    return _load_json(_needs_review_dir() / f"{safe_id}.symbol.json")
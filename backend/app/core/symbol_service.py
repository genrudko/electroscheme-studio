"""Service layer for the GOST symbol library."""

from __future__ import annotations

import json
import pathlib
from typing import Any

from app.schemas.symbol_library import SymbolLibrary

_DATA_DIR = pathlib.Path(__file__).resolve().parent.parent / "data"
_LIBRARY_PATH = _DATA_DIR / "symbol_library.json"
_cache: dict[str, Any] | None = None


def _load_raw() -> dict[str, Any]:
    global _cache
    if _cache is None:
        text = _LIBRARY_PATH.read_text(encoding="utf-8")
        _cache = json.loads(text)
    return _cache


def get_library() -> SymbolLibrary:
    return SymbolLibrary.model_validate(_load_raw())


def get_symbols() -> list[dict[str, Any]]:
    return _load_raw().get("symbols", [])


def get_symbol_by_type(symbol_type: str) -> dict[str, Any] | None:
    for s in get_symbols():
        if s.get("type") == symbol_type:
            return s
    return None

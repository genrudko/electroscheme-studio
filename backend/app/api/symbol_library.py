"""API router for the GOST symbol library."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.core.symbol_service import get_library, get_symbol_by_type

router = APIRouter(prefix="/api/symbols", tags=["symbols"])


@router.get("")
def list_symbols():
    return get_library()


@router.get("/{symbol_type}")
def get_symbol(symbol_type: str):
    sym = get_symbol_by_type(symbol_type)
    if sym is None:
        raise HTTPException(status_code=404, detail=f"Symbol type '{symbol_type}' not found")
    return sym

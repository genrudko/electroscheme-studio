"""Pydantic models for the GOST symbol library."""

from __future__ import annotations

from pydantic import BaseModel


class GostReference(BaseModel):
    id: str
    title: str
    description: str
    status: str


class SymbolCategory(BaseModel):
    id: str
    name: str
    gost: str


class SymbolTerminal(BaseModel):
    id: str
    rx: float
    ry: float


class SymbolState(BaseModel):
    id: str
    name: str
    alternate_svg: str | None = None


class SymbolDefinition(BaseModel):
    id: str
    type: str
    name: str
    category: str
    gost: str
    gost_ref: str
    viewBox: str
    default_width: float
    default_height: float
    terminals: list[SymbolTerminal]
    default_properties: dict[str, str] = {}
    svg: str
    interactive: bool = False
    default_state: str = "normal"
    current_state: str = "normal"
    states: list[SymbolState] = []
    # ГОСТ compliance metadata
    letter_designation: str = ""          # ГОСТ 2.710-81 (R, C, Q, QS, TA, ...)
    module_width: float = 0.0             # модульная ширина УГО, мм
    module_height: float = 0.0            # модульная высота УГО, мм
    line_width_main: float = 0.8          # толщина линии связи, мм
    line_width_contour: float = 0.4       # толщина контура УГО, мм


class SymbolLibrary(BaseModel):
    version: str = "1.0"
    description: str = ""
    gost_references: list[GostReference] = []
    categories: list[SymbolCategory] = []
    symbols: list[SymbolDefinition] = []

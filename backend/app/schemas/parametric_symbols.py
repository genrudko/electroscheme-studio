from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


BusbarOrientation = Literal["horizontal", "vertical"]
BusbarConnectionSide = Literal["top", "bottom", "both"]
BaySlotSide = Literal["top", "bottom", "left", "right"]
RoutingDirection = Literal["up", "down", "left", "right"]


class BusbarPreviewRequest(BaseModel):
    id: str = Field(default="param_busbar_1", min_length=1)
    name_ru: str = Field(default="Шина")
    voltage_kv: float = Field(default=35.0, ge=0.4, le=1150.0)
    length: float = Field(default=260.0, ge=80.0, le=1200.0)
    connection_count: int = Field(default=6, ge=0, le=64)
    connection_side: BusbarConnectionSide = "bottom"
    orientation: BusbarOrientation = "horizontal"
    stroke_width: float = Field(default=4.0, ge=1.0, le=16.0)
    margin: float = Field(default=20.0, ge=5.0, le=80.0)
    lead_length: float = Field(default=24.0, ge=0.0, le=120.0)
    bay_depth: float = Field(default=90.0, ge=20.0, le=260.0)


class ParametricTerminal(BaseModel):
    id: str
    x: float
    y: float
    role: Literal["busbar_connection", "busbar_end", "parameterized_connection"]
    side: Literal["top", "bottom", "left", "right", "center"]
    index: int | None = None


class ParametricBaySlot(BaseModel):
    id: str
    terminal_id: str
    index: int
    side: BaySlotSide
    bus_x: float
    bus_y: float
    terminal_x: float
    terminal_y: float
    equipment_anchor_x: float
    equipment_anchor_y: float
    preferred_routing_direction: RoutingDirection
    allowed_equipment_kinds: list[str] = Field(default_factory=list)
    reserved: bool = False


class ParametricSymbolPreview(BaseModel):
    schema_version: str = "parametric-symbol-preview-0.2"
    id: str
    name_ru: str
    kind: Literal["busbar"]
    review_status: str = "parametric_preview"
    viewBox: dict[str, float]
    svg_fragment: str
    terminals: list[ParametricTerminal]
    snap_anchors: list[ParametricTerminal]
    bay_slots: list[ParametricBaySlot] = Field(default_factory=list)
    parameters: BusbarPreviewRequest
    capabilities: dict
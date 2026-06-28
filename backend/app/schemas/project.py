"""Pydantic domain models for ElectroScheme Studio projects."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class Terminal(BaseModel):
    """Connection point on a symbol."""

    id: str
    x: float
    y: float


class Waypoint(BaseModel):
    """An intermediate bend point on a connection (sheet coordinates, mm)."""

    x: float
    y: float


class SchemeSymbol(BaseModel):
    """An electrical symbol placed on a sheet."""

    id: str
    type: str
    label: str
    x: float
    y: float
    width: float | None = None
    height: float | None = None
    rotation: float | None = None
    terminals: list[Terminal] = []
    current_state: str | None = None
    properties: dict[str, Any] = {}


# Allowed values for Connection fields
RouteMode = Literal["straight", "ortho", "manual"]
ConnectionKind = Literal["wire", "control", "bus", "polyline"]


class Connection(BaseModel):
    """A connection between two terminals.

    JSON uses ``"from"`` / ``"to"`` keys which are Python keywords,
    so we alias them to ``from_ref`` / ``to_ref``.

    ``route_mode`` controls how the connection is rendered when
    ``points`` is empty:

      * ``straight`` — direct line (legacy behaviour)
      * ``ortho``    — Manhattan-style right-angle polyline (L or Z)
      * ``manual``   — follow ``points`` exactly

    ``kind`` selects the visual class:

      * ``wire``     — primary power line (default, 0.6 mm)
      * ``control``  — secondary / control wiring (0.4 mm)
      * ``bus``      — busbar segment (1.0 mm)
      * ``polyline`` — generic graphical polyline (0.4 mm)

    ``points`` are intermediate bend vertices in sheet coordinates (mm).
    They are appended after ``from`` and before ``to`` when rendering.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    from_ref: str = Field(alias="from")
    to_ref: str = Field(alias="to")
    points: list[Waypoint] = []
    route_mode: RouteMode = "straight"
    kind: ConnectionKind = "wire"


class Sheet(BaseModel):
    """A drawing sheet in the project."""

    id: str
    name: str
    format: str = "A3"
    orientation: str = "landscape"
    width_mm: float = 420
    height_mm: float = 297


class ProjectMeta(BaseModel):
    """Project metadata."""

    name: str
    code: str = ""


class Project(BaseModel):
    """Root project model -- the single source of truth."""

    version: str = "0.1"
    project: ProjectMeta
    sheets: list[Sheet] = []
    symbols: list[SchemeSymbol] = []
    connections: list[Connection] = []

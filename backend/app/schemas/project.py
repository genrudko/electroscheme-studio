"""Pydantic domain models for ElectroScheme Studio projects."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Terminal(BaseModel):
    """Connection point on a symbol."""

    id: str
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
    properties: dict[str, Any] = {}


class Connection(BaseModel):
    """A connection between two terminals.

    JSON uses ``"from"`` / ``"to"`` keys which are Python keywords,
    so we alias them to ``from_ref`` / ``to_ref``.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    from_ref: str = Field(alias="from")
    to_ref: str = Field(alias="to")


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

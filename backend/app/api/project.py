"""Project API routes."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.project_service import get_current_project, set_current_project
from app.schemas.project import Project

router = APIRouter(prefix="/api", tags=["project"])


@router.get("/project")
def get_project() -> dict:
    """Return the current in-memory project."""
    return get_current_project().model_dump(by_alias=True)


@router.put("/project")
def update_project(payload: Project) -> dict:
    """Replace the current in-memory project."""
    set_current_project(payload)
    return {"status": "ok"}

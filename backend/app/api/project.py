"""Project API routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.core.project_service import get_current_project, set_current_project
from app.schemas.project import Connection, Project, SchemeSymbol

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


@router.post("/project/symbols")
def add_symbol(payload: SchemeSymbol) -> dict:
    """Add a new symbol to the current project."""
    project = get_current_project()
    if any(s.id == payload.id for s in project.symbols):
        raise HTTPException(status_code=409, detail=f"Symbol id '{payload.id}' already exists")
    project.symbols.append(payload)
    set_current_project(project)
    return {"status": "ok", "symbol_id": payload.id}


@router.delete("/project/symbols/{symbol_id}")
def delete_symbol(symbol_id: str) -> dict:
    """Remove a symbol from the current project."""
    project = get_current_project()
    before = len(project.symbols)
    project.symbols = [s for s in project.symbols if s.id != symbol_id]
    if len(project.symbols) == before:
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol_id}' not found")
    project.connections = [
        c for c in project.connections
        if not c.from_ref.startswith(symbol_id + ".") and not c.to_ref.startswith(symbol_id + ".")
    ]
    set_current_project(project)
    return {"status": "ok", "symbol_id": symbol_id}


@router.post("/project/connections")
def add_connection(payload: Connection) -> dict:
    """Add a new connection between two terminals."""
    project = get_current_project()
    if any(c.id == payload.id for c in project.connections):
        raise HTTPException(
            status_code=409,
            detail=f"Connection id '{payload.id}' already exists",
        )
    project.connections.append(payload)
    set_current_project(project)
    return {"status": "ok", "connection_id": payload.id}


@router.put("/project/connections/{connection_id}")
def update_connection(connection_id: str, payload: Connection) -> dict:
    """Replace an existing connection (used for waypoints/kind edits)."""
    project = get_current_project()
    for i, c in enumerate(project.connections):
        if c.id == connection_id:
            payload.id = connection_id
            project.connections[i] = payload
            set_current_project(project)
            return {"status": "ok", "connection_id": connection_id}
    raise HTTPException(status_code=404, detail=f"Connection '{connection_id}' not found")


@router.delete("/project/connections/{connection_id}")
def delete_connection(connection_id: str) -> dict:
    """Remove a connection from the current project."""
    project = get_current_project()
    before = len(project.connections)
    project.connections = [c for c in project.connections if c.id != connection_id]
    if len(project.connections) == before:
        raise HTTPException(status_code=404, detail=f"Connection '{connection_id}' not found")
    set_current_project(project)
    return {"status": "ok", "connection_id": connection_id}

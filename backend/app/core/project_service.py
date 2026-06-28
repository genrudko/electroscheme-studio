"""Project loading, storage, and serialisation."""

from __future__ import annotations

import json
from pathlib import Path

from app.schemas.project import Project


_current_project: Project | None = None

_EXAMPLES_DIR = Path(__file__).resolve().parents[3] / "examples"


def get_demo_project() -> Project:
    """Load the demo project from the examples directory."""
    path = _EXAMPLES_DIR / "minimal_project.electroscheme.json"
    return load_project_file(path)


def load_project_file(path: Path) -> Project:
    """Parse a ``.electroscheme.json`` file into a *Project*."""
    with open(path, encoding="utf-8-sig") as fh:
        data = json.load(fh)
    return Project.model_validate(data)


def save_project_file(project: Project, path: Path) -> None:
    """Serialise a *Project* to a JSON file."""
    data = project.model_dump(by_alias=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def get_current_project() -> Project:
    """Return the in-memory project (lazy-loads the demo)."""
    global _current_project
    if _current_project is None:
        _current_project = get_demo_project()
    return _current_project


def set_current_project(project: Project) -> None:
    """Replace the in-memory project."""
    global _current_project
    _current_project = project

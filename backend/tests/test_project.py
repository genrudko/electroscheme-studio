"""Smoke tests for domain models, project service, and legacy endpoints."""

from app.schemas.project import (
    Connection, Project, ProjectMeta, SchemeSymbol, Sheet, Terminal,
)
from app.core.project_service import get_demo_project
from app.main import health, demo_project


def test_models():
    t = Terminal(id="t1", x=10, y=20)
    assert t.id == "t1"

    s = SchemeSymbol(
        id="q1", type="circuit_breaker", label="Q1",
        x=100, y=100, terminals=[t],
    )
    assert len(s.terminals) == 1

    c = Connection.model_validate({"id": "c1", "from": "busbar.t1", "to": "q1.a"})
    assert c.from_ref == "busbar.t1"
    dumped = c.model_dump(by_alias=True)
    assert dumped["from"] == "busbar.t1"
    assert dumped["to"] == "q1.a"

    p = Project(
        version="0.1",
        project=ProjectMeta(name="Test", code="test"),
        sheets=[Sheet(id="s1", name="Sheet 1")],
    )
    data = p.model_dump(by_alias=True)
    p2 = Project.model_validate(data)
    assert p2.project.name == "Test"
    print("  model tests: OK")


def test_demo_load():
    p = get_demo_project()
    assert p.version == "0.1"
    assert p.project.name == "Minimal Demo"
    assert len(p.symbols) == 2
    assert len(p.connections) == 1
    assert p.connections[0].from_ref == "busbar_1.t1"
    print("  demo project load: OK")


def test_legacy_endpoints():
    assert health()["status"] == "ok"
    assert demo_project()["version"] == "0.1"
    print("  legacy endpoints: OK")


if __name__ == "__main__":
    test_models()
    test_demo_load()
    test_legacy_endpoints()
    print("All smoke tests passed.")

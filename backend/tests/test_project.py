"""Smoke tests for domain models, project service, legacy endpoints,
and the new connection model (route_mode / kind / waypoints)."""

from app.schemas.project import (
    Connection, Project, ProjectMeta, SchemeSymbol, Sheet, Terminal, Waypoint,
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
    assert c.route_mode == "straight"
    assert c.kind == "wire"
    assert c.points == []
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


def test_connection_with_waypoints():
    """A connection with explicit waypoints and manual routing round-trips
    through model_dump / model_validate without losing data."""
    c = Connection.model_validate({
        "id": "c2",
        "from": "a.x",
        "to": "b.y",
        "route_mode": "manual",
        "kind": "control",
        "points": [{"x": 10, "y": 20}, {"x": 30, "y": 40}],
    })
    assert c.route_mode == "manual"
    assert c.kind == "control"
    assert len(c.points) == 2
    assert c.points[0].x == 10 and c.points[0].y == 20
    dumped = c.model_dump(by_alias=True)
    c2 = Connection.model_validate(dumped)
    assert c2.points[1].x == 30 and c2.points[1].y == 40
    print("  connection waypoints: OK")


def test_demo_load():
    p = get_demo_project()
    assert p.version == "0.1"
    assert p.project.name == "ElectroScheme Demo"
    assert len(p.symbols) == 7
    assert len(p.connections) == 8
    # The demo includes both ortho and manual routes
    ortho = [c for c in p.connections if c.route_mode == "ortho"]
    manual = [c for c in p.connections if c.route_mode == "manual"]
    assert len(ortho) == 7
    assert len(manual) == 1
    assert manual[0].kind == "control"
    assert len(manual[0].points) == 2
    print(f"  demo project load: OK ({len(p.connections)} connections)")


def test_legacy_endpoints():
    assert health()["status"] == "ok"
    assert demo_project()["version"] == "0.1"
    print("  legacy endpoints: OK")


if __name__ == "__main__":
    test_models()
    test_connection_with_waypoints()
    test_demo_load()
    test_legacy_endpoints()
    print("All smoke tests passed.")

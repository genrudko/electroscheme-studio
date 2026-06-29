# Clean interactive busbar review canvas

## Problem

The first patch_026 attempt failed because the generated builder called `write_text()` without defining it.

## Repair

The builder now explicitly defines:

```python
def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
```

The interactive page is still generated from parametric busbar previews, not from static SVG snapshots.

## Coordinate contract

Each review card has one SVG coordinate system for:

```text
grid
busbar
bay slot markers
bay number labels
bus caption
alignment guides
drag math
```

This is the correct base for manual text placement experiments.
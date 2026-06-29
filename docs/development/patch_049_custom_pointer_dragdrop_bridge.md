# Patch 049 — custom pointer drag/drop bridge

## Decision

The project must restore real drag'n'drop. `click-to-place` is not used.

## Fix

The palette now performs deterministic pointer-based drag'n'drop:

```text
pointerdown on palette item
pointermove beyond threshold
pointerup anywhere
window custom event -> CanvasViewport placement
```

The custom event is:

```text
electroscheme:palette-pointer-drop
```

CanvasViewport handles it and places the payload via:

```text
worldPointFromClient(...)
```

This avoids reliance on native HTML5 `DragEvent` propagation through SVG/canvas layers while preserving the actual press-drag-release UX.

## Smoke wording

The exact smoke phrase is intentionally recorded here:

```text
click-to-place is not used
```

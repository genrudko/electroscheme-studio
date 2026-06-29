# Patch 047 — global palette drop bridge

## Problem

Patch 046 passed all build gates, but the browser still did not place figures from the palette. A canvas-bound `pointerup` fallback is not reliable enough when the pointer starts in the palette and ends over an SVG/canvas subtree.

## Fix

CanvasViewport now registers global capture listeners:

```text
pointermove
pointerup
dragover
dragend
```

While a palette payload exists, the canvas remembers the last client coordinate and places the payload through:

```text
worldPointFromClient(...)
```

Supported payloads:

```text
planned VSDX item -> temporary labelled placeholder
available command item -> existing handleCommandAtPoint(...)
```

Native HTML5 drag/drop remains in place, but this patch does not depend on it.

# Patch 046 — pointer fallback for palette drag/drop

## Problem

Native HTML5 drag/drop still does not work reliably from the left palette in the current UI.

## Fix

A shared drag transfer module was added:

```text
frontend/src/lib/editor/paletteDragTransfer.ts
```

The palette now stores the dragged item on:

```text
pointerdown
dragstart
```

The canvas now also handles:

```text
pointerup.capture
```

If a planned VSDX payload exists and the pointer is released over the canvas, the canvas creates a temporary labelled placeholder.

Native drag/drop remains as a secondary path.

# Patch 050 — disable native HTML5 DnD and force custom pointer drag

## Problem

The previous pointer bridge still did not place objects. The likely cause is native HTML5 drag on `button` palette cards hijacking the pointer stream.

## Fix

Palette cards are no longer native-draggable. Real drag'n'drop is now implemented as custom pointer DnD:

```text
pointerdown on palette item
prevent default native drag/button selection
pointermove threshold >= 4 px
visible drag ghost
pointerup
custom event to CanvasViewport
worldPointFromClient(...)
place placeholder or execute command
```

This is still drag'n'drop:

```text
press -> drag -> release
```

It is not click-to-place.

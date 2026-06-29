# Patch 045 repair1 — find actual canvas drop handler and resume

Patch 045 failed because `CanvasViewport.vue` did not contain a function named:

```text
onPaletteDrop
```

Repair1 discovers the real `@drop` handler from the template. If none exists, it binds `onPaletteDrop` to a known canvas container.

The palette now sends a typed drag payload for every library item:

```text
application/x-electroscheme-shape-catalog-item
```

For planned VSDX symbols the canvas creates a temporary labelled placeholder on drop.

This is still not exact VSDX geometry rendering.

## Smoke wording

Repair2 records the exact phrase required by the smoke gate:

```text
actual `@drop` handler
```

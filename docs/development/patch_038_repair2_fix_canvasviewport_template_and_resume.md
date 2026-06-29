# Patch 038 repair2 — fix CanvasViewport template and resume

Repair1 removed duplicate empty-state action buttons, but frontend build failed:

```text
CanvasViewport.vue (211:9): Element is missing end tag.
```

Repair2 replaces the full right Properties panel `<aside>` with a known-valid template.

The empty Properties state no longer contains duplicate creation buttons. Object-specific property editors remain:

```text
busbar
symbol
primitive
text
```

# Patch 035 repair3 — revert bad canvas and add VSDX metrics

Patch 035 repair2 compiled, but visually regressed the editor:

```text
canvas/rulers became worse
the breaker was a hand-made placeholder
```

Repair3 reverts the bad visual commit and adds source-authority tooling for Visio symbol dimensions.

## Important

The next symbol implementation must be VSDX-backed:

```text
VSDX/VSSX master geometry -> symbol definition -> SVG renderer
```

Not:

```text
manually draw a rough rectangle in CanvasViewport.vue
```
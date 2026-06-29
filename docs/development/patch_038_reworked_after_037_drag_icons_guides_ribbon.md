# Patch 038 reworked after patch 037 — drag, icons, guides and Ribbon

## Reason

Patch 037 passed gates, but frontend build emitted non-fatal warnings:

```text
Duplicate key "svgPreview" in shapeCatalog.ts
```

That was a real visual/behavior bug: available figure cards could receive wrong preview icons and library behavior became unstable.

## Fixes

```text
Clean shapeCatalog.ts, no duplicate svgPreview keys.
Restore robust ShapePalette dragstart behavior.
SVG preview children no longer intercept pointer/drag events.
Planned status is shown as a compact icon, not a long text badge.
Long figure names wrap instead of clipping.
Horizontal guide drag is repaired when the CanvasViewport guide markup matches known structure.
Guide lines are thinner, more transparent and more dashed.
Right empty Properties panel no longer duplicates Add busbar/Add text.
Redundant Ribbon Busbars/Bays tab is removed.
Ribbon collapse and UI scale are introduced.
```

## Next UI architecture step

The Ribbon should be converted from ad-hoc blocks to a declarative command model:

```text
RibbonTab -> RibbonGroup -> RibbonCommand
```

That will make it possible to reproduce Visio-like tabs without hardcoding button fragments inside one component.

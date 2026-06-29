# Patch 038 — guides, properties panel and Visio-like Ribbon UI foundation

## Fixed / improved

```text
Horizontal guide drag target is repaired when the local CanvasViewport structure matches known guide markup.
Guide lines are visually demoted: thinner, more transparent, more frequent dash pattern.
Long figure names in the left library are allowed to wrap instead of being clipped.
The empty right Properties panel no longer duplicates library actions with Add busbar/Add text buttons.
The redundant Busbars/Bays Ribbon tab is removed from the visible tab array.
Ribbon gets a collapse/expand control.
UI scale is added to CanvasSettings and exposed in Ribbon controls.
```

## New UI settings

```text
uiScale: 0.8 … 1.35, default 1.0
ribbonCollapsed: boolean, default false
```

## Note

This patch does not complete the final Visio-like Ribbon architecture. It removes rough duplication and adds the first permanent Ribbon layout controls. The next step should be a tab-by-tab Ribbon command model instead of ad-hoc groups inside one component.

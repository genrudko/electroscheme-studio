# Patch 058 — structural View Ribbon groups

## Problem

The brute-force horizontal CSS from patch 057 made the Ribbon worse by squeezing all View controls into one unreadable row.

## Fix

The View tab panel in `RibbonBar.vue` is structurally rewritten into explicit command groups while reusing the existing Vue-bound controls extracted from the original template:

```text
Канвас
Отображение и привязки
Направляющие
```

Controls are arranged horizontally by groups. Inside large groups controls use a compact two-row grid, without inner vertical scrollbar and without text overlap.

## Scope

No drag/drop, model, renderer, canvas, or equipment logic changes.

# Patch 052 — units, busbar limit and ruler mm labels

## User-facing changes

```text
Busbar connection count limit: 40 -> 100
Busbar cell step label: explicitly мм
View grid step label: explicitly мм
View tolerance label: explicitly мм
Ruler: intermediate numeric labels appear between major values when zoomed enough
Ruler unit: мм
```

## Implementation notes

`frontend/src/lib/editor/rulerMmOverlay.ts` observes existing ruler DOM labels and adds smaller intermediate labels only when there is enough screen distance between two major values.

This keeps the current ruler scaling logic intact and only improves readability at zoom.

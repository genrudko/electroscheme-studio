# Patch 043 — palette text flow and canvas placeholder cleanup

## Fixed

```text
No-icon palette cards are forced to one text column.
Palette titles no longer use aggressive anywhere-breaking.
Decorative empty-canvas/page-format texts are removed from frontend sources when present.
Editor chrome and SVG text are not selectable during selection drag.
Common empty/page placeholder classes are hidden.
```

## Removed UI noise

```text
ПУСТОЙ КАНВАС
А3 альбомная
```

These labels do not help editing and interfere with selection gestures.

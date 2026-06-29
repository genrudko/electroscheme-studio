# Patch 038 repair1 — remove duplicate empty Properties buttons

The reworked patch 038 failed at smoke because `CanvasViewport.vue` still contained old empty-state buttons:

```text
Добавить шину
Добавить текст
```

Those actions are duplicated and should not live in the empty Properties panel. Figure creation belongs to:

```text
left shape library
Ribbon
context menu
```

Repair1 removes the old buttons and resumes the patch gates.

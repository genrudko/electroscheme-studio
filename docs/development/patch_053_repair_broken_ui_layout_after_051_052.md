# Patch 053 — repair broken UI layout after patch 051/052

## Problem

Screenshots after patch 051/052 showed that the UI was still visually poor and the ribbon layout became broken: the active View tab expanded into a giant form area and reduced the drawing workspace.

The patch 052 ruler DOM overlay also did not solve intermediate ruler labels reliably.

## Fix

```text
compact ribbon max height
horizontal ribbon group flow
compact controls in View tab
remove broken DOM ruler overlay side-effect import
hide ruler overlay DOM labels
keep busbar/mm constants and labels from patch 052
keep drag/drop logic untouched
```

## Note

Intermediate ruler labels still need a proper implementation inside the real ruler renderer. The patch 052 DOM-guessing overlay is disabled because it is not reliable enough.

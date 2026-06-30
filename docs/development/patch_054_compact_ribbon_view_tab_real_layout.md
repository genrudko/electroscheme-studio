# Patch 054 — compact real ribbon layout

## Problem

After patch 053 the active View tab was still rendered like a large form block. The issue is that earlier CSS treated direct children of the ribbon content as command groups, but in the actual DOM they can be full tab panels.

## Fix

```text
direct children of ribbon content are neutral wrappers
nested sections/groups/fieldsets are compact command islands
ribbon total height is capped to 92 px
active tab content is a horizontal strip
labels/inputs/buttons are inline and compact
```

No drag/drop logic is changed.

# Patch 057 — force Ribbon controls horizontal

## Problem

After patch 056 the UI became stable again, but Ribbon controls are still stacked vertically and the ribbon body shows an internal vertical scrollbar.

## Fix

```text
Ribbon body height: compact 46 px
Ribbon body layout: row nowrap
Nested Ribbon wrappers: flattened to horizontal inline-flex
Labels: label + control in one row
Inner vertical scrollbar: disabled
Overflow strategy: horizontal scroll only if controls do not fit
```

## Scope

No drag/drop, model, renderer, or equipment logic changes.

## Repair1

Repair1 fixes only the missing smoke marker and resumes build/commit.

```text
horizontal scroll only
```

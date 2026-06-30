# Patch 059 — expand View ribbon and unclip controls

## Problem

Patch 058 made the View tab structure cleaner, but the ribbon is too low. Controls in groups are clipped.

## Fix

```text
Ribbon max height increased moderately
View panel height: 96 px
Command group height: 84 px
Canvas group uses 3 compact rows
Display group remains 2 rows with more room
No inner vertical scroll
```

## Scope

No drag/drop, model, renderer, canvas, or equipment logic changes.

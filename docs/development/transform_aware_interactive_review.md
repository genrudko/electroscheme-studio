# Transform-aware interactive review

## Problem

The interactive review page embeds SVG snapshots. Some labels are inside transformed SVG groups. The previous logic mixed coordinate systems:

```text
text label x/y = local element coordinates
guide line x/y = root SVG coordinates
```

That is why the guide crosshair could appear above/left of the actual label.

## Fix

Dragging now uses this pipeline:

```text
screen pointer
в†’ root SVG point
в†’ snapping / guide calculation in root coordinates
в†’ conversion back into the text element local coordinate system
в†’ x/y write-back to the label
```

Guide candidates are also collected in root coordinates using SVG CTM transforms.

## Grid-aligned default

The default busbar `end_slot_offset` is changed from `14` to `12`.
With current defaults:

```text
margin = 24
end_slot_offset = 12
connection_spacing = 48
guide grid = 6
```

bay slot centers land on grid-aligned coordinates.
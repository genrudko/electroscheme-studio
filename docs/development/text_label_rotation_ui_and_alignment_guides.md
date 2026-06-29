# Text label rotation UI and alignment guides

## User feedback

The previous patch technically added rotation, but it was not obvious how to use it. Text placement also needed helper guide lines to align labels neatly against objects and other labels.

## Changes

### Common text tools

The Parametric Busbar panel now has a dedicated `Text tools` block at the top:

```text
Selected text
0°
+90°
-90°
180°
Reset
Show alignment guides
Snap text to guides
Snap tolerance
Guide grid step
```

This applies to both:

```text
bus-label
bay-label
```

### Selection

Click any text label in the preview:

```text
1С 10 кВ
1
2
3
...
```

The selected text is shown in the `Text tools` block.

### Rotation

After selecting a label, use:

```text
0°
+90°
-90°
180°
```

This is clearer than the previous separated controls.

### Alignment guides

During drag, guide lines are drawn against:

```text
bay slot centers
busbar edges
busbar center lines
other text labels
grid step
```

If snapping is enabled, nearby guides are highlighted and the text snaps to them.

### Interactive review

`visual_checks/parametric_busbar/interactive.html` now also supports:

```text
select text
drag text
alignment guides
rotation toolbar
```

This is for visual experimentation only and does not write model JSON.

## Next expected check

Open:

```text
visual_checks/parametric_busbar/interactive.html
```

and test:

```text
drag bus caption
drag bay number
snap to bay slot center
snap to another text baseline
rotate selected text
```
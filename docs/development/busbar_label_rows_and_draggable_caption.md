# Busbar label rows and draggable caption

## Feedback addressed

1. In both-side busbar mode, top and bottom labels overlapped.
2. The busbar dispatcher caption could collide with the busbar.
3. The caption must be movable like a Visio pinned text box.
4. The caption must support rotation presets.
5. The previous end-slot offset was visually too small.

## Label rows

For horizontal busbars:

- one-side mode keeps labels above the busbar;
- both-side mode can use separate rows:
  - top-side slots above;
  - bottom-side slots below.

For vertical busbars:

- both-side mode can split labels to left/right rows.

## Bus caption

New parameters:

```text
bus_label_gap
bus_label_offset_x
bus_label_offset_y
bus_label_rotation_mode
bus_label_rotation_deg
```

The frontend supports:

```text
0°
+90°
-90°
180°
```

The caption can also be dragged directly in the preview. The drag changes `bus_label_offset_x` and `bus_label_offset_y`.

## End offset

Default `end_slot_offset` is now 14 instead of 6.25 because the previous value was visually too small in the review snapshot.

## Next visual check

Open:

```text
visual_checks/parametric_busbar/index.html
```

and verify:

- both-side labels no longer overlap;
- caption no longer sits on the busbar;
- larger end offset looks visually correct;
- drag and rotation behavior in the WebUI panel is usable.
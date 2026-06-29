# Draggable and rotatable bay number labels

## User feedback

The interactive review works, but cell number labels also need:

```text
manual movement
rotation presets
```

## Model additions

```text
TextLabelOverride
bay_label_default_rotation_deg
bay_label_overrides
```

Each bay slot label can now have an override keyed by bay slot id:

```json
{
  "bay_slot_bottom_1": {
    "offset_x": 8,
    "offset_y": -4,
    "rotation_deg": 90
  }
}
```

## SVG contract

Bay number labels are rendered with:

```text
data-role="bay-label"
data-bay-slot-id="..."
data-draggable="true"
data-rotation="..."
```

This makes them selectable and draggable in the UI and in the interactive review page.

## Frontend behavior

In the Parametric Busbar panel:

- drag a cell number label to set its X/Y offset;
- click/drag a number to select it;
- use presets `0°`, `+90°`, `-90°`, `180°`;
- use `All 0°`, `All +90°`, `All -90°` for global default rotation.

## Visual review

The interactive visual page now supports both:

```text
bus captions
bay number labels
```

The browser capture tool was made more robust by adding a temporary browser profile and a fallback screenshot mode.
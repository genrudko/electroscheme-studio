# Parametric busbar bay slot numbering

## Purpose

Bay/cell numbering on busbars is not decorative text.

It is part of the engineering model because automatic scheme generation must be able to bind equipment, bay slots and labels together.

## User requirement

The model must support numbering cells above bay slots on busbars.

## New request parameters

```text
bay_numbering_enabled
bay_numbering_prefix
bay_numbering_start
bay_numbering_step
bay_label_position
bay_label_offset
```

Default:

```text
enabled = true
prefix = "Яч. "
start = 1
step = 1
position = above
```

## New bay slot fields

```text
label_number
label
label_x
label_y
```

Example:

```json
{
  "id": "bay_slot_bottom_3",
  "terminal_id": "tap_bottom_3",
  "label_number": 3,
  "label": "Яч. 3"
}
```

## SVG rendering

Labels are rendered as SVG `<text>` elements with:

```text
font-family: Arial
font-size: 10
text-anchor: middle
dominant-baseline: middle
```

The label remains linked to the bay slot through:

```text
data-bay-slot-id
```

## Why this matters

Later, when the auto-generator creates an RU section, bay slots can be assigned real cell numbers:

```text
1С-35:
  bay_slot_bottom_1 → Яч. 1
  bay_slot_bottom_2 → Яч. 2
  bay_slot_bottom_3 → Яч. 3
```

Then equipment placement can depend on this mapping:

```text
cell number
→ bay slot
→ equipment
→ terminal
→ routed connection
```

## Next direction

Recommended next patch:

```text
patch_017_parametric_busbar_project_placement
```

It should place a generated parametric busbar instance into the project canvas/model.
# Parametric busbar bay slot model

## Purpose

A busbar is not just a thick SVG line with connection taps.

For automatic scheme generation, a busbar must expose semantic bay slots that describe where equipment can be placed and how it should be connected.

## New model

`ParametricSymbolPreview` now includes:

```text
bay_slots: ParametricBaySlot[]
```

Each slot includes:

```text
id
terminal_id
index
side
bus_x / bus_y
terminal_x / terminal_y
equipment_anchor_x / equipment_anchor_y
preferred_routing_direction
allowed_equipment_kinds
reserved
```

## Why this matters

The future auto-layout pipeline can now work like this:

```text
busbar section
→ generated bay slots
→ select equipment for each slot
→ place equipment at equipment_anchor
→ connect equipment terminal to busbar terminal
→ route wire in preferred direction
```

## Current behavior

For horizontal busbars:

- top connections create top bay slots;
- bottom connections create bottom bay slots.

For vertical busbars:

- `top` option maps to left-side slots;
- `bottom` option maps to right-side slots.

This keeps the old UI compatible while giving the layout engine real directional semantics.

## Next direction

Recommended next functional patch:

```text
patch_016_parametric_busbar_project_placement
```

That patch should let the project model place a parametric busbar instance on the canvas, instead of only previewing it.
# Parametric busbar visual alignment

## Why this patch exists

User feedback on the visual review was explicit:

- bay slots must be rendered inside the busbar;
- labels must resemble the Visio examples;
- core parameters must include voltage class, point spacing, point count and bus thickness.

## Main changes

### 1. Busbar body

The busbar is now rendered as a rectangle instead of a thick line.

This is closer to the Visio stencil behavior and makes internal slot points look correct.

### 2. Internal slot markers

Bay slot markers are now drawn as circles inside the busbar body.

They are still semantic bay slots for auto-generation, but visually they are part of the busbar.

### 3. Number labels

Default visual behavior:

- horizontal busbar: slot numbers above the busbar;
- vertical busbar: slot numbers at the side of the busbar.

### 4. Bus caption

A dedicated bus label is supported, for example:

```text
1С 10 кВ
```

### 5. Parameters

The review panel now exposes:

```text
voltage_kv
connection_count
connection_spacing
thickness_mm
slot_diameter
bus_label
bus_label_position
bay_numbering_style
```

## Visual review policy

After geometry changes, regenerate visual review snapshots and inspect them before further UI or placement work.
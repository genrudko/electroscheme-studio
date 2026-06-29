# Parametric busbar end slot offset

## User feedback

The visual model is now close, but the distance from the first and last bay slots to the end of the busbar must be a defined parameter.

## Added parameters

```text
end_slot_offset
fit_length_to_slots
```

Default:

```text
end_slot_offset = 6.25
fit_length_to_slots = true
```

## Geometry rule

When `fit_length_to_slots = true`:

```text
bus_length = 2 * end_slot_offset + connection_spacing * (connection_count - 1)
```

Slot positions:

```text
slot_1 = bus_start + end_slot_offset
slot_n = slot_1 + connection_spacing * (n - 1)
```

This matches the Visio-like parameterization:

```text
distance from edge to first slot
spacing between slots
number of points
bus thickness
```

## Why this matters

The bar length is no longer visually arbitrary. It is now derived from the actual electrical layout parameters.

This is necessary before using busbars as the basis for automatic scheme generation.
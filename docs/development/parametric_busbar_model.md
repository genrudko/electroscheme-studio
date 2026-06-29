# Parametric busbar model

## Purpose

This patch introduces the first real parametric symbol family: busbar.

Busbars must not be treated as static imported SVG fragments only. They need parameters because they are structural elements for both manual editing and automatic scheme generation.

## Backend

Added:

```text
backend/app/schemas/parametric_symbols.py
backend/app/core/parametric_busbar.py
backend/app/api/parametric_symbols.py
```

API:

```text
GET  /api/parametric-symbols/busbar/default
POST /api/parametric-symbols/busbar/preview
```

## Parameters

```text
length
connection_count
connection_side
orientation
stroke_width
margin
lead_length
voltage_kv
```

## Generated model

The API returns:

```text
viewBox
svg_fragment
terminals
snap_anchors
parameters
capabilities
```

## Why this matters

Automatic scheme generation will need to create bus sections first, then place bays and connect equipment to generated busbar terminals.

```text
bus section
→ generated connection points
→ bay placement
→ equipment terminals
→ routed connections
```

## Current limitations

- The model is preview-only.
- It is not persisted into project files yet.
- It is not converted into core SymbolDefinition yet.
- It does not yet support named bay slots.

## Next development direction

Recommended next patches:

```text
patch_015_parametric_busbar_project_placement
patch_016_busbar_bay_slot_model
patch_017_switching_device_state_model
```
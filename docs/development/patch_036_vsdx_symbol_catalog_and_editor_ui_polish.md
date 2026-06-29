# Patch 036 — VSDX-backed symbol catalog and editor UI polish

## Why

Manual placeholders for electrical symbols are not acceptable. Symbol dimensions, connection points and raw ShapeSheet properties must come from the Visio VSDX/VSSX master library.

## What this patch adds

```text
tools/build_vsdx_symbol_catalog.py
frontend/src/lib/editor/vsdxSymbolCatalog.generated.ts
docs/source_authority/vsdx_symbol_catalog.generated.md
frontend/src/assets/editor-design-system.css
```

## Symbol catalog

The catalog now merges:

```text
core available editor objects
planned VSDX-backed symbols
```

VSDX-backed symbols are not yet rendered as exact SVG geometry. They are shown as planned library items with:

```text
master id
title
category
width/height in mm
connection point count
shape count
ShapeSheet Prop/User cell counts
semantic data fields
```

## Semantic fields

The generator adds scaffolding for engineering properties:

```text
transformers:
  winding_count
  primary_voltage_kv
  secondary_voltage_kv
  winding_connection_group
  neutral_grounding
  tap_changer

switching:
  switch_state
  truck_position
  control_mode
  connection_control_enabled

busbars/lines:
  voltage_class_id
  connection_point_count
  line_type
```

## UI polish

A global editor design-system CSS layer improves the left shape palette, Ribbon buttons and property panel without changing canvas logic.
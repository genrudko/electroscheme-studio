# Symbol library authoring strategy

## Decision

The symbol library is authoring-first and Visio-import-assisted.

The source of truth is not image recognition.

Preferred sources:

1. manually authored SymbolDefinition JSON;
2. Visio VSDX masters with vector geometry;
3. reviewed imported drafts.

Rejected as primary source:

```text
PDF screenshot → neural network recognition → production symbol
```

## SymbolDefinition requirements

Every symbol must eventually have:

```text
id
name_ru
name_en
category
viewBox
geometry or svg fragment
terminals
snap anchors
parameters
feature flags
capabilities
style policy
review status
source metadata
```

## Required feature flags

```json
{
  "colorizable_by_voltage_class": true,
  "multi_state_candidate": false,
  "busbar_configurable_connection_points": false,
  "rotatable": true,
  "snap_anchors_required": true,
  "stretchable_leads_candidate": false,
  "auto_layout_eligible": true,
  "requires_review": true
}
```

## Capabilities model

Symbols are interactive engineering objects.

Minimum capability groups:

```json
{
  "rotation": {
    "enabled": true,
    "allowed_degrees": [0, 90, 180, 270],
    "terminal_transform_required": true,
    "label_rotation_policy": "keep_readable"
  },
  "stretching": {
    "enabled": true,
    "body_geometry_locked": true,
    "stretchable_parts": ["connection_leads"]
  },
  "snapping": {
    "enabled": true,
    "snap_to_terminals": true,
    "snap_to_busbar_generated_points": true,
    "connection_graph_node_required": true
  },
  "voltage_style": {
    "enabled": true,
    "stroke_token": "var(--voltage-color)"
  }
}
```

## State variants

State variants must be modeled explicitly.

Example:

```json
{
  "states": {
    "closed": { "geometry_ref": "closed" },
    "open": { "geometry_ref": "open" },
    "unreliable": { "overlay": "question_mark" },
    "repair": { "overlay": "repair_marker" }
  }
}
```

## Busbar parameters

Busbar symbols must support parameters.

Example:

```json
{
  "parameters": {
    "orientation": "horizontal",
    "connection_count": 5,
    "connection_spacing": 40,
    "length": 240
  }
}
```

The renderer generates terminals from the parameters.

## Stretchable leads

Many symbols need adjustable lead length.

This is not the same as scaling the full symbol.

Correct:

```text
body locked
lead_in length changes
lead_out length changes
terminals move accordingly
connection graph preserved
```

Incorrect:

```text
scale whole symbol non-uniformly
distort breaker/transformer geometry
lose connection point positions
```

## Voltage style policy

Hard-coded imported colors should be normalized into style tokens.

Preferred token:

```text
var(--voltage-color)
```

The actual color is resolved by profile:

```text
normal_scheme
operational_scheme
ptk_dark
```

## Import review statuses

```text
needs_review
accepted
rejected
needs_manual_terminals
needs_state_mapping
needs_busbar_parameters
needs_rotation_check
needs_stretch_mapping
needs_snap_mapping
```

## Promotion to core library

A symbol may be promoted to core only after:

1. geometry preview checked;
2. terminals checked;
3. rotation checked;
4. snap anchors checked;
5. stretch behavior checked if applicable;
6. state variants checked if applicable;
7. voltage color behavior checked;
8. category and Russian name checked;
9. auto-layout mapping checked if relevant.

<!-- ESS_SYMBOL_CAPABILITY_REQUIREMENTS_V1 -->

## Expanded symbol capability requirements

The complete living requirements ledger is maintained in:

`	ext
docs/development/symbol_capability_requirements.md
`

Agents must consult that file before implementing symbol import, symbol rendering, editing, snapping, routing, state handling, busbar behavior, sheet templates or automatic scheme generation.

Non-negotiable capability classes:

1. voltage-class colorization;
2. rotation-safe terminals and snap anchors;
3. stretchable leads without body distortion;
4. terminal/snap based binding between figures;
5. explicit state variants for switching equipment;
6. KRU trolley state and position combinations;
7. configurable busbar connection points;
8. composite symbols with internal/external terminals;
9. labels as metadata-driven objects;
10. telemetry and state overlays separated from base geometry;
11. sheet templates and stamps separated from electrical symbols;
12. import provenance and manual review;
13. validation gates before core promotion;
14. undo/redo and fast editing workflow;
15. automatic scheme generation from equipment/topology lists;
16. manual override for auto-generated layouts;
17. schema/library versioning and migration.

Do not reduce imported Visio masters to static SVG stickers.

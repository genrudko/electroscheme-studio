# Visio import strategy

## Purpose

The Visio importer is the preferred path for building the symbol library.

The project must not rely on neural-network recognition of screenshots or PDF fragments as the source of truth for electrical symbols. Recognition may be used only as a helper. The reliable source is vector geometry from Visio masters.

## Source

Expected source file:

```text
G:\electroscheme-studio\Фигуры.vsdx
```

If the file name differs, pass it to the inspector:

```powershell
python tools/visio_inspect_vsdx.py "G:\electroscheme-studio\Фигуры(1).vsdx" --out "_reports\visio_figures"
```

## Import pipeline

```text
VSDX pages
→ page usage and category detection
→ Visio masters
→ ShapeSheet geometry audit
→ connection point extraction
→ import candidates
→ Imported / Needs Review
→ manual acceptance
→ Core symbol library
```

## Non-negotiable rules

1. Imported Visio symbols are never promoted directly to the core library.
2. Every imported symbol starts with `review_status = needs_review`.
3. Every symbol must be colorizable by voltage class.
4. Every symbol must be rotatable.
5. Terminals and snap anchors must rotate with the symbol.
6. Switching devices must preserve state variants.
7. Busbars must preserve configurable connection point behavior.
8. KRU trolley symbols must preserve both breaker state and trolley position.
9. Stretchable connection leads must not distort the symbol body.
10. Symbols must expose snap anchors for fast figure-to-figure binding.
11. Stamps and frames are not ordinary electrical symbols; they belong to the sheet/template library.
12. Automatic scheme generation from an equipment list is a first-class product goal.

## Critical semantic features

### Switching devices

Switching devices include:

- circuit breakers;
- load-break switches;
- disconnectors;
- earthing switches;
- automatic breakers;
- KRU trolley variants.

Required base states:

```text
closed
open
unreliable
repair
```

For normal scheme symbols, visible variants may be simpler. For operational/PTK symbols, state visualization is mandatory.

### KRU trolley states

KRU trolley symbols may encode both device state and trolley position.

Required states:

```text
breaker_closed_trolley_service
breaker_open_trolley_service
breaker_unreliable_trolley_service
trolley_withdrawn_repair
trolley_withdrawn_test
```

These must not be flattened into a single static icon.

### Busbars

Busbars are not just static lines.

They require:

- configurable number of connection points;
- configurable spacing;
- configurable length;
- generated terminals;
- voltage-class color;
- stroke width multiplier;
- optional labels for bus section/system name.

Default rule from the STO profile:

```text
busbar stroke width = 4 × normal connection line stroke width
```

### Rotation

All imported electrical symbols must be rotatable.

Rotation must affect:

- body geometry;
- terminals;
- snap anchors;
- generated busbar connection points;
- connection graph endpoints.

Text labels should use a readable-label policy:

```text
label_rotation_policy = keep_readable
```

### Stretching

Stretching must be semantic, not destructive.

Allowed:

```text
connection lead length
busbar length
line segment length
generated terminal spacing
```

Not allowed by default:

```text
non-uniform scaling of symbol body
distortion of switching-device geometry
distortion of transformer circles
```

### Snapping and binding

Each useful symbol must expose connection anchors.

The editor must support:

- snap symbol terminal to another terminal;
- snap symbol terminal to generated busbar point;
- keep connection graph stable after move/rotate/stretch;
- re-route connections without losing topology.

### Voltage-class colorization

Every symbol must support voltage-class colorization.

The geometry should use style tokens, not hard-coded imported colors:

```text
stroke: var(--voltage-color)
fill: none or state-dependent
```

The final renderer resolves this from a style profile:

```text
normal_scheme
operational_scheme
ptk_dark
```

### Stamps and frames

Visio pages containing stamps, frames and text blocks must be treated separately.

Target:

```text
templates/sheets
```

Not:

```text
symbols/core
```

## Inspector output

The inspector writes:

```text
_reports/visio_figures/pages.json
_reports/visio_figures/masters.json
_reports/visio_figures/import_candidates.json
_reports/visio_figures/master_geometry_audit.json
_reports/visio_figures/masters.csv
_reports/visio_figures/README.md
```

## Next step after inspection

The next patch should not import all symbols blindly.

Preferred next patch:

```text
patch_006_visio_master_to_symbol_draft_converter
```

It should create draft symbols under:

```text
symbols/imported/visio/needs_review
```

The converter must retain:

- original Visio master ID;
- original name;
- source page;
- geometry audit;
- connection points;
- feature flags;
- capabilities;
- review status.
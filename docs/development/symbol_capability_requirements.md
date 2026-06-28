# Symbol capability requirements

This document is the living requirements ledger for ElectroScheme Studio symbols, editor behavior, Visio import and automatic scheme generation.

The list is intentionally broader than the current MVP. User-provided requirements are not treated as final or exhaustive. Agents must add missing product requirements here before implementing features that affect symbol geometry, editing, snapping, routing, import or automatic scheme generation.

## Product principle

A symbol is not a static SVG sticker.

A symbol is an editable engineering object with:

- geometry;
- terminals;
- snap anchors;
- state;
- parameters;
- voltage style;
- rotation behavior;
- stretch behavior;
- connection graph behavior;
- import provenance;
- review status;
- auto-layout metadata.

If any of these are lost, the symbol library is not production-ready.

## Mandatory capabilities

### 1. Geometry preservation

Imported geometry must preserve the real shape as much as practical.

Required:

- lines;
- polylines;
- rectangles;
- circles and ellipses;
- arcs;
- text where it is part of the symbol;
- groups;
- nested shapes;
- local transforms;
- connection points;
- proportional dimensions.

Do not flatten vector masters into raster images.

### 2. Voltage-class colorization

All electrical symbols must support colorization by voltage class.

Required profiles:

- normal scheme profile;
- operational scheme profile;
- PTK/dark profile.

Geometry must use style tokens rather than fixed colors where possible:

```text
var(--voltage-color)
var(--state-color)
var(--symbol-stroke)
var(--symbol-fill)
```

### 3. Rotation

All electrical symbols must rotate without losing semantics.

Required rotations:

```text
0°
90°
180°
270°
```

Rotation must transform:

- body geometry;
- terminals;
- snap anchors;
- generated busbar terminals;
- connection graph endpoints;
- selection bounding box;
- resize handles;
- stretch handles.

Text labels must follow a readability policy:

```text
label_rotation_policy = keep_readable
```

### 4. Stretching without distortion

Some symbols must support stretching, but not destructive scaling.

Allowed stretch behavior:

- extend incoming/outgoing connection leads;
- extend line-like symbols;
- extend busbar length;
- change generated busbar terminal spacing;
- change cable/line segment length;
- move terminal anchors with the stretched part.

Forbidden by default:

- non-uniform scaling of breaker bodies;
- non-uniform scaling of transformer circles;
- distortion of contact geometry;
- distortion of state overlays;
- moving terminals without updating connection graph.

### 5. Snap anchors and binding

Symbols must expose snap anchors for fast editing.

Required interactions:

- terminal-to-terminal snapping;
- terminal-to-busbar generated point snapping;
- terminal-to-line snapping when allowed;
- preserve connection after symbol move;
- preserve connection after rotation;
- preserve connection after stretch;
- allow reconnect by dragging endpoint;
- allow detach without deleting symbol.

The editor must treat connections as graph edges, not decorative lines.

### 6. Multi-state equipment

Switching equipment must preserve states.

Minimum state vocabulary:

```text
closed
open
unreliable
repair
transition
manual_unconfirmed
blocked
grounded
```

Applies to:

- circuit breakers;
- load-break switches;
- disconnectors;
- earthing switches;
- automatic breakers;
- short-circuiters;
- separators;
- KRU trolley assemblies.

### 7. KRU trolley semantics

KRU trolley symbols are composite stateful objects.

They can encode:

- breaker state;
- trolley position;
- control/test/repair position;
- connector state;
- visible indication marks.

Required state combinations:

```text
breaker_closed_trolley_service
breaker_open_trolley_service
breaker_unreliable_trolley_service
trolley_withdrawn_repair
trolley_withdrawn_test
```

Do not flatten these into one static symbol.

### 8. Busbar semantics

Busbars are parametric objects.

Required parameters:

- orientation;
- length;
- stroke width;
- voltage class;
- busbar name;
- connection point count;
- connection point spacing;
- connection point side;
- terminal generation policy;
- optional section split points.

Required behavior:

- add/remove connection points;
- redistribute connection points;
- snap bay equipment to busbar points;
- keep existing connections when length changes if possible;
- maintain 4x stroke-width rule for normal schemes.

### 9. Composite symbols

Some equipment must be represented as composed objects.

Examples:

- transformer bay;
- KRU trolley + breaker;
- disconnector + earthing switch;
- transformer with CT/VT attachments;
- line bay;
- bus coupler bay;
- section breaker;
- WTG feeder cell.

Composite symbols must expose internal and external terminals.

### 10. Labeling

Labels are not decorative only.

Labels may include:

- dispatcher name;
- equipment type;
- bay name;
- voltage class;
- rated value;
- state text;
- measurement text;
- manual notes.

Required behavior:

- labels move with symbol by default;
- labels can be detached/repositioned;
- labels keep readable orientation;
- labels can be hidden by profile;
- labels can be generated from equipment metadata.

### 11. Measurements and telemetry overlays

The future editor must support operational overlays.

Examples:

- P;
- Q;
- I;
- U;
- F;
- temperature;
- state markers;
- repair marker;
- unreliable marker;
- grounding marker;
- command pending marker.

These must not be baked into the base symbol geometry.

### 12. Layers and display profiles

The renderer must support layers/profiles.

Minimum layers:

- primary scheme;
- labels;
- telemetry;
- protection/automation notes;
- repair/grounding overlays;
- templates/stamps;
- construction/grid;
- imported-needs-review markers.

Minimum profiles:

- normal scheme;
- operational black-and-white;
- PTK dark;
- print/export.

### 13. Sheet templates and stamps

Frames, stamps and title blocks are sheet templates, not electrical symbols.

Required behavior:

- A3/A2/A1 templates;
- right-bottom stamp placement;
- template versioning;
- editable title fields;
- print/export support.

### 14. Import provenance and review

Every imported symbol must store provenance:

- source file;
- source page;
- Visio master ID;
- Visio master name;
- import timestamp;
- geometry audit;
- connection point count;
- warnings;
- review status.

Default status:

```text
needs_review
```

Core promotion is allowed only after manual review.

### 15. Symbol validation

Each symbol must pass validation before core promotion.

Checks:

- valid ID;
- unique ID;
- category present;
- name_ru present;
- viewBox present;
- geometry present;
- terminals inside viewBox or generated by parameters;
- no duplicate terminal IDs;
- snap anchors present where required;
- rotation transform test passes;
- stretch test passes where applicable;
- voltage color token present;
- state variants present where required;
- preview renders;
- no embedded raster fallback unless explicitly accepted.

### 16. Editor performance

The editor must stay fast.

Targets for the first real editor:

- fast drag on hundreds of objects;
- no full canvas rerender on every tiny change if avoidable;
- spatial index for hit-testing later;
- cheap snap candidate lookup;
- undo/redo without huge memory churn;
- lazy rendering for off-screen elements if needed.

### 17. Undo/redo and editing safety

Required operations:

- add symbol;
- delete symbol;
- move symbol;
- rotate symbol;
- stretch symbol;
- edit label;
- connect/disconnect;
- change state;
- change voltage class;
- edit busbar connection count;
- group/ungroup where supported.

All must be undoable.

### 18. Keyboard and speed workflow

The product must be convenient for real work, not just visually correct.

Required later:

- hotkeys for rotate;
- hotkeys for wire mode;
- quick duplicate;
- quick align;
- quick distribute;
- quick snap;
- quick state toggle;
- quick voltage class change;
- search symbol by Russian name;
- insert by typing equipment kind/name.

### 19. Automatic scheme generation

Automatic scheme generation from equipment lists is a first-class feature.

Target pipeline:

```text
equipment list / station topology
→ voltage levels
→ busbars
→ bays
→ equipment placement
→ terminal graph
→ orthogonal routing
→ labels
→ validation
→ editable scheme
```

Generated schemes must remain editable.

Generated objects must keep:

- equipment ID;
- source model reference;
- symbol ID;
- voltage class;
- bay/section relation;
- terminals;
- connection graph edges;
- generated layout metadata.

### 20. Auto-layout requirements

The first auto-layout engine should be deterministic.

Rules:

- place voltage levels in bands;
- generate busbars before bays;
- place bays in declared order;
- place equipment along bay axis;
- use orthogonal routing;
- minimize crossings;
- keep labels readable;
- preserve manual edits;
- allow regeneration with locked/manual objects.

### 21. Manual override

Automatic features must not trap the user.

Required:

- lock object position;
- lock label position;
- exclude object from auto-layout;
- manually route connection;
- manually override symbol variant;
- manually override state display;
- manually override voltage color if required.

### 22. Versioning and migration

Symbol definitions must be versioned.

Required:

- schema_version;
- library_version;
- source_format;
- migration path;
- compatibility check;
- warning when old project uses old symbol definition.

### 23. Quality gates

Before any symbol import/conversion patch is accepted, the gate must report:

- number of imported candidates;
- number with geometry;
- number with connection points;
- number requiring manual terminals;
- number requiring state mapping;
- number requiring busbar parameters;
- number requiring stretch mapping;
- number requiring snap mapping;
- number rejected;
- preview generation status.

### 24. Do not lose source specificity

ГОСТ/СТО-oriented symbols may differ from IEC-style symbols.

The library must support:

- source standard/profile metadata;
- internal enterprise variants;
- station-specific variants;
- user custom symbols;
- imported raw symbols;
- reviewed core symbols.

### 25. Practical product goal

The editor must be:

```text
beautiful
convenient
fast
accurate
editable
portable
safe to regenerate
```

A static picture generator is not enough.
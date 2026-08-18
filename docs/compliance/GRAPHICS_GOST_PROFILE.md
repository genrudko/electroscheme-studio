# Graphics / ГОСТ-ЕСКД Profile Architecture

Статус: canonical foundation document

## 1. Goal

Native electrical schemes must be generated and edited through **versioned graphic-standard profiles** so that claims about ГОСТ/ЕСКД are traceable and testable.

The product must not equate `looks like an electrical scheme` with standards compliance.

## 2. Foundation baseline

Verified primary baseline includes:

- ГОСТ 2.701-2008 — scheme kinds/types and general execution requirements; Rosstandart status at 2026-08-18: `Действует`;
- ГОСТ 2.702-2011 — rules for presentation/execution of electrical schemes; Rosstandart status at 2026-08-18: `Действует`, including recorded correction ИУС 1-2021.

Applicable UGO/line/lettering/document standards for each implemented equipment/document family are added explicitly after official-catalogue verification.

## 3. Profile composition

Conceptually:

```text
GraphicProfile
├── profile ID/version
├── normative baseline date
├── source standards
├── scheme type(s)
├── symbol bindings
├── line/connection rules
├── text/designation rules
├── layout/document rules
├── output/print rules
├── enterprise stricter additions (optional)
└── coverage matrix
```

A profile version is immutable once used for an accepted/released document; future changes create a new profile version/migration choice.

## 4. Semantic symbol library

Native symbol is not just SVG/QML/path geometry.

```text
GraphicSymbolDefinition
├── semantic equipment/type binding
├── graphic profile binding
├── source/provenance
├── geometry
├── terminals/anchors
├── allowed orientation/rotation
├── parameterization/stretch rules
├── state variants
├── designation/text anchors
├── print behavior
└── validation evidence
```

The semantic equipment identity remains in Domain Core; the symbol is one representation.

## 5. Multiple graphic representations

One equipment type may have multiple valid representations depending on:

- scheme/document type;
- detail level;
- normative profile;
- operational vs normal view;
- imported compatibility format.

Example:

```text
CircuitBreaker
├── native GOST-oriented single-line representation
├── operational-state representation
└── NPT compatibility CustElem representation
```

NPT representation is not automatically promoted into native ГОСТ profile.

## 6. Required validation dimensions

Where applicable, graphic validation covers:

- symbol type/profile is permitted for the semantic object;
- terminal/connection points correspond to semantic terminals;
- required line types/weights/classes;
- crossings/junction indications;
- labels/designations/content;
- orientation/allowed transformations;
- document/sheet annotations;
- consistency of the same element across related views/documents;
- print/export readability;
- profile-specific minimum spacing or placement rules only where traceable to source/profile.

Do not invent numerical spacing rules and label them ГОСТ unless the source supports them.

## 7. Layout vs compliance

Auto-layout optimizes readability while respecting profile constraints.

A layout preference such as `keep feeders vertically aligned` may be a product heuristic, while a particular graphic rule may be normative. These must be distinguished in diagnostics.

```text
NORMATIVE_VIOLATION
PROFILE_VIOLATION
LAYOUT_QUALITY_WARNING
```

should not be collapsed into one red marker.

## 8. Symbol provenance

Each promoted native symbol must record:

- normative source(s);
- independent authoring/import source;
- any VSDX/VSSX master used for engineering reference;
- any compatibility/NPT material used only as comparison;
- licensing/usage status;
- validation screenshots/tests.

Never silently copy proprietary NPT/third-party symbol assets into native library.

## 9. VSDX/VSSX role

Visio masters may remain valuable engineering sources for geometry, connection points and historical corporate libraries, but:

- VSDX/VSSX is not normative authority;
- imported master requires source/profile mapping;
- unsupported ShapeSheet behavior must be diagnosed;
- a Visio shape that violates chosen native profile is imported as compatibility/legacy representation or requires correction, not automatically declared compliant.

## 10. Operational state rendering

Semantic state maps to visual variants through profile rules.

Example:

```text
EquipmentState
   ↓
RepresentationStateResolver
   ↓
geometry/style/text variant
```

Colors/styles are view semantics and must not change canonical state.

Unknown state needs an explicit representation and must not look identical to known OPEN/CLOSED where that would mislead users.

## 11. Print/export

Profile acceptance includes deterministic high-quality output appropriate to engineering documentation.

Initial output targets after platform selection:

- vector PDF where practical;
- high-resolution print;
- controlled SVG/export for diagnostics/interchange where appropriate;
- VSDX compatibility according to a separate supported subset when reintroduced.

Output tests compare geometry/text/style against profile tolerances rather than only successful file creation.

## 12. Coverage matrix

Each profile release maintains a matrix such as:

| Area | Source | Rules identified | Implemented | Tested | Limitations |
|---|---|---:|---:|---:|---|
| scheme type/general | ГОСТ 2.701-2008 | TBD | TBD | TBD | extraction pending |
| electrical execution | ГОСТ 2.702-2011 | TBD | TBD | TBD | extraction pending |
| breaker UGO | exact verified UGO standard | TBD | TBD | TBD | source pending |
| transformer UGO | exact verified UGO standard | TBD | TBD | TBD | source pending |

A profile is never labelled `full GOST compliant` while rows remain undefined.

## 13. First implementation slice

After Platform/UI/Domain foundations, choose a small equipment family sufficient for a representative single-line cell, for example:

- bus/bus section;
- circuit breaker;
- disconnector;
- earthing switch;
- transformer/line/load as needed.

For each exact family:

1. verify applicable Rosstandart standard(s);
2. create semantic type/terminal schema;
3. create independent native symbol;
4. add state variants;
5. add automated/profile validation;
6. render Gallery samples;
7. print/export comparison;
8. owner visual acceptance.

## 14. Enterprise graphical rules

Enterprise/site standards may impose stricter or additional presentation conventions.

They are layered as explicit profile overlays and cannot masquerade as ГОСТ requirements. Diagnostics must identify the actual source layer.

## 15. Non-goals

Foundation does not attempt to ingest every ESKD standard, freeze a complete symbol library or infer norms from legacy NPT/Visio drawings.

Standards coverage expands with real product/equipment workflows and official source verification.

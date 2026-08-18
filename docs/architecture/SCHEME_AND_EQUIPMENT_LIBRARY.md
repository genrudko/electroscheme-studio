# Scheme Module and Equipment Library

Статус: canonical foundation document

## 1. Purpose

The Scheme module turns the neutral electrical model into editable engineering representations. The Equipment Library defines reusable semantic equipment types and their permitted graphical/state representations.

They are related but deliberately separate:

```text
Equipment Library = what the equipment is
Scheme Module     = how selected project entities are represented/arranged in a view
```

## 2. Equipment Library responsibilities

A type definition may provide:

- semantic category/type ID;
- terminal schema and roles;
- typed properties/units/constraints;
- supported states;
- domain validation hooks/data;
- applicable manufacturer/model profiles;
- graphic representation bindings per profile/view;
- naming/designation metadata where appropriate.

Do not encode site instances into the type library. `QF-17` is project equipment; `circuit-breaker` is a type.

## 3. Native vs compatibility representations

One semantic type can bind to several representations:

```text
circuit-breaker
├── native ГОСТ-oriented single-line symbol
├── operational-state native symbol
├── imported Visio/legacy representation
└── NPT CustElem compatibility representation
```

Compatibility representation does not become normative/native authority automatically.

## 4. Scheme View

A Scheme View references project entities and stores view-specific data:

```text
SchemeView
├── identity/name/type
├── inclusion/filtering
├── graphic profile
├── entity placements
├── connection routes
├── labels/annotations
├── groups/regions/layers
├── layout constraints
├── viewport/document metadata
└── validation/output state
```

Electrical connections remain in Domain Core. A view route is not the connection itself.

## 5. Core editing operations

Expected foundation operations:

- add existing project entity to view;
- create new equipment through domain command then place representation;
- select/multi-select;
- move/align/distribute;
- rotate/orient where representation permits;
- reconnect semantic terminal through explicit domain command;
- edit visual route without changing semantic endpoints;
- edit typed properties through Inspector;
- copy/paste with controlled identity semantics;
- delete from view vs delete equipment from project as clearly different commands;
- undo/redo;
- search/navigate by equipment identity/name/KKS/source.

## 6. Create/delete semantics

Dangerous ambiguity must be eliminated in UX.

Examples:

```text
Remove from this scheme view
≠
Delete equipment from project
```

and:

```text
Move line bend
≠
Reconnect terminal
```

Commands and confirmation/validation reflect the semantic difference.

## 7. Auto-layout integration

Scheme module consumes `LayoutProposal` from Import/Auto-layout service and owns accepted geometry/constraints.

Manual corrections become constraints or user-owned routes, enabling incremental future updates.

The layout engine cannot invent/change electrical topology to improve appearance.

## 8. View families

Long-term architecture may support:

- normal single-line;
- temporary-normal/repair variants;
- detailed bay/switchgear views;
- operational views;
- other controlled electrical representations.

Do not implement all families in first MVP. The first vertical slice proves one representative single-line workflow while the data model allows multiple views over one equipment identity.

## 9. State visualization

Scheme renderer receives semantic state/quality plus view/profile rules.

It must support explicit uncertainty.

Example:

```text
CLOSED + GOOD
OPEN + GOOD
INTERMEDIATE
UNKNOWN / BAD QUALITY
SIMULATED CLOSED
```

Operational/simulated state visuals must be distinguishable when necessary and not overwrite canonical observed state.

## 10. Large-project strategy

The module must scale beyond small diagrams.

Expected techniques, selected by platform evidence:

- scene graph/custom drawing rather than one heavyweight widget per primitive;
- spatial indexing;
- viewport culling;
- batched render/update;
- incremental layout/routing;
- text/geometry caches where safe;
- background computation for expensive non-UI tasks with deterministic commit back to model.

Performance budgets are established by Platform Stack Spike and then regression-tested.

## 11. Routing

Connection routing is view geometry.

Initial routing may be orthogonal/domain-aware and deterministic. Requirements:

- route endpoints anchored to representation terminals;
- junction/crossing semantics consistent with profile;
- user-owned bend/route support;
- reroute affected region rather than entire diagram where feasible;
- diagnostics for impossible/overlapping routes.

Universal perfect autorouting is not an MVP requirement.

## 12. Labels and designations

Labels may come from:

- equipment operational/designation names;
- KKS/identifier properties;
- rated values;
- state/value properties;
- view-specific annotations.

The profile controls which labels are required/permitted and how they are placed. User overrides must be explicit and profile-validatable.

## 13. Validation layers

Scheme diagnostics distinguish:

```text
DOMAIN_ERROR             # e.g. invalid semantic connection
GRAPHIC_PROFILE_ERROR    # e.g. representation/profile violation
LAYOUT_WARNING           # readability/overlap
IMPORT_PROVENANCE_WARNING
NPT_COMPATIBILITY_ERROR  # only for NPT view/export path
```

One generic `invalid object` bucket is insufficient.

## 14. Equipment manufacturer profiles

A manufacturer/model profile may define:

- ratings/property defaults/limits;
- terminal layout/roles if model-specific;
- state constraints;
- additional switching restrictions;
- optional detailed representation.

It cannot weaken mandatory applicable constraints. Source manual/revision/provenance is required for production rules.

## 15. Equipment library evolution

Start with a small first family sufficient for real vertical slice.

Promotion gate for each type includes:

- domain meaning;
- terminal semantics;
- state semantics;
- validation;
- native graphic profile evidence;
- Gallery render;
- project save/load;
- import mapping;
- switching semantics where relevant.

Avoid mass-generating hundreds of symbol types before this pipeline is proven.

## 16. Search/library UX

User should locate equipment/symbols by engineering meaning, not browse a giant flat icon folder.

Search/filter candidates:

- category/type;
- voltage/application;
- manufacturer/model;
- standard/profile;
- tags/aliases;
- recently/frequently used;
- project-available types.

NPT library palette is a separate compatibility projection and may expose vendor names/definitions.

## 17. First vertical slice relationship

`IMPORT-TO-SCHEME-VERTICAL-SLICE-001` should exercise this module with a real small equipment set imported from structured data, auto-layout, manual correction, save/reopen and re-import.

That slice proves the architecture before expanding into full editor breadth.

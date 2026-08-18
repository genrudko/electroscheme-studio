# Domain and Project Model

Статус: canonical foundation document

## 1. Source of truth

The canonical engineering authority is `ElectricalProject`.

It is not defined by a drawing file or external vendor format.

Conceptual root:

```text
ElectricalProject
├── ProjectIdentity
├── Sites / Facilities
├── VoltageLevels
├── Equipment
├── Terminals
├── Connections
├── Signals
├── States
├── ComplianceProfileRefs
├── Views
├── SourceProvenance
└── ModuleExtensions
```

Exact classes/schema are PENDING until implementation spike. This document defines semantics/invariants, not a frozen serialization syntax.

## 2. Identity

All canonical engineering entities use stable internal IDs independent from display names/KKS/vendor IDs.

Example:

```text
id: eq_01J...
dispatch_name: "В-35-17"
kks: "..."           # optional/domain attribute
external_ids:
  npt: "..."         # adapter-owned mapping/reference
  import_source: "QF17"
```

Rules:

- display name changes do not change identity;
- external IDs are mapped/provenance data, not canonical identity;
- duplicate external IDs are diagnosable;
- stable IDs survive layout/view changes.

## 3. Equipment

`Equipment` represents a semantic device/object, not its picture.

Core attributes are intentionally small:

- stable ID;
- equipment type reference;
- names/designations;
- object/site/voltage context;
- typed properties;
- terminal set;
- state reference/current simulated state where applicable;
- source/provenance references.

Equipment type definitions live in Equipment Library rather than a growing inheritance hierarchy for every vendor model.

Typical domain types include, as evidence justifies:

- circuit breaker;
- disconnector;
- earthing switch;
- bus/bus section;
- transformer/autotransformer;
- line/cable;
- generator;
- load;
- measurement transformer;
- protection/control-related semantic objects where required by product modules.

Do not invent complete taxonomy during Foundation.

## 4. Equipment Library

An equipment type definition may declare:

```text
TypeDefinition
├── semantic type/category
├── terminal schema
├── supported properties
├── supported states
├── validation constraints
├── graphic representation bindings
└── optional manufacturer/model profiles
```

Manufacturer/model profile may add stricter ratings/constraints without redefining the core meaning of the equipment category.

## 5. Terminals

A terminal is the semantic connection point of equipment.

Required properties include:

- stable terminal ID;
- owning equipment ID or controlled standalone network node;
- role/name;
- optional phase/conductor semantics;
- voltage/domain constraints where applicable.

Coordinates are not terminal identity.

A symbol may visually expose terminal anchors that map to semantic terminals, but moving the symbol does not recreate terminals.

## 6. Connections

A connection represents an electrical/network relationship between semantic endpoints.

Canonical connection does not own screen polyline geometry.

Invariant examples:

- endpoints must exist;
- terminal cardinality/type rules are validated by domain/equipment library;
- connection changes are explicit transactions;
- deleting equipment with connected terminals requires an explicit strategy and diagnostics;
- a connection may be rendered differently in multiple views.

## 7. Topology Graph

Topology is derived/maintained from terminals and connections plus domain semantics.

Capabilities expected over time:

- connectivity queries;
- path search;
- electrical islands/sections;
- state-dependent continuity;
- energized/de-energized/unknown propagation with explicit source assumptions;
- switching impact calculation;
- diagnostics for impossible/dangling structures.

Important: topology engine must distinguish:

```text
NO_PATH
PATH_OPEN_BY_KNOWN_STATE
PATH_CLOSED
PATH_STATUS_UNKNOWN
```

so that unknown data does not become an optimistic safe state.

## 8. State

State consists of typed values with quality/knowledge semantics.

Examples:

```text
CircuitBreakerPosition:
  OPEN | CLOSED | INTERMEDIATE | UNKNOWN

Energization:
  ENERGIZED | DEENERGIZED_PROVEN | UNKNOWN

SignalQuality:
  GOOD | BAD | UNCERTAIN | UNKNOWN
```

`DEENERGIZED_PROVEN` is deliberately different from absence of an energized path under incomplete data.

Modules may define richer equipment states through typed extension contracts.

## 9. Signals

A signal is a domain binding/reference, not necessarily an online runtime channel.

It may carry:

- signal ID/reference;
- KKS/other external designation;
- source/system;
- type/unit;
- relation to equipment/property/state;
- quality semantics;
- provenance.

NPT ASU/TECH implementation details remain in NPT adapter/catalog.

## 10. Views

`View` is a controlled representation over project entities.

A project may have:

- general single-line view;
- voltage-level view;
- detailed switchgear/bay view;
- operational view;
- NPT-compatible mnemonic view;
- tabular view;
- switching simulation view.

A view stores/reference:

- entity inclusion/filters;
- representation profile;
- geometry/layout;
- labels/annotations;
- layer/group settings;
- layout constraints.

Views do not duplicate authoritative equipment topology unless an explicit snapshot/document use case says so.

## 11. Layout constraints

Manual correction after auto-layout is first-class data.

Possible constraints include:

- pinned position;
- fixed relative ordering;
- fixed orientation;
- bus orientation/extent;
- group/bay placement;
- user-owned edge route/bends;
- protected label placement;
- layout region assignment.

Auto-layout must classify what it may change and preserve protected constraints during incremental updates.

## 12. Provenance

Imported/generated/domain entities should retain enough provenance to explain origin and reconcile future updates.

Conceptual provenance:

```text
SourceRef
├── source type (xlsx/csv/npt/manual/visio/...)
├── source identity/file fingerprint
├── external row/object ID
├── mapping profile version
├── import timestamp/version
└── transformation notes/confidence
```

Provenance is not a substitute for canonical identity.

## 13. Compliance profile references

Project references applicable compliance/profile configuration rather than copying immutable normative text everywhere.

Conceptually:

```text
ProjectCompliance
├── baseline date
├── mandatory regulatory profile
├── graphic standard profile
├── equipment/manufacturer profiles
├── enterprise profile
├── site profile
└── project overlay
```

Resolved rules and source versions used for a release/document should be snapshot-able/auditable.

## 14. Module extensions

Vendor/module-specific information that must survive round-trip but has no neutral meaning belongs in namespaced module extensions.

Example:

```text
extensions.npt = preserve-owned payload/mapping
```

Rules:

- extension must not become required to interpret neutral topology unless promoted through an ADR/model change;
- unknown extension data should round-trip according to native project migration policy;
- module removal must produce explicit diagnostics if project depends on its extension for a feature.

## 15. Undo/redo and transactions

Engineering changes are represented as transactions/change sets.

Examples:

- add equipment;
- reconnect terminal;
- apply approved import plan;
- change rated property;
- change manual layout constraint;
- apply simulated switching operation.

Simulation state and persisted operational/current state must be clearly separated.

## 16. Native project format requirements

Before selecting physical serialization, implementation must prove:

- schema versioning;
- deterministic round-trip of known data;
- migration tests;
- stable identity;
- atomic write/recovery;
- module extension preservation;
- diffability/diagnostics;
- no hidden dependency on GUI framework object serialization.

## 17. Non-goals of initial Domain Core

Do not include until required:

- full CIM ontology;
- every protection/automation data class;
- real-time SCADA channel engine;
- complete manufacturer database;
- universal calculation model;
- generic graph theory abstractions exposed to UI users.

The model grows from validated product workflows.

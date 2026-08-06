# Target System Architecture — ElectroScheme Studio

## 1. Architecture status

This document defines the target component boundaries for the refounded product.

The final desktop shell, runtime packaging technology and exact repository layout remain subject to `DESKTOP-PLATFORM-AND-CORE-SPIKE-001`. The logical boundaries below are mandatory unless changed by an accepted ADR.

## 2. Architectural objective

Build a cross-platform desktop engineering editor in which:

- the electrical document model is authoritative;
- the editor UI is a projection and command source;
- platform-specific functions are adapters;
- symbol sources and normative profiles are versioned assets;
- core behavior is testable without launching the complete desktop application;
- Windows and Linux packages use the same project format and domain rules.

## 3. Logical layers

```text
Desktop Host
  ├─ native window / lifecycle
  ├─ filesystem dialogs
  ├─ clipboard / drag-and-drop
  ├─ printing / export integration
  ├─ update / diagnostics
  └─ platform adapters

Application Layer
  ├─ project lifecycle
  ├─ command bus and transactions
  ├─ undo / redo
  ├─ autosave / recovery
  ├─ validation orchestration
  ├─ import / export orchestration
  └─ use-case services

Domain and Document Core
  ├─ ProjectDocument
  ├─ sheets / layers
  ├─ objects / symbols / properties
  ├─ ports / terminals
  ├─ electrical connections / topology
  ├─ stable identities and references
  ├─ schema versions / migrations
  └─ domain invariants

Editor Kernel
  ├─ viewport and coordinate transforms
  ├─ selection
  ├─ interactions and gestures
  ├─ snapping
  ├─ routing presentation
  ├─ guides / rulers / grid
  ├─ handles and overlays
  └─ renderer projection

Symbol Platform
  ├─ accepted SymbolDefinition registry
  ├─ parameter and state models
  ├─ geometry and port transforms
  ├─ VSDX / VSSX source adapters
  ├─ provenance and review workflow
  └─ symbol migration/versioning

Profiles and Validation
  ├─ ГОСТ / СТО presentation profiles
  ├─ line / text / color / frame rules
  ├─ electrical validation rules
  ├─ diagnostics catalog
  └─ compliance evidence mapping

Infrastructure
  ├─ project file storage
  ├─ library storage
  ├─ PDF / SVG / raster exporters
  ├─ logs and crash diagnostics
  ├─ packaging
  └─ update channel
```

## 4. Canonical document ownership

There must be one canonical `ProjectDocument` contract.

It owns at minimum:

```text
metadata
schema_version
sheets
layers
objects
object properties
ports
connections
topology metadata
styles/profile references
embedded or referenced library versions
project settings
```

The following current prototype models are temporary sources for reconciliation, not coequal runtime models:

- backend `Project`;
- frontend `useProject` state;
- frontend `EditorDocument`;
- local object arrays and selection state inside `CanvasViewport`.

The selected target implementation may be TypeScript, Rust, Python or another justified boundary, but there must not be independent writable copies with informal synchronization.

## 5. Mutation architecture

All user-visible mutations pass through commands/transactions.

Examples:

- `InsertObject`;
- `DeleteSelection`;
- `MoveObjects`;
- `RotateObjects`;
- `ChangeProperty`;
- `ConnectPorts`;
- `DisconnectPorts`;
- `MoveWaypoint`;
- `ChangeLayer`;
- `ChangeSheetSettings`;
- `ApplySymbolParameter`.

A command must:

1. validate preconditions;
2. produce a deterministic document change;
3. update affected topology/derived indexes;
4. produce undo information or an inverse operation;
5. mark the document dirty;
6. trigger validation/render invalidation through defined events;
7. be serializable to diagnostics where practical.

Direct mutation from a UI component is forbidden in accepted product flows.

## 6. Rendering architecture

The renderer projects `ProjectDocument` into SVG or another accepted scene representation.

Rules:

- rendered DOM/SVG IDs are derived views, not domain identity;
- viewport zoom/pan never changes engineering coordinates;
- selection handles, snap hints and guides are overlay state, not saved engineering objects unless explicitly modeled;
- connection paths are rendered from topology and route data;
- symbol geometry uses a normalized local coordinate system and explicit transforms;
- print/export renderers consume the same document/profile contracts as the interactive renderer.

## 7. Editor interaction boundary

The editor kernel owns interactions, not product domain state.

It may maintain ephemeral state:

- pointer capture;
- active gesture;
- marquee rectangle;
- hovered/snap candidate;
- temporary ghost;
- viewport transform;
- open context menu;
- current tool/mode.

It must submit commands to change the document.

`CanvasViewport` or its successor must remain a composition/view layer, not a monolithic owner of document, topology, persistence and properties.

## 8. Desktop platform boundary

The product is desktop-first, but platform-specific code must be isolated behind interfaces such as:

- `FileDialogPort`;
- `ProjectFileStore`;
- `ClipboardPort`;
- `NativeDragDropPort`;
- `PrintPort`;
- `ExportDestinationPort`;
- `RecentFilesPort`;
- `UpdatePort`;
- `CrashReportPort`;
- `SystemThemePort`.

The domain/editor core must not depend directly on Electron, Tauri, Qt, browser APIs or OS-specific paths.

## 9. VSDX/VSSX tooling boundary

Visio processing is an import/source subsystem, not the runtime document model.

Pipeline:

```text
VSDX/VSSX package
→ raw ShapeSheet extraction
→ normalized source model
→ conversion diagnostics
→ review candidate
→ accepted SymbolDefinition version
→ symbol registry
```

Raw formulas, source IDs and provenance should be retained even when normalized geometry is generated.

Python tools may remain external build/import tools, may be packaged as a helper process, or may be ported. The platform spike must compare these options. Product runtime must handle tool failure explicitly and never silently accept partial conversion.

## 10. Symbol architecture

`SymbolDefinition` is separate from a placed `SymbolInstance`.

Definition owns:

- family/type;
- version;
- normalized geometry;
- default dimensions;
- ports and directions;
- parameters;
- states;
- property schema;
- transform policies;
- presentation profiles;
- provenance;
- review status.

Instance owns:

- stable object ID;
- reference to definition/version;
- position/rotation/mirroring;
- parameter values;
- property values;
- current state;
- label overrides;
- attachment/topology references.

Definitions can migrate; instance semantics must not be lost when a library version changes.

## 11. Topology architecture

Electrical topology is distinct from visible routes.

A connection owns:

- stable ID;
- endpoint references;
- electrical kind;
- route mode/data;
- junction/crossing semantics;
- validation metadata where appropriate.

Moving an object updates rendered endpoints but does not destroy endpoint references.

A visual crossing is not automatically an electrical junction. Junction semantics must be explicit.

## 12. Persistence and project format

Project files must be:

- versioned;
- deterministic where practical;
- human-inspectable or safely packaged with an inspectable manifest;
- migratable;
- validated before replacing the last known-good saved copy;
- recoverable through autosave/backup;
- portable between Windows and Linux.

The architecture spike must decide whether the project is a single JSON file, a ZIP/container with JSON and assets, or another open package. Binary-only opaque storage is not acceptable as the sole canonical format.

## 13. Validation architecture

Validation rules produce structured diagnostics:

```text
rule_id
severity
scope/object references
message key and parameters
normative source reference if applicable
fixability
location/navigation target
```

Validation groups:

- schema/integrity;
- object/property;
- port/topology;
- layout/presentation;
- ГОСТ/СТО profile;
- export/print readiness.

Rules must be independently testable and must not be embedded only in UI components.

## 14. Export and print

Interactive and output renderers share:

- document model;
- symbol definitions;
- profile rules;
- coordinate units;
- line/text metrics.

Export adapters may differ technically, but must pass visual and dimensional golden tests.

Required output path for MVP:

- SVG;
- PDF;
- print preview/print.

Raster output is secondary.

## 15. Testing architecture

Test levels:

1. pure domain/invariant tests;
2. command and migration tests;
3. symbol conversion/geometry tests;
4. renderer golden tests;
5. interaction component tests;
6. desktop end-to-end tests;
7. packaging/install smoke on Windows and Linux;
8. cross-platform same-project round-trip tests.

The core test suite must remain fast enough to run on each PR.

## 16. Deployment model

MVP is local-first and does not require a central server.

A local HTTP server may exist only if selected by the desktop architecture and justified. FastAPI is not automatically retained as a mandatory runtime merely because it exists in the prototype.

External integrations, EOD adapters and optional network services are post-MVP boundaries and must not contaminate the core.

## 17. Migration strategy

The target product is built by vertical replacement, not by endless repair of the prototype.

Recommended sequence:

1. select desktop/runtime architecture;
2. implement canonical document core alongside quarantined prototype;
3. build fresh editor kernel/design system on the new core;
4. migrate or reimplement accepted algorithms individually;
5. build accepted symbol families;
6. implement topology;
7. complete MVP vertical slice;
8. remove legacy runtime only after equivalent accepted flows exist.

At no point should two document models both be allowed to save authoritative project state.

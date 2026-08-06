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
- Windows and Linux packages use the same project format and domain rules;
- one engineering equipment identity may later have multiple controlled diagram representations;
- calculation, CIM and telemetry integrations remain adapters rather than contaminating the editor core.

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
  ├─ document variants / sheets / layers
  ├─ equipment identities
  ├─ diagram representations
  ├─ objects / symbols / properties
  ├─ ports / terminals
  ├─ electrical connections / topology
  ├─ state and normal-position data
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
  ├─ line / text / color / frame / modular-grid rules
  ├─ electrical validation rules
  ├─ representation-consistency rules
  ├─ diagnostics catalog
  └─ compliance evidence mapping

Integration Adapters
  ├─ CIM/profile exchange
  ├─ external calculation tools
  ├─ equipment registers
  ├─ read-only telemetry/state sources
  └─ future EOD/external-system adapters

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
documents and document types
sheets
layers
equipment identities
diagram representations
objects
object properties
ports
connections
topology metadata
state and normal-position data
styles/profile references
embedded or referenced library versions
project settings
```

The first schema is not required to expose every post-MVP feature in the UI, but it must define explicit ownership boundaries for identity, representation, state and document-profile references.

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
- `CreateEquipmentIdentity`;
- `CreateDiagramRepresentation`;
- `DeleteSelection`;
- `MoveObjects`;
- `RotateObjects`;
- `ChangeProperty`;
- `ChangeEquipmentState`;
- `SetNormalPosition`;
- `ConnectPorts`;
- `DisconnectPorts`;
- `MoveWaypoint`;
- `ChangeLayer`;
- `ChangeSheetSettings`;
- `ApplySymbolParameter`;
- `ChangePresentationProfile`.

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
- state-dependent graphics are selected through accepted symbol/profile rules, not arbitrary CSS mutations;
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

Visio processing is an import/source subsystem, not the runtime document model and not the product's semantic authority.

Pipeline:

```text
VSDX/VSSX package
→ raw ShapeSheet extraction
→ normalized source model
→ conversion diagnostics
→ engineering family / port-role mapping
→ normative/profile review
→ review candidate
→ automated tests
→ accepted SymbolDefinition version
→ symbol registry
```

Raw formulas, source IDs and provenance should be retained even when normalized geometry is generated.

Successful parsing or conversion does not prove electrical semantics, valid states, valid port roles or GOST/STO compliance.

Python tools may remain external build/import tools, may be packaged as a helper process, or may be ported. The platform spike must compare these options. Product runtime must handle tool failure explicitly and never silently accept partial conversion.

## 10. Symbol architecture

`SymbolDefinition` is separate from a placed `SymbolInstance`.

Definition owns:

- family/type;
- version;
- normalized geometry;
- default dimensions;
- ports and directions;
- port roles;
- parameters;
- states and allowed transitions where applicable;
- property schema;
- transform policies;
- presentation profiles;
- provenance;
- review status.

Instance owns:

- stable representation/object ID;
- optional reference to equipment identity;
- reference to definition/version;
- position/rotation/mirroring;
- parameter values;
- representation-specific property values;
- current state reference where the state belongs to the represented equipment;
- label overrides;
- attachment/topology references.

Definitions can migrate; instance semantics must not be lost when a library version changes.

## 11. Equipment identity and multiple representations

The market baseline supports a long-term distinction between the engineering object and its visual appearances.

`EquipmentIdentity` owns shared engineering meaning such as:

- stable equipment ID;
- equipment family/type;
- dispatcher or engineering designation;
- shared passport/reference properties;
- state/normal-position ownership where appropriate;
- links to external registers;
- lifecycle metadata.

`DiagramRepresentation` owns document-specific information such as:

- representation ID;
- target document/sheet;
- symbol definition/profile;
- position, rotation and local layout;
- local labels and visibility;
- representation-specific ports or phase expansion where required;
- references to shared equipment terminals through an explicit mapping.

Rules:

1. MVP may use one primary representation per equipment identity.
2. The schema must not equate equipment identity with a single SVG object forever.
3. Multiple representations are introduced only after concrete use cases and consistency rules exist.
4. Automatic conversion between arbitrary one-line, three-line and secondary diagrams is not assumed.
5. Semi-automatic representation creation must preserve user-controlled layout.
6. Cross-representation inconsistencies must be diagnosable rather than silently synchronized.

## 12. Topology architecture

Electrical topology is distinct from visible routes.

A connection owns:

- stable ID;
- endpoint references;
- electrical kind;
- optional phase/conductor semantics;
- route mode/data;
- junction/crossing semantics;
- validation metadata where appropriate.

Moving an object updates rendered endpoints but does not destroy endpoint references.

A visual crossing is not automatically an electrical junction. Junction semantics must be explicit.

Manual device position/state must remain distinct from future derived energized/de-energized topology state.

## 13. Persistence and project format

Project files must be:

- versioned;
- deterministic where practical;
- human-inspectable or safely packaged with an inspectable manifest;
- migratable;
- validated before replacing the last known-good saved copy;
- recoverable through autosave/backup;
- portable between Windows and Linux.

The architecture spike must decide whether the project is a single JSON file, a ZIP/container with JSON and assets, or another open package. Binary-only opaque storage is not acceptable as the sole canonical format.

The persisted document must retain:

- schema version;
- document/profile version references;
- equipment and representation identities;
- symbol definition versions;
- topology and state semantics;
- migration provenance where data was transformed.

## 14. Validation architecture

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
- identity/reference integrity;
- object/property;
- state/normal-position;
- port/topology;
- cross-representation consistency;
- layout/presentation;
- ГОСТ/СТО profile;
- export/print readiness.

Rules must be independently testable and must not be embedded only in UI components.

## 15. Export and print

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

## 16. CIM and external integration boundary

`ГОСТ Р 58651.9-2023` and related CIM concepts are relevant to future exchange and to architectural vocabulary such as diagram objects, points, equipment and terminals.

They do not automatically define the internal editor model.

A future CIM adapter must:

- declare the supported profile and revision;
- map canonical identities, terminals, topology and representations explicitly;
- report unsupported or lossy mappings;
- preserve external identifiers and provenance;
- avoid silently rewriting the user's project to fit an exchange format.

External calculation tools, equipment databases and telemetry sources use separate adapters. Real-time control, SCADA availability, cybersecurity and safety interlocks are outside the editor core and outside MVP.

## 17. Testing architecture

Test levels:

1. pure domain/invariant tests;
2. command and migration tests;
3. symbol conversion/geometry/semantic tests;
4. renderer golden tests;
5. interaction component tests;
6. desktop end-to-end tests;
7. packaging/install smoke on Windows and Linux;
8. cross-platform same-project round-trip tests;
9. future cross-representation consistency tests;
10. future adapter contract and loss-reporting tests.

The core test suite must remain fast enough to run on each PR.

## 18. Deployment model

MVP is local-first and does not require a central server.

A local HTTP server may exist only if selected by the desktop architecture and justified. FastAPI is not automatically retained as a mandatory runtime merely because it exists in the prototype.

External integrations, EOD adapters and optional network services are post-MVP boundaries and must not contaminate the core.

## 19. Migration strategy

The target product is built by vertical replacement, not by endless repair of the prototype.

Recommended sequence:

1. select desktop/runtime architecture;
2. implement canonical document core alongside quarantined prototype;
3. build fresh editor kernel/design system on the new core;
4. migrate or reimplement accepted algorithms individually;
5. build accepted symbol families;
6. implement topology and state contracts;
7. complete the normal single-line MVP vertical slice;
8. add normative profile evidence and cross-platform release output;
9. remove legacy runtime only after equivalent accepted flows exist;
10. add temporary-normal, operational, phase-explicit and multi-representation capabilities as separate evidence-backed vertical slices.

At no point should two document models both be allowed to save authoritative project state.

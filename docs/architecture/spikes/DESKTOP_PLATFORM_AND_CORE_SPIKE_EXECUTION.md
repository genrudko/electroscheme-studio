# DESKTOP-PLATFORM-AND-CORE-SPIKE-001 — Execution Plan

Status: in progress  
Issue: #3  
Branch: `architecture/desktop-platform-and-core-spike-001`  
Accepted base: `b95d7111d9c5a36db4c355ee91f742efea8ecc10`

## 1. Purpose

Select the desktop host, runtime boundaries and canonical core ownership through executable evidence on Windows and Linux.

This spike is not a product-feature phase. It must prevent the new product from inheriting the prototype's parallel document models, UI-owned state, CSS repair stack and incomplete persistence.

## 2. Non-negotiable constraints

- one authoritative writable document path;
- command/transaction-based mutations;
- core tests without launching the complete UI;
- Windows and Linux evidence;
- local-first operation;
- no mandatory cloud conversion;
- no automatic reuse of prototype code;
- VSDX/VSSX are interoperability formats, not the canonical model;
- no silent Visio import/export loss;
- no full MVP, permanent symbol platform or topology implementation in this PR.

## 3. Candidate set

### Candidate A — Tauri host

Proposed bounded composition:

```text
Tauri desktop host
+ Vue 3 / TypeScript / SVG temporary spike UI
+ explicit host adapters
+ canonical core candidate with justified Rust/TypeScript ownership
+ Python VSDX helper as controlled local process or build-time tool
```

### Candidate B — Electron host

Proposed bounded composition:

```text
Electron desktop host
+ Vue 3 / TypeScript / SVG temporary spike UI
+ isolated main/preload/renderer boundary
+ TypeScript canonical core candidate
+ Python VSDX helper as controlled local process or packaged tool
```

### Candidate C — Qt

Qt is not automatically entitled to a full implementation. A preliminary evidence note must first prove a material advantage sufficient to justify porting or discarding the existing TypeScript/SVG research.

Possible forms:

- Qt/Python;
- Qt/C++;
- Qt/Rust bindings.

If that threshold is not met, Qt is rejected before the full equivalent scenario.

## 4. Equivalent executable scenario

Every full candidate must use the same fixtures and acceptance script:

1. launch a desktop window;
2. create/open/save a minimal versioned document;
3. render one temporary test symbol and one busbar representation in SVG;
4. select, move and snap through a command;
5. undo and redo;
6. use native open/save dialogs through adapter interfaces;
7. copy/paste structured editor data;
8. accept file drag/drop;
9. read a controlled VSDX fixture and produce structured diagnostics;
10. read a controlled VSSX master fixture;
11. generate a minimal valid VSDX fixture;
12. open the generated file in Microsoft Visio on Windows;
13. export deterministic SVG and PDF fixtures;
14. package and start on Windows and Linux;
15. open/save the same project on both platforms without semantic differences.

The UI must remain deliberately minimal. Visual polish is not evidence in this spike.

## 5. Canonical core proof

The minimum spike document owns:

- `schema_version`;
- stable project/document/object/port/connection IDs;
- one initial document representation;
- explicit equipment-versus-representation ownership boundary;
- document type and profile references;
- source/provenance references;
- import profile and mapping version references;
- compatibility diagnostics;
- isolated foreign payload boundary;
- deterministic serialization.

Required commands:

- `InsertTemporaryObject`;
- `MoveObjects`;
- `DeleteObjects`;
- `ConnectPorts` or a bounded temporary equivalent;
- `Undo`;
- `Redo`.

Direct authoritative document mutation from the UI is prohibited.

## 6. Platform adapter proof

The spike must expose interfaces rather than framework calls inside the core:

- `FileDialogPort`;
- `ProjectFileStore`;
- `ClipboardPort`;
- `NativeDragDropPort`;
- `PrintPort`;
- `ExportDestinationPort`;
- `ProcessToolPort` for controlled VSDX tooling;
- `CrashReportPort`;
- `SystemInfoPort`.

Candidate-specific implementations must remain replaceable.

## 7. Visio interoperability proof

The spike must implement only controlled fixtures, but the evidence must be real:

### Read path

- package relationships;
- pages;
- masters and instances;
- geometry and transforms for the fixture subset;
- text;
- connection points;
- connectors;
- Shape Data;
- source IDs and formulas;
- structured unsupported-feature diagnostics.

### Write path

Generate a minimal `.vsdx` containing:

- one page with explicit size/orientation;
- at least two editable shapes;
- one connector;
- text;
- one Shape Data property;
- valid package relationships.

The Windows evidence must confirm that supported Microsoft Visio opens the file and permits a basic edit/save action.

## 8. Evidence matrix

For every candidate record:

| Area | Required evidence |
|---|---|
| Build | exact commands, tool versions, lockfiles |
| Startup | clean/warm measurements with environment metadata |
| Package | artifact type and size |
| Memory | idle baseline under comparable conditions |
| SVG/editor | pointer, zoom, move and snap behavior |
| Native integration | dialogs, clipboard, drag/drop |
| Storage | deterministic open/save and failure behavior |
| Visio | controlled read/write and Visio-open result |
| Output | deterministic SVG/PDF fixture |
| Testing | unit, component, desktop E2E and package smoke |
| Security | renderer/host/process boundary and permissions |
| Updates | signing/update path and rollback implications |
| Maintenance | languages, dependencies, build complexity |
| Licensing | runtime and packaging implications |

Measurements are comparative evidence for this repository, not universal performance claims.

## 9. Prototype disposition process

Every reused candidate asset must have:

```text
exact path and blob SHA
current responsibility
known defects and limitations
dependencies
proposed target owner
disposition
required tests
migration method
retirement condition
```

Allowed dispositions:

- `retain_as_reference`;
- `salvage_after_tests`;
- `reimplement_from_contract`;
- `retire`.

No item is accepted merely because it currently works in the prototype.

## 10. Work packages

### WP1 — Factual inventory and candidate feasibility

- inventory runtime/editor/tooling assets;
- record exact source SHAs;
- establish candidate dependency/toolchain matrix;
- decide whether Qt clears the full-spike threshold.

### WP2 — Shared fixtures and contracts

- define the minimal document fixture;
- define command/undo fixture;
- define SVG scene fixture;
- define VSDX/VSSX fixtures;
- define deterministic comparison and diagnostics formats.

### WP3 — Candidate A implementation

- Tauri host and adapters;
- bounded core/UI scenario;
- packaging and evidence.

### WP4 — Candidate B implementation

- Electron host and adapters;
- same bounded core/UI scenario;
- packaging and evidence.

### WP5 — Optional Candidate C

Run only after accepted preliminary threshold evidence.

### WP6 — Visio and cross-platform evidence

- Windows Visio open/edit/save evidence;
- Windows/Linux project round-trip;
- package smoke;
- compatibility diagnostics review.

### WP7 — Decision and migration map

- comparison report;
- ADR for desktop host/runtime;
- ADR or architecture amendment for canonical core ownership;
- target repository layout;
- complete prototype disposition;
- exact `CANONICAL-DOCUMENT-CORE-001` boundary.

## 11. Stop conditions

Stop and repair before further expansion if:

- a candidate requires UI-owned authoritative state;
- deterministic round-trip fails;
- the same core cannot be tested outside the desktop shell;
- VSDX generation relies on an online converter;
- unsupported Visio content is silently discarded;
- old `CanvasViewport` or parallel project models are imported wholesale;
- evidence differs between candidates because fixtures or acceptance scripts changed.

## 12. Exit criteria

The spike is a candidate only when:

- full equivalent scenario passes on Windows and Linux for the accepted candidates;
- generated VSDX opens in Visio on Windows;
- one desktop/runtime architecture is selected by accepted ADR;
- one canonical writable document path is proven;
- major prototype assets have dispositions;
- target repository layout is accepted;
- the next production-quality core work item is precise;
- PR remains Draft until explicit owner acceptance.
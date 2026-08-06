# Next Work Item — DESKTOP-PLATFORM-AND-CORE-SPIKE-001

Status: prepared, blocked by acceptance and merge of `PROJECT-REFOUNDATION-001`

## 1. Purpose

Select the desktop/runtime architecture and canonical core ownership using executable Windows/Linux evidence before product feature development resumes.

This work item must also classify prototype assets and prove that no quarantined UI/state/code is inherited automatically.

## 2. Required GitHub contour

Create only after `PROJECT-REFOUNDATION-001` is accepted and merged:

- issue: `[DESKTOP-PLATFORM-AND-CORE-SPIKE-001] Select desktop platform and canonical core boundary`;
- branch: `architecture/desktop-platform-and-core-spike-001`;
- Draft PR linked to that issue.

Do not reuse issue #1, branch `governance/project-refoundation-001` or PR #2 for implementation code.

## 3. Inputs

Mandatory canonical inputs:

- `docs/INDEX.md`;
- `docs/project/CURRENT_STATE.md`;
- `docs/project/PRODUCT_SCOPE.md`;
- `docs/project/PROTOTYPE_QUARANTINE.md`;
- `docs/project/MVP_AND_DEMO.md`;
- `docs/project/IMPLEMENTATION_PROGRAM.yaml`;
- `docs/research/MARKET_ANALYSIS_INTAKE_2026-08-06.md`;
- `docs/architecture/SYSTEM_ARCHITECTURE.md`;
- `docs/architecture/DOMAIN_INVARIANTS.md`;
- `docs/quality/ACCEPTANCE_GATES.md`;
- accepted ADRs.

The accepted market analysis affects benchmark scenarios and platform expectations, but does not permit feature implementation in this spike.

## 4. Questions to decide

1. Which desktop shell/runtime combination gives the best balance for Windows/Linux?
2. Can Vue/TypeScript/SVG remain the editor/rendering layer without inheriting the prototype architecture?
3. Where does the canonical document/domain core live?
4. Is FastAPI retained, reduced to tooling, replaced by direct bindings or removed from runtime?
5. How are Python VSDX tools integrated or packaged?
6. What project/package format is used for the first canonical schema?
7. How are filesystem, clipboard, drag/drop, printing and updates isolated behind adapters?
8. What is the target repository layout?
9. Which prototype assets are retained, salvaged after tests, reimplemented or retired?
10. What minimum schema boundary supports one equipment identity, one initial representation and later controlled multiple representations without overengineering MVP?
11. How will future CIM/calculation adapters attach without becoming the internal document model?

## 5. Candidate technologies

The spike must compare a small justified candidate set, not every framework on the market.

Expected initial candidates:

- Tauri + Vue/TypeScript/SVG + Rust host/core candidate;
- Electron + Vue/TypeScript/SVG + TypeScript core candidate;
- Qt/Python or Qt/C++/Rust candidate only if it can demonstrate a credible migration and testability path.

Candidates may be adjusted at issue creation from current ecosystem evidence, but the selection must remain evidence-based.

A documentation-only comparison is insufficient.

## 6. Equivalent executable scenario

Every candidate must implement the same bounded scenario:

1. launch a desktop window;
2. create/open a minimal canonical test document;
3. render one accepted temporary test symbol and one busbar representation;
4. select, move and snap an object through a command path;
5. perform undo and redo;
6. use native open/save dialog through an adapter;
7. copy/paste structured editor data through clipboard adapter;
8. demonstrate file drag/drop;
9. invoke the VSDX helper path on a controlled fixture;
10. export or print a deterministic SVG/PDF fixture;
11. package and run on Windows and Linux;
12. open the same project file on both platforms without semantic differences.

The scenario is platform/core evidence, not an MVP feature claim. Temporary test symbols must not be promoted into the product library.

## 7. Market-informed usability evidence

The equivalent scenario must also record low-friction editor observations relevant to Visio/Автограф/АСМОграф-class expectations:

- startup and new-project friction;
- pointer/keyboard responsiveness;
- selection and move predictability;
- clipboard behavior;
- native dialogs;
- large-canvas/zoom behavior;
- print/export workflow;
- packaging/install friction.

Do not attempt to reproduce a full competitor workflow during the platform spike. Detailed competitor benchmarking remains P1.

## 8. Comparison evidence

Record for every candidate:

- clean startup time;
- package size;
- idle memory;
- render/pointer behavior on the same fixture;
- implementation complexity;
- automated testability;
- Windows packaging result;
- Linux packaging result;
- native dialog behavior;
- clipboard and drag/drop behavior;
- PDF/print behavior;
- update/signing path;
- Python tooling integration path;
- security surface;
- maintenance burden;
- licensing implications;
- known blockers.

Measurements must identify machine/OS/build conditions and should not be presented as universal benchmarks.

## 9. Prototype asset inventory

Classify at minimum:

- backend `Project` model;
- `project_service.py` persistence/API flow;
- `useProject.ts`;
- `EditorDocument`;
- `EditorCommandStack`;
- `CanvasViewport.vue`;
- renderer/SVG helpers;
- coordinate/snap algorithms;
- busbar calculations;
- shape catalog/palette;
- VSDX inspector;
- ShapeSheet metrics extractor;
- VSDX master converter;
- generated symbol drafts;
- current design-system/CSS/ribbon/property panels;
- build/start scripts;
- existing CI.

For each asset record:

```text
asset
current responsibility
known defects/limitations
dependencies
target owner
disposition
required tests
migration method
retirement condition
```

Default dispositions from `PROTOTYPE_QUARANTINE.md` apply unless evidence justifies an exception.

## 10. Canonical core spike boundary

The work item may implement only the minimum schema/core needed for platform comparison.

It must prove:

- one authoritative writable document;
- stable project/document/object/port/connection IDs;
- explicit equipment-versus-representation ownership boundary;
- document type/profile version reference;
- command-based move and undo/redo;
- deterministic save/open round trip;
- no UI-owned authoritative state;
- no dependency on CIM as internal model;
- extension boundary for states and phase-aware ports without implementing advanced product features.

It must not implement the full symbol platform, topology service or MVP.

## 11. Deliverables

1. Executable candidate spikes.
2. Reproducible build/run instructions.
3. Windows/Linux evidence.
4. Comparative decision matrix.
5. Prototype asset inventory and disposition map.
6. ADR selecting desktop shell/runtime boundaries.
7. ADR or architecture amendment selecting canonical core ownership.
8. Target repository layout.
9. Minimal canonical schema spike and round-trip tests.
10. Updated `CURRENT_STATE.md` and implementation program.
11. Precise next work item for full `CANONICAL-DOCUMENT-CORE-001`.

## 12. Prohibited scope

- redesigning the product UI beyond the temporary spike shell;
- fixing the old prototype UI;
- importing the whole old `CanvasViewport` as accepted code;
- producing the permanent symbol library;
- adding normal/temporary-normal/three-line/operational workflows;
- implementing CIM import/export;
- implementing calculations or SCADA;
- adding hundreds of symbols;
- claiming GOST compliance;
- deleting prototype assets before disposition and retirement criteria are accepted;
- beginning P3/P4 product implementation inside the spike PR.

## 13. Acceptance gates

- same bounded scenario runs on Windows and Linux;
- exact builds and evidence are reproducible;
- selected architecture is justified against rejected candidates;
- one canonical writable document path is proven;
- prototype asset inventory is complete for relevant runtime/editor assets;
- no quarantined UI/state code is inherited without explicit evidence;
- desktop host, editor UI, canonical core and tooling boundaries are explicit;
- future multi-representation and adapter boundaries are possible without making them MVP scope;
- owner accepts the ADR and migration direction;
- PR remains Draft until explicit acceptance command.

## 14. Exit

After acceptance and merge, create:

```text
CANONICAL-DOCUMENT-CORE-001
```

That work item implements the first production-quality versioned project model, commands, persistence, migrations and tests. It must not continue as an unbounded extension of the spike PR.

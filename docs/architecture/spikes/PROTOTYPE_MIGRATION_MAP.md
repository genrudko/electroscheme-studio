# Prototype migration and disposition map

Status: `COMPLETE_FOR_ARCHITECTURE_DECISION`  
Factual source: `PROTOTYPE_ASSET_INVENTORY.yaml` at baseline commit `b95d7111d9c5a36db4c355ee91f742efea8ecc10`.

This map does not authorize deletion, automatic reuse or product promotion. Exact per-file blob SHA, tests and retirement criteria remain canonical in the YAML inventory.

## 1. Reimplement from accepted contracts

These assets contain useful behavior or terminology, but their ownership model conflicts with the accepted architecture:

| Area | Prototype assets | Migration method | Retirement evidence |
|---|---|---|---|
| Canonical schema | backend project schema; `editorDocument.ts` | define a minimal versioned TypeScript core from invariants; write explicit legacy import only when required | no production writer depends on either prototype schema |
| Commands and persistence | `commandStack.ts`; `project_service.py`; project API/router | implement atomic commands/transactions, deterministic serialization and failure-no-change tests | all production mutations pass through the new application command path |
| Editor shell/state | `EditorShell.vue`; `CanvasViewport.vue`; `interactionModes.ts`; context menu | rebuild around read-only projections, typed intents and command dispatch | no Vue component owns authoritative document arrays/objects |
| Preferences/profiles | canvas settings; voltage classes | split user preferences from versioned engineering profiles; fail closed on unknown values | accepted profile package owns normative data |
| Clipboard/drag-drop | `referenceClipboard.ts`; `paletteDragTransfer.ts` | versioned structured payload, ID remapping and platform-port adapters | old global/DOM transfer paths have no production imports |
| Symbol browser/catalog | `ShapePalette.vue`; `shapeCatalog.ts`; VSDX catalog generator | create source/provenance model and explicit review/promotion workflow | generated drafts cannot enter product catalog without gates |
| UI/CSS | ribbon, properties, status, shell CSS, design-system override | rebuild after application/profile contracts; do not migrate DOM selectors | new desktop UI has no dependency on legacy classes |
| Application bootstrap | browser `main.ts`; manifests/start instructions | create selected-host composition root and workspace after ADR | packaged desktop starts without prototype frontend/backend |

The old `CanvasViewport.vue` is explicitly excluded from wholesale migration. Its geometry and interaction behavior must be decomposed into independently tested contracts before any logic is reused.

## 2. Salvage only after new tests

Only bounded logic with a plausible pure boundary may be considered:

- snap/rectangle helpers;
- parametric busbar geometry and port calculations, after separating SVG/HTML output;
- VSDX inspector package traversal;
- ShapeSheet/master metrics extraction;
- master-to-symbol diagnostic conversion;
- voltage/profile data only after evidence and fail-closed semantics.

Required sequence:

1. capture independent golden fixtures and edge cases;
2. specify units, coordinate systems, formula support and diagnostics;
3. copy or rewrite the smallest pure function into the target package;
4. prove behavior without importing prototype modules;
5. record the source blob SHA in the migration commit;
6. retire the prototype implementation only after the target owner passes its acceptance gates.

`salvage_after_tests` means permission to investigate reuse, not a decision to reuse code.

## 3. Retain as reference

The following remain evidence/reference until superseded:

- FastAPI composition and backend/frontend dependency manifests;
- generated VSDX symbol drafts;
- VSDX/VSSX source packages and diagnostics;
- build/start instructions and placeholder CI history.

Reference assets cannot be imported into production packages. Generated drafts cannot become permanent symbols merely because they render.

## 4. Retire rather than migrate

The following responsibilities have no target production owner:

- mutable global `project_service` state and demo fallback;
- packaged loopback FastAPI project/busbar endpoints;
- browser-only API state owner `useProject.ts`;
- global CSS override layer and fixed prototype shell CSS;
- the three-file placeholder CI as quality evidence.

Retirement is delayed until replacement acceptance criteria are met. Physical deletion or relocation requires a later explicit work item.

## 5. Python/Visio migration boundary

Python remains appropriate for package/XML/ShapeSheet tooling, but only behind a controlled process boundary:

- versioned request/response protocol;
- content-addressed inputs and outputs;
- bounded execution time and captured stdout/stderr;
- structured compatibility diagnostics;
- no hidden local paths in generated output;
- no mutation of the in-memory canonical document;
- import/export results applied only through a validated TypeScript transaction;
- actual Microsoft Visio open/edit evidence remains a separate gate.

The prototype generated catalog currently records an absolute `G:\\electroscheme-studio\\Фигуры.vsdx` path. This is a blocking provenance defect, not harmless metadata.

## 6. Migration waves

| Wave | Work item intent | Permitted scope |
|---|---|---|
| 1 | `CANONICAL-DOCUMENT-CORE-001` | TypeScript core package, stable IDs, invariants, transactions, deterministic serializer, fixtures and migration boundary |
| 2 | editor application/geometry | typed intents, selection/view state, snap/coordinates and command dispatch |
| 3 | selected desktop platform | production host adapters, packaging, signing/updater plan and native interaction gates |
| 4 | SVG renderer/editor UI | read-only projections and new UX by contract; no legacy DOM/CSS baseline |
| 5 | Visio source pipeline | controlled read/write protocol, ShapeSheet support matrix, review/promotion workflow and real Visio evidence |
| 6 | prototype retirement | remove or relocate only assets whose target owners and retirement criteria are accepted |

## 7. Non-negotiable cutover rule

There must never be a period in which prototype and target models are both authoritative writers. A legacy reader/importer may coexist temporarily, but every successful write must be performed by exactly one accepted canonical core and transaction path.

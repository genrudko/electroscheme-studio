# Current State — ElectroScheme Studio

Дата среза: 2026-08-06  
Статус: `DESKTOP-PLATFORM-AND-CORE-SPIKE-001` in progress

## 1. GitHub state

- Repository: `genrudko/electroscheme-studio`
- Default branch: `main`
- Accepted refoundation PR: #2
- Accepted PR #2 head: `e1ca482a2cbb4e59acf43474f37e2880ffb24839`
- Merge commit: `b95d7111d9c5a36db4c355ee91f742efea8ecc10`
- Active issue: #3 `DESKTOP-PLATFORM-AND-CORE-SPIKE-001`
- Active branch: `architecture/desktop-platform-and-core-spike-001`
- Active PR: Draft PR for issue #3, created after the first substantive spike commit

Exact PR head, compare state, changed files and workflow results are volatile GitHub state and must be read from GitHub before continuation or acceptance.

## 2. Accepted product direction

ElectroScheme Studio is a standalone, desktop-first and local-first Windows/Linux engineering application.

The target product is:

> a low-friction object editor for power-engineering schemes with typed equipment, ports, topology, switching states, Russian normative profiles and a mandatory Visio migration/exchange bridge.

The first product vertical remains a complete normal single-line scheme workflow.

The product is not currently:

- an EOD module;
- a browser-only service;
- a universal CAD;
- an ETAP/PowerFactory calculation replacement;
- an EPLAN replacement for every electrical discipline;
- a SCADA system.

## 3. Accepted architecture invariants

- one versioned canonical document model;
- one authoritative writable document path;
- command/transaction-based document mutations;
- stable IDs for equipment, representations, objects, ports and connections;
- topology independent from rendered SVG paths;
- UI as projection and command source, not document owner;
- desktop/platform operations behind adapters;
- core tests without the complete desktop UI;
- deterministic and migratable project format;
- Windows/Linux semantic portability;
- VSDX/VSSX as interoperability formats, not the internal model;
- structured diagnostics and no silent import/export loss;
- prototype reuse only through explicit disposition and new tests.

## 4. Prototype status

The pre-refoundation application remains a quarantined engineering prototype.

It contains potentially useful research:

- Vue/TypeScript/SVG editor work;
- rulers, grid, guides and snapping experiments;
- pointer and palette interaction research;
- busbar and slot calculations;
- backend schema/API examples;
- VSDX/VSSX inspection and ShapeSheet extraction tools;
- generated review-required symbol drafts.

It is not:

- product UX baseline;
- visual baseline;
- architecture baseline;
- state-model baseline;
- compatibility baseline.

Default dispositions:

| Area | Default |
|---|---|
| UI/CSS | `reimplement_from_contract` |
| Interaction code | `reimplement_from_contract` |
| Writable state/document models | `reimplement_from_contract` |
| VSDX/VSSX source data | `retain_as_reference` |
| Tested ShapeSheet extraction | `salvage_after_tests` |
| Generated symbol drafts | `salvage_after_tests` |

The active factual inventory is `docs/architecture/spikes/PROTOTYPE_ASSET_INVENTORY.yaml`.

## 5. Known prototype blockers

1. Parallel writable models exist:
   - backend `Project`;
   - frontend `useProject`;
   - frontend `EditorDocument`;
   - local state in `CanvasViewport`.
2. The command stack is not the mandatory path for actual mutations.
3. `CanvasViewport` has monolithic responsibilities.
4. Persistence is not an accepted durable desktop project lifecycle.
5. VSDX tooling does not yet prove editable document import, VSDX export or controlled round-trip.
6. Generated symbols are review candidates, not accepted engineering objects.
7. Current CI is a placeholder and does not protect product behavior.
8. Windows/Linux packaging and cross-platform gates do not exist.
9. Prototype UI accumulated repair/override debt and is not accepted for reuse.

## 6. Active work item

`DESKTOP-PLATFORM-AND-CORE-SPIKE-001` selects the desktop/runtime architecture and canonical core ownership using executable evidence.

Required full candidates:

- Tauri + Vue/TypeScript/SVG;
- Electron + Vue/TypeScript/SVG.

Qt proceeds to a full equivalent implementation only if a preliminary evidence note demonstrates a material advantage sufficient to justify porting or discarding TypeScript/SVG research.

The same bounded scenario must prove:

- desktop launch;
- minimal canonical document create/open/save;
- SVG render and pointer interaction;
- command-based move and undo/redo;
- native dialogs, clipboard and drag/drop through adapters;
- deterministic storage and output;
- controlled VSDX read;
- controlled VSSX master read;
- minimal valid VSDX write;
- generated VSDX open/edit evidence in Microsoft Visio on Windows;
- Windows/Linux package smoke and same-project round-trip.

Execution contract:

- `docs/architecture/spikes/DESKTOP_PLATFORM_AND_CORE_SPIKE_EXECUTION.md`

## 7. Current spike progress

Completed:

- issue #3 created;
- branch created from accepted merge commit;
- execution plan added;
- initial exact-SHA prototype inventory added;
- first high-risk assets classified, including `CanvasViewport`, parallel document models, command stack and VSDX tools;
- canonical documentation index switched to the active work item.

In progress:

- complete prototype asset inventory;
- current candidate/toolchain evidence;
- shared fixture and acceptance definitions;
- Draft PR creation and CI bootstrap;
- executable candidate implementation.

Not yet accepted:

- desktop host;
- canonical core language/ownership;
- project package format;
- FastAPI runtime role;
- Python tooling package strategy;
- Qt full-candidate admission;
- final Visio compatibility profile;
- legacy `.vsd/.vss` migration mechanism.

## 8. Scope prohibitions

Inside this work item do not:

- repair or redesign the old prototype UI;
- port `CanvasViewport` wholesale;
- create the permanent design system;
- build full symbol families;
- implement the complete topology service;
- implement normal/temporary-normal/three-line/operational product workflows;
- implement calculations, SCADA or CIM exchange;
- treat generated VSDX parsing as semantic or normative acceptance;
- delete prototype assets before accepted retirement criteria;
- mark Ready for Review or merge without explicit owner command.

## 9. Program state

| Phase | Status |
|---|---|
| P0 Project refoundation | ACCEPTED / MERGED |
| P1 Market and workflow baseline | STRATEGIC_INPUT_RECEIVED / HANDS_ON_VALIDATION_PENDING |
| P2 Desktop/platform/core and Visio-path spike | IN_PROGRESS |
| P3 Canonical document core | BLOCKED_BY_P2 |
| P4 Editor kernel and design system | NOT_STARTED |
| P5 Symbol platform and VSSX migration | NOT_STARTED |
| P6 Electrical topology | NOT_STARTED |
| P7 Normal single-line MVP plus accepted VSDX import | NOT_STARTED |
| P8 ГОСТ/СТО profiles and output | NOT_STARTED |
| P9 Packaging, Visio export, Demo and Pilot | NOT_STARTED |
| P10 Advanced capabilities | NOT_STARTED |

## 10. Exit from current work item

The spike can become an acceptance candidate only after:

- accepted candidates pass the same scenario on Windows and Linux;
- one architecture is selected by ADR;
- one canonical writable document path is proven;
- major prototype assets have accepted dispositions;
- VSDX/VSSX read/write evidence exists;
- generated VSDX opens in Microsoft Visio on Windows;
- target repository layout is accepted;
- `CANONICAL-DOCUMENT-CORE-001` has an unambiguous boundary.
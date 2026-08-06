# Next Work Item — DESKTOP-PLATFORM-AND-CORE-SPIKE-001

This document defines the next implementation work item after acceptance and merge of `PROJECT-REFOUNDATION-001`.

## Objective

Select the cross-platform desktop/runtime architecture and canonical core ownership using executable Windows/Linux evidence, while completing a full disposition map for the quarantined prototype.

## Required work contour

Create after P0 merge:

- one GitHub issue: `DESKTOP-PLATFORM-AND-CORE-SPIKE-001`;
- one dedicated branch;
- one Draft PR;
- no product feature implementation outside the spike.

## Questions to answer

1. Which desktop shell/runtime provides the best maintainability and user experience on Windows and Linux?
2. Can Vue 3 + TypeScript + SVG be retained as the editor layer without inheriting prototype architecture?
3. Where should the canonical document/domain core live?
4. Is FastAPI needed in the packaged runtime, useful only for tooling, or removable?
5. How should Python VSDX/ShapeSheet tools be integrated and packaged?
6. What project package format best supports portability, recovery and inspectability?
7. Which prototype assets are retained, salvaged, reimplemented or retired?
8. What is the target repository/module layout?

## Candidate requirement

At least two practical desktop architectures must be compared through the same executable scenario.

Expected primary candidates:

- Vue/TypeScript/SVG in a Node-based desktop shell;
- Vue/TypeScript/SVG in a native lightweight shell such as Tauri or an equivalent accepted candidate.

A Qt/native rewrite candidate is included only if a preliminary evidence note shows a material advantage sufficient to justify losing or porting the TypeScript/SVG research.

This wording intentionally avoids preselecting a product by brand.

## Equivalent spike scenario

Each accepted candidate must implement the same minimal scenario:

1. launch a native desktop window;
2. create/open/save a versioned sample project through native dialogs;
3. render an SVG sheet with several objects;
4. zoom and pan;
5. select and move an object through a command;
6. perform undo/redo;
7. use clipboard copy/paste;
8. drag an item from a palette to the canvas;
9. invoke the VSDX helper path on a controlled fixture;
10. export or print a simple SVG/PDF fixture;
11. run automated smoke tests;
12. package and start on Windows and Linux.

The scenario is not a product UI and must use deliberately minimal styling.

## Comparison matrix

Measure and record:

- cold/warm startup;
- package size;
- memory baseline;
- SVG pointer/zoom behavior;
- large-scene baseline;
- native file dialogs;
- clipboard and drag/drop;
- printing/PDF;
- Unicode and long paths;
- Windows installer/portable options;
- Linux packaging options;
- update/signing path;
- Python helper integration;
- crash diagnostics;
- automated test tooling;
- security model;
- maintenance complexity;
- dependency and licensing implications.

## Prototype asset inventory

Inventory at minimum:

- frontend editor components;
- editor libraries and algorithms;
- old `useProject` flow;
- backend project model/API/service;
- VSDX inspector/converter/metrics tools;
- generated symbol catalogs/drafts;
- parametric busbar backend and frontend logic;
- CSS/design files;
- test assets;
- CI/workflows;
- historical PowerShell patch tooling and docs.

Each item receives:

- exact source path/SHA;
- defect/limitation summary;
- disposition;
- target owner module;
- required tests;
- migration sequence.

## Deliverables

- candidate spike code isolated from product feature development;
- Windows evidence;
- Linux evidence;
- comparison report;
- performance measurements;
- full prototype asset inventory/disposition;
- proposed target repository layout;
- proposed canonical document/core boundary;
- ADR selecting the desktop architecture;
- implementation starter for `CANONICAL-DOCUMENT-CORE-001`.

## Prohibitions

- do not redesign the product UI;
- do not migrate large prototype components before disposition;
- do not add symbol families or editor features;
- do not select a candidate based only on popularity or model preference;
- do not require a central server;
- do not preserve prototype defects as compatibility behavior;
- do not merge without owner architecture acceptance.

## Acceptance

The work item is accepted only when:

- both target platforms execute the same scenario;
- comparison evidence is reproducible;
- one architecture is selected in an ADR;
- every major prototype area has a disposition;
- the selected architecture supports a testable core independent of the full UI;
- the next canonical-document implementation boundary is unambiguous.

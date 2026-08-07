# Next Work Item — CANONICAL-DOCUMENT-CORE-001

Status: `PREPARED / BLOCKED_BY_OWNER_ACCEPTANCE_AND_MERGE_OF_PR_4`

## Purpose

Create the first production-owned, versioned **pure TypeScript canonical document core** that becomes the sole writable source of truth for ElectroScheme Studio.

This work item begins only after `DESKTOP-PLATFORM-AND-CORE-SPIKE-001` is explicitly accepted and merged.

## Required prerequisite

Before creating the next issue/branch/Draft PR, verify:

- Draft PR #4 has been explicitly accepted and merged by the owner;
- ADR-0003 and ADR-0004 are accepted through that merge;
- the final documentation-inclusive exact-head CI/platform evidence is green;
- the two manual spike gates are resolved according to owner acceptance;
- `main` contains the accepted P2 state.

Do not implement P3 inside PR #4.

## Exact scope owner

The authoritative scope is:

`docs/project/CANONICAL_DOCUMENT_CORE_001_SCOPE.md`

That scope requires only the production packages needed to establish the canonical core and test fixtures. It explicitly excludes product UI, production desktop-host implementation, full Visio import/export, symbol library, topology service and MVP workflows.

## Architecture inherited from P2

The next work item must preserve:

- Tauri 2 as the selected desktop-host direction;
- Rust limited to host/platform adapters;
- pure TypeScript as the canonical document-core owner;
- Vue/SVG as non-authoritative projection/composition;
- FastAPI excluded from packaged desktop runtime;
- Python Visio tooling behind a bounded versioned process protocol;
- one command/transaction mutation path;
- deterministic Windows/Linux document serialization;
- equipment identity separated from diagram representation;
- provenance, diagnostics and bounded foreign-payload extension points.

## Completion target

`CANONICAL-DOCUMENT-CORE-001` must produce a production-quality package with:

- versioned schema and migrations;
- stable IDs and reference-integrity validation;
- typed commands/transactions;
- deterministic serialization;
- revision/conflict diagnostics;
- undo/redo based on accepted transactions;
- structured clipboard DTOs;
- future Visio import/export boundary DTOs;
- cross-platform byte-stability tests;
- no production dependency on prototype or spike runtime code.

## Prohibited carry-over

Do not:

- extend the spike as an unbounded implementation branch;
- repair the old prototype UI;
- migrate `CanvasViewport.vue` wholesale;
- create the production symbol library;
- implement full topology;
- implement full VSDX/VSSX import/export;
- add calculations, SCADA or CIM;
- introduce a second writable project model.

## GitHub contour

Create a new issue/branch/Draft PR for `CANONICAL-DOCUMENT-CORE-001` **only after** owner acceptance and merge of PR #4.

The exact issue number, branch and PR are intentionally not pre-created here.

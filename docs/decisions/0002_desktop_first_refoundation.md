# ADR 0002 — Desktop-first refoundation with quarantined prototype reuse

Status: accepted for `PROJECT-REFOUNDATION-001`  
Date: 2026-08-06

## Context

The initial prototype was built as a local WebUI using FastAPI, Vue 3, TypeScript and SVG. It produced valuable research in VSDX/ShapeSheet import, electrical symbols, parameterized busbars, snapping and editor interaction.

The prototype also accumulated:

- parallel document/state models;
- monolithic editor ownership;
- incomplete undo/redo integration;
- in-memory persistence;
- weak CI;
- repeated UI/CSS repair patches;
- visual and interaction behavior not accepted as product quality;
- no Windows/Linux desktop packaging contract.

The owner requires a standalone application for Windows and Linux. Browser-only architecture is not mandatory. Existing prototype defects and visual decisions must not become inherited product behavior.

## Decision

1. ElectroScheme Studio is refounded as a **desktop-first, local-first, cross-platform engineering product**.
2. Windows and Linux are mandatory product platforms.
3. GitHub issue/branch/Draft PR/evidence workflow becomes the canonical development process.
4. The current `main` head `6e1209d800c0cc65da4a922506586d5a100c2a84` is preserved as a **quarantined prototype baseline**, not as product architecture or UX baseline.
5. Existing Vue/TypeScript/SVG and Python assets may be reused only after explicit asset disposition and target-contract tests.
6. UI/CSS, editor interactions and state ownership default to `reimplement_from_contract`.
7. VSDX/VSSX source data, ShapeSheet research and normative evidence default to preservation as source/reference; generated/runtime code still requires validation.
8. The final desktop shell is not selected in this ADR. It must be selected by an executable Windows/Linux comparative spike.
9. One canonical versioned document model and one command-based mutation path are required before feature development resumes.
10. A fresh design system and interaction specification are required; the prototype appearance is not a golden reference.

## Consequences

### Positive

- Product architecture is selected from measured cross-platform evidence.
- Existing knowledge is retained without inheriting defects automatically.
- Data model, topology and undo/redo become foundational rather than retrofitted.
- UI can be redesigned for electrical-engineering workflows instead of repaired incrementally.
- Project files and output can be tested consistently on Windows and Linux.
- GitHub becomes a reproducible source of truth comparable to the mature EOD workflow.

### Negative / cost

- Some prototype code will be rewritten even when superficially functional.
- Feature progress pauses during refoundation and platform/core spikes.
- A temporary period will exist where the quarantined prototype and new core coexist in the repository.
- Cross-platform packaging and testing increase engineering effort.
- VSDX/Python integration may require helper-process or packaging work depending on the selected shell.

## Rejected alternatives

### Continue patching the existing WebUI directly

Rejected because it would preserve duplicate state ownership, UI repair debt and weak persistence/undo contracts.

### Delete the repository and start with an empty project immediately

Rejected because useful source data, VSDX tooling, metrics, algorithms and domain research would be lost or needlessly rediscovered.

### Select Electron/Tauri/Qt immediately by preference

Rejected because filesystem, printing, SVG interaction, Python tooling, packaging and maintenance must be compared with executable evidence.

### Keep both backend Project and frontend EditorDocument as independent authoritative models

Rejected because informal synchronization would create data loss and semantic divergence.

### Treat the prototype UI as the first design iteration

Rejected by owner clarification: current appearance and behavior were not acceptable and must not define the new product.

## Follow-up

After merge of `PROJECT-REFOUNDATION-001`, create:

`DESKTOP-PLATFORM-AND-CORE-SPIKE-001`

It must:

- build equivalent minimal editor scenarios for accepted architecture candidates;
- run on Windows and Linux;
- classify prototype assets;
- decide runtime boundaries and repository layout;
- select the desktop shell through a follow-up ADR;
- refrain from product feature expansion.

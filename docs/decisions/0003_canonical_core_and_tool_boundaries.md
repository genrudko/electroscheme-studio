# ADR-0003: canonical document core and tool boundaries

- Status: accepted by executable spike; pending owner acceptance of PR #4
- Date: 2026-08-06
- Work item: `DESKTOP-PLATFORM-AND-CORE-SPIKE-001`

## Context

The quarantined prototype has multiple potential writable owners:

- backend Pydantic project DTOs and mutable `project_service` state;
- FastAPI mutation endpoints;
- frontend `useProject.ts` API state;
- `editorDocument.ts` types;
- arrays and objects owned directly by `CanvasViewport.vue`;
- an undo/redo stack that is not the exclusive mutation path.

That design cannot provide deterministic files, reliable undo/redo, atomic import or loss diagnostics. VSDX/VSSX and CIM also cannot become the internal project model because they have different purposes and compatibility semantics.

The executable spike proves a minimal core with stable identity, deterministic serialization, command-only mutation and identical logical output under both mandatory desktop candidates.

## Decision 1: one writable canonical core

The only authoritative writable project/document model will live in a **pure TypeScript package** named conceptually `packages/canonical-document-core`.

It owns:

- versioned schema and migrations;
- project/document/sheet/layer/equipment/representation/object/port/connection identity;
- separation of equipment identity from diagram representation;
- document type and profile/version references;
- source/provenance and import-mapping references;
- foreign/opaque non-authoritative payload boundaries;
- compatibility diagnostics;
- commands, transactions and undo/redo history;
- deterministic serialization and validation.

The core must run and be testable without Vue, browser APIs, SVG DOM, desktop host, FastAPI, Python, VSDX or CIM.

## Decision 2: Vue/TypeScript/SVG responsibility

Vue and the SVG renderer remain the editor composition and rendering layer, but they are projections over canonical state.

They may own ephemeral view state such as:

- current selection;
- hover/focus;
- viewport transform;
- open panels;
- pointer gesture state;
- temporary command previews.

They may not own or directly mutate authoritative engineering objects. Every successful user edit is dispatched as a typed command/transaction to the canonical core. The prototype `CanvasViewport.vue` is therefore reimplemented from contracts rather than migrated as a state owner.

## Decision 3: FastAPI is not packaged desktop runtime

FastAPI is not required by the executable scenario and will **not** be part of the packaged desktop runtime.

Reasons:

- a loopback HTTP server creates an unnecessary second lifecycle, network surface and failure mode;
- the prototype endpoints permit direct mutation and do not enforce the accepted transaction path;
- filesystem, dialogs, clipboard, drag/drop, printing and local process supervision are host capabilities, not HTTP services;
- the same TypeScript core can run in-process in both desktop candidates.

FastAPI may remain temporarily as a quarantined research/developer facade. Any retained tool API must be explicitly non-authoritative and must call accepted libraries rather than owning state.

## Decision 4: Python Visio tooling boundary

Python remains the preferred implementation language for bounded VSDX/VSSX/OOXML/ShapeSheet tools because the prototype contains useful package and extraction knowledge and the executable spike proves a local process boundary.

The boundary is:

- a versioned JSON request/response protocol;
- content-addressed input/output artifacts;
- bounded execution time;
- captured exit code/stdout/stderr;
- structured diagnostics and source IDs;
- deterministic package generation where possible;
- no direct access to the in-memory writable canonical document;
- no silent fallback or local absolute path in generated provenance;
- import/export results are applied only through a validated TypeScript transaction.

Python is therefore a tool runtime, not a second canonical core and not a permanent HTTP sidecar.

## Decision 5: platform capabilities

Reusable application packages depend only on typed ports for:

- filesystem;
- native open/save dialogs;
- structured clipboard;
- internal and native file drag/drop;
- PDF/printing;
- updater/signing hooks;
- process tools;
- platform information.

The selected desktop host implements these adapters. Host code may not define domain commands, project schema or renderer state.

## Executable evidence

The spike demonstrates:

- deterministic canonical JSON round trip with no semantic diff;
- stable IDs and identity/representation split;
- command-only move/snap, undo and redo;
- deterministic SVG and PDF fixtures;
- structured clipboard;
- the same Vue/SVG editor fixture in both candidates;
- packaged Windows/Linux filesystem, clipboard, PDF and Python-tool scenarios;
- controlled VSDX/VSSX reads and minimal VSDX generation from canonical JSON;
- a separate manual gate for actual Microsoft Visio open/edit/save.

## Consequences

Positive:

- one owner of truth and one mutation path;
- deterministic, testable local-first documents;
- desktop host can be replaced without rewriting domain state;
- Python tooling can evolve independently behind a stable protocol;
- Vue/SVG remains usable without inheriting prototype architecture.

Costs:

- the prototype backend/frontend models need explicit migration or retirement;
- application commands and projections must be rebuilt;
- cross-language protocol/version compatibility becomes a maintained contract;
- UI code cannot use convenient direct `v-model` mutation for document objects.

## Rejected alternatives

### Python/Pydantic canonical core

Rejected for the desktop product because it would require a permanent Python process/binding boundary for every edit and preserve a second runtime lifecycle without evidence of a compensating benefit.

### Rust canonical core in the initial product

Rejected for the next work item because both mandatory candidates already prove the required invariants in pure TypeScript, while a Rust core would require bindings and duplicate schema/serialization concerns before domain complexity justifies them. Rust remains appropriate for selected-host adapters if the desktop-host ADR selects Tauri.

### FastAPI loopback runtime

Rejected as unnecessary infrastructure and a second attack/failure surface.

### Vue store or SVG DOM as document model

Rejected because view lifecycle, rendering nodes and interaction state are not durable engineering identity.

### VSDX or CIM as internal model

Rejected because both are external exchange/provenance models and cannot satisfy the editor's single-writer and no-silent-loss contracts.

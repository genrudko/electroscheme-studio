# CANONICAL-DOCUMENT-CORE-001 — exact proposed scope

Status: `NEXT_AFTER_OWNER_ACCEPTANCE_OF_PR_4`  
Prerequisite: accepted `DESKTOP-PLATFORM-AND-CORE-SPIKE-001` and its host/core ADRs.

## Objective

Create the first production-owned, versioned TypeScript canonical document core that becomes the sole writable source of truth for ElectroScheme Studio. This work item replaces the spike fixture with an intentionally small production foundation; it does not build product UI or full electrical-domain workflows.

## Required production boundary

Create only the minimum target packages required for the core:

```text
packages/
  canonical-document-core/
  test-fixtures/
```

A root workspace may be introduced only to build and test these packages reproducibly. The selected desktop host, production Vue UI, SVG renderer, Python tool package and prototype relocation are not implemented here.

## Required model slice

The versioned schema must include stable identities and references for:

- project;
- document;
- sheet;
- layer;
- equipment identity;
- diagram representation;
- diagram object;
- port;
- connection;
- document type;
- profile and profile-version reference;
- source/provenance reference;
- import-mapping version;
- compatibility diagnostics;
- bounded foreign/opaque payload marked non-authoritative.

The work item must preserve the distinction between equipment identity and one or more diagram representations. It must not encode SVG nodes, Vue state, VSDX structures or CIM objects as the canonical model.

## Required behavior

1. Define schema versioning and explicit migration entry points.
2. Define deterministic stable-ID creation/injection policy suitable for import and new documents.
3. Implement validation of identity uniqueness and reference integrity.
4. Implement immutable or transaction-isolated state transitions.
5. Implement a typed command envelope with command ID, expected document revision and provenance metadata.
6. Implement atomic transaction application: complete success or no state change.
7. Implement undo/redo as reversible accepted transactions, not arbitrary callback closures.
8. Implement deterministic serialization with normalized ordering and line endings.
9. Implement deterministic parse/serialize/parse equality.
10. Define conflict/revision failure diagnostics.
11. Define structured clipboard DTO and deterministic ID remapping without platform APIs.
12. Define import/export boundary DTOs for future Visio tools without spawning Python.
13. Define read-only projection interfaces for future application/renderer layers.

## Fixtures

Promote a production-owned fixture set derived from, but not imported from, the spike:

- minimal empty project;
- one document/sheet/layer;
- equipment with one representation and ports;
- busbar representation;
- connection;
- provenance/opaque payload example;
- compatibility warning/error example;
- legacy prototype input fixture used only to prove explicit migration or rejection.

Fixtures must use fixed IDs and contain no local absolute paths, timestamps or host-specific metadata unless those fields are deliberately normalized.

## Mandatory tests

### Schema and invariants

- duplicate IDs rejected across the declared identity namespace;
- dangling references rejected;
- equipment/representation separation enforced;
- unsupported schema/profile/import-mapping versions fail closed;
- opaque payload cannot become authoritative state;
- VSDX/CIM/SVG/Vue/desktop-host dependencies are absent.

### Commands and transactions

- create/update/move/delete/connect/disconnect minimum command set;
- expected-revision mismatch rejected;
- partial failure leaves byte-identical prior state;
- deterministic command result for identical input;
- undo and redo restore exact logical revisions;
- deleting referenced entities requires explicit validated cascade policy;
- command history is not serialized as authoritative engineering content unless separately specified.

### Serialization and migration

- byte-identical output on Windows and Linux;
- parse/serialize round trip without semantic diff;
- stable ordering independent of insertion order;
- line-ending and numeric normalization;
- previous supported version migrates deterministically or is rejected with structured diagnostics;
- malformed/unknown input cannot silently drop data.

### Quality and ownership

- package builds and tests independently of prototype/frontend/backend;
- changed-scope gate prevents UI/host/Visio implementation creep;
- dependency graph proves no imports from `prototype` or `spikes`;
- mutation coverage proves no public direct-write escape hatch;
- generated API/schema documentation is reproducible.

## Required decisions inside the work item

- exact file extension and media type for the native project document;
- schema-version and profile-version compatibility policy;
- stable-ID format and import ID mapping rules;
- numeric/unit normalization conventions;
- transaction revision model;
- diagnostic schema and severity semantics;
- foreign payload size/security limits;
- first supported migration boundary from the quarantined prototype, including an explicit decision to migrate, preserve as opaque data or reject each legacy field.

## Explicit exclusions

Do not implement:

- production desktop host or installer;
- Vue screens, ribbon, palette, properties/status UI or visual redesign;
- SVG interaction renderer beyond non-authoritative test projections;
- full symbol library or ShapeSheet master promotion;
- Python process execution;
- full VSDX/VSSX import/export;
- Microsoft Visio automation;
- full electrical topology or domain schema P3;
- normal, temporary-normal or three-line operational workflows;
- calculations, SCADA or CIM;
- prototype deletion/relocation;
- production updater/signing.

## Acceptance deliverables

1. production TypeScript package and exact dependency lock;
2. versioned schema and generated schema documentation;
3. commands/transactions/history implementation;
4. deterministic serializer/parser/migration entry points;
5. shared production fixtures;
6. complete invariant/command/round-trip/cross-platform tests;
7. dependency and changed-scope gates;
8. architecture documentation updated from spike to production owner;
9. migration decision table for every prototype project/document field;
10. exact next work item selected from evidence, without beginning it.

## Completion condition

`CANONICAL-DOCUMENT-CORE-001` is complete only when the new package is demonstrably the sole intended production writer and no production path needs the prototype backend, `useProject.ts`, `editorDocument.ts`, `commandStack.ts` or `CanvasViewport.vue` to create, mutate, serialize or validate a project document.

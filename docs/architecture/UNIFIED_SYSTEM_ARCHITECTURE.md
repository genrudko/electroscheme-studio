# Unified System Architecture

Статус: canonical foundation document

## 1. Architectural style

Target architecture is a **modular monolith desktop application**.

Rationale:

- one primary user workstation/local project;
- shared in-memory/project domain model;
- strong transactional and undo/redo requirements;
- low value from network boundaries between modules;
- one main developer/maintainer requires low operational complexity;
- modules still need explicit ownership and test isolation.

Microservices, separate web backend and plugin marketplace are not architectural goals.

## 2. High-level structure

```text
┌───────────────────────────────────────────────────────┐
│                     Application                       │
│  startup / module composition / workspace / commands │
└──────────────┬────────────────────────────────────────┘
               │
      ┌────────┴────────┐
      │     UI Core     │
      │ shell + shared  │
      │ desktop UX      │
      └────────┬────────┘
               │
┌──────────────┴────────────────────────────────────────┐
│                    Domain Core                        │
│ project/equipment/terminal/connection/topology/state │
│ validation/transactions/versioned persistence model  │
└─────┬──────────┬──────────┬──────────┬───────────────┘
      │          │          │          │
      ▼          ▼          ▼          ▼
 Equipment    Import      Schemes    Compliance
 Library      Module      Module      Core
      │          │          │          │
      └──────────┼──────────┼──────────┘
                 │          │
                 ▼          ▼
              NPT Module  Switching/TBP
                 │          │
                 └────┬─────┘
                      │
                 Optional adapters
                 ├── platform/native
                 ├── EOD (feasibility-gated)
                 └── future exchange
```

## 3. Ownership rule

Every concept has one authoritative owner.

Examples:

| Concept | Owner |
|---|---|
| equipment identity/type/properties | Domain Core + Equipment Library definition |
| terminals/connections | Domain Core |
| electrical topology | Domain Core topology service/model |
| equipment state | Domain Core state model |
| diagram geometry | Scheme module view model |
| manual layout constraints | Scheme module |
| import mapping/staging | Import module |
| normative source/rule metadata | Compliance Core |
| NPT `sTag`/RTID/scd serialization | NPT module |
| switching sequence | Switching module |
| app shell/workspace | UI Core |
| EOD module registration/deep links | optional EOD adapter |

If two modules both persist authoritative copies of the same engineering fact, architecture is wrong unless an explicit synchronization contract is documented.

## 4. Dependency direction

Preferred dependency direction:

```text
App
↓
UI Core / module UIs
↓
Module application services
↓
Domain Core + Compliance Core
↓
Infrastructure/platform/storage adapters
```

NPT, EOD, Excel, Visio or other external formats must not be dependencies of neutral domain types.

### Forbidden dependency examples

- `Domain.Device` containing `SdeTag` or `EodJournalId` as required fields;
- topology service calling NPT XML parser directly;
- UI Core depending on switching-form templates;
- native project storage requiring Excel workbook presence;
- Scheme renderer using NPT `CustElem` as the only native symbol model.

## 5. Module contracts

Modules communicate through typed in-process contracts and domain IDs, not direct mutation of each other's private storage.

Example:

```text
Import Module
  produces ImportPlan
       ↓ approved transaction
Domain Core
  updates Equipment/Connections
       ↓ domain change set
Scheme Module
  computes incremental layout proposal
```

Similarly:

```text
Switching Module
  proposes Operation
       ↓
Compliance/Interlock evaluator
       ↓
Domain state transition simulation
       ↓
Topology recalculation
       ↓
Switching sequence result
```

## 6. Project persistence layers

Native persistence is conceptually split:

```text
Project Package
├── domain model
├── view/layout data
├── compliance/profile references
├── module-owned extension data
├── source provenance/import mappings
└── attachments/metadata as needed
```

Exact physical format remains PENDING until Domain Core spike. Requirements:

- human/diagnostic readability where reasonable;
- explicit schema version;
- deterministic IDs;
- migrations;
- unknown forward-compatible extension policy;
- atomic save/backup/recovery strategy;
- no dependency on vendor file format as native schema.

## 7. Transactions and commands

All engineering mutations that affect project meaning must support:

- validation before/after as appropriate;
- undo/redo or explicit non-undoable classification;
- atomic persistence boundary;
- change-set/diff generation;
- event notification to dependent views;
- provenance for import/generated changes where relevant.

A UI component must not directly patch arbitrary project dictionaries/JSON structures.

## 8. Topology vs view separation

Electrical topology:

```text
Terminal A ─ Connection ─ Terminal B
```

Visual route:

```text
screen polyline / bends / layers / labels
```

The same connection may have different routes in different views. Moving a symbol must not silently change electrical topology. Reconnecting a terminal is an engineering mutation and must be explicit/validated.

## 9. State model

State is semantic and separate from rendered colors/shapes.

Example:

```text
CircuitBreakerState = OPEN | CLOSED | INTERMEDIATE | UNKNOWN
Quality = GOOD | BAD | UNCERTAIN | UNKNOWN
```

Renderer maps state/profile to appearance. Switching simulation changes semantic state, then views update.

`UNKNOWN` cannot be collapsed into a safe/disabled state.

## 10. Compliance integration

Compliance Core provides:

- source registry;
- rule registry;
- applicability resolution;
- profile composition;
- local overlays;
- conflict/non-weakening checks;
- explainable validation results.

Module code may implement specialized evaluators, but normative identity/source metadata remains in Compliance Core contracts.

## 11. UI architecture boundary

UI Core owns interaction infrastructure, not engineering meaning.

For example Property Inspector is shared UI infrastructure, while actual editors/validators for breaker state or NPT `scdCommand` are registered by modules/domain descriptors.

Shared controls must be reusable without importing an entire product module.

## 12. Module activation

Early implementation may compile all first-party modules into one application. Module enablement is configuration/composition, not dynamic plugin loading requirement.

A module must declare:

- module ID/version;
- dependencies;
- capabilities/views/commands contributed;
- project extension ownership;
- compatibility/migration requirements.

Dynamic external plugins can be evaluated only after internal module contracts stabilize.

## 13. External adapters

### Platform adapter

Filesystem, dialogs, clipboard, print, OS integration, window management and packaging-specific functions remain behind platform boundaries where framework abstraction is insufficient.

### NPT adapter

NPT file semantics and vendor-specific identifiers remain isolated.

### EOD adapter

Optional, independently removable, no reverse dependency from Core.

### Future adapters

CIM, other ECAD/CAD formats or operational data sources may be added later if product workflows justify them.

## 14. Performance strategy

Performance is part of architecture, especially for:

- tens of thousands of rendered electrical objects;
- large equipment lists/tables;
- fast hit-testing/selection;
- topology recalculation;
- import diff/reconciliation;
- multi-window workspaces.

Do not model each rendered primitive as a heavyweight desktop control if benchmarks show it does not scale. Canvas implementation strategy is decided by Platform Spike evidence.

## 15. Security and trust boundary

The product is local-first but still handles imported/vendor files and optional external integrations.

Requirements:

- parsers treat imported content as untrusted data;
- no arbitrary code execution from project/import files;
- module/adapters validate paths and file operations;
- EOD/NPT integration does not grant broader OS privileges than needed;
- development runner contains no production SCADA credentials.

## 16. Architectural review triggers

An ADR/update is mandatory before:

- changing source-of-truth ownership;
- introducing separate service/process as required runtime;
- adding a second authoritative equipment/topology store;
- changing native project format incompatibly;
- allowing local policies to override mandatory baseline;
- adding online real-equipment command execution;
- making EOD/NPT a required dependency;
- switching platform/framework after accepted Platform Stack ADR.

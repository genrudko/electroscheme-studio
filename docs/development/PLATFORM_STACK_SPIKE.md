# Platform Stack Spike — Avalonia vs Qt 6

Статус: canonical decision contract  
Decision: **PENDING — DO NOT SELECT BY PREFERENCE**

## 1. Objective

Choose the desktop/UI/runtime stack for the unified product using equivalent executable evidence on realistic electrical-engineering workloads.

Final candidates:

```text
A) C# / .NET + Avalonia
B) C++ + Qt 6 / QML (with lower-level scene/rendering code where justified)
```

The existing Tauri/Vue/TypeScript/SVG Draft PR #4 remains historical benchmark/research evidence but is not a final candidate under the new unified scope.

## 2. Decision dimensions

The winning stack must minimize **total project risk and iteration cost**, not only maximize raw FPS.

Weighted decision areas:

1. heavy electrical canvas performance/scalability;
2. professional desktop UI quality and component productivity;
3. large tree/table performance;
4. multi-window/multi-monitor/mixed-DPI correctness;
5. deterministic rendering/print/export path;
6. headless/visual testability;
7. domain-core/test development productivity;
8. packaging and Windows/Linux distribution;
9. debugging/profiling/tooling;
10. dependency/licensing/maintenance burden;
11. build time and owner feedback-loop duration;
12. agent/code-maintenance complexity for a small team.

Weights and thresholds are written before final benchmark results are reviewed to reduce winner-shopping.

## 3. Equivalent architecture

Both candidates implement the same conceptual layers:

```text
App Shell
UI Core
Minimal Domain Core
Scheme Canvas
Virtualized Equipment Table
Properties Inspector
Command/Undo path
Project persistence fixture
```

Do not sabotage one candidate with intentionally naive implementation while optimizing the other.

Use idiomatic but comparable framework approaches.

## 4. Required executable scenario

### Scenario A — Application shell

- launch native desktop app;
- open/create one sample project;
- document tabs;
- properties panel;
- equipment tree/table;
- status/diagnostics;
- theme tokens/design-system sample.

### Scenario B — Multi-window/workspace

- detach one document into second top-level window;
- persist/restore positions;
- move between monitors/scales in manual Windows acceptance;
- close/reopen workspace;
- simulate missing second monitor and recover layout.

### Scenario C — Heavy scheme canvas

Render semantic electrical symbols/connections, not arbitrary colored rectangles only.

Datasets:

```text
S:   2,000 visible objects
M:  10,000 visible objects
L:  25,000 visible objects
XL: 50,000 visible objects or platform limit with documented reason
```

Each dataset includes:

- equipment symbols;
- text labels;
- buses/lines/routes;
- state variation;
- selection overlays;
- hit-test spatial index;
- zoom/pan.

Measure:

- startup/project-load time;
- first render;
- steady zoom/pan frame timing;
- selection/hit-test latency;
- drag latency;
- memory;
- CPU;
- object update/re-render cost;
- screenshot/export time.

If framework-native item-per-object approach fails, candidate may use custom scene/drawing layer, but implementation complexity is part of score.

### Scenario D — Electrical edit path

- select breaker/disconnector;
- move representation without changing topology;
- reconnect semantic terminal as explicit command;
- undo/redo;
- edit typed property;
- state change updates representation;
- validation error locates item.

### Scenario E — 100k equipment table

- 100,000 rows;
- columns with text/numeric/enum/status;
- virtualized scrolling;
- sort;
- filter/search;
- multi-select;
- edit one cell through command path;
- copy selected rows.

Measure interaction latency/memory.

### Scenario F — Import review

Use a representative staging diff table:

- 10k source rows;
- resolved/new/changed/conflict statuses;
- filter to conflicts;
- inline resolution editor;
- apply a small ImportPlan.

This tests product-relevant data UX rather than generic widgets.

### Scenario G — UI Gallery / visual testing

- render shared controls/states without full product;
- capture deterministic screenshot headlessly or in reproducible virtual display;
- compare screenshot with baseline/tolerance method;
- produce artifact in CI.

If true headless rendering is impossible, document the nearest reliable strategy and cost.

### Scenario H — print/vector output

- render representative single-line page;
- export PDF/vector or framework-appropriate deterministic print representation;
- verify text/line geometry and reproducibility;
- open output in independent viewer during owner acceptance.

### Scenario I — packaging

For Windows and Linux:

- clean build from lock/pinned environment;
- package runnable preview;
- measure package size;
- startup time;
- memory after ready;
- required external runtime/dependencies;
- restore/run artifact from clean directory.

## 5. Development-loop benchmark

Critical because prior workflows became too slow.

For each candidate measure wall-clock and developer steps for:

### Change 1 — UI-only

`increase Inspector group spacing + adjust icon alignment`

Pipeline target:

```text
edit
→ targeted compile/test
→ Gallery screenshot
→ preview artifact
```

### Change 2 — Domain rule

`add one equipment validation rule + tests`

### Change 3 — canvas behavior

`change selection handle behavior + interaction test`

Record:

- changed files/LOC;
- compile/test time warm/cold;
- runner time;
- artifact time;
- amount of framework boilerplate;
- debugging effort.

This metric has explicit decision weight.

## 6. Domain core comparison

Implement the same tiny model/tests in both languages:

```text
ElectricalProject
Equipment
Terminal
Connection
TopologyGraph
EquipmentState/UNKNOWN
Command transaction
serialization round-trip
```

Compare:

- clarity/type safety;
- test ergonomics;
- serialization/versioning options;
- graph/domain implementation complexity;
- property-based/fuzz testing tooling;
- debugging/profiling.

Do not build full Domain Core during spike.

## 7. Platform-specific native integration

Prove through adapters:

- file open/save;
- clipboard structured data;
- drag/drop file;
- print/export;
- top-level window management;
- platform-safe paths;
- HiDPI reporting.

No framework object is allowed to become canonical project serialization merely because it is convenient.

## 8. Test matrix

Automated minimum:

- Linux runner build/test;
- Windows runner build/test where available;
- unit/domain tests;
- UI Gallery capture;
- canvas benchmark artifact;
- table benchmark;
- package/restore/start check.

Manual owner evidence:

- native Windows interaction;
- visual quality;
- multi-monitor/mixed-DPI if hardware permits;
- overall desktop feel/input latency;
- PDF/print independent viewing.

## 9. Licensing/dependency gate

Before selection, record for exact framework/version:

- software licenses and distribution obligations;
- static/dynamic linking implications where relevant;
- commercial-license dependency if any feature requires it;
- third-party packages/components used by spike;
- long-term support/version policy;
- security/update strategy.

Do not rely on remembered license summaries.

## 10. Scoring

Decision report must show raw measurements first, then scoring.

Recommended shape:

| Dimension | Weight | Avalonia | Qt | Evidence |
|---|---:|---:|---:|---|
| canvas scalability | high | | | |
| UI/desktop quality | high | | | |
| DevEx iteration cost | high | | | |
| tables/tree | medium-high | | | |
| multi-monitor/HiDPI | high | | | |
| testing/visual CI | high | | | |
| packaging | medium | | | |
| domain/test productivity | medium-high | | | |
| maintenance/licensing | medium-high | | | |

No hidden tie-breaker based on prior preference.

## 11. Selection rule

Qt should win if its performance/desktop capabilities provide a **material, measured advantage** large enough to justify higher implementation/toolchain complexity for this small-team project.

Avalonia should win if it meets representative performance/desktop thresholds with simpler/faster maintainable C#/.NET development.

If neither candidate meets a mandatory threshold, stop and revisit architecture rather than selecting the less-bad one by inertia.

## 12. Relationship to old Tauri spike

PR #4 evidence remains useful for:

- packaging baseline;
- native dialog/clipboard/drop failure lessons;
- deterministic artifact methodology;
- Windows/Linux CI ideas;
- Visio tooling boundary evidence.

It does not exempt Avalonia/Qt candidates from equivalent proof and must not be merged as product foundation solely because its CI is green.

## 13. Outputs

`PLATFORM-STACK-SPIKE-001` produces:

- both candidate implementations;
- benchmark datasets/generator;
- raw JSON/CSV measurements;
- screenshots/videos where needed;
- package artifacts;
- dependency/license report;
- comparative matrix;
- owner manual acceptance record;
- final ADR selecting stack;
- target repository layout and immediate UI/Domain foundation work item.

## 14. Prohibited scope

- full product migration;
- full symbol library;
- full NPT renderer;
- full switching engine;
- design-system perfection;
- selecting stack before equivalent measurements;
- optimizing benchmark implementation in a way not available to production architecture.

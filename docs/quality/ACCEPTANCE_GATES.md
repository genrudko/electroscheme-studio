# Acceptance Gates — ElectroScheme Studio

## 1. Purpose

A change is accepted only when its risks are covered by reproducible GitHub evidence. A successful compile alone is not acceptance for an engineering editor.

## 2. Required PR evidence

Every product PR must state:

- work item and issue;
- exact base and head;
- changed-file boundary;
- architecture/domain invariants affected;
- project-format or migration impact;
- Windows/Linux impact;
- tests executed and exact results;
- visual evidence when UI/render/export changes;
- known limitations;
- rollback/recovery considerations.

PR remains Draft until implementation and evidence are complete.

## 3. Gate classes

### G0 — Repository and governance

Required for every PR:

- branch belongs to the active issue;
- no unrelated changes;
- canonical docs updated when ownership/contracts change;
- no secrets or local absolute paths in production configuration;
- dependency changes are explicit and justified;
- generated artifacts are reproducible or intentionally versioned.

### G1 — Source and static validation

Applicable checks:

- formatting/linting selected by the accepted stack;
- TypeScript strict typecheck for accepted frontend/product code;
- Python/Rust/native static checks where applicable;
- schema validation;
- dependency lock consistency;
- duplicate route/registration and dead generated-code checks;
- UTF-8 and cross-platform path checks.

A Vite build that transpiles despite type errors is not sufficient.

### G2 — Domain core

Required for document/core changes:

- stable ID tests;
- invariant tests;
- command atomicity;
- undo/redo exactness;
- deterministic serialization;
- no-op round trip;
- migration from every supported schema fixture;
- fail-closed unsupported schema behavior;
- corrupted-file and failed-save recovery tests.

### G3 — Symbol platform

Required for each accepted symbol family/version:

- source/provenance recorded;
- geometry and physical dimensions checked;
- ports and directions checked;
- rotation/mirroring checked;
- snapping checked;
- stretch/parameterization checked when applicable;
- states and properties checked;
- save/load round trip;
- interactive renderer golden;
- SVG/PDF golden;
- Windows/Linux visual tolerance.

Generated VSDX drafts cannot bypass this gate.

### G4 — Topology

Required for connection changes:

- valid port-to-port creation;
- incompatible endpoint rejection/diagnostic;
- move/rotate topology preservation;
- junction versus visual crossing behavior;
- delete/cascade/detach policy;
- waypoint editing without endpoint change;
- undo/redo;
- serialization and reopening;
- multi-object copy with internal connections;
- dangling-reference diagnostics.

### G5 — Editor interaction

Required for UI interaction changes:

- automated interaction test for the primary flow;
- pointer/mouse behavior;
- keyboard shortcut behavior;
- focus and text-input isolation;
- zoom/pan coordinate correctness;
- selection and multi-selection;
- drag cancellation and pointer capture recovery;
- command/undo integration;
- no direct document mutation bypass;
- visual evidence on Windows and Linux for platform-sensitive behavior.

### G6 — UX and visual acceptance

Required for visible product changes:

- accepted design-system component or explicit exception;
- before/after evidence;
- target resolutions and scaling levels;
- light/dark mode only if in active scope;
- text overflow/localization;
- high-DPI behavior;
- no broad emergency CSS overrides;
- no clipped controls or hidden commands;
- owner visual acceptance.

Prototype appearance is not a golden reference.

### G7 — Performance

Performance budgets are set during the platform/editor spikes. Required representative fixtures must include:

- baseline small scheme;
- demo scheme;
- large stress scheme;
- large symbol library/search index.

Measure at minimum:

- cold and warm startup;
- project open/save;
- pan/zoom frame behavior;
- selection/move latency;
- validation latency;
- memory consumption;
- export time.

A regression beyond accepted tolerance blocks merge or requires explicit owner waiver with a follow-up work item.

### G8 — Export and print

Required for output changes:

- A4/A3 physical dimensions;
- orientation;
- margins/frame/title block;
- line widths;
- text sizes and font fallback;
- color and black/white profiles;
- no editor overlays;
- SVG validity;
- PDF page count and dimensions;
- Windows/Linux visual comparison;
- print preview evidence.

### G9 — Desktop platform

Required for shell/platform changes:

Windows:

- clean-machine or clean-runner package install/start;
- open/save native dialog;
- clipboard and drag/drop;
- Unicode paths;
- printing/export;
- uninstall/update behavior when in scope.

Linux:

- declared supported distribution/package test;
- start and file dialogs;
- clipboard and drag/drop;
- Unicode paths and case sensitivity;
- printing/export;
- package install/remove when in scope.

Cross-platform:

- the same project file opens and round-trips without semantic diff;
- same symbol/library versions;
- equivalent export within approved tolerance.

### G10 — Packaging and release

Required for Demo/Pilot/Release:

- reproducible build workflow;
- versioned artifacts;
- checksums/signature or equivalent verification;
- dependency/license manifest;
- release notes;
- known limitations;
- upgrade and rollback test;
- project migration backup;
- artifact retention.

## 4. Prototype migration gate

Any reused prototype asset must include:

- exact source SHA/path;
- disposition from `PROTOTYPE_QUARANTINE.md`;
- named target owner;
- known defect list;
- new tests against target contracts;
- proof that prototype CSS/state ownership is not inherited accidentally;
- owner acceptance when visible behavior is involved.

Without this record, the default action is reimplementation or non-use.

## 5. ГОСТ/СТО gate

Any normative claim requires:

- source document and edition/date;
- applicability statement;
- encoded behavior/rule;
- rule ID and severity;
- automated or visual evidence;
- declaration of non-automated expert checks;
- wording limited to the proven compliance boundary.

## 6. MVP gate

MVP candidate must pass the complete scenario in `docs/project/MVP_AND_DEMO.md` on exact head for both Windows and Linux.

Blocking categories:

- data loss;
- broken topology;
- non-deterministic save/load;
- missing undo for primary edits;
- inability to print/export the demo scheme;
- platform-specific project incompatibility;
- unresolved critical/high diagnostics in the acceptance fixture;
- unreviewed prototype code controlling canonical data.

## 7. Demo/Pilot gate

Demo requires D1–D7 evidence.

Pilot additionally requires:

- installable artifacts;
- real project backup;
- migration/rollback procedure;
- known issue register;
- support/diagnostic procedure;
- owner field acceptance.

## 8. Waivers

A gate may be waived only by an explicit owner decision recorded in the issue/PR with:

- exact failed/omitted check;
- reason;
- risk;
- bounded scope;
- follow-up issue;
- expiry/release boundary.

A waiver cannot permit known data loss, unsafe overwrite or silent topology corruption.

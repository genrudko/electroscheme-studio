# Agent Instructions — ElectroScheme Studio

## 1. Product identity

ElectroScheme Studio is a standalone, desktop-first, local-first engineering application for normal electrical schemes and related electrical diagrams.

It is not currently a module of EOD.

Required target platforms:

- Windows;
- Linux.

The product may retain Vue 3, TypeScript and SVG as the editor/rendering layer, but browser-only deployment is not a product requirement. The desktop shell and native integration layer must be selected through an explicit architecture spike and ADR.

## 2. Canonical source

GitHub repository `genrudko/electroscheme-studio` is the only canonical source for:

- code;
- architecture;
- product plans;
- issue state;
- branches and pull requests;
- test and build evidence;
- release and migration decisions.

A local machine is a development/runtime environment only. Local logs, chat memory, patch markers and unpushed files are not authoritative.

Before work, restore factual state from GitHub:

1. current `main` head;
2. active issue;
3. active branch;
4. Draft PR and exact head;
5. changed-file boundary;
6. CI/check results;
7. canonical documents from `docs/INDEX.md`.

Do not request a handoff, old-chat summary or manually supplied SHA when GitHub can provide the state.

## 3. Work-item workflow

Every implementation or governance change must use one explicit work item:

```text
issue
→ dedicated branch
→ Draft PR
→ implementation and checks
→ owner acceptance
→ explicit merge command
```

Rules:

1. One active work item per development stream.
2. If an issue, branch and Draft PR already exist, use them; do not create replacements.
3. Do not commit directly to `main`.
4. Do not mark a PR Ready for Review without an explicit owner command.
5. Do not merge without an explicit owner command.
6. Keep the PR Draft while repairs, visual checks or acceptance evidence are incomplete.
7. Use coherent, risk-based changes rather than dozens of cosmetic repair commits.
8. Keep issue, PR description and canonical project state synchronized.

## 4. Legacy patch workflow

Historical numbered PowerShell patches under the old workflow are not the delivery mechanism for future product development.

Forbidden as the primary workflow:

```text
create local patch script
→ apply outside GitHub review
→ send transcript
→ stack repair patch over repair patch
```

Allowed uses of scripts:

- reproducible repository tooling;
- build/package automation;
- migration tools;
- developer environment bootstrap;
- one-off diagnostics preserved as reviewed code.

All resulting changes must still be visible in the branch and PR diff.

Do not delete historical patch documentation merely to clean the repository. Classify or archive it through an approved migration work item.

## 5. Prototype baseline

The `main` head `6e1209d800c0cc65da4a922506586d5a100c2a84` is the initial prototype baseline for `PROJECT-REFOUNDATION-001`.

Preserve until migration decisions are accepted:

- SVG canvas and interaction research;
- VSDX/VSSX inspection and conversion tools;
- ShapeSheet-derived metrics and generated catalogs;
- parametric busbar research;
- snapping, rulers, guides and pointer interaction work;
- symbol review data and provenance;
- existing backend/frontend examples.

Do not assume these assets are production-ready. Reuse requires tests, reconciliation and explicit ownership in the target architecture.

## 6. Product boundaries

The product must outperform general diagram editors in electrical-engineering workflows, not imitate every feature of a general CAD system.

Core product direction:

- normal electrical schemes;
- smart equipment objects;
- terminals and connection topology;
- parameterized symbols;
- explicit operating states where relevant;
- electrical properties and metadata;
- ГОСТ/СТО-oriented presentation profiles;
- validation and diagnostics;
- print-quality output;
- open, versioned project format;
- optional future automatic scheme generation from structured equipment/topology data.

Not mandatory for the first product stages:

- DWG compatibility;
- universal mechanical/building CAD;
- cloud collaboration;
- multi-user editing;
- marketplace or plugin ecosystem;
- arbitrary Visio document fidelity;
- universal autorouting;
- complete replacement of every Visio drawing feature.

Do not add a broad feature merely because another editor has it. Require a defined electrical-engineering use case and acceptance scenario.

## 7. Architecture invariants

The following are non-negotiable unless changed by an accepted ADR:

1. One canonical document model is the source of truth.
2. SVG/visual nodes are projections, not authoritative engineering data.
3. Objects, ports, connections and properties use stable IDs.
4. Connections reference ports, not incidental screen coordinates.
5. Document mutations use a command/transaction path compatible with undo/redo.
6. Save/load round trips must preserve engineering meaning.
7. Project format is versioned and migratable.
8. Desktop/platform integration is behind an adapter boundary.
9. Domain/editor core must be testable without launching the full desktop UI.
10. Generated or imported content must preserve source provenance.

Until reconciliation is complete, do not expand parallel state models such as backend `Project`, frontend `EditorDocument` and local `CanvasViewport` collections independently.

## 8. Symbol source authority

When a trusted VSDX/VSSX master exists, ShapeSheet data is an engineering source for:

- dimensions;
- geometry;
- connection points;
- formulas;
- user and property cells;
- state variants;
- text fields;
- rotation/stretch behavior clues.

Do not replace an available engineering master with a hand-drawn placeholder and call it complete.

Import is not automatic acceptance. Every promoted symbol requires evidence for:

- geometry;
- scale and dimensions;
- terminals and directions;
- rotation;
- snapping;
- stretching/parameterization where applicable;
- states;
- properties;
- ГОСТ/СТО profile;
- save/load and export.

## 9. ГОСТ/СТО claims

Never claim full compliance without encoded rules, identified normative sources and acceptance evidence.

Each rule/profile must record:

- source document and edition/date;
- applicable scope;
- exact product behavior;
- validation severity;
- test or visual evidence;
- known exceptions.

Use wording such as `ГОСТ-oriented` or `profile implemented` until the formal compliance boundary is proven.

## 10. Quality gates

Changes must run the applicable gates from `docs/quality/ACCEPTANCE_GATES.md`.

At minimum, product code must not be accepted without:

- backend/tool tests where relevant;
- frontend build and typecheck;
- schema and round-trip checks;
- invariant tests for document/topology changes;
- browser/desktop interaction evidence for UI changes;
- Windows and Linux CI coverage when platform behavior is affected.

A placeholder CI job that only checks file existence is not sufficient.

Visual acceptance is required for editor UI and print/export changes. Compilation alone is not acceptance.

## 11. Change discipline

Before editing:

1. identify the owner document/module;
2. state the invariant being changed;
3. define acceptance evidence;
4. identify migration/compatibility impact;
5. constrain the changed-file boundary.

Forbidden without explicit scope:

- broad repository reformatting;
- deleting prototype assets;
- replacing the stack;
- selecting a desktop shell by preference alone;
- adding large dependencies;
- changing public project format without migration;
- mixing UI redesign with document-model migration;
- shipping generated VSDX drafts as accepted core symbols;
- hiding failures with broad CSS overrides or exception lists.

## 12. Documentation ownership

Start with `docs/INDEX.md`.

Canonical ownership:

- `README.md` — repository entry point and public current status;
- `AGENTS.md` — contributor/agent operating contract;
- `docs/project/CURRENT_STATE.md` — volatile factual project state;
- `docs/project/PRODUCT_SCOPE.md` — product boundaries and positioning;
- `docs/project/MVP_AND_DEMO.md` — user-visible acceptance scenarios;
- `docs/project/IMPLEMENTATION_PROGRAM.yaml` — phases, dependencies and gates;
- `docs/architecture/SYSTEM_ARCHITECTURE.md` — target component structure;
- `docs/architecture/DOMAIN_INVARIANTS.md` — non-negotiable data/domain rules;
- `docs/quality/ACCEPTANCE_GATES.md` — required verification evidence;
- `docs/decisions/` — accepted architecture decisions.

When an architectural decision changes, update its owner document in the same PR.

## 13. Current work item

During `PROJECT-REFOUNDATION-001`:

- work only in issue #1;
- work only in branch `governance/project-refoundation-001`;
- create/use its Draft PR;
- do not modify product code;
- do not select the final desktop shell;
- do not delete legacy files;
- establish the canonical program and next implementation work item.

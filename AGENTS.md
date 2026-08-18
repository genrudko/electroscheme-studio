# Agent Instructions — Unified Electrical Engineering Platform

## 1. Product identity

Repository `genrudko/electroscheme-studio` is being refounded as the canonical umbrella for one **standalone, desktop-first, local-first, modular electrical-engineering software complex**.

The product unifies three former directions:

- ElectroScheme Studio;
- NPT Engineering Toolkit;
- TBP / switching-forms-generator.

These old projects are reference/migration sources, not three future sources of truth.

The repository name is historical and may be renamed later only by an accepted naming/migration decision.

## 2. Canonical source and precedence

GitHub is the canonical source for code, architecture, plans, issues, branches, PRs, tests and accepted evidence.

Before work restore from GitHub:

1. current `main`;
2. active issue;
3. active branch and Draft PR;
4. exact PR head / compare state;
5. changed files;
6. applicable workflow state;
7. canonical documents from `docs/INDEX.md`.

Do not ask the owner for handoffs/SHA/state that GitHub can provide.

For product/architecture meaning use this precedence:

```text
explicit owner instruction
→ accepted ADR
→ canonical architecture/compliance documents from docs/INDEX.md
→ CURRENT_STATE / ROADMAP
→ research and migration evidence
→ historical prototype documents
```

This file owns development procedure but does not override accepted product/engineering decisions.

## 3. Work-item workflow

Normal implementation/governance flow:

```text
issue
→ dedicated branch
→ Draft PR
→ targeted implementation/checks
→ visual/manual evidence when applicable
→ owner acceptance
→ explicit Ready/Merge command
```

Rules:

1. Reuse an existing issue/branch/Draft PR for the same work item; do not create duplicates.
2. Do not commit directly to `main`.
3. Do not mark Ready for Review without explicit owner command.
4. Do not merge without explicit owner command.
5. Keep changes risk-bounded; avoid repair-on-repair churn.
6. Full/nuclear CI is not the default tax on a small UI change.
7. Visual acceptance for UI changes must happen before expensive unrelated gates where feasible.
8. GitHub state, not chat memory or local patch markers, determines factual status.

## 4. Core architecture invariants

Unless superseded by accepted ADR:

1. `ElectricalProject` / neutral domain model is the engineering source of truth.
2. Diagram geometry is a view/projection and is not electrical topology.
3. CSV/XLSX, VSDX/VSSX, XSDE, XTABL and switching-form documents are imports/exports/views/adapters, not parallel canonical models.
4. Equipment, terminals, connections, signals and rules use stable identifiers.
5. Connections reference semantic terminals/ports, not incidental screen coordinates.
6. Mutations use explicit command/transaction paths compatible with undo/redo and validation.
7. Project storage is versioned and migratable.
8. `UNKNOWN` is first-class. Unknown position/quality/energization must never be silently interpreted as open/off/de-energized.
9. Domain Core contains no NPT implementation identifiers such as `sTag`, `RTID`, `TechData`, `CustElem` or `scd*`.
10. UI Core contains no product-specific business rules that belong to modules/domain services.
11. Domain modules are testable without launching the full UI.
12. Standalone operation must remain possible with EOD integration absent.

## 5. Target modular-monolith boundary

Initial logical ownership:

```text
Core.Domain
Core.UI
Core.Compliance
Core.ProjectStorage

Modules.EquipmentLibrary
Modules.Import
Modules.Schemes
Modules.Npt
Modules.Switching

Adapters.Platform
Adapters.Eod        # optional / feasibility-gated
App
```

Separate assemblies/libraries are allowed and expected; distributed microservices and dynamic plugin marketplace are not early requirements.

Do not introduce a shared abstraction until at least one real cross-module use case proves it.

## 6. Import and auto-layout invariants

Structured equipment/topology import is a first-class product workflow.

Required flow:

```text
source CSV/XLSX
→ mapping profile
→ normalization
→ staging candidate
→ validation/ambiguity resolution
→ reconciliation
→ ElectricalProject update
→ topology validation
→ auto-layout proposal
→ engineer review
```

Rules:

- CSV/XLSX is not native project storage.
- Never silently guess an ambiguous terminal or connection.
- Imported entities keep source/provenance identifiers.
- Re-import must show a diff/reconciliation plan before destructive change.
- Manual layout corrections are stored as layout constraints and must not be erased by routine re-import/auto-layout.
- Electrical correctness and layout confidence are separate diagnostics.

## 7. NPT compatibility boundary

NPT/Modus material is valuable industrial evidence and compatibility input, not the architecture of the new platform.

Preserve proven findings and lossless handling, including unknown fields/elements/order where applicable.

Never assume without evidence:

- that NPT `nodes` are a complete electrical topology graph;
- that every `scd*` value is KKS;
- that reconstruction from a simplified XML model is lossless;
- that an experimentally generated XSDE object is native-Modus-safe until native acceptance is proven.

NPT-specific IDs and storage rules belong in `Modules.Npt` / adapters.

Full NPT corpus and vendor binaries must not be committed to the public repository. Keep proprietary/reference material outside Git; repository tests use synthetic/cleared fixtures, while private VPS corpus tests may exercise the full reference set.

## 8. Normative/compliance discipline

The product must support traceable compliance profiles rather than hard-coded folklore.

Every encoded normative rule must carry at least:

- stable rule ID;
- source document and issuer;
- edition/amendment/effective dates;
- applicability/scope;
- normative level/authority;
- machine-checkable predicate/action where possible;
- severity;
- explanation;
- source/provenance reference;
- test/evidence status.

Never claim full compliance to a whole ГОСТ, ПУЭ, ПОТЭЭ, ПТЭЭС, ПТЭЭП/ПТЭЭПЭЭ or switching-rule set unless the claimed scope is explicitly encoded, traced and accepted.

PУЭ must not be treated as one monolithic modern version; track applicable chapters/sources/revisions.

## 9. Non-weakening local policy rule

Configuration layers may reflect manufacturer, enterprise, site and project specifics, but a lower/local layer must not weaken an applicable mandatory baseline.

Conceptual hierarchy:

```text
Mandatory regulatory baseline
→ applicable standards/profile baseline
→ manufacturer/equipment constraints
→ enterprise policy
→ site/object policy
→ project policy
```

A lower layer may add requirements or choose a stricter alternative. An attempted weakening of a locked mandatory requirement is a configuration error, not an override.

Conflict diagnostics must explain which sources/rules conflict and which rule wins.

## 10. Graphics and ГОСТ/ЕСКД

Electrical-scheme graphics are semantic assets governed by versioned graphic-standard profiles.

Do not promote a symbol because it merely looks familiar.

A promoted native symbol/profile requires, where applicable:

- equipment/domain type mapping;
- terminal semantics;
- state variants;
- normative source/profile;
- geometry/dimension evidence;
- orientation/rotation/stretch behavior;
- connection points;
- labels/designations;
- print/export evidence;
- validation tests;
- licensing/provenance clarity.

NPT graphical assets may be used as compatibility/reference evidence; do not silently copy proprietary assets into the native symbol library.

## 11. Switching, state and interlocks

Switching/TBP functionality must be driven by explicit domain state and normative rules.

Safety boundaries:

- software simulation is not physical equipment control;
- logical/project interlock is not a substitute for relay/PLC/hardwired interlock;
- TBP generation remains a draft/decision-support workflow with required human review until a separately accepted safety case says otherwise;
- no operation is considered safe merely because the model lacks contradictory data;
- denial/uncertainty must be explainable to the user.

Do not add real SCADA command execution, IEC-104 server, historian, P/Q control or redundancy to this product scope without a new explicit owner decision.

## 12. UI Core and UX quality

UI Core is a first-class architecture area, not cosmetic styling.

Target: modern, dense, professional desktop engineering UX suitable for long sessions, large projects, keyboard+mouse and multi-monitor work.

Required foundation includes:

- application shell/workspace;
- document tabs/splits/detachable windows;
- multi-window and workspace persistence;
- design system and UI Gallery;
- property inspector;
- trees and virtualized tables;
- command/shortcut/context-menu system;
- dialogs/notifications/status;
- shared canvas infrastructure;
- HiDPI/mixed-DPI support;
- accessible focus/keyboard behavior.

Reject MS-DOS/legacy-looking UI as well as sparse/mobile-first desktop composition.

UI changes require visible evidence. Do not hide structural problems behind broad CSS/style overrides.

## 13. Platform stack rule

The final UI/runtime stack is currently PENDING.

Admitted final candidates:

- Avalonia + C#/.NET;
- Qt 6 + C++/QML.

Tauri/WebView work in Draft PR #4 is retained as research evidence but is not the selected product baseline.

Do not select the stack by familiarity or preference. `PLATFORM-STACK-SPIKE` must compare equivalent scenarios and measure canvas, tables, multi-window, HiDPI, headless/visual testing, packaging and development iteration cost.

## 14. Development Platform and CI

Baseline development control plane:

```text
ChatGPT/owner
→ GitHub
→ self-hosted runner on existing VPS
→ targeted build/test/benchmark/package
→ GitHub logs/artifacts
→ owner acceptance
```

No mandatory Business/MCP/new paid service is assumed.

The local PC is an acceptance endpoint, not a required build environment.

Repository tooling should converge on one deterministic launcher (`./dev` or platform-neutral equivalent) with commands for targeted lanes.

Risk-based lanes:

- UI-only: compile + targeted UI/headless/visual evidence + preview;
- domain: core + affected module + serialization/migration;
- NPT: lossless/round-trip/corpus/format invariants;
- topology/switching/compliance: scenario/invariant/property/rule tests;
- full suite: release/nightly or genuinely systemic changes.

Do not make a small UI patch wait for unrelated full-corpus and release gates before the owner can see it.

## 15. Optional EOD integration

EOD integration is feasibility-gated and optional.

Acceptable direction: thin adapter/module registration, launcher/deep links, bounded context handoff, links to project/equipment/scheme/switching documents, optional shared authentication/context if cheap and clean.

Reject integration if it requires:

- EOD-specific entities in Domain Core;
- mandatory runtime dependency on EOD;
- separate product fork;
- duplicate UI shell implementation;
- pervasive conditional branches;
- substantial independent release/deploy burden.

Standalone product tests must pass with EOD adapter absent.

## 16. Historical/prototype preservation

Do not delete old prototype, Visio, market, Tauri or migration evidence merely because the new foundation supersedes its conclusions.

Classify each significant asset as:

- retain as evidence;
- salvage behind new contract/tests;
- reimplement from behavior;
- archive/historical;
- retire only after accepted migration.

## 17. Documentation ownership

Start with `docs/INDEX.md`.

Canonical new-foundation owners include:

- `README.md` — entry point/status;
- `AGENTS.md` — operating contract;
- `docs/project/CURRENT_STATE.md` — volatile factual state;
- `docs/project/UNIFIED_PRODUCT_VISION.md` — product goal/value;
- `docs/architecture/UNIFIED_SYSTEM_ARCHITECTURE.md` — modules/boundaries;
- `docs/architecture/DOMAIN_AND_PROJECT_MODEL.md` — source-of-truth model/invariants;
- `docs/architecture/UI_CORE.md` — shared UI architecture;
- `docs/architecture/IMPORT_AND_AUTO_LAYOUT.md` — structured import/reconciliation/layout;
- `docs/architecture/SWITCHING_AND_INTERLOCKS.md` — state transition and rule boundary;
- `docs/architecture/NPT_COMPATIBILITY_BOUNDARY.md` — NPT isolation/compatibility;
- `docs/architecture/EOD_INTEGRATION_BOUNDARY.md` — optional EOD gate;
- `docs/compliance/NORMATIVE_ARCHITECTURE.md` — compliance engine/registry;
- `docs/compliance/NORMATIVE_REGISTRY.md` — source baseline and lifecycle;
- `docs/compliance/LOCAL_POLICY_OVERLAYS.md` — enterprise/site customization;
- `docs/compliance/SAFETY_BOUNDARIES.md` — safety claims/non-claims;
- `docs/development/DEVELOPMENT_PLATFORM.md` — GitHub/VPS DevEx;
- `docs/development/PLATFORM_STACK_SPIKE.md` — Avalonia-vs-Qt decision contract;
- `docs/development/CI_AND_ACCEPTANCE.md` — risk-based gates.

Update owner documents in the same PR when their decision changes.

## 18. Current work item

For `UNIFIED-FOUNDATION-001`:

- issue #5;
- branch `architecture/unified-foundation-001`;
- Draft PR only;
- documentation/governance/architecture contracts first;
- no bulk product-code migration;
- no final platform-stack selection;
- no Ready/Merge without explicit owner command.

The immediate next sequence after accepted Foundation is:

```text
Infrastructure Spike
→ Avalonia vs Qt Platform Spike
→ UI Core + minimal Domain Core
→ structured import / topology / auto-layout vertical slice
```

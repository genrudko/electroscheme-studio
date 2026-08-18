# Current State — Unified Electrical Engineering Platform

Дата среза: **2026-08-18**  
Активная программа: `UNIFIED-FOUNDATION-001`

## GitHub factual state

- Repository: `genrudko/electroscheme-studio`
- Default branch: `main`
- Active foundation issue: #5 `UNIFIED-FOUNDATION-001`
- Active foundation branch: `architecture/unified-foundation-001`
- Foundation Draft PR: создаётся в рамках этого work item и до owner acceptance остаётся Draft.
- Previous issue #3 `DESKTOP-PLATFORM-AND-CORE-SPIKE-001`: OPEN at foundation start.
- Previous Draft PR #4: OPEN / DRAFT / NOT MERGED at foundation start; Tauri/WebView-first recommendation is superseded as a final architecture decision by the new unified scope, but PR contents remain research evidence.

Exact heads, compare counts and workflow runs are volatile and must be read directly from GitHub before implementation/acceptance actions rather than copied here as permanent facts.

## Product decision now in force

The project is no longer planned as only an independent scheme editor.

The target is one standalone, desktop-first/local-first **modular electrical-engineering complex** unifying:

1. Scheme Studio;
2. NPT Engineering Toolkit / compatibility;
3. Switching/TBP;
4. shared import/topology/state/normative/UI foundations.

`ElectricalProject` / neutral domain model becomes the source of truth. Diagram geometry, CSV/XLSX, NPT files and switching-form documents are bounded views/imports/adapters.

## Foundation status

### Accepted direction

- modular monolith;
- one neutral Domain Core;
- first-class UI Core;
- topology separated from geometry;
- explicit State Core with `UNKNOWN` as a first-class safe state;
- first-class structured CSV/XLSX Import + reconciliation + auto-layout;
- versioned normative/compliance registry;
- ГОСТ/ЕСКД graphic profiles;
- switching rules traced to Russian energy-sector normative sources;
- enterprise/site/equipment/project policy overlays that cannot weaken an applicable mandatory baseline;
- NPT compatibility behind adapter/module boundary;
- optional EOD integration behind a strict feasibility/cost gate;
- GitHub as canonical control plane and existing VPS as development execution plane;
- risk-based CI and visual-first UI acceptance;
- final platform stack to be selected only by Avalonia-vs-Qt executable spike.

### Not yet proven / not yet selected

- Avalonia vs Qt final selection;
- heavy-canvas performance of Avalonia on representative electrical workload;
- exact native project package format;
- exact domain schema version 1;
- complete equipment-type library;
- completeness/correctness of NPT `nodes` as a topology source;
- production-safe creation of arbitrary new XSDE topology objects;
- full normative rule coverage;
- exact EOD integration API/cost;
- installer/update channel;
- product/brand name.

## Important inherited evidence

### ElectroScheme Studio

Useful evidence/assets include:

- object/terminal/connection research;
- SVG/editor interaction experiments;
- VSDX/VSSX/ShapeSheet tooling;
- snapping/busbar/symbol research;
- desktop packaging and Tauri spike evidence;
- market/reference-product research.

These are migration inputs, not automatically accepted production architecture.

### NPT Engineering Toolkit

Current research baseline includes:

- ~475 parseable real XSDE files and large real industrial corpus;
- lossless XSDE round-trip for the studied corpus;
- identified NPT/Modus custom-value semantics and important non-KKS exceptions;
- embedded `CustElem` behavior and external `.menu` library role;
- large ASU/TECH/KKS signal catalog;
- lossless XTABL v6.0 core for seven production tables / 1461 records;
- proven unknown/preserve-only XTABL fields;
- evidence that NPT `nodes` are topology-related, but not proof that they form a complete neutral electrical graph;
- current Mnemo renderer fidelity is still insufficient and must not be disguised by adding unrelated editor features.

Full vendor/reference corpus must remain outside the public Git repository.

### TBP / switching-forms-generator

Useful inherited concepts include:

- draft switching-form generation with mandatory human review;
- YAML/profile-driven site-specific behavior;
- normative-reference structures;
- real operational wording/pattern research.

The new module must re-trace migrated rules to explicit source/version/applicability metadata; old behavior is not accepted merely because it exists in code/YAML.

## Normative baseline state

Foundation establishes the **registry mechanism**, not a false claim that all Russian energy-sector requirements are already encoded.

Initial authoritative-source discovery includes:

- ГОСТ 2.701-2008, ГОСТ 2.702-2011 and relevant ESKD graphical-symbol standards;
- ПОТЭЭ under Ministry of Labour order №903н with amendments;
- PTEEP consumer rules under Ministry of Energy order №811;
- PTEES under Ministry of Energy order №1070 with later amendments;
- Switching Rules under Ministry of Energy order №757 with later amendments;
- applicable PУЭ chapters/sources tracked separately rather than as one synthetic version.

Every production rule still requires source-level extraction, applicability classification, testability decision and owner/domain review.

## Development sequence after Foundation

```text
UNIFIED-FOUNDATION-001
        ↓
INFRASTRUCTURE-SPIKE-001
GitHub ↔ self-hosted VPS runner ↔ artifacts
        ↓
PLATFORM-STACK-SPIKE-001
Avalonia vs Qt
        ↓
UI-CORE-FOUNDATION-001
+
DOMAIN-CORE-FOUNDATION-001
        ↓
IMPORT-TO-SCHEME-VERTICAL-SLICE-001
CSV/XLSX → topology → auto-layout → manual correction → save → reimport
        ↓
module expansion: Scheme / NPT / Switching
```

Foundation itself must not prematurely implement product code or pick a stack.

## Explicitly out of current product scope

Without a new owner decision, do not build:

- replacement SCADA runtime;
- IEC-104 server/client platform as a product objective;
- historian;
- P/Q control;
- redundancy/failover SCADA platform;
- remote real-equipment switching execution;
- microservice platform;
- dynamic plugin marketplace;
- universal CAD replacement.

## Acceptance posture

Foundation is accepted when it makes the next implementation steps unambiguous and protects the project from four known failure modes:

1. three competing domain models;
2. legacy-looking/unusable UI despite correct backend;
3. untraceable normative folklore embedded in code;
4. development pipelines where a tiny visible repair becomes days of unrelated CI work.

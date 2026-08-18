# Unified Scope and Roadmap

Статус: canonical foundation document

## 1. Scope principle

The project grows through proven vertical slices, not through simultaneous implementation of every module.

The common Core exists to eliminate duplication between real modules, not to become an abstract mega-platform before product workflows exist.

## 2. In scope

### Foundation capabilities

- neutral electrical project/domain model;
- equipment/terminal/connection/topology/state concepts;
- versioned project persistence;
- UI Core and professional desktop shell;
- Windows/Linux packaging after measured stack selection;
- compliance/normative registry and policy layering;
- developer tooling and risk-based CI.

### Scheme Studio

- intelligent electrical objects;
- multiple views over one project model;
- electrical connections independent from visual routing;
- domain-aware auto-layout;
- manual layout editing/constraints;
- ГОСТ/ЕСКД-oriented graphic profiles with traceability;
- validation, search and property editing;
- print/export.

### Import

- CSV/XLSX sources;
- configurable mapping profiles;
- normalization;
- staging/preview;
- ambiguity/conflict resolution;
- reconciliation/update;
- topology construction;
- provenance;
- handoff to auto-layout.

### NPT Compatibility

- lossless/preserve-first XSDE handling;
- typed `scd*` editing;
- NPT signal catalog/search/bindings;
- native compatibility validation;
- XTABL editor/generator;
- project-resource resolution;
- topology extraction research where needed by neutral model;
- interoperability rather than reimplementation of SCADA runtime.

### Switching / TBP

- switching operation model;
- sequence model;
- current/simulated state;
- topology recalculation;
- normative validation;
- explainable interlocks;
- generation/checking of switching forms;
- local enterprise/site instructions as constrained overlays;
- mandatory human review unless a future safety case changes the boundary.

### Optional integration

- EOD adapter only if feasibility/cost gate passes.

## 3. Explicitly out of current scope

Unless explicitly reopened:

- complete SCADA runtime replacement;
- online IEC-104 control infrastructure;
- historian;
- wind-farm P/Q control;
- SCADA redundancy;
- automatic real-equipment execution of switching sequences;
- cloud collaboration as core dependency;
- multi-user realtime editing;
- universal CAD/mechanical/building drafting;
- full arbitrary Visio fidelity;
- arbitrary DWG ecosystem;
- plugin marketplace;
- AI/ML auto-layout before deterministic domain-aware layout is proven.

## 4. Roadmap

### F0 — Unified Foundation

Goal: make architecture, normative boundaries, UI/DevEx and migration unambiguous.

Deliverables are the canonical documents indexed in `docs/INDEX.md`.

No bulk product-code migration.

### F1 — Development Infrastructure Spike

Prove:

```text
ChatGPT/owner
→ GitHub
→ self-hosted runner on existing VPS
→ targeted build/test
→ artifact/log
→ GitHub
→ review
```

Acceptance:

- one-time runner setup documented;
- unprivileged runner account;
- repository checkout/build job;
- result/log visible through GitHub;
- artifact produced;
- path to private NPT corpus configured outside Git;
- no dependency on new paid control service.

### F2 — Platform Stack Spike

Equivalent Avalonia and Qt implementations must exercise realistic shared UI/core scenarios.

Decision output: accepted ADR selecting one stack.

### F3 — UI Core + Minimal Domain Core

UI:

- app shell;
- workspace/documents;
- multi-window;
- design system/UI Gallery;
- properties;
- tree/table controls;
- command system;
- basic shared canvas.

Domain:

- project;
- equipment;
- terminal;
- connection;
- topology graph;
- state;
- validation;
- persistence/versioning.

### F4 — Import-to-Scheme Vertical Slice

First product proof:

```text
representative CSV/XLSX
→ map fields
→ staging
→ resolve ambiguities
→ build equipment/connections
→ topology validation
→ auto-layout
→ manual correction
→ save
→ changed source re-import
→ reconciliation without destroying manual layout
```

This slice is deliberately small but must use real electrical semantics, not circles-and-lines demo data.

### F5 — Scheme Studio MVP foundation

Expand:

- equipment library;
- controlled symbols;
- scheme hierarchy/views;
- connectors/routing;
- alignment/grid/layout tools;
- searches/diagnostics;
- ГОСТ profile validation;
- high-quality output.

### F6 — NPT Compatibility Module

Integrate proven lossless cores and signal catalog under the new model.

Priority:

1. renderer fidelity for known mnemonic screenshots;
2. safe existing-object editing;
3. typed NPT properties;
4. XTABL data-driven generator/editor;
5. topology extraction experiment;
6. only then broader creation/editing where native compatibility is proven.

### F7 — Switching/TBP Module

Use shared topology/state/compliance model.

Start from validated operations/sequences and existing draft-generation experience; migrate rules only with provenance.

### F8 — Interlocks and advanced operational simulation

Add explainable logical/project interlocks and richer simulation after topology/state quality is proven.

### F9 — EOD feasibility / optional adapter

This can run earlier as a small architecture spike if useful, but production integration happens only after standalone APIs are stable.

## 5. Dependency order

```text
Foundation
   ↓
Development Infrastructure
   ↓
Platform Stack Decision
   ↓
UI Core ─────────────┐
Domain Core ─────────┼→ Import-to-Scheme vertical slice
Compliance Core ─────┘
                         ↓
                Scheme / NPT / Switching
```

NPT and TBP research may continue in parallel, but must not force their vendor/local storage concepts into Core.

## 6. Product acceptance priorities

When trade-offs occur, prioritize:

1. engineering correctness and safety boundary;
2. traceable/preservable data;
3. practical user workflow and visible usability;
4. development iteration cost;
5. broad feature count.

A technically sophisticated subsystem that the user cannot reasonably operate or iterate on is not considered complete.

## 7. Stop conditions against overengineering

Do not create:

- generalized plugin API before two concrete modules require it;
- generalized rule language before real rules show repeated patterns;
- generalized layout ontology before representative schemes prove the need;
- distributed services where in-process module calls suffice;
- universal symbol DSL before native symbol profiles establish real requirements.

Build the minimal reusable contract that current cross-module evidence justifies.

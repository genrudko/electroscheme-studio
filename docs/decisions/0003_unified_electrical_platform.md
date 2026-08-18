# ADR 0003 — Unified Electrical Engineering Platform

Status: **ACCEPTED by owner direction / recorded in UNIFIED-FOUNDATION-001**  
Date: 2026-08-18

## Context

ElectroScheme Studio, NPT Engineering Toolkit and TBP/switching-form work independently converged on the same electrical concepts: equipment identity, terminals, connections, topology, state and engineering/operational rules.

Keeping three independent architectures would duplicate project models, equipment libraries, topology logic, state handling, UI infrastructure and normative configuration.

## Decision

Build one standalone modular electrical-engineering product with shared Domain Core, UI Core and Compliance Core.

Former projects become modules/migration sources:

- Scheme Studio;
- NPT Compatibility;
- Switching/TBP.

CSV/XLSX Import and Equipment Library become first-class shared modules.

Architectural style: modular monolith unless a later ADR proves a distributed boundary is necessary.

## Consequences

Positive:

- one project/equipment identity;
- topology/state reuse across scheme, NPT and switching;
- one UI/design foundation;
- one normative policy model;
- import once, reuse across modules;
- less maintenance duplication.

Costs/risks:

- Foundation and migration work before feature expansion;
- common Core must avoid becoming an over-general mega-framework;
- old code cannot be merged mechanically;
- platform stack needs reevaluation under heavier unified scope.

## Rejected alternatives

### Keep three products permanently independent

Rejected because shared domain semantics would diverge and user would repeatedly maintain the same object data.

### Merge all old code immediately

Rejected because it would combine incompatible state models, UI stacks and research prototypes without a new ownership model.

### Build microservices around each former product

Rejected for early product due unnecessary operational complexity and weak value for local-first desktop workflows.

## Follow-up

- neutral Domain Core ADR;
- layered compliance ADR;
- Platform Stack Spike;
- migration plan;
- first Import-to-Scheme vertical slice.

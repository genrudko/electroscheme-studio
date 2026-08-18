# ADR 0004 — Neutral Domain Model as Source of Truth

Status: **ACCEPTED by owner direction / recorded in UNIFIED-FOUNDATION-001**  
Date: 2026-08-18

## Context

The product must support native schemes, structured CSV/XLSX import, NPT XSDE/XTABL compatibility, Visio interoperability and switching/TBP without creating competing authoritative models.

A drawing-first or vendor-file-first architecture would make topology/state/rules dependent on screen geometry or proprietary serialization.

## Decision

`ElectricalProject` and its neutral electrical domain model are the engineering source of truth.

Core semantic ownership includes:

- stable equipment identity;
- equipment type/properties;
- terminals;
- connections;
- topology;
- state/quality semantics;
- signal bindings at neutral boundary;
- project/view references;
- compliance profile references.

Views and external formats are projections/adapters.

NPT-specific identifiers/serialization and EOD-specific identifiers must not become required Core fields.

Topology is distinct from diagram geometry.

`UNKNOWN` is a first-class state and is never silently collapsed into a safe/negative state.

## Consequences

- CSV/XLSX import uses staging/reconciliation before Domain mutation;
- Scheme module stores layout/views separately from electrical connections;
- NPT module translates/preserves vendor data behind adapter boundary;
- Switching module consumes shared topology/state rather than recreating project data;
- project persistence must be versioned/migratable and framework-neutral.

## Rejected alternatives

### Diagram canvas as source of truth

Rejected because moving/drawing geometry must not implicitly redefine electrical topology.

### XSDE/NPT as source of truth

Rejected because it would vendor-lock all modules and pollute native product semantics.

### Excel/CSV as native project format

Rejected because spreadsheets are import inputs, cannot robustly own full topology/state/view/versioning semantics and make safe reconciliation difficult.

### TBP own equipment database

Rejected because it would duplicate identity/topology and diverge from schemes.

## Follow-up

Implement minimal Domain Core only after platform selection, with round-trip/migration and topology/state invariant tests.

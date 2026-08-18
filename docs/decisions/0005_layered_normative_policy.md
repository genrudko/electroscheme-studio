# ADR 0005 — Layered Normative Policy and Non-Weakening

Status: **ACCEPTED by owner direction / recorded in UNIFIED-FOUNDATION-001**  
Date: 2026-08-18

## Context

Russian energy-sector operational requirements come from multiple legal/normative sources. Real sites also have manufacturer manuals, enterprise standards and local instructions that can add or tighten requirements.

A simple settings file with `override=true` would be unsafe: local configuration could accidentally weaken an applicable mandatory baseline.

## Decision

Implement a versioned Compliance Core with explicit source provenance, applicability and layered policy resolution.

Conceptual layers:

```text
mandatory regulatory baseline
→ applicable standard/profile baseline
→ manufacturer/equipment constraints
→ enterprise policy
→ site/object policy
→ project policy
```

Lower/local layers may add or tighten requirements but may not disable/relax an applicable locked mandatory rule.

Attempted weakening is a policy conflict/error.

Every production rule must identify its source/version/scope and machine/review behavior.

## Consequences

- normative documents are registered with editions/amendments/effective dates;
- projects can snapshot a normative baseline date/profile;
- local policy packages are versioned and separately deployable;
- rule diagnostics identify source and conflict;
- generated switching forms retain mandatory human-review boundary until separately changed;
- graphics profiles distinguish ГОСТ/ЕСКД requirements from enterprise conventions and layout heuristics.

## Rejected alternatives

### Hard-code rules throughout modules

Rejected due poor provenance, updateability and conflict handling.

### Last-file-wins configuration

Rejected because authority/restrictiveness cannot be represented safely by load order.

### Treat all local instructions as equal to law/mandatory rules

Rejected because source authority and applicability differ and must be visible.

### Encode every rule immediately

Rejected because coverage must grow from verified sources and real workflows; fake completeness is worse than scoped coverage.

## Follow-up

- source registry;
- local policy schema/editor;
- source-version rule tests;
- switching rule extraction beginning with current Rule 757 baseline and applicable supporting acts;
- graphics coverage matrix beginning with verified ГОСТ 2.701/2.702 plus exact UGO standards per equipment family.

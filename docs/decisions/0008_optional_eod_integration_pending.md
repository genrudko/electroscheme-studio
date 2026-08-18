# ADR 0008 — Optional EOD Integration

Status: **PENDING FEASIBILITY / COST GATE**  
Date opened: 2026-08-18

## Context

The electrical product could provide value as an optional capability alongside Electronic Operational Documentation (EOD), especially through shared object/workplace context and references to schemes/switching forms.

However, integration is not valuable if it forces EOD-specific architecture into the standalone electrical product or substantially increases development/release burden.

## Current decision

Standalone operation is mandatory.

EOD integration is allowed only behind `Adapters.Eod` / a similarly isolated optional boundary.

Preferred exploration order:

1. launcher/deep-link bridge;
2. bounded module registration/context handoff;
3. only then consider stronger embedding if a real need justifies it.

## Feasibility gate

See `docs/architecture/EOD_INTEGRATION_BOUNDARY.md`.

Reject/defer if integration requires:

- EOD-specific mandatory Core fields;
- mandatory EOD runtime/network dependency;
- forked UI/product code;
- pervasive mode conditionals;
- duplicate authoritative databases;
- significant independent release/deploy burden.

## Required output

A future bounded spike must classify the result as:

```text
ACCEPT_LEVEL_1
ACCEPT_LEVEL_2
DEFER
REJECT_TOO_EXPENSIVE
```

No production integration is committed by Foundation.

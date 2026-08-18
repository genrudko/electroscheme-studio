# ADR 0008 — Optional EOD Integration

Status: **PENDING FEASIBILITY / COST GATE**  
Date opened: 2026-08-18

## Context

The electrical product could provide value as an optional capability alongside Electronic Operational Documentation (EOD), especially through shared object/workplace context and references to schemes/switching forms.

However, integration is not valuable if it forces EOD-specific architecture into the standalone electrical product or substantially increases development/release burden.

Foundation inspection of the actual EOD repository materially improved the feasibility outlook:

- `MODULE-ACTIVATION-CONTRACT-001` is accepted/merged;
- `MODULE-REGISTRY-001` is completed/merged;
- EOD already has stable first-party module manifests, scoped activation for `ORGANIZATION / ENERGY_SITE / WORKPLACE`, lifecycle/audit semantics and explicit optional-integration behavior.

Therefore integration does not need a second EOD activation/control-plane design.

## Current decision

Standalone operation is mandatory.

EOD integration is allowed only behind `Adapters.Eod` / a similarly isolated optional boundary.

The **preferred feasibility target is now Level 2** using a small EOD-side bridge module that conforms to the existing EOD registry and launches/deep-links into the standalone desktop application.

Conceptually:

```text
EOD module registry
      ↓
ELECTRICAL-BRIDGE first-party module
      ↓ typed launch/context contract
Standalone Electrical Desktop Application
```

This preference is not yet production acceptance. Exact context-security, mapping and packaging cost still require an executable spike.

Exploration order:

1. launcher/deep-link contract;
2. EOD bridge registration through the existing module registry and scoped activation;
3. bounded context handoff/cross-links;
4. only then consider stronger embedding if a real need justifies it.

## Feasibility gate

See `docs/architecture/EOD_INTEGRATION_BOUNDARY.md`.

Reject/defer if integration requires:

- EOD-specific mandatory Core fields;
- mandatory EOD runtime/network dependency;
- forked UI/product code;
- pervasive mode conditionals;
- duplicate authoritative databases;
- significant independent release/deploy burden;
- a second competing module-activation mechanism instead of the existing EOD registry.

Important security boundary:

> EOD module activation authorizes the EOD bridge capability; it does not automatically authorize arbitrary mutations in the standalone electrical application.

Desktop-side authorization/context trust remains an explicit separate contract.

## Required output

A future bounded spike must classify the result as:

```text
ACCEPT_LEVEL_1
ACCEPT_LEVEL_2
DEFER
REJECT_TOO_EXPENSIVE
```

No production integration is committed by Foundation, but current evidence makes `ACCEPT_LEVEL_2` a realistic target rather than a speculative architecture idea.

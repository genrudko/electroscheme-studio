# Optional EOD Integration Boundary

Статус: canonical foundation document  
Decision state: **FEASIBILITY-GATED / NOT COMMITTED**

## 1. Objective

Explore whether the unified electrical-engineering complex can be exposed as an optional module/capability inside Electronic Operational Documentation (EOD) **without compromising standalone architecture or materially increasing development/release cost**.

Integration is desirable only if cheap, bounded and operationally useful.

## 2. Factual EOD baseline verified during Foundation

The EOD repository already contains an accepted and implemented optional-module control plane; this is important because the electrical product does **not** need to invent an EOD activation system from scratch.

Verified GitHub evidence at 2026-08-18:

- EOD issue #61 `MODULE-ACTIVATION-CONTRACT-001` was completed through merged PR #62;
- the accepted contract defines one modular Django monolith, stable module manifests, lifecycle states, required dependencies vs optional integrations, scoped activation and history preservation;
- EOD issue #67 `MODULE-REGISTRY-001` is CLOSED/COMPLETED;
- PR #68 is merged and implements the registry/control plane;
- v1 activation scopes are `ORGANIZATION`, `ENERGY_SITE`, `WORKPLACE`;
- the registry has stable module IDs/capabilities, scoped activation, lifecycle/audit semantics and a central module-access decision boundary;
- optional integration is an explicit supported concept and does not need to become a hard dependency.

### Architectural implication

This materially improves the feasibility estimate for a **Level 2** integration.

The preferred design is not to turn the desktop electrical product into a Django/EOD component. Instead, EOD can host a **small first-party bridge module** conforming to its existing manifest/activation contract:

```text
EOD
└── ELECTRICAL-BRIDGE module
    ├── EOD manifest/capabilities
    ├── ORGANIZATION/SITE/WORKPLACE activation
    ├── navigation/deep-link UI
    ├── context mapping
    └── optional references to released artifacts
             │
             ▼
Standalone Electrical Desktop Application
```

The EOD registry controls whether the **bridge capability** is available in a given EOD scope. It does not automatically authorize mutations inside the desktop application; that remains a separate explicit security/context contract.

This architecture reuses EOD's already accepted modularity instead of coupling the two products internally.

## 3. Non-negotiable principle

```text
Standalone Electrical Product
          │
          └── optional EOD Adapter / EOD Bridge Module
```

Never:

```text
EOD runtime
   ↓ required dependency
Electrical Product Core
```

Domain Core, project storage, Scheme, Import and Switching must work when EOD is absent.

## 4. Potential useful integration scenarios

Low-coupling scenarios worth evaluating:

- EOD module registry/launcher opens the standalone complex;
- deep link from EOD object/workplace to electrical project/view/equipment;
- deep link from electrical product back to related EOD document/journal/instruction;
- bounded context handoff: organization/site/workplace/user/project/equipment IDs as actually supported by both products;
- attach/reference released scheme or switching form in EOD workflow;
- optional shared authentication/session identity if a future explicit contract makes it cheap and secure;
- module availability/activation controlled by the existing EOD registry without EOD owning electrical project data.

These scenarios should prefer links/contracts over embedding the entire desktop UI runtime.

## 5. Integration levels

### Level 0 — none

Products operate independently. This mode is always supported and is the architectural baseline.

### Level 1 — launcher/deep-link bridge

EOD can launch/focus the standalone application with typed context.

Conceptual URI examples:

```text
electrical://project/{id}/view/{id}
electrical://project/{id}/equipment/{id}
electrical://project/{id}/switching/{sequenceId}
```

Exact URI/security contract is PENDING.

### Level 2 — bounded EOD bridge module + context integration

EOD exposes a first-party bridge module through its existing module registry and passes bounded context to the standalone application. Runtime and electrical project storage remain independent.

Because EOD already has accepted scoped module activation and optional-integration semantics, this level is now the **preferred feasibility target**, subject to an executable spike.

### Level 3 — embedded native UI/runtime integration

High cost/risk. Not accepted by default and requires a separate architecture proof plus owner approval.

The existence of an EOD module registry does not justify embedding a desktop Qt/Avalonia UI into Django/web runtime.

## 6. Feasibility gate

EOD integration is accepted only if a small spike demonstrates all of the following:

1. standalone application remains unchanged in its core architecture;
2. EOD bridge/adapter can be removed/disabled cleanly;
3. Domain Core contains zero EOD-specific mandatory fields/types;
4. integration uses a narrow versioned contract;
5. existing EOD module manifest/activation semantics can be reused rather than forked;
6. no separate fork of the electrical UI shell is needed;
7. packaging/release duplication is small and measurable;
8. failure/unavailability of EOD does not prevent local electrical project work;
9. access control/context handoff is explicit and auditable;
10. EOD scope activation is not mistaken for desktop-project authorization;
11. maintenance burden is acceptable for a small project/team.

## 7. Reject/cost triggers

Reject or defer integration if it requires any of the following:

- EOD-specific entities in neutral Domain Core;
- a required network dependency on EOD for normal project opening/editing;
- duplicate UI implementation for embedded vs standalone modes;
- pervasive `if (eodMode)` branches across modules;
- separate long-lived product fork;
- separate electrical project database synchronized bidirectionally with EOD;
- substantial independent installer/release pipeline;
- privileged EOD/server credentials on development runners;
- incompatible desktop/web framework compromise solely to embed the product;
- bypassing the existing EOD module registry with a second competing activation mechanism.

## 8. Data ownership

Default ownership:

| Data | Owner |
|---|---|
| electrical project/equipment/topology/views | electrical product |
| scheme release/export artifact | electrical product; EOD may reference/copy released artifact |
| switching semantic sequence | electrical product |
| EOD journal/document/workflow records | EOD |
| EOD bridge activation/audit | EOD module registry |
| cross-links/context mappings | explicit integration record / bridge contract |

Do not create silent mirrored authoritative copies.

## 9. Identity mapping

Integration may map:

```text
EOD Organization / EnergySite / Workplace
↔ ElectricalProject site/context

EOD related object/document
↔ Electrical equipment/view/sequence/release reference
```

Mapping must be explicit, versioned and repairable. User-visible names are not stable identity keys.

Do not invent an `EOD Workplace -> Electrical Site` relationship when neither product has explicit evidence for it; use configured mapping.

## 10. Authentication and permissions

If shared identity is implemented later:

- adapter receives the minimum required claims/context;
- standalone local mode remains defined;
- authorization decisions for electrical project mutations remain owned by the electrical product unless an accepted integration contract delegates specific decisions;
- EOD `ModuleAccessDecision` controls access to the EOD bridge capability, not every desktop action automatically;
- a deep link is not authorization by itself;
- signed/short-lived launch context should be evaluated rather than trusting arbitrary URI parameters when identity matters.

## 11. UX boundary

Preferred initial UX is seamless-but-separate:

- EOD shows the electrical capability only where its existing scoped module registry allows it;
- open module/link in one action;
- focus existing application instance when practical;
- navigate directly to relevant project/equipment/view;
- return/reference related EOD object;
- avoid requiring the user to manually locate the same context twice.

Do not force an embedded web-like experience if it degrades desktop engineering UX or multi-monitor support.

## 12. Suggested feasibility spike

A later `EOD-INTEGRATION-FEASIBILITY-001` should implement only:

1. inspect/reuse the current EOD module manifest/capability registration API from merged `MODULE-REGISTRY-001`;
2. register one `ELECTRICAL-BRIDGE` test module/capability;
3. activate it for selected Organization/EnergySite/Workplace scopes using existing EOD lifecycle semantics;
4. pass typed `organization/site/workplace/project/equipment` context where mappings exist;
5. open/focus a standalone electrical preview app on the target context;
6. produce a callback/deep link to an EOD record;
7. prove an inactive bridge is hidden/blocked through the existing EOD access seam;
8. measure changed files, runtime dependencies, packaging changes and maintenance burden;
9. demonstrate standalone electrical operation with the EOD adapter removed.

No shared database and no embedded full UI in the first spike.

## 13. Current feasibility assessment

Based on the now-verified EOD registry architecture, integration is **not currently a reason to reject the unified product design**.

The likely low-cost path is:

```text
EOD first-party bridge module
+ existing scoped activation registry
+ versioned deep-link/context protocol
+ standalone desktop app
```

This is significantly cheaper than embedding or rewriting the electrical product as an EOD web module.

However, the exact bridge API, launch-context security and deployment/packaging cost are still unproven and remain the purpose of the feasibility spike.

## 14. Decision outcome

After the spike, classify integration as one of:

```text
ACCEPT_LEVEL_1
ACCEPT_LEVEL_2
DEFER
REJECT_TOO_EXPENSIVE
```

`REJECT_TOO_EXPENSIVE` remains a valid successful engineering result: EOD integration is explicitly optional and must not distort the main product.

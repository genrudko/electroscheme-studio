# Optional EOD Integration Boundary

Статус: canonical foundation document  
Decision state: **FEASIBILITY-GATED / NOT COMMITTED**

## 1. Objective

Explore whether the unified electrical-engineering complex can be exposed as an optional module/capability inside Electronic Operational Documentation (EOD) **without compromising standalone architecture or materially increasing development/release cost**.

Integration is desirable only if cheap, bounded and operationally useful.

## 2. Non-negotiable principle

```text
Standalone Electrical Product
          │
          └── optional EOD Adapter
```

Never:

```text
EOD runtime
   ↓ required dependency
Electrical Product Core
```

Domain Core, project storage, Scheme, Import and Switching must work when EOD is absent.

## 3. Potential useful integration scenarios

Low-coupling scenarios worth evaluating:

- EOD module registry/launcher opens the standalone complex;
- deep link from EOD object/workplace to electrical project/view/equipment;
- deep link from electrical product back to related EOD document/journal/instruction;
- bounded context handoff: site/workplace/user/project ID;
- attach/reference released scheme or switching form in EOD workflow;
- optional shared authentication/session identity if an existing EOD contract makes it cheap;
- module availability/activation controlled from EOD without EOD owning electrical project data.

These scenarios should prefer links/contracts over embedding the entire desktop UI runtime.

## 4. Integration levels

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

### Level 2 — bounded module registration/context integration

EOD exposes the product as an activated capability and passes allowed workplace/site/user context. Runtime and storage remain independent.

### Level 3 — embedded native UI/runtime integration

High cost/risk. Not accepted by default and requires a separate architecture proof plus owner approval.

## 5. Feasibility gate

EOD integration is accepted only if a small spike demonstrates all of the following:

1. standalone application remains unchanged in its core architecture;
2. adapter can be removed/disabled cleanly;
3. Domain Core contains zero EOD-specific mandatory fields/types;
4. integration uses a narrow versioned contract;
5. no separate fork of the UI shell is needed;
6. packaging/release duplication is small and measurable;
7. failure/unavailability of EOD does not prevent local project work;
8. access control/context handoff is explicit and auditable;
9. maintenance burden is acceptable for a small project/team.

## 6. Reject/cost triggers

Reject or defer integration if it requires any of the following:

- EOD-specific entities in neutral Domain Core;
- a required network dependency on EOD for normal project opening/editing;
- duplicate UI implementation for embedded vs standalone modes;
- pervasive `if (eodMode)` branches across modules;
- separate long-lived product fork;
- separate project database synchronized bidirectionally with EOD;
- substantial independent installer/release pipeline;
- privileged EOD/server credentials on development runners;
- incompatible desktop/web framework compromise solely to embed the product.

## 7. Data ownership

Default ownership:

| Data | Owner |
|---|---|
| electrical project/equipment/topology/views | electrical product |
| scheme release/export artifact | electrical product; EOD may reference/copy released artifact |
| switching semantic sequence | electrical product |
| EOD journal/document/workflow records | EOD |
| cross-links | adapter/explicit integration record |

Do not create silent mirrored authoritative copies.

## 8. Identity mapping

Integration may map:

```text
EOD site/workplace/object ID
↔ ElectricalProject site/equipment/view ID
```

Mapping must be explicit, versioned and repairable. User-visible names are not stable identity keys.

## 9. Authentication and permissions

If shared identity is implemented later:

- adapter receives the minimum required claims/context;
- standalone local mode remains defined;
- authorization decisions for electrical project mutations remain owned by the electrical product unless an accepted integration contract delegates specific decisions;
- a deep link is not authorization by itself.

## 10. UX boundary

Preferred initial UX is seamless-but-separate:

- open module/link in one action;
- focus existing application instance when practical;
- navigate directly to relevant project/equipment/view;
- return/reference related EOD object;
- avoid requiring the user to manually locate the same context twice.

Do not force an embedded web-like experience if it degrades desktop engineering UX or multi-monitor support.

## 11. Suggested feasibility spike

A later `EOD-INTEGRATION-FEASIBILITY-001` should implement only:

1. register one dummy/real module launcher in EOD-compatible way;
2. pass a typed `site/project/equipment` context;
3. open/focus a standalone preview app on the target context;
4. produce a callback/deep link to an EOD record;
5. measure changed files, runtime dependencies, packaging changes and maintenance burden;
6. demonstrate standalone operation with adapter removed.

No shared database and no embedded full UI in the first spike.

## 12. Decision outcome

After the spike, classify integration as one of:

```text
ACCEPT_LEVEL_1
ACCEPT_LEVEL_2
DEFER
REJECT_TOO_EXPENSIVE
```

`REJECT_TOO_EXPENSIVE` is a valid successful engineering result: EOD integration is explicitly optional and must not distort the main product.

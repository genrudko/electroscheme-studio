# Switching and Interlock Architecture

Статус: canonical foundation document

## 1. Purpose

Switching/TBP module uses the shared electrical model to prepare, simulate and validate switching sequences and to generate/check switching-form documents.

It is not a real-equipment control system.

## 2. Core flow

```text
ElectricalProject
+ current/baseline state
+ applicable normative/local policies
        ↓
SwitchingOperation proposal
        ↓
Rule / interlock evaluation
        ↓
ALLOW / BLOCK / UNKNOWN / REQUIRES_CONFIRMATION
        ↓
if simulated apply:
StateTransition
        ↓
Topology recalculation
        ↓
next simulated state
        ↓
SwitchingSequence
```

## 3. SwitchingOperation

Operation is semantic, not merely a text line.

Conceptual fields:

- stable operation ID;
- operation type;
- target equipment/terminal/network object;
- intended state/action;
- prerequisites/authorization references where modeled;
- source (manual/generated/template);
- rule evaluation result;
- generated wording/document fragment;
- sequence position;
- simulation before/after snapshots or references.

Example operation types may include, only as product evidence justifies:

- open/close switching device;
- operate earthing switch;
- check/confirm position;
- apply/remove portable grounding where represented;
- operations with protection/automation devices;
- organizational/check steps required by applicable rules.

Do not freeze an exhaustive operation taxonomy during Foundation.

## 4. Sequence model

SwitchingSequence is an ordered set of semantic operations with metadata and validation state.

It must support:

- manual authoring;
- template-based generation;
- future assisted generation;
- insert/remove/reorder with revalidation;
- per-step simulation;
- whole-sequence validation;
- document rendering/export;
- provenance of generated steps/rules;
- explicit unresolved conditions.

Reordering one step can invalidate downstream assumptions; sequence validation must account for state after each preceding step.

## 5. State transition

Each simulatable operation defines a proposed state change.

Before applying in simulation:

1. verify target identity/type;
2. evaluate applicable hard/mandatory rules;
3. evaluate local/manufacturer constraints;
4. determine whether required state/quality evidence is known;
5. calculate transition;
6. recalculate affected topology;
7. store explanation/evidence.

Simulation state is never silently written back as observed real-world state.

## 6. Interlock engine

Interlock engine evaluates predicates over:

- equipment type/state;
- terminal/connectivity topology;
- energization knowledge;
- dependent devices;
- configured site/project relationships;
- rule/profile data.

A rule may be generic or project-specific.

Example semantic shape (illustrative, not a normative rule):

```text
operation: CLOSE_EARTHING_SWITCH(target)
requires:
  target_section energization == DEENERGIZED_PROVEN
  AND no known closed energized path
  AND conflicting devices satisfy required states
```

The engine must not encode `UNKNOWN` as success.

## 7. Explainability

Every block/warning/unknown result should produce a user-facing explanation containing as applicable:

- operation;
- equipment/section;
- violated/unsatisfied rule ID;
- normative/local source;
- current facts/states used;
- unknown/missing facts;
- topology path/dependency that caused result;
- what confirmation/action is required.

Good result:

```text
BLOCKED: ЗН-35-17 cannot be closed.
Rule: ...
Reason: section remains connected to energized bus through QS-35-17.
Evidence path: Bus35-A → ... → QS-35-17 → Section-17.
```

Avoid opaque `Operation not allowed` messages.

## 8. Normative rules vs physical interlocks

Three distinct layers must stay explicit:

1. **normative/logical operational rules** implemented by software;
2. **site/project operational interlocks/instructions** configured in project/profile;
3. **physical/hardwired/protection/controller interlocks** existing in real equipment.

The software model can represent knowledge about layer 3 but does not claim to replace or verify physical implementation unless a separate engineering/commissioning workflow explicitly does so.

## 9. Human review boundary

Inherited TBP principle remains the safe baseline:

> generated forms/sequences are drafts/decision support requiring qualified human review before operational use.

A future change to this boundary requires separate safety, legal/normative and product acceptance work. It cannot be relaxed by ordinary configuration.

## 10. Normative integration

Switching module does not hard-code document names in conditionals as its primary rule architecture.

It consumes resolved rules from Compliance Core with:

- source/version/effective dates;
- applicability;
- authority/severity;
- non-weakening/local overlays;
- test/evidence status.

Applicable sources include, but are not limited to, the registered Russian energy-sector documents in `docs/compliance/NORMATIVE_REGISTRY.md`.

## 11. Local instructions and enterprise policy

Site-specific switching instructions are expected and first-class.

They may define:

- additional checks;
- stricter sequences;
- equipment-specific restrictions;
- local dispatch/operational naming;
- mandatory intermediate steps;
- approved template wording;
- special conditions for normal/repair schemes.

They cannot suppress an applicable locked mandatory requirement. Conflict is an error requiring rule/profile review.

## 12. Operational names vs identity

Display/dispatch names used in switching documents are attributes/views over stable equipment identity.

This supports:

- local naming schemes;
- legacy aliases;
- import/NPT IDs;
- renamed equipment without breaking historical sequence identity.

Document output must use the naming profile applicable to the target organization/site.

## 13. Topology dependency

Switching safety logic can only be as reliable as topology/state data.

The module must report degraded confidence when:

- topology is incomplete;
- imported connections are unresolved;
- equipment state is UNKNOWN;
- signal quality is bad/uncertain;
- required local policy data is missing.

No automatic rule converts missing evidence into a pass.

## 14. Scheme integration

A strong target UX is integrated visual sequence authoring:

```text
select equipment on operational scheme
→ choose semantic operation
→ validate
→ append to sequence
→ simulate
→ update visual state/topology
→ continue
```

Textual form and visual simulation remain synchronized through operation IDs/domain entities, not text parsing.

## 15. Document generation

Switching-form document is an output/projection of semantic sequence plus organization/profile requirements.

Formatting/templates can vary by enterprise/site without changing semantic operation identity.

The document generator must identify unresolved/blocking validations and never silently render a blocked sequence as approved/ready.

## 16. Testing strategy

Switching logic requires stronger gates than normal UI:

- unit tests for predicates/rule resolution;
- scenario tests on known schemes/states;
- invariant/property tests where useful;
- regression fixtures from accepted operational examples;
- normative rule tests bound to rule IDs/source versions;
- negative tests for UNKNOWN/incomplete topology;
- sequence revalidation after reorder/change.

## 17. Prohibited early features

Do not add without explicit new scope:

- direct equipment command transmission;
- bypass of human review;
- automatic approval/signature;
- assertion that simulation guarantees real physical safety;
- local policy switch that disables mandatory rules;
- black-box AI-generated sequence accepted without deterministic validation/provenance.

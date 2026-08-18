# Safety Boundaries

Статус: canonical foundation document

## 1. Why this document exists

The product will reason about electrical topology, equipment state and switching operations. That can create dangerous overconfidence if software capability is described more strongly than the evidence supports.

This document defines non-negotiable claim boundaries.

## 2. Product role

Current product role:

```text
engineering model
+ scheme/document authoring
+ compatibility tooling
+ deterministic validation
+ switching simulation / decision support
+ draft switching-form generation/checking
```

Current product role does **not** include autonomous real-equipment control.

## 3. UNKNOWN is first-class

Invariant:

> Lack of evidence that equipment/section is energized is not proof that it is de-energized.

Examples:

- unknown breaker position ≠ OPEN;
- missing signal ≠ OFF;
- bad signal quality ≠ safe state;
- missing topology edge ≠ open circuit;
- no modeled voltage source path under incomplete model ≠ absence of voltage.

Safety-sensitive rules must propagate uncertainty.

## 4. Energization semantics

Prefer explicit semantic states such as:

```text
ENERGIZED
DEENERGIZED_PROVEN
UNKNOWN
```

instead of a simple boolean `isEnergized` when the evidence model cannot justify it.

The exact proof model is a later domain design decision, but optimistic collapse is prohibited.

## 5. Simulation vs observation

Clearly separate:

```text
OBSERVED/IMPORTED BASELINE STATE
SIMULATED STATE
PLANNED/TARGET STATE
```

A simulated operation must never silently become a claimed real-world state.

UI/output must make simulation context obvious.

## 6. Logical interlock vs physical interlock

The system may implement:

- generic logical/domain interlocks;
- project/site-specific operational restrictions;
- knowledge about manufacturer/device constraints.

It does not thereby verify:

- physical lock condition;
- actual PLC/relay/controller logic;
- hardwired circuits;
- mechanical interlock health;
- actual absence/presence of voltage in the field.

These distinctions remain visible in diagnostics/documentation.

## 7. Switching-form generation

Until a separately accepted safety case changes it:

> Any generated or assisted switching form/sequence is a draft requiring qualified human review and approval under the applicable organizational procedure.

No UI label should imply automatic approval merely because software validation passes.

## 8. Normative coverage boundary

A passing machine validation means only:

```text
all implemented/applicable rules in the selected profile passed or were resolved
```

It does not mean:

```text
all possible requirements of Russian law/standards/site instructions are satisfied
```

unless a formally defined coverage scope supports that claim.

## 9. Incomplete project model

When project data has unresolved:

- equipment identity;
- terminals/connections;
- topology;
- state;
- applicable policy;
- source version;

safety-sensitive functions must degrade explicitly:

```text
BLOCKED
UNKNOWN
REQUIRES_CONFIRMATION
```

rather than silently proceeding.

## 10. Imported data trust

CSV/XLSX, NPT, Visio or other imported information is not trusted merely because parsing succeeded.

Safety-relevant import requires semantic validation and explicit ambiguity review.

Provenance must allow the user to see the source of critical facts.

## 11. Automated topology inference

Auto-detected/inferred topology is not equivalent to verified topology.

Each inferred connection should have a resolution status. Critical switching logic may require only confirmed connections depending on the policy/profile.

NPT `nodes` extraction remains research until manually and systematically verified against known schemes.

## 12. AI/LLM boundary

AI may assist with:

- discovery;
- mapping suggestions;
- text explanation;
- draft rule extraction;
- layout suggestions;
- documentation.

AI output must not become normative authority or bypass deterministic safety validation/human review.

For a safety-sensitive action, deterministic domain/rule result and source evidence take precedence over generated prose.

## 13. Real-time / SCADA integration

NPT signal semantics may be imported for engineering/compatibility. Current scope does not authorize online control.

Adding any real-equipment command path would require a new explicit work item covering at least:

- threat/safety model;
- authentication/authorization;
- command confirmation;
- communications quality;
- fail-safe behavior;
- audit;
- commissioning/field validation;
- applicable regulatory and organizational requirements.

Do not grow such a path incrementally as an incidental feature.

## 14. Fail-safe defaults

Examples:

- unknown rule source/version → do not claim validated baseline;
- missing critical policy → block profile activation/critical operation as defined by policy;
- parse failure → preserve original file and avoid partial destructive write;
- failed save validation → restore/retain backup and show error;
- unknown switching prerequisite → do not auto-allow;
- conflicting mandatory/local policy → report conflict, mandatory baseline remains effective.

## 15. Auditability

For critical validation/simulation outcomes retain enough data to reproduce/explain:

- project/model revision;
- state baseline;
- sequence revision;
- rule/profile versions;
- relevant facts;
- result/explanation;
- user confirmations/overrides only where overrides are legally/product-permitted.

An audit record is not a substitute for formal organizational approval, but it supports traceability.

## 16. Prohibited claims/features without separate acceptance

- `100% safe switching guaranteed`;
- `fully compliant with all PУЭ/POTEE/PTEES` without coverage evidence;
- automatic bypass of blocked mandatory rules;
- treating unknown state as safe;
- executing real switching based solely on model result;
- implying software replaces field verification, protective devices or physical interlocks.

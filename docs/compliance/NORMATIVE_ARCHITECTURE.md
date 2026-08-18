# Normative / Compliance Architecture

Статус: canonical foundation document

## 1. Purpose

The product must convert applicable engineering and operational requirements into **traceable, versioned, explainable rules/profiles** without pretending that naming a document equals implementing it.

Compliance architecture serves three main areas:

1. graphics/scheme execution;
2. electrical/domain validation;
3. switching/TBP/interlocks.

## 2. Core principle

A production rule is not just code.

```text
Rule
├── identity
├── authority / layer
├── source provenance
├── edition / amendment chain
├── effective period
├── applicability
├── semantic requirement
├── machine-checkable implementation (optional)
├── severity / blocking policy
├── explanation
├── test/evidence
└── exceptions/limitations
```

If a requirement cannot be automated reliably, it may still exist as a review/checklist/documentation rule rather than being omitted or falsely automated.

## 3. Normative source types

Conceptual source classes:

```text
FEDERAL_MANDATORY_RULE
SECTOR_MANDATORY_RULE
TECHNICAL_REGULATION
STANDARD_GOST_ESKD
OTHER_STANDARD_PROFILE
MANUFACTURER_REQUIREMENT
ENTERPRISE_STANDARD_OR_INSTRUCTION
SITE_OBJECT_INSTRUCTION
PROJECT_REQUIREMENT
RECOMMENDATION_GUIDANCE
```

Actual legal force/applicability must be determined per source and context; enum names are software classification aids, not legal conclusions by themselves.

## 4. Source registry

Every source record should include at least:

```text
source_id
issuer
identifier
full_title
source_type
publication/registration reference
edition/amendment identifiers
effective_from
effective_until (if known)
status: ACTIVE | FUTURE | SUPERSEDED | PARTIAL_REVIEW | UNKNOWN
scope/applicability notes
last_verified_at
verification_source
```

For standards, registry also records official status/current changes from the national standards catalogue.

For legal/normative acts, prefer official publication/issuer sources and retain official publication identifiers.

## 5. Rule registry

Rule ID must be stable across implementation refactors.

Example conceptual ID:

```text
SWITCH.RU.757.<section>.<semantic-name>
GRAPHICS.ESKD.2_702.<semantic-name>
SITE.KVWES.<instruction>.<semantic-name>
```

Exact naming convention is chosen in Compliance Core implementation.

Rule record includes:

- source references (one or more);
- quoted/paraphrased requirement note maintained within copyright/legal limits;
- applicability predicate;
- implementation type;
- severity;
- non-weakening lock state;
- test fixture/scenario IDs;
- review owner/status.

## 6. Applicability resolution

Not every registered source applies to every project/equipment/operation.

Applicability may depend on:

- organization role (consumer vs subject of electric power industry etc.);
- equipment/object category;
- voltage class;
- installation type;
- operation type;
- work conditions;
- date/baseline edition;
- scheme/document type;
- project/site profile;
- manufacturer/model;
- local instruction scope.

Compliance Core must explain why a rule is or is not applicable.

## 7. Baseline date and reproducibility

A project/released document should be verifiable against a recorded normative baseline.

Conceptually:

```text
project compliance baseline date: 2026-08-18
resolved sources/rules: ...
```

When the registry later updates, the product must distinguish:

- rules applicable to the old release/baseline;
- new current rules;
- migration/revalidation requirements.

Do not silently change historical validation conclusions without recording the new baseline.

## 8. Amendment/supersession lifecycle

Registry supports:

```text
BASE ACT
  ├── amendment A
  ├── amendment B
  └── amendment C
```

and:

```text
source A superseded/replaced by source B
```

Current effective text is a resolved version, while provenance retains the chain.

A source update triggers:

1. registry update;
2. impacted rule identification;
3. rule review;
4. tests/fixtures update;
5. project/profile migration/revalidation decision;
6. release note when user-visible behavior changes.

## 9. Implementation classes

Each requirement is classified by what software can validly do:

### MACHINE_BLOCKING

Deterministic condition can be checked and violation must block an operation/output under the selected profile.

### MACHINE_ERROR / WARNING

Deterministic validation finding without automatic operational block in all contexts.

### ASSISTED_REVIEW

Software can collect facts/pre-fill/check partial conditions but qualified human judgement remains required.

### DOCUMENTATION_ONLY

Relevant requirement is recorded and surfaced but not machine-checkable in current model.

### OUT_OF_PRODUCT_BOUNDARY

Requirement concerns physical/process/organizational control outside software authority; product may reference it but must not claim verification.

## 10. Rule evaluation result

Result should carry:

```text
rule_id
status: PASS | FAIL | UNKNOWN | NOT_APPLICABLE | REQUIRES_REVIEW
severity
affected_entity/operation
facts_used
missing/unknown facts
source reference
explanation
suggested resolution (if appropriate)
```

`UNKNOWN` is not PASS.

## 11. Rule layers and non-weakening

Resolved project policy is composed from baseline + local layers.

Mandatory locked rules cannot be disabled or relaxed by local overlays.

Local rules may:

- add additional checks;
- narrow permitted conditions;
- require extra steps;
- choose stricter limits;
- define local naming/templates;
- encode equipment-specific restrictions.

Attempted weakening produces `POLICY_CONFLICT`.

See `LOCAL_POLICY_OVERLAYS.md`.

## 12. Graphics profiles

Standards-oriented scheme rules are handled as graphic/document profiles, not hard-coded renderer magic.

A profile may define/check:

- symbol family/profile;
- line styles/weights;
- connection semantics;
- labels/designations;
- text/annotation rules;
- permitted orientation/transformation;
- sheet/document conventions;
- print/export requirements.

See `GRAPHICS_GOST_PROFILE.md`.

## 13. Switching rules

Switching/TBP consumes the same rule registry but uses specialized evaluators over topology/state/sequence context.

Rule engine must preserve source and explanation in generated diagnostics and, where required, in audit/report output.

## 14. Local policy storage

Local/company/site policies are versioned project/profile assets with provenance:

```text
policy_id
organization/site
source document ID/revision/date
approved/effective period
rules/templates/mappings
supersedes
```

The product must not encourage users to copy entire copyrighted/proprietary manuals into a public repository; store only what is authorized/needed in controlled environments.

## 15. Review workflow

Normative rule development is a domain-engineering workflow:

```text
source identified
→ current edition verified
→ relevant provision scoped
→ semantic rule proposal
→ implementation class chosen
→ domain/legal/normative review as appropriate
→ tests/evidence
→ accepted profile release
```

Chat/LLM extraction can assist discovery/drafting but is not normative authority.

## 16. No fake full-compliance claims

Until a defined coverage matrix is complete, product language must use scoped claims such as:

- `ГОСТ 2.702 profile: implemented rules X/Y/Z`;
- `Switching baseline 2026-08-18: selected rules encoded`;
- `validation does not cover organizational requirements ...`.

Do not present a green status as `соответствует всем требованиям ПУЭ/ПТЭЭС/ПОТЭЭ` unless the entire claimed scope is formally defined and proven.

## 17. Testing

Compliance tests are indexed by rule ID and source version.

Required patterns:

- positive scenario;
- negative scenario;
- boundary values;
- NOT_APPLICABLE scenario;
- UNKNOWN/missing-fact scenario;
- local stricter overlay scenario;
- attempted weakening conflict scenario;
- amendment migration regression where source changes.

## 18. Update monitoring

A future maintenance workflow may periodically check official source registries for changes, but automatic detection never automatically changes production rule semantics.

Update flow requires human/domain review before a new normative profile becomes active.

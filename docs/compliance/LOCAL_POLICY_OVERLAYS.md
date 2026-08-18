# Local Policy Overlays

Статус: canonical foundation document

## 1. Purpose

Different enterprises, sites and equipment fleets often have legitimate additional restrictions, instructions, naming conventions and approved workflows.

The product must support this **without allowing local configuration to weaken an applicable mandatory requirement**.

## 2. Layer model

Conceptual resolution order:

```text
Mandatory regulatory baseline
        ↓
Applicable standards/profile baseline
        ↓
Manufacturer/equipment constraints
        ↓
Enterprise policy/instruction
        ↓
Site/object instruction
        ↓
Project-specific policy
```

This is not a simple `last write wins` stack.

Authority, applicability and restrictiveness are evaluated explicitly.

## 3. Non-weakening invariant

For a locked mandatory rule `R`:

```text
local overlay may:
  add stricter condition
  add extra prerequisite
  reduce allowed range
  add required check/step
  add local wording/template

local overlay may NOT:
  disable R
  enlarge allowed range beyond R
  convert blocking requirement into warning
  treat UNKNOWN as PASS where R requires proof
  suppress mandatory step solely by configuration
```

Attempted weakening produces a configuration error and the mandatory baseline remains effective.

## 4. Policy package

Conceptual package:

```text
PolicyPackage
├── policy_id
├── name
├── layer
├── organization/site/equipment scope
├── source document metadata
├── revision/effective dates
├── approval metadata where appropriate
├── parent/dependencies
├── rules
├── templates/naming conventions
├── mappings
└── signature/hash/provenance metadata as later required
```

Exact serialization is PENDING.

## 5. Applicability

A local package may target:

- one enterprise;
- one branch/site/object;
- voltage level;
- equipment type;
- manufacturer/model;
- specific bay/installation class;
- switching operation category;
- document/scheme profile.

Do not encode site name checks throughout application code. Applicability belongs to profile/rule resolution.

## 6. Manufacturer/equipment constraints

Examples of legitimate model-specific constraints:

- sequence restrictions from operating manual;
- mechanical/electrical interlock dependencies known for that model;
- allowed operating states/ratings;
- required delay/check before another action;
- special maintenance/inspection prerequisites.

These constraints require source manual revision/model applicability and must be distinguishable from government norms and company policy.

## 7. Enterprise/site rules

Examples:

- stricter switching sequence;
- extra position confirmation;
- additional dispatcher/shift checks;
- local operational names;
- approved switching-form wording;
- forbidden operation combinations specific to installed arrangement;
- requirement to use a particular view/document during switching;
- stricter scheme-release/approval process.

Again, source layer must be shown to user.

## 8. Rule composition

Prefer semantic composition over arbitrary override text.

Illustrative limit rule:

```text
baseline: X <= 100
enterprise: X <= 80
resolved: X <= 80
```

Attempted:

```text
site: X <= 120
```

Result:

```text
POLICY_CONFLICT_WEAKENING
baseline remains X <= 100 (or stricter effective upper-layer rule)
```

For boolean prerequisites:

```text
mandatory requires A
local requires B
resolved requires A AND B
```

Where rules are not mathematically comparable, Compliance Core requires explicit composition semantics or human policy review rather than guessing which is stricter.

## 9. Conflict classes

At minimum:

```text
WEAKENING_ATTEMPT
CONTRADICTORY_REQUIREMENTS
AMBIGUOUS_PRECEDENCE
MISSING_REQUIRED_SOURCE
OUT_OF_SCOPE_REFERENCE
EXPIRED_POLICY
UNRESOLVED_APPLICABILITY
```

Diagnostics should identify both rules/sources.

## 10. Policy authoring UX

Do not expose raw code/config as the only administration interface forever.

Target editor should support:

- source metadata;
- applicability selectors;
- typed rule parameters;
- rule explanation;
- comparison with inherited baseline;
- preview of resolved effective policy;
- conflict validation before activation;
- test scenarios;
- revision history/diff.

Early implementation may use version-controlled structured files plus validation tooling before a full UI exists.

## 11. Policy lifecycle

Suggested states:

```text
DRAFT
UNDER_REVIEW
APPROVED
ACTIVE
SUPERSEDED
EXPIRED
```

The product must record which package versions were active for a released scheme/switching form/project baseline.

## 12. Project portability

A project references required policy package identities/versions and should be able to report:

- available/resolved;
- missing;
- newer version available;
- incompatible version;
- superseded baseline.

If required safety/normative policy is missing, do not silently use defaults and show a green validation status.

## 13. Public vs private storage

Enterprise/site/manufacturer policy material can be confidential/proprietary.

Architecture must allow:

- public product repository to contain schema/examples only;
- private policy packages on controlled VPS/local deployment;
- no required upload of private instructions to public GitHub;
- tests with synthetic/cleared examples in public CI.

## 14. Deployment profiles

Different sites may enable different first-party modules/profile packages, but should run the same product codebase where possible.

Avoid per-site forks such as:

```text
product-kvwes
product-site2
product-site3
```

Prefer:

```text
same executable
+ project/site policy package
+ enabled modules
+ local symbol/template package if authorized
```

## 15. Tests

Every local policy package intended for operational use should have at least:

- schema validation;
- source metadata validation;
- non-weakening check;
- positive/negative example scenarios for critical rules;
- compatibility test with declared baseline profile;
- expiry/effective-date checks;
- resolution snapshot test.

## 16. Anti-goals

Do not implement:

- unrestricted scripting from policy files;
- `disableMandatoryRule=true` escape hatch;
- arbitrary site-specific code branches where policy data suffices;
- opaque override precedence based only on file load order.

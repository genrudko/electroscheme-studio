# Import, Reconciliation and Auto Layout

Статус: canonical foundation document

## 1. Product role

Structured import is a first-class module and one of the central product differentiators.

The objective is not merely `CSV → objects on canvas`.

The objective is:

```text
structured source
→ normalized engineering candidate
→ validated topology
→ canonical ElectricalProject
→ domain-aware diagram proposal
→ engineer corrections
→ safe re-import/update
```

## 2. Supported first sources

Initial target:

- CSV;
- XLSX.

The importer must not force one rigid corporate template as the only accepted source.

Users may map external columns to canonical semantics and save mapping profiles.

Example:

```text
"Поз."          → equipment.external_id
"Тип"           → equipment.type
"Наименование"  → equipment.name
"Откуда"        → connection.from
"Куда"          → connection.to
"U, кВ"         → equipment.rated_voltage
```

## 3. Import pipeline

```text
Source file
  ↓
Source reader
  ↓
Mapping profile
  ↓
Normalization
  ↓
ImportCandidate
  ↓
Semantic/type validation
  ↓
Connection/terminal resolution
  ↓
Staging review
  ↓
Reconciliation against project
  ↓
Approved ImportPlan
  ↓ atomic transaction
ElectricalProject
```

Each stage must be independently diagnosable/testable.

## 4. Mapping profiles

A mapping profile records:

- profile ID/version/name;
- accepted source sheet/table patterns;
- column mappings;
- transforms/normalizers;
- unit mappings;
- equipment type mapping rules;
- identifier strategy;
- connection-reference syntax;
- required/optional columns;
- default values with explicit provenance;
- source organization/site scope if applicable.

Mapping profile is configuration, not executable arbitrary code from the spreadsheet.

## 5. Confidence and ambiguity

Importer outputs explicit resolution status.

Minimum classes:

```text
RESOLVED
REQUIRES_CONFIRMATION
CONFLICT
INVALID
```

Optional confidence score may assist ordering, but status and rationale must be deterministic/explainable.

Example ambiguity:

- source says `Q1 → T1`;
- `T1` has multiple suitable terminals;
- there is no unambiguous rule from source/profile/context.

Correct behavior: present candidate terminals and reason for ambiguity.

Incorrect behavior: silently choose first terminal.

## 6. Staging model

ImportCandidate must be separate from canonical project.

Staging review summarizes:

- new equipment;
- matched existing equipment;
- changed properties;
- new/changed/removed connections;
- unresolved references;
- duplicate IDs;
- type conflicts;
- voltage/domain conflicts;
- unknown source rows/columns preserved for diagnostics where useful.

No canonical mutation happens until ImportPlan is approved.

## 7. Reconciliation

Repeat import is a primary scenario.

Entity matching uses explicit stable provenance/mapping rules, not only display names.

Possible results:

```text
UNCHANGED
ADD
UPDATE
REMOVE_CANDIDATE
RELINK
CONFLICT
MANUAL_MATCH_REQUIRED
```

Potential deletion/removal must be especially explicit. If imported source no longer contains an entity, the importer must distinguish:

- source-authoritative deletion;
- source omission/filter;
- project-owned entity;
- ambiguous disappearance.

Do not delete automatically unless profile/source authority and user approval permit it.

## 8. Provenance

For each imported entity/field where practical retain:

- source file/content fingerprint;
- sheet/table;
- row/external ID;
- mapping profile/version;
- raw value relevant to reconciliation;
- normalized value;
- transformation/rule used;
- import revision.

This allows future update/diff and explains why the project contains a value.

## 9. Topology construction

After equipment/terminal resolution, importer builds proposed semantic connections.

Validation includes as applicable:

- endpoint existence;
- terminal compatibility;
- duplicate connection;
- impossible self/loop patterns where domain forbids them;
- voltage-level mismatch;
- equipment terminal cardinality;
- dangling network fragments;
- unknown/unsupported equipment types;
- object/site containment consistency.

The exact electrical rule set grows through Compliance/Equipment Library profiles.

## 10. Auto-layout is not topology

Auto-layout consumes a valid or partially valid topology graph and produces geometry for a selected view.

```text
TopologyGraph + ViewProfile + ExistingConstraints
        ↓
LayoutProposal
```

The proposal may be rejected/edited without changing topology.

## 11. Domain-aware layout

Initial deterministic strategies may understand concepts such as:

- voltage levels;
- bus/bus sections;
- bay/feeder grouping;
- transformers as level boundaries;
- sequence of switching equipment along an electrical path;
- earthing switches related to a section;
- lines/generators/loads;
- orientation preferences;
- standard spacing and label regions.

Avoid generic force-directed layout as the primary electrical scheme strategy.

## 12. Layout constraints

Manual engineer edits create controlled constraints.

Examples:

```text
PinnedPosition
FixedOrientation
RelativeOrder
GroupRegion
BusOrientation
UserOwnedRoute
ProtectedLabelPosition
KeepTogether
MinimumSpacingOverride
```

Constraints have scope and priority; impossible constraint sets produce diagnostics rather than corrupt geometry.

## 13. Incremental layout

Re-import/layout update must minimize disruption.

Priority order:

1. preserve user-owned/locked constraints;
2. preserve unchanged local neighborhoods where possible;
3. place new/changed entities near semantically related equipment;
4. reroute only impacted routes where feasible;
5. expose layout conflicts for review.

A global full re-layout is an explicit command, not the default update behavior.

## 14. Layout profiles

Possible future profiles:

- substation single-line;
- switchgear/bay;
- wind farm collector system;
- auxiliary power;
- free/legacy imported view.

Profiles are introduced only after representative examples prove repeated layout semantics.

## 15. First vertical-slice acceptance

Use a small real/representative electrical object, not synthetic arbitrary graph only.

Required scenario:

1. open CSV/XLSX;
2. map fields or select saved profile;
3. create equipment/terminals/connections;
4. show staging summary;
5. resolve at least one deliberately ambiguous case;
6. apply ImportPlan;
7. render auto-generated one-line view;
8. manually move/lock/re-route selected elements;
9. save/reopen native project;
10. import modified source adding/changing equipment;
11. show reconciliation diff;
12. apply update;
13. prove previous manual layout constraints survive;
14. validate topology before/after.

## 16. Failure modes to prevent

- source rows become permanent native storage format;
- importer mutates canonical project while parsing;
- ambiguous terminals chosen silently;
- entity matching by display name only;
- every re-import destroys diagram layout;
- layout engine changes electrical connections to make drawing prettier;
- user-owned manual edits cannot be distinguished from auto-generated geometry;
- custom corporate spreadsheet requires hard-coded one-off parser instead of reusable mapping profile when general mapping is sufficient.

## 17. Future source adapters

After first CSV/XLSX workflow, the same staging/reconciliation contracts can support:

- NPT project import;
- controlled Visio extraction;
- CIM/exchange formats;
- corporate databases/APIs;
- other engineering exports.

New sources must reuse canonical staging/reconciliation semantics rather than write directly to Domain Core.

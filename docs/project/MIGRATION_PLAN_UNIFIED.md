# Migration Plan — Three Directions to One Product

Статус: canonical foundation document

## 1. Purpose

Migration does **not** mean copying three repositories/codebases into one tree.

It means extracting proven knowledge/behavior/data contracts from each previous direction, assigning a new module owner, adding missing tests/provenance, and retiring duplicate state models only after equivalent behavior is accepted.

## 2. Migration rule

For every significant asset classify:

```text
RETAIN_AS_EVIDENCE
SALVAGE_BEHIND_NEW_CONTRACT
REIMPLEMENT_FROM_BEHAVIOR
MIGRATE_DATA_ONLY
ARCHIVE_HISTORICAL
RETIRE_AFTER_ACCEPTANCE
```

Every salvaged/migrated asset records:

- source repository/path/commit where possible;
- current responsibility;
- known defects/limitations;
- new owner module;
- required tests/evidence;
- dependency/licensing/provenance concerns;
- retirement condition for the old implementation.

## 3. ElectroScheme Studio migration

Repository `genrudko/electroscheme-studio` becomes the umbrella only for continuity; this does not imply its old frontend/backend architecture owns the new product.

### Likely retain as evidence

- VSDX/VSSX inspection/ShapeSheet research;
- market/reference-product research;
- prototype quarantine/disposition method;
- snapping/grid/busbar experiments;
- platform/packaging measurements;
- Tauri spike implementation and failure evidence;
- Visio controlled fixtures/round-trip knowledge.

### Likely reimplement from behavior/new contract

- application shell;
- current CSS/design/ribbon/property composition;
- large canvas ownership/state composition;
- duplicated frontend/backend document state;
- product-level command/mutation path if current implementation conflicts with new Domain Core.

### Pending after Platform Spike

- any Vue/TypeScript/SVG code reuse;
- Rust/Tauri native adapters;
- current web build pipeline.

No Tauri/WebView asset is promoted merely because PR #4 reached green CI.

## 4. NPT Engineering Toolkit migration

NPT research is a major compatibility/domain corpus and should be preserved carefully.

### Proven concepts to carry forward

- lossless/preserve-first XML handling;
- XSDE document/object inventory and semantics;
- embedded CustElem vs external `.menu` library distinction;
- typed custom-value semantics (`scdState`, `scdCommand`, `scdValue`, `scdColor`, etc.);
- ASU/TECH/KKS signal catalog model/search;
- XTABL v6.0 lossless records and proven field meanings;
- preserve-only handling for unknown XTABL fields;
- native resource/path alias handling;
- explicit safe/unsafe creation boundaries.

### Must remain NPT-specific

- `sTag` allocation/counters;
- `RTID`/`TechData` registry semantics;
- `CustElem` embedding/storage;
- `scd*` serialization;
- XSDE XML order/comments/unknown fields;
- XTABL raw-record specifics.

These live in NPT adapters/storage and translate to/from neutral domain entities where translation is justified.

### Critical unresolved migration experiment

NPT `nodes` are topology-related but are not yet proven to reconstruct a complete neutral electrical graph.

Required evidence:

1. select one small known real cell/mnemonic;
2. extract object/Tech/node relations;
3. map to neutral terminals/connections;
4. render or graph the extracted topology independently;
5. manually compare with visible one-line diagram;
6. test energized/de-energized propagation under several known switching states;
7. record unmapped/ambiguous relationships.

Until this passes, do not make NPT topology import a core invariant.

### Renderer status

Existing Mnemo Editor rendering is not accepted for fidelity. Before broad NPT editor expansion, compare a known mnemonic side-by-side against native NPT/Modus and classify differences as geometry/style/resource vs runtime-state semantics.

## 5. Switching-forms-generator / TBP migration

Repository `genrudko/switching-forms-generator` remains reference during migration.

### Valuable concepts

- draft-generation workflow;
- mandatory human review boundary;
- profiles/local customization;
- operational wording/patterns;
- normative reference data;
- real project tests/examples.

### Migration requirement

Existing code/YAML behavior is **not normative authority by itself**.

Each rule migrated into the new Compliance/Switching modules must be reclassified:

```text
normative mandatory
normative conditional
enterprise/site policy
manufacturer/equipment constraint
formatting/wording convention
heuristic/recommendation
```

and linked to source/version/applicability metadata.

### Domain migration

TBP must consume shared:

- equipment identity;
- terminals/connections/topology;
- state;
- compliance rules.

It must not recreate a second project/equipment database.

## 6. Data migration philosophy

Old project data may be imported through explicit adapters/migrations, but the native project format is not required to mimic any old format.

Where round-trip compatibility is required (notably NPT), preserve vendor-specific payload in adapter-owned structures/extension blocks rather than flattening unknown information into neutral Core.

## 7. Repository strategy

During Foundation and early spikes:

- do not delete old files from `electroscheme-studio`;
- do not vendor private TBP repo into public repo;
- do not commit NPT vendor binaries/full corpus;
- create new product tree only after platform stack selection;
- record old asset disposition before retirement.

The old TBP repo and NPT artifacts may remain separate reference sources until their new modules reach accepted parity for selected workflows.

## 8. Migration gates

An old subsystem can be retired only if:

1. target module/owner exists;
2. required behavior/data has a mapping decision;
3. representative tests pass;
4. no required provenance/unknown fields are lost;
5. owner accepts the replacement workflow;
6. rollback/reference material remains available where legally/operationally appropriate.

## 9. Anti-goal

Do not optimize migration for preserving old implementation effort.

The objective is preserving **validated knowledge, user value, format semantics and evidence** while discarding architecture that would reproduce the old projects' limitations.

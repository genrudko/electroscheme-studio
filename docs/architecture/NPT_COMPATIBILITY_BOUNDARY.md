# NPT Compatibility Boundary

Статус: canonical foundation document

## 1. Role

NPT Expert/Modus compatibility is a product module/adaptation layer, not the source architecture of the unified platform.

NPT provides two things:

1. a valuable real industrial corpus for requirements/topology/state/equipment research;
2. a compatibility target for XSDE/XTABL/project workflows.

## 2. Boundary

```text
NPT project/files/catalog
        ↕
Modules.Npt
├── parsers/writers
├── lossless vendor payload
├── signal/catalog adapter
├── vendor IDs/counters
├── NPT renderer/editor semantics
└── compatibility validation
        ↕ mapping
Neutral Domain Core
```

Core does not know how NPT serializes `sTag`, `TechData`, `RTID`, `CustElem` or `scd*`.

## 3. Proven research baseline to preserve

Current evidence includes:

- 475 studied XSDE documents parse successfully;
- large real object corpus (~145k objects in the studied set);
- lossless unchanged XSDE round-trip demonstrated across the studied corpus;
- embedded `customView`/`CustElem` definitions cover used custom views in the studied documents;
- external `.menu` libraries are relevant to insertion/palette, while embedded definitions are source of truth for an existing saved file;
- NPT custom-value semantics are typed and not uniformly KKS;
- `scdCommand` may be KKS-like or a named NPT command;
- `scdValue`, `scdColor`, `scdFormat` and other literals must not be treated as signal references;
- ASU/TECH/KKS catalog research exists at large real scale;
- XTABL v6.0 lossless core is proven for seven current tables / 1461 records;
- several XTABL fields remain preserve-only/unknown and must not be guessed;
- NPT ID/counter allocation has hidden/reserved behavior; simple `+1` assumptions are unsafe for arbitrary new-object creation.

These are compatibility facts, not neutral domain invariants.

## 4. Lossless/preserve-first rule

When editing vendor files, unknown data is preserved by default.

XSDE writer must preserve where required:

- unknown attributes/elements;
- XML order;
- comments;
- embedded definitions;
- vendor-specific values;
- untouched byte representation where lossless core permits.

Do not reconstruct full documents from a simplified neutral representation and discard unknown content.

A mapped neutral model may coexist with an adapter-owned preservation layer.

## 5. Safe editing vs creation

Different capabilities have different evidence levels.

Current posture:

- reading existing objects: strong evidence;
- lossless unchanged write: strong evidence;
- editing known non-topological properties/objects: promising/proven in bounded cases;
- inserting arbitrary new Tech-backed objects: experimental until native Modus/SCADA acceptance is repeated;
- electrical topology creation/reconnection and `nodes` manipulation: blocked until explicitly proven.

UI must reflect capability level rather than expose unsafe actions behind a generic property editor.

## 6. Renderer fidelity

Existing prototype Mnemo renderer is not accepted as visually faithful.

Before broad editor feature expansion:

1. choose known mnemonic(s);
2. capture native NPT/Modus screenshot at known state/scale;
3. render the same XSDE;
4. compare geometry, text, colors, line styles, custom symbols, images/resources and clipping;
5. separate static-render defects from runtime-state/value semantics;
6. close high-impact fidelity gaps first.

Do not claim success because object skeletons are recognizable.

## 7. NPT signal catalog

Shared NPT catalog may expose neutral signal references/search results but retains source system semantics.

Catalog concepts:

- ASU signal;
- TECH parameter;
- device;
- hierarchy/tree;
- link/cross-reference;
- KKS;
- metadata/unit/type.

Neutral Domain SignalBinding references catalog identity through adapter contracts. Core does not copy the NPT SQL/data model.

## 8. Typed property model

NPT property UI requires typed descriptors:

```text
signal reference
command reference or named command
literal state-to-text mapping
literal color mapping
format string
device reference
quality/static flags
preserve-only unknown
```

Generic `name=value string` editing is insufficient as the primary UX.

## 9. XTABL direction

The Table Editor should preserve NPT format compatibility while replacing the legacy row-by-row authoring workflow.

High-value target:

```text
select equipment set (e.g. WTG 1..84)
+ select parameter columns
+ choose template/profile
→ generate table records
→ review/edit
→ write compatible XTABL
```

For new records, use proven field semantics and known-good templates; unknown fields remain copied/preserved rather than inferred.

## 10. Topology extraction experiment

Critical unknown: whether `nodes`/Tech relationships are sufficient to reconstruct usable electrical connectivity.

Required experiment is described in migration plan and must produce:

- neutral graph artifact;
- mapping table NPT object ↔ domain equipment/terminal;
- unresolved references;
- visual/manual comparison;
- state-dependent connectivity test.

Until accepted, NPT topology extraction is a research adapter, not a promised import capability.

## 11. Native assets and IP/provenance

NPT symbol/library assets may be necessary for compatibility rendering/editing of NPT files where rights/usage permit.

They are not automatically the native symbol library of Scheme Studio.

Native product symbols should have independent provenance and applicable standards basis. Compatibility and native representation may map the same semantic equipment to different graphical assets.

## 12. Corpus location

Full NPT reference corpus/vendor binaries remain outside public Git repository, on controlled development storage/VPS.

Repository contains:

- synthetic fixtures;
- cleared/minimal examples where permissible;
- schemas/tests/expected normalized outputs created by the project.

Full-corpus compatibility tests run only in controlled runner lane.

## 13. Module deliverables

NPT module eventually includes:

- project/file discovery;
- XSDE Mnemo Editor;
- faithful renderer;
- typed properties;
- signal picker/catalog;
- validation/diagnostics;
- safe backup/save/reparse;
- XTABL editor/generator;
- controlled resource library palette;
- optional topology import after proof.

It does not include replacement NPT runtime/server/SCADA services under current scope.

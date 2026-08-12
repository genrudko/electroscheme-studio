# Visio interoperability spike report

Status: `AUTOMATED_BOUNDARY_PROVEN; MICROSOFT_VISIO_GATE_PARTIAL`  
Work item: `DESKTOP-PLATFORM-AND-CORE-SPIKE-001`

## 1. Scope proved by this spike

The spike proves that mandatory Visio interoperability can remain local-first and independent of the writable canonical document model.

Implemented and automated:

- relationship-aware controlled VSDX OPC/ZIP package read;
- controlled VSSX master package generation and read;
- XML well-formedness checks for package parts;
- kind-specific required-part checks for drawing and stencil packages;
- content-type checks for controlled Visio parts;
- OPC relationship graph traversal and dangling-relationship rejection;
- Visio-specific `document -> pages -> page` and `document -> masters -> master` relationship checks;
- Page/Rel ownership checks that reject the previously false-green inline relationship form;
- PageSheet ownership checks;
- controlled 1-D connector validation using `BeginX/BeginY/EndX/EndY`;
- negative regression tests for the old malformed VSDX structure and dangling relationships;
- source ID extraction and structured diagnostics;
- deterministic minimal VSDX generation from canonical JSON;
- deterministic generated-fixture SHA-256 checks;
- packaged Python process execution through the same bounded host port in Electron and Tauri;
- generated VSDX reinspection after write;
- provenance-friendly content-addressed evidence;
- no network requirement and no Microsoft Visio dependency during normal package read/write.

Not proved and not claimed:

- arbitrary VSDX/VSSX support;
- complete ShapeSheet formula evaluation;
- group/transform fidelity for real engineering libraries;
- legacy binary `.vsd/.vss` parsing;
- lossless arbitrary Visio round trip;
- full edit/save/reopen acceptance of the final exact artifact by Microsoft Visio.

## 2. Controlled fixtures

### Canonical source

`spikes/shared/fixtures/canonical-project.json`

The canonical fixture contains fixed IDs, one equipment identity, one representation, one busbar and one connection. It has no host path or timestamp dependency.

### VSDX

`spikes/shared/fixtures/visio/controlled-minimal.vsdx`

Current deterministic SHA-256:

```text
37af1404c342757d8641d3faa43a472d5559c821c0057647a7f33a226dad2664
```

It is deterministically generated from the canonical fixture and retained as the exact automated package fixture.

The writer now produces the relationship chain:

```text
package
  -> visio/document.xml
      -> visio/pages/pages.xml
          -> visio/pages/page1.xml
```

`pages.xml` owns the PageSheet and child `Rel`; `page1.xml` owns PageContents/shapes. The controlled connector is a 1-D shape with direct begin/end cells.

### VSSX

`controlled-master.vssx` is generated in CI from versioned package/XML source rather than uploaded as an opaque binary.

Current deterministic SHA-256:

```text
4184ec60635d67b6aa653cf2dd6f83ec0a34f4146668a3df6d8eb3927712b4f8
```

The generated stencil contains a controlled master, PageSheet, relationship-safe master part and connection row. CI validates it and packages the same generated artifact with both desktop candidates.

## 3. Protocol boundary

The executable protocol is conceptually:

```json
{
  "protocol": "electroscheme-visio-tool/1",
  "operation": "inspect | generate-vsdx",
  "kind": "vsdx | vssx",
  "status": "ok | invalid",
  "sha256": "content digest",
  "parts": [],
  "sourceIds": [],
  "diagnostics": []
}
```

The desktop host supervises the Python process with:

- explicit executable and argument list;
- no shell command interpolation;
- closed stdin;
- captured stdout/stderr and exit code;
- 15-second timeout;
- explicit output path;
- renderer access only through a typed platform port.

The process does not receive a writable in-memory project object. Its output is data/evidence that must be parsed, validated and applied through a future TypeScript import/export transaction.

## 4. Package validation

Drawing requirements include:

- `[Content_Types].xml`;
- root relationships;
- core properties;
- `visio/document.xml` and relationships;
- pages collection and relationships;
- controlled page content;
- one internal package-document relationship;
- one document-pages relationship;
- one pages-page relationship;
- no dangling internal relationships;
- Page child `Rel` matching the pages relationship ID;
- PageSheet in `pages.xml`, not `page1.xml`;
- controlled connector direct 1-D endpoint cells.

Stencil requirements include:

- the common document/core package parts;
- masters collection and relationships;
- controlled master content;
- one document-masters relationship;
- one masters-master relationship;
- matching Master child `Rel`.

The validator intentionally does not require optional extended-properties parts from arbitrary third-party packages. The controlled fixture includes `docProps/app.xml`, but absence of an optional part is not itself treated as package corruption.

Package validation is fail-closed for malformed required relationships, missing required parts, malformed XML and dangling relationships. It is necessary evidence but is not equivalent to Microsoft Visio acceptance.

## 5. Regression that invalidated the old green claim

The previous CI validator could return green for a package that was ZIP/XML-valid but structurally wrong for Visio.

The repaired test suite now constructs and rejects the old defect class, including:

- inline `<Pages r:id="...">` ownership in `document.xml`;
- `r:id` attached directly to `<Page>` instead of child `<Rel>`;
- missing required Page relationship semantics;
- dangling relationship target.

These regressions are part of the normal `shared-contracts` CI path, so future generator changes cannot silently restore the old false-green behavior.

## 6. Minimal VSDX write path

`generate-vsdx` reads the controlled canonical JSON and generates an OPC package with:

- deterministic part ordering;
- fixed ZIP timestamps/permissions;
- project title metadata;
- equipment designation as source/Shape Data text;
- one busbar shape;
- one 1-D connector and connection records;
- relationship-safe pages structure;
- reproducible byte output.

The current writer is a spike proof, not the production exporter. It supports only the controlled fixture and must not be generalized into a compatibility claim.

Repair-evidence run `31603119700` independently generated and inspected the same VSDX on Windows and Linux. The controlled and generated VSDX hashes were equal (`37af1404...`), and both platform scenarios reported empty diagnostics.

## 7. Source/provenance ownership

Recommended production ownership:

| Concern | Owner |
|---|---|
| authoritative engineering identity and commands | TypeScript canonical document core |
| source package digest and source IDs | canonical provenance references populated through import transaction |
| package/XML/ShapeSheet extraction | isolated Python Visio tool |
| mapping rule version | explicit import/export profile referenced by canonical diagnostics/provenance |
| unsupported feature diagnostics | structured tool output normalized by TypeScript application layer |
| foreign/opaque payload | bounded non-authoritative canonical payload reference |
| SVG/UI rendering | projection only |

No generated TypeScript catalog may contain a local absolute source path. The prototype catalog's `G:\\electroscheme-studio\\Фигуры.vsdx` path is a known provenance defect.

## 8. Microsoft Visio owner evidence

Owner manual evidence exists for an earlier repaired VSDX artifact with SHA-256:

```text
b9758d3b9f6c96cc761f4ddac31b72cec53d0701f499b4c5242a423663e28784
```

The owner opened that repaired artifact in Microsoft Visio Professional on Windows and reported:

- file opened successfully;
- no damage/repair message appeared;
- `Q-SPK-1` displayed;
- `BUS` displayed;
- the connector displayed;
- the page looked visually correct.

This is accepted as positive owner evidence for **Visio open/render of the repaired package structure**.

It does **not** prove:

- arbitrary VSDX support;
- lossless round-trip compatibility;
- edit/save/reopen preservation;
- byte-for-byte acceptance of the current regenerated fixture.

The source-level repair was later reconstructed in GitHub because the previous chat could not push it. The deterministic repository fixture produced by that reconstruction is `37af1404...`, not the owner-tested `b9758d3b...`. This digest difference is recorded explicitly rather than pretending the owner tested bytes that were never supplied to Visio.

## 9. Remaining Microsoft Visio gate

State:

```text
OWNER_OR_WINDOWS_VISIO_EVIDENCE_REQUIRED — PARTIAL
```

Protocol:

`spikes/evidence/VISIO_MANUAL_ACCEPTANCE_PROTOCOL.md`

Already positive:

- repaired-structure open/render in Microsoft Visio Professional on Windows.

Still required by the formal exact-artifact protocol before the gate can be closed:

1. use the final Windows artifact recorded in Draft PR #4;
2. verify the current controlled/generated VSDX SHA;
3. open the exact final-artifact files without repair warning;
4. edit the controlled shape/text/Shape Data;
5. save a modified VSDX;
6. close and reopen it;
7. verify the modification persists and preserve exact evidence.

Until that exact-artifact edit/save/reopen evidence exists, the spike must not claim full Microsoft Visio acceptance or lossless round trip.

## 10. Independent non-Visio evidence

As an additional automated check, the repaired controlled VSDX was opened by LibreOffice headless and converted to PDF; expected `Q-SPK-1` and `BUS` text were present in the converted output.

This is useful independent package/render evidence but is not a substitute for Microsoft Visio.

## 11. Legacy VSD/VSS strategy

Binary `.vsd/.vss` support is not implemented in this spike. The recommended evidence-driven strategy is:

1. inventory actual customer prevalence and versions;
2. prefer one-time conversion in Microsoft Visio or an explicitly evaluated local converter when legal/operationally available;
3. preserve original binary file digest and conversion provenance;
4. import only the converted VSDX/VSSX through the controlled profile;
5. report unsupported/lost features explicitly;
6. do not embed Microsoft Visio automation as a normal runtime dependency unless a later ADR proves it is required for a defined legacy bridge.

Legacy support must not silently broaden the native document model or postpone loss reporting.

## 12. Production follow-up

`CANONICAL-DOCUMENT-CORE-001` reserves provenance, mapping-version, diagnostics and foreign-payload boundaries but does not implement the full Visio pipeline.

A later Visio-source-pipeline work item must add:

- relationship-safe OPC traversal beyond the controlled subset;
- ShapeSheet support matrix and formula evaluator policy;
- group/transform/text/connection fidelity fixtures;
- content-addressed real-corpus evidence;
- explicit supported-subset profiles;
- review/promotion flow for VSSX masters;
- import/export no-silent-loss reports;
- real Microsoft Visio open/edit/save acceptance for supported profiles.

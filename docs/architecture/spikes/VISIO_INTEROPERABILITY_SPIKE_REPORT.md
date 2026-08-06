# Visio interoperability spike report

Status: `AUTOMATED_BOUNDARY_PROVEN; MICROSOFT_VISIO_GATE_OPEN`  
Work item: `DESKTOP-PLATFORM-AND-CORE-SPIKE-001`

## 1. Scope proved by this spike

The spike proves that mandatory Visio interoperability can remain local-first and independent of the writable canonical document model.

Implemented and automated:

- controlled VSDX OPC/ZIP package read;
- controlled VSSX master package generation and read;
- XML well-formedness checks for package parts;
- kind-specific required-part checks for drawing and stencil packages;
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
- actual open/edit/save acceptance by Microsoft Visio.

## 2. Controlled fixtures

### Canonical source

`spikes/shared/fixtures/canonical-project.json`

The canonical fixture contains fixed IDs, one equipment identity, one representation, one busbar and one connection. It has no host path or timestamp dependency.

### VSDX

`spikes/shared/fixtures/visio/controlled-minimal.vsdx`

Expected SHA-256:

```text
541c036d6ca34971d4470c7d4523f4eee83f80c31c2de5effea220837b463af2
```

It is deterministically generated from the canonical fixture and retained as the exact artifact for the Microsoft Visio manual protocol.

### VSSX

`controlled-master.vssx` is generated in CI from versioned package/XML source rather than uploaded as an opaque binary.

Expected SHA-256:

```text
93cca0049e9393d6f221469ad1653277944e9567c43dd7458296896bd516a02d
```

The generated stencil contains a controlled master, ShapeSheet dimensions and a connection row. CI validates it and packages the same generated artifact with both desktop candidates.

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
- controlled page content.

Stencil requirements include:

- the common document/core package parts;
- masters collection and relationships;
- controlled master content.

Package validation is intentionally fail-closed for missing required parts and malformed XML. It is necessary evidence but is not equivalent to Microsoft Visio acceptance.

## 5. Minimal VSDX write path

`generate-vsdx` reads the controlled canonical JSON and generates an OPC package with:

- deterministic part ordering;
- fixed ZIP timestamps/permissions;
- project title metadata;
- equipment designation as source/Shape Data text;
- one busbar shape;
- one connector and connection records;
- reproducible byte output.

The current writer is a spike proof, not the production exporter. It supports only the controlled fixture and must not be generalized into a compatibility claim.

## 6. Source/provenance ownership

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

## 7. Microsoft Visio gate

State:

```text
OWNER_OR_WINDOWS_VISIO_EVIDENCE_REQUIRED
```

Protocol:

`spikes/evidence/VISIO_MANUAL_ACCEPTANCE_PROTOCOL.md`

The gate requires a supported Microsoft Visio desktop build on Windows to:

1. verify artifact SHA;
2. open without repair dialog;
3. show and permit editing of the controlled shapes/text/Shape Data;
4. save a modified copy;
5. reopen and preserve the modification;
6. retain screenshots, exact Visio/Windows build information and the edited artifact.

Until this is run, the spike may state only that the package is reproducible and structurally validated. It may not state that Microsoft Visio accepts or edits it.

## 8. Legacy VSD/VSS strategy

Binary `.vsd/.vss` support is not implemented in this spike. The recommended evidence-driven strategy is:

1. inventory actual customer prevalence and versions;
2. prefer one-time conversion in Microsoft Visio or an explicitly evaluated local converter when legal/operationally available;
3. preserve original binary file digest and conversion provenance;
4. import only the converted VSDX/VSSX through the controlled profile;
5. report unsupported/lost features explicitly;
6. do not embed Microsoft Visio automation as a normal runtime dependency unless a later ADR proves it is required for a defined legacy bridge.

Legacy support must not silently broaden the native document model or postpone loss reporting.

## 9. Production follow-up

`CANONICAL-DOCUMENT-CORE-001` reserves provenance, mapping-version, diagnostics and foreign-payload boundaries but does not implement the full Visio pipeline.

A later Visio-source-pipeline work item must add:

- relationship-safe OPC traversal;
- ShapeSheet support matrix and formula evaluator policy;
- group/transform/text/connection fidelity fixtures;
- content-addressed real-corpus evidence;
- explicit supported-subset profiles;
- review/promotion flow for VSSX masters;
- import/export no-silent-loss reports;
- real Microsoft Visio open/edit/save acceptance.

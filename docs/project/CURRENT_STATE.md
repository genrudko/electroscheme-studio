# Current State — ElectroScheme Studio

Дата среза: 2026-08-12  
Статус: `DESKTOP-PLATFORM-AND-CORE-SPIKE-001` — `ACCEPTANCE_CANDIDATE / OWNER_MANUAL_GATES_PENDING`

## 1. Canonical GitHub state

- repository: `genrudko/electroscheme-studio`;
- default branch: `main`;
- accepted refoundation PR: #2;
- accepted merge/base commit: `b95d7111d9c5a36db4c355ee91f742efea8ecc10`;
- active issue: #3 `DESKTOP-PLATFORM-AND-CORE-SPIKE-001`;
- active branch: `architecture/desktop-platform-and-core-spike-001`;
- active PR: Draft PR #4;
- PR must remain Draft and unmerged until explicit owner command.

Exact head, ahead/behind, changed-file count, workflow run IDs and artifact IDs/digests are volatile GitHub metadata. Read them from Draft PR #4 and GitHub Actions before acceptance; do not create a self-referential exact-head loop in committed documentation.

At the 2026-08-12 repair-evidence snapshot the branch is `behind_by: 0`. Final acceptance still requires the same condition on the documentation-inclusive exact head.

## 2. Product direction

ElectroScheme Studio is a standalone, desktop-first and local-first Windows/Linux engineering application.

The first complete product vertical remains a normal single-line power-engineering scheme workflow with typed equipment, ports, topology, operating-state semantics, Russian normative profiles and a mandatory Visio migration/exchange bridge.

It is not:

- an EOD module;
- a browser-only service;
- a universal CAD;
- an ETAP/PowerFactory calculation replacement;
- a replacement for every EPLAN discipline;
- a SCADA system.

## 3. Architecture decisions prepared for owner acceptance

### Canonical core

ADR-0003 establishes:

- one pure TypeScript canonical document core;
- one authoritative writable project/document path;
- typed commands/transactions and deterministic serialization;
- Vue/SVG as projection and command source, not state owner;
- FastAPI excluded from packaged desktop runtime;
- Python Visio tooling isolated behind a versioned process protocol.

### Desktop host

ADR-0004 selects **Tauri 2** as the architecture candidate for owner acceptance.

Target composition:

```text
Tauri 2 host / Rust platform adapters
+ Vue 3 / TypeScript / SVG editor composition
+ pure TypeScript canonical document core
+ bounded Python Visio tooling process
```

The host recommendation is evidence-based and remains pending explicit owner acceptance of Draft PR #4.

Qt remains `NOT_ADMITTED_TO_FULL_SPIKE`.

## 4. 2026-08-12 Save and VSDX repair evidence

Manual Windows testing of the previous Tauri artifact exposed a real regression that automation had not proved:

- previous exact head: `9a99545694717007a5e4b20f2f72e903082e2af1`;
- **Save result: FAIL** — pressing Save did not show a native Windows Save dialog;
- PDF native save on the same owner environment worked;
- therefore prior automated scenario success was not accepted as native-dialog evidence.

Repository repair was then restored at source level:

- JSON Save and PDF now share one Rust `native_save_bytes` helper;
- the helper receives the current Tauri `WebviewWindow` as native-dialog parent;
- JSON is passed to the helper as bytes, the same way as PDF;
- cancellation remains a non-error and is surfaced in the UI as `save cancelled`;
- write/invoke failures are surfaced in the UI as `save failed: <diagnostic>`;
- no fixed-path or silent-save workaround was introduced.

The same repair also restores the VSDX generator/validator/test boundary:

- explicit OPC relationship graph `package -> document -> pages -> page`;
- `Page/Rel` relationship ownership rather than the previously invalid inline relationship shape;
- correct PageSheet ownership;
- controlled 1-D connector cells `BeginX/BeginY/EndX/EndY`;
- relationship/content-type checks and dangling-relationship rejection;
- negative regression fixture for the previously false-green VSDX structure;
- deterministic VSDX/VSSX generation.

Repair-evidence Desktop Platform Spike run `31603119700` completed successfully on repair head `5032bbda0e947465c54c3ca62dc70d7b7237de40`:

- `shared-contracts` — SUCCESS;
- `candidate-build (ubuntu-22.04)` — SUCCESS;
- `candidate-build (windows-2022)` — SUCCESS;
- `comparative-evidence` — SUCCESS;
- repaired Tauri compiled on Windows and Linux;
- packaged/restored Tauri scenario passed on Windows and Linux;
- Windows native Save dialog itself remains intentionally outside the automated claim.

Repair-evidence selected-Tauri measurements:

| Platform | Archive | Unpacked | Startup-to-ready | Process-tree RSS |
|---|---:|---:|---:|---:|
| Windows | ~2.53 MB | ~8.75 MB | ~494.0 ms | ~277.2 MB |
| Linux | ~4.21 MB | ~15.93 MB | ~30.32 s | ~410.3 MB |

The Linux startup value remains an explicit hosted-Xvfb anomaly/risk and is not a production performance claim.

## 5. Automated platform evidence boundary

The automated evidence contract has been achieved on the repair code state:

- canonical document read and deterministic round trip;
- structured clipboard round trip;
- deterministic PDF output;
- controlled VSDX read;
- controlled VSSX read;
- minimal VSDX generation;
- generated VSDX package reinspection;
- deterministic archive/package-root execution;
- artifact archive restore verification;
- npm/Cargo lock equality and immutability checks;
- zero-result all-dependency and production-only npm audits.

The repaired controlled/generated VSDX SHA-256 is:

```text
37af1404c342757d8641d3faa43a472d5559c821c0057647a7f33a226dad2664
```

The repaired controlled VSSX SHA-256 is:

```text
4184ec60635d67b6aa653cf2dd6f83ec0a34f4146668a3df6d8eb3927712b4f8
```

Automated evidence does **not** prove real native-dialog visibility, real OS drag/drop, independent cross-application clipboard lifetime, printer-driver behavior or Microsoft Visio edit/save/reopen.

The final documentation-inclusive exact head must repeat all applicable automated gates before owner acceptance.

## 6. Candidate result

### Tauri

Automated packaged scenario:

- Windows — PASS;
- Linux — PASS.

Decision remains: Tauri 2 is the selected architecture candidate, not yet an accepted/merged architecture.

### Electron

- Linux secure packaged scenario — PASS;
- Windows secure packaged scenario — `FAIL_SECURE_NATIVE_STARTUP`;
- Windows packaged process exits with native `0x80000003` before renderer evidence.

Electron remains valid comparison evidence but is not the selected product host.

Full comparison: `docs/architecture/spikes/DESKTOP_PLATFORM_COMPARISON.md`.

## 7. Reproducibility and security state

Canonical dependency inputs:

- `spikes/package-lock.json`;
- `spikes/tauri/src-tauri/Cargo.lock`.

Required workflow behavior remains:

- `npm ci --ignore-scripts`;
- Cargo metadata with `--locked`;
- Tauri build with locked Cargo resolution;
- zero-result all-dependency and production-only npm audits;
- build failure if committed locks or neutral icon resources change;
- LF policy for lockfiles across Windows/Linux checkout;
- artifact manifests contain lock SHA-256 values and exact toolchain versions.

The former Vite high-severity finding remains repaired by the exact update `7.1.1 -> 7.3.6` without `npm audit fix --force`.

## 8. Canonical core and prototype state

The spike proves:

- stable project/document/sheet/layer/equipment/representation/object/port/connection identities;
- equipment identity separated from diagram representation;
- command-only move/snap plus undo/redo;
- deterministic JSON/SVG/PDF;
- host-independent TypeScript core;
- typed platform ports;
- explicit source/provenance/import-mapping/diagnostic boundaries.

The pre-refoundation application remains quarantined engineering research.

Default dispositions remain:

| Area | Disposition |
|---|---|
| UI/CSS | `reimplement_from_contract` |
| Interaction/state code | `reimplement_from_contract` |
| Writable document models | `reimplement_from_contract` |
| VSDX/VSSX source data | `retain_as_reference` |
| Tested ShapeSheet extraction | `salvage_after_tests` |
| Generated symbol drafts | `salvage_after_tests` |

Canonical inventory and migration mapping:

- `docs/architecture/spikes/PROTOTYPE_ASSET_INVENTORY.yaml`;
- `docs/architecture/spikes/PROTOTYPE_MIGRATION_MAP.md`.

## 9. Visio boundary and owner evidence

Automated evidence now validates the repaired relationship-safe controlled package boundary and rejects the previously false-green malformed package class.

Owner evidence already exists for a repaired VSDX artifact with SHA-256:

```text
b9758d3b9f6c96cc761f4ddac31b72cec53d0701f499b4c5242a423663e28784
```

In Microsoft Visio Professional on Windows the owner reported:

- file opened without corruption/repair message;
- `Q-SPK-1` rendered;
- `BUS` rendered;
- connector rendered;
- document appeared visually correct.

This is accepted as positive **open/render** evidence for the repaired VSDX structure. It is not a claim of full arbitrary VSDX compatibility or lossless round trip.

The current deterministic repository fixture has a different content digest (`37af1404...`) after source-level restoration. Therefore the existing owner evidence must not be misrepresented as byte-for-byte validation of the current final artifact. The formal exact-artifact edit/save/reopen protocol remains open.

Production Python packaging is also not complete: the spike currently assumes an available interpreter. End-user installation of Python is not an accepted product runtime dependency.

## 10. Remaining external/manual gates

Two external gate families remain open for owner acceptance:

- `OWNER_OR_WINDOWS_VISIO_EVIDENCE_REQUIRED` — **PARTIAL**: repaired VSDX open/render evidence is positive; exact final artifact edit/save/reopen is still required by the formal protocol;
- `OWNER_OR_INTERACTIVE_RUNNER_EVIDENCE_REQUIRED` — **OPEN**: the previous Windows artifact failed native Save; a new final artifact containing the common parented native-save helper must be retested.

Protocols:

- `spikes/evidence/VISIO_MANUAL_ACCEPTANCE_PROTOCOL.md`;
- `spikes/evidence/DESKTOP_MANUAL_ACCEPTANCE_PROTOCOL.md`.

Both protocols use downloaded exact-run artifacts and require no project build.

## 11. Program state

| Phase | State |
|---|---|
| P0 Project refoundation | `ACCEPTED / MERGED` |
| P1 Market and workflow baseline | `STRATEGIC_INPUT_RECEIVED / HANDS_ON_VALIDATION_PENDING` |
| P2 Desktop/platform/core and Visio-path spike | `ACCEPTANCE_CANDIDATE / OWNER_MANUAL_GATES_PENDING` |
| P3 Canonical document core | `BLOCKED_BY_P2_ACCEPTANCE_AND_MERGE` |
| P4 Editor kernel and design system | `NOT_STARTED` |
| P5 Symbol platform and VSSX migration | `NOT_STARTED` |
| P6 Electrical topology | `NOT_STARTED` |
| P7 Normal single-line MVP and accepted VSDX import | `NOT_STARTED` |
| P8 ГОСТ/СТО profiles and output | `NOT_STARTED` |
| P9 Packaging, Visio export, demo and pilot | `NOT_STARTED` |
| P10 Advanced capabilities | `NOT_STARTED` |

`docs/project/IMPLEMENTATION_PROGRAM.yaml` remains semantically synchronized: P2 is still a candidate, PR #4 is still Draft, Tauri remains the selected candidate, and the same two external/manual gate families remain open. Volatile exact-run metadata remains intentionally outside that YAML.

## 12. Next work item

After owner acceptance and merge of PR #4, the next work item is exactly:

```text
CANONICAL-DOCUMENT-CORE-001
```

Its production boundary is owned by:

`docs/project/CANONICAL_DOCUMENT_CORE_001_SCOPE.md`

Do not begin P3 implementation inside PR #4.

## 13. Acceptance boundary for PR #4

Draft PR #4 is ready for final owner/manual acceptance only when:

- comparison matrix and ADR-0004 are synchronized;
- canonical project/program/next-work-item documentation is synchronized;
- final documentation-inclusive exact head has green CI;
- final documentation-inclusive exact head has green `shared-contracts`, Windows candidate, Linux candidate and `comparative-evidence`;
- all four final evidence artifacts are published;
- final artifact metadata is recorded in PR #4;
- `behind_by: 0`;
- issue #3 remains open;
- PR #4 remains OPEN / DRAFT / NOT MERGED;
- the remaining manual subgates are represented without converting automated IPC/scenario checks into native-UI evidence.

Do not mark Ready for Review or merge without explicit owner command.

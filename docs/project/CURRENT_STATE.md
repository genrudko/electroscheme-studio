# Current State — ElectroScheme Studio

Дата среза: 2026-08-07  
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

At the decision-input snapshot the branch is `behind_by: 0`. Final acceptance still requires the same condition on the documentation-inclusive exact head.

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

## 4. Automated platform evidence

The automated evidence contract has been achieved on the decision-input code state:

- `shared-contracts` — success;
- `candidate-build (ubuntu-22.04)` — success;
- `candidate-build (windows-2022)` — success;
- `comparative-evidence` — success;
- all four required evidence artifacts published;
- artifact archives independently inspected and their SHA-256 values matched the package manifests;
- npm all-dependency and production audit results contain zero vulnerabilities;
- npm/Cargo lock SHA values are equal across the platform evidence;
- candidate package archives are restored before scenario/measurement execution;
- source-tree launches are rejected by the evidence harness.

The final documentation-inclusive exact head must repeat all applicable automated gates before owner acceptance.

## 5. Candidate result

### Tauri

Automated packaged scenario:

- Windows — PASS;
- Linux — PASS.

Proved automatically on both operating systems:

- canonical document read and deterministic round trip;
- structured clipboard round trip;
- deterministic PDF output;
- controlled VSDX read;
- controlled VSSX read;
- minimal VSDX generation;
- generated VSDX package reinspection;
- deterministic archive/package-root execution.

Decision-input hosted-runner measurements:

| Platform | Archive | Unpacked | Startup-to-ready | Process-tree RSS |
|---|---:|---:|---:|---:|
| Windows | ~2.52 MB | ~8.72 MB | ~730.6 ms | ~285.5 MB |
| Linux | ~4.18 MB | ~15.77 MB | ~30.42 s | ~415.1 MB |

The Linux startup value is an explicit anomaly/risk of the hosted Xvfb evidence and is not a production performance claim.

### Electron

- Linux secure packaged scenario — PASS;
- Windows secure packaged scenario — `FAIL_SECURE_NATIVE_STARTUP`;
- Windows packaged process exits with native `0x80000003` before renderer evidence.

Electron remains valid comparison evidence but is not the selected product host.

Decision-input Linux measurements:

- archive ~125.04 MB;
- unpacked ~327.43 MB;
- startup-to-ready ~419.2 ms;
- process-tree RSS ~625.6 MB.

Windows package evidence exists (~143.73 MB archive / ~364.25 MB unpacked), but startup/RSS are not accepted because the secure runtime did not reach renderer-ready.

Full comparison: `docs/architecture/spikes/DESKTOP_PLATFORM_COMPARISON.md`.

## 6. Reproducibility and security state

Canonical dependency inputs:

- `spikes/package-lock.json`;
- `spikes/tauri/src-tauri/Cargo.lock`.

Required workflow behavior:

- `npm ci --ignore-scripts`;
- Cargo metadata with `--locked`;
- Tauri build with locked Cargo resolution;
- zero-result all-dependency and production-only npm audits;
- build failure if committed locks or neutral icon resources change;
- LF policy for lockfiles across Windows/Linux checkout;
- artifact manifests contain lock SHA-256 values and exact toolchain versions.

The former Vite high-severity finding was repaired by the exact update `7.1.1 -> 7.3.6` without `npm audit fix --force`.

## 7. Canonical core and prototype state

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

## 8. Visio boundary

Automated evidence proves a local, deterministic package/tool boundary for:

- controlled VSDX read;
- controlled VSSX read;
- minimal VSDX write;
- generated package reinspection;
- source IDs and structured diagnostics;
- no network dependency.

It does **not** prove that Microsoft Visio desktop accepts, edits and resaves the generated file.

Production Python packaging is also not complete: the spike currently assumes an available interpreter. End-user installation of Python is not an accepted product runtime dependency.

## 9. Remaining external/manual gates

Exactly two external gates are allowed to remain open for owner acceptance:

- `OWNER_OR_WINDOWS_VISIO_EVIDENCE_REQUIRED`;
- `OWNER_OR_INTERACTIVE_RUNNER_EVIDENCE_REQUIRED`.

Protocols:

- `spikes/evidence/VISIO_MANUAL_ACCEPTANCE_PROTOCOL.md`;
- `spikes/evidence/DESKTOP_MANUAL_ACCEPTANCE_PROTOCOL.md`.

Both protocols use downloaded exact-run artifacts and require no project build.

## 10. Program state

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

## 11. Next work item

After owner acceptance and merge of PR #4, the next work item is exactly:

```text
CANONICAL-DOCUMENT-CORE-001
```

Its production boundary is owned by:

`docs/project/CANONICAL_DOCUMENT_CORE_001_SCOPE.md`

Do not begin P3 implementation inside PR #4.

## 12. Acceptance boundary for PR #4

Draft PR #4 is ready for final owner/manual acceptance only when:

- comparison matrix and ADR-0004 are committed;
- canonical project/program/next-work-item documentation is synchronized;
- final documentation-inclusive exact head has green CI;
- final documentation-inclusive exact head has green `shared-contracts`, Windows candidate, Linux candidate and `comparative-evidence`;
- all four final evidence artifacts are published;
- final artifact metadata is recorded in PR #4;
- `behind_by: 0`;
- issue #3 remains open;
- PR #4 remains OPEN / DRAFT / NOT MERGED;
- only the two manual gates above remain open.

Do not mark Ready for Review or merge without explicit owner command.

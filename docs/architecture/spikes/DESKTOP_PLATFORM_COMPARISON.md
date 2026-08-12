# Desktop Platform Comparison — executable spike evidence

Status: `ACCEPTANCE_CANDIDATE / OWNER_MANUAL_GATES_PENDING`  
Work item: `DESKTOP-PLATFORM-AND-CORE-SPIKE-001`

## Decision summary

**Selected architecture candidate: Tauri 2**.

The recommendation is unchanged after the 2026-08-12 Save/VSDX repair and new Windows/Linux evidence. Tauri remains the only candidate in this spike that passes the required packaged runtime scenario on both Windows and Linux while preserving the accepted pure-TypeScript canonical-core boundary.

This remains a recommendation pending explicit owner acceptance of Draft PR #4. It is not a merge decision and does not close native-UI or Microsoft Visio manual gates.

Electron remains comparison/diagnostic evidence. Qt remains `NOT_ADMITTED_TO_FULL_SPIKE`.

## Evidence set used for the repaired decision input

Repair-evidence Desktop Platform Spike:

- workflow run: `31603119700`;
- exact repair head: `5032bbda0e947465c54c3ca62dc70d7b7237de40`;
- base: `b95d7111d9c5a36db4c355ee91f742efea8ecc10`;
- `shared-contracts`: SUCCESS;
- `candidate-build (ubuntu-22.04)`: SUCCESS;
- `candidate-build (windows-2022)`: SUCCESS;
- `comparative-evidence`: SUCCESS.

The final documentation-inclusive exact head is recorded in Draft PR #4 after this document is synchronized and CI reruns. Do not treat the repair-evidence head above as the final volatile PR metadata once documentation changes exist.

Artifact evidence from the repair run:

- `desktop-spike-security-lock-evidence` — ID `9143968791`, GitHub digest `sha256:734f2d916e131ddf705eeb935497dd5509389d3a202fa86c394d5dc1aee8da65`;
- `desktop-spike-Windows-X64` — ID `9144209468`, GitHub digest `sha256:b067079653e2873276a179cc44d25b3dda6b6e84a5935cecaba385dbf36391dd`;
- `desktop-spike-Linux-X64` — ID `9144188571`, GitHub digest `sha256:4305b5fddf296cea076d30d51ca8c3603669128229be0427f615949e1ad342c7`;
- `desktop-spike-comparison-evidence` — ID `9144220383`, GitHub digest `sha256:0c8226b71487b5d7c43d49c0d0c4f1c23b8f67b6b016427088c70d4d6675c90e`.

The platform and comparison artifacts were downloaded and independently inspected after the run. Exact-head, lock SHA, archive SHA, package-root restore and scenario evidence agreed.

## Repaired logical-output and Visio hashes

Passing scenarios on Windows/Linux share:

- canonical JSON SHA-256: `27cecbade2af98d9705e4200b4db5028fceee16e8bfb4a27fe9f7b6e3d8a0092`;
- structured clipboard SHA-256: `85668015e87a5631541344d23add09967ec1816eacb049052564b5fb3e85bd4f`;
- deterministic PDF SHA-256: `3a29985d47486297452c62391f7bc25bc7bf4954f503c3b76c6066ee8002e08f`;
- controlled VSDX SHA-256: `37af1404c342757d8641d3faa43a472d5559c821c0057647a7f33a226dad2664`;
- generated VSDX SHA-256: `37af1404c342757d8641d3faa43a472d5559c821c0057647a7f33a226dad2664`;
- controlled VSSX SHA-256: `4184ec60635d67b6aa653cf2dd6f83ec0a34f4146668a3df6d8eb3927712b4f8`.

## Quantitative comparison

These are one-run GitHub-hosted-runner measurements, not universal benchmarks.

| Platform | Candidate | Archive MB | Unpacked MB | Startup ms | Process-tree RSS MB | Packaged scenario | Restored artifact layout |
|---|---:|---:|---:|---:|---:|---|---|
| Windows | Electron | 143.74 | 364.26 | n/a | n/a | `FAIL_SECURE_NATIVE_STARTUP` | VERIFIED |
| Windows | Tauri | 2.53 | 8.75 | 493.97 | 277.18 | PASS | VERIFIED |
| Linux | Electron | 125.05 | 327.44 | 412.30 | 629.42 | PASS | VERIFIED |
| Linux | Tauri | 4.21 | 15.93 | 30315.21 | 410.35 | PASS | VERIFIED |

Selected Tauri archive verification from the repair run:

- Windows Tauri archive SHA-256: `8f64e6edebecbd628a6ff2a509603a736e41ae9e7cf5642873c72955159ca4e6`;
- Windows unpacked tree SHA-256: `dbf4f241eb0662ee99c6794d2564a046ebed842b49ac5ad338c714d7b49c1ef2`;
- Linux Tauri archive SHA-256: `58d7e2d3367120a043152cead3c138e6e2c2d842bcb1213993588a1850bd86bb`;
- Linux unpacked tree SHA-256: `d932e7e005301369cc0bfdaecec313eb7142958e5ca66eaba640f1d413bde503`.

The repair-run Windows artifact contains:

```text
evidence/generated/tauri-portable-win32-x64/ElectroSchemeSpikeTauri.exe
```

Repair-run EXE SHA-256:

```text
57a132bcb9d7177723a6b6f428410392fa08354fb660f3d3b108609466dac809
```

The final owner test must use the final documentation-inclusive artifact recorded in PR #4, not this intermediate repair-run artifact if the branch head changes.

## Functional/platform comparison

| Criterion | Electron evidence | Tauri evidence | Decision impact |
|---|---|---|---|
| Shared pure-TypeScript canonical core | PASS | PASS | neutral; core remains host-independent |
| Shared Vue/TypeScript/SVG editor projection | PASS where renderer starts | PASS | neutral architecture layer |
| Windows packaged secure runtime | FAIL before renderer (`0x80000003`) | PASS | strong Tauri advantage for this work item |
| Linux packaged secure runtime | PASS | PASS | both viable on Linux |
| Deterministic package archive/restore | VERIFIED | VERIFIED | neutral |
| Package/archive size | large bundled Chromium tree | materially smaller system-webview package | Tauri advantage, not sole decision basis |
| Process-tree RSS | Linux materially higher; Windows no passing measurement | lower than Electron Linux in this run; Windows measured | Tauri advantage in observed run |
| Native dialogs | architecture path exists; Windows candidate did not reach renderer | current host uses `rfd`; real native Save remains manual gate | Tauri path viable, manual evidence still required |
| Clipboard | shared typed port; Linux scenario PASS | shared typed port; Windows/Linux scenario PASS | neutral until cross-app manual test |
| OS drag/drop | adapter exists | adapter exists | manual OS-event evidence required |
| PDF output | deterministic output path exists | deterministic output + native destination path | Tauri path currently stronger; independent viewer/print still manual |
| VSDX/VSSX Python process | bounded process adapter | bounded process adapter | neutral; same protocol |
| Controlled VSDX/VSSX scenario | Linux PASS; Windows never reaches renderer | Windows/Linux PASS | Tauri advantage for required pair |
| Updater/signing path | mature Electron ecosystem | Tauri signed updater/distribution path exists | both viable, implementation deferred |
| Runtime languages | Node/Chromium + TypeScript + Python tool | Rust host + TypeScript core/UI + Python tool | Tauri has more language boundaries but narrower privileged host |
| Dependency/security surface | bundled Chromium/Node runtime is product-owned | system webview + Rust host; smaller packaged dependency surface | Tauri advantage with system-webview trade-off |
| Cross-platform rendering consistency | bundled Chromium improves engine consistency | WebView2 Windows / WebKitGTK Linux diverge | Electron advantage; requires explicit Tauri visual gates |
| CI/build complexity | JS/Electron packaging | Rust/Tauri toolchain + native Linux deps | Electron simpler build stack; Tauri accepted cost |
| Python production packaging | pending | pending | equal follow-up blocker |

## 2026-08-12 native Save regression and repair

Owner manual testing of the previous Windows Tauri artifact (`9a995456...`) found:

```text
Save: FAIL
```

Pressing Save did not show the native Windows Save dialog. PDF save did work in the same owner environment.

This invalidated any prior claim that the automated in-app scenario proved real native Save behavior.

The repair now uses one common Rust helper for JSON Save and PDF:

```text
Save JSON ─┐
           ├──> parented common native save helper -> write bytes
PDF ───────┘
```

Properties of the repair:

- current Tauri `WebviewWindow` is passed as parent to `rfd::FileDialog::set_parent`;
- JSON content is passed as bytes;
- JSON/PDF no longer maintain separate almost-identical save implementations;
- cancel returns a non-error and UI text `save cancelled`;
- write/invoke failure is shown in UI as `save failed: <diagnostic>`.

The new code compiled and ran in packaged scenarios on Windows/Linux in run `31603119700`. This proves source/build/package integration only. It does **not** prove the visible native Save dialog; that remains the explicit owner/interactive gate.

## VSDX/VSSX comparison evidence

The earlier validator had a false-green class: ZIP/XML validity plus a few file checks was not sufficient to prove a structurally valid Visio package.

The repaired writer/validator now verifies:

- package -> document relationship;
- document -> pages relationship;
- pages -> page relationship;
- matching `Page/Rel` ID;
- content types;
- dangling relationships;
- PageSheet ownership;
- controlled 1-D connector endpoint cells;
- deterministic bytes.

Both Windows and Linux packaged Tauri scenarios read controlled VSDX/VSSX, generated the minimal VSDX and reinspected it successfully.

Owner Microsoft Visio Professional evidence is positive for open/render of a prior repaired VSDX SHA `b9758d3b...`, but the final exact-artifact edit/save/reopen subgate remains open. See `docs/architecture/spikes/VISIO_INTEROPERABILITY_SPIKE_REPORT.md`.

## Security and dependency boundary

The repair changed no dependency lock input.

The evidence contract still requires:

- committed `package-lock.json`;
- committed `Cargo.lock`;
- `npm ci --ignore-scripts`;
- Cargo/Tauri locked resolution;
- lock and neutral-icon immutability checks;
- all-dependency and production-only `npm audit` success;
- deterministic package archives with archive SHA and unpacked tree digest;
- exact-head checkout and same-run aggregation.

Repair-evidence lock hashes:

- npm lock SHA-256: `0bd9554bba53000a3d01247979e0b1e2e84c5493b7331fe4e418b59d1d9099eb`;
- Cargo lock SHA-256: `c58ede42a2c003b66d03e17a14af53247929a29f0d8871d5a8f2eb98a8b50cb3`.

## Host recommendation

Tauri 2 remains the recommendation because it gives the best verified combination for this repository:

1. required packaged scenario passes on both mandatory OSes;
2. materially smaller package footprint than Electron;
3. narrower privileged desktop-host boundary;
4. canonical TypeScript core and Vue/SVG remain host-independent;
5. bounded local Python tooling remains viable;
6. Windows failure observed in Electron is not waived;
7. repaired native Save path can use the current Tauri window as the platform-dialog parent without introducing another runtime layer.

This is not an argument that Electron is generally unsuitable for Windows. It is a project decision based on the evidence produced by this exact spike.

## Known Tauri risks / costs

### System webview variance

Windows uses WebView2 and Linux uses WebKitGTK. Cross-platform rendering and interaction are therefore standing product gates.

### Linux hosted-runner startup anomaly

Tauri again measured about 30 seconds on the Linux hosted Xvfb run. This is retained as evidence and requires real interactive Linux remeasurement before any production performance baseline.

### Rust + TypeScript + Python

Three languages are acceptable only with strict ownership:

- Rust: platform/host boundary;
- TypeScript: sole writable canonical/domain/application state;
- Python: bounded Visio extraction/generation tooling.

Schema/domain duplication across languages is forbidden.

### Python sidecar packaging

The spike still assumes an available Python interpreter. Production users must not be required to install/configure Python; a future packaging decision must ship/version/verify the sidecar or remove the runtime dependency.

### Signing/updater

The path is architectural only. Keys, rollback, offline distribution and production updater evidence are deferred.

## Manual acceptance boundary

Automated evidence intentionally leaves:

```text
OWNER_OR_WINDOWS_VISIO_EVIDENCE_REQUIRED
OWNER_OR_INTERACTIVE_RUNNER_EVIDENCE_REQUIRED
```

Current nuance:

- Visio gate: **partial** — repaired-structure open/render owner evidence is positive; final exact-artifact edit/save/reopen remains open;
- interactive desktop gate: **open** — old Windows Save failed; repaired final Windows artifact must prove the native Save dialog, cancel behavior and actual file creation.

The relevant protocols are:

- `spikes/evidence/VISIO_MANUAL_ACCEPTANCE_PROTOCOL.md`;
- `spikes/evidence/DESKTOP_MANUAL_ACCEPTANCE_PROTOCOL.md`.

## Acceptance consequence

The repair evidence strengthens rather than changes the host recommendation. It also narrows what may be claimed:

- Tauri packaged Windows/Linux automation: proven;
- common parented Save implementation: source/build/package proven;
- real native Windows Save dialog after repair: **not yet proven**;
- repaired VSDX structure: automated regression proven;
- Microsoft Visio open/render of prior repaired artifact: owner evidence positive;
- final exact-artifact Visio edit/save/reopen: **not yet proven**.

PR #4 remains Draft until explicit owner action.

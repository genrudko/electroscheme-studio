# Desktop platform comparison — DESKTOP-PLATFORM-AND-CORE-SPIKE-001

Status: `DECISION_INPUT_COMPLETE / OWNER_ACCEPTANCE_PENDING`

## Evidence boundary

This comparison is based on the equivalent packaged candidate scenario and deterministic archive evidence produced by GitHub Actions for the spike code at evidence head `c329f6776bdcce4dae619632b6c0871e59f239c8` (Desktop Platform Spike run `31149632006`).

The values below are comparative evidence for that hosted-runner execution. They are not universal performance benchmarks. Volatile final exact-head run IDs and artifact IDs/digests belong in Draft PR #4 rather than this document.

All four required evidence artifacts were published and independently inspected. Portable archive SHA-256 values matched their package manifests, lock SHA values were identical across Windows/Linux, and the comparison aggregator verified one head/run/lock set.

## Automated comparison

| Area | Tauri 2 candidate | Electron candidate | Decision impact |
|---|---|---|---|
| Windows packaged secure scenario | **PASS** | **FAIL_SECURE_NATIVE_STARTUP** (`0x80000003`) before renderer evidence | decisive advantage Tauri |
| Linux packaged secure scenario | **PASS** | **PASS** | both viable on Linux |
| Windows archive / unpacked | 2.52 MB / 8.72 MB | 143.73 MB / 364.25 MB | strong Tauri footprint advantage |
| Linux archive / unpacked | 4.18 MB / 15.77 MB | 125.04 MB / 327.43 MB | strong Tauri footprint advantage |
| Windows startup-to-ready | ~730.6 ms | unavailable because secure startup fails | Tauri is the only passing Windows measurement |
| Windows process-tree RSS | ~285.5 MB | unavailable because secure startup fails | Tauri is the only passing Windows measurement |
| Linux startup-to-ready | ~30.42 s | ~419.2 ms | material Tauri hosted/Xvfb anomaly; requires interactive remeasurement |
| Linux process-tree RSS | ~415.1 MB | ~625.6 MB | Tauri lower in this run |
| Canonical JSON / SVG / PDF logical hashes | deterministic and cross-platform equal | equal where secure renderer was reached | no semantic disadvantage for Tauri |
| Controlled VSDX read | PASS | PASS on Linux; Windows renderer not reached | Tauri meets selected-host requirement |
| Controlled VSSX read | PASS | PASS on Linux; Windows renderer not reached | Tauri meets selected-host requirement |
| Minimal VSDX generation + reinspection | PASS | PASS on Linux; Windows renderer not reached | Tauri meets selected-host requirement |
| Archive restore / package-root launch | VERIFIED | VERIFIED | both evidence paths are reproducible |
| Renderer security boundary | Tauri webview + Rust command/capability boundary | sandboxed renderer + context-isolated narrow preload | both architecturally acceptable in design |
| Native renderer/runtime | system WebView2/WebKitGTK | bundled Chromium | Electron has stronger engine consistency; Tauri has smaller runtime and system-webview variance risk |
| Canonical core ownership | pure TypeScript, host-independent | pure TypeScript, host-independent | neutral; owned by ADR-0003 |
| Python Visio tooling | supervised local process; production packaging still required | supervised local process; production packaging still required | neutral spike blocker for product packaging |
| Runtime languages | Rust host + TypeScript core/UI + bounded Python tool | TypeScript/Node host/core/UI + bounded Python tool | Tauri has one extra production host language |
| Updater/signing path | Tauri signed updater/distribution path available; not implemented in spike | Windows autoUpdater / Linux package-specific or custom path; not implemented | Tauri gives a more uniform product route, still a later packaging gate |
| Dependency/update surface | Rust/Tauri + system webview + JS build deps | Electron/Chromium/Node + JS deps | Tauri avoids shipping its own Chromium runtime |
| Qt admission | not admitted to full spike; no material advantage was demonstrated | same | Qt remains rejected at admission gate |

## Deterministic evidence

Canonical evidence hashes:

- npm lock: `0bd9554bba53000a3d01247979e0b1e2e84c5493b7331fe4e418b59d1d9099eb`;
- Cargo lock: `c58ede42a2c003b66d03e17a14af53247929a29f0d8871d5a8f2eb98a8b50cb3`;
- canonical JSON: `27cecbade2af98d9705e4200b4db5028fceee16e8bfb4a27fe9f7b6e3d8a0092`;
- deterministic SVG: `c23ed5a5f6f072816eda220fb90f3baf8f2ce0960e362450437da800b7dc8ba4`;
- deterministic PDF: `3a29985d47486297452c62391f7bc25bc7bf4954f503c3b76c6066ee8002e08f`;
- controlled/generated VSDX: `541c036d6ca34971d4470c7d4523f4eee83f80c31c2de5effea220837b463af2`;
- controlled VSSX: `93cca0049e9393d6f221469ad1653277944e9567c43dd7458296896bd516a02d`.

The selected Tauri candidate passed on Windows and Linux from deterministic archives restored inside the job. The Windows Electron artifact was also deterministically packaged and restored, but the secure packaged process exited with native code `0x80000003` before renderer evidence was produced. That failure is retained as negative comparison evidence and is not converted into a pass.

## Recommendation

**Select Tauri 2 as the ElectroScheme Studio desktop host**, subject to owner acceptance of Draft PR #4.

The selected composition is:

```text
Tauri 2 desktop host
+ Rust platform adapters/process supervision
+ Vue 3 / TypeScript / SVG editor composition
+ pure TypeScript canonical document core
+ bounded versioned Python Visio tooling process
```

The recommendation is not based on package size alone. Tauri is the only candidate that completed the secure packaged scenario on both mandatory operating systems, while also preserving the host-independent TypeScript core and producing a materially smaller runtime footprint.

Electron remains useful as comparison evidence and as proof that the shared core/UI are host-independent. It is rejected for the current product architecture because the mandatory Windows secure packaged scenario does not pass on the tested evidence boundary.

Qt remains behind its admission gate because neither Tauri nor the shared TypeScript/SVG architecture exposed a limitation that justifies a Qt rewrite.

## Accepted risks and follow-up boundaries

The host decision does **not** close these product risks:

1. **Linux startup anomaly.** The ~30.4 s Tauri startup on the GitHub/Xvfb environment is not accepted as normal product performance. The interactive Linux acceptance run must record real desktop startup behavior before a production performance baseline is set.
2. **System-webview variance.** Windows uses WebView2 and Linux uses WebKitGTK. Cross-platform visual/interaction acceptance remains mandatory for editor and print work.
3. **Python packaging.** The spike candidate currently uses an external Python interpreter. Production packaging must provide a versioned, verifiable sidecar/tool distribution or remove that external prerequisite; an end-user Python installation is not an accepted product dependency.
4. **Signing/updater.** Tauri signing/updater support is an architecture path, not an implemented release mechanism. Release signing, updater, rollback and offline deployment remain P9/package gates.
5. **Microsoft Visio acceptance.** Structural VSDX validation does not prove Microsoft Visio open/edit/save behavior.
6. **Interactive native integration.** CI does not prove real native dialogs, OS drag/drop, independent clipboard lifetime or printer-driver behavior.

## Remaining acceptance gates

Only external/manual evidence is allowed to remain open for this spike candidate:

- `OWNER_OR_WINDOWS_VISIO_EVIDENCE_REQUIRED`;
- `OWNER_OR_INTERACTIVE_RUNNER_EVIDENCE_REQUIRED`.

The exact no-build procedures are owned by:

- `spikes/evidence/VISIO_MANUAL_ACCEPTANCE_PROTOCOL.md`;
- `spikes/evidence/DESKTOP_MANUAL_ACCEPTANCE_PROTOCOL.md`.

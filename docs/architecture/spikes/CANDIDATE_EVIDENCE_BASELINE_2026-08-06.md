# Desktop Candidate Evidence Baseline — 2026-08-06

Status: preliminary official-source evidence  
Work item: `DESKTOP-PLATFORM-AND-CORE-SPIKE-001`

## 1. Evidence rule

This document records what the frameworks officially support and which risks require executable proof.

It does not select the architecture. Vendor documentation cannot replace the equivalent Windows/Linux scenario, package measurements or Visio interoperability evidence.

Only primary project documentation is used for the baseline below.

## 2. Tauri 2 baseline

### Officially documented capabilities

- Tauri uses a core process and webview processes with IPC routed through the core process.
- IPC uses asynchronous message passing.
- capabilities and permissions can limit which windows/webviews access commands and scoped resources.
- native dialog plugins expose open/save selectors on Windows and Linux.
- external binaries can be packaged as sidecars, including Python tools packaged as executables.
- sidecars use target-specific binary names and must be built for each platform/architecture.
- distribution documentation covers Windows installers and multiple Linux formats.
- Windows packages can bundle WebView2 for offline or controlled-runtime environments.
- the updater supports signed update artifacts and target/architecture-specific endpoints.

### Primary sources

- Core concepts: https://v2.tauri.app/concept/
- Process model: https://v2.tauri.app/concept/process-model/
- IPC: https://v2.tauri.app/concept/inter-process-communication/
- Capabilities: https://v2.tauri.app/security/capabilities/
- Runtime authority: https://v2.tauri.app/security/runtime-authority/
- Sidecars: https://v2.tauri.app/develop/sidecar/
- Plugins: https://v2.tauri.app/plugin/
- Distribution: https://v2.tauri.app/distribute/
- Windows installer/WebView2: https://v2.tauri.app/distribute/windows-installer/
- Updater: https://v2.tauri.app/plugin/updater/

### Preliminary advantages to prove

- smaller host/runtime footprint than a bundled Chromium candidate;
- explicit Rust-side host and permissions boundary;
- suitable local sidecar path for Python VSDX tooling;
- reuse of Vue/TypeScript/SVG renderer without Node access in the UI;
- broad Linux package options.

### Preliminary risks to prove

- rendering and pointer behavior may differ because Windows and Linux use system webview stacks rather than one bundled Chromium version;
- WebView2 availability/bundling policy affects Windows installer size and offline deployment;
- Python sidecar packaging multiplies artifacts by OS/architecture and introduces process lifecycle/versioning concerns;
- Rust plus TypeScript plus Python can create a three-language maintenance boundary;
- printing and PDF behavior must be tested rather than inferred from generic webview capability;
- capability configuration must remain narrow without obstructing file, clipboard and tool workflows.

### Mandatory spike evidence

- identical SVG fixture on Windows WebView2 and selected Linux WebKitGTK environment;
- pointer capture, zoom, drag/drop and clipboard behavior;
- bundled/offline WebView2 decision and artifact-size comparison;
- controlled Python sidecar execution, timeout, cancellation and diagnostics;
- deterministic PDF/output path;
- signed/update and rollback strategy.

## 3. Electron baseline

### Officially documented capabilities

- Electron embeds Chromium and Node.js and supports Windows and Linux from one JavaScript/HTML/CSS codebase.
- applications have a main process and renderer processes.
- privileged functions should be exposed through preload and narrow `contextBridge` APIs.
- context isolation is enabled by default and process sandboxing is a recommended/default boundary in modern Electron.
- official security guidance requires local/trusted content, restrictive CSP, sender validation and current Electron versions.
- native open/save dialogs are available in the main process.
- clipboard access should be performed through main/preload rather than direct renderer access.
- native file drag can be exposed through preload/main IPC.
- `webContents.printToPDF` and system printing APIs exist.
- Electron Forge provides platform-specific makers for Windows and Linux packages.
- built-in `autoUpdater` supports Windows but not Linux; Linux updates normally rely on package managers or an application-specific mechanism.

### Primary sources

- Introduction: https://www.electronjs.org/docs/latest/
- Process model: https://www.electronjs.org/docs/latest/tutorial/process-model
- Context isolation: https://www.electronjs.org/docs/latest/tutorial/context-isolation
- Security checklist: https://www.electronjs.org/docs/latest/tutorial/security
- Dialog: https://www.electronjs.org/docs/latest/api/dialog
- Clipboard: https://www.electronjs.org/docs/latest/api/clipboard
- Native file drag/drop: https://www.electronjs.org/docs/latest/tutorial/native-file-drag-drop/
- Printing/PDF: https://www.electronjs.org/docs/latest/api/web-contents
- Updating: https://www.electronjs.org/docs/latest/tutorial/updates
- autoUpdater: https://www.electronjs.org/docs/latest/api/auto-updater
- Electron Forge: https://www.electronforge.io/
- Makers: https://www.electronforge.io/config/makers

### Preliminary advantages to prove

- one bundled Chromium engine can reduce Windows/Linux rendering variance;
- Vue/TypeScript/SVG integration is direct;
- TypeScript can plausibly own the spike core without a Rust bridge;
- Node main/utility processes provide a straightforward local process path for Python tools;
- mature desktop APIs and automation ecosystem.

### Preliminary risks to prove

- runtime/package and idle-memory overhead;
- Chromium, Node.js and Electron security/update cadence becomes product maintenance responsibility;
- an unsafe or broad preload bridge would violate the adapter and least-privilege contract;
- Electron API access is moving away from renderer use, so all privileged flows require deliberate main/preload ownership;
- Linux has no built-in Electron autoUpdater path;
- packaging targets and signing requirements differ by platform and may require platform-native builders;
- NPM dependency surface must be tightly controlled.

### Mandatory spike evidence

- sandboxed renderer with context isolation and restrictive CSP;
- typed narrow preload API corresponding only to accepted platform ports;
- package size, idle memory and startup measurements;
- same SVG fixture and pointer behavior on Windows/Linux;
- Python tool process lifecycle and cancellation;
- Windows and Linux package/update/rollback strategy;
- exact dependency and vulnerability-management burden.

## 4. Qt preliminary admission threshold

### Officially documented capabilities

- Qt 6 provides mature Windows support and platform deployment tools such as `windeployqt`.
- Windows deployment collects Qt libraries, plugins, QML modules and runtime dependencies.
- Linux and Windows deployment have platform-specific dependencies and packaging requirements.
- Qt is dual-licensed; proprietary distribution requires either a commercial license or compliance with applicable LGPL/GPL terms.
- Qt WebEngine embeds Chromium and introduces additional distribution and licensing considerations.

### Primary sources

- Qt licensing: https://doc.qt.io/qt-6/licensing.html
- Deployment overview: https://doc.qt.io/qt-6/deployment.html
- Windows support: https://doc.qt.io/qt-6/windows.html
- Windows deployment: https://doc.qt.io/qt-6/windows-deployment.html
- Qt WebEngine licensing: https://doc.qt.io/qt-6/qtwebengine-licensing.html

### Admission rule

Qt is admitted to the full equivalent spike only if a short executable/preliminary note demonstrates a material advantage in at least one decisive area:

- editor performance or predictable rendering for the accepted large SVG/scene fixture;
- print/PDF fidelity;
- native integration impossible or materially weaker in both Tauri and Electron;
- simpler canonical core and packaging boundary despite the required port;
- materially lower long-term risk for Windows/Linux support.

The following are not sufficient reasons:

- “native is always better”;
- personal framework preference;
- theoretical lower overhead without measurements;
- UI aesthetics;
- avoiding Rust while introducing a larger Python/C++/QML rewrite.

### Preliminary risks

- the existing Vue/TypeScript/SVG research would require a large port or Qt WebEngine, which reduces the reason to choose Qt;
- Qt Widgets/QGraphics/QML alternatives create substantially different editor implementations, making equivalent comparison more expensive;
- licensing and module selection must be resolved before a proprietary distribution decision;
- Qt WebEngine still embeds Chromium and may combine a large runtime with a full UI rewrite.

## 5. Initial comparison hypotheses

These are hypotheses, not decisions:

| Topic | Tauri hypothesis | Electron hypothesis | Qt hypothesis |
|---|---|---|---|
| Existing Vue/SVG reuse | strong | strong | weak unless WebEngine |
| Cross-platform render consistency | webview-dependent risk | likely strongest | implementation-dependent |
| Package/runtime size | likely smallest host | likely largest | variable |
| Core language simplicity | Rust/TS split risk | TypeScript candidate | Python/C++/QML split risk |
| Python VSDX tooling | packaged sidecar | child/utility process | direct Python only in Qt/Python candidate |
| Security boundary | capabilities + Rust commands | sandbox + narrow preload | native/module-specific |
| Linux updates | Tauri updater/package options to verify | package manager/custom path | package-specific/custom path |
| Print/PDF | must prove | documented APIs, still must prove | potentially strong, must prove |
| Maintenance burden | Rust + TS + Python | TS + Node + Python | likely highest port cost |

## 6. First evidence decision

Both Tauri and Electron remain full candidates.

Qt is provisionally held at the admission-gate stage. No evidence currently justifies paying the full rewrite/comparison cost before the Tauri/Electron shared fixtures exist.

This is not a final rejection. The decision must be revisited if the shared fixtures expose a decisive limitation in both webview-based candidates.

## 7. Immediate implementation consequences

1. Shared core/fixture code must not import Tauri or Electron APIs.
2. Candidate adapters must implement the same typed ports.
3. Vue/SVG rendering fixture must be identical.
4. Python VSDX helper protocol must be process-neutral and versioned.
5. Security configuration is part of acceptance, not a later hardening task.
6. Windows and Linux packaging must run from reproducible platform-specific CI jobs.
7. No final selection occurs before measurement and Visio-open evidence.
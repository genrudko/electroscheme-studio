# ADR-0004: Tauri desktop host and runtime boundaries

- Status: proposed by executable spike; pending owner acceptance of Draft PR #4
- Date: 2026-08-07
- Work item: `DESKTOP-PLATFORM-AND-CORE-SPIKE-001`
- Depends on: ADR-0003 canonical document core and tool boundaries

## Context

ElectroScheme Studio requires one maintainable desktop host for Windows and Linux while preserving:

- a host-independent TypeScript canonical document core;
- Vue/TypeScript/SVG as the editor composition/rendering layer;
- local-first operation;
- native filesystem/dialog/clipboard/drag-drop/print integration behind typed ports;
- bounded local Python VSDX/VSSX tooling;
- deterministic Windows/Linux project behavior;
- no inheritance of the quarantined prototype's writable state ownership.

The spike implemented equivalent Tauri and Electron candidates using the same canonical fixture, shared UI, platform-port contracts, package/archive contract and Visio tool protocol.

Qt was held behind a material-advantage admission gate and did not demonstrate evidence sufficient to justify a full rewrite.

## Decision

Select **Tauri 2** as the target desktop host for ElectroScheme Studio.

The production architecture direction is:

```text
Tauri 2 host
  ├─ window/lifecycle
  ├─ filesystem and native dialog adapters
  ├─ clipboard and drag/drop adapters
  ├─ print/export destination adapters
  ├─ updater/signing hooks
  └─ supervised external tool/process adapter

Vue 3 / TypeScript / SVG
  └─ editor composition and non-authoritative rendering

Pure TypeScript canonical document core
  └─ sole writable engineering document owner

Python Visio tooling
  └─ bounded versioned process protocol; never a second document owner
```

Rust owns only host/platform responsibilities that require the Tauri boundary. It does not own the canonical engineering schema, domain commands or editor state.

ADR-0003 remains authoritative for the canonical core and Python tool boundary.

## Evidence

The decision input is documented in `docs/architecture/spikes/DESKTOP_PLATFORM_COMPARISON.md`.

The executable evidence demonstrated:

- Tauri secure packaged scenario: PASS on Windows and Linux;
- Tauri deterministic archive restore and package-root launch: VERIFIED on Windows and Linux;
- Tauri controlled VSDX/VSSX read and minimal VSDX generation: PASS on Windows and Linux;
- deterministic canonical JSON/SVG/PDF logical output across passing candidate/platform scenarios;
- materially smaller Tauri archives and unpacked package trees than Electron;
- lower Tauri process-tree RSS than Electron on the Linux evidence run;
- Electron Linux secure packaged scenario: PASS;
- Electron Windows secure packaged scenario: FAIL before renderer evidence with native exit `0x80000003`.

The Electron Windows failure is not treated as proof that Electron is generally unusable on Windows. It is sufficient to reject Electron for this work item because the mandatory secure packaged Windows acceptance scenario did not pass while Tauri did.

## Post-manual repair evidence — 2026-08-12

Owner manual testing exposed an important limitation in the earlier automated evidence boundary.

On the previous Windows Tauri artifact from head `9a99545694717007a5e4b20f2f72e903082e2af1`:

```text
Save: FAIL
```

Pressing **Save** did not show a native Windows Save dialog, while the PDF native save path worked on the same machine. Therefore successful command/IPC scenarios were not accepted as evidence of real native-dialog behavior.

The repository repair now makes JSON Save and PDF use one common Rust native-save helper. The current Tauri `WebviewWindow` is supplied to `rfd::FileDialog::set_parent(...)`, JSON is passed as bytes, cancellation remains non-error, and write failures are surfaced as `save failed: <diagnostic>`.

Repair-evidence Desktop Platform Spike run `31603119700` on head `5032bbda0e947465c54c3ca62dc70d7b7237de40` completed successfully on Windows and Linux, including Tauri compilation, deterministic packaging/archive restore and packaged in-app scenarios.

This is source/build/package evidence for the repaired path. It is **not** a claim that the visible Windows Save dialog now works. The final exact Windows artifact still requires owner/interactive verification under `OWNER_OR_INTERACTIVE_RUNNER_EVIDENCE_REQUIRED`.

The same repair restored stricter relationship-aware VSDX generation/validation and negative regressions for the previously false-green malformed package class. Owner Microsoft Visio Professional evidence is positive for open/render of a prior repaired VSDX artifact (`b9758d3b9f6c96cc761f4ddac31b72cec53d0701f499b4c5242a423663e28784`). The reconstructed deterministic GitHub fixture has SHA-256 `37af1404c342757d8641d3faa43a472d5559c821c0057647a7f33a226dad2664`, so exact-artifact Visio edit/save/reopen remains an open manual subgate rather than being inferred from the earlier artifact.

These findings do not reverse the host recommendation. They strengthen the requirement that native UI and Microsoft Visio behavior remain explicit manual gates instead of being inferred from automated IPC/package checks.

## Why Tauri

Tauri is selected because it satisfies the mandatory platform scenario on both operating systems and provides the stronger overall product boundary for this repository:

1. one passing host across Windows and Linux;
2. very small host/package footprint relative to bundled Chromium;
3. explicit Rust-side native/process boundary;
4. no need to place Node.js privileges in the renderer;
5. compatibility with the accepted pure TypeScript core and Vue/SVG editor;
6. viable signed updater/distribution path for later production work;
7. viable local sidecar/process path for Visio tooling.

Package size alone is not the deciding factor.

## Known costs and constraints

### System webviews

Tauri does not provide one identical bundled rendering engine on every OS.

- Windows depends on WebView2;
- Linux depends on WebKitGTK.

Therefore cross-platform visual, interaction and print evidence remains a standing quality requirement. The host choice must not be used to waive Windows/Linux acceptance.

### Linux startup evidence

The hosted Linux/Xvfb run measured about 30 seconds from process start to renderer-ready, much slower than the Electron Linux candidate.

This is recorded as a real spike anomaly, not normalized away and not treated as a universal Tauri characteristic. It requires remeasurement on an interactive Linux desktop before a production performance baseline is accepted.

### Three-language boundary

The selected product can contain:

- Rust for desktop host/platform adapters;
- TypeScript for canonical core, application/editor and Vue/SVG;
- Python for bounded Visio tooling.

This is accepted only because ownership is explicit. Cross-language duplication of canonical schema/domain state is forbidden.

### Python runtime packaging

The spike proves process supervision but currently relies on an available Python interpreter.

Production packages must not require users to install/configure Python. A later packaging/tooling work item must either:

- ship a versioned/verifiable platform-specific sidecar; or
- replace the relevant Python runtime dependency.

This is a release/packaging blocker, not a reason to move the canonical core to Python or Rust.

### Signing/updater

Tauri's updater/signing path is selected as the architecture direction, not implemented by this spike. Signing keys, update artifacts, rollback and offline deployment are separate production gates.

## Electron disposition

Electron is rejected as the production host for the current architecture decision.

Reasons:

- mandatory Windows secure packaged scenario did not reach renderer evidence;
- substantially larger package/runtime footprint;
- bundled Chromium/Node update cadence becomes product maintenance responsibility;
- Linux updater path is less uniform.

What is retained from the Electron candidate:

- evidence that the shared TypeScript core/UI are host-independent;
- security-boundary lessons for privileged adapters;
- Linux comparison measurements;
- diagnostic history.

No Electron host code is promoted automatically into production packages.

## Qt disposition

Qt remains `NOT_ADMITTED_TO_FULL_SPIKE`.

No evidence demonstrated a material advantage in editor capability, print fidelity, native integration or long-term platform risk sufficient to justify replacing the accepted Vue/TypeScript/SVG direction.

Qt may be reconsidered only by a future ADR backed by a concrete blocker in the selected architecture.

## Platform-port rule

Product/application packages may depend only on typed platform ports. Direct Tauri imports are limited to the desktop host/adapter layer.

Forbidden:

- Tauri commands defining domain mutations;
- Rust becoming a second canonical document owner;
- Vue components invoking unrestricted native APIs;
- Python tools writing authoritative project state;
- host-specific paths or APIs inside `canonical-document-core`.

## Consequences

Positive:

- desktop-host decision is closed before production core implementation;
- one selected host passes both mandatory OS automated scenarios;
- canonical core stays independently testable and replaceable;
- native privileges remain behind a narrow host boundary;
- prototype FastAPI runtime is not required;
- future packaging/updater work has a defined target.

Costs:

- Rust toolchain becomes part of desktop-host development;
- system-webview behavior requires explicit cross-platform testing;
- Python tool packaging remains to be industrialized;
- Linux startup anomaly must be investigated on real interactive evidence.

## Acceptance boundary

This ADR becomes accepted only with explicit owner acceptance of Draft PR #4.

Before merge, all automatable gates must be green on one final documentation-inclusive exact head. The only permitted open gate families are:

- `OWNER_OR_WINDOWS_VISIO_EVIDENCE_REQUIRED` — currently partial because open/render evidence exists while exact-artifact edit/save/reopen remains open;
- `OWNER_OR_INTERACTIVE_RUNNER_EVIDENCE_REQUIRED` — currently open and must include a real retest of the repaired native Save dialog.

Ready for Review and merge remain owner-only actions.

# Desktop platform manual acceptance protocol

Status: `OWNER_OR_INTERACTIVE_RUNNER_EVIDENCE_REQUIRED`  
Selected host candidate: `Tauri 2`

This protocol validates the remaining real-desktop behavior of the selected Tauri candidate. Automated CI already proves packaged canonical-file, structured-clipboard, deterministic-PDF, Python-tool and VSDX/VSSX scenarios. It does not prove native dialogs, real OS drag/drop, independent clipboard applications or printer-driver behavior.

No project build is required.

## 1. Select exact artifacts

Use only the final Windows and Linux artifacts recorded in Draft PR #4:

- `desktop-spike-Windows-X64`;
- `desktop-spike-Linux-X64`.

For each artifact:

1. Record workflow run ID, exact head, artifact ID/name and GitHub digest from PR #4.
2. Extract the outer GitHub artifact ZIP into a new temporary directory.
3. Open `evidence/generated/measurements-windows.json` or `measurements-linux.json`.
4. Confirm `workflow_run_id`, `exact_head`, artifact name and lock SHA values match PR #4.
5. Open `evidence/generated/tauri-package-manifest-windows.json` or `tauri-package-manifest-linux.json`.
6. Confirm `artifact_layout_round_trip_verified: true`.
7. Verify the authoritative Tauri archive SHA-256 against `archive_sha256` in the manifest.

Windows:

```powershell
Get-FileHash .\evidence\generated\archives\tauri-windows-x64.tar.gz -Algorithm SHA256
```

Linux:

```bash
sha256sum evidence/generated/archives/tauri-linux-x64.tar.gz
```

8. Extract the verified `tar.gz` into a separate empty directory. Do not launch from source checkout, `node_modules`, Cargo `target` or CI staging directories.

Current spike runtime prerequisites:

- Python 3.13 available as `python` on Windows and `python3` on Linux;
- WebView2 available on Windows;
- WebKitGTK 4.1 runtime libraries available on Linux.

These are spike prerequisites, not accepted production packaging requirements. Missing prerequisites are recorded as `FAILED_WITH_EVIDENCE`; do not rebuild or silently alter the package.

## 2. Launch paths

Launch only from the extracted Tauri archive:

| Platform | Executable |
|---|---|
| Windows | `tauri-portable-win32-x64\ElectroSchemeSpikeTauri.exe` |
| Linux | `tauri-portable-linux-x64/ElectroSchemeSpikeTauri` |

Record:

- OS version;
- runtime prerequisites;
- time from launch to usable editor-ready state;
- whether any security/runtime warning appears.

The Linux timing is especially important because hosted/Xvfb evidence showed a ~30 s startup anomaly. Record the real interactive result rather than assuming the CI value is representative.

## 3. Native open/save dialogs

On each OS:

1. Launch Tauri.
2. Select **Save**.
3. Confirm a platform-native save dialog appears, defaults to `desktop-platform-spike.esspike.json`, filters JSON and permits cancellation without creating a file.
4. Save to a non-repository temporary directory.
5. Select **Open**, choose the saved file and confirm the editor returns to ready without semantic/visual change.
6. Compare the saved file with packaged `fixtures/canonical-project.json` after deterministic normalization.
7. Preserve screenshot/video, saved path and SHA-256.

## 4. Native file drag/drop

1. Drag the saved canonical JSON from the OS file manager into the SVG sheet.
2. Confirm exactly one drop is handled and the project opens.
3. Cancel a second drag and confirm no file is opened.
4. Drop invalid JSON and confirm a visible error without replacing the current project.
5. Preserve video and diagnostics.

## 5. Structured clipboard across applications

1. Select the test figure and use **Copy**.
2. Paste into an independent plain-text editor and preserve the versioned JSON payload.
3. Copy that payload back and use **Paste** in Tauri.
4. Confirm it is accepted as structured editor data and does not become arbitrary SVG/DOM state.
5. Repeat after closing/reopening the app to observe OS clipboard lifetime.
6. Preserve payload and SHA-256.

## 6. PDF and print boundary

1. Select **PDF** and save through the native dialog.
2. Open the PDF in an independent viewer.
3. Confirm it opens without repair warning and contains expected title/content.
4. Invoke the available platform print path and print through the OS PDF printer where available.
5. Record viewer, OS, printer-driver versions and output SHA-256.

Automated deterministic PDF equality does not prove production typography, pagination or printer-driver compatibility.

## 7. Evidence result

Preserve for each OS:

- exact workflow run/head;
- artifact ID/name/digest;
- Tauri package manifest and archive SHA;
- OS/runtime versions;
- screenshots/video;
- saved JSON/PDF outputs and SHA;
- startup observation;
- result and diagnostics.

Use only:

- `PASSED_WITH_EVIDENCE`;
- `FAILED_WITH_EVIDENCE`;
- `NOT_RUN`.

Electron is not part of the owner manual acceptance protocol because it was rejected by the automated Windows secure-runtime comparison. Do not convert its Linux pass into product-host acceptance.

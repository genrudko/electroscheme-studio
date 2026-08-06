# Desktop platform manual acceptance protocol

Status: `OWNER_OR_INTERACTIVE_RUNNER_EVIDENCE_REQUIRED`

Automated CI exercises canonical files, structured clipboard, deterministic PDF, Python tooling and VSDX/VSSX operations inside packaged Electron and Tauri candidates. Native dialogs, OS drag/drop, independent clipboard applications and printer-driver behavior still require a real interactive desktop.

No project build is required for this protocol.

## 1. Select and verify the exact artifacts

Use only the Windows and Linux artifacts from the workflow run and exact head recorded in Draft PR #4:

- `desktop-spike-Windows-X64`;
- `desktop-spike-Linux-X64`.

For each downloaded GitHub artifact:

1. Record workflow run ID, exact head, artifact ID/name and GitHub artifact digest from PR metadata.
2. Extract the outer GitHub artifact ZIP into a new temporary directory.
3. Open `evidence/generated/measurements-windows.json` or `measurements-linux.json` and confirm its `workflow_run_id`, `exact_head`, artifact name and lock SHA values match PR metadata.
4. For each candidate, open `evidence/generated/<candidate>-package-manifest-<platform>.json`.
5. Verify `artifact_layout_round_trip_verified` is `true`.
6. Verify the portable archive SHA-256:

   Windows PowerShell:

   ```powershell
   Get-FileHash .\evidence\generated\archives\electron-windows-x64.tar.gz -Algorithm SHA256
   Get-FileHash .\evidence\generated\archives\tauri-windows-x64.tar.gz -Algorithm SHA256
   ```

   Linux:

   ```bash
   sha256sum evidence/generated/archives/electron-linux-x64.tar.gz
   sha256sum evidence/generated/archives/tauri-linux-x64.tar.gz
   ```

7. Compare each result with `archive_sha256` in the corresponding package manifest.
8. Extract each verified `tar.gz` into a separate empty directory. The archive, not the surrounding GitHub ZIP, is authoritative for Linux executable modes.

Current spike runtime prerequisites are not build prerequisites:

- Python 3.13 available as `python` on Windows and `python3` on Linux;
- WebView2 available for the Windows Tauri candidate;
- WebKitGTK 4.1 runtime libraries available for the Linux Tauri candidate.

Record missing prerequisites as `FAILED_WITH_EVIDENCE`; do not rebuild or silently modify the package.

## 2. Launch paths

Launch only from the extracted portable archives:

| Platform | Candidate | Executable |
|---|---|---|
| Windows | Electron | `ElectroSchemeSpikeElectron-win32-x64\ElectroSchemeSpikeElectron.exe` |
| Windows | Tauri | `tauri-portable-win32-x64\ElectroSchemeSpikeTauri.exe` |
| Linux | Electron | `ElectroSchemeSpikeElectron-linux-x64/ElectroSchemeSpikeElectron` |
| Linux | Tauri | `tauri-portable-linux-x64/ElectroSchemeSpikeTauri` |

Do not launch from a source checkout, `node_modules`, Cargo `target` directory or CI staging path.

## 3. Native open/save dialogs

For each candidate and OS:

1. Launch the executable listed above.
2. Select **Save**.
3. Confirm a platform-native save dialog appears, defaults to `desktop-platform-spike.esspike.json`, filters JSON files and permits cancellation without creating a file.
4. Save to a non-repository temporary directory.
5. Select **Open**, choose the saved file and confirm the editor returns to `ready` without semantic or visual changes.
6. Compare the saved file with the packaged `fixtures/canonical-project.json` for Tauri or `resources/app.asar.unpacked/shared/fixtures/canonical-project.json` for Electron after deterministic normalization.
7. Record OS version, candidate, artifact ID, screenshot/video, saved path and SHA-256.

## 4. Native file drag/drop

1. Drag the saved canonical JSON file from the OS file manager into the SVG sheet.
2. Confirm exactly one drop event is handled and the project opens.
3. Cancel a second drag and confirm no file is opened.
4. Drop an invalid JSON file and confirm a visible error without replacement of the current project.
5. Record video and application diagnostics.

## 5. Structured clipboard across the application boundary

1. Select the test figure and use **Copy**.
2. Paste into an independent plain-text editor and preserve the versioned JSON payload.
3. Copy that payload back from the text editor and select **Paste**.
4. Confirm it is accepted as structured data and does not become arbitrary SVG/DOM state.
5. Repeat after closing and reopening the candidate to identify platform clipboard-lifetime behavior.
6. Record the clipboard payload and SHA-256.

## 6. PDF and print boundary

1. Select **PDF** and save through the native dialog.
2. Open the PDF in an independent viewer.
3. Confirm it opens without a repair warning and contains the expected title/content.
4. Invoke the candidate's platform print path when available and print through the OS PDF printer.
5. Record viewer, OS and printer-driver versions plus output SHA-256.

The automated deterministic PDF proves logical output equality. It does not prove production typography, pagination or printer-driver compatibility.

## 7. Evidence record

For every candidate/OS pair preserve:

- exact workflow run and head;
- artifact ID/name/digest;
- package manifest and archive SHA-256;
- OS/runtime prerequisites;
- screen recording or screenshots;
- saved canonical JSON and PDF outputs with SHA-256;
- result and observed diagnostics.

Use only:

- `PASSED_WITH_EVIDENCE`;
- `FAILED_WITH_EVIDENCE`;
- `NOT_RUN`.

Do not convert automated package/build success into a manual interaction pass.

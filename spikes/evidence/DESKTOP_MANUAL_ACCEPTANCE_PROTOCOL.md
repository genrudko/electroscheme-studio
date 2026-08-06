# Desktop platform manual acceptance protocol

Status: `OWNER_OR_INTERACTIVE_RUNNER_EVIDENCE_REQUIRED`

Automated CI exercises the same in-app canonical/filesystem/clipboard/PDF/Python/VSDX/VSSX scenario in packaged Electron and Tauri candidates on Windows and Linux. The following interactions are not honestly proven by synthetic IPC calls and require a real desktop session.

Run this protocol for each candidate and OS artifact from the accepted workflow run.

## 1. Native open/save dialogs

1. Launch the packaged candidate.
2. Select **Save**.
3. Confirm the platform-native save dialog appears, defaults to `desktop-platform-spike.esspike.json`, filters JSON files and permits cancellation without creating a file.
4. Save to a non-repository temporary directory.
5. Select **Open**, choose the saved file and confirm the editor returns to `ready` without semantic or visual changes.
6. Compare the saved file byte-for-byte with `shared/fixtures/canonical-project.json` after deterministic normalization.
7. Record OS, artifact name, screenshot/video and saved file SHA-256.

## 2. Native file drag/drop

1. Drag the same canonical JSON file from the OS file manager into the SVG sheet.
2. Confirm exactly one drop event is handled and the project opens.
3. Repeat after cancelling a drag; confirm no file is opened.
4. Drop an invalid JSON file; confirm a visible error and no replacement of the current project.
5. Record video and application diagnostics.

## 3. Structured clipboard across application boundary

1. Select the temporary test figure and use **Copy**.
2. Paste into a plain-text editor and preserve the versioned JSON payload.
3. Copy that payload back from the text editor and select **Paste**.
4. Confirm it is accepted as structured data and does not become arbitrary SVG/DOM state.
5. Record the clipboard payload and SHA-256.

## 4. PDF and print path

1. Select **PDF** and save through the native dialog.
2. Open the PDF in an independent viewer.
3. Confirm the title is present and the file opens without repair.
4. Invoke the candidate's platform print path when available and print to the OS PDF printer.
5. Record viewer/OS versions, output files and SHA-256.

The spike's deterministic PDF fixture proves logical cross-platform output. It does not yet prove production typography, pagination or printer-driver compatibility.

## 5. Result states

Use only:

- `PASSED_WITH_EVIDENCE`;
- `FAILED_WITH_EVIDENCE`;
- `NOT_RUN`.

Do not convert automated package/build success into a manual interaction pass.

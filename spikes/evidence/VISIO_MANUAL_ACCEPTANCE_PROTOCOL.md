# Microsoft Visio manual acceptance protocol

Status: `OWNER_OR_WINDOWS_VISIO_EVIDENCE_REQUIRED`

This protocol validates the controlled input and both VSDX files generated inside packaged Windows candidates. No project build is required.

## 1. Select the exact Windows artifact

Use `desktop-spike-Windows-X64` from the workflow run and exact head recorded in Draft PR #4.

1. Record workflow run ID, exact head, artifact ID/name and GitHub artifact digest.
2. Extract the downloaded GitHub artifact into a new temporary directory.
3. Open `evidence/generated/measurements-windows.json` and confirm the run, head and lock SHA values match PR metadata.
4. Confirm both scenario files have `status: "ok"` and all checks are `true`:
   - `evidence/generated/electron-scenario-windows.json`;
   - `evidence/generated/tauri-scenario-windows.json`.

## 2. Files that must be tested

Test all three files from the extracted artifact:

1. controlled package fixture:
   - `evidence/generated/visio-fixtures/controlled-minimal.vsdx`;
2. generated through packaged Electron:
   - `evidence/generated/electron-generated-minimal.vsdx`;
3. generated through packaged Tauri:
   - `evidence/generated/tauri-generated-minimal.vsdx`.

Do not substitute a source-tree file or regenerate any file locally.

## 3. Verify SHA-256 before opening

For the controlled file, read the expected SHA from `tool_results.vsdx.sha256` in either Windows scenario JSON.

For each generated file, read the expected SHA from both:

- `tool_results.generated.sha256`;
- `tool_results.generatedInspection.sha256`.

The two generated values for the same candidate must agree.

Verify locally:

```powershell
Get-FileHash .\evidence\generated\visio-fixtures\controlled-minimal.vsdx -Algorithm SHA256
Get-FileHash .\evidence\generated\electron-generated-minimal.vsdx -Algorithm SHA256
Get-FileHash .\evidence\generated\tauri-generated-minimal.vsdx -Algorithm SHA256
```

Record any mismatch as `FAILED_WITH_EVIDENCE`; do not open a mismatched file as accepted evidence.

## 4. Microsoft Visio checks

Record Microsoft Visio edition, exact build, Windows version and date.

For each of the three files:

1. Open it in Microsoft Visio desktop on Windows.
2. Confirm it opens without a repair, corruption, blocked-content or compatibility warning.
3. Confirm exactly one expected page opens.
4. Confirm shapes, connector and text are visible and editable.
5. For the controlled fixture, confirm Shape Data/source value `Q-SPK-1` is present.
6. Move one shape, edit its visible text and save as a new VSDX outside the artifact directory.
7. Close Visio completely.
8. Reopen the saved copy and confirm the move and text edit persist without a repair dialog.
9. Preserve before/after screenshots and the edited copy.

A pass for the controlled fixture does not imply a pass for either generated candidate file. Record each separately.

## 5. Evidence record

For every file preserve:

- workflow run, exact head and artifact identity;
- original filename and SHA-256;
- Visio edition/build and Windows version;
- opening result and every warning/dialog;
- screenshot before edit;
- edited copy and SHA-256;
- screenshot after reopen;
- result state.

Use only:

- `PASSED_WITH_EVIDENCE`;
- `FAILED_WITH_EVIDENCE`;
- `NOT_RUN`.

Automated ZIP/XML/package validation is necessary but is not evidence that Microsoft Visio accepted, edited and resaved the file.

# Microsoft Visio manual acceptance protocol

Status: `OWNER_OR_WINDOWS_VISIO_EVIDENCE_REQUIRED`  
Selected host candidate: `Tauri 2`

This protocol validates the controlled VSDX input and VSDX generated through the packaged Tauri Windows candidate. No project build is required.

## 1. Select exact Windows artifact

Use only `desktop-spike-Windows-X64` from the final workflow run/exact head recorded in Draft PR #4.

1. Record workflow run ID, exact head, artifact ID/name and GitHub digest.
2. Extract the GitHub artifact into a new temporary directory.
3. Open `evidence/generated/measurements-windows.json` and confirm run/head/lock SHA values match PR #4.
4. Open `evidence/generated/tauri-scenario-windows.json`.
5. Confirm `status: "ok"` and every scenario check is `true`.
6. Open `evidence/generated/tauri-package-manifest-windows.json` and confirm `artifact_layout_round_trip_verified: true`.

The Electron Windows scenario is intentionally not an input to this protocol: it is retained as negative comparison evidence and did not reach the secure renderer.

## 2. Files to test

Test both files from the extracted artifact:

1. controlled package fixture:
   - `evidence/generated/visio-fixtures/controlled-minimal.vsdx`;
2. generated through packaged Tauri:
   - `evidence/generated/tauri-generated-minimal.vsdx`.

Do not substitute a source-tree file and do not regenerate locally.

The current controlled writer is deterministic, so the two files may be byte-identical. They are still recorded separately because one is the controlled input fixture and one is the output produced through the packaged selected-host process path.

## 3. Verify SHA-256

Expected values come from `evidence/generated/tauri-scenario-windows.json`:

- controlled: `tool_results.vsdx.sha256`;
- generated: both `tool_results.generated.sha256` and `tool_results.generatedInspection.sha256`.

The generated values must agree.

Verify locally:

```powershell
Get-FileHash .\evidence\generated\visio-fixtures\controlled-minimal.vsdx -Algorithm SHA256
Get-FileHash .\evidence\generated\tauri-generated-minimal.vsdx -Algorithm SHA256
```

For the current controlled fixture family, expected SHA-256 is:

```text
541c036d6ca34971d4470c7d4523f4eee83f80c31c2de5effea220837b463af2
```

Any mismatch is `FAILED_WITH_EVIDENCE`; do not accept a mismatched file.

## 4. Microsoft Visio checks

Record Microsoft Visio edition/build, Windows version and date.

For each of the two files:

1. Open it in Microsoft Visio desktop.
2. Confirm no repair, corruption, blocked-content or compatibility warning.
3. Confirm exactly one expected page opens.
4. Confirm shapes, connector and text are visible and editable.
5. Confirm source/Shape Data value `Q-SPK-1` is present where expected.
6. Move one shape, edit visible text and save as a new VSDX outside the artifact directory.
7. Close Visio completely.
8. Reopen the saved copy and confirm the move/text edit persist without a repair dialog.
9. Preserve before/after screenshots and the edited copy.

A pass for the controlled fixture does not automatically substitute for the packaged Tauri output record even if their input bytes are currently identical; preserve both provenance records.

## 5. Evidence result

For each file preserve:

- workflow run/head and artifact identity;
- original filename/SHA;
- Visio edition/build and Windows version;
- opening result and every warning/dialog;
- screenshot before edit;
- edited copy and SHA;
- screenshot after reopen;
- result state.

Use only:

- `PASSED_WITH_EVIDENCE`;
- `FAILED_WITH_EVIDENCE`;
- `NOT_RUN`.

Automated ZIP/XML/package validation is necessary but is not evidence that Microsoft Visio accepted, edited and resaved the file.

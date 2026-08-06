# Microsoft Visio manual acceptance protocol

Status: `OWNER_OR_WINDOWS_VISIO_EVIDENCE_REQUIRED`

Artifact: `spikes/shared/fixtures/visio/controlled-minimal.vsdx`

1. Verify SHA-256 against `SHA256SUMS.txt`.
2. Open the file in a supported Microsoft Visio desktop version on Windows.
3. Record Visio edition, exact build, Windows version and date.
4. Confirm one page opens without a repair dialog.
5. Confirm two shapes, connector, text and Shape Data value `Q-SPK-1` are visible/editable.
6. Move shape `Q-SPK-1`, edit its text, save as a new VSDX and close.
7. Reopen the saved copy and confirm the edit persists.
8. Preserve screenshots and the edited VSDX as GitHub-controlled evidence.

Automated package validation is necessary but is not evidence that Microsoft Visio accepted the file.

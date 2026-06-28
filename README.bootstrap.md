# ElectroScheme Studio Bootstrap

Code name: $ProjectCodeName

This folder was prepared by:

- Patch: $PatchName
- Timestamp: $Timestamp

## Project goal

Local WebUI application for creating interactive electrical schemes with ГОСТ-oriented symbol libraries, smart equipment objects, connection model, and export to PDF/JPEG/SVG.

## Planned stack

### Backend

- Python 3.12+
- FastAPI
- Pydantic
- Uvicorn

### Frontend

- Node.js LTS
- Vue 3
- Vite
- TypeScript
- SVG-based rendering

### Storage

Initial stage:

- open JSON project format

Later stage:

- SQLite project/database storage

### Export

Initial:

- SVG

Later:

- PDF
- PNG/JPEG

## Patch flow

Expected workflow:

1. Apply patch.
2. Send full PowerShell log.
3. Receive next patch or repair patch.

Next expected patch:

`	ext
patch_001_bootstrap_repository.ps1
`

## Notes

This bootstrap patch does not create the application yet.
It prepares the environment and verifies basic tooling.

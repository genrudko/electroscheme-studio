# ElectroScheme Studio

**ElectroScheme Studio** is a local-first WebUI application for creating interactive electrical schemes with ГОСТ-oriented symbol libraries, smart equipment objects, connection topology, validation checks, and export to PDF/JPEG/SVG.

Repository code name: $ProjectCodeName.

## Scope

The project is not intended to replace a full CAD system. The first target is a focused engineering editor:

- SVG-based scheme canvas;
- smart electrical symbols with terminals;
- model-backed connections;
- ГОСТ-oriented visual profiles;
- project JSON format;
- local WebUI;
- PDF/JPEG/SVG export later.

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
- SVG renderer

### Storage

- JSON project format first;
- SQLite later.

## Development workflow

This repository is maintained through PowerShell patch scripts.

Patch directory:

`	ext
C:\1
`

Project directory:

`	ext
G:\electroscheme-studio
`

Typical flow:

1. Apply a patch from C:\1.
2. Review PowerShell output.
3. Send the full log.
4. Continue with the next patch or repair patch.

## Current status

Initial repository bootstrap.

# ADR 0001 — Initial Stack

## Decision

Use:

- Python + FastAPI for backend;
- Vue 3 + Vite + TypeScript for frontend;
- SVG as the primary scheme rendering layer;
- JSON as the initial project storage format.

## Rationale

SVG is a strong fit for engineering diagrams because symbols remain vector, addressable, clickable, and printable.

JSON keeps the early model transparent and patch-friendly.

FastAPI leaves room for validation, export, and future integrations.

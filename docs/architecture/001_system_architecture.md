# System Architecture

## Layers

`	ext
Project JSON
    ↓
Domain model
    ↓
Topology / terminals / connections
    ↓
Layout model
    ↓
SVG renderer
    ↓
WebUI interaction
    ↓
Export pipeline
`

## Backend

The backend owns:

- project loading/saving;
- schema validation;
- example project API;
- future checks;
- future export orchestration.

## Frontend

The frontend owns:

- SVG canvas;
- zoom/pan later;
- selection;
- property panels;
- visual editing later.

## Model principle

The scheme is not the source of truth as a drawing.  
The project model is the source of truth.

A circuit breaker is stored as an equipment/symbol object with terminals and metadata, not as unrelated SVG primitives.

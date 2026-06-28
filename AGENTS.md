# Agent Instructions — ElectroScheme Studio

## Product direction

Build a local-first WebUI application for interactive electrical schemes with ГОСТ-oriented visual language.

The application must be model-backed: symbols are not just drawings; they represent electrical entities with terminals, connections, labels, and metadata.

## Hard boundaries

- Do not add DWG support at this stage.
- Do not implement cloud/multi-user features at this stage.
- Do not claim full ГОСТ/СТО compliance until rules and sources are explicitly encoded.
- Prefer SVG as the source visual representation.
- Prefer JSON project format before SQLite.

## Patch discipline

Each patch must:

- have a numbered name;
- write clear logs;
- be idempotent where practical;
- avoid destructive changes;
- include a status summary;
- keep architecture docs in sync when important decisions change.

## Naming

Product name: ElectroScheme Studio  
Repository/folder name: electroscheme-studio

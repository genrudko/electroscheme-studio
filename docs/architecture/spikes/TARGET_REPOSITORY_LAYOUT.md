# Target repository layout

Status: `PROPOSED_BY_DESKTOP-PLATFORM-AND-CORE-SPIKE-001`  
Scope: architecture target only; no broad repository move is authorized in PR #4.

## Design constraints

The layout must make architectural ownership visible in imports and build boundaries:

- exactly one package owns the writable canonical document;
- Vue components and SVG renderer are projections and cannot own authoritative state;
- desktop capabilities are accessed only through typed ports;
- the selected desktop host implements adapters but does not define domain behavior;
- Python Visio tooling is a bounded external tool, never a second project model;
- imported VSDX/VSSX data and generated symbol drafts remain quarantined until explicit review/promotion;
- the old prototype remains in place until each retirement criterion is accepted.

## Proposed production layout

```text
apps/
  desktop/
    package.json
    src/
      bootstrap/
      composition/
    host/
      selected-host-adapters/
      capabilities/
      updater/
      packaging/

packages/
  canonical-document-core/
    src/
      model/
      invariants/
      commands/
      transactions/
      history/
      serialization/
      migrations/
    fixtures/
    test/

  editor-application/
    src/
      selection/
      interaction-state-machine/
      command-dispatch/
      clipboard/
      drag-drop/
      view-state/
    test/

  editor-geometry/
    src/
      coordinates/
      snapping/
      transforms/
      hit-testing/
    test/

  editor-renderer-svg/
    src/
      projections/
      render-tree/
      svg-output/
    fixtures/
    test/

  platform-ports/
    src/
      filesystem.ts
      dialogs.ts
      clipboard.ts
      drag-drop.ts
      print.ts
      updater.ts
      process-tools.ts

  document-profiles/
    src/
      profile-schema/
      version-resolution/
      validation/

  symbol-source-model/
    src/
      source-identity/
      provenance/
      compatibility-diagnostics/
      opaque-payload/

  visio-tool-protocol/
    src/
      request-response-schema/
      diagnostics/
      process-supervision/

  test-fixtures/
    canonical/
    svg/
    pdf/
    visio/

tools/
  visio-python/
    pyproject.toml
    src/
      package-reader/
      shapesheet-extractor/
      source-normalizer/
      vsdx-writer/
    tests/

  research-api/
    # Optional developer/research facade only; not packaged desktop runtime.

quality/
  schemas/
  changed-scope/
  deterministic-output/
  package-validation/
  cross-platform/

prototype/
  # Logical quarantine target for the current frontend/backend/tools tree.
  # Physical relocation is a later governed work item, not PR #4.

spikes/
  desktop-platform-and-core-001/
    # Accepted evidence retained as architecture history, not imported by production packages.

docs/
  architecture/
  decisions/
  project/
  quality/
```

## Dependency direction

Allowed production dependency direction:

```text
selected desktop host adapters
        -> platform-ports
        -> editor-application
        -> canonical-document-core

Vue composition/UI
        -> editor-application
        -> editor-renderer-svg
        -> canonical-document-core (read-only projections and command types)

visio-tool-protocol
        -> canonical-document-core import/export DTO boundary

Python visio tool
        <-> versioned process protocol
        !-> writable in-memory canonical core
```

Forbidden directions:

- `canonical-document-core -> Vue`, SVG DOM, desktop host, Python, VSDX or CIM;
- `editor-renderer-svg -> filesystem`, native dialogs or updater;
- Vue components mutating document objects directly;
- Python tools writing project files without a validated import/export transaction in the application layer;
- host-specific adapters imported by reusable packages;
- production packages importing code from `prototype/` or `spikes/`.

## Workspace and build ownership

After the architecture decision is accepted:

- the root workspace owns exact JavaScript dependency resolution and task orchestration;
- the selected host owns desktop packaging/signing/updater configuration;
- `canonical-document-core` is independently testable in Node without a browser or host;
- Python tooling has an isolated locked environment and a versioned JSON protocol;
- Windows and Linux build jobs consume the same canonical/editor fixtures;
- generated VSDX/VSSX artifacts are content-addressed and published as evidence, not silently committed from local machines.

## Migration rule

This document is a target map, not permission for a repository-wide move. `CANONICAL-DOCUMENT-CORE-001` may create only the packages required to establish the accepted core and its immediate test fixtures. UI, renderer, platform adapters and prototype relocation remain later work items unless explicitly included by an accepted program amendment.

# Current buildable prototype baseline

This checkpoint accepts the current buildable prototype left after the early coding-agent work and cleanup patches.

## Status

The project has passed the minimal development gates:

- backend compile;
- backend app import;
- frontend production build.

## What is accepted

The current source tree may include a preliminary symbol-library API, frontend symbol components, editor/routing helpers and example project changes.

This is accepted as a buildable prototype baseline, not as final architecture.

## What is not accepted as final truth

The generated symbol library is not considered production-ready.

Known constraints:

- Visio VSDX masters remain the preferred source for symbol geometry.
- Imported symbols must go through `Imported / Needs Review`.
- State handling for switching devices must remain explicit.
- Busbars must become parametric.
- Terminals, snap anchors, rotation, stretching and voltage colorization require proper validation.
- Automatic scheme generation remains a first-class target and must not be blocked by current prototype structure.

## Next development direction

Next patches should stop doing cleanup work and start implementing the real pipeline:

```text
Visio master geometry
→ normalized draft symbols
→ SVG preview
→ reviewed SymbolDefinition
→ editor placement/snap/routing
→ automatic scheme generation
```

## Rule for future agents

Do not overwrite this baseline with generated code unless the gates remain green and the change advances the documented symbol capability requirements.
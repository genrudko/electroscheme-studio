# Patch 033 repair1 — resume after smoke token failure

Patch 033 failed before build/commit because its smoke test searched for the literal token:

```text
Ctrl+C
```

inside `EditorShell.vue`.

The implementation was already present as key handling logic:

```text
event.ctrlKey && key === 'c'
```

This repair adds `shortcutRegistry.ts` so shortcuts have explicit labels for UI/tooltips/docs, and uses a corrected smoke test that checks both:

```text
shortcut registry labels
actual keydown implementation tokens
```

The repair then resumes the backend/frontend gates and commits the full patch 033 working tree.
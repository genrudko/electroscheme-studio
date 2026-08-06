# Executable desktop platform spike

This directory is quarantined evidence for `DESKTOP-PLATFORM-AND-CORE-SPIKE-001`; it is not production application code.

Both candidates use exactly the same TypeScript canonical fixture, command history, deterministic serializer, Vue component and SVG scene. Electron and Tauri implement only platform adapters and lifecycle/security boundaries.

## Local checks

```bash
npm install --ignore-scripts
npm test
python -m unittest tools/test_visio_spike_tool.py -v
npm run build
```

Tauri build additionally requires Rust 1.97.1 and platform prerequisites.

The generated VSDX fixture is package-tested automatically. Opening/editing/saving it in Microsoft Visio remains a separate manual acceptance gate and must not be inferred from ZIP/XML validation.

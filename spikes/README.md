# Executable desktop platform spike

This directory is quarantined evidence for `DESKTOP-PLATFORM-AND-CORE-SPIKE-001`; it is not production application code.

Both candidates use exactly the same TypeScript canonical fixture, command history, deterministic serializer, Vue component and SVG scene. Electron and Tauri implement only platform adapters and lifecycle/security boundaries.

## Local checks

```bash
npm ci --ignore-scripts
npm test
python -m unittest \
  tools/test_visio_spike_tool.py \
  tools/test_archive_candidate.py \
  tools/test_compare_candidate_evidence.py \
  -v
npm run build
```

Tauri build additionally requires Rust 1.97.1, the committed `src-tauri/Cargo.lock`, and platform prerequisites. Candidate evidence uses locked npm and Cargo resolution; dependency lockfiles are canonical repository inputs rather than CI-generated substitutes.

The one-time bootstrap that creates the initial lockfiles and neutral Tauri resources is setup evidence only. It is not a substitute for the final exact-head Windows/Linux candidate workflow.

## Portable candidate artifact contract

Each platform job packages Electron and Tauri into separate candidate directories, then runs `tools/archive_candidate.py` for each directory. The helper creates a deterministic `tar.gz`, records its SHA-256 and unpacked tree digest, deletes the staging directory, restores it from the archive and verifies that file content, entry modes and symlinks are unchanged.

The automated in-app scenario and startup/RSS harness require the corresponding package manifest and reject a launch command that does not reference the restored package root. Therefore scenario and measurement JSON prove execution from the archived artifact layout rather than from the source tree. The published GitHub artifact includes both the portable archives and restored directories; on Linux the `tar.gz` is the authoritative download format because a surrounding ZIP is not required to preserve executable bits.

The generated VSDX fixture is package-tested automatically. Opening/editing/saving it in Microsoft Visio remains a separate manual acceptance gate and must not be inferred from ZIP/XML validation.

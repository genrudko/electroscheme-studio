# Controlled Visio fixtures

`controlled-minimal.vsdx` and `controlled-master.vssx` are generated from versioned package/XML source. They are not stored as opaque binary source artifacts.

Generate both fixtures with:

```bash
python tools/generate_controlled_visio_fixtures.py evidence/generated/visio-fixtures \
  --canonical shared/fixtures/canonical-project.json
```

Expected SHA-256 values are recorded in `SHA256SUMS.txt`.

CI generates both artifacts from the same versioned source, verifies deterministic byte equality, expected hashes and package structure, then includes the generated artifacts in both packaged desktop candidates.

The Microsoft Visio manual acceptance protocol must use the exact generated artifact from the recorded workflow run. A source-tree binary must never be substituted for that artifact.

This keeps the source-of-truth chain text/reproducibility based and removes opaque binary-upload corruption from the repository boundary.

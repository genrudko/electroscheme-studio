# Controlled Visio fixtures

`controlled-minimal.vsdx` is checked in because it is the exact artifact used by the Microsoft Visio manual acceptance protocol.

`controlled-master.vssx` is **generated**, not uploaded manually. Run:

```bash
python tools/generate_controlled_visio_fixtures.py evidence/generated/visio-fixtures \
  --canonical shared/fixtures/canonical-project.json
```

The expected SHA-256 values are recorded in `SHA256SUMS.txt`. CI generates the VSSX from versioned XML/package source, verifies its SHA and package structure, then includes that generated artifact in both packaged desktop candidates. This avoids silent corruption through an opaque binary-upload path while preserving a reproducible shared VSSX fixture.

# Repository hygiene

## Purpose

ElectroScheme Studio uses patch-based development. The repository must stay understandable even when coding agents create temporary scripts, reports and generated files.

This document defines what should be committed, ignored, audited or reviewed.

## Commit policy

Commit only intentional source changes.

Good commit candidates:

- backend source;
- frontend source;
- schemas;
- documented tools;
- development docs;
- reviewed symbol library files;
- reviewed examples.

Do not commit by default:

- `_logs/`;
- `_reports/`;
- `_patches/`;
- `node_modules/`;
- `.venv/`;
- `dist/`;
- `*.tsbuildinfo`;
- temporary agent scripts;
- temporary audit output;
- local Visio working banks unless we explicitly decide to version them.

## Visio source banks

Local Visio files are useful as import sources but should not be committed blindly.

Current default:

```text
Фигуры*.vsdx
*.vsd
*.vss
```

are treated as local source banks.

Later, if a source bank must be versioned, use an explicit path and possibly Git LFS.

## Dirty tree handling

If the tree is dirty after an agent run:

1. Do not delete files blindly.
2. Generate a hygiene audit.
3. Classify modified/untracked files.
4. Decide:
   - keep and commit;
   - revert;
   - ignore;
   - move to docs/reference;
   - move to symbols/imported/needs_review.
5. Only then proceed with functional development.

## Audit tool

Run:

```powershell
python tools/repository_hygiene_audit.py --root G:\electroscheme-studio --out G:\electroscheme-studio\_reports\repository_hygiene
```

The tool writes:

```text
_reports/repository_hygiene/repository_hygiene_audit.json
_reports/repository_hygiene/README.md
```

## Current known dirty-tree categories

Earlier coding-agent work may leave files in these groups:

- backend source changes;
- frontend source changes;
- generated symbol library backend files;
- generated symbol frontend/editor files;
- temporary `_patches/*.py` scripts;
- local `Фигуры.vsdx`;
- local notes like `План.txt`;
- local reference folder `ГОСТ/`.

Those must be reviewed, not silently committed.
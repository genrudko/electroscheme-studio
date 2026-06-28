# Source change review gate

## Purpose

This gate is used when a coding agent has left substantial backend/frontend changes in the working tree.

The goal is to decide what to do with those changes without blindly committing, reverting or deleting them.

## What the gate checks

The tool writes reports to:

```text
_reports/source_change_review
```

Reports include:

- current `git status --short`;
- diff stat;
- backend/frontend/examples/schemas diff patch;
- untracked files excluding ignored files;
- classification by file group;
- suggested review decision.

## Build gates

The patch also runs warning-mode gates:

- Python compile for `backend/app`;
- backend app import smoke;
- frontend `npm run build` if npm is available.

Failures here do not abort the patch. They mark the result as `WARNING`, because the point is to inspect the dirty working tree safely.

## Decision options after gate

### Accept

Use this only if:

- backend compiles/imports;
- frontend builds;
- changes match product architecture;
- terminal geometry is correct;
- symbol state handling is correct;
- Visio importer strategy is not bypassed.

### Rewrite

Use this if the idea is useful but implementation quality is low.

### Revert/quarantine

Use this if changes are noisy, unsafe or conflict with the Visio-driven symbol strategy.

### Split

Use this when the agent mixed unrelated work:

- backend API;
- frontend editor;
- symbol library;
- routing;
- docs;
- examples.

Split into separate small patches.

## Important rule

Do not accept generated symbol libraries as core truth if they were not imported from reviewed Visio masters or manually authored according to the symbol capability requirements.
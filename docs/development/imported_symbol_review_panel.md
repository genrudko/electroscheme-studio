# Imported symbol review panel

## Purpose

The imported Visio draft symbols can now be reviewed directly inside the frontend WebUI.

This is the first in-app workflow for the Visio symbol pipeline.

## Component

```text
frontend/src/components/ImportedSymbolReviewPanel.vue
```

The component calls:

```text
GET /api/imported-symbols
GET /api/imported-symbols/{symbol_id}
```

and displays:

- validation summary;
- category filter;
- search;
- issue filter;
- symbol list;
- SVG preview;
- terminals count;
- quality score;
- warnings/errors;
- capability flags.

## Current status

This is a review/browse panel only.

It does not yet:

- accept/reject symbols;
- edit symbol geometry;
- map states;
- parameterize busbars;
- promote symbols to core library.

## Next development steps

Recommended next steps:

```text
patch_013_imported_symbol_review_status_model
patch_014_parametric_busbar_model
patch_015_switching_device_state_model
```

The most useful next patch is likely `patch_013`, because it will turn review from read-only browsing into a real workflow:

```text
needs_review
→ accepted
→ rejected
→ needs_manual_terminals
→ needs_state_mapping
→ needs_busbar_parameters
```
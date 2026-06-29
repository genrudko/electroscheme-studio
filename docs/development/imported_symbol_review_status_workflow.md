# Imported symbol review status workflow

## Purpose

The imported symbol review panel is no longer read-only.

Every imported Visio draft symbol now has a persisted workflow status and optional review note.

## Status store

```text
symbols/imported/visio/review_status.json
```

Allowed statuses:

```text
needs_review
accepted
rejected
needs_geometry_review
needs_manual_terminals
needs_state_mapping
needs_busbar_parameters
```

## Backend API

```text
GET /api/imported-symbols/review-status
PUT /api/imported-symbols/{symbol_id}/review-status
```

Example update body:

```json
{
  "status": "needs_manual_terminals",
  "note": "No valid Visio connection points were imported.",
  "updated_by": "webui"
}
```

## Frontend

`ImportedSymbolReviewPanel.vue` now supports:

- workflow status filter;
- status selector;
- note editing;
- save action;
- workflow summary counters.

## Initial status policy

The initializer assigns initial statuses:

- busbar → `needs_busbar_parameters`;
- switching equipment and KRU trolley → `needs_state_mapping`;
- no terminals → `needs_manual_terminals`;
- converter warnings → `needs_geometry_review`;
- otherwise → `needs_review`.

## Next step

Next functional patch should implement one of:

```text
patch_014_parametric_busbar_model
patch_014_review_status_accepted_export_gate
patch_014_symbol_terminal_editor_first_pass
```

Most useful next step: parametric busbar model, because busbars are the backbone for automatic scheme generation.
# Symbol draft review workflow

Imported Visio symbols are now reviewable objects, not raw JSON dumps.

## Generated files

```text
symbols/imported/visio/review_report.json
symbols/imported/visio/review_report.html
symbols/imported/visio/review_summary.md
```

Open:

```text
symbols/imported/visio/review_report.html
```

to visually inspect imported draft symbols.

## Backend API

```text
GET /api/imported-symbols
GET /api/imported-symbols/{symbol_id}
```

These endpoints expose imported draft symbols only.

## Review policy

Draft symbols remain:

```json
"review_status": "needs_review"
```

Promotion to core library is a separate future operation.

## What to review first

1. Symbols with validation errors.
2. Busbars.
3. Circuit breakers.
4. Disconnectors.
5. Earthing switches.
6. KRU trolley symbols.
7. Symbols without terminals.
8. Symbols with many converter warnings.

## Next development direction

Recommended next patches:

```text
patch_012_imported_symbol_review_panel_frontend
patch_013_parametric_busbar_model
patch_014_switching_device_state_model
```
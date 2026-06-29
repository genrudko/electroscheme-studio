# Patch 039 — VSDX page libraries and UI foundation

## Main decision

The left figure library must follow the source Visio page/library layout. Fuzzy title classification is secondary metadata only.

This prevents cases such as autotransformers being pushed into a miscellaneous group when the VSDX file already placed them on a transformer-related page.

## Generated artifacts

```text
frontend/src/lib/editor/vsdxSymbolCatalog.generated.ts
docs/source_authority/vsdx_symbol_catalog.generated.md
docs/source_authority/vsdx_page_libraries.generated.md
_reports/patch_039_vsdx_page_libraries/
```

## UI foundation

```text
frontend/src/lib/editor/editorIconSet.ts
frontend/src/lib/editor/ribbonCommandModel.ts
```

These are foundation files for the next large UI patch that will convert RibbonBar to a real declarative Visio-like command model.
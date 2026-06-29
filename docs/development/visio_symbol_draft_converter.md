# Visio symbol draft converter

## Purpose

This is the first real development step after repository cleanup.

The converter turns Visio VSDX masters into reviewable draft symbols.

```text
Фигуры.vsdx
→ Visio masters
→ draft SymbolDefinition JSON
→ preview.svg
→ manual review
→ accepted core symbols later
```

## Output

Generated files:

```text
symbols/imported/visio/needs_review/*.symbol.json
symbols/imported/visio/index.json
symbols/imported/visio/conversion_summary.json
symbols/imported/visio/preview.svg
symbols/imported/visio/README.md
```

## Review status

Every generated symbol is marked:

```json
"review_status": "needs_review"
```

No generated symbol is promoted to the core library automatically.

## Preserved semantics

The converter creates draft metadata for:

- voltage-class colorization;
- rotation;
- terminal/snap anchors;
- stretchable leads;
- busbar parameters;
- switching-device state requirements;
- KRU trolley state combinations;
- source provenance.

## Known first-draft limitations

The converter is intentionally conservative.

Known limitations:

- advanced Visio group/local transforms may need improvement;
- arcs/splines may use line fallback;
- busbars still require parameterized post-processing;
- switching-device states still require mapping/normalization;
- preview SVG is for review, not final rendering.

## Next expected patch

After this patch, the next useful development patch is:

```text
patch_011_symbol_draft_validation_and_preview_ui
```

It should add validation checks for generated draft symbols and expose imported Visio drafts in the frontend as a reviewable symbol library.
# Patch 055 — rewrite Ribbon component layout

## Problem

CSS-only global fixes did not work. The View tab still rendered as an unacceptable form-like area because previous selectors styled random direct children of the ribbon as command groups.

## Implementation

```text
actual Ribbon Vue component is detected by tab/View labels
component is marked with ess-ribbon-rewritten
dedicated CSS module ribbon-rewrite.css is imported after global editor CSS
direct children of command row are neutral wrappers
nested groups/sections become compact command islands
Ribbon is capped to 88 px total height
```

## Scope

No drag/drop logic, equipment model, canvas model, or renderer logic is changed.

## Repair1

Repair1 only fixes the smoke marker and resumes build/commit after the writer already selected:

```text
frontend/src/components/editor/RibbonBar.vue
```

Smoke marker:

```text
direct children are wrappers/panels
```

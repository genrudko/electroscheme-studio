# Patch 056 — rollback failed Ribbon skins and restore stable UI

## Why

Patches 051-055 made the editor UI worse. The latest screenshot still shows an unacceptable Ribbon and misplaced visual chrome.

## What this patch removes

```text
patch_051 broad professional skin block
patch_052 DOM ruler overlay CSS/import
patch_053 ribbon repair CSS block
patch_054 ribbon repair CSS block
patch_055 ribbon-rewrite.css import and marker
frontend/src/assets/ribbon-rewrite.css
```

## What remains

```text
working drag/drop from patch_050_repair1
busbar limit/mm constants and labels from patch_052
stable compact baseline CSS
```

## Next step

Rewrite RibbonBar.vue structurally from its source template. No more broad CSS patches over random divs.

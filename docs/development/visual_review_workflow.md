# Visual review workflow

## Purpose

Visual/UI and geometry-related patches must not continue blindly.

The project now includes generated visual review snapshots so geometry can be inspected before further development.

## Current visual review target

```text
visual_checks/parametric_busbar/index.html
```

Open this file locally in a browser.

## What to check

For parametric busbars:

- cell/bay numbers are readable;
- labels do not overlap the busbar;
- labels do not collide with bay slot markers;
- dense busbars remain readable;
- vertical busbar labels are acceptable;
- slot markers are useful and not visually noisy;
- top/bottom/both-side behavior is correct.

## Generated files

```text
visual_checks/parametric_busbar/index.html
visual_checks/parametric_busbar/manifest.json
visual_checks/parametric_busbar/*.svg
```

## Rule for future visual patches

Before continuing geometry/UI work, generate visual snapshots and pause for feedback when the change affects:

- symbol geometry;
- label placement;
- terminal/snap/bay-slot visualization;
- canvas layout;
- automatic placement;
- scheme appearance.

## Feedback format

Useful comments are specific, for example:

```text
01_horizontal_bottom_numbered: labels should be closer to the busbar.
03_horizontal_both_sides: top and bottom numbering sequence should be independent.
07_dense_16_slots: labels overlap; need every second label or smaller font.
```

## Next direction after review

After visual review, likely next patches:

```text
patch_018_adjust_busbar_label_policy_from_feedback
patch_019_parametric_busbar_project_placement
patch_020_auto_layout_section_seed
```
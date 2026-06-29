# Scoped alignment guides to drawing area

The interactive review SVG contains both drawing content and review-card content: title, description, metadata and the drawing viewport. Alignment guides must not use the whole snapshot as their coordinate field.

The guide engine now resolves the drawing viewport as the largest viewport-like rectangle inside the SVG. Guide lines and guide candidates are then scoped to that viewport.

Valid guide sources:

```text
bay slot centers
busbar edges
busbar center lines
other text inside the drawing viewport
grid lines inside the drawing viewport
```

Ignored guide sources:

```text
review title
description
metadata
card chrome
text outside the drawing viewport
```

This prevents the “crosshair” from crossing the snapshot header or looking offset relative to the actual scheme.
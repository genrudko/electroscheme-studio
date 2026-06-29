# Reference-point copy/paste

## Requirement

In addition to normal copy/paste, the editor must support copy/paste relative to a picked reference point.

This is the workflow used in CAD tools such as KOMPAS-3D and is very useful when repeating bay/cell objects, textboxes and groups while preserving exact relative spacing.

## Basic workflow

```text
1. Select object or group.
2. Choose Copy by reference point.
3. Pick base/reference point.
4. Pick one or more insertion points.
5. Each pasted object keeps the original offset from the reference point.
```

## Current prototype

`visual_checks/parametric_busbar/interactive.html` implements this for text labels:

```text
select text
Copy from text center
Copy by reference point
Paste by point
Cancel
Clear copies
```

Keyboard shortcuts:

```text
Ctrl+C  copy selected text from its center
Ctrl+V  start paste-by-point
Esc     cancel mode
```

The prototype is visual-only and does not persist pasted text into the project model yet.

## Future model-backed editor behavior

The same capability must apply to:

```text
text boxes
symbols
busbars
bay groups
switchgear bay templates
mixed selections
```

The model contract should store a clipboard payload like:

```json
{
  "mode": "copy_by_reference_point",
  "base_point": { "x": 120, "y": 40 },
  "items": [
    {
      "kind": "text_box",
      "id": "source_text_1",
      "anchor": { "x": 140, "y": 50 },
      "offset_from_base": { "x": 20, "y": 10 }
    }
  ]
}
```

When pasting at a new point:

```text
new_item_position = paste_point + offset_from_base
```

For groups, every item keeps its own offset from the same base point.

## Why it matters

This is especially important for electrical schemes:

```text
repeat cell numbers
repeat bay labels
copy a breaker + text label set
copy a KRU bay fragment
copy several identical feeder cells at exact spacing
```

Normal Ctrl+C/Ctrl+V cannot express the user's intended insertion point. Reference-point paste can.
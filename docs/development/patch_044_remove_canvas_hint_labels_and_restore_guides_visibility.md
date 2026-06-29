# Patch 044 — remove canvas hint labels and restore guide visibility

## Removed from drawing surface

```text
А3 альбомная
Добавьте объект через ленту либо ПКМ-меню
0,0 origin label when rendered as a decorative label
```

These labels are not useful on the editable surface.

## Guide visibility

Guide lines are restored to a visible auxiliary style:

```text
blue
thin
dashed
transparent enough not to look like a real electrical line
with a wider invisible hit target for dragging
```

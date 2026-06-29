# Infinite canvas, rulers, voltage busbars and multiselect

## Scope

Patch 031 upgrades the editor shell toward Visio-like behavior.

## Infinite canvas

The canvas is no longer clamped to a fixed positive coordinate sheet.

The view origin can go negative, and pan can move in all directions.

The coordinate origin is shown subtly:

```text
red dashed cross
small 0,0 marker
```

## ISO page

The editor now has a visible ISO page frame inside the infinite workspace.

Supported settings:

```text
A4 / A3 / A2 / A1 / A0
portrait / landscape
```

The page is centered around the coordinate origin for now.

## Rulers

Top and left rulers use their own SVG coordinate systems and track the same view origin as the canvas.

They are explicitly visible below the Ribbon.

## Guides

Guides are real editable canvas objects:

```text
drag from top ruler -> vertical guide
drag from left ruler -> horizontal guide
drag existing guide -> move it
clear guides from Ribbon
```

## Busbar voltage and auto-length

Busbar has:

```text
voltageKv
automatic voltage color
slot count
slot spacing
auto width = 24 + (slots - 1) * slotSpacing
```

Removing a slot shortens the busbar automatically.

## Multiselect

Shift+click toggles object selection.

Dragging one selected object moves the whole selected group.

Current multiselect supports text and busbar objects in the in-memory editor prototype.

## Remaining limitations

This is still an in-memory editor shell. The next major step should be a model-backed document state and command stack.
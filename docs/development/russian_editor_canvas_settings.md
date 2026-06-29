# Russian editor UI and canvas settings

## User feedback fixed

Patch 029 addresses the first visual review of the editor shell:

```text
hardcoded busbar on canvas
English UI
rough Ribbon button labels
missing canvas settings
missing grid/snap/guide controls
```

## Canvas is now empty by default

The editor starts with an empty canvas. The demo busbar is no longer hardcoded in the SVG template.

A busbar can be inserted explicitly through:

```text
Ribbon → Объекты → Шина
Right-click canvas → Добавить шину
Properties panel → Добавить шину
```

This keeps the canvas as an editor workspace, not a baked-in preview.

## Russian UI

The editor shell is now localized to Russian:

```text
Ribbon tabs
Ribbon groups
buttons
context menu
properties panel
status bar
empty canvas hint
mode messages
```

## Canvas settings

Initial settings:

```text
zoom
grid visible
grid step
snap enabled
snap tolerance
snap to grid
snap to bay slots
snap to objects
guide visibility
```

These settings are stored in `CanvasSettings` and passed from `EditorShell` to `RibbonBar` and `CanvasViewport`.

## Reference point mode

The reference-point workflow remains active:

```text
select object
copy by reference point
virtual point snaps to enabled targets
paste by point with ghost preview
```

The virtual point is shown only in copy/paste point modes, so it no longer looks like a random permanent marker on the canvas.

## Next steps

The next editor patches should continue along this line:

```text
real object model
command stack
undo / redo
object creation tools
busbar properties editor
symbol preview palette
context-aware right-click menus
pan/zoom viewport behavior
```
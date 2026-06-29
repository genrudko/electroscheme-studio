# Editor UI architecture

## Decision

The project is moving from review pages to a real editor shell.

Review pages remain useful for:

```text
visual regression
isolated geometry experiments
quick algorithm checks
```

New UX features should be implemented in the editor/canvas stack.

## First editor shell

Patch 028 introduces:

```text
EditorShell
RibbonBar
CanvasViewport
CanvasContextMenu
StatusBar
```

and editor support libraries:

```text
interactionModes
snapService
referenceClipboard
```

## Target UI direction

The main UI should be closer to Visio and KOMPAS-3D:

```text
Ribbon at the top
SVG canvas in the center
properties panel on the side
status bar at the bottom
context menu on right-click
```

## Interaction modes

Initial modes:

```text
select
pan
copy_by_reference
paste_by_point
```

`copy_by_reference` is a real editor mode, not just a button action.

## Reference-point copy/paste

Workflow:

```text
select object
Copy by reference point
pick virtual base point
pick one or more paste points
```

The virtual point snaps to:

```text
grid
bay slots
object centers
future terminals
future anchors
future guides
```

The status bar shows pointer coordinates and snap type.

## Command-stack direction

All future tools should go through commands:

```text
MoveObjectCommand
RotateObjectCommand
CopyByReferenceCommand
PasteAtPointCommand
CreateBusbarCommand
CreateTextBoxCommand
CreateBaySlotCommand
```

This will make undo/redo, history, hotkeys and batch operations possible.

## Current limitations

This patch is a first editor shell. It uses an in-memory demo busbar and text labels. It does not yet persist object changes to the project model.

Next steps:

```text
model-backed canvas objects
command stack
persistent project document state
real text box object
busbar object editor integration
group selection
object layer / selection layer / guides layer separation
```
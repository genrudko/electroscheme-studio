# Patch 033 — editor architecture, palette, layers and shortcuts

## Why this patch exists

The previous patches added many UI capabilities directly into `CanvasViewport.vue`. That was useful for quick visual progress, but it is not sustainable.

Patch 033 starts the proper editor architecture while keeping the current working canvas alive.

## Added architecture

New editor modules:

```text
editorDocument.ts
commandStack.ts
shapeCatalog.ts
ribbonCommandRegistry.ts
editorClipboard.ts
voltageClasses.ts
```

## Editor document model

The first document model contains:

```text
settings
layers
objects
selection
busbar objects
text objects
primitive objects
image object contract
```

This is the foundation for:

```text
save/load
undo/redo
layers
image insertion
shape data
export
```

## Command stack

`EditorCommandStack` provides:

```text
execute
undo
redo
clear
state
```

Patch 033 wires the shell-level keyboard shortcuts to the command stack foundation. Canvas operations will be migrated to real undoable commands in the next phase.

## Left shape palette

The editor now has a Visio-like left panel:

```text
Фигуры
Поиск фигур
Библиотеки
Фигуры
Слои
```

The palette can insert current canvas objects through the existing command channel:

```text
Шина
Текст
Прямоугольник
Эллипс
Линия
```

## Layers shell

Layers are visible in the left panel:

```text
Схема
Подписи
Направляющие
Изображения
```

At this stage this is a shell, but it uses the same `EditorLayer` model that will later control visibility, locking and print/export behavior.

## Keyboard shortcuts

Added shell-level shortcuts:

```text
Ctrl+C
Ctrl+X
Ctrl+V
Ctrl+Z
Ctrl+Y
Delete
Escape
```

## Voltage repair carried forward

This patch also keeps the repair from patch_032_repair1:

```text
voltageClassId
stable low-voltage classes
35 / 10 / 6 / 0.4 all map to rgb(95,95,95)
```

## Next phase

After the Visio workflow video, the next patch should connect `CanvasViewport` to `editorDocument` and turn canvas operations into undoable commands.
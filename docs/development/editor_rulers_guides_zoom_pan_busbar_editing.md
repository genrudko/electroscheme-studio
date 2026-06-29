# Editor rulers, pulled guides, zoom, pan and editable busbars

## User feedback fixed

Patch 030 addresses these editor shell issues:

```text
need Visio-like top and left rulers
zoom slider must be in bottom bar
mouse wheel should zoom the canvas
middle mouse button should pan
UI must fit one screen without page/ribbon scroll
only canvas area may scroll
guides were toggle-only, not real objects
guides must be pulled from rulers
inserted busbar must be selectable, movable and editable
Ribbon tabs must have meaningful content
```

## Rulers

The canvas now has:

```text
top ruler
left ruler
ruler corner
tick marks based on current grid step
```

## Pulled guides

Guides can be created by:

```text
dragging from the top ruler -> vertical guide
dragging from the left ruler -> horizontal guide
Ribbon / View -> Vertical / Horizontal guide
right-click menu -> guide commands
```

Guides are visible canvas objects and can be dragged after creation.

## Zoom and pan

Zoom controls:

```text
bottom status bar slider
mouse wheel over canvas
100% button in bottom bar
```

Pan controls:

```text
middle mouse button drag
```

## One-screen layout

The shell uses fixed rows:

```text
Ribbon
canvas area
bottom status/zoom bar
```

The page itself does not scroll. Canvas area can scroll.

## Editable busbar

Inserted busbars are no longer just visual background. They are selectable objects.

Supported in this patch:

```text
select busbar
move busbar by dragging
edit X/Y
edit length
edit thickness
edit slot count
edit slot spacing
edit label
delete busbar
```

Bay labels and caption are regenerated from busbar parameters for now.

## Ribbon

Ribbon tabs now show different command groups by active tab:

```text
Главная
Вставка
Шины / ячейки
Вид
Текст
Символы
Соединения
Экспорт
```

Some tabs still contain forward-looking placeholders, but they are no longer just a duplicated all-in-one toolbar.
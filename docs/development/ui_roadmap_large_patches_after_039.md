# UI roadmap after patch 039

## Patch 039 scope

Patch 039 moves the figure library grouping to the real VSDX page/library authority and adds UI foundation files:

```text
editorIconSet.ts
ribbonCommandModel.ts
```

## Next two large UI patches

### Patch 040 — declarative Visio-like Ribbon

Convert the current Ribbon component from ad-hoc groups to:

```text
RibbonTab -> RibbonGroup -> RibbonCommand
```

Required tabs:

```text
Главная
Вставка
Рисование
Символы
Соединения
Вид
Экспорт
```

Required features:

```text
SVG icons from editorIconSet
compact/collapsed Ribbon
UI scale
real View commands: rulers, grid, guides, layers
real Insert/Drawing commands
```

### Patch 041 — canvas interaction and properties UX

Required features:

```text
proper selection rectangle
Ctrl additive selection
multi-drag
better right Properties inspector
context menu command model
mini-toolbar icons
guide manipulation polish
```

After these two patches, return to the equipment library and exact VSDX master renderer.
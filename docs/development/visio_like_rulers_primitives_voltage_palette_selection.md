# Visio-like ruler rendering, primitives, voltage palette and selection

## Patch 032

Patch 031 moved in the right direction but the visual implementation was unacceptable:

```text
rulers were visually stretched
rulers did not reliably align with the grid at zoom
ISO page visually washed out the grid
origin marker was too large
voltage colors were not based on the provided codifier
selection outline was too thick
multiselect used Shift instead of Ctrl
there was no marquee selection rectangle
basic graphic primitives were missing
text style controls were missing
```

## Rulers

Rulers are now HTML/CSS pixel rulers, not stretched SVG text.

Tick positions are computed as:

```text
screen = (world - viewOrigin) * zoom
```

This keeps ruler ticks aligned with the SVG canvas grid at different zoom levels.

## Selection

Selection follows Visio-style expectations:

```text
Ctrl+click toggles object selection
dragging a rectangle on empty canvas performs marquee selection
dragging one selected object moves the selected group
```

## Voltage colors

Busbar colors now follow the provided voltage-class codifier:

```text
1150 кВ      rgb(205,138,255)
800/750 кВ  rgb(0,0,168)
500 кВ      rgb(213,0,0)
400 кВ      rgb(255,100,30)
330 кВ      rgb(0,170,0)
220 кВ      rgb(255,210,0)
110 кВ      rgb(0,153,255)
0,4–35 кВ   rgb(95,95,95)
```

## ISO page and origin

ISO page is a thin outline only. The grid remains visible through the page.

The coordinate origin marker is deliberately subtle.

## Graphic primitives

The editor now has basic primitives:

```text
rectangle
ellipse
line
```

They can be selected, moved, multi-selected, and styled in the properties panel.

## Text style controls

Text properties now include:

```text
font family
font size
color
bold
italic
rotation
```

## Remaining work

This patch still does not implement full model-backed persistence, command stack, native clipboard, layers, or image insertion. Those should be added on top of the editor document model.
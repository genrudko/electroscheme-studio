# Patch 037 — Ribbon standards and VSDX SVG previews

## Fixed

```text
Ribbon no longer clips command groups vertically.
Left shape library can show inline SVG previews instead of crude text glyphs.
Engineering profile settings are exposed in the editor model and Ribbon View tab.
```

## Engineering settings

Defaults:

```text
modularGridStepMm = 2.5
ugoLineWidthMm = 0.4
electricalConnectionLineWidthMm = 0.4
```

Line width values are clamped to the standard range:

```text
0.2 … 1.0 mm
```

## VSDX previews

The generated VSDX catalog now includes `svgPreview`.

The preview is an approximate ShapeSheet geometry projection meant for library cards. It is not yet the final exact drawing renderer for inserted schematic objects.

# Patch 041 — safe library icons and icon override system

## Problem

Generated per-item icons are inconsistent. Some are acceptable, some are wrong. Guessing a precise UGO from the Russian title is not reliable.

## New policy

Default palette mode is conservative:

```text
Библиотека
```

This shows stable library/category icons, not guessed exact equipment icons.

The user can switch to:

```text
УГО
```

This enables high-confidence exact icons only.

The user can also switch to:

```text
Без иконок
```

This removes icons from cards entirely.

## Override system

Added:

```text
frontend/src/lib/editor/paletteIconPolicy.ts
```

Manual overrides are intentionally explicit:

```ts
paletteIconOverrides
```

We should fill it only after visual review or after implementing exact VSDX renderer.

## Long-term correct fix

The real solution is still:

```text
VSDX master ShapeSheet -> exact SVG renderer -> palette thumbnail + insertable symbol
```

Until then, no UI should pretend that guessed icons are source-authoritative.

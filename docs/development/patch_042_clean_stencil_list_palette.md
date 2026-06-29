# Patch 042 — clean stencil list palette

## Reason

Patch 041 technically worked but the UI was still visually noisy. Some generated icons remained misleading.

## New default

The left palette now defaults to:

```text
Список
```

That means no icon is shown by default.

Optional modes are hidden under:

```text
Вид списка
```

Available modes:

```text
Список — no icons, clean stencil list
Группы — conservative library/category icons
УГО — high-confidence icons only
```

## Removed from visible cards

```text
spinner-like planned marker
planned dot
permanent library badge
permanent port badge
raw VSDX micro-preview
```

VSDX details remain in tooltip.

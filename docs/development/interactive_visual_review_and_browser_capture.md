# Interactive visual review and browser capture

## Why

The normal `index.html` visual review page is a static page. It is useful for inspection, but not for dragging.

This patch adds:

```text
visual_checks/parametric_busbar/interactive.html
```

The interactive page embeds SVG inline and allows visually dragging bus captions.

## WebUI drag fix

The Parametric Busbar panel now moves the caption immediately during pointer drag and refreshes the preview after pointer release.

## Browser capture

A headless Edge/Chrome capture tool was added:

```text
tools/capture_visual_review_browser.py
```

It creates screenshots in:

```text
_reports/visual_review_browser_captures
```

This lets visual checks be reviewed without manually taking screenshots of the browser window.

## Expected workflow

1. Generate visual snapshots.
2. Generate `interactive.html`.
3. Capture static and interactive pages with headless browser.
4. Inspect PNGs or upload them for review.
5. Only then continue geometry/UI patches.
# Patch 040 — stencil palette cleanup

## Problem

Raw VSDX ShapeSheet micro-previews are not acceptable as user-facing library icons yet. They make the palette look broken and visually noisy.

## Decision

Until the exact VSDX master renderer exists, the left library uses clean semantic engineering icons:

```text
circuit breaker
withdrawable truck
disconnector
earthing switch
short-circuiter
transformer / autotransformer / VT / CT
machine / generator / motor
busbar / line
arrester
fuse
reactor
capacitor
generic VSDX object
```

VSDX data is preserved:

```text
source page/library
master id
size
connection point count
source summary
```

but it is shown in tooltip/details, not as permanent clutter in each card.

## Explicit UI rules

```text
No raw VSDX micro-preview as the primary palette icon.
No spinner-like planned icon.
No permanent “1 port.” / “2 port.” badge.
No disabled-looking planned cards.
No fake claim that planned symbols are insertable before the VSDX renderer exists.
```

The next renderer stage must implement exact VSDX master rendering before these symbols become insertable.

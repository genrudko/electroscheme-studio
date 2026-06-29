# Voltage class id palette repair

Patch 032 introduced the voltage codifier, but busbar selection was still based on numeric `voltageKv`.

This repair introduces stable `voltageClassId` values:

```text
1150
800
750
500
400
330
220
110
35
10
6
0.4
```

The 35 kV and lower selectable classes all map to the codifier color:

```text
rgb(95, 95, 95)
```

This avoids ambiguous lower-voltage handling and keeps the UI selection explicit even when several classes share the same codifier color.

The old numeric `voltageKv` field is retained for compatibility and synchronized from `voltageClassId`.
# STO normal scheme profile

Source document:

```text
СТО 56947007-29.240.10.035-2009
Правила оформления нормальных схем электрических соединений подстанций
и графического отображения информации посредством программно-технических комплексов
```

This document is used as a style and display profile for ElectroScheme Studio. It is not treated as the only possible symbol source.

## Normal scheme principles

Normal schemes should represent substation equipment and primary electrical connections.

The drawing should be readable and should use simple vertical and horizontal connections with the minimum practical number of crossings.

The relative location and orientation of switchgear areas should normally correspond to the top view of the substation.

## Voltage color palette for normal schemes

| Voltage class | RGB |
|---|---|
| 1150 кВ | 205, 138, 255 |
| 800/750 кВ | 0, 0, 168 |
| 500 кВ | 213, 0, 0 |
| 400 кВ | 255, 100, 30 |
| 330 кВ | 0, 170, 0 |
| 220 кВ | 255, 210, 0 |
| 110 кВ | 0, 153, 255 |
| 0,4–35 кВ | 95, 95, 95 |

## PTK / operational display palette

| Voltage class | RGB |
|---|---|
| Background | 0, 0, 0 |
| 800/750 кВ | 50, 100, 255 |
| 500 кВ | 213, 0, 0 |
| 400 кВ | 255, 100, 30 |
| 330 кВ | 0, 170, 0 |
| 220 кВ | 255, 210, 0 |
| 150 кВ | 205, 138, 255 |
| 110 кВ | 60, 160, 255 |
| 35/24/20/10/6 кВ | gray |

## Text

Equipment labels on normal schemes:

```text
font-family: Arial
color: black
```

For printed schemes, label height should not be less than 1.5 mm.

## Busbars

Busbars must be shown as thick lines.

Rule:

```text
busbar stroke width = 4 × normal line stroke width
```

For the editor, busbars must be parameterized:

- number of connection points;
- connection point spacing;
- orientation;
- length;
- voltage class;
- bus/section label.

## Switching states for operational/PTK display

Switching equipment needs explicit state variants.

Minimum state vocabulary:

```text
closed
open
unreliable
repair
transition
manual_unconfirmed
```

This affects:

- breakers;
- disconnectors;
- earthing switches;
- KRU trolleys;
- other switching devices.

## Editor interaction requirements

Symbols must remain useful as editable objects, not static SVG stickers.

Required behavior:

- rotate without losing terminal positions;
- move without breaking connection graph;
- stretch leads without distorting core symbol geometry;
- snap terminals to terminals and busbar generated points;
- re-color by voltage class;
- preserve topology when auto-routed.

## Symbol import impact

The Visio importer must not reduce stateful or parametric equipment to a single static drawing.

Every imported symbol should carry semantic feature flags:

```json
{
  "colorizable_by_voltage_class": true,
  "multi_state_candidate": true,
  "busbar_configurable_connection_points": false,
  "rotatable": true,
  "snap_anchors_required": true,
  "stretchable_leads_candidate": true,
  "auto_layout_eligible": true,
  "requires_review": true
}
```
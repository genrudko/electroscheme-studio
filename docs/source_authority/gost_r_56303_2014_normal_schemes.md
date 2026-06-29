# Source authority — ГОСТ Р 56303-2014 normal schemes

## Source

Primary working reference:

```text
https://elektroshema.ru/2009-02-05-22-57-45/ugo-2/144-normalnaya-sxema.html
```

The page states that examples are based on **ГОСТ Р 56303-2014**, with notes where СТО 56947007-25.040.70.101-2011 differs.

## Voltage color palette — ГОСТ Р 56303-2014

| Voltage class | Color name | RGB |
|---:|---|---:|
| 1150 кВ | сиреневый | 205:138:255 |
| 800 кВ | темно-синий | 0:0:168 |
| 750 кВ | темно-синий | 0:0:168 |
| 500 кВ | красный | 213:0:0 |
| 400 кВ | оранжевый | 255:100:30 |
| 330 кВ | зеленый | 0:170:0 |
| 220 кВ | желто-зеленый | 181:181:0 |
| 150 кВ | хаки | 170:150:0 |
| 110 кВ | голубой | 0:153:255 |
| 60 кВ | лиловый | 255:51:204 |
| 35 кВ | коричневый | 102:51:0 |
| 20 кВ | ярко-фиолетовый | 160:32:240 |
| 15 кВ | ярко-фиолетовый | 160:32:240 |
| 10 кВ | фиолетовый | 102:0:204 |
| 6 кВ | темно-зеленый | 0:102:0 |
| 3 кВ | темно-зеленый | 0:102:0 |
| ниже 3 кВ | серый | 127:127:127 |

## Engineering style rules

Default schema style profile:

```text
modular grid step = 2.5 mm
UGO line width = 0.4 mm
electrical connection line width = 0.4 mm
busbar uses voltage class color
busbar connection points are white
```

## UGO category groups to model

The shape catalog must grow by the same high-level groups:

```text
transformers
switching apparatus
compensation and filter devices
surge arresters / OPN
generators / motors
fuses
lines / busbars / grounding
```
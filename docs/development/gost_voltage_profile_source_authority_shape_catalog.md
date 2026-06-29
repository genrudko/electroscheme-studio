# Patch 034 — ГОСТ voltage palette, display profile and source authority

## Fix

Patch 033 still carried the temporary simplification:

```text
0.4–35 kV = gray
```

That is wrong for the ГОСТ Р 56303-2014 palette.

Patch 034 replaces it with the complete voltage palette from the Elektroshema reference.

## Display profiles

Added a style profile contract:

```text
gost_r_56303_2014
sto_fsk_placeholder
```

The active default is:

```text
gost_r_56303_2014
```

The СТО ФСК profile is intentionally a placeholder until its colors and symbol differences are implemented separately.

## Engineering defaults

Added default engineering schema style:

```text
modularGridStepMm = 2.5
ugoLineWidthMm = 0.4
electricalConnectionLineWidthMm = 0.4
busbarUsesVoltageColor = true
busbarConnectionPointFill = #ffffff
```

## Shape catalog

Expanded catalog categories according to the source page:

```text
Линии / шины / заземление
Коммутационные аппараты
Трансформаторы
Компенсация / фильтры
Разрядники / ОПН
Генераторы / двигатели
Предохранители
```

Only currently implemented primitives are enabled. ГОСТ-specific symbols are added as planned entries so the UI does not pretend that unfinished UGO are already implemented.

## Visual verification

Create/select a busbar and change voltage class:

```text
35 kV -> rgb(102,51,0) brown
20/15 kV -> rgb(160,32,240) bright violet
10 kV -> rgb(102,0,204) violet
6/3 kV -> rgb(0,102,0) dark green
below 3 kV -> rgb(127,127,127) gray
```
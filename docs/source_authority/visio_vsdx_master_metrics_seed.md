# Visio VSDX master metrics seed

Source file analyzed in ChatGPT sandbox:

```text
Фигуры(1).vsdx
```

The VSDX/VSSX symbol geometry must be treated as source authority for symbol size, ports and default geometry. Do not hand-draw electrical symbols in the editor when the same figure exists in the Visio source.

## Extracted key metrics

Values below are extracted from Visio ShapeSheet master/page data. Visio stores many linear values in inches; the table below is converted to millimetres.

| Master | Page size | Shape count | Connection points | Notes |
|---|---:|---:|---:|---|
| Выключатель | 7.5 × 15.0 mm | 3 | 2 | Main group line is 15 mm; child symbols include 5.0 × 5.0 mm and 7.5 × 7.5 mm elements. |
| Разъединитель | 2.5 × 15.0 mm | 2 | 2 | Main group line is 15 mm; child active geometry is 7.5 × 7.5 mm. |
| Выключатель нагрузки | 7.5 × 15.0 mm | 2 | 2 | Main group line is 15 mm. |
| Автоматический выключатель | 2.9 × 15.0 mm | 3 | 2 | Top group line is 25 mm in master geometry; child active geometry is 7.5 × 7.5 mm. |
| Шина1 | top group width 55.0 mm | 12 | 22 | Slot/circle elements are 1.5 × 1.5 mm; visible slot centres include 5/20/35/50 mm in the master group. |

## Design rule

For the editor:

```text
symbol dimensions, connection ports and default terminal locations come from VSDX/VSSX master metrics
temporary placeholder symbols are forbidden once a source master exists
```

## Tool

Use:

```powershell
python tools/extract_vsdx_master_metrics.py "path\to\Фигуры(1).vsdx" --json-out _reports\vsdx_master_metrics.json --csv-out _reports\vsdx_master_metrics.csv
```

The tool reads:

```text
visio/masters/masters.xml
visio/masters/master<ID>.xml
ShapeSheet PageWidth/PageHeight
Shape/Cell Width, Height, PinX, PinY, BeginX, BeginY, EndX, EndY
Connection sections
Geometry sections
```
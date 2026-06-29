from __future__ import annotations

import argparse
import csv
import json
import math
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

NS = {"v": "http://schemas.microsoft.com/office/visio/2012/main"}
INCH_TO_MM = 25.4


def _cell_value(element: ET.Element | None, name: str) -> str | None:
    if element is None:
        return None
    for cell in element.findall("v:Cell", NS):
        if cell.attrib.get("N") == name:
            return cell.attrib.get("V") or cell.attrib.get("F")
    return None


def _float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        result = float(value)
    except ValueError:
        return None
    if math.isnan(result) or math.isinf(result):
        return None
    return result


def _mm(value_inch: float | None) -> float | None:
    if value_inch is None:
        return None
    return round(value_inch * INCH_TO_MM, 3)


def _section_rows(element: ET.Element, section_name: str) -> int:
    total = 0
    for section in element.findall("v:Section", NS):
        if section.attrib.get("N") == section_name:
            total += len(section.findall("v:Row", NS))
    return total


def _walk_shapes(parent: ET.Element):
    for shape in parent.findall("v:Shape", NS):
        yield shape
        nested = shape.find("v:Shapes", NS)
        if nested is not None:
            yield from _walk_shapes(nested)


def _shape_metrics(shape: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {
        "id": shape.attrib.get("ID"),
        "type": shape.attrib.get("Type"),
    }
    for key in ("PinX", "PinY", "Width", "Height", "LocPinX", "LocPinY", "Angle", "BeginX", "BeginY", "EndX", "EndY"):
        value = _float(_cell_value(shape, key))
        if value is not None:
            data[f"{key}_raw"] = value
            if key != "Angle":
                data[f"{key}_mm"] = _mm(value)
    data["connection_rows"] = _section_rows(shape, "Connection")
    data["geometry_rows"] = _section_rows(shape, "Geometry")
    return data


def extract_metrics(vsdx_path: Path) -> list[dict[str, Any]]:
    with zipfile.ZipFile(vsdx_path) as archive:
        names = set(archive.namelist())
        masters_xml = archive.read("visio/masters/masters.xml")
        masters_root = ET.fromstring(masters_xml)

        result: list[dict[str, Any]] = []

        for master in masters_root.findall("v:Master", NS):
            master_id = master.attrib.get("ID")
            name = master.attrib.get("Name") or master.attrib.get("NameU") or ""
            page_sheet = master.find("v:PageSheet", NS)
            page_width_in = _float(_cell_value(page_sheet, "PageWidth"))
            page_height_in = _float(_cell_value(page_sheet, "PageHeight"))

            master_path = f"visio/masters/master{master_id}.xml"
            top_shape: dict[str, Any] | None = None
            top_children: list[dict[str, Any]] = []
            shape_count = 0
            connection_count = 0
            geometry_row_count = 0

            if master_path in names:
                contents = ET.fromstring(archive.read(master_path))
                shapes = contents.find("v:Shapes", NS)
                if shapes is not None:
                    all_shapes = list(_walk_shapes(shapes))
                    shape_count = len(all_shapes)
                    connection_count = sum(_section_rows(shape, "Connection") for shape in all_shapes)
                    geometry_row_count = sum(_section_rows(shape, "Geometry") for shape in all_shapes)

                    top_shapes = shapes.findall("v:Shape", NS)
                    if top_shapes:
                        top_shape = _shape_metrics(top_shapes[0])
                        nested = top_shapes[0].find("v:Shapes", NS)
                        if nested is not None:
                            top_children = [_shape_metrics(child) for child in nested.findall("v:Shape", NS)]

            result.append(
                {
                    "id": master_id,
                    "name": name,
                    "master_path": master_path if master_path in names else None,
                    "page_width_mm": _mm(page_width_in),
                    "page_height_mm": _mm(page_height_in),
                    "shape_count": shape_count,
                    "connection_count": connection_count,
                    "geometry_section_row_count": geometry_row_count,
                    "top_shape": top_shape,
                    "top_children": top_children,
                }
            )

        return result


def write_csv(path: Path, metrics: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "id",
        "name",
        "master_path",
        "page_width_mm",
        "page_height_mm",
        "shape_count",
        "connection_count",
        "geometry_section_row_count",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(metrics)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract Visio VSDX/VSSX master dimensions and connection point metrics.")
    parser.add_argument("input", type=Path, help="Path to .vsdx or .vssx file")
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--csv-out", type=Path, default=None)
    args = parser.parse_args()

    metrics = extract_metrics(args.input)

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.csv_out:
        write_csv(args.csv_out, metrics)

    print(f"VSDX_MASTER_METRICS_COUNT={len(metrics)}")
    for item in metrics:
        if item["name"] in {"Выключатель", "Разъединитель", "Выключатель нагрузки", "Автоматический выключатель"}:
            print(
                f"{item['id']};{item['name']};"
                f"{item['page_width_mm']}x{item['page_height_mm']}mm;"
                f"connections={item['connection_count']};"
                f"shapes={item['shape_count']}"
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
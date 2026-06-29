from __future__ import annotations

import argparse
import csv
import html
import json
import math
import re
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET

NS = {
    "v": "http://schemas.microsoft.com/office/visio/2012/main",
    "r": "http://schemas.openxmlformats.org/package/2006/relationships",
}


@dataclass
class SymbolDataField:
    id: str
    label: str
    type: str
    source: str


@dataclass
class SymbolConnectionPoint:
    id: str
    x: float | None
    y: float | None


@dataclass
class VsdxSymbolDefinition:
    id: str
    masterId: str
    title: str
    categoryId: str
    widthMm: float
    heightMm: float
    connectionCount: int
    shapeCount: int
    geometrySectionCount: int
    propertyNames: list[str]
    userCellNames: list[str]
    connectionPoints: list[SymbolConnectionPoint]
    dataFields: list[SymbolDataField]
    preview: str
    svgPreview: str
    status: str
    sourcePath: str


def cell_value(shape: ET.Element | None, name: str) -> str | None:
    if shape is None:
        return None
    for cell in shape.findall("v:Cell", NS):
        if cell.attrib.get("N") == name:
            return cell.attrib.get("V") or cell.attrib.get("F")
    return None


def row_cell_value(row: ET.Element, name: str) -> str | None:
    for cell in row.findall("v:Cell", NS):
        if cell.attrib.get("N") == name:
            return cell.attrib.get("V") or cell.attrib.get("F")
    return None


def to_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    # ShapeSheet formulas can appear here. For preview, ignore complex formulas.
    if not re.fullmatch(r"[-+]?\d+([.,]\d+)?([eE][-+]?\d+)?", text):
        return None
    try:
        return float(text.replace(",", "."))
    except ValueError:
        return None


def inches_to_mm(value: float | None) -> float:
    if value is None or not math.isfinite(value):
        return 0.0
    return round(value * 25.4, 3)


def safe_id(text: str, fallback: str) -> str:
    text = text.strip().lower()
    text = (
        text.replace("ё", "е")
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace("-", "_")
        .replace(".", "_")
    )
    text = re.sub(r"[^a-zа-я0-9_]+", "", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or fallback


def read_xml(zf: zipfile.ZipFile, path: str) -> ET.Element:
    return ET.fromstring(zf.read(path))


def get_master_rels(zf: zipfile.ZipFile) -> dict[str, str]:
    rel_path = "visio/masters/_rels/masters.xml.rels"
    if rel_path not in zf.namelist():
        return {}
    root = read_xml(zf, rel_path)
    result: dict[str, str] = {}
    rel_ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    for rel in root.findall(f"{{{rel_ns}}}Relationship"):
        rid = rel.attrib.get("Id")
        target = rel.attrib.get("Target")
        if rid and target:
            result[rid] = "visio/masters/" + target.lstrip("/")
    return result


def count_descendant_shapes(root: ET.Element) -> int:
    return len(root.findall(".//v:Shape", NS))


def find_master_root_shape(master_root: ET.Element) -> ET.Element | None:
    shapes = master_root.find(".//v:Shapes", NS)
    if shapes is None:
        return None
    return shapes.find("v:Shape", NS)


def iter_sections(root: ET.Element, section_name: str) -> list[ET.Element]:
    return [section for section in root.findall(".//v:Section", NS) if section.attrib.get("N") == section_name]


def count_geometry_sections(root: ET.Element) -> int:
    return len([section for section in root.findall(".//v:Section", NS) if (section.attrib.get("N") or "").lower().startswith("geometry")])


def collect_connection_points(root: ET.Element) -> list[SymbolConnectionPoint]:
    points: list[SymbolConnectionPoint] = []
    point_index = 1
    for section in iter_sections(root, "Connection"):
        for row in section.findall("v:Row", NS):
            x = inches_to_mm(to_float(row_cell_value(row, "X")))
            y = inches_to_mm(to_float(row_cell_value(row, "Y")))
            points.append(SymbolConnectionPoint(id=f"p{point_index}", x=x, y=y))
            point_index += 1
    return points


def collect_section_names(root: ET.Element, section_name: str) -> list[str]:
    names: list[str] = []
    for section in iter_sections(root, section_name):
        for row in section.findall("v:Row", NS):
            name = row.attrib.get("N") or row.attrib.get("IX")
            if name is not None:
                names.append(str(name))
    return sorted(set(names))


def normalize_name(name: str) -> str:
    return name.lower().replace("ё", "е")


def categorize(title: str) -> str:
    text = normalize_name(title)
    if any(token in text for token in ["шина", "кабель", "кл", "линия", "заземл", "земл"]):
        return "busbars_lines_grounding"
    if any(token in text for token in ["выключ", "разъедин", "отдел", "тележ", "контакт", "переключ"]):
        return "switching"
    if any(token in text for token in ["трансформ", "тн", "тт", "автотранс"]):
        return "transformers"
    if any(token in text for token in ["реактор", "дгр", "конденс", "фильтр", "компенс"]):
        return "compensation_filters"
    if any(token in text for token in ["опн", "разряд", "ограничитель"]):
        return "surge_arresters"
    if any(token in text for token in ["генератор", "двигател", "мотор"]):
        return "generators_motors"
    if any(token in text for token in ["предохран", "плавк"]):
        return "fuses"
    return "vsdx_symbols"


def preview_for(title: str, category: str) -> str:
    text = normalize_name(title)
    if category == "busbars_lines_grounding":
        if "зазем" in text:
            return "⏚"
        return "▰"
    if category == "switching":
        if "разъедин" in text:
            return "╱"
        return "□"
    if category == "transformers":
        return "◎"
    if category == "compensation_filters":
        return "⌁"
    if category == "surge_arresters":
        return "⚡"
    if category == "generators_motors":
        return "G" if "генератор" in text else "M"
    if category == "fuses":
        return "⌁"
    return "◇"


def semantic_fields(title: str, category: str) -> list[SymbolDataField]:
    text = normalize_name(title)
    fields: list[SymbolDataField] = []

    def add(id_: str, label: str, type_: str, source: str = "semantic_scaffold") -> None:
        fields.append(SymbolDataField(id=id_, label=label, type=type_, source=source))

    if category == "transformers":
        add("winding_count", "Количество обмоток", "number")
        add("primary_voltage_kv", "Напряжение ВН, кВ", "number")
        add("secondary_voltage_kv", "Напряжение НН/СН, кВ", "number")
        add("winding_connection_group", "Схема/группа соединения обмоток", "enum")
        add("neutral_grounding", "Режим нейтрали", "enum")
        add("tap_changer", "РПН/ПБВ", "enum")
        if "тн" in text or "напряж" in text:
            add("metering_secondary", "Измерительная вторичная цепь", "boolean")
        if "тт" in text or "тока" in text:
            add("ratio", "Коэффициент трансформации", "string")
    elif category == "switching":
        add("switch_state", "Положение", "enum")
        add("truck_position", "Положение тележки", "enum")
        add("control_mode", "Режим управления", "enum")
        add("connection_control_enabled", "Контроль соединений", "boolean")
        if "зазем" in text:
            add("earthing_state", "Положение ЗН", "enum")
    elif category == "busbars_lines_grounding":
        add("voltage_class_id", "Класс напряжения", "voltageClass")
        add("connection_point_count", "Количество точек подключения", "number")
        add("line_type", "Тип линии/шины", "enum")
    elif category == "compensation_filters":
        add("rated_reactive_power", "Номинальная реактивная мощность", "number")
        add("rated_voltage_kv", "Номинальное напряжение, кВ", "number")
    elif category == "surge_arresters":
        add("rated_voltage_kv", "Номинальное напряжение, кВ", "number")
        add("arrester_type", "Тип ОПН/разрядника", "enum")
    elif category == "generators_motors":
        add("rated_power_mw", "Номинальная мощность", "number")
        add("rated_voltage_kv", "Номинальное напряжение, кВ", "number")
    elif category == "fuses":
        add("rated_current_a", "Номинальный ток, А", "number")
        add("fuse_type", "Тип предохранителя", "enum")

    return fields


def geometry_row_to_cmd(row: ET.Element, height_mm: float) -> tuple[str, list[float]] | None:
    row_type = row.attrib.get("T") or row.attrib.get("N") or ""
    x = inches_to_mm(to_float(row_cell_value(row, "X")))
    y_raw = inches_to_mm(to_float(row_cell_value(row, "Y")))
    y = height_mm - y_raw

    if row_type in {"MoveTo", "RelMoveTo"}:
        return ("M", [x, y])
    if row_type in {"LineTo", "RelLineTo"}:
        return ("L", [x, y])
    if row_type in {"ArcTo", "RelArcTo"}:
        # Approximate arc as a line for compact preview; exact ArcTo renderer comes later.
        return ("L", [x, y])
    return None


def collect_svg_paths(master_root: ET.Element, width_mm: float, height_mm: float, max_paths: int = 12) -> list[str]:
    paths: list[str] = []
    if width_mm <= 0 or height_mm <= 0:
        return paths

    for section in master_root.findall(".//v:Section", NS):
        name = section.attrib.get("N") or ""
        if not name.lower().startswith("geometry"):
            continue

        chunks: list[str] = []
        for row in section.findall("v:Row", NS):
            cmd = geometry_row_to_cmd(row, height_mm)
            if cmd is None:
                continue
            command, values = cmd
            chunks.append(f"{command}{values[0]:.3f},{values[1]:.3f}")

        if len(chunks) >= 2:
            paths.append(" ".join(chunks))
            if len(paths) >= max_paths:
                break

    return paths


def svg_preview(title: str, category: str, width_mm: float, height_mm: float, connection_points: list[SymbolConnectionPoint], paths: list[str]) -> str:
    stroke = "#6d0ad6"
    if width_mm <= 0 or height_mm <= 0:
        return fallback_svg(preview_for(title, category), category)

    pad = max(width_mm, height_mm) * 0.12
    view_x = -pad
    view_y = -pad
    view_w = width_mm + 2 * pad
    view_h = height_mm + 2 * pad

    body: list[str] = []
    if paths:
        for path in paths[:10]:
            body.append(f'<path d="{html.escape(path)}" fill="none" stroke="{stroke}" stroke-width="0.8" stroke-linecap="round" stroke-linejoin="round"/>')
    else:
        body.append(f'<rect x="0" y="0" width="{width_mm:.3f}" height="{height_mm:.3f}" fill="none" stroke="{stroke}" stroke-width="0.8"/>')

    for point in connection_points[:8]:
        if point.x is None or point.y is None:
            continue
        body.append(f'<circle cx="{point.x:.3f}" cy="{height_mm - point.y:.3f}" r="{max(min(width_mm, height_mm) * 0.045, 0.35):.3f}" fill="#fff" stroke="{stroke}" stroke-width="0.55"/>')

    label = html.escape(title)
    return f'<svg viewBox="{view_x:.3f} {view_y:.3f} {view_w:.3f} {view_h:.3f}" aria-label="{label}" role="img">{"".join(body)}</svg>'


def fallback_svg(symbol: str, category: str) -> str:
    safe = html.escape(symbol)
    if symbol == "▰":
        return '<svg viewBox="0 0 64 32" aria-hidden="true"><rect x="7" y="12" width="50" height="8" rx="1.5" fill="#6d0ad6" stroke="#111827" stroke-width="1"/><circle cx="17" cy="16" r="3" fill="#fff" stroke="#111827" stroke-width="1"/><circle cx="32" cy="16" r="3" fill="#fff" stroke="#111827" stroke-width="1"/><circle cx="47" cy="16" r="3" fill="#fff" stroke="#111827" stroke-width="1"/></svg>'
    return f'<svg viewBox="0 0 64 32" aria-hidden="true"><text x="32" y="22" text-anchor="middle" font-size="20" font-family="Arial" font-weight="700" fill="#6d0ad6">{safe}</text></svg>'


def parse_vsdx(path: Path) -> list[VsdxSymbolDefinition]:
    with zipfile.ZipFile(path) as zf:
        masters_xml_path = "visio/masters/masters.xml"
        if masters_xml_path not in zf.namelist():
            raise RuntimeError(f"masters.xml not found in {path}")

        rels = get_master_rels(zf)
        masters_root = read_xml(zf, masters_xml_path)
        result: list[VsdxSymbolDefinition] = []

        for index, master in enumerate(masters_root.findall(".//v:Master", NS), start=1):
            master_id = master.attrib.get("ID") or str(index)
            raw_title = master.attrib.get("Name") or master.attrib.get("NameU") or f"Master {master_id}"
            rel_id = master.attrib.get(f"{{{NS['r']}}}id")
            master_path = rels.get(rel_id or "", f"visio/masters/master{master_id}.xml")
            if master_path not in zf.namelist():
                continue

            master_root = read_xml(zf, master_path)
            root_shape = find_master_root_shape(master_root)
            width_mm = inches_to_mm(to_float(cell_value(root_shape, "Width")) if root_shape is not None else None)
            height_mm = inches_to_mm(to_float(cell_value(root_shape, "Height")) if root_shape is not None else None)
            connections = collect_connection_points(master_root)
            prop_names = collect_section_names(master_root, "Prop")
            user_cell_names = collect_section_names(master_root, "User")
            category = categorize(raw_title)
            safe = safe_id(raw_title, f"master_{master_id}")
            paths = collect_svg_paths(master_root, width_mm, height_mm)

            result.append(
                VsdxSymbolDefinition(
                    id=f"vsdx_{safe}_{master_id}",
                    masterId=str(master_id),
                    title=raw_title,
                    categoryId=category,
                    widthMm=width_mm,
                    heightMm=height_mm,
                    connectionCount=len(connections),
                    shapeCount=count_descendant_shapes(master_root),
                    geometrySectionCount=count_geometry_sections(master_root),
                    propertyNames=prop_names,
                    userCellNames=user_cell_names,
                    connectionPoints=connections,
                    dataFields=semantic_fields(raw_title, category),
                    preview=preview_for(raw_title, category),
                    svgPreview=svg_preview(raw_title, category, width_mm, height_mm, connections, paths),
                    status="planned",
                    sourcePath=master_path,
                )
            )

        return result


def fallback_defs() -> list[VsdxSymbolDefinition]:
    return [
        VsdxSymbolDefinition(
            id="vsdx_fallback_circuit_breaker",
            masterId="fallback",
            title="Выключатель",
            categoryId="switching",
            widthMm=7.5,
            heightMm=15.0,
            connectionCount=2,
            shapeCount=3,
            geometrySectionCount=0,
            propertyNames=[],
            userCellNames=[],
            connectionPoints=[SymbolConnectionPoint("p1", 3.75, 0), SymbolConnectionPoint("p2", 3.75, 15)],
            dataFields=semantic_fields("Выключатель", "switching"),
            preview="□",
            svgPreview=fallback_svg("□", "switching"),
            status="planned",
            sourcePath="fallback",
        )
    ]


def generated_ts(defs: list[VsdxSymbolDefinition], source_path: Path | None) -> str:
    payload = []
    for item in defs:
        data = asdict(item)
        data["connectionPoints"] = [asdict(point) for point in item.connectionPoints]
        data["dataFields"] = [asdict(field) for field in item.dataFields]
        payload.append(data)

    source_comment = str(source_path) if source_path else "fallback/no-vsdx"
    json_payload = json.dumps(payload, ensure_ascii=False, indent=2)
    return f"""// Auto-generated by tools/build_vsdx_symbol_catalog.py
// Source: {source_comment}
// Do not edit manually.

export type VsdxSymbolDataField = {{
  id: string
  label: string
  type: string
  source: string
}}

export type VsdxSymbolConnectionPoint = {{
  id: string
  x: number | null
  y: number | null
}}

export type VsdxSymbolDefinition = {{
  id: string
  masterId: string
  title: string
  categoryId: string
  widthMm: number
  heightMm: number
  connectionCount: number
  shapeCount: number
  geometrySectionCount: number
  propertyNames: string[]
  userCellNames: string[]
  connectionPoints: VsdxSymbolConnectionPoint[]
  dataFields: VsdxSymbolDataField[]
  preview: string
  svgPreview: string
  status: 'planned'
  sourcePath: string
}}

export const vsdxSymbolDefinitions: VsdxSymbolDefinition[] = {json_payload}

export const vsdxSymbolCatalogSummary = {{
  source: {json.dumps(source_comment, ensure_ascii=False)},
  count: vsdxSymbolDefinitions.length,
}}
"""


def generated_md(defs: list[VsdxSymbolDefinition], source_path: Path | None) -> str:
    lines = [
        "# VSDX symbol catalog — generated",
        "",
        f"Source: `{source_path if source_path else 'fallback/no-vsdx'}`",
        "",
        f"Symbol count: **{len(defs)}**",
        "",
        "| Master | Title | Category | Size, mm | Ports | Shapes | Data fields | SVG preview |",
        "|---:|---|---|---:|---:|---:|---|---|",
    ]
    for item in defs:
        fields = ", ".join(field.label for field in item.dataFields[:4])
        if len(item.dataFields) > 4:
            fields += ", …"
        lines.append(
            f"| {item.masterId} | {item.title} | {item.categoryId} | "
            f"{item.widthMm:g} × {item.heightMm:g} | {item.connectionCount} | {item.shapeCount} | {fields} | yes |"
        )
    lines.append("")
    lines.append("The SVG previews are compact library previews. Exact insertable master rendering is the next renderer stage.")
    return "\n".join(lines) + "\n"


def write_csv(defs: list[VsdxSymbolDefinition], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(["masterId", "title", "categoryId", "widthMm", "heightMm", "connectionCount", "shapeCount", "geometrySectionCount", "propertyNames", "userCellNames", "dataFields", "hasSvgPreview"])
        for item in defs:
            writer.writerow([
                item.masterId,
                item.title,
                item.categoryId,
                item.widthMm,
                item.heightMm,
                item.connectionCount,
                item.shapeCount,
                item.geometrySectionCount,
                ";".join(item.propertyNames),
                ";".join(item.userCellNames),
                ";".join(field.id for field in item.dataFields),
                bool(item.svgPreview),
            ])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vsdx", type=Path, default=None)
    parser.add_argument("--ts-out", type=Path, required=True)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--csv-out", type=Path, required=True)
    parser.add_argument("--md-out", type=Path, required=True)
    args = parser.parse_args()

    source = args.vsdx if args.vsdx and args.vsdx.exists() else None
    defs = parse_vsdx(source) if source else fallback_defs()

    args.ts_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.md_out.parent.mkdir(parents=True, exist_ok=True)

    args.ts_out.write_text(generated_ts(defs, source), encoding="utf-8")
    args.json_out.write_text(json.dumps([asdict(item) for item in defs], ensure_ascii=False, indent=2), encoding="utf-8")
    args.md_out.write_text(generated_md(defs, source), encoding="utf-8")
    write_csv(defs, args.csv_out)

    print(f"VSDX_SYMBOL_COUNT={len(defs)}")
    print(f"VSDX_SVG_PREVIEW_COUNT={sum(1 for item in defs if item.svgPreview)}")
    if source:
        print(f"VSDX_SOURCE={source}")
    else:
        print("VSDX_SOURCE=fallback")
    for item in defs[:12]:
        print(f"{item.masterId};{item.title};{item.categoryId};{item.widthMm:g}x{item.heightMm:g}mm;ports={item.connectionCount};svg={bool(item.svgPreview)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
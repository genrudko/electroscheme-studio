#!/usr/bin/env python3
"""Convert Visio VSDX masters to reviewable ElectroScheme draft symbols.

This is a draft converter, not a final core-library importer.

Design rules:
- every generated symbol is `review_status = needs_review`;
- generated symbols are placed under symbols/imported/visio/needs_review;
- imported geometry is a first draft and keeps conversion warnings;
- terminals/connection points are preserved where coordinates can be resolved;
- voltage colorization, rotation, snap and stretch policies are present in metadata;
- no symbol is promoted to core automatically.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import re
import sys
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


VISIO_MAIN_NS = "http://schemas.microsoft.com/office/visio/2012/main"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
DOC_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

NS = {
    "v": VISIO_MAIN_NS,
    "rel": REL_NS,
}

KIND_RULES: list[tuple[str, list[str]]] = [
    ("busbar", ["шина", "шины", "ошинов", "токопровод", "шинный"]),
    ("circuit_breaker", ["выключатель", "автоматический выключатель", "вакуумный", "элегазовый"]),
    ("load_break_switch", ["выключатель нагрузки"]),
    ("disconnector", ["разъединитель", "отделитель"]),
    ("earthing_switch", ["заземляющий", "заземление", "зн"]),
    ("kru_trolley", ["тележка", "выкатн"]),
    ("fuse", ["предохранитель"]),
    ("surge_arrester", ["опн", "разрядник"]),
    ("transformer", ["трансформатор", "ат", "тсн", "тт", "тн"]),
    ("generator_motor", ["генератор", "двигатель", "дизель"]),
    ("reactor_compensation", ["реактор", "дгр", "компенсатор", "конденсатор", "укрм", "фильтр"]),
    ("line_grounding", ["лэп", "линия", "кабель", "кл", "вл", "заземл"]),
    ("stamp_frame", ["штамп", "рамка", "основная надпись"]),
    ("annotation", ["текст", "надпись", "граница", "опора", "стрелка"]),
]

STATE_KEYWORDS: dict[str, list[str]] = {
    "closed": ["включ", "closed"],
    "open": ["отключ", "open"],
    "unreliable": ["недостовер", "unknown", "invalid"],
    "repair": ["ремонт", "repair"],
    "test": ["контроль", "test"],
    "service": ["рабоч", "вкач", "service", "connected"],
    "withdrawn": ["выкач", "withdrawn"],
}

UNSUPPORTED_ROW_TYPES = {
    "SplineStart",
    "SplineKnot",
    "PolylineTo",
    "NURBSTo",
    "RelMoveTo",
    "RelLineTo",
    "RelCubBezTo",
    "InfiniteLine",
}


def read_xml(zf: zipfile.ZipFile, name: str) -> ET.Element | None:
    try:
        data = zf.read(name)
    except KeyError:
        return None

    try:
        return ET.fromstring(data)
    except ET.ParseError:
        return None


def strip_ns(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[-1]
    return tag


def rels_for(zf: zipfile.ZipFile, part_name: str) -> dict[str, str]:
    part = Path(part_name)
    rel_path = str(part.parent / "_rels" / f"{part.name}.rels").replace("\\", "/")
    root = read_xml(zf, rel_path)
    rels: dict[str, str] = {}
    if root is None:
        return rels

    base_dir = part.parent
    for rel in root.findall("rel:Relationship", NS):
        rel_id = rel.attrib.get("Id", "")
        target = rel.attrib.get("Target", "")
        if not rel_id or not target:
            continue
        if target.startswith("/"):
            normalized = target.lstrip("/")
        else:
            normalized = str((base_dir / target).as_posix())
        rels[rel_id] = normalized
    return rels


def text_of(cell: ET.Element | None) -> str:
    if cell is None:
        return ""
    value = cell.attrib.get("V")
    if value is not None:
        return value
    return "".join(cell.itertext()).strip()


def cell_formula(cell: ET.Element | None) -> str:
    if cell is None:
        return ""
    return cell.attrib.get("F", "")


def direct_cell(parent: ET.Element, name: str) -> ET.Element | None:
    for cell in parent.findall("v:Cell", NS):
        if cell.attrib.get("N") == name:
            return cell
    return None


def find_cell(parent: ET.Element, name: str) -> ET.Element | None:
    direct = direct_cell(parent, name)
    if direct is not None:
        return direct
    for cell in parent.findall(".//v:Cell", NS):
        if cell.attrib.get("N") == name:
            return cell
    return None


def parse_float(value: str) -> float | None:
    if value is None:
        return None
    value = str(value).strip()
    if not value:
        return None
    value = value.replace(",", ".")
    try:
        result = float(value)
    except ValueError:
        return None
    if math.isfinite(result):
        return result
    return None


def cell_float(parent: ET.Element, name: str) -> float | None:
    return parse_float(text_of(find_cell(parent, name)))


def row_float(row: ET.Element, name: str) -> float | None:
    return parse_float(text_of(direct_cell(row, name)))


def normalize_name(value: str) -> str:
    value = value.strip()
    if not value:
        return "unnamed"
    replacements = {
        "ё": "е",
        "Ё": "Е",
        "№": "n",
        " ": "_",
        "-": "_",
        "/": "_",
        "\\": "_",
        "(": "",
        ")": "",
        ",": "",
        ".": "",
        ":": "",
        ";": "",
        "«": "",
        "»": "",
        '"': "",
        "'": "",
        "+": "plus",
        "=": "",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    value = re.sub(r"[^0-9A-Za-zА-Яа-я_]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value.lower() or "unnamed"


def classify_kind(name: str, page_names: list[str] | None = None) -> str:
    page_text = " ".join(page_names or [])
    haystack = f"{name} {page_text}".lower()
    for kind, keywords in KIND_RULES:
        if any(keyword in haystack for keyword in keywords):
            return kind
    return "unknown"


def detect_state_tokens(name: str) -> list[str]:
    haystack = name.lower()
    result: list[str] = []
    for state_id, keywords in STATE_KEYWORDS.items():
        if any(keyword in haystack for keyword in keywords):
            result.append(state_id)
    return result


def is_switching_kind(kind: str) -> bool:
    return kind in {
        "circuit_breaker",
        "load_break_switch",
        "disconnector",
        "earthing_switch",
        "kru_trolley",
    }


def collect_pages(zf: zipfile.ZipFile) -> tuple[list[dict[str, Any]], dict[str, list[str]]]:
    pages_root = read_xml(zf, "visio/pages/pages.xml")
    pages: list[dict[str, Any]] = []
    master_usage: dict[str, list[str]] = {}
    if pages_root is None:
        return pages, master_usage

    rels = rels_for(zf, "visio/pages/pages.xml")
    for page in pages_root.findall(".//v:Page", NS):
        page_id = page.attrib.get("ID", "")
        page_name = page.attrib.get("NameU") or page.attrib.get("Name") or f"Page {page_id}"
        rel_id = ""
        for child in page:
            if strip_ns(child.tag) == "Rel":
                rel_id = child.attrib.get(f"{{{DOC_REL_NS}}}id", "") or child.attrib.get("r:id", "")
        page_part = rels.get(rel_id, "") if rel_id else ""

        shape_count = 0
        refs: dict[str, int] = {}
        if page_part:
            root = read_xml(zf, page_part)
            if root is not None:
                shapes = root.findall(".//v:Shape", NS)
                shape_count = len(shapes)
                for shape in shapes:
                    master_id = shape.attrib.get("Master", "")
                    if master_id:
                        refs[master_id] = refs.get(master_id, 0) + 1
                        master_usage.setdefault(master_id, []).append(page_name)

        pages.append(
            {
                "id": page_id,
                "name": page_name,
                "part": page_part,
                "shape_count": shape_count,
                "shape_master_refs": refs,
            }
        )

    for key, values in list(master_usage.items()):
        master_usage[key] = sorted(set(values))
    return pages, master_usage


def collect_master_index(zf: zipfile.ZipFile) -> list[dict[str, str]]:
    masters_root = read_xml(zf, "visio/masters/masters.xml")
    if masters_root is None:
        return []

    rels = rels_for(zf, "visio/masters/masters.xml")
    result: list[dict[str, str]] = []
    for master in masters_root.findall(".//v:Master", NS):
        master_id = master.attrib.get("ID", "")
        name = master.attrib.get("NameU") or master.attrib.get("Name") or f"Master {master_id}"
        rel_id = ""
        for child in master:
            if strip_ns(child.tag) == "Rel":
                rel_id = child.attrib.get(f"{{{DOC_REL_NS}}}id", "") or child.attrib.get("r:id", "")
        part = rels.get(rel_id, "") if rel_id else ""
        result.append({"id": master_id, "name": name, "part": part})
    return result


def shape_sections(shape: ET.Element) -> dict[str, list[ET.Element]]:
    sections: dict[str, list[ET.Element]] = {}
    for section in shape.findall("v:Section", NS):
        name = section.attrib.get("N", "")
        if name:
            sections.setdefault(name, []).append(section)
    return sections


def shape_dimensions(shape: ET.Element) -> dict[str, float]:
    width = cell_float(shape, "Width")
    height = cell_float(shape, "Height")
    pin_x = cell_float(shape, "PinX")
    pin_y = cell_float(shape, "PinY")
    angle = cell_float(shape, "Angle")
    return {
        "width": width if width and width > 0 else 1.0,
        "height": height if height and height > 0 else 1.0,
        "pin_x": pin_x if pin_x is not None else 0.0,
        "pin_y": pin_y if pin_y is not None else 0.0,
        "angle": angle if angle is not None else 0.0,
    }


def collect_text(shape: ET.Element) -> str:
    values: list[str] = []
    for text_node in shape.findall(".//v:Text", NS):
        value = "".join(text_node.itertext()).strip()
        if value:
            values.append(value)
    return " ".join(values)


def transform_point(x: float, y: float, width: float, height: float) -> tuple[float, float]:
    return (x, height - y)


def fmt_num(value: float) -> str:
    if abs(value) < 1e-9:
        value = 0.0
    return f"{value:.6g}"


def path_style() -> str:
    return 'stroke="var(--voltage-color, currentColor)" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"'


def fill_style() -> str:
    return 'stroke="var(--voltage-color, currentColor)" fill="none" stroke-width="1.5" vector-effect="non-scaling-stroke"'


def convert_geometry_sections(shape: ET.Element, base_width: float, base_height: float) -> tuple[list[str], list[str], dict[str, int]]:
    warnings: list[str] = []
    elements: list[str] = []
    row_counts: dict[str, int] = {}

    sections = shape_sections(shape)
    geom_sections = [section for name, group in sections.items() if name.startswith("Geometry") for section in group]
    if not geom_sections:
        return elements, ["no Geometry section on shape"], row_counts

    for section_index, section in enumerate(geom_sections, start=1):
        commands: list[str] = []
        for row in section.findall("v:Row", NS):
            row_type = row.attrib.get("T") or row.attrib.get("N") or "Row"
            row_counts[row_type] = row_counts.get(row_type, 0) + 1

            x = row_float(row, "X")
            y = row_float(row, "Y")

            if row_type in {"MoveTo", "LineTo", "ArcTo", "EllipticalArcTo"} and x is not None and y is not None:
                sx, sy = transform_point(x, y, base_width, base_height)
                if row_type == "MoveTo":
                    commands.append(f"M {fmt_num(sx)} {fmt_num(sy)}")
                elif row_type == "LineTo":
                    commands.append(f"L {fmt_num(sx)} {fmt_num(sy)}")
                else:
                    commands.append(f"L {fmt_num(sx)} {fmt_num(sy)}")
                    warnings.append(f"{row_type} converted as line fallback")
                continue

            if row_type == "Ellipse":
                cx = row_float(row, "X")
                cy = row_float(row, "Y")
                ax = row_float(row, "A")
                ay = row_float(row, "B")
                if cx is not None and cy is not None:
                    sx, sy = transform_point(cx, cy, base_width, base_height)
                    rx = abs((ax if ax is not None else cx + base_width * 0.2) - cx)
                    ry = abs((ay if ay is not None else cy + base_height * 0.2) - cy)
                    if rx <= 0:
                        rx = max(base_width * 0.15, 0.05)
                    if ry <= 0:
                        ry = max(base_height * 0.15, 0.05)
                    elements.append(
                        f'<ellipse cx="{fmt_num(sx)}" cy="{fmt_num(sy)}" rx="{fmt_num(rx)}" ry="{fmt_num(ry)}" {fill_style()} />'
                    )
                else:
                    warnings.append("Ellipse row without numeric center")
                continue

            if row_type == "NoFill" or row_type == "NoLine":
                continue

            if row_type in UNSUPPORTED_ROW_TYPES:
                warnings.append(f"unsupported geometry row: {row_type}")
                continue

            warnings.append(f"unhandled geometry row: {row_type}")

        if commands:
            d = " ".join(commands)
            elements.append(f'<path d="{html.escape(d, quote=True)}" {path_style()} data-geometry-section="{section_index}" />')

    return elements, warnings, row_counts


def collect_connection_points(shape: ET.Element, base_width: float, base_height: float) -> tuple[list[dict[str, Any]], list[str]]:
    terminals: list[dict[str, Any]] = []
    warnings: list[str] = []
    sections = shape_sections(shape)
    cp_index = 1
    for section in sections.get("Connection", []):
        for row in section.findall("v:Row", NS):
            x_cell = direct_cell(row, "X")
            y_cell = direct_cell(row, "Y")
            x = parse_float(text_of(x_cell))
            y = parse_float(text_of(y_cell))
            raw_x = text_of(x_cell)
            raw_y = text_of(y_cell)
            terminal: dict[str, Any] = {
                "id": row.attrib.get("N") or f"t{cp_index}",
                "role": "terminal",
                "source": "visio_connection_point",
                "raw": {
                    "x": raw_x,
                    "y": raw_y,
                    "formula_x": cell_formula(x_cell),
                    "formula_y": cell_formula(y_cell),
                },
            }
            if x is not None and y is not None:
                sx, sy = transform_point(x, y, base_width, base_height)
                terminal["x"] = sx
                terminal["y"] = sy
            else:
                terminal["needs_review"] = True
                warnings.append(f"connection point {terminal['id']} has non-numeric coordinates")
            terminals.append(terminal)
            cp_index += 1
    return terminals, warnings


def choose_geometry_shapes(root: ET.Element) -> list[ET.Element]:
    all_shapes = root.findall(".//v:Shape", NS)
    if not all_shapes:
        return []
    with_geom = []
    for shape in all_shapes:
        sections = shape_sections(shape)
        if any(name.startswith("Geometry") for name in sections):
            with_geom.append(shape)
    if with_geom:
        return with_geom
    return [all_shapes[0]]


def find_base_shape(root: ET.Element) -> ET.Element | None:
    shapes = root.findall(".//v:Shape", NS)
    if not shapes:
        return None
    for shape in shapes:
        dims = shape_dimensions(shape)
        if dims["width"] > 0 and dims["height"] > 0:
            return shape
    return shapes[0]


def make_capabilities(kind: str, state_tokens: list[str], terminal_count: int, row_counts: dict[str, int]) -> dict[str, Any]:
    multi_state = is_switching_kind(kind) or bool(state_tokens)
    busbar = kind == "busbar"
    stretchable = kind in {"busbar", "line_grounding"} or row_counts.get("LineTo", 0) >= 2
    return {
        "feature_flags": {
            "colorizable_by_voltage_class": True,
            "multi_state_candidate": multi_state,
            "busbar_configurable_connection_points": busbar,
            "rotatable": True,
            "snap_anchors_required": True,
            "stretchable_leads_candidate": stretchable,
            "auto_layout_eligible": kind not in {"stamp_frame", "annotation"},
            "requires_review": True,
        },
        "rotation": {
            "enabled": True,
            "allowed_degrees": [0, 90, 180, 270],
            "terminal_transform_required": True,
            "snap_anchor_transform_required": True,
            "label_rotation_policy": "keep_readable",
        },
        "stretching": {
            "enabled": stretchable,
            "body_geometry_locked": True,
            "stretchable_parts": ["connection_leads", "busbar_length"] if stretchable else [],
        },
        "snapping": {
            "enabled": True,
            "terminal_count": terminal_count,
            "snap_to_terminals": True,
            "snap_to_busbar_generated_points": busbar,
            "connection_graph_node_required": True,
        },
        "voltage_style": {
            "enabled": True,
            "stroke_token": "var(--voltage-color)",
            "normal_scheme_palette": "STO table 1",
            "ptk_palette": "STO table 5",
        },
        "states": {
            "enabled": multi_state,
            "detected_tokens": state_tokens,
            "required_for_switching_device": ["closed", "open", "unreliable", "repair"] if multi_state else [],
            "kru_trolley_extra_states": [
                "breaker_closed_trolley_service",
                "breaker_open_trolley_service",
                "breaker_unreliable_trolley_service",
                "trolley_withdrawn_repair",
                "trolley_withdrawn_test",
            ] if kind == "kru_trolley" else [],
        },
        "busbar": {
            "enabled": busbar,
            "connection_point_count": max(terminal_count, 2) if busbar else 0,
            "connection_spacing": "parameterized" if busbar else None,
            "length": "parameterized" if busbar else "fixed",
            "stroke_width_multiplier": 4 if busbar else None,
        },
    }


def convert_master(zf: zipfile.ZipFile, master: dict[str, str], page_usage: list[str]) -> dict[str, Any] | None:
    part = master.get("part", "")
    if not part:
        return None
    root = read_xml(zf, part)
    if root is None:
        return None

    base_shape = find_base_shape(root)
    if base_shape is None:
        return None

    dims = shape_dimensions(base_shape)
    width = max(dims["width"], 1.0)
    height = max(dims["height"], 1.0)
    name = master["name"]
    normalized = normalize_name(name)
    symbol_id = f"visio_{master['id']}_{normalized}"
    kind = classify_kind(name, page_usage)
    state_tokens = detect_state_tokens(name)

    geometry_shapes = choose_geometry_shapes(root)
    svg_elements: list[str] = []
    warnings: list[str] = []
    combined_row_counts: dict[str, int] = {}

    if len(geometry_shapes) > 1:
        warnings.append("multiple Visio shapes flattened without full local transform support")

    for shape in geometry_shapes:
        elements, shape_warnings, row_counts = convert_geometry_sections(shape, width, height)
        svg_elements.extend(elements)
        warnings.extend(shape_warnings)
        for key, count in row_counts.items():
            combined_row_counts[key] = combined_row_counts.get(key, 0) + count

    terminals, terminal_warnings = collect_connection_points(base_shape, width, height)
    warnings.extend(terminal_warnings)

    if not svg_elements:
        warnings.append("no SVG elements generated; placeholder bounding box used")
        svg_elements.append(f'<rect x="0" y="0" width="{fmt_num(width)}" height="{fmt_num(height)}" stroke-dasharray="3 2" {fill_style()} />')

    text = collect_text(base_shape)
    capabilities = make_capabilities(kind, state_tokens, len(terminals), combined_row_counts)

    symbol = {
        "schema_version": "draft-0.1",
        "id": symbol_id,
        "name_ru": name,
        "name_en": "",
        "category": kind,
        "review_status": "needs_review",
        "source": {
            "format": "vsdx",
            "master_id": master["id"],
            "master_name": name,
            "master_part": part,
            "page_usage": page_usage,
            "text": text,
        },
        "viewBox": {
            "x": 0,
            "y": 0,
            "width": width,
            "height": height,
        },
        "svg_fragment": "\n".join(svg_elements),
        "terminals": terminals,
        "snap_anchors": terminals,
        "capabilities": capabilities,
        "conversion": {
            "row_counts": combined_row_counts,
            "warnings": sorted(set(warnings)),
            "requires_manual_review": True,
            "known_limitations": [
                "local transforms and group transforms are not fully normalized yet",
                "advanced arcs/splines may use line fallback",
                "imported symbols are drafts only",
            ],
        },
    }
    return symbol


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def read_symbol(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def cleanup_old_drafts(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for path in out_dir.glob("*.symbol.json"):
        path.unlink()


def write_preview(preview_path: Path, symbols: list[dict[str, Any]]) -> None:
    cell_w = 190
    cell_h = 150
    cols = 4
    rows = max(1, math.ceil(len(symbols) / cols))
    width = cell_w * cols
    height = cell_h * rows

    parts: list[str] = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    parts.append('<rect width="100%" height="100%" fill="white"/>')
    parts.append('<style>text{font-family:Arial,sans-serif;font-size:10px;fill:#111}.cell{fill:none;stroke:#ddd;stroke-width:1}.warn{fill:#b00020}.symbol{color:#5f5f5f;--voltage-color:#5f5f5f}</style>')

    for index, symbol in enumerate(symbols):
        col = index % cols
        row = index // cols
        x = col * cell_w
        y = row * cell_h
        vb = symbol.get("viewBox", {})
        vb_w = float(vb.get("width") or 1.0)
        vb_h = float(vb.get("height") or 1.0)
        scale = min((cell_w - 30) / vb_w, (cell_h - 50) / vb_h)
        if scale <= 0 or not math.isfinite(scale):
            scale = 1.0
        tx = x + 15
        ty = y + 15
        name = html.escape(str(symbol.get("name_ru", "")))
        sid = html.escape(str(symbol.get("id", "")))
        warn_count = len(symbol.get("conversion", {}).get("warnings", []))
        parts.append(f'<g transform="translate({x},{y})">')
        parts.append(f'<rect class="cell" x="0" y="0" width="{cell_w}" height="{cell_h}"/>')
        parts.append(f'<g class="symbol" transform="translate({tx - x},{ty - y}) scale({fmt_num(scale)})">')
        parts.append(symbol.get("svg_fragment", ""))
        parts.append("</g>")
        parts.append(f'<text x="8" y="{cell_h - 25}">{name[:60]}</text>')
        parts.append(f'<text x="8" y="{cell_h - 12}">{sid[:70]}</text>')
        if warn_count:
            parts.append(f'<text class="warn" x="{cell_w - 55}" y="15">warn:{warn_count}</text>')
        parts.append("</g>")

    parts.append("</svg>")
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    preview_path.write_text("\n".join(parts) + "\n", encoding="utf-8")


def write_readme(path: Path, summary: dict[str, Any]) -> None:
    lines: list[str] = []
    lines.append("# Imported Visio draft symbols")
    lines.append("")
    lines.append("These files are generated draft symbols from Visio VSDX masters.")
    lines.append("")
    lines.append("They are **not** core library symbols yet.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    for key in [
        "source",
        "masters_total",
        "draft_symbols_written",
        "symbols_with_terminals",
        "symbols_with_warnings",
        "preview",
    ]:
        lines.append(f"- {key}: `{summary.get(key)}`")
    lines.append("")
    lines.append("## Review workflow")
    lines.append("")
    lines.append("1. Open `preview.svg`.")
    lines.append("2. Review geometry per symbol.")
    lines.append("3. Check terminals/snap anchors.")
    lines.append("4. Map switching-device states.")
    lines.append("5. Convert accepted drafts into reviewed SymbolDefinition files.")
    lines.append("")
    lines.append("## Important")
    lines.append("")
    lines.append("- Busbars require parameterization.")
    lines.append("- Switching devices require explicit state variants.")
    lines.append("- Rotation, stretching and voltage colorization must be validated before core promotion.")
    lines.append("- Group/local transforms are still first-draft and may require manual correction.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def convert(vsdx: Path, out_dir: Path, index_path: Path, preview_path: Path, summary_path: Path) -> dict[str, Any]:
    if not vsdx.exists():
        raise FileNotFoundError(vsdx)

    cleanup_old_drafts(out_dir)

    with zipfile.ZipFile(vsdx, "r") as zf:
        pages, master_usage = collect_pages(zf)
        master_index = collect_master_index(zf)
        symbols: list[dict[str, Any]] = []
        failures: list[dict[str, str]] = []

        for master in master_index:
            try:
                symbol = convert_master(zf, master, master_usage.get(master["id"], []))
            except Exception as exc:  # noqa: BLE001
                failures.append({"master_id": master.get("id", ""), "name": master.get("name", ""), "error": str(exc)})
                continue
            if symbol is None:
                failures.append({"master_id": master.get("id", ""), "name": master.get("name", ""), "error": "not convertible"})
                continue
            symbols.append(symbol)

    symbols.sort(key=lambda item: str(item["id"]))
    for symbol in symbols:
        write_json(out_dir / f"{symbol['id']}.symbol.json", symbol)

    index = {
        "schema_version": "draft-index-0.1",
        "source": str(vsdx),
        "review_status": "needs_review",
        "symbols": [
            {
                "id": symbol["id"],
                "name_ru": symbol["name_ru"],
                "category": symbol["category"],
                "path": f"needs_review/{symbol['id']}.symbol.json",
                "warning_count": len(symbol.get("conversion", {}).get("warnings", [])),
                "terminal_count": len(symbol.get("terminals", [])),
            }
            for symbol in symbols
        ],
        "failures": failures,
    }
    write_json(index_path, index)
    write_preview(preview_path, symbols)

    summary = {
        "source": str(vsdx),
        "pages_total": len(pages),
        "masters_total": len(master_index),
        "draft_symbols_written": len(symbols),
        "conversion_failures": len(failures),
        "symbols_with_terminals": sum(1 for symbol in symbols if symbol.get("terminals")),
        "symbols_with_warnings": sum(1 for symbol in symbols if symbol.get("conversion", {}).get("warnings")),
        "preview": str(preview_path),
        "out_dir": str(out_dir),
        "index": str(index_path),
    }
    write_json(summary_path, summary)
    write_readme(index_path.parent / "README.md", summary)
    return summary


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Convert Visio VSDX masters to draft symbol JSON files.")
    parser.add_argument("vsdx", type=Path)
    parser.add_argument("--out", type=Path, default=Path("symbols/imported/visio/needs_review"))
    parser.add_argument("--index", type=Path, default=Path("symbols/imported/visio/index.json"))
    parser.add_argument("--preview", type=Path, default=Path("symbols/imported/visio/preview.svg"))
    parser.add_argument("--summary", type=Path, default=Path("symbols/imported/visio/conversion_summary.json"))
    args = parser.parse_args(argv)

    summary = convert(args.vsdx, args.out, args.index, args.preview, args.summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if summary["draft_symbols_written"] <= 0:
        print("No draft symbols generated", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
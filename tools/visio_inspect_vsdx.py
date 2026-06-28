#!/usr/bin/env python3
"""Inspect Visio VSDX files for ElectroScheme Studio symbol import.

This tool is intentionally an inspector, not a final importer.

It preserves important semantics that must not be lost:
- multi-state switching devices;
- KRU trolley state/position combinations;
- configurable busbar connection points;
- voltage-class colorization;
- rotation-safe terminals and anchors;
- stretchable connection leads without body distortion;
- snap anchors for fast figure-to-figure binding;
- future automatic scheme generation from equipment lists.
"""

from __future__ import annotations

import argparse
import csv
import json
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


VOLTAGE_CLASSES = [
    {"id": "1150kv", "label": "1150 кВ", "normal_rgb": [205, 138, 255], "ptk_rgb": None},
    {"id": "800_750kv", "label": "800/750 кВ", "normal_rgb": [0, 0, 168], "ptk_rgb": [50, 100, 255]},
    {"id": "500kv", "label": "500 кВ", "normal_rgb": [213, 0, 0], "ptk_rgb": [213, 0, 0]},
    {"id": "400kv", "label": "400 кВ", "normal_rgb": [255, 100, 30], "ptk_rgb": [255, 100, 30]},
    {"id": "330kv", "label": "330 кВ", "normal_rgb": [0, 170, 0], "ptk_rgb": [0, 170, 0]},
    {"id": "220kv", "label": "220 кВ", "normal_rgb": [255, 210, 0], "ptk_rgb": [255, 210, 0]},
    {"id": "150kv", "label": "150 кВ", "normal_rgb": None, "ptk_rgb": [205, 138, 255]},
    {"id": "110kv", "label": "110 кВ", "normal_rgb": [0, 153, 255], "ptk_rgb": [60, 160, 255]},
    {"id": "35_6kv", "label": "0,4–35 кВ / 6–35 кВ", "normal_rgb": [95, 95, 95], "ptk_rgb": None},
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


def text_of(cell: ET.Element | None) -> str:
    if cell is None:
        return ""
    value = cell.attrib.get("V")
    if value is not None:
        return value
    return "".join(cell.itertext()).strip()


def find_cell(parent: ET.Element, name: str) -> ET.Element | None:
    for cell in parent.findall(".//v:Cell", NS):
        if cell.attrib.get("N") == name:
            return cell
    return None


def normalize_name(name: str) -> str:
    name = name.strip()
    if not name:
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
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    name = re.sub(r"[^0-9A-Za-zА-Яа-я_]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name.lower() or "unnamed"


def classify_kind(name: str, page_name: str = "") -> str:
    haystack = f"{name} {page_name}".lower()
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


def is_multistate_candidate(kind: str, name: str) -> bool:
    if kind in {"circuit_breaker", "load_break_switch", "disconnector", "earthing_switch", "kru_trolley"}:
        return True
    return bool(detect_state_tokens(name))


def is_busbar_configurable_candidate(kind: str, name: str, connection_count: int) -> bool:
    if kind != "busbar":
        return False
    return connection_count >= 2 or any(token in name.lower() for token in ["шина", "ошинов", "токопровод"])


def is_stretchable_lead_candidate(kind: str, name: str, geometry_row_counts: dict[str, int]) -> bool:
    haystack = name.lower()
    if kind in {"line_grounding", "busbar"}:
        return True
    if any(token in haystack for token in ["линия", "кабель", "ошинов", "провод", "соедин"]):
        return True
    return int(geometry_row_counts.get("LineTo", 0)) >= 2


def shape_sections(shape: ET.Element) -> dict[str, list[ET.Element]]:
    sections: dict[str, list[ET.Element]] = {}
    for section in shape.findall("v:Section", NS):
        name = section.attrib.get("N", "")
        if not name:
            continue
        sections.setdefault(name, []).append(section)
    return sections


def geometry_stats(shape: ET.Element) -> dict[str, Any]:
    sections = shape_sections(shape)
    geometry_sections = [s for name, section_list in sections.items() if name.startswith("Geometry") for s in section_list]
    row_counts: dict[str, int] = {}
    formula_cells = 0
    for section in geometry_sections:
        for row in section.findall("v:Row", NS):
            row_name = row.attrib.get("T") or row.attrib.get("N") or "Row"
            row_counts[row_name] = row_counts.get(row_name, 0) + 1
            for cell in row.findall("v:Cell", NS):
                if "F" in cell.attrib:
                    formula_cells += 1

    return {
        "geometry_section_count": len(geometry_sections),
        "geometry_row_counts": row_counts,
        "geometry_row_total": sum(row_counts.values()),
        "formula_cell_count": formula_cells,
        "has_geometry": len(geometry_sections) > 0,
    }


def connection_points(shape: ET.Element) -> list[dict[str, Any]]:
    points: list[dict[str, Any]] = []
    sections = shape_sections(shape)
    for section in sections.get("Connection", []):
        for index, row in enumerate(section.findall("v:Row", NS), start=1):
            x = text_of(find_cell(row, "X"))
            y = text_of(find_cell(row, "Y"))
            dir_x = text_of(find_cell(row, "DirX"))
            dir_y = text_of(find_cell(row, "DirY"))
            points.append(
                {
                    "id": row.attrib.get("N") or f"cp{index}",
                    "x": x,
                    "y": y,
                    "dir_x": dir_x,
                    "dir_y": dir_y,
                    "raw_name": row.attrib.get("N", ""),
                    "role": "snap_anchor",
                }
            )
    return points


def shape_dimensions(shape: ET.Element) -> dict[str, str]:
    return {
        "pin_x": text_of(find_cell(shape, "PinX")),
        "pin_y": text_of(find_cell(shape, "PinY")),
        "width": text_of(find_cell(shape, "Width")),
        "height": text_of(find_cell(shape, "Height")),
        "angle": text_of(find_cell(shape, "Angle")),
    }


def collect_text(shape: ET.Element) -> str:
    texts: list[str] = []
    for text in shape.findall(".//v:Text", NS):
        t = "".join(text.itertext()).strip()
        if t:
            texts.append(t)
    return " ".join(texts)


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


def collect_pages(zf: zipfile.ZipFile) -> tuple[list[dict[str, Any]], dict[str, str]]:
    pages_root = read_xml(zf, "visio/pages/pages.xml")
    pages: list[dict[str, Any]] = []
    page_id_to_name: dict[str, str] = {}
    if pages_root is None:
        return pages, page_id_to_name

    rels = rels_for(zf, "visio/pages/pages.xml")
    for page in pages_root.findall(".//v:Page", NS):
        page_id = page.attrib.get("ID", "")
        page_name = page.attrib.get("NameU") or page.attrib.get("Name") or f"Page {page_id}"
        rel_id = ""
        page_part = ""
        for child in page:
            if strip_ns(child.tag) == "Rel":
                rel_id = child.attrib.get(f"{{{DOC_REL_NS}}}id", "") or child.attrib.get("r:id", "")
        if rel_id:
            page_part = rels.get(rel_id, "")

        page_report: dict[str, Any] = {
            "id": page_id,
            "name": page_name,
            "part": page_part,
            "shape_count": 0,
            "shape_master_refs": {},
            "shape_names": [],
        }

        if page_part:
            page_root = read_xml(zf, page_part)
            if page_root is not None:
                shapes = page_root.findall(".//v:Shape", NS)
                page_report["shape_count"] = len(shapes)
                refs: dict[str, int] = {}
                names: list[str] = []
                for shape in shapes:
                    master = shape.attrib.get("Master", "")
                    if master:
                        refs[master] = refs.get(master, 0) + 1
                    nm = shape.attrib.get("NameU") or shape.attrib.get("Name") or shape.attrib.get("ID", "")
                    if nm:
                        names.append(nm)
                page_report["shape_master_refs"] = refs
                page_report["shape_names"] = names[:100]

        pages.append(page_report)
        if page_id:
            page_id_to_name[page_id] = page_name

    return pages, page_id_to_name


def collect_masters(zf: zipfile.ZipFile) -> list[dict[str, Any]]:
    masters_root = read_xml(zf, "visio/masters/masters.xml")
    if masters_root is None:
        return []

    rels = rels_for(zf, "visio/masters/masters.xml")
    masters: list[dict[str, Any]] = []

    for master in masters_root.findall(".//v:Master", NS):
        master_id = master.attrib.get("ID", "")
        name = master.attrib.get("NameU") or master.attrib.get("Name") or f"Master {master_id}"
        rel_id = ""
        master_part = ""

        for child in master:
            if strip_ns(child.tag) == "Rel":
                rel_id = child.attrib.get(f"{{{DOC_REL_NS}}}id", "") or child.attrib.get("r:id", "")

        if rel_id:
            master_part = rels.get(rel_id, "")

        master_report: dict[str, Any] = {
            "id": master_id,
            "name": name,
            "normalized_id": normalize_name(name),
            "part": master_part,
            "kind": classify_kind(name),
            "text": "",
            "shape_count": 0,
            "top_shape_name": "",
            "dimensions": {},
            "geometry": {
                "geometry_section_count": 0,
                "geometry_row_counts": {},
                "geometry_row_total": 0,
                "formula_cell_count": 0,
                "has_geometry": False,
            },
            "connection_points": [],
            "connection_point_count": 0,
            "state_tokens": detect_state_tokens(name),
            "feature_flags": {},
            "capabilities": {},
            "import_status": "needs_review",
            "warnings": [],
        }

        if master_part:
            root = read_xml(zf, master_part)
            if root is not None:
                shapes = root.findall(".//v:Shape", NS)
                master_report["shape_count"] = len(shapes)

                target_shape = shapes[0] if shapes else None
                if target_shape is not None:
                    master_report["top_shape_name"] = (
                        target_shape.attrib.get("NameU")
                        or target_shape.attrib.get("Name")
                        or target_shape.attrib.get("ID", "")
                    )
                    master_report["dimensions"] = shape_dimensions(target_shape)
                    master_report["text"] = collect_text(target_shape)
                    geom = geometry_stats(target_shape)
                    master_report["geometry"] = geom
                    cps = connection_points(target_shape)
                    master_report["connection_points"] = cps
                    master_report["connection_point_count"] = len(cps)

                    if not geom["has_geometry"]:
                        master_report["warnings"].append("top shape has no Geometry section")
                    if len(cps) == 0:
                        master_report["warnings"].append("no connection points on top shape")
                else:
                    master_report["warnings"].append("master part has no shapes")
        else:
            master_report["warnings"].append("master part not resolved")

        kind = classify_kind(master_report["name"], "")
        master_report["kind"] = kind

        row_counts = master_report.get("geometry", {}).get("geometry_row_counts", {})
        cp_count = int(master_report.get("connection_point_count", 0) or 0)

        master_report["feature_flags"] = {
            "multi_state_candidate": is_multistate_candidate(kind, str(master_report["name"])),
            "busbar_configurable_connection_points": is_busbar_configurable_candidate(kind, str(master_report["name"]), cp_count),
            "voltage_colorizable": True,
            "rotatable": True,
            "snap_anchors_required": True,
            "stretchable_leads_candidate": is_stretchable_lead_candidate(kind, str(master_report["name"]), row_counts),
            "auto_layout_eligible": kind not in {"stamp_frame", "annotation"},
            "requires_review": True,
        }

        master_report["capabilities"] = {
            "rotation": {
                "enabled": True,
                "allowed_degrees": [0, 90, 180, 270],
                "terminal_transform_required": True,
                "label_rotation_policy": "keep_readable",
            },
            "scaling": {
                "uniform_scale": True,
                "non_uniform_scale": False,
                "do_not_distort_symbol_body": True,
            },
            "stretching": {
                "enabled": bool(master_report["feature_flags"]["stretchable_leads_candidate"]),
                "stretchable_parts": ["connection_leads", "busbar_length"] if master_report["feature_flags"]["stretchable_leads_candidate"] else [],
                "body_geometry_locked": True,
            },
            "snapping": {
                "enabled": True,
                "snap_to_terminals": True,
                "snap_to_busbar_generated_points": kind == "busbar",
                "connection_graph_node_required": True,
            },
            "voltage_style": {
                "enabled": True,
                "stroke_token": "var(--voltage-color)",
                "normal_scheme_palette": "STO table 1",
                "ptk_palette": "STO table 5",
            },
        }

        masters.append(master_report)

    return masters


def attach_page_usage(masters: list[dict[str, Any]], pages: list[dict[str, Any]]) -> None:
    usage: dict[str, list[str]] = {}
    for page in pages:
        page_name = page.get("name", "")
        refs = page.get("shape_master_refs", {})
        if isinstance(refs, dict):
            for master_id in refs:
                usage.setdefault(str(master_id), []).append(page_name)

    for master in masters:
        master_id = str(master.get("id", ""))
        page_names = usage.get(master_id, [])
        master["page_usage"] = page_names
        if page_names and master.get("kind") == "unknown":
            master["kind"] = classify_kind(str(master.get("name", "")), " ".join(page_names))

        kind = str(master.get("kind", "unknown"))
        row_counts = master.get("geometry", {}).get("geometry_row_counts", {})
        cp_count = int(master.get("connection_point_count", 0) or 0)
        flags = master.setdefault("feature_flags", {})
        flags["multi_state_candidate"] = is_multistate_candidate(kind, str(master.get("name", "")))
        flags["busbar_configurable_connection_points"] = is_busbar_configurable_candidate(kind, str(master.get("name", "")), cp_count)
        flags["stretchable_leads_candidate"] = is_stretchable_lead_candidate(kind, str(master.get("name", "")), row_counts)
        flags["auto_layout_eligible"] = kind not in {"stamp_frame", "annotation"}


def build_import_candidates(masters: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for master in masters:
        flags = master.get("feature_flags", {})
        warnings = list(master.get("warnings", []))

        if master.get("geometry", {}).get("has_geometry") is not True:
            warnings.append("cannot convert until geometry extraction supports this master structure")

        kind = str(master.get("kind", "unknown"))
        is_busbar = bool(flags.get("busbar_configurable_connection_points"))
        is_multistate = bool(flags.get("multi_state_candidate"))

        candidates.append(
            {
                "source_master_id": master.get("id"),
                "source_name": master.get("name"),
                "symbol_id": master.get("normalized_id"),
                "kind": kind,
                "page_usage": master.get("page_usage", []),
                "review_status": "needs_review",
                "do_not_promote_to_core_without_manual_review": True,
                "color_policy": {
                    "colorizable_by_voltage_class": True,
                    "stroke_token": "var(--voltage-color)",
                    "fill_token": "none_or_state_dependent",
                    "normal_scheme_palette_source": "STO 56947007-29.240.10.035-2009 table 1",
                    "ptk_palette_source": "STO 56947007-29.240.10.035-2009 table 5",
                },
                "transform_policy": {
                    "rotatable": True,
                    "allowed_rotation_degrees": [0, 90, 180, 270],
                    "terminal_transform_required": True,
                    "snap_anchor_transform_required": True,
                    "label_rotation_policy": "keep_readable",
                    "uniform_scaling_allowed": True,
                    "non_uniform_symbol_body_scaling_allowed": False,
                },
                "stretch_policy": {
                    "stretchable": bool(flags.get("stretchable_leads_candidate")),
                    "stretchable_parts": ["connection_leads", "generated_busbar_segments"] if flags.get("stretchable_leads_candidate") else [],
                    "body_geometry_locked": True,
                    "lead_length_parameters": ["lead_in", "lead_out"] if flags.get("stretchable_leads_candidate") else [],
                },
                "snap_policy": {
                    "snap_to_terminals": True,
                    "snap_to_connection_points": True,
                    "connection_graph_node_required": True,
                    "auto_connect_candidate": True,
                },
                "state_policy": {
                    "has_state_variants": is_multistate,
                    "detected_state_tokens": master.get("state_tokens", []),
                    "required_states_if_switching_device": [
                        "closed",
                        "open",
                        "unreliable",
                        "repair",
                    ] if is_multistate else [],
                    "kru_trolley_extra_states": [
                        "breaker_closed_trolley_service",
                        "breaker_open_trolley_service",
                        "breaker_unreliable_trolley_service",
                        "trolley_withdrawn_repair",
                        "trolley_withdrawn_test",
                    ] if kind == "kru_trolley" else [],
                },
                "busbar_policy": {
                    "configurable_connection_points": is_busbar,
                    "minimum_connection_points": 2 if is_busbar else 0,
                    "connection_point_spacing": "parameterized",
                    "length": "parameterized" if is_busbar else "fixed",
                    "busbar_stroke_width_multiplier": 4 if is_busbar else None,
                },
                "auto_layout_policy": {
                    "eligible": bool(flags.get("auto_layout_eligible")),
                    "may_be_placed_from_equipment_list": bool(flags.get("auto_layout_eligible")),
                    "requires_terminals_for_graph_layout": True,
                    "equipment_mapping_required": kind not in {"stamp_frame", "annotation"},
                },
                "connection_point_count": master.get("connection_point_count", 0),
                "geometry_row_total": master.get("geometry", {}).get("geometry_row_total", 0),
                "warnings": sorted(set(warnings)),
            }
        )

    return candidates


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, masters: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "id",
        "name",
        "normalized_id",
        "kind",
        "page_usage",
        "shape_count",
        "geometry_section_count",
        "geometry_row_total",
        "connection_point_count",
        "multi_state_candidate",
        "busbar_configurable_connection_points",
        "stretchable_leads_candidate",
        "rotatable",
        "voltage_colorizable",
        "auto_layout_eligible",
        "warnings",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for master in masters:
            flags = master.get("feature_flags", {})
            geometry = master.get("geometry", {})
            writer.writerow(
                {
                    "id": master.get("id", ""),
                    "name": master.get("name", ""),
                    "normalized_id": master.get("normalized_id", ""),
                    "kind": master.get("kind", ""),
                    "page_usage": "; ".join(master.get("page_usage", [])),
                    "shape_count": master.get("shape_count", 0),
                    "geometry_section_count": geometry.get("geometry_section_count", 0),
                    "geometry_row_total": geometry.get("geometry_row_total", 0),
                    "connection_point_count": master.get("connection_point_count", 0),
                    "multi_state_candidate": flags.get("multi_state_candidate", False),
                    "busbar_configurable_connection_points": flags.get("busbar_configurable_connection_points", False),
                    "stretchable_leads_candidate": flags.get("stretchable_leads_candidate", False),
                    "rotatable": flags.get("rotatable", True),
                    "voltage_colorizable": flags.get("voltage_colorizable", True),
                    "auto_layout_eligible": flags.get("auto_layout_eligible", True),
                    "warnings": "; ".join(master.get("warnings", [])),
                }
            )


def write_markdown(path: Path, source: Path, pages: list[dict[str, Any]], masters: list[dict[str, Any]], candidates: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    by_kind: dict[str, int] = {}
    for master in masters:
        kind = str(master.get("kind", "unknown"))
        by_kind[kind] = by_kind.get(kind, 0) + 1

    connection_total = sum(int(master.get("connection_point_count", 0) or 0) for master in masters)
    multistate = sum(1 for master in masters if master.get("feature_flags", {}).get("multi_state_candidate"))
    busbars = sum(1 for master in masters if master.get("feature_flags", {}).get("busbar_configurable_connection_points"))
    stretchable = sum(1 for master in masters if master.get("feature_flags", {}).get("stretchable_leads_candidate"))
    geometry_ok = sum(1 for master in masters if master.get("geometry", {}).get("has_geometry"))
    auto_layout = sum(1 for master in masters if master.get("feature_flags", {}).get("auto_layout_eligible"))

    lines: list[str] = []
    lines.append("# Visio VSDX inspection report")
    lines.append("")
    lines.append(f"Source: `{source}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Pages: {len(pages)}")
    lines.append(f"- Masters: {len(masters)}")
    lines.append(f"- Masters with top-level geometry: {geometry_ok}")
    lines.append(f"- Total connection points: {connection_total}")
    lines.append(f"- Multi-state candidates: {multistate}")
    lines.append(f"- Busbar configurable connection point candidates: {busbars}")
    lines.append(f"- Stretchable lead candidates: {stretchable}")
    lines.append(f"- Auto-layout eligible candidates: {auto_layout}")
    lines.append(f"- Import candidates: {len(candidates)}")
    lines.append("")
    lines.append("## Critical import policies")
    lines.append("")
    lines.append("- Do not promote imported symbols directly to the core library.")
    lines.append("- Keep all imported symbols in `Imported / Needs Review` until manually accepted.")
    lines.append("- Preserve state variants for breakers, disconnectors, earthing switches and KRU trolleys.")
    lines.append("- Preserve configurable connection point logic for busbars and bus sections.")
    lines.append("- Every symbol must be colorizable by voltage class.")
    lines.append("- Every symbol must be rotatable with terminal/snap-anchor transform.")
    lines.append("- Stretchable connection leads must not distort the symbol body.")
    lines.append("- Snap anchors are mandatory for fast figure-to-figure binding.")
    lines.append("- Busbars must use a 4x stroke-width multiplier relative to normal connection lines.")
    lines.append("- Automatic scheme generation requires equipment-to-symbol mapping and terminal graph data.")
    lines.append("")
    lines.append("## Pages")
    lines.append("")
    lines.append("| Page | Shapes | Master refs |")
    lines.append("|---|---:|---:|")
    for page in pages:
        lines.append(f"| {page.get('name', '')} | {page.get('shape_count', 0)} | {len(page.get('shape_master_refs', {}))} |")
    lines.append("")
    lines.append("## Masters by kind")
    lines.append("")
    lines.append("| Kind | Count |")
    lines.append("|---|---:|")
    for kind, count in sorted(by_kind.items()):
        lines.append(f"| {kind} | {count} |")
    lines.append("")
    lines.append("## High-risk candidates")
    lines.append("")
    lines.append("| Master | Kind | Reason |")
    lines.append("|---|---|---|")
    for candidate in candidates:
        reasons: list[str] = []
        if candidate.get("state_policy", {}).get("has_state_variants"):
            reasons.append("state variants")
        if candidate.get("busbar_policy", {}).get("configurable_connection_points"):
            reasons.append("configurable busbar connection points")
        if candidate.get("stretch_policy", {}).get("stretchable"):
            reasons.append("stretchable leads")
        if candidate.get("transform_policy", {}).get("rotatable"):
            reasons.append("rotation-safe terminals")
        if candidate.get("warnings"):
            reasons.extend(candidate.get("warnings", []))
        if reasons:
            reason_text = "; ".join(str(r) for r in reasons[:6])
            lines.append(f"| {candidate.get('source_name', '')} | {candidate.get('kind', '')} | {reason_text} |")
    lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def inspect_vsdx(source: Path, out_dir: Path) -> dict[str, Any]:
    if not source.exists():
        raise FileNotFoundError(source)

    with zipfile.ZipFile(source, "r") as zf:
        pages, _ = collect_pages(zf)
        masters = collect_masters(zf)
        attach_page_usage(masters, pages)
        candidates = build_import_candidates(masters)

    report = {
        "source": str(source),
        "format": "vsdx",
        "pages_count": len(pages),
        "masters_count": len(masters),
        "connection_points_total": sum(int(master.get("connection_point_count", 0) or 0) for master in masters),
        "voltage_classes": VOLTAGE_CLASSES,
        "policies": {
            "import_target": "Imported / Needs Review",
            "manual_review_required": True,
            "core_library_promotion_requires_review": True,
            "all_symbols_colorizable_by_voltage_class": True,
            "switching_devices_require_state_variants": True,
            "busbars_require_configurable_connection_points": True,
            "symbols_are_rotatable": True,
            "terminals_transform_with_rotation": True,
            "stretchable_leads_without_body_distortion": True,
            "snap_anchors_required": True,
            "automatic_scheme_generation_is_first_class_goal": True,
        },
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "pages.json", pages)
    write_json(out_dir / "masters.json", masters)
    write_json(out_dir / "import_candidates.json", candidates)
    write_json(
        out_dir / "master_geometry_audit.json",
        {
            "source": str(source),
            "summary": report,
            "masters": [
                {
                    "id": master.get("id"),
                    "name": master.get("name"),
                    "kind": master.get("kind"),
                    "geometry": master.get("geometry"),
                    "connection_point_count": master.get("connection_point_count"),
                    "feature_flags": master.get("feature_flags"),
                    "capabilities": master.get("capabilities"),
                    "warnings": master.get("warnings"),
                }
                for master in masters
            ],
        },
    )
    write_json(out_dir / "visio_import_report.json", report)
    write_csv(out_dir / "masters.csv", masters)
    write_markdown(out_dir / "README.md", source, pages, masters, candidates)

    return report


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Inspect a Visio VSDX file for ElectroScheme Studio symbol import.")
    parser.add_argument("vsdx", type=Path, help="Path to .vsdx file")
    parser.add_argument("--out", type=Path, default=Path("_reports/visio_figures"), help="Output report directory")
    args = parser.parse_args(argv)

    report = inspect_vsdx(args.vsdx, args.out)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
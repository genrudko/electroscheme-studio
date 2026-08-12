#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import posixpath
import re
import zipfile
from xml.etree import ElementTree as ET

from generate_controlled_visio_fixtures import _write_package, build_vsdx

REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
VISIO_NS = "http://schemas.microsoft.com/office/visio/2012/main"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
EXTENDED_PROPS_NS = "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
REL = f"{{{REL_NS}}}Relationship"
RID = f"{{{OFFICE_REL_NS}}}id"
APP_VERSION_RE = re.compile(r"^\d{2}\.\d{4}$")

COMMON_REQUIRED = {
    "[Content_Types].xml",
    "_rels/.rels",
    "docProps/core.xml",
    "visio/document.xml",
    "visio/_rels/document.xml.rels",
}
REQUIRED_BY_KIND = {
    "vsdx": COMMON_REQUIRED | {"visio/pages/pages.xml", "visio/pages/_rels/pages.xml.rels", "visio/pages/page1.xml"},
    "vssx": COMMON_REQUIRED | {"visio/masters/masters.xml", "visio/masters/_rels/masters.xml.rels", "visio/masters/master1.xml"},
}
EXPECTED_CONTENT_TYPES = {
    "vsdx": {
        "/docProps/core.xml": "application/vnd.openxmlformats-package.core-properties+xml",
        "/visio/document.xml": "application/vnd.ms-visio.drawing.main+xml",
        "/visio/pages/pages.xml": "application/vnd.ms-visio.pages+xml",
        "/visio/pages/page1.xml": "application/vnd.ms-visio.page+xml",
    },
    "vssx": {
        "/docProps/core.xml": "application/vnd.openxmlformats-package.core-properties+xml",
        "/visio/document.xml": "application/vnd.ms-visio.stencil.main+xml",
        "/visio/masters/masters.xml": "application/vnd.ms-visio.masters+xml",
        "/visio/masters/master1.xml": "application/vnd.ms-visio.master+xml",
    },
}


def _source_for_rels(name: str) -> str | None:
    if name == "_rels/.rels":
        return None
    directory, filename = posixpath.split(name)
    if posixpath.basename(directory) != "_rels" or not filename.endswith(".rels"):
        return None
    source_dir = posixpath.dirname(directory)
    source_name = filename[:-5]
    return posixpath.join(source_dir, source_name) if source_dir else source_name


def _target(source: str | None, target: str) -> str:
    if target.startswith("/"):
        return posixpath.normpath(target.lstrip("/"))
    base = posixpath.dirname(source) if source else ""
    return posixpath.normpath(posixpath.join(base, target))


def _relationships(archive: zipfile.ZipFile, names: set[str], diagnostics: list[dict]) -> dict[str | None, dict[str, dict[str, str]]]:
    graph: dict[str | None, dict[str, dict[str, str]]] = {}
    for rels_name in sorted(name for name in names if name.endswith(".rels")):
        source = _source_for_rels(rels_name)
        try:
            root = ET.fromstring(archive.read(rels_name))
        except ET.ParseError:
            continue
        relationships: dict[str, dict[str, str]] = {}
        for item in root.findall(REL):
            rid = item.get("Id", "")
            target_mode = item.get("TargetMode", "Internal")
            resolved = item.get("Target", "") if target_mode == "External" else _target(source, item.get("Target", ""))
            relationships[rid] = {"type": item.get("Type", ""), "target": resolved, "mode": target_mode}
            if target_mode != "External" and resolved not in names:
                diagnostics.append({"severity": "error", "code": "DANGLING_RELATIONSHIP", "source": source or "PACKAGE", "relationshipId": rid, "target": resolved})
        graph[source] = relationships
    return graph


def _require_relationship(graph: dict, source: str | None, rel_type: str, target: str, diagnostics: list[dict]) -> str | None:
    matches = [(rid, rel) for rid, rel in graph.get(source, {}).items() if rel["type"] == rel_type and rel["target"] == target and rel["mode"] != "External"]
    if len(matches) != 1:
        diagnostics.append({"severity": "error", "code": "REQUIRED_RELATIONSHIP_MISSING", "source": source or "PACKAGE", "type": rel_type, "target": target, "matches": len(matches)})
        return None
    return matches[0][0]


def _validate_content_types(archive: zipfile.ZipFile, kind: str, diagnostics: list[dict]) -> None:
    try:
        root = ET.fromstring(archive.read("[Content_Types].xml"))
    except (KeyError, ET.ParseError):
        return
    overrides = {item.get("PartName", ""): item.get("ContentType", "") for item in root.findall(f"{{{CT_NS}}}Override")}
    for part, expected in EXPECTED_CONTENT_TYPES[kind].items():
        if overrides.get(part) != expected:
            diagnostics.append({"severity": "error", "code": "CONTENT_TYPE_MISMATCH", "part": part, "expected": expected, "actual": overrides.get(part)})


def _validate_extended_properties(archive: zipfile.ZipFile, diagnostics: list[dict]) -> None:
    try:
        root = ET.fromstring(archive.read("docProps/app.xml"))
    except (KeyError, ET.ParseError):
        return
    if root.tag != f"{{{EXTENDED_PROPS_NS}}}Properties":
        diagnostics.append({"severity": "error", "code": "EXTENDED_PROPERTIES_ROOT_INVALID", "part": "docProps/app.xml"})
        return
    app_version = root.find(f"{{{EXTENDED_PROPS_NS}}}AppVersion")
    if app_version is not None:
        value = (app_version.text or "").strip()
        if not APP_VERSION_RE.fullmatch(value):
            diagnostics.append({"severity": "error", "code": "APP_VERSION_INVALID", "part": "docProps/app.xml", "value": value, "expectedFormat": "XX.YYYY"})


def _validate_vsdx(archive: zipfile.ZipFile, graph: dict, diagnostics: list[dict]) -> None:
    document_rel = _require_relationship(graph, None, "http://schemas.microsoft.com/visio/2010/relationships/document", "visio/document.xml", diagnostics)
    pages_rel = _require_relationship(graph, "visio/document.xml", "http://schemas.microsoft.com/visio/2010/relationships/pages", "visio/pages/pages.xml", diagnostics)
    page_rel = _require_relationship(graph, "visio/pages/pages.xml", "http://schemas.microsoft.com/visio/2010/relationships/page", "visio/pages/page1.xml", diagnostics)
    del document_rel, pages_rel
    try:
        document = ET.fromstring(archive.read("visio/document.xml"))
        if document.tag != f"{{{VISIO_NS}}}VisioDocument":
            diagnostics.append({"severity": "error", "code": "VISIO_ROOT_INVALID", "part": "visio/document.xml"})
        if document.find(f"{{{VISIO_NS}}}Pages") is not None:
            diagnostics.append({"severity": "error", "code": "INLINE_PAGES_RELATION_INVALID", "part": "visio/document.xml"})
        pages = ET.fromstring(archive.read("visio/pages/pages.xml"))
        page = pages.find(f"{{{VISIO_NS}}}Page")
        if page is None:
            diagnostics.append({"severity": "error", "code": "PAGE_ELEMENT_MISSING"})
        else:
            rel_element = page.find(f"{{{VISIO_NS}}}Rel")
            if rel_element is None or rel_element.get(RID) != page_rel:
                diagnostics.append({"severity": "error", "code": "PAGE_REL_INVALID", "expectedRelationshipId": page_rel, "actualRelationshipId": None if rel_element is None else rel_element.get(RID)})
            if page.get(RID) is not None:
                diagnostics.append({"severity": "error", "code": "PAGE_REL_ATTRIBUTE_INVALID"})
            page_sheet = page.find(f"{{{VISIO_NS}}}PageSheet")
            if page_sheet is None:
                diagnostics.append({"severity": "error", "code": "PAGE_SHEET_MISSING"})
        contents = ET.fromstring(archive.read("visio/pages/page1.xml"))
        if contents.tag != f"{{{VISIO_NS}}}PageContents":
            diagnostics.append({"severity": "error", "code": "PAGE_CONTENTS_ROOT_INVALID"})
        if contents.find(f"{{{VISIO_NS}}}PageSheet") is not None:
            diagnostics.append({"severity": "error", "code": "PAGE_SHEET_WRONG_PART"})
        connector = next((shape for shape in contents.findall(f".//{{{VISIO_NS}}}Shape") if shape.get("ID") == "3"), None)
        required = {"BeginX", "BeginY", "EndX", "EndY"}
        cells = set() if connector is None else {cell.get("N") for cell in connector.findall(f"{{{VISIO_NS}}}Cell")}
        if connector is None or not required.issubset(cells):
            diagnostics.append({"severity": "error", "code": "ONE_D_CONNECTOR_INVALID", "requiredCells": sorted(required), "actualCells": sorted(item for item in cells if item)})
    except (KeyError, ET.ParseError) as error:
        diagnostics.append({"severity": "error", "code": "VISIO_STRUCTURE_PARSE_FAILED", "message": str(error)})


def _validate_vssx(archive: zipfile.ZipFile, graph: dict, diagnostics: list[dict]) -> None:
    _require_relationship(graph, None, "http://schemas.microsoft.com/visio/2010/relationships/document", "visio/document.xml", diagnostics)
    _require_relationship(graph, "visio/document.xml", "http://schemas.microsoft.com/visio/2010/relationships/masters", "visio/masters/masters.xml", diagnostics)
    master_rel = _require_relationship(graph, "visio/masters/masters.xml", "http://schemas.microsoft.com/visio/2010/relationships/master", "visio/masters/master1.xml", diagnostics)
    try:
        masters = ET.fromstring(archive.read("visio/masters/masters.xml"))
        master = masters.find(f"{{{VISIO_NS}}}Master")
        rel_element = None if master is None else master.find(f"{{{VISIO_NS}}}Rel")
        if master is None or rel_element is None or rel_element.get(RID) != master_rel:
            diagnostics.append({"severity": "error", "code": "MASTER_REL_INVALID", "expectedRelationshipId": master_rel})
    except (KeyError, ET.ParseError) as error:
        diagnostics.append({"severity": "error", "code": "VISIO_STRUCTURE_PARSE_FAILED", "message": str(error)})


def inspect_package(path: pathlib.Path, kind: str) -> dict:
    diagnostics: list[dict] = []
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            missing = sorted(REQUIRED_BY_KIND[kind] - names)
            if missing:
                diagnostics.append({"severity": "error", "code": "PACKAGE_PART_MISSING", "kind": kind, "parts": missing})
            xml_parts: list[str] = []
            source_ids: list[str] = []
            for name in sorted(item for item in names if item.endswith((".xml", ".rels"))):
                try:
                    root = ET.fromstring(archive.read(name))
                    xml_parts.append(name)
                    source_ids.extend(element.attrib["ID"] for element in root.iter() if "ID" in element.attrib)
                except ET.ParseError as error:
                    diagnostics.append({"severity": "error", "code": "INVALID_XML", "part": name, "message": str(error)})
            if "[Content_Types].xml" in names:
                _validate_content_types(archive, kind, diagnostics)
            if "docProps/app.xml" in names:
                _validate_extended_properties(archive, diagnostics)
            graph = _relationships(archive, names, diagnostics)
            if kind == "vsdx":
                _validate_vsdx(archive, graph, diagnostics)
            else:
                _validate_vssx(archive, graph, diagnostics)
            return {"protocol": "electroscheme-visio-tool/1", "operation": "inspect", "kind": kind, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "parts": sorted(names), "xmlParts": xml_parts, "sourceIds": sorted(set(source_ids)), "diagnostics": diagnostics, "status": "ok" if not any(item["severity"] == "error" for item in diagnostics) else "invalid"}
    except (OSError, zipfile.BadZipFile) as error:
        return {"protocol": "electroscheme-visio-tool/1", "operation": "inspect", "kind": kind, "status": "invalid", "diagnostics": [{"severity": "error", "code": "PACKAGE_OPEN_FAILED", "message": str(error)}]}


def generate_vsdx(canonical_path: pathlib.Path, output_path: pathlib.Path) -> dict:
    project = json.loads(canonical_path.read_text(encoding="utf-8"))
    _write_package(output_path, build_vsdx(project))
    result = inspect_package(output_path, "vsdx")
    result["operation"] = "generate-vsdx"
    result["canonicalProjectId"] = project.get("projectId")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    inspect = commands.add_parser("inspect")
    inspect.add_argument("kind", choices=["vsdx", "vssx"])
    inspect.add_argument("path", type=pathlib.Path)
    generate = commands.add_parser("generate-vsdx")
    generate.add_argument("canonical_path", type=pathlib.Path)
    generate.add_argument("output_path", type=pathlib.Path)
    args = parser.parse_args()
    result = inspect_package(args.path, args.kind) if args.command == "inspect" else generate_vsdx(args.canonical_path, args.output_path)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    raise SystemExit(0 if result["status"] == "ok" else 2)


if __name__ == "__main__":
    main()

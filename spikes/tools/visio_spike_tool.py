#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import zipfile
from xml.etree import ElementTree as ET

from generate_controlled_visio_fixtures import _write_package, build_vsdx

COMMON_REQUIRED = {
    "[Content_Types].xml",
    "_rels/.rels",
    "docProps/core.xml",
    "visio/document.xml",
    "visio/_rels/document.xml.rels",
}

REQUIRED_BY_KIND = {
    "vsdx": COMMON_REQUIRED
    | {
        "visio/pages/pages.xml",
        "visio/pages/_rels/pages.xml.rels",
        "visio/pages/page1.xml",
    },
    "vssx": COMMON_REQUIRED
    | {
        "visio/masters/masters.xml",
        "visio/masters/_rels/masters.xml.rels",
        "visio/masters/master1.xml",
    },
}


def inspect_package(path: pathlib.Path, kind: str) -> dict:
    diagnostics: list[dict] = []
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            missing = sorted(REQUIRED_BY_KIND[kind] - names)
            if missing:
                diagnostics.append(
                    {
                        "severity": "error",
                        "code": "PACKAGE_PART_MISSING",
                        "kind": kind,
                        "parts": missing,
                    }
                )
            xml_parts: list[str] = []
            source_ids: list[str] = []
            for name in sorted(item for item in names if item.endswith((".xml", ".rels"))):
                try:
                    root = ET.fromstring(archive.read(name))
                    xml_parts.append(name)
                    source_ids.extend(element.attrib["ID"] for element in root.iter() if "ID" in element.attrib)
                except ET.ParseError as error:
                    diagnostics.append(
                        {
                            "severity": "error",
                            "code": "INVALID_XML",
                            "part": name,
                            "message": str(error),
                        }
                    )
            return {
                "protocol": "electroscheme-visio-tool/1",
                "operation": "inspect",
                "kind": kind,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "parts": sorted(names),
                "xmlParts": xml_parts,
                "sourceIds": sorted(set(source_ids)),
                "diagnostics": diagnostics,
                "status": "ok" if not any(item["severity"] == "error" for item in diagnostics) else "invalid",
            }
    except (OSError, zipfile.BadZipFile) as error:
        return {
            "protocol": "electroscheme-visio-tool/1",
            "operation": "inspect",
            "kind": kind,
            "status": "invalid",
            "diagnostics": [{"severity": "error", "code": "PACKAGE_OPEN_FAILED", "message": str(error)}],
        }


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
    if args.command == "inspect":
        result = inspect_package(args.path, args.kind)
    else:
        result = generate_vsdx(args.canonical_path, args.output_path)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    raise SystemExit(0 if result["status"] == "ok" else 2)


if __name__ == "__main__":
    main()

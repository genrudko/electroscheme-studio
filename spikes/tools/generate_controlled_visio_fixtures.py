#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import zipfile
from xml.sax.saxutils import escape

FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def _xml(text: str) -> bytes:
    return text.strip().encode("utf-8")


def _write_package(path: pathlib.Path, entries: dict[str, bytes]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.create_system = 3
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, entries[name])


def build_vsdx(project: dict) -> dict[str, bytes]:
    title = escape(str(project.get("title", "ElectroScheme controlled fixture")))
    equipment = project.get("equipment") or []
    designation = escape(str(equipment[0].get("designation", "Q-SPK-1"))) if equipment else "Q-SPK-1"
    return {
        "[Content_Types].xml": _xml(f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/visio/document.xml" ContentType="application/vnd.ms-visio.drawing.main+xml"/>
  <Override PartName="/visio/pages/pages.xml" ContentType="application/vnd.ms-visio.pages+xml"/>
  <Override PartName="/visio/pages/page1.xml" ContentType="application/vnd.ms-visio.page+xml"/>
</Types>'''),
        "_rels/.rels": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/document" Target="visio/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>'''),
        "docProps/core.xml": _xml(f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <dc:title>{title}</dc:title>
</cp:coreProperties>'''),
        "visio/_rels/document.xml.rels": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/pages" Target="pages/pages.xml"/>
</Relationships>'''),
        "visio/document.xml": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<VisioDocument xmlns="http://schemas.microsoft.com/office/visio/2012/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <DocumentProperties/>
  <Pages r:id="rId1"/>
</VisioDocument>'''),
        "visio/pages/_rels/pages.xml.rels": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/page" Target="page1.xml"/>
</Relationships>'''),
        "visio/pages/pages.xml": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Pages xmlns="http://schemas.microsoft.com/office/visio/2012/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <Page ID="0" NameU="Page-1" Name="Page-1" r:id="rId1"/>
</Pages>'''),
        "visio/pages/page1.xml": _xml(f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PageContents xmlns="http://schemas.microsoft.com/office/visio/2012/main">
  <PageSheet><Cell N="PageWidth" V="11"/><Cell N="PageHeight" V="8.5"/></PageSheet>
  <Shapes>
    <Shape ID="1" Type="Shape" NameU="Rectangle.1">
      <Cell N="PinX" V="2"/><Cell N="PinY" V="5"/><Cell N="Width" V="1"/><Cell N="Height" V="0.6"/>
      <Section N="Property"><Row N="Prop.EngineeringId"><Cell N="Value" V="{designation}"/></Row></Section>
      <Text>{designation}</Text>
    </Shape>
    <Shape ID="2" Type="Shape" NameU="Rectangle.2">
      <Cell N="PinX" V="6"/><Cell N="PinY" V="5"/><Cell N="Width" V="2"/><Cell N="Height" V="0.15"/><Text>BUS</Text>
    </Shape>
    <Shape ID="3" Type="Shape" NameU="Dynamic connector.3">
      <Cell N="BeginX" V="2"/><Cell N="BeginY" V="4.7"/><Cell N="EndX" V="5"/><Cell N="EndY" V="5"/><Text>CONNECTOR</Text>
    </Shape>
  </Shapes>
  <Connects>
    <Connect FromSheet="3" FromCell="BeginX" ToSheet="1" ToPart="3"/>
    <Connect FromSheet="3" FromCell="EndX" ToSheet="2" ToPart="3"/>
  </Connects>
</PageContents>'''),
    }


def build_vssx() -> dict[str, bytes]:
    return {
        "[Content_Types].xml": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/visio/document.xml" ContentType="application/vnd.ms-visio.stencil.main+xml"/>
  <Override PartName="/visio/masters/masters.xml" ContentType="application/vnd.ms-visio.masters+xml"/>
  <Override PartName="/visio/masters/master1.xml" ContentType="application/vnd.ms-visio.master+xml"/>
</Types>'''),
        "_rels/.rels": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/document" Target="visio/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>'''),
        "docProps/core.xml": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>ElectroScheme controlled VSSX fixture</dc:title></cp:coreProperties>'''),
        "visio/_rels/document.xml.rels": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/masters" Target="masters/masters.xml"/>
</Relationships>'''),
        "visio/document.xml": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<VisioDocument xmlns="http://schemas.microsoft.com/office/visio/2012/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><DocumentProperties/><Masters r:id="rId1"/></VisioDocument>'''),
        "visio/masters/_rels/masters.xml.rels": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/master" Target="master1.xml"/></Relationships>'''),
        "visio/masters/masters.xml": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Masters xmlns="http://schemas.microsoft.com/office/visio/2012/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><Master ID="1" Name="Controlled Master" NameU="Controlled Master" r:id="rId1"/></Masters>'''),
        "visio/masters/master1.xml": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<MasterContents xmlns="http://schemas.microsoft.com/office/visio/2012/main"><Shapes><Shape ID="10" Type="Shape" NameU="ControlledMaster.10"><Cell N="Width" V="1"/><Cell N="Height" V="1"/><Section N="Connection"><Row IX="0"><Cell N="X" V="0.5"/><Cell N="Y" V="0"/></Row></Section><Text>MASTER</Text></Shape></Shapes></MasterContents>'''),
    }


def generate(output_dir: pathlib.Path, canonical_path: pathlib.Path | None = None) -> None:
    project = json.loads(canonical_path.read_text(encoding="utf-8")) if canonical_path else {
        "title": "Desktop platform canonical fixture",
        "equipment": [{"designation": "Q-SPK-1"}],
    }
    _write_package(output_dir / "controlled-minimal.vsdx", build_vsdx(project))
    _write_package(output_dir / "controlled-master.vssx", build_vssx())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=pathlib.Path)
    parser.add_argument("--canonical", type=pathlib.Path)
    args = parser.parse_args()
    generate(args.output_dir, args.canonical)


if __name__ == "__main__":
    main()

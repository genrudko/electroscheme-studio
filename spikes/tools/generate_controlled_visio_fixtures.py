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


def _document_xml() -> bytes:
    return _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<VisioDocument xmlns="http://schemas.microsoft.com/office/visio/2012/main" xml:space="preserve">
  <FaceNames><FaceName NameU="Calibri"/></FaceNames>
  <StyleSheets>
    <StyleSheet ID="0" NameU="No Style" Name="No Style">
      <Cell N="EnableLineProps" V="1"/><Cell N="EnableFillProps" V="1"/><Cell N="EnableTextProps" V="1"/>
      <Cell N="LineWeight" V="0.01041666666666667"/><Cell N="LineColor" V="0"/><Cell N="LinePattern" V="1"/>
      <Cell N="FillForegnd" V="1"/><Cell N="FillBkgnd" V="1"/><Cell N="FillPattern" V="1"/>
    </StyleSheet>
  </StyleSheets>
</VisioDocument>''')


def _rectangle_shape(shape_id: int, name: str, pin_x: float, pin_y: float, width: float, height: float, text: str, engineering_id: str | None = None) -> str:
    property_xml = ""
    if engineering_id is not None:
        property_xml = f'''\n      <Section N="Property"><Row N="Prop.EngineeringId"><Cell N="Label" V="EngineeringId"/><Cell N="Type" V="0"/><Cell N="Value" V="{engineering_id}"/></Row></Section>'''
    return f'''    <Shape ID="{shape_id}" Type="Shape" NameU="{name}" LineStyle="0" FillStyle="0" TextStyle="0">
      <Cell N="PinX" V="{pin_x}"/><Cell N="PinY" V="{pin_y}"/><Cell N="Width" V="{width}"/><Cell N="Height" V="{height}"/>
      <Cell N="LocPinX" V="{width / 2}"/><Cell N="LocPinY" V="{height / 2}"/>{property_xml}
      <Section N="Geometry" IX="0"><Cell N="NoFill" V="0"/><Cell N="NoLine" V="0"/>
        <Row IX="1" T="MoveTo"><Cell N="X" V="0"/><Cell N="Y" V="0"/></Row>
        <Row IX="2" T="LineTo"><Cell N="X" V="{width}"/><Cell N="Y" V="0"/></Row>
        <Row IX="3" T="LineTo"><Cell N="X" V="{width}"/><Cell N="Y" V="{height}"/></Row>
        <Row IX="4" T="LineTo"><Cell N="X" V="0"/><Cell N="Y" V="{height}"/></Row>
        <Row IX="5" T="LineTo"><Cell N="X" V="0"/><Cell N="Y" V="0"/></Row>
      </Section>
      <Text>{text}</Text>
    </Shape>'''


def build_vsdx(project: dict) -> dict[str, bytes]:
    title = escape(str(project.get("title", "ElectroScheme controlled fixture")))
    equipment = project.get("equipment") or []
    designation = escape(str(equipment[0].get("designation", "Q-SPK-1"))) if equipment else "Q-SPK-1"
    page = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PageContents xmlns="http://schemas.microsoft.com/office/visio/2012/main" xml:space="preserve">
  <Shapes>
{_rectangle_shape(1, "Equipment.1", 2, 5, 1, 0.6, designation, designation)}
{_rectangle_shape(2, "Busbar.2", 6, 5, 2, 0.15, "BUS")}
    <Shape ID="3" Type="Shape" NameU="Connector.3" LineStyle="0" FillStyle="0" TextStyle="0">
      <Cell N="BeginX" V="2.5"/><Cell N="BeginY" V="5"/><Cell N="EndX" V="5"/><Cell N="EndY" V="5"/>
      <Cell N="PinX" V="3.75"/><Cell N="PinY" V="5"/><Cell N="Width" V="2.5"/><Cell N="Height" V="0"/>
      <Cell N="LocPinX" V="1.25"/><Cell N="LocPinY" V="0"/>
      <Section N="Geometry" IX="0"><Cell N="NoFill" V="1"/><Cell N="NoLine" V="0"/>
        <Row IX="1" T="MoveTo"><Cell N="X" V="0"/><Cell N="Y" V="0"/></Row>
        <Row IX="2" T="LineTo"><Cell N="X" V="2.5"/><Cell N="Y" V="0"/></Row>
      </Section>
    </Shape>
  </Shapes>
  <Connects>
    <Connect FromSheet="3" FromCell="BeginX" ToSheet="1" ToPart="3"/>
    <Connect FromSheet="3" FromCell="EndX" ToSheet="2" ToPart="3"/>
  </Connects>
</PageContents>'''
    return {
        "[Content_Types].xml": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/visio/document.xml" ContentType="application/vnd.ms-visio.drawing.main+xml"/>
  <Override PartName="/visio/pages/pages.xml" ContentType="application/vnd.ms-visio.pages+xml"/>
  <Override PartName="/visio/pages/page1.xml" ContentType="application/vnd.ms-visio.page+xml"/>
</Types>'''),
        "_rels/.rels": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/document" Target="visio/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''),
        "docProps/app.xml": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>ElectroScheme Studio</Application><AppVersion>01.0000</AppVersion></Properties>'''),
        "docProps/core.xml": _xml(f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>{title}</dc:title></cp:coreProperties>'''),
        "visio/_rels/document.xml.rels": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/pages" Target="pages/pages.xml"/></Relationships>'''),
        "visio/document.xml": _document_xml(),
        "visio/pages/_rels/pages.xml.rels": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/page" Target="page1.xml"/></Relationships>'''),
        "visio/pages/pages.xml": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Pages xmlns="http://schemas.microsoft.com/office/visio/2012/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xml:space="preserve">
  <Page ID="0" NameU="Page-1" Name="Page-1">
    <PageSheet LineStyle="0" FillStyle="0" TextStyle="0"><Cell N="PageWidth" V="11"/><Cell N="PageHeight" V="8.5"/><Cell N="PageScale" V="1"/><Cell N="DrawingScale" V="1"/></PageSheet>
    <Rel r:id="rId1"/>
  </Page>
</Pages>'''),
        "visio/pages/page1.xml": _xml(page),
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
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/document" Target="visio/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>'''),
        "docProps/core.xml": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>ElectroScheme controlled VSSX fixture</dc:title></cp:coreProperties>'''),
        "visio/_rels/document.xml.rels": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/masters" Target="masters/masters.xml"/></Relationships>'''),
        "visio/document.xml": _document_xml(),
        "visio/masters/_rels/masters.xml.rels": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/master" Target="master1.xml"/></Relationships>'''),
        "visio/masters/masters.xml": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Masters xmlns="http://schemas.microsoft.com/office/visio/2012/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xml:space="preserve"><Master ID="1" Name="Controlled Master" NameU="Controlled Master"><PageSheet LineStyle="0" FillStyle="0" TextStyle="0"><Cell N="PageWidth" V="1"/><Cell N="PageHeight" V="1"/><Cell N="PageScale" V="1"/><Cell N="DrawingScale" V="1"/></PageSheet><Rel r:id="rId1"/></Master></Masters>'''),
        "visio/masters/master1.xml": _xml('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<MasterContents xmlns="http://schemas.microsoft.com/office/visio/2012/main"><Shapes><Shape ID="10" Type="Shape" NameU="ControlledMaster.10"><Cell N="PinX" V="0.5"/><Cell N="PinY" V="0.5"/><Cell N="Width" V="1"/><Cell N="Height" V="1"/><Section N="Connection"><Row IX="0"><Cell N="X" V="0.5"/><Cell N="Y" V="0"/></Row></Section><Text>MASTER</Text></Shape></Shapes></MasterContents>'''),
    }


def generate(output_dir: pathlib.Path, canonical_path: pathlib.Path | None = None) -> None:
    project = json.loads(canonical_path.read_text(encoding="utf-8")) if canonical_path else {"title": "Desktop platform canonical fixture", "equipment": [{"designation": "Q-SPK-1"}]}
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

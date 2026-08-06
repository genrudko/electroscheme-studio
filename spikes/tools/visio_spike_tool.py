#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, pathlib, zipfile
from xml.etree import ElementTree as ET
REQUIRED={"[Content_Types].xml","_rels/.rels","visio/document.xml","visio/_rels/document.xml.rels"}
def inspect_package(path:pathlib.Path,kind:str)->dict:
 diagnostics=[]
 try:
  with zipfile.ZipFile(path) as z:
   names=set(z.namelist()); missing=sorted(REQUIRED-names)
   if missing: diagnostics.append({"severity":"error","code":"PACKAGE_PART_MISSING","parts":missing})
   xml_parts=[]
   for name in sorted(n for n in names if n.endswith((".xml",".rels"))):
    try: ET.fromstring(z.read(name)); xml_parts.append(name)
    except ET.ParseError as exc: diagnostics.append({"severity":"error","code":"INVALID_XML","part":name,"message":str(exc)})
   source_ids=[]
   for name in sorted(n for n in names if n.endswith(".xml")):
    try:
     root=ET.fromstring(z.read(name)); source_ids += [e.attrib["ID"] for e in root.iter() if "ID" in e.attrib]
    except ET.ParseError: pass
   return {"protocol":"electroscheme-visio-tool/1","operation":"inspect","kind":kind,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"parts":sorted(names),"xmlParts":xml_parts,"sourceIds":sorted(set(source_ids)),"diagnostics":diagnostics,"status":"ok" if not any(d["severity"]=="error" for d in diagnostics) else "invalid"}
 except (OSError,zipfile.BadZipFile) as exc:
  return {"protocol":"electroscheme-visio-tool/1","operation":"inspect","kind":kind,"status":"invalid","diagnostics":[{"severity":"error","code":"PACKAGE_OPEN_FAILED","message":str(exc)}]}
def main():
 p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True); i=sub.add_parser("inspect"); i.add_argument("kind",choices=["vsdx","vssx"]); i.add_argument("path",type=pathlib.Path); args=p.parse_args(); result=inspect_package(args.path,args.kind); print(json.dumps(result,sort_keys=True,separators=(",",":"))); raise SystemExit(0 if result["status"]=="ok" else 2)
if __name__=="__main__": main()

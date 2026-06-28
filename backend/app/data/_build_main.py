# -*- coding: utf-8 -*-
"""Generate symbol_library.json — GOST/ESKD-compliant symbol library.

Usage:
    cd G:\\electroscheme-studio\\backend\\app\\data
    python _build_main.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _build_library import CATEGORIES
from _build_symbols import build_primary_symbols
from _build_symbols2 import build_secondary_symbols


GOST_REFERENCES = [
    {"id": "GOST_2_701_2008", "title": "ГОСТ 2.701-2008", "description": "Схемы. Виды и элементы", "status": "действующий"},
    {"id": "GOST_2_702_2011", "title": "ГОСТ 2.702-2011", "description": "Правила выполнения", "status": "действующий"},
    {"id": "GOST_2_709_89", "title": "ГОСТ 2.709-89", "description": "Линии связей", "status": "действующий"},
    {"id": "GOST_2_710_81", "title": "ГОСТ 2.710-81", "description": "Аппараты коммутационные, контакторы, реле", "status": "действующий"},
    {"id": "GOST_2_721_74", "title": "ГОСТ 2.721-74", "description": "Обозначения условные соединений, шины, зажимы", "status": "действующий"},
    {"id": "GOST_2_722_68", "title": "ГОСТ 2.722-68", "description": "Электрические машины", "status": "действующий"},
    {"id": "GOST_2_723_68", "title": "ГОСТ 2.723-68", "description": "Трансформаторы и катушки индуктивности", "status": "действующий"},
    {"id": "GOST_2_727_68", "title": "ГОСТ 2.727-68", "description": "Лампы и устройства сигнализации", "status": "действующий"},
    {"id": "GOST_2_728_74", "title": "ГОСТ 2.728-74", "description": "Пассивные элементы, предохранители, приборы", "status": "действующий"},
    {"id": "GOST_2_729_68", "title": "ГОСТ 2.729-68", "description": "Трансформаторы, дроссели", "status": "действующий"},
    {"id": "GOST_2_730_73", "title": "ГОСТ 2.730-73", "description": "Трансформаторы тока и напряжения", "status": "действующий"},
    {"id": "GOST_2_742_68", "title": "ГОСТ 2.742-68", "description": "Разрядники и ограничители перенапряжений", "status": "действующий"},
    {"id": "GOST_2_747_68", "title": "ГОСТ 2.747-68", "description": "Условные обозначения элементов телемеханики", "status": "действующий"},
    {"id": "GOST_2_755_87", "title": "ГОСТ 2.755-87", "description": "Коннекторы и клеммы", "status": "действующий"},
    {"id": "GOST_2_756_76", "title": "ГОСТ 2.756-76", "description": "Обозначения заземления", "status": "действующий"},
    {"id": "GOST_2_759_82", "title": "ГОСТ 2.759-82", "description": "Реле, катушки контакторов, контакты", "status": "действующий"},
    {"id": "GOST_2_768_90", "title": "ГОСТ 2.768-90", "description": "Управляющие и распределительные устройства", "status": "действующий"},
]


def _dedup(symbols: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for s in symbols:
        sid = s["id"]
        if sid not in seen:
            seen.add(sid)
            out.append(s)
    return out


def _assign_categories(symbols: list[dict], categories: list[dict]) -> list[dict]:
    cat_map = {c["id"]: c for c in categories}
    for s in symbols:
        cid = s.get("category", "")
        if cid not in cat_map:
            cat_map[cid] = {
                "id": cid,
                "name": cid.replace("_", " ").title(),
                "gost": s.get("gost", ""),
                "description": "",
                "svg_preview": "",
            }
    return list(cat_map.values())


def main():
    data_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(data_dir, "symbol_library.json")

    symbols = build_primary_symbols() + build_secondary_symbols()
    symbols = _dedup(symbols)
    categories = _assign_categories(symbols, CATEGORIES)

    library = {
        "version": "6.0",
        "description": (
            "GOST/ESKD-compliant symbol library for single-line and normal-mode "
            "electrical connection diagrams of power facilities 6-750 kV"
        ),
        "gost_references": GOST_REFERENCES,
        "categories": categories,
        "symbols": symbols,
    }

    encoding = _Utf8NoBom()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(library, f, ensure_ascii=False, indent=2, sort_keys=False)

    _strip_bom(out_path)

    print(f"Generated {out_path}")
    print(f"  Categories: {len(categories)}")
    print(f"  Symbols:    {len(symbols)}")


class _Utf8NoBom:
    pass


def _strip_bom(path: str):
    with open(path, "rb") as f:
        data = f.read()
    if data[:3] == b"\xef\xbb\xbf":
        data = data[3:]
    with open(path, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()

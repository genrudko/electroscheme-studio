"""
_append.py  —  appends the remaining symbols + main() to _gen_v2.py
Run this once after _gen_v2.py has been partially written, then run _gen_v2.py to produce JSON.
"""
import io
import os

SRC = r"G:\electroscheme-studio\backend\app\data\_gen_v2.py"
NEW = SRC  # overwrite in place with full content

# We read existing, strip any trailing partial line, then append the rest.
with io.open(SRC, "r", encoding="utf-8") as f:
    content = f.read()

# Find last complete S.append for "truck" - cut there
marker = 'S.append(("truck"'
idx = content.find(marker)
# back up to the start of the line
line_start = content.rfind("\n", 0, idx) + 1
content = content[:line_start]

TAIL = '''
S.append(("truck","switchgear","Тележка КРУ","switchgear","ЕСКД/СТО","-","-2 6 104 30",96,30,
    [{"id":"t1","rx":10,"ry":-3},{"id":"t2","rx":90,"ry":-3},{"id":"t3","rx":10,"ry":33},{"id":"t4","rx":90,"ry":33}],
    {"type":"выдвижной","units":"-"},
    '<rect x="10" y="5" width="80" height="20" fill="none" stroke="black" stroke-width="1.2"/><line x1="10" y1="5" x2="10" y2="25" stroke="black" stroke-width="1"/><line x1="90" y1="5" x2="90" y2="25" stroke="black" stroke-width="1"/><circle cx="10" cy="15" r="2" fill="black"/><circle cx="90" cy="15" r="2" fill="black"/>',
    False, None, []))

S.append(("bus_section_disconnector","switchgear","Разъединитель секционный","switchgear","ЕСКД/СТО","-","-2 6 104 30",96,30,
    [{"id":"t1","rx":5,"ry":15},{"id":"t2","rx":95,"ry":15}],
    {"voltage_kv":10,"units":"кВ"},
    '<line x1="5" y1="15" x2="40" y2="15" stroke="black" stroke-width="1.2"/><line x1="60" y1="15" x2="95" y2="15" stroke="black" stroke-width="1.2"/><circle cx="5" cy="15" r="3" fill="black"/><circle cx="95" cy="15" r="3" fill="black"/><line x1="40" y1="15" x2="48" y2="5" stroke="black" stroke-width="1.2"/><circle cx="50" cy="20" r="2" fill="black"/><line x1="52" y1="20" x2="58" y2="20" stroke="black" stroke-width="1.2"/><text x="48" y="28" font-size="7" font-family="Arial" text-anchor="middle" fill="black">секц</text>',
    True,"in_service",[{"id":"in_service","name":"В работе","alternate_svg":'<line x1="5" y1="15" x2="40" y2="15" stroke="black" stroke-width="1.2"/><line x1="60" y1="15" x2="95" y2="15" stroke="black" stroke-width="1.2"/><circle cx="5" cy="15" r="3" fill="black"/><circle cx="95" cy="15" r="3" fill="black"/><line x1="40" y1="15" x2="50" y2="15" stroke="black" stroke-width="1.2"/><line x1="50" y1="15" x2="58" y2="20" stroke="black" stroke-width="1.2"/><text x="48" y="28" font-size="7" font-family="Arial" text-anchor="middle" fill="black">секц</text>'},{"id":"bypass","name":"Шунтирован","alternate_svg":'<line x1="5" y1="15" x2="40" y2="15" stroke="black" stroke-width="1.2"/><line x1="60" y1="15" x2="95" y2="15" stroke="black" stroke-width="1.2"/><circle cx="5" cy="15" r="3" fill="black"/><circle cx="95" cy="15" r="3" fill="black"/><line x1="40" y1="15" x2="50" y2="15" stroke="black" stroke-width="1.2"/><line x1="50" y1="15" x2="58" y2="8" stroke="black" stroke-width="1.2"/><text x="48" y="28" font-size="7" font-family="Arial" text-anchor="middle" fill="black">секц</text>'}]))

S.append(("bus_disconnector","switchgear","Шинный разъединитель","switchgear","ЕСКД/СТО","-","-2 6 104 30",96,30,
    [{"id":"t1","rx":5,"ry":15},{"id":"t2","rx":95,"ry":15}],
    {"voltage_kv":10,"units":"кВ"},
    '<line x1="5" y1="15" x2="40" y2="15" stroke="black" stroke-width="1.2"/><line x1="60" y1="15" x2="95" y2="15" stroke="black" stroke-width="1.2"/><circle cx="5" cy="15" r="3" fill="black"/><circle cx="95" cy="15" r="3" fill="black"/><line x1="40" y1="15" x2="48" y2="5" stroke="black" stroke-width="1.2"/><circle cx="50" cy="20" r="2" fill="black"/><line x1="52" y1="20" x2="58" y2="20" stroke="black" stroke-width="1.2"/><text x="48" y="12" font-size="7" font-family="Arial" text-anchor="middle" fill="black">шин</text>',
    False, None, []))

S.append(("line_disconnector","switchgear","Линейный разъединитель","switchgear","ЕСКД/СТО","-","-2 6 104 30",96,30,
    [{"id":"t1","rx":50,"ry":0},{"id":"t2","rx":50,"ry":30}],
    {"voltage_kv":10,"units":"кВ"},
    '<line x1="50" y1="0" x2="50" y2="10" stroke="black" stroke-width="1.2"/><line x1="50" y1="20" x2="50" y2="30" stroke="black" stroke-width="1.2"/><circle cx="50" cy="0" r="3" fill="black"/><circle cx="50" cy="30" r="3" fill="black"/><line x1="50" y1="10" x2="42" y2="15" stroke="black" stroke-width="1.2"/><circle cx="50" cy="20" r="2" fill="black"/><line x1="50" y1="20" x2="44" y2="22" stroke="black" stroke-width="1.2"/>',
    False, None, []))

S.append(("outgoing_protection","switchgear","Защита отходящей линии","switchgear","ЕСКД/СТО","-","-2 6 104 30",96,30,
    [{"id":"t1","rx":50,"ry":0},{"id":"t2","rx":50,"ry":30}],
    {"voltage_kv":10,"current_a":630,"units":"кВ/А"},
    '<rect x="40" y="5" width="20" height="20" fill="none" stroke="black" stroke-width="1.2"/><line x1="50" y1="0" x2="50" y2="5" stroke="black" stroke-width="1.2"/><line x1="50" y1="25" x2="50" y2="30" stroke="black" stroke-width="1.2"/><circle cx="50" cy="0" r="3" fill="black"/><circle cx="50" cy="30" r="3" fill="black"/><line x1="44" y1="15" x2="56" y2="15" stroke="black" stroke-width="1"/>',
    False, None, []))

S.append(("switchgear_bus_tie","switchgear","Секционный АВ","switchgear","ЕСКД/СТО","-","-2 6 104 30",96,30,
    [{"id":"t1","rx":50,"ry":0},{"id":"t2","rx":50,"ry":30}],
    {"voltage_kv":10,"current_a":1000,"units":"кВ/А"},
    '<rect x="40" y="5" width="20" height="20" rx="2" fill="none" stroke="black" stroke-width="1.2"/><line x1="50" y1="0" x2="50" y2="5" stroke="black" stroke-width="1.2"/><line x1="50" y1="25" x2="50" y2="30" stroke="black" stroke-width="1.2"/><circle cx="50" cy="0" r="3" fill="black"/><circle cx="50" cy="30" r="3" fill="black"/><text x="50" y="18" font-size="7" font-family="Arial" text-anchor="middle" fill="black">АВ</text>',
    True,"closed",[{"id":"closed","name":"Включён","alternate_svg":'<rect x="40" y="5" width="20" height="20" rx="2" fill="none" stroke="black" stroke-width="1.2"/><line x1="50" y1="0" x2="50" y2="5" stroke="black" stroke-width="1.2"/><line x1="50" y1="25" x2="50" y2="30" stroke="black" stroke-width="1.2"/><circle cx="50" cy="0" r="3" fill="black"/><circle cx="50" cy="30" r="3" fill="black"/><line x1="50" y1="10" x2="50" y2="20" stroke="black" stroke-width="1.5"/><text x="65" y="18" font-size="7" font-family="Arial" fill="black">closed</text>'},{"id":"open","name":"Отключён","alternate_svg":'<rect x="40" y="5" width="20" height="20" rx="2" fill="none" stroke="black" stroke-width="1.2"/><line x1="50" y1="0" x2="50" y2="5" stroke="black" stroke-width="1.2"/><line x1="50" y1="25" x2="50" y2="30" stroke="black" stroke-width="1.2"/><circle cx="50" cy="0" r="3" fill="black"/><circle cx="50" cy="30" r="3" fill="black"/><line x1="50" y1="10" x2="50" y2="15" stroke="black" stroke-width="1.5"/><line x1="50" y1="15" x2="44" y2="20" stroke="black" stroke-width="1.2"/><text x="65" y="18" font-size="7" font-family="Arial" fill="black">open</text>'},{"id":"test","name":"Тестовое положение","alternate_svg":'<rect x="40" y="5" width="20" height="20" rx="2" fill="none" stroke="gray" stroke-width="1.2" stroke-dasharray="2,1"/><line x1="50" y1="0" x2="50" y2="5" stroke="gray" stroke-width="1.2"/><line x1="50" y1="25" x2="50" y2="30" stroke="gray" stroke-width="1.2"/><circle cx="50" cy="0" r="3" fill="gray"/><circle cx="50" cy="30" r="3" fill="gray"/><text x="65" y="18" font-size="7" font-family="Arial" fill="gray">test</text>'},{"id":"disconnected","name":"Отключено и выкачено","alternate_svg":'<rect x="40" y="5" width="20" height="20" rx="2" fill="none" stroke="gray" stroke-width="1.2" stroke-dasharray="1,1"/><line x1="50" y1="0" x2="50" y2="5" stroke="gray" stroke-width="1"/><line x1="50" y1="25" x2="50" y2="30" stroke="gray" stroke-width="1"/><circle cx="50" cy="0" r="2" fill="gray"/><circle cx="50" cy="30" r="2" fill="gray"/><text x="65" y="18" font-size="7" font-family="Arial" fill="gray">disc</text>'}]))

# ---------------------------------------------------------------------------
# Semiconductors
# ---------------------------------------------------------------------------
S.append(("diode","semiconductors","Диод","semiconductors","ГОСТ 2.730-73","1.1","-2 6 104 30",96,30,
    [{"id":"t1","rx":0,"ry":15},{"id":"t2","rx":95,"ry":15}],
    {"current_a":100,"voltage_v":1000,"series":"1N","units":"А/В"},
    '<line x1="0" y1="15" x2="35" y2="15" stroke="black" stroke-width="1.2"/><polygon points="35,8 35,22 55,15" fill="none" stroke="black" stroke-width="1.2"/><line x1="55" y1="8" x2="55" y2="22" stroke="black" stroke-width="1.2"/><line x1="55" y1="15" x2="95" y2="15" stroke="black" stroke-width="1.2"/>',
    False, None, []))

S.append(("thyristor","semiconductors","Тиристор","semiconductors","ГОСТ 2.730-73","5.1","-2 6 104 30",96,30,
    [{"id":"t1","rx":0,"ry":15},{"id":"t2","rx":95,"ry":15},{"id":"gate","rx":50,"ry":25}],
    {"current_a":200,"voltage_v":1600,"series":"T","units":"А/В"},
    '<line x1="0" y1="15" x2="35" y2="15" stroke="black" stroke-width="1.2"/><polygon points="35,8 35,22 55,15" fill="none" stroke="black" stroke-width="1.2"/><line x1="55" y1="8" x2="55" y2="22" stroke="black" stroke-width="1.2"/><line x1="48" y1="22" x2="62" y2="22" stroke="black" stroke-width="1.2"/><line x1="48" y1="22" x2="48" y2="30" stroke="black" stroke-width="1.2"/><line x1="55" y1="15" x2="95" y2="15" stroke="black" stroke-width="1.2"/><circle cx="48" cy="30" r="2" fill="black"/>',
    False, None, []))

S.append(("varistor","semiconductors","Варистор","semiconductors","ГОСТ 2.730-73","3.3","-2 6 104 30",96,30,
    [{"id":"t1","rx":0,"ry":15},{"id":"t2","rx":95,"ry":15}],
    {"voltage_v":275,"energy_j":100,"units":"В/Дж"},
    '<line x1="0" y1="15" x2="35" y2="15" stroke="black" stroke-width="1.2"/><rect x="35" y="8" width="20" height="14" fill="none" stroke="black" stroke-width="1.2"/><line x1="35" y1="15" x2="45" y2="10" stroke="black" stroke-width="1"/><line x1="55" y1="15" x2="45" y2="20" stroke="black" stroke-width="1"/><line x1="55" y1="8" x2="55" y2="22" stroke="black" stroke-width="1.2"/><line x1="55" y1="15" x2="95" y2="15" stroke="black" stroke-width="1.2"/>',
    False, None, []))

# ---------------------------------------------------------------------------
# General
# ---------------------------------------------------------------------------
S.append(("ground","general","Заземление","general","ГОСТ 2.721-74","7.1.3.1","-2 -6 30 40",24,36,
    [{"id":"t1","rx":12,"ry":0}],
    {"type":"protective","units":"-"},
    '<line x1="12" y1="0" x2="12" y2="14" stroke="black" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="black" stroke-width="1.2"/><line x1="4" y1="19" x2="20" y2="19" stroke="black" stroke-width="1"/><line x1="8" y1="24" x2="16" y2="24" stroke="black" stroke-width="0.8"/><line x1="10" y1="29" x2="14" y2="29" stroke="black" stroke-width="0.7"/>',
    False, None, []))

S.append(("connection_point","general","Точка соединения","general","ГОСТ 2.721-74","4.1","-2 -2 12 12",8,8,
    [{"id":"t1","rx":6,"ry":6}],
    {"units":"-"},
    '<circle cx="6" cy="6" r="3" fill="black"/>',
    False, None, []))

S.append(("chassis_ground","general","Корпусное заземление","general","ГОСТ 2.721-74","7.1.3.3","-2 -6 36 40",28,36,
    [{"id":"t1","rx":14,"ry":0}],
    {"type":"chassis","units":"-"},
    '<line x1="14" y1="0" x2="14" y2="22" stroke="black" stroke-width="1.2"/><line x1="0" y1="22" x2="28" y2="22" stroke="black" stroke-width="1.2"/><line x1="10" y1="14" x2="18" y2="14" stroke="black" stroke-width="1"/><line x1="12" y1="10" x2="16" y2="10" stroke="black" stroke-width="0.8"/><polygon points="25,14 25,22 28,18 22,18" fill="black"/>',
    False, None, []))

# ---------------------------------------------------------------------------
# Scheme types (graphic macros for scheme templates)
# ---------------------------------------------------------------------------
S.append(("scheme_type_electric","scheme_types","Электрическая схема","scheme_types","ГОСТ 2.701-2008","Е","0 0 200 150",200,150,
    [],
    {"type":"diagram","code":"E","units":"-"},
    '<rect x="0" y="0" width="200" height="150" fill="none" stroke="black" stroke-width="1.2"/><text x="100" y="75" font-size="14" font-family="Arial" text-anchor="middle" fill="black">СХЕМА ЭЛЕКТРИЧЕСКАЯ (Е)</text>',
    False, None, []))

S.append(("scheme_type_single_line","scheme_types","Однолинейная схема","scheme_types","ГОСТ 2.701-2008","0","0 0 200 150",200,150,
    [],
    {"type":"diagram","code":"0","units":"-"},
    '<rect x="0" y="0" width="200" height="150" fill="none" stroke="black" stroke-width="1.2"/><text x="100" y="75" font-size="14" font-family="Arial" text-anchor="middle" fill="black">СХЕМА ОДНОЛИНЕЙНАЯ (0)</text>',
    False, None, []))

S.append(("scheme_type_multi_line","scheme_types","Многолинейная схема","scheme_types","ГОСТ 2.701-2008","1","0 0 200 150",200,150,
    [],
    {"type":"diagram","code":"1","units":"-"},
    '<rect x="0" y="0" width="200" height="150" fill="none" stroke="black" stroke-width="1.2"/><text x="100" y="75" font-size="14" font-family="Arial" text-anchor="middle" fill="black">СХЕМА МНОГОЛИНЕЙНАЯ (1)</text>',
    False, None, []))

# ---------------------------------------------------------------------------
# Build the JSON structure
# ---------------------------------------------------------------------------
def build_library():
    categories_order = [
        ("passive","Пассивные компоненты"),
        ("magnetic","Магнитные компоненты"),
        ("measuring_transformers","Измерительные трансформаторы"),
        ("switching","Коммутационные аппараты"),
        ("protection","Защитные аппараты"),
        ("relay_protection","Релейная защита и автоматика"),
        ("machines","Машины и источники"),
        ("instruments","Приборы измерения"),
        ("power_lines","Линии и проводники"),
        ("switchgear","Комплектные распределительные устройства"),
        ("semiconductors","Полупроводники"),
        ("general","Общие графические элементы"),
        ("scheme_types","Типы схем"),
    ]

    gost_references = [
        ("ГОСТ 2.728-74","Обозначения условные графические в схемах. Резисторы, конденсаторы"),
        ("ГОСТ 2.723-68","Обозначения условные графические в схемах. Катушки индуктивности, дроссели, реакторы, трансформаторы"),
        ("ГОСТ 2.755-87","Обозначения условные графические в схемах. Устройства коммутационные"),
        ("ГОСТ 2.727-68","Обозначения условные графические в схемах. Разрядники, предохранители"),
        ("ГОСТ 2.756-76","Обозначения условные графические в схемах. Электрические связи"),
        ("ГОСТ 2.722-68","Обозначения условные графические в схемах. Электрические машины"),
        ("ГОСТ 2.729-68","Обозначения условные графические в схемы. Приборы электроизмерительные"),
        ("ГОСТ 2.721-74","Обозначения условные графические в схемах. Обозначения общего применения"),
        ("ГОСТ 2.701-2008","ЕСКД. Схемы. Виды и типы"),
        ("ГОСТ 2.730-73","Обозначения условные графические в схемах. Приборы полупроводниковые"),
        ("ЕСКД/СТО","Единая система конструкторской документации и стандарты организаций (секционные и шинные разъединители, ячейки КРУ)"),
    ]

    symbols = []
    for e in S:
        sid,cat_type,name,category,gost,gost_ref,vb,w,h,terminals,props,svg,interactive,def_state,states = e
        symbols.append({
            "id": sid,
            "type": cat_type,
            "name": name,
            "category": category,
            "gost": gost,
            "gost_ref": gost_ref,
            "viewBox": vb,
            "default_width": w,
            "default_height": h,
            "terminals": terminals,
            "default_properties": props,
            "svg": svg,
            "interactive": interactive,
            "default_state": def_state,
            "current_state": def_state,
            "states": states
        })

    categories = []
    for cid, cname in categories_order:
        cat_syms = [sym for sym in symbols if sym["category"] == cid]
        categories.append({
            "id": cid,
            "name": cname,
            "symbol_count": len(cat_syms),
            "symbols": [sym["id"] for sym in cat_syms]
        })

    return {
        "version": "2.0",
        "description": "Расширенная библиотека графических символов ElectroScheme Studio для схем энергообъектов",
        "gost_references": [{"code": code, "title": title} for code, title in gost_references],
        "categories": categories,
        "symbols": symbols,
        "total_symbols": len(symbols)
    }


def main():
    lib = build_library()
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "symbol_library.json")
    write_utf8_no_bom(out_path, json.dumps(lib, ensure_ascii=False, indent=2))
    print("OK written:", out_path)
    print("Total symbols:", lib["total_symbols"])
    for cat in lib["categories"]:
        print(f"  {cat['id']}: {cat['name']} ({cat['symbol_count']})")

if __name__ == "__main__":
    main()
'''

content += TAIL

with io.open(NEW, "w", encoding="utf-8") as f:
    f.write(content)

print("appended OK, new size:", len(content))

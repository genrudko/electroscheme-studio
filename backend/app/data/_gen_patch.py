"""
Patch: add 8 more symbols to reach 80+ total, then regenerate JSON.
"""
import io
import os
import json

SRC = r"G:\electroscheme-studio\backend\app\data\_gen_v2.py"

with io.open(SRC, "r", encoding="utf-8") as f:
    content = f.read()

# Insert before the build_library function
marker = "# ---------------------------------------------------------------------------\n# Build the JSON structure"
idx = content.find(marker)
head = content[:idx]
tail = content[idx:]

EXTRA = '''# ---------------------------------------------------------------------------
# Extra symbols to reach 80+
# ---------------------------------------------------------------------------
S.append(("fuse_vault","protection","Предохранитель-выключатель","protection","ГОСТ 2.727-68","3.11","-2 6 104 30",96,30,
    [{"id":"t1","rx":0,"ry":15},{"id":"t2","rx":95,"ry":15}],
    {"voltage_kv":10,"current_a":630,"units":"кВ/А"},
    '<line x1="0" y1="15" x2="30" y2="15" stroke="black" stroke-width="1.2"/><rect x="30" y="8" width="35" height="14" fill="none" stroke="black" stroke-width="1.2"/><line x1="40" y1="12" x2="55" y2="12" stroke="black" stroke-width="1"/><line x1="40" y1="18" x2="55" y2="18" stroke="black" stroke-width="1"/><line x1="65" y1="15" x2="95" y2="15" stroke="black" stroke-width="1.2"/>',
    False, None, []))

S.append(("reactor_air","magnetic","Реактор дугогасящий","magnetic","ГОСТ 2.723-68","3.1","-2 6 104 30",96,30,
    [{"id":"t1","rx":0,"ry":15},{"id":"t2","rx":95,"ry":15}],
    {"voltage_kv":10,"current_a":100,"units":"кВ/А"},
    '<line x1="0" y1="15" x2="25" y2="15" stroke="black" stroke-width="1.2"/><path d="M25,15 q5,-10 10,0 q5,10 10,0 q5,-10 10,0 q5,10 10,0 q5,-10 10,0" fill="none" stroke="black" stroke-width="1.2"/><line x1="75" y1="15" x2="95" y2="15" stroke="black" stroke-width="1.2"/><line x1="50" y1="25" x2="50" y2="30" stroke="black" stroke-width="1"/><line x1="45" y1="30" x2="55" y2="30" stroke="black" stroke-width="1"/>',
    False, None, []))

S.append(("ct_iron_core","measuring_transformers","ТТ с железным сердечником","measuring_transformers","ГОСТ 2.723-68","5.1","-2 6 104 30",96,30,
    [{"id":"t1","rx":0,"ry":10},{"id":"t2","rx":95,"ry":10},{"id":"s1","rx":0,"ry":22},{"id":"s2","rx":95,"ry":22}],
    {"ratio":"100/5","class":"0.5","units":"А/А"},
    '<line x1="0" y1="10" x2="25" y2="10" stroke="black" stroke-width="1.2"/><circle cx="50" cy="10" r="22" fill="none" stroke="black" stroke-width="1.2"/><line x1="75" y1="10" x2="95" y2="10" stroke="black" stroke-width="1.2"/><line x1="0" y1="22" x2="25" y2="22" stroke="black" stroke-width="1"/><line x1="75" y1="22" x2="95" y2="22" stroke="black" stroke-width="1"/><text x="50" y="14" font-size="7" font-family="Arial" text-anchor="middle" fill="black">ТТ</text>',
    False, None, []))

S.append(("vt_group","measuring_transformers","Группа напряжения","measuring_transformers","ГОСТ 2.723-68","5.2","-2 6 104 40",96,40,
    [{"id":"t1","rx":50,"ry":0},{"id":"t2","rx":50,"ry":40},{"id":"s1","rx":80,"ry":0},{"id":"s2","rx":80,"ry":40}],
    {"ratio":"10000/100","class":"0.5","units":"В/В"},
    '<line x1="50" y1="0" x2="50" y2="10" stroke="black" stroke-width="1.2"/><circle cx="50" cy="20" r="10" fill="none" stroke="black" stroke-width="1.2"/><line x1="50" y1="30" x2="50" y2="40" stroke="black" stroke-width="1.2"/><line x1="80" y1="0" x2="80" y2="10" stroke="black" stroke-width="1"/><circle cx="80" cy="20" r="10" fill="none" stroke="black" stroke-width="1"/><line x1="80" y1="30" x2="80" y2="40" stroke="black" stroke-width="1"/><text x="50" y="24" font-size="6" font-family="Arial" text-anchor="middle" fill="black">ТН</text><text x="80" y="24" font-size="6" font-family="Arial" text-anchor="middle" fill="black">ТН</text>',
    False, None, []))

S.append(("relay_differential","relay_protection","Реле дифференциальное","relay_protection","ГОСТ 2.756-76","3.1","-2 6 104 30",96,30,
    [{"id":"t1","rx":0,"ry":10},{"id":"t2","rx":95,"ry":10},{"id":"s1","rx":0,"ry":22},{"id":"s2","rx":95,"ry":22}],
    {"type":"differential","units":"-"},
    '<rect x="25" y="3" width="45" height="24" fill="none" stroke="black" stroke-width="1.2"/><line x1="0" y1="10" x2="25" y2="10" stroke="black" stroke-width="1"/><line x1="70" y1="10" x2="95" y2="10" stroke="black" stroke-width="1"/><line x1="0" y1="22" x2="25" y2="22" stroke="black" stroke-width="1"/><line x1="70" y1="22" x2="95" y2="22" stroke="black" stroke-width="1"/><text x="47" y="18" font-size="7" font-family="Arial" text-anchor="middle" fill="black">I1-I2</text>',
    False, None, []))

S.append(("relay_frequency","relay_protection","Реле частоты","relay_protection","ГОСТ 2.756-76","3.1","-2 6 104 30",96,30,
    [{"id":"t1","rx":0,"ry":15},{"id":"t2","rx":95,"ry":15}],
    {"type":"frequency","units":"Гц"},
    '<rect x="25" y="3" width="45" height="24" fill="none" stroke="black" stroke-width="1.2"/><line x1="0" y1="15" x2="25" y2="15" stroke="black" stroke-width="1"/><line x1="70" y1="15" x2="95" y2="15" stroke="black" stroke-width="1"/><text x="47" y="18" font-size="8" font-family="Arial" text-anchor="middle" fill="black">Hz</text>',
    False, None, []))

S.append(("motor_dc","machines","Двигатель постоянного тока","machines","ГОСТ 2.722-68","2.2","-2 6 104 30",96,30,
    [{"id":"t1","rx":50,"ry":0},{"id":"t2","rx":50,"ry":30}],
    {"power_kw":10,"voltage_v":220,"units":"кВт/В"},
    '<circle cx="50" cy="15" r="14" fill="none" stroke="black" stroke-width="1.2"/><line x1="50" y1="1" x2="50" y2="5" stroke="black" stroke-width="1.2"/><line x1="50" y1="25" x2="50" y2="29" stroke="black" stroke-width="1.2"/><text x="50" y="19" font-size="10" font-family="Arial" text-anchor="middle" fill="black">M</text><text x="62" y="22" font-size="6" font-family="Arial" fill="black">=</text>',
    False, None, []))

S.append(("battery","machines","Аккумуляторная батарея","machines","ГОСТ 2.728-74","1.1","-2 6 104 30",96,30,
    [{"id":"t1","rx":0,"ry":15},{"id":"t2","rx":95,"ry":15}],
    {"voltage_v":12,"capacity_ah":100,"units":"В/Ач"},
    '<line x1="0" y1="15" x2="30" y2="15" stroke="black" stroke-width="1.2"/><line x1="30" y1="8" x2="30" y2="22" stroke="black" stroke-width="1.5"/><line x1="38" y1="5" x2="38" y2="25" stroke="black" stroke-width="0.8"/><line x1="45" y1="8" x2="45" y2="22" stroke="black" stroke-width="1.5"/><line x1="53" y1="5" x2="53" y2="25" stroke="black" stroke-width="0.8"/><line x1="60" y1="8" x2="60" y2="22" stroke="black" stroke-width="1.5"/><line x1="60" y1="15" x2="95" y2="15" stroke="black" stroke-width="1.2"/><text x="34" y="4" font-size="8" font-family="Arial" fill="black">+</text>',
    False, None, []))

'''

content = head + EXTRA + tail

with io.open(SRC, "w", encoding="utf-8") as f:
    f.write(content)

print("patched OK, new size:", len(content))

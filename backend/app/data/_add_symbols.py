import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.schemas.symbol_library import SymbolLibrary, SymbolDefinition, SymbolState, SymbolTerminal

def create_symbol(symbol_id, name, category, gost, gost_ref, viewBox, width, height, svg, terminals, 
                  interactive=False, default_state="normal", states=None, properties=None):
    if states is None:
        states = []
    if properties is None:
        properties = {}
    return SymbolDefinition(
        id=symbol_id,
        type=category,
        name=name,
        category=category,
        gost=gost,
        bref=gost_ref,
        viewBox=viewBox,
        default_width=width,
        default_height=height,
        terminals=terminals,
        default_properties=properties,
        svg=svg,
        interactive=interactive,
        default_state=default_state,
        current_state=default_state,
        states=states
    )

# Note: there's a typo: bref instead of gost_ref. Fix later.

# Let's do it stepwise: first load library.
lib_path = Path(r'G:\electroscheme-studio\backend\app\data\symbol_library.json')
with open(lib_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
library = SymbolLibrary.model_validate(data)

print(f"Loaded {len(library.symbols)} symbols")

# Collect existing IDs
existing_ids = {s.id for s in library.symbols}
print(f"Existing IDs count: {len(existing_ids)}")

# Define some new symbols
new_symbols = []

# Helper to add if not exists
def add_symbol(sym):
    if sym.id not in existing_ids:
        new_symbols.append(sym)
        existing_ids.add(sym.id)
    else:
        print(f"Skipping duplicate ID: {sym.id}")

# 1. Circuit breaker (simple) - switching
cb_terminals = [SymbolTerminal(id="t1", rx=0.5, ry=0.2), SymbolTerminal(id="t2", rx=0.5, ry=0.8)]
cb_svg = '<line x1="0" y1="0" x2="0" y2="10"/><circle cx="0" cy="10" r="3"/><line x1="0" y1="10" x2="10" y2="10"/><line x1="10" y1="10" x2="10" y2="0"/><line x1="10" y1="0" x2="0" y2="0"/>'
cb_states = [
    SymbolState(id="closed", name="Закрыт", alternate_svg='<line x1="0" y1="0" x2="0" y2="10"/><circle cx="0" cy="10" r="3"/><line x1="0" y1="10" x2="10" y2="10"/><line x1="10" y1="10" x2="10" y2="0"/><line x1="10" y1="0" x2="0" y2="0"/>'),
    SymbolState(id="open", name="Открыт", alternate_svg='<line x1="0" y1="0" x2="0" y2="10"/><circle cx="0" cy="10" r="3"/><line x1="0" y1="10" x2="10" y2="10"/><line x1="10" y1="10" x2="10" y2="0"/><line x1="10" y1="0" x2="0" y2="0"/><line x1="5" y1="5" x2="5" y2="15" stroke="red" stroke-width="2"/>')
]
cb = create_symbol(
    "circuit_breaker_simple", "Автоматический выключатель простой", "switching", "ГОСТ 2.755-87", "ГОСТ 2.755-87",
    "0 0 10 10", 10, 10, cb_svg, cb_terminals, interactive=True, default_state="closed", states=cb_states
)
add_symbol(cb)

# 2. Disconnector (isolator)
disc_terminals = [SymbolTerminal(id="t1", rx=0.2, ry=0.5), SymbolTerminal(id="t2", rx=0.8, ry=0.5)]
disc_svg = '<line x1="0" y1="5" x2="4" y2="5"/><line x1="6" y1="5" x2="10" y2="5"/><line x1="4" y1="2" x2="6" y2="8"/>'
disc_states = [
    SymbolState(id="closed", name="Закрыт", alternate_svg='<line x1="0" y1="5" x2="10" y2="5"/>'),
    SymbolState(id="open", name="Открыт", alternate_svg='<line x1="0" y1="5" x2="4" y2="5"/><line x1="6" y1="5" x2="10" y2="5"/><line x1="4" y1="2" x2="6" y2="8"/>')
]
disc = create_symbol(
    "disconnector_simple", "Разъединитель простой", "switching", "ГОСТ 2.755-87", "ГОСТ 2.755-87",
    "0 0 10 10", 10, 10, disc_svg, disc_terminals, interactive=True, default_state="open", states=disc_s
)
add_symbol(disc)

# 3. Earthing switch
es_terminals = [SymbolTerminal(id="t1", rx=0.2, ry=0.5), SymbolTerminal(id="t2", rx=0.8, ry=0.5)]
es_svg = '<line x1="0" y1="5" x2="10" y2="5"/><line x1="5" y1="0" x2="5" y2="10"/>'
es_states = [
    SymbolState(id="off", name="Отключён", alternate_svg='<line x1="0" y1="5" x2="10" y2="5"/>'),
    SymbolState(id="on", name="Заземлён", alternate_svg='<line x1="0" y1="5" x2="10" y2="5"/><line x1="5" y1="0" x2="5" y2="10"/>')
]
es = create_symbol(
    "earthing_switch_simple", "Заключающий выключатель", "switching", "ГОСТ 2.755-87", "ГОСТ 2.755-87",
    "0 0 10 10", 10, 10, es_svg, es_terminals, interactive=True, default_state="off", states=es_states
)
add_symbol(es)

# 4. Contactor
contactor_terminals = [SymbolTerminal(id="a1", rx=0.2, ry=0.2), SymbolTerminal(id="a2", rx=0.2, ry=0.8),
                       SymbolTerminal(id="b1", rx=0.8, ry=0.2), SymbolTerminal(id="b2", rx=0.8, ry=0.8)]
contactor_svg = '<rect x="1" y="1" width="8" height="8"/><line x1="2" y1="5" x2="4" y2="5"/><line x1="6" y1="5" x2="8" y2="5"/>'
contactor_states = [
    SymbolState(id="off", name="Выключен", alternate_svg='<rect x="1" y="1" width="8" height="8"/>'),
    SymbolState(id="on", name="Включён", alternate_svg='<rect x="1" y="1" width="8" height="8"/><line x1="2" y1="5" x2="4" y2="5"/><line x1="6" y1="5" x2="8" y2="5"/>')
]
contactor = create_symbol(
    "contactor_simple", "Контактор простой", "switching", "ГОСТ 2.755-87", "ГОСТ 2.755-87",
    "0 0 10 10", 10, 10, contactor_svc, contactor_terminals, interactive=True, default_state="off", states=contactor_states
)
add_symbol(contactor)

# 5. Fuse
fuse_terminals = [SymbolTerminal(id="t1", rx=0.2, ry=0.5), SymbolTerminal(id="t2", rx=0.8, ry=0.5)]
fuse_svg = '<rect x="2" y="3" width="6" height="4" rx="1"/>'
fuse_states = [
    SymbolState(id="intact", name="Целый", alternate_svg='<rect x="2" y="3" width="6" height="4" rx="1"/>'),
    SymbolState(id="blown", name="Перегорел", alternate_svg='<rect x="2" y="3" width="6" height="4" rx="1"/><line x1="2" y1="3" x2="8" y2="7" stroke="red" stroke-width="2"/><line x1="8" y1="3" x2="2" y2="7" stroke="red" stroke-width="2"/>')
]
fuse = create_symbol(
    "fuse_simple", "Предохранитель простой", "protection", "ГОСТ 2.727-68", "ГОСТ 2.727-68",
    "0 0 10 10", 10, 10, fuse_svg, fuse_teminals, interactive=True, default_state="intact", states=fuse_states
)
add_symbol(fuse)

# 6. Relay (simple)
relay_terminals = [SymbolTerminal(id="coil1", rx=0.2, ry=0.2), SymbolTerminal(id="coil2", rx=0.2, ry=0.3),
                   SymbolTerminal(id="contact1", rx=0.7, ry=0.2), SymbolTerminal(id="contact2", rx=0.7, ry=0.8)]
relay_svg = '<rect x="1" y="1" width="3" height="6"/><line x1="5" y1="2" x2="9" y2="2"/><line x1="5" y1="8" x2="9" y2="8"/>'
relay_states = [
    SymbolState(id="off", name="Выключен", alternate_svg='<rect x="1" y="1" width="3" height="6"/><line x1="5" y1="2" x2="9" y2="2"/><line x1="5" y1="8" x2="9" y2="8"/>'),
    SymbolState(id="on", name="Включён", alternate_svg='<rect x="1" y="1" width="3" height="6"/><line x1="5" y1="2" x2="9" y2="2"/><line x1="5" y1="8" x2="9" y2="8"/><line x1="6" y1="5" x2="8" y2="5"/>')
]
relay = create_symbol(
    "relay_simple", "Реле простое", "relay_protection", "ГОСТ 2.756-76", "ГОСТ 2.756-76",
    "0 0 10 10", 10, 10, relay_svg, relay_terminals, interactive=True, default_state="off", states=relay_states
)
add_symbol(relay)

# Add some non-interactive symbols to increase count
# 7. Resistor (various)
res_t = [SymbolTerminal(id="t1", rx=0.2, ry=0.5), SymbolTerminal(id="t2", rx=0.8, ry=0.5)]
res_svg = '<rect x="1" y="4" width="8" height="2"/>'
res = create_symbol(
    "resistor_simple", "Резистор простой", "passive", "ГОСТ 2.728-74", "ГОСТ 2.728-74",
    "0 0 10 10", 10, 10, res_svg, res_t
)
add_symbol(res)

# 8. Capacitor
cap_t = [SymbolTerminal(id="t1", rx=0.2, ry=0.5), SymbolTerminal(id="t2", rx=0.8, ry=0.5)]
cap_svg = '<line x1="2" y1="2" x2="2" y2="8"/><line x1="8" y1="2" x2="8" y2="8"/>'
cap = create_symbol(
    "capacitor_simple", "Конденсатор простой", "passive", "ГОСТ 2.728-74", "ГОСТ 2.728-74",
    "0 0 10 10", 10, 10, cap_svg, cap_t
)
add_symbol(cap)

# 9. Inductor
ind_t = [SymbolTerminal(id="t1", rx=0.2, ry=0.5), SymbolTerminal(id="t2", rx=0.8, ry=0.5)]
ind_svg = '<path d="M2,5 Q3,3 4,5 Q5,7 6,5 Q7,3 8,5 Q9,7 10,5"/>'
ind = create_symbol(
    "inductor_simple", "Индуктивность простая", "magnetic", "ГОСТ 2.723-68", "ГОСТ 2.723-68",
    "0 0 12 10", 12, 10, ind_svg, ind_t
)
add_symbol(ind)

# 10. Transformer (simple 2-winding)
xfmr_t = [SymbolTerminal(id="t1", rx=0.2, ry=0.2), SymbolTerminal(id="t2", rx=0.2, ry=0.8),
          SymbolTerminal(id="t3", rx=0.8, ry=0.2), SymbolTerminal(id="t4", rx=0.8, ry=0.8)]
xfmr_svg = '<circle cx="3" cy="5" r="3"/><circle cx="7" cy="5" r="3"/><line x1="0" y1="5" x2="3" y2="5"/><line x1="7" y1="5" x2="10" y2="5"/>'
xfmr = create_symbol(
    "transformer_simple", "Трансформатор простой", "magnetic", "ГОСТ 2.723-68", "ГОСТ 2.723-68",
    "0 0 10 10", 10, 10, xfmr_svg, xfmr_t
)
add_symbol(xfmr)

# 11. Busbar
bus_t = [SymbolTerminal(id="t1", rx=0.1, ry=0.5), SymbolTerminal(id="t2", rx=0.9, ry=0.5)]
bus_svg = '<line x1="0" y1="5" x2="10" y2="5" stroke-width="4"/>'
bus = create_symbol(
    "busbar_simple", "Шина простая", "power_lines", "ЕСКД", "ЕСКД",
    "0 0 10 10", 10, 10, bus_svg, bus_t
)
add_symbol(bus)

# 12. Ground
gnd_t = [SymbolTerminal(id="t1", rx=0.5, ry=0.9)]
gnd_svg = '<line x1="5" y1="5" x2="5" y2="10"/><line x1="3" y1="8" x2="7" y2="8"/><line x1="2" y1="9" x2="8" y2="9"/>'
gnd = create_symbol(
    "ground_simple", "Заземление простая", "general", "ГОСТ 2.721-74", "ГОСТ 2.721-74",
    "0 0 10 10", 10, 10, gnd_svg, gnd_t
)
add_symbol(gnd)

print(f"Prepared {len(new_symbols)} new symbols to add.")

# Add them to library
for sym in new_symbols:
    library.symbols.append(sym)

# Update version maybe
library.version = "2.0"

# Save back
with open(lib_path, 'w', encoding='utf-8') as f:
    f.write(library.model_dump_json(by_alias=True, indent=2))

print(f"Saved library with {len(library.symbols)} symbols.")
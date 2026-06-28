import json, sys
path = r'G:\electroscheme-studio\backend\app\data\symbol_library.json'
with open(path, 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== CATEGORIES ===")
for c in d['categories']:
    print("  {} | {} | {}".format(c['id'], c['name'], c['gost']))

print("\n=== SYMBOLS ===")
for s in d['symbols']:
    interactive = s.get('interactive', False)
    states = [st['id'] for st in s.get('states', [])]
    alt = sum(1 for st in s.get('states', []) if st.get('alternate_svg'))
    print("  {:35s} cat={:25s} int={} states={} alt_svg={}".format(
        s['id'], s['category'], interactive, states, alt))

print("\n=== GOST REFS ===")
for r in d['gost_references']:
    print("  {} | {}".format(r['id'], r['title']))

print("\nTotal: {} symbols, {} interactive".format(
    len(d['symbols']),
    sum(1 for s in d['symbols'] if s.get('interactive', False))
))

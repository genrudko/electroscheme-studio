import json

with open(r'G:\electroscheme-studio\backend\app\data\symbol_library.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total symbols: {len(data['symbols'])}")
print(f"Categories: {len(data['categories'])}")
print(f"GOST references: {len(data['gost_references'])}")

# Count interactive symbols
interactive_count = sum(1 for s in data['symbols'] if s.get('interactive', False))
print(f"Interactive symbols: {interactive_count}")
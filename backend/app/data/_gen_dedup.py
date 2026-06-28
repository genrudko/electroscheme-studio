"""
Remove duplicate S.append entries for relay_differential and motor_dc (keep the new patched ones).
"""
import io
import re

SRC = r"G:\electroscheme-studio\backend\app\data\_gen_v2.py"

with io.open(SRC, "r", encoding="utf-8") as f:
    content = f.read()

# Find all entries and remove those whose id is in the original block (the old duplicates)
# Strategy: for each duplicate id, remove the FIRST S.append occurrence (original), keep LAST (patched)
for dup_id in ["relay_differential", "motor_dc"]:
    marker = f'S.append(("{dup_id}"'
    first = content.find(marker)
    second = content.find(marker, first + 1)
    if second == -1:
        print(f"only one {dup_id}, skip")
        continue
    # remove first occurrence - find its line
    line_start = content.rfind("\n", 0, first) + 1
    # find end of first S.append - look for '))'
    # Due to multiline entries, find next '\n))' or pattern
    # Search for the closing )) after first
    depth = 0
    i = first
    started = False
    while i < len(content):
        ch = content[i]
        if ch == '(':
            depth += 1
            started = True
        elif ch == ')':
            depth -= 1
            if started and depth == 0:
                break
        i += 1
    # include trailing newline
    line_end = content.find("\n", i) + 1
    removed = content[line_start:line_end]
    print(f"removing first {dup_id} entry: {len(removed)} chars")
    content = content[:line_start] + content[line_end:]

with io.open(SRC, "w", encoding="utf-8") as f:
    f.write(content)
print("dedup done, new size:", len(content))

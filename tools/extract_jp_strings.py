# -*- coding: utf-8 -*-
"""extract_jp_strings.py — trich TAT CA string literal chua JP trong uitexts toml -> slice"""
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
src, out = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8-sig').read()
jp = re.compile(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]')

# find all basic-string literals "..." (no real newline inside), unescape toml
vals = {}
order = []
for m in re.finditer(r'"((?:[^"\\]|\\.)*)"', t):
    lit = m.group(1)
    if not jp.search(lit):
        continue
    # unescape toml escapes for translation
    unesc = lit.replace('\\"', '"').replace('\\\\', '\\').replace('\\n', '\n').replace('\\t', '\t')
    if unesc not in vals:
        vals[unesc] = lit
        order.append(unesc)

items = [{'id': i, 'jp': s, 'lit': vals[s]} for i, s in enumerate(order)]
json.dump(items, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('unique JP strings:', len(items), '->', out)

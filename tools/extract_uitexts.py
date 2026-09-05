# -*- coding: utf-8 -*-
"""extract_uitexts.py — parse [texts] bang line-based section detection"""
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
src, out = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8', errors='replace').read()
lines = t.splitlines()
# locate [texts] section: a line exactly '[texts]'
start = None
for idx, ln in enumerate(lines):
    if ln.strip() == '[texts]':
        start = idx
        break
end = len(lines)
if start is not None:
    for idx in range(start+1, len(lines)):
        s = lines[idx].strip()
        if s.startswith('[') and s.endswith(']') and not s.startswith('#') and '=' in s and not re.search(r'[\u3040-\u30ff\u4e00-\u9fff]', s):
            end = idx
            break
block = lines[start+1:end] if start is not None else []
items = []
for ln in block:
    mm = re.match(r'^\s*([A-Za-z_0-9]+)\s*=\s*"(.*)"\s*$', ln)
    if mm:
        items.append({'key': mm.group(1), 'jp': mm.group(2)})
json.dump(items, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('keys', len(items), '->', out)

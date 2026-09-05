# -*- coding: utf-8 -*-
"""slice_any.py — tách slice dịch từ 1 file extract JSON.
Dùng: python slice_any.py <extract.json> <out_slice.json> [max_items] [skip_dialogues]
Slice gồm cả dialogues (kind=d) và selects (kind=s) để translator dịch một thể.
"""
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
TAG_RE = re.compile(r'^(?:%[a-zA-Z]+;?)+')

extract, out = sys.argv[1], sys.argv[2]
max_items = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
skip = int(sys.argv[4]) if len(sys.argv) > 4 else 0

data = json.load(open(extract, encoding='utf-8'))
items = []
di_global = 0
n_v2 = 0
n_v0 = 0
for si, scene in enumerate(data.get('scenes', [])):
    for ti, text in enumerate(scene.get('texts', [])):
        for di, dial in enumerate(text.get('dialogues', [])):
            vals = dial.get('values', [])
            jp = ''
            src = ''
            if len(vals) > 2 and isinstance(vals[2], str) and vals[2].strip():
                jp = vals[2]
                src = 'v2'
            elif len(vals) > 0 and isinstance(vals[0], str) and vals[0].strip():
                # values[0]-only line: strip control tag prefix for translation
                raw = vals[0].strip()
                jp = TAG_RE.sub('', raw)
                # skip pure numbers/system (e.g. "10:12." is kept; empty after strip is skipped)
                if jp.strip():
                    src = 'v0'
                else:
                    jp = ''
            if jp.strip():
                if skip <= di_global < skip + max_items:
                    items.append({'kind': 'd', 'i': di_global, 'si': si, 'ti': ti,
                                  'di': di, 'name': text.get('name'), 'jp': jp, 'src': src})
                    if src == 'v2':
                        n_v2 += 1
                    else:
                        n_v0 += 1
            di_global += 1
for si, scene in enumerate(data.get('scenes', [])):
    for sel, s in enumerate(scene.get('selects', [])):
        if isinstance(s, str) and s.strip():
            items.append({'kind': 's', 'si': si, 'sel': sel, 'jp': s})

json.dump(items, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'total_dialogues={di_global} slice_items={len(items)} (v2={n_v2} v0={n_v0}) -> {out}')

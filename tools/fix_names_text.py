# -*- coding: utf-8 -*-
"""bulk fix ten trong vi text theo official DB"""
import sys, os, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
W = sys.argv[1]
pairs = [
    ('Anzu', 'Anju'),
    ('Hiroto', 'Hiromu'),
    ('Yuma', 'Yuuma'),
    ('Kisyo', 'Hinami'),
    ('Ms. Izawa', 'Izawa-sensei'),
]
# word-boundary-ish: khong doi neu di theo chu cai
def fix(s):
    for a, b in pairs:
        s = re.sub(r'(?<![A-Za-z])' + re.escape(a) + r'(?![A-Za-z])', b, s)
    return s

total = 0
files = 0
for fn in sorted(os.listdir(W)):
    if not fn.endswith('.slice.vi.json'):
        continue
    p = os.path.join(W, fn)
    d = json.load(open(p, encoding='utf-8'))
    changed = 0
    for r in d:
        if r.get('vi'):
            nv = fix(r['vi'])
            if nv != r['vi']:
                r['vi'] = nv
                changed += 1
    if changed:
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        files += 1
        total += changed
print(f'fixed {total} lines in {files} files')

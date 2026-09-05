# -*- coding: utf-8 -*-
import sys, os, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
B = sys.argv[1]
W = os.path.join(B, 'work')
nm = json.load(open(os.path.join(B, 'names_map.json'), encoding='utf-8'))
# bo sung whole-name + thieu
nm['新・学生会長'] = 'New Student Council President'
nm['おばちゃん'] = 'Auntie'

def tr_name(n):
    if not n:
        return None
    if n in nm:
        return nm[n]
    parts = n.split('・')
    if all(p in nm for p in parts):
        return ' & '.join(nm[p] for p in parts)
    return None

# full-width -> ascii table
tbl = {}
for c in range(0xFF01, 0xFF5F):
    tbl[c] = c - 0xFEE0
TBL = {k: chr(v) for k, v in tbl.items()}

strip_count = 0
norm_count = 0
files = 0
for fn in sorted(os.listdir(W)):
    if not fn.endswith('.slice.vi.json'):
        continue
    p = os.path.join(W, fn)
    d = json.load(open(p, encoding='utf-8'))
    ch = 0
    for r in d:
        v = r.get('vi')
        if not v:
            continue
        nv = v.translate(TBL)
        en_name = tr_name(r.get('name'))
        if en_name:
            for sep in (': ', ':'):
                pre = en_name + sep
                if nv.startswith(pre):
                    nv = nv[len(pre):].lstrip()
                    strip_count += 1
                    break
        if nv != v:
            r['vi'] = nv
            ch += 1
        if v != v.translate(TBL):
            norm_count += 1
    if ch:
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        files += 1
print(f'strip_prefix={strip_count} normalized_lines={norm_count} files_changed={files}')

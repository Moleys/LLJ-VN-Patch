# -*- coding: utf-8 -*-
"""merge_any.py — ghép bản dịch vào extract JSON (dịch values[0] giữ tag, [2], [3], selects) + name fields."""
import json, re, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# load names map (component-based; composite names joined with '・' get ' & ')
_namemap = {}
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'names_map.json')
if os.path.exists(_p):
    _namemap = json.load(open(_p, encoding='utf-8'))

def tr_name(n):
    if not n or not _namemap:
        return n
    if n in _namemap:
        return _namemap[n]
    parts = n.split('・')
    if all(p in _namemap for p in parts):
        return ' & '.join(_namemap[p] for p in parts)
    return n

extract, vislice, out = sys.argv[1], sys.argv[2], sys.argv[3]
data = json.load(open(extract, encoding='utf-8'))
virecs = json.load(open(vislice, encoding='utf-8'))
vmap_d = {r['i']: r for r in virecs if r.get('kind', 'd') == 'd' and r.get('vi')}
vmap_s = {(r['si'], r['sel']): r['vi'] for r in virecs if r.get('kind') == 's' and r.get('vi')}
TAG_RE = re.compile(r'^(?:%[a-zA-Z]+;?)+')

idx = applied = mismatch = 0
for si, scene in enumerate(data.get('scenes', [])):
    for ti, text in enumerate(scene.get('texts', [])):
        if text.get('name'):
            text['name'] = tr_name(text['name'])
        for di, dial in enumerate(text.get('dialogues', [])):
            if dial.get('display_name'):
                dial['display_name'] = tr_name(dial['display_name'])
            r = vmap_d.get(idx)
            vals = dial.get('values', [])
            if r and len(vals) >= 2:
                if 'si' in r and (r['si'], r['ti'], r['di']) != (si, ti, di):
                    mismatch += 1
                else:
                    vi = r['vi']
                    v0 = vals[0] if isinstance(vals[0], str) else ''
                    if len(vals) == 2:
                        # v0-only line: [text, int]
                        m = TAG_RE.match(v0) if isinstance(v0, str) else None
                        tag = m.group(0) if m else ''
                        vals[0] = tag + vi
                    elif len(vals) >= 4:
                        v2 = vals[2] if isinstance(vals[2], str) else ''
                        v2_strip = v2.strip() if isinstance(v2, str) else ''
                        if v2_strip:
                            if isinstance(v0, str) and v0:
                                if v2 and v2 in v0:
                                    vals[0] = v0.replace(v2, vi)
                                else:
                                    m = TAG_RE.match(v0)
                                    vals[0] = (m.group(0) if m else '') + vi
                            vals[2] = vi
                            if len(vals) > 3:
                                vals[3] = vi
                        else:
                            if isinstance(v0, str) and v0:
                                m = TAG_RE.match(v0)
                                tag = m.group(0) if m else ''
                                vals[0] = tag + vi
                    else:
                        m = TAG_RE.match(v0) if isinstance(v0, str) else None
                        tag = m.group(0) if m else ''
                        vals[0] = tag + vi
                    applied += 1
            idx += 1

sel_applied = 0
for (si, sel), vi in vmap_s.items():
    try:
        data['scenes'][si]['selects'][sel] = vi
        sel_applied += 1
    except Exception:
        pass

json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'dialogues_applied={applied} index_mismatch={mismatch} selects_applied={sel_applied} -> {out}')

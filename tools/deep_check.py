# -*- coding: utf-8 -*-
import sys, os, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
B = sys.argv[1]
W = os.path.join(B, 'work')
skip = json.load(open(os.path.join(B, 'chua_dich.json'), encoding='utf-8'))
nm = json.load(open(os.path.join(B, 'names_map.json'), encoding='utf-8'))

def skset(base):
    raw = skip.get(base, [])
    if isinstance(raw, dict):
        return set(raw.get('d', []))
    return set(raw)

# JP thuc su (loai ー U+30FC va pai-wan used as stretch)
jp_real = re.compile(r'[\u3040-\u309f\u3040-\u309f\u30a0-\u30fa\u30a2-\u30fa\u4e00-\u9fff\uff01-\uff5e]')
# nhung 只 loai ー : dung tap ky tu JP khong bao gom U+30FC
jp2 = re.compile(r'[\u3040-\u309f\u30a1-\u30fa\u4e00-\u9fff\uff01-\uff5e\uff0b]')

jp = re.compile(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]')
unexpected_real = []
unexpected_stretch = 0
jpnames = {}
for fn in sorted(os.listdir(W)):
    if not fn.endswith('.patched.json'):
        continue
    base = fn[:-len('.patched.json')]
    sk = skset(base)
    d = json.load(open(os.path.join(W, fn), encoding='utf-8'))
    idx = 0
    for si, s in enumerate(d.get('scenes', [])):
        for t in s.get('texts', []):
            if t.get('name') and jp2.search(t['name']):
                jpnames.setdefault(t['name'], 0)
                jpnames[t['name']] += 1
            for dl in t.get('dialogues', []):
                if dl.get('display_name') and jp2.search(dl['display_name']):
                    jpnames.setdefault('DN:' + dl['display_name'], 0)
                    jpnames['DN:' + dl['display_name']] += 1
                v = dl.get('values', [])
                v0 = v[0] if len(v) > 0 and isinstance(v[0], str) else ''
                if v0.strip() and jp2.search(v0) and idx not in sk:
                    unexpected_real.append((base[:30], idx, v0[:70]))
                elif v0.strip() and ('ー' in v0) and jp.search(v0) and idx not in sk and not jp2.search(v0):
                    unexpected_stretch += 1
                idx += 1

print('JP that su sot (ngoai skip):', len(unexpected_real))
for b in unexpected_real[:40]:
    print('   ', b)
print('--- chi chua ー (false positive):', unexpected_stretch)
print('--- JP name-fields con sot:', len(jpnames))
for k, c in sorted(jpnames.items(), key=lambda x: -x[1]):
    print('   ', repr(k), c)

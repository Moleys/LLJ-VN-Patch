# -*- coding: utf-8 -*-
import sys, json, os, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
base = sys.argv[1]
u = os.path.join(base, 'ui_work')
src = os.path.join(u, 'uitexts_jp.toml')
vi = os.path.join(u, 'uitexts.slice.vi.json')
outp = os.path.join(u, 'uitexts_en_merged.toml')

def sanitize(v):
    v = v.replace('\\', '\\\\')      # escape backslashes
    v = v.replace('"', '\\"')        # escape quotes
    v = re.sub(r'\s*\r?\n\s*', ' ', v)  # newlines -> space
    v = re.sub(r'\s{2,}', ' ', v).strip()
    return v

recs = json.load(open(vi, encoding='utf-8'))
m = {}
for r in recs:
    if r.get('vi') and r['vi'].strip():
        m[r['key']] = sanitize(r['vi'])

t = open(src, encoding='utf-8-sig').read()
lines = t.splitlines()
outl = []
count = 0
in_texts = False
import re as _re
for ln in lines:
    s = ln.strip()
    if s == '[texts]':
        in_texts = True; outl.append(ln); continue
    if in_texts and s.startswith('[') and s.endswith(']') and '=' not in s:
        in_texts = False
    mm = _re.match(r'^(\s*)([A-Za-z_0-9]+)(\s*=\s*)"(.*)"(\s*)$', ln) if in_texts else None
    if mm and mm.group(2) in m:
        outl.append(f"{mm.group(1)}{mm.group(2)}{mm.group(3)}\"{m[mm.group(2)]}\"{mm.group(5)}")
        count += 1
        continue
    outl.append(ln)
new = '\n'.join(outl)
raw = new.encode('utf-8')
if raw[:3] == b'\xef\xbb\xbf':
    raw = raw[3:]
open(outp, 'wb').write(raw)
print('replaced', count)

# validate
import tomllib
try:
    d = tomllib.loads(raw.decode('utf-8'))
    print('TOML OK. top keys:', list(d.keys()))
except Exception as e:
    print('TOML STILL BROKEN:', e)

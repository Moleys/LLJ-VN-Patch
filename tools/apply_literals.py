# -*- coding: utf-8 -*-
import sys, json, os, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
base = sys.argv[1]
u = os.path.join(base, 'ui_work')
target = os.path.join(u, 'uitexts_en_merged.toml')

jp = re.compile(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]')

# build jp->en map
m = {}
# from [texts] slice (jp->vi)
for r in json.load(open(os.path.join(u, 'uitexts.slice.vi.json'), encoding='utf-8')):
    if r.get('vi') and r.get('jp'):
        m[r['jp']] = r['vi']
# from rest batches (jp->en)
for i in range(3):
    for r in json.load(open(os.path.join(u, f'uitexts.rest.slice_b{i}.vi.json'), encoding='utf-8')):
        if r.get('en'):
            m[r['jp']] = r['en']
print('map size', len(m))

def esc_en(v):
    v = v.replace('\\', '\\\\')
    v = v.replace('"', '\\"')
    v = re.sub(r'\s*\r?\n\s*', ' ', v)
    v = re.sub(r'\s{2,}', ' ', v)
    return v.strip()

t = open(target, encoding='utf-8').read()

# match single or double quoted literals containing JP
pat = re.compile(r'"((?:[^"\\]|\\.)*)"|\'([^\']*)\'')
count = 0
nomap = []

def repl(mm):
    global count
    if mm.group(1) is not None:
        content = mm.group(1).replace('\\"', '"').replace('\\\\', '\\').replace('\\n', '\n').replace('\\t', '\t')
    else:
        content = mm.group(2)
    if not jp.search(content):
        return mm.group(0)
    en = m.get(content)
    if en is None:
        # try normalized (strip spaces)
        en = m.get(content.strip())
    if en is None:
        if content not in nomap:
            nomap.append(content)
        return mm.group(0)
    count += 1
    return '"' + esc_en(en) + '"'

t2 = pat.sub(repl, t)
open(target, 'w', encoding='utf-8', newline='\n').write(t2)
print('replaced occurrences:', count, 'unmapped JP strings:', len(nomap))
for s in nomap[:30]:
    print('  NOMAP', repr(s[:70]))

import tomllib
try:
    tomllib.loads(t2)
    print('TOML OK')
except Exception as e:
    print('TOML BROKEN:', e)

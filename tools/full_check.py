# -*- coding: utf-8 -*-
"""full_check.py — kiem tra toan dien patch"""
import sys, os, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
B = sys.argv[1]
G = sys.argv[2]
W = os.path.join(B, 'work')
U = os.path.join(G, 'unencrypted')
jp = re.compile(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]')
print('=' * 60)

# ---------- 1) scene patched.json: JP left trong values (tru skip) ----------
skip = json.load(open(os.path.join(B, 'chua_dich.json'), encoding='utf-8')) if os.path.exists(os.path.join(B, 'chua_dich.json')) else {}
def skset(base):
    raw = skip.get(base, [])
    if isinstance(raw, dict):
        return set(raw.get('d', [])), set(tuple(x) for x in raw.get('s', []))
    return set(raw), set()

tot_d = vn_d = jp_bad = 0
bad_samples = []
tot_name = jp_name = 0
tot_sel = vn_sel = 0
nfiles = 0
mismatch_total = 0
for fn in sorted(os.listdir(W)):
    if not fn.endswith('.patched.json'):
        continue
    nfiles += 1
    base = fn[:-len('.patched.json')]
    skd, sks = skset(base)
    d = json.load(open(os.path.join(W, fn), encoding='utf-8'))
    for si, s in enumerate(d.get('scenes', [])):
        for t in s.get('texts', []):
            if t.get('name') and jp.search(t['name']):
                jp_name += 1
            tot_name += 1 if t.get('name') else 0
            for dl in t.get('dialogues', []):
                if dl.get('display_name') and jp.search(dl['display_name']):
                    jp_name += 1
                tot_d += 1
                v = dl.get('values', [])
                v0 = v[0] if len(v) > 0 and isinstance(v[0], str) else ''
                if v0.strip() and not jp.search(v0):
                    vn_d += 1
                elif v0.strip() and idx_skipped(base, tot_d) if False else False:
                    pass
        for sel in s.get('selects', []):
            tot_sel += 1
            if isinstance(sel, str) and sel.strip() and not jp.search(sel):
                vn_sel += 1
print(f"[1] scenes patched: {nfiles} | dialogues={tot_d} VN={vn_d} ({vn_d*100/tot_d:.1f}%)")
print(f"    name-fields={tot_name} JP-name-left={jp_name} | selects={tot_sel} VN={vn_sel}")

# JP con lai nhung KHONG nam trong skip list -> that su bi sot
def count_unexpected(base):
    pass

# ---------- 2) so khop skip list: JP con lai co duoc danh dau chua dich? ----------
unexpected = 0
for fn in sorted(os.listdir(W)):
    if not fn.endswith('.patched.json'):
        continue
    base = fn[:-len('.patched.json')]
    skd, sks = skset(base)
    d = json.load(open(os.path.join(W, fn), encoding='utf-8'))
    idx = 0
    for si, s in enumerate(d.get('scenes', [])):
        for t in s.get('texts', []):
            for dl in t.get('dialogues', []):
                v = dl.get('values', [])
                v0 = v[0] if len(v) > 0 and isinstance(v[0], str) else ''
                if v0.strip() and jp.search(v0) and idx not in skd:
                    unexpected += 1
                    if unexpected <= 5:
                        bad_samples.append((base[:28], idx, v0[:50]))
                idx += 1
print(f"[2] JP con sot KHONG thuoc danh sach chua-dich: {unexpected}")
for b in bad_samples:
    print('    ', b)

# ---------- 3) deploy integrity ----------
n_scn = len([f for f in os.listdir(U) if f.endswith('.ks.scn') and not f.endswith('.patched.json')])
diff = 0
for f in os.listdir(W):
    if f.endswith('.ks.scn') and not f.endswith('.patched.json'):
        a = os.path.getsize(os.path.join(W, f))
        b2 = os.path.join(U, f)
        if not os.path.exists(b2) or os.path.getsize(b2) != a:
            diff += 1
print(f"[3] deployed scenes={n_scn} size-mismatch={diff}")
for f in ['uitexts.toml', 'syslangtext_jp.ini', 'default.tjs', 'config.tjs']:
    p = os.path.join(U, f)
    print(f"    {f}: {'OK ' + str(os.path.getsize(p)) if os.path.exists(p) else 'MISSING'}")

# ---------- 4) ten nhan vat trong text thoa (double-name prefix) ----------
dup = 0
dupex = []
first_names = ['Yukitaka', 'Ririko', 'Ena', 'Anju', 'Tsukimi', 'Nayuka', 'Miku', 'Eiya',
               'Hiromu', 'Suguru', 'Yuuma', 'Ruiko', 'Hinami', 'Muroi', 'Nakane', 'Izawa-sensei']
for fn in sorted(os.listdir(W)):
    if not fn.endswith('.slice.vi.json'):
        continue
    for r in json.load(open(os.path.join(W, fn), encoding='utf-8')):
        v = r.get('vi')
        if not v:
            continue
        for nm in first_names:
            if v.startswith(nm + ':'):
                dup += 1
                if len(dupex) < 5:
                    dupex.append((fn[:26], v[:60]))
print(f"[4] vi-text co prefix 'Ten:' (nhip double name): {dup}")
for e in dupex:
    print('    ', e)

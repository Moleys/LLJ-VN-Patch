# -*- coding: utf-8 -*-
"""bulk_merge_patch.py — merge vi -> patched.json -> PSB -> deploy check"""
import os, sys, subprocess, shutil, pathlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
B = sys.argv[1]
G = sys.argv[2] if len(sys.argv) > 2 else None
W = os.path.join(B, 'work')
T = os.path.join(B, 'text_extract')
S = os.path.join(B, 'scn_named')
P = os.path.join(B, 'scn_tool', 'scn-script-patch.exe')
merged = patched = 0
for fn in sorted(os.listdir(W)):
    if not fn.endswith('.slice.vi.json'):
        continue
    base = fn[:-len('.slice.vi.json')]
    ex = os.path.join(T, base + '.json')
    pa = os.path.join(W, base + '.patched.json')
    if os.path.exists(pa):
        continue  # already done
    if not os.path.exists(ex):
        print(f"MISSING extract {base}")
        continue
    r = subprocess.run([sys.executable, os.path.join(B, 'merge_any.py'), ex, os.path.join(W, fn), pa],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    print(r.stdout.strip())
    if r.stderr.strip():
        print("ERR " + r.stderr.strip()[:300])
    merged += 1
for fn in sorted(os.listdir(W)):
    if not fn.endswith('.patched.json'):
        continue
    base = fn[:-len('.patched.json')]
    pj = os.path.join(W, fn)
    psb = os.path.join(S, base + '.psb')
    out = os.path.join(W, base)
    if os.path.exists(out):
        continue
    if not os.path.exists(psb):
        print(f"MISSING psb {base}")
        continue
    r = subprocess.run([P, pj, psb, out], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.stdout.strip():
        print("OUT " + r.stdout.strip()[:300])
    if r.stderr.strip():
        print("ERR " + r.stderr.strip()[:300])
    if os.path.exists(out):
        patched += 1
        print(f"PATCHED {base} {os.path.getsize(out)}")
    else:
        print(f"FAIL patch {base}")
print(f"merged_new={merged} patched_new={patched}")
if G:
    U = os.path.join(G, 'unencrypted')
    n = 0
    for fn in sorted(os.listdir(W)):
        if not fn.endswith('.ks.scn'):
            continue
        if fn.endswith('.patched.json'):
            continue
        shutil.copyfile(os.path.join(W, fn), os.path.join(U, fn))
        n += 1
    print(f"deployed_total_in_work={n}")

# -*- coding: utf-8 -*-
"""verify batch: check patched JSON for leftover JP, write TIENDO.md"""
import os, json, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
B = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Mol\Downloads\[250926] [ゆずソフト] ライムライト・レモネードジャム 通常版 + Voice Tokuten(1)\_translation_work"
W = os.path.join(B, 'work')
T = os.path.join(B, 'text_extract')
jp = re.compile(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]')
rows = []
done_vi = 0
for fn in sorted(os.listdir(W)):
    if not fn.endswith('.patched.json'):
        continue
    base = fn[:-len('.patched.json')]
    d = json.load(open(os.path.join(W, fn), encoding='utf-8'))
    n = 0
    left = 0
    ex = ''
    for s in d.get('scenes', []):
        for t in s.get('texts', []):
            for dl in t.get('dialogues', []):
                v = dl.get('values', [])
                if len(v) > 2 and isinstance(v[2], str) and v[2].strip():
                    n += 1
                    if jp.search(v[2]):
                        left += 1
                        if not ex:
                            ex = v[2][:60]
    rows.append((base, n, left, ex))
    done_vi += n
print(f"patched_files={len(rows)} patched_sentences={done_vi}")
for base, n, left, ex in rows:
    print(f"{base[:30]} n={n} left_jp={left} {ex[:30]}")
# overall slice progress
total_slice = 0
done_slice = 0
for fn in os.listdir(W):
    if fn.endswith('.slice.json'):
        total_slice += len(json.load(open(os.path.join(W, fn), encoding='utf-8')))
    if fn.endswith('.slice.vi.json'):
        done_slice += len(json.load(open(os.path.join(W, fn), encoding='utf-8')))
print(f"SLICE total={total_slice} translated={done_slice} pct={done_slice*100/max(1,total_slice):.1f}%")

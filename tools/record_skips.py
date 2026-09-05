# -*- coding: utf-8 -*-
"""record_skips.py — UNION cac i trong todo.json chua co vi vao chua_dich.json"""
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
B=sys.argv[1]
W=os.path.join(B,'work')
skip_path=os.path.join(B,'chua_dich.json')
skip=json.load(open(skip_path,encoding='utf-8')) if os.path.exists(skip_path) else {}
targets=sys.argv[2:]  # base names; neu rong: quet tat ca todo.json
if not targets:
    targets=[f[:-len('.todo.json')] for f in os.listdir(W) if f.endswith('.todo.json')]
for base in targets:
    todo=os.path.join(W,base+'.todo.json')
    vi=os.path.join(W,base+'.slice.vi.json')
    if not os.path.exists(todo):
        continue
    items=json.load(open(todo,encoding='utf-8'))
    done=set()
    if os.path.exists(vi):
        for r in json.load(open(vi,encoding='utf-8')):
            if r.get('vi'):
                if r.get('kind','d')=='d': done.add(r['i'])
                else: done.add(('s',r['si'],r['sel']))
    new=[it['i'] for it in items if it.get('kind','d')=='d' and it['i'] not in done]
    old=set(skip.get(base,[]))
    skip[base]=sorted(old.union(new))
    print(base,'skip_total',len(skip[base]),'new',len(new))
json.dump(skip,open(skip_path,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('wrote',skip_path)

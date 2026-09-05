# -*- coding: utf-8 -*-
"""gen_todo2.py — tao todo, bo qua cac dong chua dich da danh dau"""
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
B=sys.argv[1]
W=os.path.join(B,'work')
skip_path=os.path.join(B,'chua_dich.json')
skip={}
if os.path.exists(skip_path):
    skip=json.load(open(skip_path,encoding='utf-8'))
# skip: {base: [i,...]} dialogue; {base: {"d":[...], "s":[[si,sel],..]}} ca selects
todos=[]
skipped_total=0
for fn in sorted(os.listdir(W)):
    if not fn.endswith('.slice.json'): continue
    base=fn[:-len('.slice.json')]
    vi_fn=base+'.slice.vi.json'
    items=json.load(open(os.path.join(W,fn),encoding='utf-8'))
    done=set()
    if os.path.exists(os.path.join(W,vi_fn)):
        try:
            for r in json.load(open(os.path.join(W,vi_fn),encoding='utf-8')):
                if r.get('vi'):
                    if r.get('kind','d')=='d': done.add(r['i'])
                    else: done.add(('s',r['si'],r['sel']))
        except: pass
    raw = skip.get(base, [])
    if isinstance(raw, dict):
        sk = set(raw.get('d', []))
        sk_s = set(tuple(x) for x in raw.get('s', []))
    else:
        sk = set(raw)
        sk_s = set()
    miss=[]
    for it in items:
        if it.get('kind','d') == 's':
            k=('s',it['si'],it['sel'])
            if k in done or (it['si'],it['sel']) in sk_s:
                continue
            miss.append(it)
            continue
        k=it['i']
        if k in done or it['i'] in sk:
            if it['i'] in sk and k not in done:
                skipped_total+=1
            continue
        miss.append(it)
    if miss:
        # xoa todo cu neu co de tranh stale
        out=base+'.todo.json'
        json.dump(miss,open(os.path.join(W,out),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
        todos.append((len(miss),base))
    else:
        # khong con miss -> xoa todo cu neu ton tai
        out=os.path.join(W,base+'.todo.json')
        if os.path.exists(out):
            os.remove(out)
print('files_with_todo',len(todos),'total_missing',sum(n for n,_ in todos),'marked_chua_dich',skipped_total)
for n,b in sorted(todos)[:20]:
    print(n,b[:50])

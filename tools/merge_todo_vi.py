# -*- coding: utf-8 -*-
"""merge_todo_vi.py — gop todo.vi.json vao slice.vi.json (append, khong trung i)"""
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
B=sys.argv[1]
W=os.path.join(B,'work')
merged=0
for fn in sorted(os.listdir(W)):
    if not fn.endswith('.todo.vi.json'): continue
    base=fn[:-len('.todo.vi.json')]
    vi_path=os.path.join(W,base+'.slice.vi.json')
    todo_vi=json.load(open(os.path.join(W,fn),encoding='utf-8'))
    if os.path.exists(vi_path):
        cur=json.load(open(vi_path,encoding='utf-8'))
    else:
        cur=[]
    have=set()
    for r in cur:
        if r.get('kind','d')=='d': have.add(r['i'])
        else: have.add(('s',r['si'],r['sel']))
    added=0
    for r in todo_vi:
        if not r.get('vi'): continue
        k=r['i'] if r.get('kind','d')=='d' else ('s',r['si'],r['sel'])
        if k not in have:
            cur.append(r); have.add(k); added+=1
    # sort by i for d, keep s at end
    cur_d=sorted([r for r in cur if r.get('kind','d')=='d'],key=lambda x:x['i'])
    cur_s=[r for r in cur if r.get('kind')=='s']
    cur=cur_d+cur_s
    json.dump(cur,open(vi_path,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    # remove todo files to avoid re-merge? keep todo.json, remove todo.vi.json
    os.remove(os.path.join(W,fn))
    merged+=1
    print(f"{base[:30]} +{added}")
print(f"merged_todo_files={merged}")

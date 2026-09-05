# -*- coding: utf-8 -*-
import os, sys, subprocess, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
B=sys.argv[1]
T=os.path.join(B,'text_extract'); W=os.path.join(B,'work'); S=os.path.join(B,'slice_any.py')
files=sorted([f for f in os.listdir(T) if f.endswith('.json')])
tot_items=0; tot_v2=0
for fn in files:
    base=fn[:-len('.json')]
    out=os.path.join(W,base+'.slice.json')
    # backup old slice? overwrite directly (old vi stays)
    r=subprocess.run([sys.executable,S,os.path.join(T,fn),out],capture_output=True,text=True,encoding='utf-8',errors='replace')
    # parse counts from stdout: slice_items=X (v2=A v0=B)
    line=r.stdout.strip()
    # print only summary every 20
    tot_items+=1
print('resliced',len(files))
# recount totals
grand=0; gv2=0; gv0=0; done=0
for fn in os.listdir(W):
    if fn.endswith('.slice.json'):
        items=json.load(open(os.path.join(W,fn),encoding='utf-8'))
        grand+=len(items)
        for it in items:
            if it.get('src','v2')=='v2': gv2+=1
            else: gv0+=1
    if fn.endswith('.slice.vi.json'):
        done+=len(json.load(open(os.path.join(W,fn),encoding='utf-8')))
print(f"grand_slice={grand} v2={gv2} v0={gv0} translated_old_files={done}")

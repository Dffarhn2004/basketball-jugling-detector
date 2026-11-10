"""Phase 4 candidate fix: distance-based association of RAW E2 detections (no ByteTrack IoU) + bounce = down->up reversal near floor.
Parameters are tuned on DEV (0-30 s) only; HOLDOUT (30-60 s) is evaluated once with the chosen parameters.
GT v2, E2 baseline and E3 outputs are read-only. No model training."""
from pathlib import Path
import csv, json, itertools, sys
from collections import defaultdict
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'artifacts/runs/Phase4_bridging'; OUT.mkdir(parents=True,exist_ok=True)
FPS=30.0; H=720.0; SPLIT_S=30.0
def read(p):
    with Path(p).open(newline='',encoding='utf8') as f: return list(csv.DictReader(f))
def detect_raw():
    cache=OUT/'raw_0_60s.csv'
    if cache.exists(): return
    import cv2; from ultralytics import YOLO
    model=YOLO(str(ROOT/'artifacts/runs/E2_finetuned_cpu/weights/best.pt')); cap=cv2.VideoCapture(str(ROOT/'videofull.mp4')); rows=[]
    for fi in range(1800):
        ok,img=cap.read()
        if not ok: break
        r=model.predict(img,conf=0.25,imgsz=640,classes=[0],verbose=False)[0]
        for b,s in zip(r.boxes.xyxy.tolist(),r.boxes.conf.tolist()): rows.append({'frame_idx':fi,'x1':b[0],'y1':b[1],'x2':b[2],'y2':b[3],'confidence':s})
    with cache.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['frame_idx','x1','y1','x2','y2','confidence']); w.writeheader(); w.writerows(rows)
def load_raw():
    d=defaultdict(list)
    for r in read(OUT/'raw_0_60s.csv'):
        x1,y1,x2,y2=(float(r[k]) for k in ('x1','y1','x2','y2')); d[int(r['frame_idx'])].append((( x1+x2)/2,(y1+y2)/2,y2,max(x2-x1,y2-y1),float(r['confidence'])))
    return d
def track(raw,gate=2.2,max_miss=6,min_conf=.3,n=1800):
    tracks=[]; active=[]   # track: dict(id,pts=[(f,cx,cy,by)],vx,vy,last,size)
    nid=0
    for f in range(n):
        dets=[d for d in raw.get(f,[]) if d[4]>=min_conf]; used=set(); cand=[]
        for ti,t in enumerate(active):
            gap=f-t['last']; px=t['cx']+t['vx']*gap; py=t['cy']+t['vy']*gap
            for di,d in enumerate(dets):
                dist=np.hypot(d[0]-px,d[1]-py)
                if dist<=gate*max(t['size'],d[3])*(1+.25*(gap-1)): cand.append((dist,ti,di))
        usedt=set()
        for dist,ti,di in sorted(cand):
            if ti in usedt or di in used: continue
            usedt.add(ti); used.add(di); t=active[ti]; d=dets[di]; gap=f-t['last']
            t['vx']=(d[0]-t['cx'])/gap; t['vy']=(d[1]-t['cy'])/gap; t['cx'],t['cy'],t['last'],t['size']=d[0],d[1],f,d[3]; t['pts'].append((f,d[0],d[1],d[2]))
        for di,d in enumerate(dets):
            if di in used: continue
            t={'id':nid,'pts':[(f,d[0],d[1],d[2])],'cx':d[0],'cy':d[1],'vx':0.,'vy':0.,'last':f,'size':d[3]}; nid+=1; active.append(t); tracks.append(t)
        active=[t for t in active if f-t['last']<=max_miss]
    return tracks
def events(tracks,floor=.72,min_drop=25,min_rise=25,win=5,dedup=.2):
    ev=[]
    for t in tracks:
        p=t['pts']
        if len(p)<5: continue
        fr=np.array([a[0] for a in p]); cy=np.array([a[2] for a in p]); by=np.array([a[3] for a in p])
        for i in range(1,len(p)-1):
            a=int(np.searchsorted(fr,fr[i]-win,side='left')); b=int(np.searchsorted(fr,fr[i]+win,side='right'))
            if a>=i or b<=i+1: continue
            if by[i]<floor*H: continue
            drop=cy[i]-cy[a:i].min(); rise=cy[i]-cy[i+1:b].min()
            if drop<min_drop or rise<min_drop: continue
            if cy[i]<cy[a:b].max(): continue      # local max of y (lowest point)
            ev.append({'frame_idx':int(fr[i]),'time_s':fr[i]/FPS,'track_id':t['id'],'bottom_y':float(by[i])})
    ev.sort(key=lambda e:e['time_s']); out=[]
    for e in ev:
        if out and e['frame_idx']-out[-1]['frame_idx']<=round(dedup*30): 
            if e['bottom_y']>out[-1]['bottom_y']: out[-1]=e
            continue
        out.append(e)
    return out
def score(pred_t,gt_t,tol=.1):
    used=set(); tp=0
    for t in sorted(pred_t):
        c=[(abs(t-g),i) for i,g in enumerate(gt_t) if i not in used and abs(t-g)<=tol]
        if c: used.add(min(c)[1]); tp+=1
    fp=len(pred_t)-tp; fn=len(gt_t)-tp; p=tp/(tp+fp) if tp+fp else 0; r=tp/len(gt_t) if gt_t else 0
    return {'pred':len(pred_t),'gt':len(gt_t),'tp':tp,'fp':fp,'fn':fn,'precision':round(p,3),'recall':round(r,3),'f1':round(2*p*r/(p+r),3) if p+r else 0}
def split(ts,lo,hi): return [t for t in ts if lo<=t<hi]
def main():
    detect_raw(); raw=load_raw()
    gt=[float(r['time_s']) for r in read(ROOT/'data/annotations/bounce_events_gt_v2.csv') if r['review_status']=='approved']
    base=[float(r['time_s']) for r in read(ROOT/'artifacts/runs/Phase4_pilot_60s/bounce_events_pred.csv')]
    e3=[float(r['time_s']) for r in read(ROOT/'artifacts/runs/Phase4_motion_first/E3_B_adaptive.csv')]
    grid=dict(gate=[1.5,2.2,3.0],floor=[.65,.72,.78],min_drop=[15,25,40],max_miss=[4,8])
    res=[]
    for gate,floor,md,mm in itertools.product(grid['gate'],grid['floor'],grid['min_drop'],grid['max_miss']):
        ev=events(track(raw,gate=gate,max_miss=mm),floor=floor,min_drop=md,min_rise=md)
        s=score(split([e['time_s'] for e in ev],0,SPLIT_S),split(gt,0,SPLIT_S)); res.append(({'gate':gate,'floor':floor,'min_drop':md,'max_miss':mm},s))
    res.sort(key=lambda x:-x[1]['f1']); best=res[0][0]
    json.dump([{'params':a,'dev':b} for a,b in res],open(OUT/'dev_grid.json','w'),indent=1)
    ev=events(track(raw,gate=best['gate'],max_miss=best['max_miss']),floor=best['floor'],min_drop=best['min_drop'],min_rise=best['min_drop'])
    with (OUT/'bridging_events.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['frame_idx','time_s','track_id','bottom_y']); w.writeheader(); w.writerows(ev)
    pt=[e['time_s'] for e in ev]; report={'chosen_params_from_dev':best,'dev_0_30s':{},'holdout_30_60s':{}}
    for name,(lo,hi) in {'dev_0_30s':(0,SPLIT_S),'holdout_30_60s':(SPLIT_S,60.1)}.items():
        g=split(gt,lo,hi); report[name]={'bridging':score(split(pt,lo,hi),g),'E2_baseline':score(split(base,lo,hi),g),'E3B':score(split(e3,lo,hi),g)}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)); print(json.dumps(report,indent=2)); print('top5 dev',[ (a,b['f1']) for a,b in res[:5]])
if __name__=='__main__': main()

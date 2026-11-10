"""Run the FROZEN bridging method (params from dev 0-30 s: gate 1.5, floor .65, min_drop 15, max_miss 4) on frames 1800..end.
No tuning, no GT for this segment. Detection is resumable (appends to raw_1800_end.csv)."""
from pathlib import Path
import csv, json, sys, time
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'artifacts/runs/Phase4_bridging'
sys.path.insert(0,str(ROOT/'scripts')); import phase4_bridging as pb
CACHE=OUT/'raw_1800_end.csv'; DONE=OUT/'raw_1800_end.progress'; START=1800; END=36003; FIELDS=['frame_idx','x1','y1','x2','y2','confidence']
def detect():
    import cv2; from ultralytics import YOLO
    last=int(DONE.read_text()) if DONE.exists() else START-1
    if last>=END-1: return
    model=YOLO(str(ROOT/'artifacts/runs/E2_finetuned_cpu/weights/best.pt')); cap=cv2.VideoCapture(str(ROOT/'videofull.mp4')); cap.set(cv2.CAP_PROP_POS_FRAMES,last+1)
    new=not CACHE.exists(); f=CACHE.open('a',newline=''); w=csv.DictWriter(f,fieldnames=FIELDS)
    if new: w.writeheader()
    t0=time.time()
    for fi in range(last+1,END):
        ok,img=cap.read()
        if not ok: break
        r=model.predict(img,conf=0.25,imgsz=640,classes=[0],verbose=False)[0]
        for b,s in zip(r.boxes.xyxy.tolist(),r.boxes.conf.tolist()): w.writerow({'frame_idx':fi,'x1':b[0],'y1':b[1],'x2':b[2],'y2':b[3],'confidence':s})
        if fi%500==0: f.flush(); DONE.write_text(str(fi)); print(fi,round(time.time()-t0),'s',flush=True)
    f.flush(); DONE.write_text(str(fi)); f.close()
def run_events():
    raw=pb.load_raw()   # frames 0..1799
    d=pb.defaultdict(list)
    for r in pb.read(CACHE):
        x1,y1,x2,y2=(float(r[k]) for k in ('x1','y1','x2','y2')); d[int(r['frame_idx'])].append(((x1+x2)/2,(y1+y2)/2,y2,max(x2-x1,y2-y1),float(r['confidence'])))
    raw.update(d); n=max(raw)+1
    pb_range=pb.track.__globals__; 
    # track() loops over 1800 frames; generalise by temporary override
    import types
    src=pb.track
    def track_all(raw,gate=1.5,max_miss=4,min_conf=.3):
        tracks=[];active=[];nid=0
        for f in range(n):
            dets=[x for x in raw.get(f,[]) if x[4]>=min_conf]; used=set(); cand=[]
            for ti,t in enumerate(active):
                gap=f-t['last']; px=t['cx']+t['vx']*gap; py=t['cy']+t['vy']*gap
                for di,x in enumerate(dets):
                    dist=np.hypot(x[0]-px,x[1]-py)
                    if dist<=gate*max(t['size'],x[3])*(1+.25*(gap-1)): cand.append((dist,ti,di))
            usedt=set()
            for dist,ti,di in sorted(cand):
                if ti in usedt or di in used: continue
                usedt.add(ti); used.add(di); t=active[ti]; x=dets[di]; gap=f-t['last']
                t['vx']=(x[0]-t['cx'])/gap; t['vy']=(x[1]-t['cy'])/gap; t['cx'],t['cy'],t['last'],t['size']=x[0],x[1],f,x[3]; t['pts'].append((f,x[0],x[1],x[2]))
            for di,x in enumerate(dets):
                if di in used: continue
                t={'id':nid,'pts':[(f,x[0],x[1],x[2])],'cx':x[0],'cy':x[1],'vx':0.,'vy':0.,'last':f,'size':x[3]}; nid+=1; active.append(t); tracks.append(t)
            active=[t for t in active if f-t['last']<=max_miss]
        return tracks
    ev=pb.events(track_all(raw),floor=.65,min_drop=15,min_rise=15)
    with (OUT/'bridging_events_full.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['frame_idx','time_s','track_id','bottom_y']); w.writeheader(); w.writerows(ev)
    per_min=np.bincount([int(e['time_s']//60) for e in ev],minlength=20)
    rep={'frames':n,'events_total':len(ev),'events_0_60s':int(per_min[0]),'events_after_60s':len(ev)-int(per_min[0]),'events_per_minute':per_min.tolist(),
         'note':'No GT after 60 s: counts only, not accuracy. Frozen params from dev 0-30 s.'}
    (OUT/'full_video_report.json').write_text(json.dumps(rep,indent=1)); print(json.dumps(rep))
if __name__=='__main__':
    if '--events-only' not in sys.argv: detect()
    run_events()

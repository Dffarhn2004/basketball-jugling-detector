"""Run the FROZEN final model (E2 weights + distance association, params from dev 0-30 s of the training video) on a NEW video.
No tuning. Outputs raw detections, events, report."""
from pathlib import Path
import csv, json, sys, time
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'scripts')); import phase4_bridging as pb
VID=ROOT/(sys.argv[1] if len(sys.argv)>1 else 'videotesting.mp4'); OUT=ROOT/'artifacts/runs/Phase5_test_video'; OUT.mkdir(parents=True,exist_ok=True); RAW=OUT/'raw_detections.csv'
import cv2
cap=cv2.VideoCapture(str(VID)); N=int(cap.get(7)); FPS=cap.get(5); H=cap.get(4)
if not RAW.exists():
    from ultralytics import YOLO
    model=YOLO(str(ROOT/'artifacts/runs/E2_finetuned_cpu/weights/best.pt')); rows=[]; t0=time.time()
    for fi in range(N):
        ok,img=cap.read()
        if not ok: N=fi; break
        r=model.predict(img,conf=0.25,imgsz=640,classes=[0],verbose=False)[0]
        for b,s in zip(r.boxes.xyxy.tolist(),r.boxes.conf.tolist()): rows.append({'frame_idx':fi,'x1':b[0],'y1':b[1],'x2':b[2],'y2':b[3],'confidence':s})
        if fi%500==0: print(fi,round(time.time()-t0),flush=True)
    with RAW.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['frame_idx','x1','y1','x2','y2','confidence']); w.writeheader(); w.writerows(rows)
raw=pb.defaultdict(list)
for r in pb.read(RAW):
    x1,y1,x2,y2=(float(r[k]) for k in ('x1','y1','x2','y2')); raw[int(r['frame_idx'])].append(((x1+x2)/2,(y1+y2)/2,y2,max(x2-x1,y2-y1),float(r['confidence'])))
pb.H=H; pb.FPS=FPS
tracks=pb.track(raw,gate=1.5,max_miss=4,n=N); ev=pb.events(tracks,floor=.65,min_drop=15,min_rise=15)
with (OUT/'events.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['frame_idx','time_s','track_id','bottom_y']); w.writeheader(); w.writerows(ev)
fdet=sum(1 for f in range(N) if raw.get(f)); by=[e['bottom_y']/H for e in ev]
rep={'video':VID.name,'frames':N,'fps':FPS,'duration_s':round(N/FPS,1),'frames_with_detection':fdet,'detections':sum(len(v) for v in raw.values()),'tracks':len(tracks),'events':len(ev),'events_per_minute':round(len(ev)/(N/FPS/60),1),
     'event_bottom_y_over_H_min_median_max':[round(min(by),2),round(float(np.median(by)),2),round(max(by),2)] if by else None,'note':'Frozen params, no GT: counts only.'}
(OUT/'report.json').write_text(json.dumps(rep,indent=1)); print(json.dumps(rep))

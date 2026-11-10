from pathlib import Path
import csv, json, time
from collections import defaultdict, deque
import cv2
from ultralytics import YOLO
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/runs/Phase4_pilot_60s'; OUT.mkdir(parents=True,exist_ok=True)

def gt(path):
 rows=[]
 with path.open(newline='',encoding='utf8') as f:
  for r in csv.DictReader(f):
   if r['review_status']=='approved': rows.append(float(r['time_s']))
 return rows

def match(pred,truth,tol=.1):
 used=set(); tp=[]; fp=[]
 for t in sorted(pred):
  cand=[(abs(t-g),i,g) for i,g in enumerate(truth) if i not in used and abs(t-g)<=tol]
  if cand:
   _,i,g=min(cand);used.add(i);tp.append((t,g,t-g))
  else:fp.append(t)
 return tp,fp,[g for i,g in enumerate(truth) if i not in used]

def main():
 video=ROOT/'videofull.mp4'; model=YOLO(str(ROOT/'artifacts/runs/E2_finetuned_cpu/weights/best.pt'))
 cap=cv2.VideoCapture(str(video)); fps=cap.get(cv2.CAP_PROP_FPS) or 30; n=min(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),int(60*fps)); w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH));h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
 track=[]; events=[]; trails=defaultdict(lambda:deque(maxlen=12)); states={}; prev_bottom={}; candidate={}; start=time.perf_counter(); out=cv2.VideoWriter(str(OUT/'bounce_preview_60s.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),fps,(w,h))
 for fi in range(n):
  ok,img=cap.read()
  if not ok: break
  r=model.track(img,conf=.25,tracker=str(OUT/'bytetrack_phase4.yaml'),persist=True,classes=[0],imgsz=640,verbose=False)[0]
  ids=r.boxes.id.int().tolist() if r.boxes.id is not None else []
  boxes=r.boxes.xyxy.tolist(); scores=r.boxes.conf.tolist();
  for b,s,tid in zip(boxes,scores,ids):
   x1,y1,x2,y2=map(int,b); cx=(x1+x2)/2; bottom=y2; trails[tid].append((cx,bottom)); track.append({'frame_idx':fi,'time_s':fi/fps,'track_id':tid,'x1':x1,'y1':y1,'x2':x2,'y2':y2,'cx':cx,'cy':(y1+y2)/2,'bottom_y':bottom,'confidence':float(s)})
   prev=prev_bottom.get(tid); state=states.get(tid,'FALLING'); near=bottom>h*.75
   if prev is not None and near and bottom-prev>1: candidate[tid]=fi
   if prev is not None and candidate.get(tid) is not None and bottom-prev<-1 and fi-candidate[tid]>=1:
    t=candidate.pop(tid)/fps
    if not events or t-events[-1]['time_s']>.15 or events[-1]['track_id']!=tid: events.append({'event_id':f'P4-{len(events)+1:04d}','frame_idx':fi,'time_s':t,'track_id':tid,'state':'BOUNCE_CONFIRMED'})
   prev_bottom[tid]=bottom; states[tid]=state
   cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2);cv2.putText(img,f'ball {tid}',(x1,y1-5),0,.6,(0,255,0),2)
  for tid,pts in list(trails.items()):
   if len(pts)>1 and tid in ids: cv2.polylines(img,[__import__('numpy').array(list(pts)[-12:],dtype='int32')],False,(255,180,0),2)
  for ev in events:
   if ev['frame_idx']==fi:
    cv2.drawMarker(img,(int(ev.get('x',w//2)),int(ev.get('y',h*.8))),(0,0,255),cv2.MARKER_CROSS,30,3)
    cv2.putText(img,'BOUNCE +1',(int(ev.get('x',w//2))+12,int(ev.get('y',h*.8))-12),0,.8,(0,0,255),2)
  cv2.putText(img,f'Phase4 pilot  t={fi/fps:.2f}s  bounces={len(events)}',(20,30),0,.8,(0,0,255),2);out.write(img)
 cap.release();out.release(); elapsed=time.perf_counter()-start
 with (OUT/'tracking.csv').open('w',newline='') as f:
  wri=csv.DictWriter(f,fieldnames=track[0].keys());wri.writeheader();wri.writerows(track)
 with (OUT/'bounce_events_pred.csv').open('w',newline='') as f:
  wri=csv.DictWriter(f,fieldnames=events[0].keys() if events else ['event_id','frame_idx','time_s','track_id','state']);wri.writeheader();wri.writerows(events)
 truth=gt(ROOT/'data/annotations/bounce_events_gt.csv'); pred=[x['time_s'] for x in events];tp,fp,fn=match(pred,truth); summary={'frames_processed':n,'runtime_s':elapsed,'fps_video':fps,'tracking_rows':len(track),'predicted_bounces':len(pred),'approved_gt':len(truth),'tp':len(tp),'fp':len(fp),'fn':len(fn),'tolerance_s':.1,'note':'Diagnostic only: detector-derived trajectories and incomplete coordinate-free GT; no full audit of physical contact.'}
 (OUT/'summary.json').write_text(json.dumps(summary,indent=2));
 with (OUT/'event_errors.csv').open('w',newline='') as f:
  wri=csv.writer(f);wri.writerow(['type','pred_time_s','gt_time_s','error_s']);wri.writerows([['TP',a,b,e] for a,b,e in tp]+[['FP',a,'',''] for a in fp]+[['FN','',a,''] for a in fn])
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()

from pathlib import Path
import csv, json, statistics
from collections import Counter, defaultdict
import cv2
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'artifacts/runs/Phase4_visual_audit'; OUT.mkdir(parents=True,exist_ok=True)
TRACK=ROOT/'artifacts/runs/Phase4_pilot_60s/tracking.csv'; VIDEO=ROOT/'videofull.mp4'
def read(p):
 with p.open(newline='',encoding='utf8') as f:return list(csv.DictReader(f))
def match(pred,gt):
 used=set();tp=[];fp=[]
 for p in sorted(pred,key=lambda r:float(r['time_s'])):
  c=[(abs(float(p['time_s'])-float(g['time_s'])),i,g) for i,g in enumerate(gt) if i not in used and abs(float(p['time_s'])-float(g['time_s']))<=.1]
  if c:d,i,g=min(c);used.add(i);tp.append((p,g))
  else:fp.append(p)
 return tp,fp,[g for i,g in enumerate(gt) if i not in used]
track=read(TRACK); byframe=defaultdict(list)
for r in track:byframe[int(float(r['frame_idx']))].append(r)
pred=read(ROOT/'artifacts/runs/Phase4_pilot_60s/bounce_events_pred.csv'); e3=read(ROOT/'artifacts/runs/Phase4_motion_first/E3_B_adaptive.csv'); gt=[r for r in read(ROOT/'data/annotations/bounce_events_gt_v2.csv') if r['review_status']=='approved']
_,_,fn=match(pred,gt); _,fp3,_=match(e3,gt)
def select(rows,n=20):return rows if len(rows)<=n else [rows[round(i*(len(rows)-1)/(n-1))] for i in range(n)]
fn=select(fn);fp3=select(fp3)
worksheet=OUT/'visual_review_worksheet.csv'
with worksheet.open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=['case_id','kind','time_s','frame_idx','track_ids_nearby','detection_rows_nearby','human_category','notes']);w.writeheader()
 for i,r in enumerate(fn,1):
  t=float(r['time_s']); near=[x for x in track if abs(float(x['time_s'])-t)<=.5];w.writerow({'case_id':f'FN-{i:02d}','kind':'FN_E2','time_s':t,'frame_idx':r['frame_idx'],'track_ids_nearby':','.join(sorted({x['track_id'] for x in near})),'detection_rows_nearby':len(near),'human_category':'UNREVIEWED','notes':''})
 for i,r in enumerate(fp3,1):
  t=float(r['time_s']); near=[x for x in track if abs(float(x['time_s'])-t)<=.5];w.writerow({'case_id':f'FP-{i:02d}','kind':'FP_E3B','time_s':t,'frame_idx':r['frame_idx'],'track_ids_nearby':','.join(sorted({x['track_id'] for x in near})),'detection_rows_nearby':len(near),'human_category':'UNREVIEWED','notes':''})
# frames + short clips; only original boxes/tracks, no GT/prediction overlay claim
cap=cv2.VideoCapture(str(VIDEO)); fps=cap.get(cv2.CAP_PROP_FPS) or 30
for kind,rows in [('FN',fn),('FP',fp3)]:
 for i,r in enumerate(rows,1):
  t=float(r['time_s']); center=int(t*fps); cap.set(cv2.CAP_PROP_POS_FRAMES,max(0,center-int(.5*fps))); frames=[]
  for _ in range(int(fps*1.0)+1):
   ok,img=cap.read()
   if not ok:break
   fi=int(cap.get(cv2.CAP_PROP_POS_FRAMES))-1
   for b in byframe.get(fi,[]):
    x1,y1,x2,y2=map(int,[float(b['x1']),float(b['y1']),float(b['x2']),float(b['y2'])]);cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2);cv2.putText(img,f"id={b['track_id']} c={float(b['confidence']):.2f}",(x1,y1-5),0,.45,(0,255,0),1)
   cv2.putText(img,f'{kind}-{i:02d} t={fi/fps:.3f}s',(10,25),0,.7,(0,0,255),2);frames.append(img)
  if frames:
   h,w=frames[0].shape[:2]; out=cv2.VideoWriter(str(OUT/f'{kind}_{i:02d}.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),fps,(w,h))
   for im in frames:out.write(im)
   out.release()
# track audit
lengths=Counter(r['track_id'] for r in track); starts=Counter(int(float(r['time_s'])) for r in track)
(OUT/'tracking_audit.json').write_text(json.dumps({'rows':len(track),'unique_track_ids':len(lengths),'mean_track_length':statistics.mean(lengths.values()),'median_track_length':statistics.median(lengths.values()),'new_track_ids_per_second':len(lengths)/60,'frames_with_detections':len(byframe)},indent=2))
print(json.dumps({'fn_samples':len(fn),'fp_samples':len(fp3),'track_audit':{'unique_ids':len(lengths),'mean_length':statistics.mean(lengths.values()),'median_length':statistics.median(lengths.values())}},indent=2))

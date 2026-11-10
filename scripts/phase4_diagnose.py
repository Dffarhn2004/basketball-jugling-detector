"""Phase 4 diagnostic pass (no training, no parameter changes, GT/E2/E3 outputs read-only).
Runs E2 weights as plain detector (conf floor 0.05) on GT v2 frame +/-W, then joins with the
pilot tracking.csv and baseline FSM rules to explain each unmatched (FN) GT event."""
from pathlib import Path
import csv, json
from collections import defaultdict, Counter
import cv2
from ultralytics import YOLO
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/runs/Phase4_diagnostics'; OUT.mkdir(parents=True,exist_ok=True)
W=6; FLOOR=0.05
def read(p):
    with Path(p).open(newline='',encoding='utf8') as f: return list(csv.DictReader(f))
gt=[r for r in read(ROOT/'data/annotations/bounce_events_gt_v2.csv') if r['review_status']=='approved']
pred=read(ROOT/'artifacts/runs/Phase4_pilot_60s/bounce_events_pred.csv')
e3=read(ROOT/'artifacts/runs/Phase4_motion_first/E3_B_adaptive.csv')
trk=read(ROOT/'artifacts/runs/Phase4_pilot_60s/tracking.csv')
byf=defaultdict(list)
for r in trk: byf[int(r['frame_idx'])].append(r)
def match(preds,truth):
    used=set(); matched=set()
    for p in sorted(preds,key=lambda r:float(r['time_s'])):
        c=[(abs(float(p['time_s'])-float(g['time_s'])),i) for i,g in enumerate(truth) if i not in used and abs(float(p['time_s'])-float(g['time_s']))<=.1]
        if c: used.add(min(c)[1])
    return used
m2=match(pred,gt); m3=match(e3,gt)
# raw detections (cached)
cache=OUT/'raw_detections.csv'
frames=sorted({f for g in gt for f in range(int(g['frame_idx'])-W-4,int(g['frame_idx'])+W+5) if f>=0})
if not cache.exists():
    model=YOLO(str(ROOT/'artifacts/runs/E2_finetuned_cpu/weights/best.pt'))
    cap=cv2.VideoCapture(str(ROOT/'videofull.mp4')); rows=[]
    for fi in frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES,fi); ok,img=cap.read()
        if not ok: continue
        r=model.predict(img,conf=FLOOR,imgsz=640,classes=[0],verbose=False)[0]
        for b,s in zip(r.boxes.xyxy.tolist(),r.boxes.conf.tolist()):
            rows.append({'frame_idx':fi,'x1':b[0],'y1':b[1],'x2':b[2],'y2':b[3],'confidence':s})
    cap.release()
    with cache.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['frame_idx','x1','y1','x2','y2','confidence']); w.writeheader(); w.writerows(rows)
raw=defaultdict(list)
for r in read(cache): raw[int(r['frame_idx'])].append(r)
H=cv2.VideoCapture(str(ROOT/'videofull.mp4')).get(cv2.CAP_PROP_FRAME_HEIGHT)
def maxconf(fr,lo,hi):
    return max([float(d['confidence']) for f in range(lo,hi+1) for d in raw.get(f,[])],default=0.0)
out=[]
for i,g in enumerate(gt):
    f0=int(g['frame_idx']); lo,hi=f0-3,f0+3
    c_raw=maxconf(raw,lo,hi); c_wide=maxconf(raw,f0-W,f0+W)
    n_raw05=sum(1 for f in range(f0-W,f0+W+1) if raw.get(f))
    n_raw25=sum(1 for f in range(f0-W,f0+W+1) if any(float(d['confidence'])>=.25 for d in raw.get(f,[])))
    tr=[(f,r) for f in range(f0-10,f0+11) for r in byf.get(f,[])]
    ids=sorted({r['track_id'] for _,r in tr},key=int)
    tr_at=[r for f in range(lo,hi+1) for r in byf.get(f,[])]
    # frames in +/-W with any tracked box; longest gap
    have=[f for f in range(f0-W,f0+W+1) if byf.get(f)]
    gap=0;cur=0
    for f in range(f0-W,f0+W+1):
        cur=0 if byf.get(f) else cur+1; gap=max(gap,cur)
    # bottom_y behaviour of tracked ball(s) near GT
    bys=[float(r['bottom_y']) for _,r in tr]; maxb=max(bys,default=0)/H
    # down-then-up reversal on any track in +/-10
    rev=False
    for tid in ids:
        s=sorted([(f,float(r['bottom_y'])) for f,r in tr if r['track_id']==tid])
        d=[b[1]-a[1] for a,b in zip(s,s[1:])]
        if any(x>1 for x in d) and any(x<-1 for x in d) and max(range(len(d)),key=lambda k:d[k]) < len(d) and any(d[k]>1 and any(d[j]<-1 for j in range(k+1,len(d))) for k in range(len(d))): rev=True
    if i in m2: cause='TP_E2'
    elif c_raw<FLOOR: cause='detector_absent'
    elif c_raw<.25 and not tr_at: cause='low_confidence_only'
    elif not tr_at: cause='detected_but_untracked_at_gt'
    elif maxb<=.75: cause='fsm_floor_zone_reject(bottom_y<=0.75H)'
    elif not rev: cause='fsm_no_down_up_reversal_in_track'
    else: cause='fsm_other_or_timing_offset'
    out.append({'event_id':g['event_id'],'time_s':g['time_s'],'frame_idx':f0,'matched_E2':i in m2,'matched_E3B':i in m3,
      'raw_max_conf_gt+-3':round(c_raw,3),'raw_max_conf_gt+-6':round(c_wide,3),'raw_frames_conf>=.05_of_13':n_raw05,'raw_frames_conf>=.25_of_13':n_raw25,
      'tracked_box_at_gt+-3':bool(tr_at),'tracked_frames_of_13':len(have),'max_track_gap_frames':gap,'track_ids_gt+-10':'|'.join(ids),'n_track_ids':len(ids),
      'max_bottom_y_over_H':round(maxb,3),'down_then_up_in_track':rev,'diagnosed_cause':cause,'visual_label':'UNVERIFIED'})
with (OUT/'per_event_diagnostics.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
fn=[o for o in out if o['diagnosed_cause']!='TP_E2']
summ={'gt_events':len(out),'E2_tp':len(out)-len(fn),'E2_fn':len(fn),'cause_counts_among_fn':Counter(o['diagnosed_cause'] for o in fn),
 'multi_track_ids_gt+-10_among_fn':sum(o['n_track_ids']>1 for o in fn),'fn_with_gap>=2':sum(o['max_track_gap_frames']>=2 for o in fn),'frame_height':H,'window_frames':W,'conf_floor':FLOOR,
 'note':'Automatic diagnosis from detector/tracker/FSM traces; physical contact not verified; visual_label remains UNVERIFIED.'}
(OUT/'diagnostics_summary.json').write_text(json.dumps(summ,indent=2,default=dict)); print(json.dumps(summ,indent=2,default=dict))

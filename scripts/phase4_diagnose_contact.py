"""Per-ball diagnosis for annotated contact points (data/annotations/contact_points_sample.csv).
For each 'contact' case: is the contact ball detected (raw, conf>=.05 and >=.25) and tracked near (x,y) at marked frame +/-3,
which track ID, was that track continuous, and does its bottom_y show a down-then-up reversal around the contact?
Read-only on GT/E2/E3. Needs raw detections from scripts/phase4_diagnose.py (covers GT v2 frames +/-10 only)."""
from pathlib import Path
import csv, json
from collections import defaultdict, Counter
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'artifacts/runs/Phase4_diagnostics'
def read(p):
    with Path(p).open(newline='',encoding='utf8') as f: return list(csv.DictReader(f))
cp=[r for r in read(ROOT/'data/annotations/contact_points_sample.csv') if r['status']=='contact']
raw=defaultdict(list); trk=defaultdict(list)
for r in read(D/'raw_detections.csv'): raw[int(r['frame_idx'])].append(r)
for r in read(ROOT/'artifacts/runs/Phase4_pilot_60s/tracking.csv'): trk[int(r['frame_idx'])].append(r)
def inside(b,x,y,pad=25): return float(b['x1'])-pad<=x<=float(b['x2'])+pad and float(b['y1'])-pad<=y<=float(b['y2'])+pad
rows=[]
for c in cp:
    f0=int(c['marked_frame_idx']); x=float(c['x_contact_px']); y=float(c['y_contact_px'])
    rng=range(f0-3,f0+4)
    rawhit=[float(d['confidence']) for f in rng for d in raw.get(f,[]) if inside(d,x,y)]
    thit=[(f,r) for f in rng for r in trk.get(f,[]) if inside(r,x,y)]
    ids=Counter(r['track_id'] for _,r in thit); tid=ids.most_common(1)[0][0] if ids else ''
    rev=False; cont=''
    if tid:
        s=sorted((int(f),float(r['bottom_y'])) for f in range(f0-10,f0+11) for r in trk.get(f,[]) if r['track_id']==tid)
        fr=[a for a,_ in s]; cont=len(s)==(fr[-1]-fr[0]+1) if s else ''
        d=[b[1]-a[1] for a,b in zip(s,s[1:])]
        rev=any(d[k]>1 and any(d[j]<-1 for j in range(k+1,len(d))) for k in range(len(d)))
    if not rawhit: cause='contact_ball_not_detected(conf<.05)'
    elif max(rawhit)<.25: cause='contact_ball_low_conf_only'
    elif not thit: cause='detected_but_not_tracked'
    elif not rev: cause='tracked_no_down_up_reversal'
    else: cause='tracked_with_reversal(FSM/timing)'
    rows.append({'case_id':c['case_id'],'kind':c['kind'],'marked_frame':f0,'x':x,'y':y,'raw_max_conf_near_ball':round(max(rawhit),3) if rawhit else 0,
      'tracked_near_ball':bool(thit),'track_id':tid,'track_continuous_gt+-10':cont,'down_then_up':rev,'cause':cause})
if rows:
    with (D/'contact_diagnostics.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(json.dumps({'annotated_contact_cases':len(rows),'by_kind_cause':Counter(f"{r['kind']}:{r['cause']}" for r in rows)},indent=2,default=dict))

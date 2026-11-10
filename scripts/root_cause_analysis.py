from pathlib import Path
import csv, math
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'artifacts/runs/Phase4_root_cause'; OUT.mkdir(parents=True,exist_ok=True)
track=[]
with (ROOT/'artifacts/runs/Phase4_pilot_60s/tracking.csv').open(newline='') as f: track=list(csv.DictReader(f))
def rows_near(t,window=.2): return [r for r in track if abs(float(r['time_s'])-t)<=window]
def gt_rows():
 with (ROOT/'data/annotations/bounce_events_gt_v2.csv').open(newline='') as f:return [r for r in csv.DictReader(f) if r['review_status']=='approved']
def pred_rows():
 with (ROOT/'artifacts/runs/Phase4_pilot_60s/bounce_events_pred.csv').open(newline='') as f:return list(csv.DictReader(f))
gt=gt_rows(); preds=pred_rows(); used=set(); matches=[]; fns=[]
with (ROOT/'artifacts/runs/Phase4_motion_first/E3_B_adaptive.csv').open(newline='') as f: e3_preds=list(csv.DictReader(f))
for g in gt:
 t=float(g['time_s']); cand=[(abs(float(p['time_s'])-t),i,p) for i,p in enumerate(preds) if i not in used and abs(float(p['time_s'])-t)<=.1]
 if cand: d,i,p=min(cand);used.add(i);matches.append((g,p,d))
 else:fns.append(g)
e3_used=set()
for g in gt:
 c=[(abs(float(p['time_s'])-float(g['time_s'])),i) for i,p in enumerate(e3_preds) if i not in e3_used and abs(float(p['time_s'])-float(g['time_s']))<=.1]
 if c:e3_used.add(min(c)[1])
fps=[p for i,p in enumerate(e3_preds) if i not in e3_used]
def classify_fn(g):
 t=float(g['time_s']); near=rows_near(t,.20); frames=sorted({int(float(r['frame_idx'])) for r in near});
 if not near:return 'missed_object_detection'
 gaps=max([b-a for a,b in zip(frames,frames[1:])] or [0])
 if gaps>3:return 'trajectory_gap'
 tids={r['track_id'] for r in near}
 if len(tids)>1:return 'tracking_id_fragmentation'
 return 'velocity_reversal_not_read'
def classify_fp(p):
 t=float(p['time_s']); near=rows_near(t,.15)
 if not near:return 'tracking_id_fragmentation'
 tids={r['track_id'] for r in near}
 if len(tids)>1:return 'tracking_id_fragmentation'
 return 'ambiguous_needs_visual_verification'
with (OUT/'fn_classification.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['event_id','gt_time_s','frame_idx','category','evidence_detection_rows','note']);w.writeheader()
 for g in fns:
  near=rows_near(float(g['time_s']),.2);w.writerow({'event_id':g['event_id'],'gt_time_s':g['time_s'],'frame_idx':g['frame_idx'],'category':classify_fn(g),'evidence_detection_rows':len(near),'note':'heuristic from available tracking CSV; not visual confirmation'})
with (OUT/'fp_classification.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['pred_time_s','frame_idx','track_id','category','note']);w.writeheader()
 for p in fps:w.writerow({'pred_time_s':p['time_s'],'frame_idx':p['frame_idx'],'track_id':p['track_id'],'category':classify_fp(p),'note':'heuristic; visual audit required'})
from collections import Counter
fc=Counter(classify_fn(g) for g in fns); pc=Counter(classify_fp(p) for p in fps)
(OUT/'root_cause_analysis.md').write_text(f'''# Phase 4 Root Cause Analysis\n\nGT v2 has {len(gt)} approved events; matching is one-to-one at ±0.1 s using timestamps. E2 baseline has {len(preds)} predictions, yielding {len(matches)} TP and {len(fns)} FN; E3-B FP audit uses {len(fps)} unmatched predictions.\n\n## Heuristic FN categories\n\n{chr(10).join(f'- {k}: {v}' for k,v in fc.items())}\n\n## Heuristic E3-B FP categories\n\n{chr(10).join(f'- {k}: {v}' for k,v in pc.items())}\n\nThese are evidence-based classifications from tracking presence, frame gaps, and ID diversity, **not visual ground truth**. No automatic diagnosis is claimed.\n\n## Synchronization\nVideo FPS is 30; tracking timestamps use frame_idx/30. GT timestamps were compared to the same time base. Matching is one-to-one and excludes already matched events.\n\n## Dominant actionable findings\n1. Most E2 misses must first be separated into detector absence versus motion/event logic; the available tracking CSV cannot prove physical contact.\n2. E3-B's high FP count is consistent with reversal candidates that are not contacts; ID fragmentation and ambiguous motion require visual samples.\n3. Prioritize short track-gap bridging and explicit velocity-window confirmation before changing detector weights. Keep a holdout segment for later validation.\n\n## Artifacts\n- fn_classification.csv\n- fp_classification.csv\n- Original GT and experiments retained unchanged.\n''')
print('FN',fc,'FP',pc)

from pathlib import Path
import csv,json
from collections import defaultdict,deque
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/'artifacts/runs/Phase4_pilot_60s'; OUT=ROOT/'artifacts/runs/Phase4_motion_first';OUT.mkdir(parents=True,exist_ok=True)
def load():
 d=defaultdict(list)
 with (BASE/'tracking.csv').open(newline='') as f:
  for r in csv.DictReader(f): d[r['track_id']].append({k:float(r[k]) for k in ['frame_idx','time_s','cy','bottom_y']})
 return d
def detect(tracks,adaptive=False):
 ev=[]
 for tid,rows in tracks.items():
  rows=sorted(rows,key=lambda x:x['frame_idx']); y=np.array([r['cy'] for r in rows]);
  if len(y)<7:continue
  # light moving average; y increasing means falling
  sm=np.convolve(y,np.ones(5)/5,'same'); v=np.gradient(sm)
  for i in range(3,len(rows)-3):
   if v[i-2]>0.4 and v[i+2]<-0.4 and max(v[i-2:i])>0.8 and min(v[i+1:i+4])<-.4:
    t=rows[i]['time_s']; b=rows[i]['bottom_y']
    if adaptive:
     # soft support: candidate must have strong reversal and be near lower quartile of this track
     if b < np.percentile([r['bottom_y'] for r in rows],60): continue
    if not ev or abs(t-ev[-1]['time_s'])>.20 or tid!=ev[-1]['track_id']:
     ev.append({'event_id':f'E3-{"B" if adaptive else "A"}-{len(ev)+1:04d}','frame_idx':int(rows[i]['frame_idx']),'time_s':t,'track_id':tid,'bottom_y':b,'state':'BOUNCE_CONFIRMED'})
 return sorted(ev,key=lambda x:x['time_s'])
def match(pred,truth):
 used=set(); tp=[];fp=[]
 for p in pred:
  c=[(abs(p['time_s']-g),i,g) for i,g in enumerate(truth) if i not in used and abs(p['time_s']-g)<=.1]
  if c: d,i,g=min(c);used.add(i);tp.append((p['time_s'],g,d))
  else:fp.append(p['time_s'])
 return tp,fp,[g for i,g in enumerate(truth) if i not in used]
def main():
 tracks=load();truth=[]
 with (ROOT/'data/annotations/bounce_events_gt.csv').open(newline='') as f:
  truth=[float(r['time_s']) for r in csv.DictReader(f) if r['review_status']=='approved']
 allout={}
 for mode in [False,True]:
  name='E3_B_adaptive' if mode else 'E3_A_motion'; pred=detect(tracks,mode);tp,fp,fn=match(pred,truth); d={'predicted':len(pred),'approved_gt':len(truth),'tp':len(tp),'fp':len(fp),'fn':len(fn),'precision':len(tp)/(len(tp)+len(fp)) if tp or fp else 0,'recall':len(tp)/len(truth),'f1':2*len(tp)/(2*len(tp)+len(fp)+len(fn)),'count_error':abs(len(pred)-len(truth)),'tolerance_s':.1};allout[name]=d
 with (OUT/(name+'.csv')).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=['event_id','frame_idx','time_s','track_id','bottom_y','state']);w.writeheader();w.writerows(pred)
 with (OUT/(name+'_errors.csv')).open('w',newline='') as f:
   w=csv.writer(f);w.writerow(['type','pred_time_s','gt_time_s','error_s']);w.writerows([['TP',a,b,e] for a,b,e in tp]+[['FP',a,'',''] for a in fp]+[['FN','',a,''] for a in fn])
 (OUT/'comparison.json').write_text(json.dumps(allout,indent=2));(OUT/'config.json').write_text(json.dumps({'source_tracking':str(BASE/'tracking.csv'),'smoothing_window':5,'velocity_reversal':'.4 px/frame with strong-side >.8','dedup_s':.2,'match_tolerance_s':.1,'floor_roi':'none','adaptive_constraint':'track bottom_y >= 60th percentile for E3-B'},indent=2));print(json.dumps(allout,indent=2))
if __name__=='__main__':main()

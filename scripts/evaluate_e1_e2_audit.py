from pathlib import Path
import csv,json,time,hashlib,platform
import cv2
from ultralytics import YOLO
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'artifacts/evaluation/E1_vs_E2'; OUT.mkdir(parents=True,exist_ok=True)
IMG=640; FLOOR=.001; MATCH=.5
sets={'val':ROOT/'data/cvat_phase2_reviewed/final/val/obj_train_data','test':ROOT/'data/cvat_phase2_reviewed/final/test/obj_train_data'}
def iou(a,b):
 x=max(0,min(a[2],b[2])-max(a[0],b[0])); y=max(0,min(a[3],b[3])-max(a[1],b[1])); z=x*y; aa=max(0,a[2]-a[0])*max(0,a[3]-a[1]);bb=max(0,b[2]-b[0])*max(0,b[3]-b[1]);return z/(aa+bb-z+1e-9)
def gt(im):
 w,h=1280,720; out=[]
 for l in im.with_suffix('.txt').read_text().splitlines():
  if l.strip(): _,x,y,bw,bh=map(float,l.split());out.append([(x-bw/2)*w,(y-bh/2)*h,(x+bw/2)*w,(y+bh/2)*h])
 return out
def collect(model,cls,folder):
 out=[]
 for im in sorted(folder.glob('*.jpg')):
  r=model.predict(str(im),imgsz=IMG,conf=FLOOR,classes=[cls],device='cpu',verbose=False)[0]; pred=[(b.tolist(),float(s)) for b,s in zip(r.boxes.xyxy.cpu(),r.boxes.conf.cpu())];out.append((im,gt(im),pred))
 return out
def stats(data,thr=.25,match=.5):
 tp=fp=fn=0; ranked=[]; per=[]
 for im,g,p in data:
  p=[x for x in p if x[1]>=thr]; used=set(); t=f=0
  for b,s in sorted(p,key=lambda x:-x[1]):
   q=max([(iou(b,z),j) for j,z in enumerate(g) if j not in used],default=(0,-1))
   if q[0]>=match:used.add(q[1]);tp+=1;t+=1;ranked.append((s,1))
   else:fp+=1;f+=1;ranked.append((s,0))
  fn+=len(g)-t;per.append({'image':im.name,'gt':len(g),'pred':len(p),'tp':t,'fp':f,'fn':len(g)-t})
 p=tp/(tp+fp) if tp+fp else 0;r=tp/(tp+fn) if tp+fn else 0;f1=2*p*r/(p+r) if p+r else 0
 return {'precision':p,'recall':r,'f1':f1,'tp':tp,'fp':fp,'fn':fn,'per':per}
def ap(data,match):
 all=[]; n=sum(len(g) for _,g,_ in data)
 for im,g,p in data:
  used=set()
  for b,s in sorted(p,key=lambda x:-x[1]):
   q=max([(iou(b,z),j) for j,z in enumerate(g) if j not in used],default=(0,-1)); ok=q[0]>=match
   if ok:used.add(q[1])
   all.append((s,int(ok)))
 all.sort(reverse=True); tp=fp=0; rec=[];pre=[]
 for _,ok in all:
  tp+=ok;fp+=1-ok;rec.append(tp/n);pre.append(tp/(tp+fp))
 return sum(max((p for r,p in zip(rec,pre) if r>=x),default=0) for x in [i/100 for i in range(101)])/101
def main():
 models=[('E1',ROOT/'yolo26n.pt',32),('E2',ROOT/'artifacts/runs/E2_finetuned_cpu/weights/best.pt',0)]; final={}; logs=[]
 for name,path,cls in models:
  m=YOLO(str(path)); val=collect(m,cls,sets['val']); test=collect(m,cls,sets['test']); best=(0,0)
  for t in [i/100 for i in range(5,96,5)]:
   s=stats(val,t); (best:= (s['f1'],t)) if s['f1']>best[0] else None
  threshold=best[1]; fs=stats(test,threshold); maps=sum(ap(test,x) for x in [0.5+i*.05 for i in range(10)])/10
  aps=ap(test,.5); final[name]={'threshold_from_val':threshold,'test':{k:v for k,v in fs.items() if k!='per'},'AP50':aps,'mAP50_95':maps}
  for r in fs['per']: logs.append({'model':name,**r})
  with (OUT/f'pr_{name}.csv').open('w',newline='') as f:
   w=csv.writer(f);w.writerow(['threshold','precision','recall','f1']);
   for t in [i/100 for i in range(5,96,5)]:
    s=stats(val,t);w.writerow([t,s['precision'],s['recall'],s['f1']])
  with (OUT/f'false_positive_{name}.csv').open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=['image','gt','pred','tp','fp','fn']);w.writeheader();w.writerows([r for r in fs['per'] if r['fp'] or r['fn']])
 with (OUT/'per_image_final.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['model','image','gt','pred','tp','fp','fn']);w.writeheader();w.writerows(logs)
 config={'imgsz':IMG,'floor_conf':FLOOR,'match_iou':MATCH,'threshold_selection':'validation F1 grid 0.05..0.95','ap_iou':'0.50:0.05:0.95','device':'cpu','batch':1,'nms':'Ultralytics predict defaults','python':platform.python_version()}
 (OUT/'evaluation_config.json').write_text(json.dumps(config,indent=2));(OUT/'final_metrics.json').write_text(json.dumps(final,indent=2))
 (OUT/'evaluation_audit.md').write_text('# Phase 3B Evaluation Audit\n\nThe earlier diagnostic used confidence floor 0.001, explaining E2 high recall and low operating precision: AP integrates the ranked precision-recall curve, while fixed-threshold precision counts every retained prediction. Final thresholds were selected only on validation by F1 grid and then frozen for test. E1 class 32 and E2 class 0 were remapped to canonical basketball. Matching is one-to-one greedy by descending confidence at IoU 0.5. Test was not used for threshold selection.\n')
 print(json.dumps(final,indent=2))
if __name__=='__main__':main()

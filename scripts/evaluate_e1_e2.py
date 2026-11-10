from pathlib import Path
import csv, hashlib, json, time
import cv2
from ultralytics import YOLO

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/evaluation/E1_vs_E2'; OUT.mkdir(parents=True,exist_ok=True)
TEST=ROOT/'data/cvat_phase2_reviewed/final/test/obj_train_data'
IMAGES=sorted(TEST.glob('*.jpg')); IOU=.5; CONF=.001; IMGSZ=640

def sha(p):
 h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def box_iou(a,b):
 x1=max(a[0],b[0]); y1=max(a[1],b[1]); x2=min(a[2],b[2]); y2=min(a[3],b[3]); inter=max(0,x2-x1)*max(0,y2-y1)
 aa=max(0,a[2]-a[0])*max(0,a[3]-a[1]); bb=max(0,b[2]-b[0])*max(0,b[3]-b[1]); return inter/(aa+bb-inter+1e-9)
def gt_for(im):
 w,h=1280,720; out=[]
 for line in im.with_suffix('.txt').read_text().splitlines():
  if not line.strip(): continue
  _,x,y,bw,bh=map(float,line.split()); out.append([(x-bw/2)*w,(y-bh/2)*h,(x+bw/2)*w,(y+bh/2)*h])
 return out
def ap(rec,prec):
 r=[i/100 for i in range(101)]; return sum(max((p for rr,p in zip(rec,prec) if rr>=x),default=0) for x in r)/101

def evaluate(model_path, e1=False):
 model=YOLO(str(model_path)); rows=[]; tp_all=[]; fp_all=[]; scores=[]; n_gt=0; total=0
 for im in IMAGES:
  gt=gt_for(im); n_gt+=len(gt); start=time.perf_counter(); res=model.predict(str(im),imgsz=IMGSZ,conf=CONF,verbose=False,device='cpu')[0]; elapsed=time.perf_counter()-start; total+=elapsed
  pred=[]
  for b,c,s in zip(res.boxes.xyxy.cpu().tolist(),res.boxes.cls.cpu().tolist(),res.boxes.conf.cpu().tolist()):
   if (e1 and int(c)==32) or ((not e1) and int(c)==0): pred.append((b,float(s)))
  used=set(); tp=fp=0
  for b,s in sorted(pred,key=lambda z:-z[1]):
   best=max([(box_iou(b,g),i) for i,g in enumerate(gt) if i not in used],default=(0,-1))
   ok=best[0]>=IOU
   if ok: used.add(best[1]); tp+=1; tp_all.append(1); fp_all.append(0)
   else: fp+=1; tp_all.append(0); fp_all.append(1)
   scores.append(s)
  rows.append({'image':im.name,'gt':len(gt),'pred':len(pred),'tp':tp,'fp':fp,'fn':len(gt)-tp,'inference_ms':elapsed*1000})
 order=sorted(range(len(scores)),key=lambda i:-scores[i]); cumtp=cumfp=0; rec=[]; prec=[]
 for i in order:
  cumtp+=tp_all[i]; cumfp+=fp_all[i]; rec.append(cumtp/n_gt); prec.append(cumtp/(cumtp+cumfp))
 p= sum(tp_all)/(sum(tp_all)+sum(fp_all)) if sum(tp_all)+sum(fp_all) else 0; r=sum(tp_all)/n_gt if n_gt else 0
 return {'model':str(model_path),'images':len(IMAGES),'gt':n_gt,'tp':sum(tp_all),'fp':sum(fp_all),'fn':n_gt-sum(tp_all),'precision':p,'recall':r,'ap50':ap(rec,prec),'mean_inference_ms':total/len(IMAGES)*1000,'rows':rows}

def main():
 e1=evaluate(ROOT/'yolo26n.pt',True); e2=evaluate(ROOT/'artifacts/runs/E2_finetuned_cpu/weights/best.pt',False)
 (OUT/'metrics.json').write_text(json.dumps({'protocol':{'imgsz':IMGSZ,'confidence':CONF,'iou_match':IOU,'device':'cpu','e1_class':32,'e2_class':0},'E1':{k:v for k,v in e1.items() if k!='rows'},'E2':{k:v for k,v in e2.items() if k!='rows'}},indent=2))
 with (OUT/'per_image.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['model','image','gt','pred','tp','fp','fn','inference_ms']); w.writeheader()
  for name,d in [('E1',e1),('E2',e2)]:
   for r in d['rows']: w.writerow({'model':name,**r})
 for name,d in [('E1',e1),('E2',e2)]:
  m=YOLO(d['model']); pred=ROOT/'artifacts/evaluation/E1_vs_E2/predictions'/name; pred.mkdir(parents=True,exist_ok=True)
  for im in IMAGES: m.predict(str(im),imgsz=IMGSZ,conf=.25,classes=[32] if name=='E1' else [0],save=True,project=str(pred),name='vis',exist_ok=True,verbose=False,device='cpu')
 (OUT/'evaluation_summary.md').write_text('# E1 vs E2 test evaluation\n\nMetrics are computed on the identical 18-image test split with E1 COCO class 32 remapped to canonical basketball and E2 class 0. Matching IoU=0.5, prediction confidence floor=0.001, imgsz=640, CPU. AP is the 101-point interpolated AP over confidence-ranked detections. No threshold tuning was performed on test.\n\nNote: three reviewed frames contain four boxes; counts alone do not prove errors, and no annotations were deleted automatically.\n')
 print(json.dumps({'E1':{k:e1[k] for k in ['precision','recall','ap50','mean_inference_ms']},'E2':{k:e2[k] for k in ['precision','recall','ap50','mean_inference_ms']}},indent=2))
if __name__=='__main__': main()

from pathlib import Path
import csv, cv2
ROOT=Path(__file__).resolve().parents[1]; outdir=ROOT/'artifacts/runs/Phase4_motion_first'; video=ROOT/'videofull.mp4'
events=[]
with (outdir/'E3_B_adaptive.csv').open(newline='') as f: events=list(csv.DictReader(f))
byframe={}
for e in events: byframe.setdefault(int(e['frame_idx']),[]).append(e)
cap=cv2.VideoCapture(str(video)); fps=cap.get(cv2.CAP_PROP_FPS) or 30; n=min(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),int(60*fps)); w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out=cv2.VideoWriter(str(outdir/'bounce_preview_E3_B_60s.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),fps,(w,h)); total=0
for fi in range(n):
 ok,img=cap.read()
 if not ok: break
 for e in byframe.get(fi,[]):
  total+=1; cv2.drawMarker(img,(w//2,int(h*.8)),(0,0,255),cv2.MARKER_CROSS,30,3); cv2.putText(img,'BOUNCE +1',(w//2+15,int(h*.8)-12),0,.8,(0,0,255),2)
 cv2.putText(img,f'E3-B adaptive | t={fi/fps:.2f}s | bounces={total}',(20,32),0,.8,(0,0,255),2); out.write(img)
cap.release();out.release();print(f'events={len(events)} output={outdir/"bounce_preview_E3_B_60s.mp4"}')

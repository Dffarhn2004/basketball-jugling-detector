"""Create immutable Phase 1 intake and a short YOLO/ByteTrack baseline."""
from pathlib import Path
import csv, hashlib, json, shutil, time
import cv2
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "videofull.mp4"
RUN = ROOT / "artifacts" / "runs" / "E1_20261016_0025"
RUN.mkdir(parents=True, exist_ok=False)

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024), b""): h.update(block)
    return h.hexdigest()

cap=cv2.VideoCapture(str(SRC)); fps=cap.get(cv2.CAP_PROP_FPS); n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)); duration=n/fps
fourcc=int(cap.get(cv2.CAP_PROP_FOURCC)); codec=''.join(chr((fourcc >> 8*i)&255) for i in range(4))
meta={"source":"videofull.mp4","sha256":sha256(SRC),"bytes":SRC.stat().st_size,"width":w,"height":h,"fps_nominal":fps,"frame_count":n,"duration_seconds":duration,"codec":codec,"audio":"not inspected","timebase":"OpenCV frame index / 30 FPS; PTS unavailable via OpenCV","rights_notes":"User-provided local file; preserve original."}
(RUN/"video_metadata.json").write_text(json.dumps(meta,indent=2), encoding="utf-8")
clip=RUN/"clip_60s.mp4"; out=cv2.VideoWriter(str(clip),cv2.VideoWriter_fourcc(*'mp4v'),fps,(w,h))
for i in range(min(n,int(fps*60))):
    ok,frame=cap.read()
    if not ok: break
    out.write(frame)
out.release(); cap.release()
config={"run_id":RUN.name,"model":"yolo26n.pt","device":"cpu","imgsz":640,"conf":0.25,"iou":0.7,"classes":"sports ball (canonical COCO name)","tracker":"bytetrack.yaml","clip_seconds":60,"weights_modified":False}
(RUN/"config.json").write_text(json.dumps(config,indent=2), encoding="utf-8")
model=YOLO("yolo26n.pt")
(RUN/"model_metadata.json").write_text(json.dumps({"package":"ultralytics","version":"8.4.177","model_names":model.names,"weights":"yolo26n.pt","weights_hash":"not exposed by API; file path recorded","device":"cpu"},indent=2,default=str),encoding="utf-8")
cap=cv2.VideoCapture(str(clip)); writer=cv2.VideoWriter(str(RUN/"preview.mp4"),cv2.VideoWriter_fourcc(*'mp4v'),fps,(w,h)); rows=[]; start=time.time()
for i,result in enumerate(model.track(source=str(clip), stream=True, persist=True, tracker="bytetrack.yaml", imgsz=640, conf=0.25, iou=0.7, classes=[32], device="cpu", verbose=False)):
    frame=result.plot()
    writer.write(frame)
    boxes=result.boxes
    if boxes is not None:
        for j in range(len(boxes)):
            xyxy=boxes.xyxy[j].cpu().tolist(); conf=float(boxes.conf[j].cpu()); tid=int(boxes.id[j].cpu()) if boxes.id is not None else None
            rows.append([i, i/fps, tid, *xyxy, conf, 32, "sports ball"])
writer.release(); cap.release()
with (RUN/"detections_tracks.csv").open("w",newline="",encoding="utf-8") as f:
    cw=csv.writer(f); cw.writerow(["frame_idx","timestamp_s","track_id","x1","y1","x2","y2","confidence","class_id","class_name"]); cw.writerows(rows)
(RUN/"run_summary.json").write_text(json.dumps({"frames_processed":i+1,"detections":len(rows),"elapsed_seconds":time.time()-start,"observations":"Requires manual review of preview for misses, false positives, blur, occlusion, and ID switches; no accuracy claims."},indent=2),encoding="utf-8")
print(RUN)

"""Sample temporal-split frames and export YOLO candidate labels for human review."""
from __future__ import annotations
import csv, hashlib, json
from pathlib import Path
import cv2
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
VIDEO = ROOT / "videofull.mp4"
OUT = ROOT / "data" / "detection"
RUN_ID = "phase2_annotation_v1"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""): h.update(block)
    return h.hexdigest()

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Sample temporal-split frames and create unverified YOLO candidates.")
    parser.add_argument("--interval-s", type=float, default=2.0, help="seconds between samples; default targets about 400-600 frames")
    args = parser.parse_args()
    if args.interval_s <= 0:
        parser.error("--interval-s must be positive")
    manifest = []
    segments = []
    with (ROOT / "data/splits/split_manifest.csv").open(newline="", encoding="utf8") as f:
        for row in csv.DictReader(f):
            if row["split"] in {"train", "val", "test"}:
                segments.append(row)
    # Temporal split and exclusion buffers are fixed; interval only samples within allowed segments.
    cap = cv2.VideoCapture(str(VIDEO)); fps = cap.get(cv2.CAP_PROP_FPS)
    for seg in segments:
        start, end = float(seg["start_time_s"]), float(seg["end_time_s"])
        t = start + min(args.interval_s / 2, 5.0)
        while t < end:
            frame_idx = round(t * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ok, image = cap.read()
            if not ok: raise RuntimeError(f"could not decode frame {frame_idx}")
            split = seg["split"]; image_dir = OUT / "images" / split; label_dir = OUT / "labels" / split
            image_dir.mkdir(parents=True, exist_ok=True); label_dir.mkdir(parents=True, exist_ok=True)
            name = f"{RUN_ID}_{frame_idx:06d}"
            image_path = image_dir / f"{name}.jpg"; image_path_str = str(image_path.relative_to(ROOT))
            cv2.imwrite(str(image_path), image)
            manifest.append([name, frame_idx, frame_idx / fps, split, "uniform_time", image_path_str, "candidate_unreviewed"])
            t += args.interval_s
    cap.release()
    (OUT / "frame_manifest.csv").parent.mkdir(exist_ok=True)
    with (OUT / "frame_manifest.csv").open("w", newline="", encoding="utf8") as f:
        w = csv.writer(f); w.writerow(["file","source_frame_idx","source_time_s","split","selection_reason","image_file","annotation_status"]); w.writerows(manifest)
    model = YOLO("yolo26n.pt")
    with (OUT / "candidate_labels.csv").open("w", newline="", encoding="utf8") as f:
        w = csv.writer(f); w.writerow(["file","class_id","pretrained_class_id","class_name","x1","y1","x2","y2","confidence","candidate_status"])
        for row in manifest:
            result = model.predict(source=str(ROOT / row[5]), device="cpu", imgsz=640, conf=0.25, classes=[32], verbose=False)[0]
            h, width = result.orig_shape
            label_path = OUT / "labels" / row[3] / f"{row[0]}.txt"
            with label_path.open("w", encoding="utf8") as labels:
                for box in result.boxes:
                    x1,y1,x2,y2 = box.xyxy[0].tolist(); conf=float(box.conf[0])
                    w.writerow([row[0],0,32,"sports ball",x1,y1,x2,y2,conf,"candidate_unreviewed"])
                    labels.write(f"0 {((x1+x2)/2)/width:.8f} {((y1+y2)/2)/h:.8f} {(x2-x1)/width:.8f} {(y2-y1)/h:.8f}\n")
    (OUT / "annotation_instructions.md").write_text("Candidate labels map COCO class 32 sports ball to dataset class 0 basketball. Human must correct, approve, or reject every box; candidate_status is never ground truth. Import images/labels into CVAT as YOLO 1.1, review, then export YOLO and replace only after versioning.", encoding="utf8")
    print(json.dumps({"frames":len(manifest),"by_split":{s:sum(r[3]==s for r in manifest) for s in ("train","val","test")},"status":"candidate_unreviewed"}, indent=2))
if __name__ == "__main__": main()

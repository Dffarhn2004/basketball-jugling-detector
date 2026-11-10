"""Jalankan metode akhir (parameter beku) dengan bobot E2-blur pada segmen GT, simpan event ke CSV.
Pakai: python scripts/compare_blur_segments.py <start_s> <end_s> [bobot]   (bobot default E2_blur_cpu/best.pt)
Konvensi sama dengan prediksi E2: waktu = frame / 30; conf 0.25, imgsz 640, kelas 0."""
import csv, sys
from pathlib import Path
import cv2
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "scripts")); import phase4_bridging as pb
S, E = float(sys.argv[1]), float(sys.argv[2])
W = ROOT / (sys.argv[3] if len(sys.argv) > 3 else "artifacts/runs/E2_blur_cpu/weights/best.pt")
OUT = ROOT / "artifacts/runs/Phase5_blur"; OUT.mkdir(parents=True, exist_ok=True); tag = f"{S:g}_{E:g}"
RAW, EV = OUT / f"raw_{tag}.csv", OUT / f"events_{tag}.csv"
a, b = int(S * 30), int(E * 30)
if not RAW.exists():
    from ultralytics import YOLO
    model = YOLO(str(W)); cap = cv2.VideoCapture(str(ROOT / "videofull.mp4")); cap.set(cv2.CAP_PROP_POS_FRAMES, a); rows = []
    for fi in range(a, b):
        ok, img = cap.read()
        if not ok: break
        r = model.predict(img, conf=0.25, imgsz=640, classes=[0], verbose=False)[0]
        rows += [dict(frame_idx=fi, x1=x[0], y1=x[1], x2=x[2], y2=x[3], confidence=s) for x, s in zip(r.boxes.xyxy.tolist(), r.boxes.conf.tolist())]
    with RAW.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["frame_idx", "x1", "y1", "x2", "y2", "confidence"]); w.writeheader(); w.writerows(rows)
raw = pb.defaultdict(list)
for r in pb.read(RAW):
    x1, y1, x2, y2 = (float(r[k]) for k in ("x1", "y1", "x2", "y2")); raw[int(r["frame_idx"])].append(((x1+x2)/2, (y1+y2)/2, y2, max(x2-x1, y2-y1), float(r["confidence"])))
tracks = pb.track(raw, gate=1.5, max_miss=4, n=b); ev = pb.events(tracks, floor=.65, min_drop=15, min_rise=15)
with EV.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["frame_idx", "time_s", "track_id", "bottom_y"]); w.writeheader(); w.writerows(ev)
print(tag, "events:", sum(1 for e in ev if S <= e["time_s"] < E))

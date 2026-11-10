# Tracking with ByteTrack

## Kegunaan
Asosiasikan bbox bola antarfame menjadi track sementara sehingga bisa memperkirakan arah, kecepatan dan fase bounce.

## Input/Output
Input: bbox `(x1,y1,x2,y2)`, confidence, class dan frame/time. Output: `track_id`, bbox, confidence, time per frame. Jika ID hilang, jangan membuat koordinat palsu.

## Usage sketch (frame by frame)
```python
import cv2
from ultralytics import YOLO

model = YOLO('yolo26n.pt')
cap = cv2.VideoCapture('data/raw/source.mp4')
while True:
    ok, frame = cap.read()
    if not ok:
        break
    result = model.track(frame, persist=True, tracker='bytetrack.yaml')[0]
    # extract result.boxes.id, .xyxy, .conf if available
    # append frame/time metadata and parse only real ball class
cap.release()
```
Jangan membuka video dari awal untuk tiap frame; `persist=True` digunakan hanya selama stream yang sama. Reset state tracker antar klip independen dan jangan mengasumsikan global ID antar segmen.

## Field yang disimpan
`frame_idx,time_s,track_id,x1,y1,x2,y2,confidence,center_x,center_y,bottom_y,visible_flag`.

## Parameter yang dapat dioptimasi di validation
- `track_high_thresh`, `track_low_thresh`, `new_track_thresh`, `track_buffer`, `match_thresh` bila didukung config versi sekarang.
- `conf` detector harus konsisten pada E1/E2.

## Failure modes
- ID switch dua bola saling melewati.
- Track fragmented setelah occlusion.
- Low-confidence ball missed saat blur.
- False new track untuk bayangan/objek mirip bola.

## QC
Review 4 klip: bergerak cepat, bola overlap, kontak dekat lantai, tangan menghalangi. Catat metrics tracking jika GT IDs tersedia, tetapi tugas utamanya **event count**, bukan MOT benchmark.

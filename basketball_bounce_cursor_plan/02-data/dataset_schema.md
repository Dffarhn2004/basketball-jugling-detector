# Data Contracts: Images, Labels, Events, Manifests

## Struktur target
```text
data/
  raw/source.mp4
  metadata/source_video.json
  splits/split_manifest.csv
  detection/
    images/{train,val,test}/
    labels/{train,val,test}/
    dataset.yaml
  annotations/
    bounce_events_gt.csv
    gt_review_log.csv
    coverage_manifest.csv
  clips/
```

## `dataset.yaml` (contoh untuk Ultralytics)
```yaml
path: data/detection
train: images/train
val: images/val
test: images/test
names:
  0: basketball
```
Periksa path aktual saat CLI dijalankan; Ultralytics dapat menginterpretasi `path` relatif konfigurasi/environment.

## `frame_manifest.csv`
Kolom minimal: `file,source_frame_idx,source_time_s,split,selection_reason,source_sha256`.

## `bounce_events_gt.csv`
Kolom minimal: `event_id,frame_idx,time_s,x_contact_px,y_contact_px,confidence,review_status,segment_id,notes`.

## `detections.csv`
`run_id,frame_idx,time_s,det_idx,class_id,conf,x1,y1,x2,y2` (semua pixel coordinates pada original resolution).

## `tracks.csv`
`run_id,frame_idx,time_s,track_id,conf,x1,y1,x2,y2,center_x,center_y,bottom_y`.

## `events_pred.csv`
`run_id,event_id,time_s,frame_idx,x_contact_px,y_contact_px,track_id,confidence,reason,model_id`.

## `metrics.json`
```json
{
  "run_id": "TBD",
  "split": "test",
  "tp": null,
  "fp": null,
  "fn": null,
  "precision": null,
  "recall": null,
  "f1": null,
  "ground_truth_count": null,
  "predicted_count": null,
  "absolute_percentage_error": null
}
```

## Unit + null handling
- Time seconds float; frame index zero-based integer; coordinates px on source frame.
- Missing GT location may be `null`/empty, not fake `(0,0)`.
- Track ID is optional: fail to track ≠ fail to produce event location.
- Schema upgrade requires version bump and migration check.

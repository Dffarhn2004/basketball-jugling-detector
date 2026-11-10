# Phase 2 External Human Review Package

This package contains the frozen Phase 2 candidate dataset and E1 review artifacts. Paths inside the ZIP are relative to the project root, so each item can be traced back to its original location.

## Package contents

- `artifacts/runs/E1_20261016_0025/error_analysis/contact_sheet_30.jpg` — 30-frame contact sheet for rapid visual triage.
- `artifacts/runs/E1_20261016_0025/error_analysis/manual_review.csv` — per-sampled-frame review checklist.
- `artifacts/runs/E1_20261016_0025/preview.mp4` — rendered E1 preview video, 60.0 s at 30 FPS.
- `artifacts/runs/E1_20261016_0025/clip_60s.mp4` — 60-second source clip for annotation, 60.0 s at 30 FPS.
- `artifacts/runs/E1_20261016_0025/detections_tracks.csv` — E1 detections and tracking rows.
- `data/detection/frame_manifest.csv` — sampled-frame manifest with source frame/time and split information.
- `data/detection/candidate_labels.csv` — candidate detections requiring human verification.
- `data/detection/dataset.yaml` — YOLO dataset split and class definition (`0: basketball`).
- `data/annotations/ANNOTATION_GUIDE.md` — detailed detection and bounce annotation guidance.
- `data/detection/images/{train,val,test}/` — all 111 sampled images (75 train, 18 val, 18 test).
- `data/detection/labels/{train,val,test}/` — matching YOLO label files, including empty files where no candidate box was recorded.

No model weights, Python environment, or full 20-minute source video is included. No training or annotation changes were performed; the E1 baseline and candidate annotations remain unchanged.

## Bounce definition

A valid bounce is one physical contact between one basketball and the floor. The clearest contact frame should be marked. Catching, throwing, hand redirection, and other non-floor contacts are not bounces. Simultaneous contacts by different balls are separate events. Reviewers should record timestamp, contact coordinates, confidence (`certain`, `probable`, or `uncertain`), and review status (`approved`, `excluded`, or `unresolved`) according to `data/annotations/ANNOTATION_GUIDE.md`.

## CSV return format

Please return CSV files without changing the supplied source rows or column names. Use UTF-8 CSV with one header row. For frame/detection review, preserve the identifiers (`frame_idx`, `time_s`, `file`, and/or source track/detection IDs) and fill review fields such as `review_status` and `notes`; use `approved`, `excluded`, or `unresolved` consistently. For bounce events, use one row per physical event with at least:

`event_id,frame_idx,time_s,x,y,confidence,review_status,reviewer,notes`

Use integer `frame_idx`, seconds for `time_s`, pixel coordinates for `x,y`, confidence in `certain|probable|uncertain`, and status in `approved|excluded|unresolved`. Do not overwrite candidate/model values; add reviewer decisions in the designated review fields or a separate returned CSV. Empty-label images must still be reviewed and explicitly retained as empty when appropriate.

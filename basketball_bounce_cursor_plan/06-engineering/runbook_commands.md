# Execution Runbook — From Empty Repo to Submission

Commands below are **target commands that Cursor needs to implement**, not claims that they already work.

## 0. Setup
```shell
python -m bounce_counter doctor
pytest -q
```

## 1. Video metadata
```shell
python -m bounce_counter video-info --input data/raw/source.mp4 --output data/metadata/source_video.json
```
Check duration/frame count/codec. Fail if video missing.

## 2. Baseline E1
```shell
python -m bounce_counter detect --input data/raw/source.mp4 --config configs/pretrained_e1.yaml --run-id E1_BASE
```
Record **immutable** predictions and run manifest before changing detector.

## 3. Validate annotation + splits
```shell
python -m bounce_counter validate-data --config data/detection/dataset.yaml
```

## 4. E2 training
```shell
python -m bounce_counter train --config configs/finetune_e2.yaml --run-id E2_TRAIN
```

## 5. Model inference & event counting
```shell
python -m bounce_counter track --input data/raw/source.mp4 --config configs/pipeline_v0.yaml --run-id E2_TRACK
python -m bounce_counter count --tracks artifacts/runs/E2_TRACK/tracks.csv --config configs/pipeline_v0.yaml --run-id E2_EVENTS
```

## 6. Evaluate
```shell
python -m bounce_counter evaluate --prediction artifacts/runs/E2_EVENTS/events.csv --ground-truth data/annotations/bounce_events_gt.csv --split test --config configs/evaluation.yaml
```

## 7. Render video
```shell
python -m bounce_counter render --input data/raw/source.mp4 --run-id E2_EVENTS --output artifacts/videos/final.mp4
```

## 8. Final integrity
- `pytest -q` green.
- Every predicted event aligned with rendered counter.
- Every unmatched event audited.
- GT approved by reviewer.
- All deliverables accessible via link.

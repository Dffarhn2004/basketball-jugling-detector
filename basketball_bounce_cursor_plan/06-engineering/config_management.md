# Configuration Management

## Prinsip
- Satu YAML untuk model + inference, satu YAML untuk pipeline/event, satu YAML evaluation.
- Simpan snapshot config ke tiap run untuk E1/E2/E3.
- Gunakan schema validation (`pydantic` dataclasses atau typed config) dengan documented ranges.
- Tidak ada threshold tersebar di kode.

## Example event config (placeholder belum dikalibrasi)
```yaml
video:
  input: data/raw/source.mp4
  use_presentation_timestamps: true
model:
  weights: yolo26n.pt
  imgsz: 640
  confidence: 0.25
  iou: 0.7
tracking:
  backend: bytetrack.yaml
floor:
  mode: line
  points_px: null
  tolerance_px: null
event:
  smoothing_window_frames: 3
  min_downward_velocity_px_s: null
  min_upward_velocity_px_s: null
  confirm_frames: null
  max_gap_frames: null
  cooldown_ms: null
  dedup_temporal_tolerance_s: null
  dedup_spatial_tolerance_px: null
```

## Null bukan default runtime valid
Parameter `null` yang perlu kalibrasi menyebabkan validator menolak full pipeline run. Jangan diam-diam mengisi angka arbitrer. Cursor dapat menyediakan mode `calibrate-floor`/default candidate explicit di validation.

## Versioning
`pipeline_v0.yaml` dibekukan saat baseline E1/E2. `pipeline_v1.yaml` adalah tuned E3. Jangan edit v0 setelah E1 tanpa membuat `v0.1` dan rerun fairness benchmark.

## Secrets
Proyek offline secara desain. Jika memakai layanan luar untuk video/GPU, pakai `.env` yang gitignored, jangan tulis credential dalam config committed.

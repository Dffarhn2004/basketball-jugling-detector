# Proposed Command Line Interface

Cursor implement CLI bertahap. Format flags di bawah adalah **target API proyek**, belum ada script yang dijalankan.

```shell
python -m bounce_counter doctor
python -m bounce_counter video-info --input data/raw/source.mp4 --output data/metadata/source_video.json
python -m bounce_counter extract-frames --input data/raw/source.mp4 --split-manifest data/splits/split_manifest.csv --output data/detection/
python -m bounce_counter validate-data --config data/detection/dataset.yaml
python -m bounce_counter detect --input data/raw/source.mp4 --config configs/pretrained_e1.yaml --run-id E1_base
python -m bounce_counter train --config configs/finetune_e2.yaml --run-id E2_train_v1
python -m bounce_counter track --input data/raw/source.mp4 --run-id E2_track_v1 --config configs/pipeline_v0.yaml
python -m bounce_counter count --tracks artifacts/runs/E2_track_v1/tracks.csv --config configs/pipeline_v0.yaml --run-id E2_events_v1
python -m bounce_counter evaluate --prediction artifacts/runs/E2_events_v1/events.csv --ground-truth data/annotations/bounce_events_gt.csv --split-manifest data/splits/split_manifest.csv --split test --config configs/evaluation.yaml
python -m bounce_counter render --input data/raw/source.mp4 --run-id E2_events_v1 --output artifacts/videos/e2_annotated.mp4
```

## CLI contract
- `--help` di setiap subcommand.
- Exit nonzero pada failed validation/file missing/schema error.
- Print output folder, count, warning, run_id; jangan print success sebelum output valid.
- Paths bisa relatif/absolut via pathlib.
- Semua long tasks menunjukkan progress per frame/seconds, bukan hanya spinner.
- `--dry-run` tersedia untuk train/full-video render bila mudah ditambahkan.

## Key flags yang disarankan
- `--device cpu|cuda:0` untuk inference/training (validasi availability).
- `--start-time`, `--end-time` untuk sample clip.
- `--config` untuk YAML all settings.
- `--seed` training.
- `--output`/`--run-id` untuk provenance.

## Jangan buat terlalu banyak fitur
Hanya CLI yang dipakai eksperimen. Jangan implement API server kecuali pengguna meminta.

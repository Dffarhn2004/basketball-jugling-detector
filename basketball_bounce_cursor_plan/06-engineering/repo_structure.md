# Target Repository Layout (untuk Dibuat oleh Cursor)

```text
basketball-bounce-counter/
├── AGENTS.md
├── README.md
├── PROJECT_STATUS.md
├── DECISIONS.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── configs/
│   ├── dataset.yaml
│   ├── pretrained_e1.yaml
│   ├── finetune_e2.yaml
│   ├── pipeline_v0.yaml
│   ├── pipeline_v1.yaml
│   └── evaluation.yaml
├── src/bounce_counter/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── config.py
│   ├── schemas.py
│   ├── io/video.py
│   ├── io/csv_io.py
│   ├── io/metadata.py
│   ├── detection/model.py
│   ├── detection/detector.py
│   ├── tracking/bytetrack.py
│   ├── events/trajectory.py
│   ├── events/floor.py
│   ├── events/state_machine.py
│   ├── events/dedup.py
│   ├── evaluation/matching.py
│   ├── evaluation/metrics.py
│   ├── evaluation/errors.py
│   ├── visualization/render.py
│   └── training/train.py
├── scripts/
│   ├── collect_video_info.py
│   ├── extract_frames.py
│   └── make_error_clips.py
├── tests/
│   ├── unit/
│   └── integration/
├── data/                         # user-supplied, largely gitignored
│   ├── raw/
│   ├── detection/
│   ├── annotations/
│   └── splits/
├── artifacts/                    # gitignored unless selected reports
│   ├── runs/
│   ├── models/
│   ├── reports/
│   └── videos/
├── docs/                         # move/copy this planning pack here if desired
└── .github/workflows/tests.yml   # optional
```

## Scope control
- Implement only modules needed by the phase.
- Tunda `training/train.py` sampai P3 agar baseline tidak terpengaruh.
- Gunakan modul statistik pure Python/numpy terpisah dari torch.

## Gitignore principles
Ignore `data/raw/`, datasets frame imagery jika rights/privacy unclear, `artifacts/runs/` large, `*.pt` large weights, `.venv/`, cache. Sertakan schema/contoh config, source scripts, README; opsi LFS bila weights perlu diserahkan.

## Reproducibility
Artifact path selalu deterministic dari run id; jangan menimpa output eksperimen lama. Frame/sample artifacts disimpan sesuai provenance.

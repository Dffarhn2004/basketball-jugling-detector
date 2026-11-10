# Training Runs, Configuration Freeze, dan Reproducibility

## Unique run ID
Gunakan `YYYYMMDD_HHMMSS_E2_name` atau UUID ringkas; jangan overwrite folder experiment.

## Minimal manifest
```json
{
  "run_id": "TBD",
  "experiment": "E2",
  "git_commit": "TBD",
  "seed": 42,
  "model_base": "yolo26n.pt",
  "checkpoint_sha256": "TBD",
  "dataset_version": "TBD",
  "split_manifest_sha256": "TBD",
  "training_config": "configs/train_e2.yaml",
  "python_version": "TBD",
  "torch_version": "TBD",
  "ultralytics_version": "TBD",
  "device": "TBD",
  "started_at": "TBD",
  "finished_at": "TBD",
  "best_checkpoint": "TBD",
  "notes": ""
}
```

## Reproducibility checklist
- [ ] `pip freeze` / lock file.
- [ ] deterministic seed, perlu diakui bahwa GPU kadang nondeterministic.
- [ ] Dataset split dan annotation hash.
- [ ] Exact config training.
- [ ] Checkpoint dari experiment terpilih.
- [ ] Number of images, epochs actually completed, stop reason.
- [ ] Metrics dari real validation run.

## Run promotion
1. Semua run hasilnya independen, tidak overwrite.
2. Simpan pointer `artifacts/models/selected_detector.json` menuju approved checkpoint.
3. Promotion hanya setelah val evaluation dan QC.
4. Test evaluation tidak dijalankan pada semua candidate repeatedly untuk memilih pemenang.

## Pelaporan
Pisahkan `planned hyperparameters`, `executed hyperparameters`, dan `selected model` untuk menghindari claims yang tidak benar.

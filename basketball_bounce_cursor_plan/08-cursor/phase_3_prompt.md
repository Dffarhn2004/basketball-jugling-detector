# Cursor Prompt — Phase 3: Fine-Tuning

> Baca `AGENTS.md`, `03-model/fine_tuning_plan.md`, `03-model/augmentation_guide.md`, `03-model/training_runs_and_reproducibility.md`, `02-data/splits_leakage.md`, dan `05-experiments/experiment_matrix.md`. Kerjakan HANYA Phase 3. Validasi dataset dan jumlah label cukup, pisahkan validation dari holdout test. Tunjukkan command dan estimated compute terlebih dulu sebelum training GPU. Bila disetujui dan resource tersedia, fine-tune YOLO26n dari pretrained weights. Simpan config lengkap, random seed, package versions, dataset hashes, training/validation curves, best/last checkpoint serta mAP metrik nyata. Gunakan validation untuk memilih checkpoint dan hyperparameter; jangan pakai test untuk tuning. Jangan mengarang metrik bila training gagal. Simpan `E2` checkpoint yang distinct dari `E1`; update status & tests.

## Acceptance
- Fine-tuned weights berasal dari gradient training nyata.
- Training params dan curve tersedia.
- E1 baseline remains unchanged.

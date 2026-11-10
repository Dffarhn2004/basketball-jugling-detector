# Cursor Prompt — Phase 1: Video Intake & Pretrained Baseline

> Baca `AGENTS.md`, `02-data/video_intake_and_provenance.md`, `03-model/baseline_pretrained.md`, `04-pipeline/pipeline_contracts.md`, dan `05-experiments/experiment_matrix.md`. Kerjakan HANYA Phase 1. Pastikan ada file video lokal yang legal dan dapat diakses; jika belum ada, jelaskan blocker dan jalankan tes unit yang tidak membutuhkan video. Implementasikan video metadata (fps, frame count, PTS/timebase, duration, resolution, sha256), segment selection, dan ekstraksi frame. Jalankan pretrained YOLO26n pada potongan pendek representatif dengan config tersimpan. Catat detection outputs per frame, temporal trajectory awal ByteTrack, model version/weight hash, runtime, serta contoh error yang terlihat. Jangan latih model dan jangan menghitung final bounce GT palsu. Snapshot E1 baseline harus immutable dengan run ID unik. Jalankan tests, update status; berhenti setelah gate.

## Acceptance
- Media metadata konsisten dengan decode sampled frames.
- E1 baseline outputs tersimpan dengan path manifest.
- Pretrained weights tidak mengalami gradient update.
- Video analysis menggunakan actual timestamps, bukan tebakan.

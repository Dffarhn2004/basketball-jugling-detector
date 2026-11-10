# Implementation Backlog — Actionable Work Items

Kolom `D` = dependensi. Status awal seluruh item = **TODO**.

| ID | Prioritas | Task | D | Hasil/Acceptance |
|---|---|---|---|---|
| P0-01 | P0 | Buat package Python dengan layout `src/` | - | import sukses |
| P0-02 | P0 | Buat CLI `doctor`, `video-info`, `detect`, `track`, `count`, `evaluate`, `render` | 01 | help jelas |
| P0-03 | P0 | Buat config & schema validation | 01 | konfigurasi invalid ditolak |
| P0-04 | P0 | Setup unit test & CI lokal | 01 | pytest lulus |
| P1-01 | P0 | Verifikasi video source legal/local | - | source.mp4 terbaca, sha256 |
| P1-02 | P0 | Simpan video metadata, timebase | 01 | JSON metadata |
| P1-03 | P0 | Jalankan E1 pretrained di clip 60s | 02 | detections CSV + preview |
| P1-04 | P0 | Simpan E1 baseline immutable | 03 | run manifest dan config |
| P1-05 | P1 | Curate failure examples | 03 | kandidat frame sulit |
| P2-01 | P0 | Buat splits berdasarkan waktu | P1-02 | tidak overlap / leakage |
| P2-02 | P0 | Ekstrak train/val/test representative frames | 01 | frame manifest |
| P2-03 | P0 | Anotasi bbox bola | 02 | YOLO label files |
| P2-04 | P0 | QC bounding boxes | 03 | QC report |
| P2-05 | P0 | Manual GT bounce event full video | P1-02 | full GT CSV |
| P2-06 | P0 | Review dan resolve uncertain contacts | 05 | reviewed GT |
| P2-07 | P0 | Dataset validator dan hash version | 03,06 | dataset.yaml valid |
| P3-01 | P0 | Training fine-tune E2 | P2-07 | best.pt + log |
| P3-02 | P0 | Evaluate mAP detector on val/test | 01 | metrics actual |
| P3-03 | P1 | Error examples after fine-tuning | 02 | before/after panels |
| P4-01 | P0 | Tracking ByteTrack module | P1-03 | stable track schema |
| P4-02 | P0 | Smoothing & floor calibration | 01 | unit tests |
| P4-03 | P0 | Event state machine | 02 | events CSV |
| P4-04 | P0 | Deduplicate & simultaneous handling | 03 | synthetic tests |
| P4-05 | P0 | Video renderer + output writer | 03 | annotated MP4 |
| P5-01 | P0 | Freeze test protocol & matching tolerance | P2-05 | eval config |
| P5-02 | P0 | E1/E2 comparison on same test | P3,P4 | metrics + configs |
| P5-03 | P1 | E3 val-only optimization | 02 | tuned config |
| P5-04 | P0 | Full video inference and overall count | P4 | totals + timestamps |
| P5-05 | P0 | FP/FN exhaustive audit | P5-02,04 | errors.csv lengkap |
| P5-06 | P0 | Write report and render demo | P5-05 | submission assets |
| P5-07 | P0 | Reproduction test and packaging | P5-06 | clean instructions |

## Cara memakai backlog

Pilih **maksimal 1–3 task dalam satu iterasi Cursor**. Setelah selesai, sertakan path file, perintah, output test, dan catatan temuan. Jangan sekaligus memerintah agent membuat sistem penuh tanpa checkpoint.

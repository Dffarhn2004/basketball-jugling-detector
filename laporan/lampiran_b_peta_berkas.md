> The Juggling Bounces Challenge, laporan proyek. Bagian ini berdiri sendiri; lihat [README.md](README.md) untuk urutan.

## Lampiran B — Peta Berkas

| Berkas / folder | Isi |
|---|---|
| `data/cvat_phase2_reviewed/final/` | Anotasi deteksi (YOLO) yang sudah ditinjau |
| `data/annotations/bounce_events_gt_v2.csv` | GT bounce v2 (126 event) |
| `data/annotations/gt_segment_300_360.csv`, `gt_segment_900_960.csv` | GT bounce manual segmen tambahan (135 event masing-masing, sudah dikoreksi); `*.backup-before-correction.csv` = GT asli |
| `data/cvat_phase2_reviewed/final_blur/`, `configs/train_e2_blur.yaml` | Dataset latih dengan salinan motion blur (E2-blur) |
| `artifacts/runs/E2_blur_cpu/` | Training E2-blur |
| `artifacts/runs/Phase5_blur/` | Event E2-blur pada segmen GT dan hasil evaluasinya |
| `artifacts/runs/Phase5_gt_eval/` | Evaluasi E2 pada segmen GT (`eval_vs_gt.json`, `errors.csv`, klip error) |
| `artifacts/runs/Phase5_test_video/` | Hasil pada `videotesting.mp4` (tanpa GT) |
| `data/annotations/contact_points_sample.csv` | Titik kontak sampel (usulan AI, belum diverifikasi manusia) |
| `artifacts/runs/E2_finetuned_cpu/` | Training E2 (bobot, kurva, hasil) |
| `artifacts/evaluation/E1_vs_E2/` | Evaluasi detector |
| `artifacts/runs/Phase4_pilot_60s/` | Iterasi 1 (E2 + ByteTrack) |
| `artifacts/runs/Phase4_motion_first/` | Iterasi 2 (E3) |
| `artifacts/runs/Phase4_root_cause/` | Analisis heuristik awal |
| `artifacts/runs/Phase4_diagnostics/` | Diagnostik deteksi mentah |
| `artifacts/runs/Phase4_bridging/` | Metode akhir, event, video, klip verifikasi |
| `PROJECT_STATUS.md`, `CHANGELOG.md` | Catatan kerja berkelanjutan |

---
[< Lampiran A](lampiran_a_cara_mereproduksi.md) | [Daftar isi](README.md)

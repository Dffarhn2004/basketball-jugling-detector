# Changelog

## Unreleased (Phase 3-4 summary, added 2026-11-03)

- Phase 3: fine-tuned E2 on CPU; E2 test F1 0.98 vs E1 0.80 (`artifacts/evaluation/E1_vs_E2`).
- Phase 4: E2 + tracking pilot on 0-60 s, then motion-first E3-A/E3-B; E3 produced many false positives (E3-B P 0.13 / R 0.22 on GT v2).
- Added GT v2 (126 events) and re-evaluation; v1 (46) and v2 metrics are not comparable.
- Added heuristic root-cause analysis (tracking fragmentation); external visual review of 20 FN clips did not confirm it (10 detector-dropout candidates, 9 unclear, 1 ambiguous).
- Visual audit package is missing the 20 FP clips; human sign-off pending.
- Diagnostic pass (`scripts/phase4_diagnose.py`): detector fires near 105/107 FN; 15 FN fail the fixed floor-zone rule; multi-ball frames and missing GT contact coordinates block per-ball attribution. FP clips verified present (20/20) in the complete ZIP.
- Added contact-point tooling (`annotate_contact_points.py`, `export_contact_frames.py`, `phase4_diagnose_contact.py`). 4 AI-proposed points: raw detector sees the contact ball in ~7 frames, tracker keeps 1-5; hypothesis is tracker association loss.
- Added `scripts/phase4_bridging.py` (raw-detection distance association + lowest-point rule): holdout 30-60 s F1 1.00, dev F1 0.98, vs E2 0.27 and E3-B 0.16. Single video, GT v2 not second-pass reviewed; see `artifacts/runs/Phase4_bridging/SUMMARY.md`.
- Ran frozen bridging method on the full 20-min video: 2685 events, stable 124-139 per minute; no GT after 60 s, so counts only.
- Blind human verification on minutes 2-20: 20/20 predicted bounces real; 2/10 no-prediction clips contained a missed bounce.
- PROJECT_STATUS.md rewritten to reflect Phase 4. No E4, full-video inference or test-set tuning performed.

## Unreleased

- Recorded human reviewer sign-off for all 111 CVAT-reviewed detection images; prepared reviewed dataset with 336 valid class-0 boxes under `data/cvat_phase2_reviewed/final/`.
- Final QC found three val/test frames with 4 boxes; counts alone are not evidence of duplicates/false positives, and no boxes were removed automatically.
- Validated `data/detection/dataset.yaml` and temporal boundaries against `data/splits/split_manifest.csv`. Detection dataset is READY FOR FINE-TUNING; fine-tuning/Phase 3 has not started.
- Next step is manual 0–60 second bounce-event GT using `scripts/bounce_annotator.py`.

- Added configurable temporal sampling interval while preserving fixed train/validation/test intervals and exclusion buffers.
- Added Windows annotation workflow guide with CVAT/local YOLO review instructions and P2 checklist.
- Added annotation progress checker for reviewed/pending/rejected frames and verified/pending bounce events.
- Improved bounce annotator resume behavior and added tests for simultaneous events and empty labels.
- Verified CLI help and test suite: 6 tests passed.
- P2 remains blocked pending human box review, pilot annotation, second-pass review, and sign-off.
- No training, fine-tuning, full-video inference, or baseline modification performed.

- 2026-11-10: GT manual segmen 300-360 s & 900-960 s (135 event each); evaluation F1 0.985 (orig GT) / 1.00 (corrected GT). E2-blur trained (`E2_blur_cpu`): no measurable gain; final model stays E2. Report PDF rebuilt (23 pages).

- 2026-11-11: GT manual seluruh video (`gt_full_video.csv`, 2.702 tanda; total acuan 2.697 setelah koreksi -5). Pipeline 2.685: APE 0.44% (0.63% vs 2.702). Per event: 18 FN, 1 FP. Alat baru: `annotate_full.py`, `compare_full_count.py`; `make_error_clips.py --errors`. Laporan diperbarui (Bagian 6.5, 7, 8, 9, lampiran); 22->25 halaman. Koreksi GT 313 s (segmen 300-360) tidak didukung GT penuh: kemungkinan E2 menghitung satu bounce dua kali.

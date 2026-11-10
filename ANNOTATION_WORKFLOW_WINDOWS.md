# Phase 2 annotation workflow (Windows)

## Detection candidates

From PowerShell with the repository active:

```powershell
python scripts\sample_annotation_frames.py --interval-s 2
python scripts\annotation_progress.py
```

This samples only the existing train/validation/test temporal intervals. It never samples exclusion buffers. Candidate labels are generated from COCO `sports ball` (32) and written as dataset class `basketball` (0). They remain `candidate_unreviewed`.

Review options:

1. Open the images and labels in CVAT using the YOLO 1.1 importer, review every box, add missing boxes, remove false positives, and export YOLO 1.1.
2. Alternatively use a local image annotation tool that supports YOLO text labels. Preserve the original candidate directory and write reviewed labels to a versioned directory.

Never use test images to adjust model or detector thresholds. Test labels are held out for final evaluation only.

## Bounce pilot

```powershell
python scripts\bounce_annotator.py videofull.mp4 --start 0 --end 60 --output data\annotations\bounce_events_gt.csv
python scripts\annotation_progress.py
```

Controls: `Space` play/pause, `A`/left step backward, `D`/right step forward, `1` normal, `2` 2x, `4` 4x, `B` mark one event, `U` undo, `Q` save and quit. Press `B` once per ball contact; simultaneous balls therefore get separate rows. Coordinates may be left blank when not identifiable. Use `uncertain` for ambiguous events, then perform a second pass with model output hidden.

The CSV is saved after every mark/undo, so rerunning the same command resumes existing annotations. Do not mark `approved` until the second pass is complete.

## P2 pass checklist

- [ ] Every sampled image reviewed; labels approved/rejected and no blank candidate silently accepted.
- [ ] All boxes class 0 and within bounds.
- [ ] Temporal manifest has no overlap and buffers remain untouched.
- [ ] Pilot 0–60 s reviewed twice.
- [ ] Duplicate events removed; simultaneous contacts retained as separate events.
- [ ] `certain`/`probable`/`uncertain` decisions and reviewer recorded.
- [ ] Progress output shows zero pending frames and zero unreviewed pilot events.
- [ ] Reviewer sign-off recorded in `gt_review_log.csv`.

P2 is not PASS until these human actions are complete and the validators/tests pass.

## GT bounce untuk seluruh video (annotate_full.py)

```powershell
python scripts/annotate_full.py videofull.mp4            # anotasi; berhenti dengan q, lanjut dengan perintah yang sama
python scripts/compare_full_count.py                      # bandingkan dengan hitungan pipeline
```

- Tombol: spasi putar/jeda, **b** tandai, **u** batalkan, **r** mundur 3 s, **[ ]** lompat 10 s, **a/d** atau panah maju-mundur 1 frame, **1 2 3 4** kecepatan 0,25x 0,5x 1x 2x, **q** simpan dan keluar.
- Saat memutar, waktu tanda dikurangi `--lag-ms` (default 150 ms) untuk jeda reaksi; saat jeda, frame dicatat persis.
- Jangan melihat prediksi atau video overlay sebelum selesai. Anotasi berurutan dari awal; jangan lompat jauh dengan `]`, atau beri `--end` eksplisit saat membandingkan.
- `compare_full_count.py` memakai menit penuh yang sudah selesai ditonton. Hasil: total dan APE, tabel per menit, dan `errors.csv`. Perbandingan per event memakai koreksi jeda reaksi otomatis; total dan per menit tidak bergantung padanya.

# Project Status

_Last updated: 2026-11-03 (artifacts last modified 2026-10-16)_

## Current phase

Phase 4 — Bounce event detection (diagnostic stage). E4 and full-video processing have NOT started.

## Phase summary

| Phase | Scope | Status |
|---|---|---|
| 0 | CLI skeleton, configs, tests | Done |
| 1 | E1 baseline (YOLO26n pretrained) | Done (`artifacts/runs/E1_20261016_0025`) |
| 2 | Detection annotation (CVAT, 111 images, 336 boxes, signed off) | Done |
| 3 | E2 fine-tuning (CPU) + E1 vs E2 evaluation | Done |
| 4 | Bounce event detection (E2 baseline, E3-A/E3-B motion-first) | In progress; results poor, diagnosis unresolved |
| 5+ | Holdout validation, full video, report, demo | Not started |

## Results so far

Detection (test split, 18 images, 56 GT boxes):
- E1: P 0.81 / R 0.79 / F1 0.80, AP50 0.82
- E2: P 1.00 / R 0.96 / F1 0.98, AP50 0.96 (fine-tuning clearly helps)

Bounce events, first 60 s, tolerance 0.1 s:

| Experiment | GT | Pred | TP | FP | FN | P | R | F1 |
|---|---|---|---|---|---|---|---|---|
| E2 baseline, GT v1 (46 events) | 46 | 19 | 12 | 7 | 34 | - | - | - |
| E2 baseline, GT v2 (126 events) | 126 | 19 | 19 | 0 | 107 | 1.00 | 0.15 | 0.26 |
| E3-A motion, GT v1 | 46 | 265 | 17 | 248 | 29 | 0.06 | 0.37 | 0.11 |
| E3-B adaptive, GT v1 | 46 | 210 | 16 | 194 | 30 | 0.08 | 0.35 | 0.125 |
| E3-B adaptive, GT v2 | 126 | 210 | 28 | 182 | 98 | 0.13 | 0.22 | 0.17 |

Caution: v1 (46) and v2 (126) GT are different sets, so rows are not comparable across GT versions. Use GT v2 (`data/annotations/bounce_events_gt_v2.csv`) as the reference going forward. Motion-first E3 is worse than the E2 baseline in precision (many FP).

## Root cause: partly narrowed, still unresolved

Diagnostic pass 2026-11-03 (`scripts/phase4_diagnose.py`, output in `artifacts/runs/Phase4_diagnostics/`, see SUMMARY.md there):
- Detector absence is not dominant: for 105/107 E2 FN the detector fired and a tracked box exists within GT +/-3 frames. Only 2 FN lack a box.
- 15 FN have bottom_y <= 0.75H, so the baseline fixed floor-zone rule cannot fire (likely wrong for far-from-camera bounces).
- 76 FN have a tracked box but no down-then-up reversal in any track; 14 unclear or timing offset.
- Heuristic RCA ("105 tracking fragmentation") and the external review ("10/20 detector dropout") are both NOT supported as stated. Frames contain 2-3 balls and GT v2 has no contact coordinates, so a box near GT may be a different ball; multiple track IDs are not evidence of ID switching.
- External visual review (`Phase4_visual_review_results`) is AI-assisted, human sign-off PENDING.

Per-ball check (2026-11-04, 4 AI-proposed contact points, unverified): the raw detector sees the contact ball at conf ~0.8 in ~7 frames around contact, but the pilot tracker output keeps only 1-5 of them and changes track ID. Working hypothesis: ByteTrack IoU association loses the fast, blurred ball; raw-detection bridging is the candidate fix. Extended to 7 cases: raw conf>=.25 ball-frames near contact 31, tracked only 9 (29%). The 'floor-zone' FN (FN-14/20) look like the same dropout, not a bad threshold. Human verification still pending before building.

## Candidate fix result (2026-11-04)

`scripts/phase4_bridging.py` (raw E2 detections, distance-based association, lowest-point bounce rule; params chosen on 0-30 s only): HOLDOUT 30-60 s P 1.00 / R 1.00 / F1 1.00 (70/70, 0 FP); DEV 0-30 s F1 0.98. Baselines on the same segments: E2 F1 0.25-0.27, E3-B 0.16-0.18. Details and caveats: `artifacts/runs/Phase4_bridging/SUMMARY.md`. Caveats: single video/camera, fixed floor fraction, GT v2 has no second-pass review, only 0-60 s evaluated.

Full video (2026-11-04, `scripts/phase4_bridging_full.py`, frozen params, 36003 frames): 2685 events; per minute 124, 139, 137, 134, 134, 135, 135, 135, 133, 133, 136, 136, 134, 134, 133, 135, 136, 133, 133, 136. Stable ~135/min, in line with GT v2 (126 in minute 1). No GT after 60 s, so this is a count/consistency check, not accuracy. Files in `artifacts/runs/Phase4_bridging/` (`bridging_events_full.csv`, `full_video_report.json`).

Blind human check, minutes 2-20 (2026-11-04, 30 clips, human answers via `verify_clicker.py`): all 20 clips centred on predicted events were confirmed as real floor contacts (precision 20/20; 95% lower bound ~0.84). In 10 clips centred on random times with no prediction within +/-0.25 s, 2 contained a bounce (V02 at 989.1 s, V09 at 751.9 s), so some bounces are missed; recall not quantified. Small sample, single video.

## Open blockers

1. GT v2 lacks contact coordinates. Sample file `data/annotations/contact_points_sample.csv` has 4 AI-proposed points (FN-02/03/04/08); human verification and the remaining cases are still pending.
2. `visual_review_worksheet.csv` is still UNREVIEWED (human review needed).
3. FN-01 GT timing (~3.033 s) needs a human check on the original video.
4. The FP clips were NOT missing: `Phase4_visual_audit/Phase4_visual_audit_complete.zip` (23:19) holds 20 FN + 20 FP, all 31 frames and playable. The external review used the older 21:28 `Phase4_visual_audit.zip` (FN only).

## Next steps

1. Annotate contact coordinates for the sample, re-run the diagnostic on the nearest box only.
2. Then choose among floor-zone/FSM repair, detector recovery, or tracker changes.
3. Double-check GT v2 (second pass); then run the bridging method on the rest of the video (new unseen segments) before report and demo.

Constraints: keep GT v2, the E2 baseline and E3 outputs immutable; do not train or tune on the test set. E4 and full-video processing not started.

## Update 2026-11-10

- Manual GT on two new full-video segments (300-360 s, 900-960 s; 135 events each). E2 bridging, frozen params: 133 TP / 2 FP / 2 FN (F1 0.985) vs original GT, 135/0/0 after 4 GT corrections (corrections follow E2 predictions, so an upper bound).
- Motion-blur experiment (E2-blur, `artifacts/runs/E2_blur_cpu`): detector test AP50 0.974 vs 0.977, bounce results equivalent; E2 stays final.
- Report PDF (`laporan/laporan_final.pdf`, 23 pages) rebuilt with these results. Remaining: demo URL, GitHub/ZIP, final read-through.

## Update 2026-11-11

- Full-video manual GT (`data/annotations/gt_full_video.csv`, 2,702 marks; reference total 2,697 after the annotator removed 5, not identified per event). Pipeline 2,685: APE 0.44% (0.63% vs 2,702). Per event (+-0.2 s after lag offset): 18 FN, 1 FP, F1 ~0.9965 (approximate: reaction lag varies, cadence aliasing). Output: `artifacts/runs/Phase5_full_gt_eval/` (summary, per_minute, errors, clips).
- Independent full GT supports 3 of 4 earlier segment GT corrections; NOT the 313 s one (likely E2 double count). Open: causes of the 19 errors are undiagnosed; second-person review of GT.
- Report PDF rebuilt (25 pages) with these results. Remaining: demo URL, name/NIM, repo link.

## Housekeeping

- 2026-11-10: stray `nul` file deleted; `README.md` rewritten (setup, run commands, structure); `.gitignore` now excludes `*.mp4` and `*.zip`; report PDF built via `scripts/build_report_pdf.py` (`laporan/laporan_final.pdf`, demo URL still a placeholder).
- Phase 5 test video (`videotesting.mp4`, 162 s): frozen params gave 78 events, no GT yet (`artifacts/runs/Phase5_test_video/`).
- `data/cvat_phase2_reviewd` is a misspelled duplicate of `cvat_phase2_reviewed` (only zips; left untouched, delete manually if unwanted).
- Fine-tuned weights (`*.pt`) are gitignored; include `E2_finetuned_cpu/weights/best.pt` in the ZIP if submitting by ZIP.

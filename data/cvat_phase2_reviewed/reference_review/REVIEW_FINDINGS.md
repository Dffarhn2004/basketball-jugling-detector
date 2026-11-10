# Phase 2 — External Visual Review Findings (AI-assisted)

**Source:** `phase2_review_package.zip` supplied in this conversation. Review artifacts are separate; originals are not overwritten.  
**Status:** **AI-assisted visual triage only, NOT human sign-off. P2 remains BLOCKED.**  
**Scope:** dataset structure and CSVs; all 24 empty-label images; 30-frame E1 contact sheet; representative nonempty examples including anomalous boxes; original `clip_60s.mp4` inspected for entry context. **The complete 60 s event-by-event bounce ground truth has NOT been produced.**

## 1. Verified technical checks

- Sampled images: **111**; splits train=75, val=18, test=18.
- Candidate boxes: **143**, in **87** frames; empty candidate files: **24**.
- Candidate counts per image: **{0: 24, 1: 42, 2: 35, 3: 9, 4: 1}**.
- YOLO `.txt` candidate rows: **143**; malformed/mismatched pair checks: **0** of 111. All inspected image dimensions are 1280×720. This verifies **syntax/consistency**, not semantic correctness.
- Temporal sample ranges: train includes beginning and end of video; val 635–805 s; test 845–1015 s. The original **`split_manifest.csv` is absent** from the supplied ZIP: validate planned interval boundaries and 30s exclusion buffers in source repo before claiming full split gate.
- E1 source contact sheet has 30 sampled frames at 2-second interval, corresponding `detections_tracks.csv` and two videos. Tracking data alone is not a verified event detection result.
- `clip_60s.mp4` contains a video track but **no audio track**, so audio bounce validation is not possible on this clip.

## 2. Critical: 24/24 visually checked empty labels are WRONG as no-object examples

Every empty-labeled sampled image visibly contains **three basketballs**. This is not a true background-only frame. See `dataset_review_queue.csv` for the 24 exact frame IDs, timestamps, and splits.

**Impact:** If trained as empty/no-object images, these examples could teach the detector to suppress real basketball detections. **Do not train yet.** A correct annotation requires drawing boxes for all identifiable basketballs and verifying every frame. The same concern affects partially labeled frames: 42 images have 1 candidate and 35 images have 2 candidates, often while three balls are visible.

## 3. Other visual annotation errors (examples)

| Timestamp | Issue | Evidence / action |
|---:|---|---|
| 175 s | Duplicate lower ball | 2 candidate boxes overlap same lower ball; middle ball missing; visually correct all three |
| 585 s | Duplicate lower ball | Both boxes cover lower ball; two upper balls missing |
| 775 s | Spurious floor box | Small box over background at floor, not a ball |
| 865 s | Duplicate + floor artifact | 4 predicted boxes are NOT four balls; one duplicate and one small floor artifact; center ball missed |
| 1075 s | Spurious floor box | Small false-positive rectangle near floor, while one real ball missing |

3 source frames have candidate overlaps IoU >0.5 (175/585/865 s). High IoU alone is only an **automatic suspicion**: here the boxes were also inspected visually. See `specific_correction_issues.csv` for row-by-row corrective suggestions. DO NOT silently NMS all overlapping GT annotations: two genuinely overlapping basketballs may require separate boxes.

## 4. E1 pretrained contact-sheet triage

- At 0 and 2 s, scene appears empty (no balls visible).
- At 4 s, player/balls partly enter the camera field; uncertain visible count.
- At 6 s, two balls are clearly visible.
- From 8 to 58 s at the 2-second sample instants, three basketballs are visible but detections are frequently missing.
- The E1 sample has 144 unique track IDs in the 60 s CSV, which indicates substantial fragmentation **but is not a verified ID-switch count**.
- The initial 771 detections / 1800 frames is not precision or recall. E1 source CSV should remain frozen.

See `baseline_contact_sheet_ai_review.csv`; these are **initial visual estimates** pending independent human verification, not entries to paste directly as approved manual audit.

## 5. Prioritized human work to unblock P2

1. Start with the 24 priority **P0** empty-labeled images. Manually add every ball. Then resolve the 5 P0 anomaly frames.
2. Manually check all remaining frames, including supposedly correct 3-box frames. Reject duplicate and false-positive boxes, mark genuinely absent/occluded objects carefully.
3. Validate all 111 frames after corrections; then decide whether to expand to 400–600 if needed. If expanded, **never random-mix adjacent video times between splits**.
4. Manually annotate all floor-contact events on 60s pilot, with frame stepping and two verification passes; record multiple simultaneous contacts separately.
5. User or named real human reviewer signs off. An AI visual inspection is **not** a substitute for the specified human review.
6. Run dataset QC and annotation progress on corrected data; only when the gate is verified should Phase 3 start.

## 6. What this review does not establish

- No accepted ground truth, detector recall, precision, mAP, event F1, true bounce count, or verified ID-switch count.
- No precise corrected YOLO bounding boxes for all three balls. Existing labels were left untouched.
- No full-video GT: only a 60-second clip is provided here.
- No test-set tuning; the test examples were inspected **only for dataset annotation quality**. For strict blind performance analysis, use a separately held-out test segment in future.

## 7. Research story this evidence supports

**Pretrained detector produces incomplete and sometimes false basketball candidates → correct human annotations are required → fine-tune on verified samples → compare E1 vs E2 on same frozen evaluation and pipeline settings → evaluate final bounce events only against independently verified timestamp GT.**

Do **not** assume E2 will improve without measured comparisons.

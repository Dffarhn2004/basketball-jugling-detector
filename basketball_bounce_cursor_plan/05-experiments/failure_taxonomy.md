# Failure Taxonomy — For Every FP / FN

## Primary category (exactly one per case)
- `detector_miss`: bola tidak ditemukan pada frame penting.
- `false_detection`: bukan bola dianggap bola.
- `motion_blur`: bola blur menyebabkan lokalisasi/tracking buruk.
- `occlusion`: tertutup pemain/bola lain.
- `id_switch`: ID berubah dan kejadian terganggu.
- `track_fragmentation`: track terputus dalam fase bounce.
- `floor_geometry_error`: floor band salah pada lokasi tersebut.
- `hand_catch_false_positive`: gerak tangan dianggap pantulan.
- `velocity_smoothing_error`: reversal hilang/bergeser setelah filter.
- `event_threshold_error`: threshold terlalu ketat/longgar.
- `duplicate_count`: satu kontak dihitung >1.
- `simultaneous_event_merge`: dua kontak digabung satu.
- `timestamp_misalignment`: waktu frame/PTS tidak cocok.
- `annotation_ambiguity`: GT masih uncertain; butuh adjudication.
- `other`: wajib dilengkapi sebab spesifik.

## Secondary tags (0..n)
Contoh `low_confidence`, `ball_near_edge`, `low_resolution`, `two_balls_overlap`, `bad_light`.

## Case record
- `case_id`, `run_id`, `FP/FN`, GT event/pred event ID, timestamp absolute, ±3s clip path.
- `primary_cause`, `secondary_tags`, `evidence_frame_paths`, `why_failed`, `possible_fix`, `reviewed_by`, `review_status`.

## Audit level of evidence
1. Inspect saved detections raw.
2. Inspect tracks near timestamp.
3. Inspect trajectory plotted and floor contact threshold.
4. Confirm final state transitions and dedup.
5. Assign proximate primary failure, distinguish root vs symptom.

## Contoh penjelasan yang sah
"Pada `00:01:23.200`, satu bola tertutup tangan selama lima frame sehingga tracker kehilangan observasi; state machine tidak melihat gerakan naik dan tidak mengeluarkan event (FN)." **Gunakan hanya setelah video benar-benar membuktikannya.**

## Larangan
Jangan menulis “akibat motion blur” untuk setiap failure tanpa inspeksi. Jangan hanya melaporkan lima contoh jika masih ada 200 error; soal meminta penandaan **setiap** miss/overcount.

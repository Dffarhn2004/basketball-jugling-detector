# Exhaustive Error Audit Playbook

## Audit automation
1. `evaluate` menghasilkan one-to-one matching.
2. Simpan setiap unmatched GT sebagai FN, setiap unmatched pred sebagai FP.
3. Auto-cut clip ±1–3 detik untuk setiap kasus (handle boundaries video).
4. Auto-plot trajectory y/t + bbox + floor threshold bila memungkinkan.
5. Buat `audit_queue.csv` terurut berdasarkan timestamp.
6. Human reviewer klasifikasi **semua** kasus, bukan hanya sampled errors.

## Required columns
`case_id,type,run_id,event_id,absolute_time_s,hhmmss,segment_id,clip_path,primary_cause,secondary_tags,evidence,possible_fix,review_status`.

## Coverage assurance
- `n_reviewed_FP == FP_count`.
- `n_reviewed_FN == FN_count`.
- Semua valid mismatch dievaluasi di seluruh interval yang diklaim.
- Human correction pada GT harus versioned; setelah revisi, rerun matching metrics pada versi GT baru.

## Grouping, not omission
Untuk laporan utama, boleh kelompokkan kegagalan berdasarkan kategori + tabel timestamp lengkap di appendix/CSV supplemental. Jangan hanya menampilkan contoh representatif jika soal minta **setiap** case diidentifikasi.

## Example use cases
- FN: bola blur lalu tracker kehilangan ID -> catat frame before/after.
- FP: tangan menangkap bola dekat lantai -> jelaskan floor-band ambiguity.
- FP: ID-switch melahirkan 2 kandidat duplikat -> evaluasi spatial-temporal dedup.
- FN: 2 bola kontak bersamaan lalu event merge -> uji dedup radius.

## Re-review setelah tweak
- Jangan retune berdasarkan **test** errors, kecuali menyatakan eksperimen sebagai post-hoc dan menyiapkan holdout baru untuk validasi.
- Jika hanya memperbaiki bug fatal, dokumentasikan bugfix dan rerun seluruh experiments dari checkpoint frozen.

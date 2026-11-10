# Cursor — Mulai Kerjakan Proyek

## Cara penggunaan

1. Ekstrak folder ZIP ke root proyek baru / repo.
2. Buka folder tersebut di Cursor.
3. Pastikan Cursor bisa melihat `AGENTS.md` dan seluruh direktori dokumentasi.
4. Kirim **prompt pembuka** di bawah ke Cursor Agent.
5. Setelah Phase 0 beres, lanjut prompt Phase 1; jangan lompat ke fine-tuning sebelum baseline disimpan.

## Prompt pembuka (copy paste)

> Baca `AGENTS.md`, `README.md`, `00-brief/assignment_requirements.md`, `01-planning/roadmap_4_weeks.md`, `01-planning/milestones_and_gates.md`, `06-engineering/repo_structure.md`, dan `08-cursor/phase_0_prompt.md`. Implementasikan **hanya Phase 0** secara bertahap. Bangun skeleton project Python yang rapi, konfigurasi, environment validation, unit-test scaffolding, README teknis, dan CLI stub. Jangan download/latih model tanpa persetujuanku. Jangan mengarang hasil. Update `PROJECT_STATUS.md` beserta tes aktual dan next step.

## Prinsip menjalankan fase

`Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5`

Ada loop iterasi saat masalah terdeteksi, tetapi baseline yang disimpan tidak boleh diubah/dihapus.

## Prompt lanjutan

Lihat folder `08-cursor/`:
- `phase_0_prompt.md` — scaffolding.
- `phase_1_prompt.md` — video, pretrained, baseline.
- `phase_2_prompt.md` — dataset, anotasi, ground truth.
- `phase_3_prompt.md` — fine-tuning.
- `phase_4_prompt.md` — tracking + event counter.
- `phase_5_prompt.md` — experiments, video demo, report.
- `bugfix_prompt.md` — debug tanpa merusak reproducibility.

## Verifikasi bahwa Cursor memahami tugas

Minta Cursor menjelaskan:
- Apa **event bounce** yang dihitung?
- Mengapa E1 harus disimpan sebelum E2?
- Bagaimana split dataset menghindari data leakage?
- Mengapa `accuracy jumlah` saja dapat menipu?
- Bagaimana menandai setiap FP/FN dengan timestamp?
- Apa beda fine-tuning weight detector vs tuning threshold?

Jika jawabannya tidak jelas, suruh Cursor membaca ulang dokumentasi terkait.

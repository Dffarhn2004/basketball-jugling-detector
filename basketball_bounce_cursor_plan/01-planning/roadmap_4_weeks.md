# Roadmap 4 Pekan sampai 14 November 2026

Tanggal pada tabel adalah **target internal**, bukan jadwal dari dosen.

| Periode | Fokus | Output wajib | Risiko |
|---|---|---|---|
| 15–21 Okt | P0 + P1: setup, video, baseline | metadata video, pretrained output dan samples, executable CLI | akses file video |
| 22–28 Okt | P2: GT dan anotasi | split temporal, anotasi object, manual event GT + review plan | beban anotasi |
| 29 Okt–4 Nov | P3: fine-tuning & validation | best checkpoint + training config/log | komputasi/overfitting |
| 5–10 Nov | P4: state machine, tests & P5 experiments | count CSV, E1/E2/E3 eval, errors CSV | event FP/FN |
| 11–13 Nov | report + demo + submission QA | PDF, annotated MP4, code repository | audit error lengkap |
| 14 Nov | deadline | semua tautan dan artefak dapat diakses | keterlambatan |

## Critical path

`file video sah → event ground truth manual → pretrained snapshot → fine-tuning → event detector → frozen evaluation → failure analysis → report & demo`

**Ground truth manual adalah pekerjaan terbesar.** Mulai protokol anotasi lebih awal walaupun pelabelan lengkap dilakukan di fase 2.

## Strategi agar tugas tidak melebar

1. Target pertama: output 30–60 detik dengan tiga bbox, ID, penghitung bounce.
2. Output baseline E1 sebelum training. Simpan konfigurasi + predictions yang bisa dianalisis.
3. Training hanya satu bobot utama + satu/two run tuning yang relevan.
4. Evaluasi test memakai standar tetap; hindari random split frame.
5. Seluruh video dijalankan setelah pipeline stabil. Laporkan jika kualitas penuh lebih buruk daripada test.

## Jika waktu mepet

- Tetap prioritaskan memenuhi **semua requirement dosen**, terutama manual GT dan audit setiap miss/over-count.
- Pangkas UI, refactor berlebihan, perbandingan 4+ model, dashboard, cluster training, deployment.
- Gunakan E1/E2 utama; E3 hanya jika cukup waktu, namun tulis alasan apabila dibatalkan.
- Jangan menghapus error cases untuk membuat hasil terlihat sempurna.

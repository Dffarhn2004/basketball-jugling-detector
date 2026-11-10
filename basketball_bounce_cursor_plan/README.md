# The Juggling Bounces Challenge — Cursor Project Pack

> **Proyek:** Deep Learning for Dynamic Event Detection (S2)  
> **Video:** https://www.youtube.com/watch?v=oWqwY1MLBck  
> **Deadline dari soal:** 14 November 2026  
> **Status:** Planning package, belum ada eksperimen yang dijalankan  
> **Arsitektur utama:** `YOLO26n pretrained → ByteTrack → physics-aware state machine` dibandingkan dengan `YOLO26n fine-tuned → pipeline identik`, kemudian optimasi pipeline.

## Mulai di sini

1. Baca [`AGENTS.md`](AGENTS.md) — instruksi paling penting untuk Cursor/agent.
2. Baca [`CURSOR_START_HERE.md`](CURSOR_START_HERE.md) — perintah pembuka dan alur kerja.
3. Baca [`00-brief/assignment_requirements.md`](00-brief/assignment_requirements.md) — kewajiban asli dari PDF.
4. Baca [`01-planning/roadmap_4_weeks.md`](01-planning/roadmap_4_weeks.md) dan [`01-planning/task_backlog.md`](01-planning/task_backlog.md).
5. Jalankan instruksi fase demi fase dari [`08-cursor/`](08-cursor/README.md).

## Goal akhir

Hitung **seluruh kejadian bola basket menyentuh lantai** dalam video yang diberikan, mencakup ketiga bola dan kejadian simultan, dengan:
- CSV ground truth manual dan aturan anotasi yang eksplisit.
- Baseline pretrained yang tersimpan **sebelum fine-tuning**.
- Model detector hasil fine-tuning dan riwayat eksperimen yang bisa direproduksi.
- Tracking, timestamp bounce, count akhir, dan video anotasi.
- Evaluasi event-level (TP, FP, FN, precision, recall, F1), error jumlah, serta audit seluruh kesalahan.
- PDF laporan; tautan video demo Unlisted; repo source code / ZIP.

## Perbedaan yang wajib dipahami

| Tahap | Bobot dilatih? | Boleh mengklaim fine-tuning model? |
|---|---:|---|
| E1: pretrained YOLO26n | Tidak | Tidak |
| E2: fine-tuned YOLO26n | Ya | Ya, untuk detector |
| E3: E2 + tuning tracker/event | Tidak untuk YOLO tambahan | Tidak; ini tuning parameter pipeline |

Tidak boleh menyebut state machine atau ByteTrack sebagai jaringan deep learning yang dilatih khusus, kecuali benar-benar ada training yang terdokumentasi.

## Paket ini berisi apa?

**Dokumentasi Markdown dan aturan kerja** untuk membimbing Cursor **membangun** kode. Paket ZIP ini bukan implementasi siap jalan dan tidak mengandung dataset, video, model weight, atau hasil training. Semua hasil yang belum diketahui ditandai `TBD`, **bukan angka rekaan**.

## Prinsip pengerjaan

- *Keep it simple, measure it rigorously.*
- Gunakan satu detector kecil + satu tracker + state machine yang dapat dijelaskan.
- Berhenti pada setiap quality gate jika hasil belum valid; lakukan debugging berbasis bukti.
- Pisahkan train, validation, dan test secara temporal.
- Video penuh harus dihitung; evaluasi pada test bersih dilaporkan terpisah dari hasil pada seluruh video.
- Jangan menjadikan angka ≈3.200 dari deskripsi video sebagai ground truth.

## Navigasi dokumen

- `00-brief/`: tugas, tujuan, risiko, keputusan arsitektur.
- `01-planning/`: sprint, milestone, backlog, acceptance criteria.
- `02-data/`: video, anotasi frame, event, ground truth, split.
- `03-model/`: pretrained, training, augmentasi, inferensi.
- `04-pipeline/`: tracking, kontak lantai, state machine, dedup, overlay.
- `05-experiments/`: metrik, ablation, failure analysis, tabel.
- `06-engineering/`: struktur kode, CLI, testing, environment, commands.
- `07-deliverables/`: laporan, demo, README, submission.
- `08-cursor/`: prompt siap pakai per fase.
- `09-references/`: tautan resmi, glosarium, FAQ.
- `10-templates/`: pencatatan run/eksperimen/error/review.

**Sumber utama:** `Tugas 1 - Deep Learning (S2 - B).pdf` yang diberikan pengguna, dua halaman. Semua saran arsitektur dan metodologi adalah rencana implementasi (bukan instruksi wajib dari dosen).

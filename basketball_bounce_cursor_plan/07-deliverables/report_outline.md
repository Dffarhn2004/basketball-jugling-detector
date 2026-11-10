# Blueprint laporan teknis PDF

**Wajib letakkan tautan video demonstrasi aktif di halaman pertama / atas laporan**, bukan hanya lampiran.

## Cover
- Judul, nama/NIM, kelas, tanggal, git commit hash model & kode yang dipakai.
- Demonstration video URL (Unlisted/Drive/LMS) dan source repo URL.

## Abstract
- Problem, data, metode, desain pembandingan E1/E2/E3, hasil **aktual**, keterbatasan.
- Tulis belakangan setelah evaluasi final. Jangan mengarang statistik.

## 1. Introduction & Problem Definition
- Tantangan tiga bola simultan, bounce sebagai floor-contact event, bukan klasifikasi frame saja.
- Ruang lingkup video tunggal, tantangan blur/occlusion, definisi event dan sumber ground truth.
- Research questions dan contribution claims yang bisa diuji.

## 2. Related Work & Architecture
- Peran YOLO26n sebagai object detector, ByteTrack sebagai MOT, state machine sebagai event analyzer.
- Bandingkan singkat TrackNet/RT-DETR/temporal CNN; alasan tetap memilih arsitektur sederhana.
- Diagram pipeline; tradeoffs speed, precision, task suitability.
- Nyatakan tidak melatih ByteTrack / state machine.

## 3. Dataset & Ground Truth
- Sumber video, FPS/timebase, resolution, jumlah frame, durasi aktual, checksum.
- Anotasi detection bbox vs anotasi bounce event sebagai dua artefak berbeda.
- Data sampling, split berdasarkan interval waktu, temporal exclusion buffer dan QC.
- Number of GT bounce events dalam video **hanya setelah label selesai**.

## 4. Training & Fine-Tuning
- Baseline pretrained tanpa update bobot.
- Bobot awal, environment, hardware, optimizer, batch, image size, epoch, seed, augmentasi, best checkpoint.
- mAP, precision, recall pada split validation/test; learning curves bila ada.
- Aturan model selection tanpa test leakage.

## 5. Tracking & Event Detection
- Detector output format; ByteTrack confidence & tracking buffer.
- Konversi koordinat bola bottom-center, smoothing, floor reference (line/ROI atau perspektif), velocity signs.
- Finite state machine FALLING→CONTACT_CANDIDATE→RISING→COUNTED.
- Hysteresis, dedup frame, simultaneous balls, ID fragmentation, video annotation.
- Pseudocode dan contoh konkret valid vs invalid bounce.

## 6. Experiments
- E1 pretrained/default, E2 fine-tuned/same params, E3 fine-tuned/optimized via validation.
- Tabel detector mAP, event TP/FP/FN/Precision/Recall/F1, count error, APE, runtime.
- Bandingkan **segmen holdout test** secara adil; laporkan **video penuh** secara terpisah.
- Jelaskan E2 bisa saja tidak mengungguli E1: interpretasi tidak dimanipulasi.

## 7. Failure Analysis (wajib per kesalahan)
- Daftar **setiap** FP/FN ber-timestamp pada cakupan evaluasi; untuk tugas video penuh audit seluruh mismatch video penuh.
- Kategori penyebab: blur, occlusion, ID switch, hand catch, floor ROI, temporal misalignment, duplicate.
- Thumbnail/gambar contoh + caption, failure table lengkap sebagai appendix jika panjang.
- Perbaikan prospektif; bedakan yang diuji vs yang hanya diusulkan.

## 8. Discussion, Limitations, Conclusion
- Jawab research questions dengan data nyata.
- Generalisasi satu video terbatas; anotasi manual memakan waktu; margin error dan FPS.
- Temuan dan next experiments minimal (bukan janji generik).

## References & Appendices
- Perangkat lunak, paper model, URL resmi dan tanggal akses.
- Full parameter configs, split manifest, raw events, matching tolerances, failure audit table.

## QA laporan
- [ ] Seluruh angka traceable ke `runs/*` (ada path + hash).
- [ ] Laporan jelas membedakan training detector vs tuning parameter.
- [ ] Link demo bekerja tanpa login privat yang menghalangi dosen.
- [ ] Tidak ada estimasi 3.200 dianggap sebagai ground truth.

# Decision Log / Architecture Decision Records

## ADR-001 — Fokus simplicity-first
**Status:** Accepted (planning)  
**Pilihan:** Satu detector pretrained/fine-tuned, ByteTrack, finite-state machine.  
**Alasan:** Lebih cepat dituntaskan, dapat dianalisis kesalahannya, dan memenuhi tugas training deep learning.  
**Ditolak sementara:** Multi-model ensemble, TCN, LSTM, Transformer video, tracking multi-camera, realtime service.

## ADR-002 — YOLO26n sebagai detector
**Status:** Provisional, validasi package/weights saat environment setup.  
**Alasan:** Model kecil, pretrained tersedia menurut dokumentasi Ultralytics; API training dan tracking seragam.  
**Risiko:** Bola blur, ID-switch, incomplete detections.  
**Fallback:** Model nano stabil yang tersedia jika versi terpasang tidak mendukung, didokumentasikan dengan alasan dan versi, tanpa mengubah tujuan eksperimen.

## ADR-003 — Ground truth manual
**Status:** Accepted.  
**Alasan:** Ini persyaratan eksplisit soal. Tidak boleh mengganti dengan estimasi deskripsi YouTube atau otomatisasi tanpa audit.

## ADR-004 — Temporal split
**Status:** Accepted.  
**Alasan:** Frame berdekatan sangat mirip; random frame split mencemari evaluasi. Evaluasi test harus pada rentang waktu yang tidak dipakai tuning.

## ADR-005 — Perbandingan E1, E2, E3
**Status:** Accepted.  
**Alasan:** Membuktikan dampak fine-tuning detector dan optimasi pipeline secara terpisah.

## ADR-006 — Tidak memaksa live/realtime
**Status:** Accepted.  
**Alasan:** Soal meminta processed output video dan count, bukan streaming realtime. Offline processing memungkinkan lookahead beberapa frame.

## ADR-007 — Scope video
**Status:** Accepted.  
**Aturan:** Hitung frame yang benar-benar tersedia di rekaman. Klaim pencipta video tentang percobaan lebih panjang bukan truth untuk rekaman.

## Proses perubahan ADR

Sebelum mengganti model/arsitektur: catat:
1. Masalah konkret yang dibuktikan metrik.
2. Alternatif yang dievaluasi.
3. Trade-off compute, anotasi, waktu, akurasi.
4. Keputusan dan konsekuensi ke eksperimen lama.

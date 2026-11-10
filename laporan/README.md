# The Juggling Bounces Challenge — Laporan Proyek (daftar isi)

**Menghitung otomatis berapa kali bola basket menyentuh lantai pada video juggling 20 menit, dengan pipeline deep learning (deteksi, tracking, deteksi event temporal).**

Mata kuliah Deep Learning (S2). Tenggat tugas: 14 November 2026.
**Laporan akhir:** [`laporan_final.pdf`](laporan_final.pdf), dibangun dari [`laporan_final.md`](laporan_final.md) dengan `python scripts/build_report_pdf.py "<url-video-demo>"`.
File per bagian di bawah adalah catatan kerja rinci dan bisa tertinggal dari laporan akhir; jika berbeda, `laporan_final.md` yang berlaku.

---

## Daftar isi (satu file per bagian)

1. [Ringkasan](00_ringkasan.md)
2. [1. Analisis Masalah dan Arsitektur](01_analisis_masalah_dan_arsitektur.md)
3. [2. Data dan Strategi Training](02_data_dan_strategi_training.md)
4. [3. Anotasi Event Bounce (Ground Truth)](03_anotasi_event_bounce_ground_truth.md)
5. [4. Eksperimen Detector: E1 vs E2](04_eksperimen_detector_e1_vs_e2.md)
6. [5. Rekayasa Pipeline: dari Deteksi ke Hitungan](05_rekayasa_pipeline_dari_deteksi_ke_hitungan.md)
7. [6. Hasil Kuantitatif](06_hasil_kuantitatif.md)
8. [7. Analisis Kegagalan](07_analisis_kegagalan.md)
9. [8. Mengapa Metode Ini Bekerja, dan Apa Batasnya](08_mengapa_metode_ini_bekerja_dan_apa_batasnya.md)
10. [9. Integritas Eksperimen dan Kemungkinan Bias](09_integritas_eksperimen_dan_kemungkinan_bias.md)
11. [10. Kesimpulan](10_kesimpulan.md)
12. [11. Kesesuaian dengan Ketentuan Tugas dan Celah yang Tersisa](11_kesesuaian_dengan_tugas_dan_celah.md)
13. [Lampiran A — Cara Mereproduksi](lampiran_a_cara_mereproduksi.md)
14. [Lampiran B — Peta Berkas](lampiran_b_peta_berkas.md)

Gambar ada di `gambar/`. Cerita utamanya mengalir dari ringkasan lalu bagian 1 ke 10; bagian 11 memeriksa kesesuaian dengan soal; lampiran berisi cara reproduksi dan peta berkas.

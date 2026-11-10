> The Juggling Bounces Challenge, laporan proyek. Bagian ini berdiri sendiri; lihat [README.md](README.md) untuk urutan.

## 11. Kesesuaian dengan Ketentuan Tugas dan Celah yang Tersisa

| Tuntutan tugas | Status | Catatan |
|---|---|---|
| 1. Analisis masalah dan arsitektur | Terpenuhi | Bagian 1 |
| 2. Strategi data dan training (termasuk augmentasi motion blur) | Terpenuhi, dengan catatan | Bagian 2; augmentasi motion blur diuji lewat model pembanding E2-blur (Bagian 2.4, 6.2). Blur kasar (seluruh gambar) dan tidak memberi keuntungan terukur, sehingga model akhir tetap E2 |
| 3. Rekayasa pipeline (centroid tracking, deteksi puncak, menolak tangkapan tangan) | Terpenuhi | Bagian 5.4 |
| 4. Performa kuantitatif: GT manual untuk video, bandingkan prediksi, hitung error/APE | **Sebagian** | GT manual pada tiga segmen (0–60, 300–360, 900–960 s; sekitar 4 dari 20 menit): APE 1,6% pada 0–60 s dan 0% pada dua segmen lain (dengan catatan koreksi GT, Bagian 6.2 dan 9); seluruh 20 menit belum punya hitungan manual |
| 5. Analisis kegagalan per timestamp | Sebagian | Lengkap untuk tiga segmen ber-GT (Bagian 7); di luar itu hanya dua miss terverifikasi |
| Format laporan PDF | Belum | Dokumen ini berbentuk Markdown, perlu dikonversi |


---
[< 10. Kesimpulan](10_kesimpulan.md) | [ Lampiran A — Cara Mereproduksi >](lampiran_a_cara_mereproduksi.md) | [Daftar isi](README.md)

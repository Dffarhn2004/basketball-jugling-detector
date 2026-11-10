> The Juggling Bounces Challenge, laporan proyek. Bagian ini berdiri sendiri; lihat [README.md](README.md) untuk urutan.

## Ringkasan

Tugas ini meminta pipeline yang menghitung total sentuhan bola ke lantai pada video seorang pria yang menjuggling tiga bola basket. Masalahnya kami pecah menjadi tiga tahap: **lokalisasi bola** (detector YOLO26n yang di-fine-tune), **tracking** (menyambung deteksi antar frame), dan **deteksi event** (menentukan frame saat bola menyentuh lantai).

Hasil utama:

- **Detector.** Fine-tuning pada 111 gambar yang kami anotasi sendiri menaikkan F1 pada set test dari 0,80 (YOLO26n pretrained) menjadi 0,98.
- **Event bounce.** Pendekatan pertama (E2 + ByteTrack + aturan gerak) hanya menemukan 19 dari 126 bounce ground truth (recall 0,15). Pendekatan gerak murni (E3) menghasilkan ratusan false positive (F1 sekitar 0,17).
- **Penyebab.** Dugaan awal kami (fragmentasi ID tracker, detector gagal) ternyata keliru atau belum terbukti. Setelah diperiksa dengan deteksi mentah, detector sebenarnya melihat bola kontak, tetapi **tracker berbasis IoU membuang sebagian besar deteksi itu** karena bola bergerak cepat dan blur.
- **Perbaikan.** Penyambungan deteksi mentah berdasarkan jarak posisi, plus aturan titik terendah lintasan. Dengan parameter yang dipilih hanya dari detik 0–30, hasilnya F1 1,00 pada detik 30–60 (70 dari 70 bounce, 0 false positive).
- **Dua segmen GT tambahan.** Pada 300–360 s dan 900–960 s (135 event masing-masing), parameter beku memberi F1 0,985 dengan GT asli; setelah empat selisih diperiksa dan GT dikoreksi, F1 1,00. Skor setelah koreksi adalah batas atas karena koreksinya searah dengan prediksi (Bagian 6.2 dan 9).
- **Augmentasi motion blur.** Model pembanding E2-blur (set latih ditambah salinan berblur) tidak memberi perbedaan yang dapat dibuktikan, baik pada detector (AP50 0,974 vs 0,977) maupun pada hitungan bounce; pipeline akhir tetap memakai E2 (Bagian 2.4 dan 6.2).
- **Seluruh video.** Metode ini menghitung **2.685 bounce** pada 20 menit, stabil sekitar 135 per menit. Verifikasi buta oleh manusia pada 30 klip: 20 dari 20 bounce yang diklaim benar, 2 dari 10 klip acak tanpa klaim ternyata memuat bounce yang terlewat.

Keterbatasan penting: satu video, satu kamera, ground truth manual mencakup tiga segmen 60 detik (0–60, 300–360, 900–960 s; sekitar 4 dari 20 menit), dan 2.685 belum dibandingkan dengan hitungan manual seluruh video (Bagian 11).


---
[ 1. Analisis Masalah dan Arsitektur >](01_analisis_masalah_dan_arsitektur.md) | [Daftar isi](README.md)

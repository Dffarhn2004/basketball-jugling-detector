> The Juggling Bounces Challenge, laporan proyek. Bagian ini berdiri sendiri; lihat [README.md](README.md) untuk urutan.

## 3. Anotasi Event Bounce (Ground Truth)

- Event bounce **tidak** dianotasi di CVAT. Kami menandai waktu kontak dengan alat `scripts/bounce_annotator.py`, lalu menyimpannya di `data/annotations/`.
- **GT v1:** 46 event (anotasi awal, tidak lengkap). **GT v2:** 126 event pada detik 0–60, semua berstatus `approved`.
- GT v1 dan v2 adalah himpunan yang berbeda, sehingga metrik yang dihitung pada keduanya **tidak sebanding**. Semua evaluasi akhir memakai GT v2.
- Kecocokan prediksi dengan GT dihitung **satu-ke-satu** dengan toleransi **±0,1 detik** (±3 frame).
- **GT segmen tambahan (video penuh, anotasi manual terpisah):** dua segmen 60 detik di luar 0–60 detik, yaitu **300–360 s** (`gt_segment_300_360.csv`, 135 event) dan **900–960 s** (`gt_segment_900_960.csv`, 135 event). Keduanya dianotasi tanpa melihat prediksi model, memakai alat dan aturan yang sama (frame kontak pertama bola dengan lantai; waktu = frame ÷ 30).
- **Koreksi GT setelah membandingkan dengan prediksi.** Pada perbandingan awal, selisih GT dan prediksi diperiksa lewat klip lambat (0,25x). Pada semua selisih yang diperiksa (2 kasus di segmen 300–360 dan 2 kasus di segmen 900–960), penulis menilai GT-nya yang keliru dan prediksi yang benar, lalu GT dikoreksi: satu event digeser dan satu event dipecah menjadi dua di 300–360, serta dua event digeser di 900–960. Berkas asli disimpan sebagai `*.backup-before-correction.csv`. Koreksi hanya dilakukan di titik yang berbeda; event yang cocok tidak diperiksa ulang. Karena frame koreksi diambil dari frame prediksi, skor "setelah koreksi" bukan ukuran independen (lihat Bagian 6.2 dan 9).
- GT v2 belum melalui pemeriksaan kedua (`gt_review_log.csv` mencatat pass A/B `not_started`). Dua event (GT-0041 dan GT-0042) berjarak hanya 1 frame (0,033 detik) dan kemungkinan satu bounce yang tercatat dua kali.


---
[< 2. Data dan Strategi Training](02_data_dan_strategi_training.md) | [ 4. Eksperimen Detector: E1 vs E2 >](04_eksperimen_detector_e1_vs_e2.md) | [Daftar isi](README.md)

> The Juggling Bounces Challenge, laporan proyek. Bagian ini berdiri sendiri; lihat [README.md](README.md) untuk urutan.

## Lampiran A — Cara Mereproduksi

Semua perintah dijalankan dari folder proyek; deteksi mentah disimpan agar tahap-tahap setelahnya cepat.

```
# Evaluasi detector E1 vs E2
python scripts/evaluate_e1_e2.py

# Diagnostik penyebab kegagalan (deteksi mentah di sekitar frame GT)
python scripts/phase4_diagnose.py

# Metode akhir pada 0-60 detik (membuat raw_0_60s.csv lalu mengevaluasi)
python scripts/phase4_bridging.py

# Seluruh video (deteksi frame 1800 sampai akhir, lalu event)
python scripts/phase4_bridging_full.py

# Model pembanding dengan augmentasi motion blur
python scripts/make_blur_dataset.py
python scripts/train_e2_blur.py
python scripts/compare_blur_segments.py 900 960
python scripts/evaluate_test_video.py --start 900 --end 960 --pred artifacts/runs/Phase5_blur/events_900_960.csv

# Evaluasi pada segmen GT tambahan (setelah anotasi manual dengan scripts/bounce_annotator.py)
python scripts/evaluate_test_video.py --start 300 --end 360
python scripts/evaluate_test_video.py --start 900 --end 960
# Klip lambat di sekitar error (opsional)
python scripts/make_error_clips.py 900 960 955.4

# Klip verifikasi buta, antarmuka klik, dan penilaian
python scripts/make_verify_clips.py
python scripts/verify_clicker.py
python scripts/score_verify_clips.py

# Video akhir dengan tracking dan counter
python scripts/render_final_video.py
```
---
[< 11. Kesesuaian dengan Ketentuan Tugas dan Celah yang Tersisa](11_kesesuaian_dengan_tugas_dan_celah.md) | [Lampiran B >](lampiran_b_peta_berkas.md) | [Daftar isi](README.md)

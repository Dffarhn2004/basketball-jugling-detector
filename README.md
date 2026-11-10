# Basketball Bounce Counter — The Juggling Bounces Challenge

Pipeline deep learning untuk menghitung berapa kali bola basket menyentuh lantai pada video juggling tiga bola.

1. **Lokalisasi:** YOLO26n (`yolo26n.pt`) di-fine-tune pada 111 gambar beranotasi sendiri (model E2).
2. **Tracking:** penyambungan deteksi mentah berdasarkan jarak posisi (bukan IoU).
3. **Event bounce:** aturan titik terendah lintasan di zona lantai (turun lalu naik).

Laporan lengkap: [`laporan/laporan_final.pdf`](laporan/laporan_final.pdf) (sumber Markdown di [`laporan/`](laporan/README.md)).
Video demo: _isi URL YouTube Unlisted di sini_.

## Setup (Windows)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[phase0]"
python -m bounce_counter doctor
pytest -q
```

## Data dan bobot yang dibutuhkan

Berkas besar tidak ikut repo (lihat `.gitignore`). Letakkan di root proyek:

| Berkas | Keterangan |
|---|---|
| `videofull.mp4` | Video 20 menit (YouTube `oWqwY1MLBck`) |
| `videotesting.mp4` | Video uji baru (opsional) |
| `yolo26n.pt` | Bobot pretrained (E1) |
| `artifacts/runs/E2_finetuned_cpu/weights/best.pt` | Bobot fine-tuned (E2), model akhir |
| `artifacts/runs/E2_blur_cpu/weights/best.pt` | Bobot E2-blur (hanya untuk eksperimen motion blur) |

Ground truth bounce: `data/annotations/bounce_events_gt_v2.csv` (126 event, detik 0–60) dan dua segmen tambahan `gt_segment_300_360.csv`, `gt_segment_900_960.csv` (135 event masing-masing). Dataset deteksi: `data/detection/dataset.yaml`.

## Menjalankan

Semua dari root proyek. Deteksi mentah disimpan ke CSV sehingga tahap berikutnya cepat.

```powershell
# Evaluasi detector E1 vs E2 (test split)
python scripts/evaluate_e1_e2.py

# Metode akhir pada 0-60 detik (evaluasi terhadap GT v2)
python scripts/phase4_bridging.py

# Seluruh video: hitungan bounce
python scripts/phase4_bridging_full.py

# Evaluasi segmen ber-GT (TP/FP/FN, APE, errors.csv)
python scripts/evaluate_test_video.py --start 900 --end 960

# GT manual seluruh video (tombol B; lanjut otomatis) lalu bandingkan dengan hitungan pipeline
python scripts/annotate_full.py videofull.mp4
python scripts/compare_full_count.py

# Eksperimen augmentasi motion blur (E2-blur)
python scripts/make_blur_dataset.py
python scripts/train_e2_blur.py
python scripts/compare_blur_segments.py 900 960

# Video baru tanpa GT (parameter dibekukan)
python scripts/phase5_test_video.py videotesting.mp4

# Render video demo (bounding box, track ID, counter)
python scripts/render_final_video.py

# Bangun ulang laporan PDF
python scripts/build_report_pdf.py "<url-video-demo>"
```

Daftar skrip lain (anotasi, klip verifikasi buta, diagnostik): lihat [`laporan/lampiran_a_cara_mereproduksi.md`](laporan/lampiran_a_cara_mereproduksi.md) dan [`laporan/lampiran_b_peta_berkas.md`](laporan/lampiran_b_peta_berkas.md).

## Struktur

```
src/bounce_counter/   CLI dan QC data
scripts/              skrip eksperimen per fase
configs/              konfigurasi E1, E2, pipeline
data/                 anotasi, split, dataset deteksi
artifacts/            hasil run dan evaluasi
laporan/              laporan (Markdown + PDF)
tests/                unit test
```

## Hasil ringkas

- Detector (test, 18 gambar): E1 F1 0,80 vs E2 F1 0,98.
- Bounce, detik 30–60 (holdout): 70/70 benar, 0 false positive. Seluruh video: 2.685 bounce (~135/menit).
- GT manual tambahan (300–360 s dan 900–960 s, 135 event masing-masing): F1 0,985 dengan GT asli, 1,00 setelah koreksi GT (batas atas, lihat laporan bagian 6.2 dan 9).
- Augmentasi motion blur (E2-blur): tidak ada perbedaan terukur terhadap E2; model akhir tetap E2.
- GT manual seluruh video (2.702 tanda, total acuan 2.697): pipeline 2.685, selisih −12, APE 0,44% (0,63% terhadap 2.702 tanda mentah); 18 FN dan 1 FP per event.
- Keterbatasan: satu video, satu kamera, GT satu penganotasi tanpa pemeriksaan kedua; angka F1 per event hanya perkiraan. Detail di laporan bagian 6.5, 7.3, dan 8.

Status terkini: [`PROJECT_STATUS.md`](PROJECT_STATUS.md).

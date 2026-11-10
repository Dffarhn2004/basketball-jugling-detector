# E1/E2/E3 — Controlled Experiment Matrix

| ID | Detector | ByteTrack | State Machine | Tujuan |
|---|---|---|---|---|
| E1 | `yolo26n.pt` pretrained | fixed config V0 | fixed config V0 | baseline tanpa fine-tune |
| E2 | fine-tuned `best.pt` | **sama persis V0** | **sama persis V0** | efek fine-tuning murni |
| E3 | **sama persis E2** | val-optimized V1 | val-optimized V1 | efek pipeline tuning |

## Urutan
1. Save E1 immutable.
2. Buat data training, train E2 di train, pilih checkpoint di validation.
3. Bandingkan E1/E2 di validation dengan config event sama; belum touch final test tuning.
4. E3 optimize V1 hanya dengan validation.
5. Freeze semua config/weights lalu evaluasi test **sekali final**.
6. Evaluasi count video penuh sesuai tugas, pisahkan data train/test dalam pembahasan.

## Yang harus identik E1/E2
- Input video/timebase, frame ROI & resize, encoder decode.
- Detector confidence/IoU threshold dan class mapping secara semantik (class ID bisa berbeda).
- Tracker algo/threshold, smoothing, floor calibration.
- Bounce candidate threshold, cooldown, dedup.
- Matching method & tolerance.

## Jika E2 justru lebih buruk
Tetap laporkan: mungkin overfit, dataset kurang representatif, model pretrained sudah cukup baik, atau lower confidence menghasilkan noise. **Jangan** re-label test atau menghapus error examples untuk menghasilkan cerita positif.

## Penanda pada metrics
- E1/E2/E3 `phase=validation` atau `phase=test`, `run_id`, data split version, GT version.
- Report detection mAP dan event F1 berbeda tabel.
- Report speed FPS dan hardware agar perbandingan runtime transparan.

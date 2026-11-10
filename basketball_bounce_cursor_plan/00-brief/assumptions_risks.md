# Assumptions, Risks, Mitigations

| Risiko | Dampak | Mitigasi dan bukti |
|---|---|---|
| File video lokal tidak tersedia | Seluruh pipeline blocked | Minta file yang sah dan catat sha256 |
| FPS variable / timestamp salah | Event match dan jumlah salah | Simpan `frame_index`, FPS nominal, dan PTS jika tersedia |
| Video 20 menit dan GT ribuan event | Anotasi manual berat | Anotasi per segment, double review, QC |
| Motion blur | Detector miss | Sampel sulit, fine-tune + augmentasi terkontrol |
| ID switch | Count ganda / hilang | Spatiotemporal dedup, tracker debug |
| Bola overlap / tangan menutup | Multiple event tidak terlihat | Audit frame, review segment, `uncertain` label |
| Lantai tak berupa garis Y konstan | Kontak salah | Konfigurasi floor ROI / perspektif |
| Random train/test split | Metrik tampak terlalu bagus | Temporal non-overlap + buffer |
| Threshold tuning di test | Leakage | Validation-only tuning |
| Detektor bagus tetapi bounce jelek | Metrik salah sasaran | Evaluate detection dan event secara terpisah |
| Fine-tuning lebih buruk | Cerita penelitian tetap sah | Laporkan failure dan ablation tanpa memanipulasi |
| GPU terbatas | Training lambat | Nano, crop ROI, imgsz 640, batch kecil |
| Copyright video | Video upload diblokir | Unlisted, izin/ketentuan, fallback Drive/LMS dari soal |
| AGPL/dependency license | Distribusi ulang terganggu | Periksa lisensi aktual sebelum publikasi |
| Event simultan | Count undercount | Event identity bertumpu pada waktu **dan** lokasi |
| Overfitting satu video | Generalization terbatas | Caveat laporan, temporal holdout |

## Prioritas risiko
1. Ground truth video penuh tidak selesai.
2. Event counter false-positive pada hand catches.
3. Dataset leakage dari frame berdekatan.
4. Tracking ID terfragmentasi.
5. Packaging/export dan deadline.

## Respons ketika risk terjadi
- Catat `PROJECT_STATUS.md`.
- Jangan klaim teratasi tanpa bukti.
- Buat reproduksi minimal dan unit test.
- Dokumentasikan mitigasi yang benar-benar diuji.

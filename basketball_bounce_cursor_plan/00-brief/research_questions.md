# Research Questions & Hypotheses

## RQ1 — Kecukupan pretrained detector
Seberapa baik pretrained YOLO26n menemukan bola pada video spesifik dan bagaimana kegagalannya memengaruhi event counting?

**Hipotesis (untuk diuji, bukan fakta):** Deteksi berkurang kualitasnya ketika bola tertutup tangan, tumpang tindih atau blur.

## RQ2 — Efek fine-tuning
Apakah fine-tuning pada sampel video yang teranotasi meningkatkan detection mAP dan event F1 bila komponen lain dibekukan?

**H0:** Tidak ada peningkatan yang konsisten.  
**H1:** Ada peningkatan pada deteksi dan/atau event count.

## RQ3 — Efek pipeline tuning
Apakah optimasi threshold tracker dan physics-aware event detector mengurangi false-positive/false-negative dibanding konfigurasi tetap?

**H0:** Optimasi tidak memberi perubahan yang berarti.  
**H1:** Optimasi di validation meningkatkan kinerja pada test holdout.

## RQ4 — Jenis kegagalan yang dominan
Kesalahan mana yang paling banyak berkontribusi pada selisih count?
- detector miss / blur
- occlusion
- tracker ID switch / fragment
- hand catch sebagai bounce palsu
- floor localization error
- duplicate counting
- event yang berimpitan

## Variabel eksperimen
- Independen E1→E2: checkpoint detector.
- Independen E2→E3: tracker/event params.
- Dependen: event TP/FP/FN, precision, recall, F1, APE, mAP, runtime/FPS.
- Kontrol: segment video, frame resolution/timebase, annotation GT, aturan matching, execution environment (dicatat).

## Catatan inferensi ilmiah
Dataset berasal dari satu video. Hasil test holdout temporal masih **intra-video**; jangan menggeneralisasikan secara berlebihan ke arena, sudut kamera, atau bola lain tanpa eksperimen tambahan.

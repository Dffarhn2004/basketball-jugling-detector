# Inference Protocol & Model Comparison

## Standardized inference
- Decode input original, simpan `frame_idx` dan PTS.
- Resize internal sesuai model `imgsz` tetapi bbox output diubah ke source pixel space.
- E1/E2 gunakan `imgsz`, `conf`, `iou`, tracker config, FPS handling, floor ROI, event params sama.
- Filter `basketball` / `sports ball` berdasarkan nama kelas yang dicari, bukan numeric ID tetap.
- Catat skipped frames, tracking resets, error OpenCV decoder, frame drops.

## E1 vs E2 fairness
```
pretrained weights --- same input video --- same tracker --- same state machine --- metrics
finetuned weights -- same input video --- same tracker --- same state machine --- metrics
```
Kecuali bobot, semuanya harus identik untuk E1 vs E2. Jika baseline hanya dijalankan pretrained dengan filter COCO sports ball, jelaskan mapping ke custom one-class.

## E3
E3 menggunakan fine-tuned weights E2 dan memilih parameter tracker/event di validation, lalu freeze untuk test. Jangan mencampur efek E2/E3.

## Postprocessing consistency
- Waktu event didefinisikan pada source timestamps.
- Confidence output detektor bukan otomatis confidence bounce.
- Tracking ID bisa hilang/bertukar; report event tetap menggunakan event_id unik.
- Semua raw files disimpan sebelum smoothing/dedup supaya analisis dapat ditelusuri.

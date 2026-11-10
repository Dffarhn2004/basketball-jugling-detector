# Architecture — Why This Pipeline?

```
source.mp4
   |
   v
Frame decoder (OpenCV; preserve frame_index and timestamp)
   |
   v
YOLO26n detector: E1 pretrained / E2 fine-tuned
   |
   v
ByteTrack: associate detections into short trajectories
   |
   v
Trajectory smoothing and local floor-contact candidate search
   |
   v
Bounce state machine: falling -> contact candidate -> rising
   |
   v
Contact validation + deduplication across frames / ID switches
   |
   +--> events.csv, summary.json, failures.csv
   |
   v
Annotated demo video
```

## Mengapa YOLO?
- Bobot pretrained tersedia, fine-tuning sederhana, output bounding box langsung.
- Runtime relatif hemat, ekosistem terdokumentasi.
- Detector saja **belum menghitung bounce**.

## Mengapa ByteTrack?
- Bisa memanfaatkan deteksi confidence rendah untuk mempertahankan lintasan.
- Integrasi minimal dengan Ultralytics.
- Tracker bisa ID-switch saat overlap/blur; harus ditangani pada postprocessing.

## Mengapa state machine bukan TCN?
- Lebih sedikit data anotasi temporal untuk memulai.
- Interpretabilitas tinggi (jelaskan aturan secara eksplisit pada laporan).
- Kesalahan lebih mudah dibagi menjadi masalah localization/tracking/event.
- Weakness: perubahan sudut kamera / gerakan tangan bisa menipu rule, perlu validasi floor.

## Alternatif yang sengaja ditunda
- RT-DETR: mengubah detector, tidak langsung menyelesaikan bounce.
- TrackNet: adaptasi multi-ball heatmap lebih mahal.
- TCN/LSTM: butuh label temporal kuat, eksperimen terpisah.
- End-to-end video transformer: compute/data overhead besar.

## Model-level vs pipeline-level tuning
Fine-tuning melakukan gradient updates pada bobot detector. Confidence threshold, track buffer, radius floor, smoothing window adalah parameter pipeline. Laporan harus memisahkan keduanya.

## Kontrak fairness
E1 dan E2 menggunakan **satu parameter set pipeline default sama persis**. E3 memakai bobot E2 dan parameter yang ditentukan dengan validation. Ketiganya dievaluasi pada test yang sama.

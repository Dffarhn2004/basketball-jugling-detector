# E1 — Pretrained Baseline Protocol

## Tujuan
Membuktikan seberapa baik model YOLO26n pretrained menangkap tiga bola tanpa data latihan spesifik. Baseline adalah **pembanding ilmiah**, bukan sekadar demo.

## Konfigurasi yang harus disimpan
- Checkpoint `yolo26n.pt`, versi package dan SHA checkpoint jika tersedia.
- `imgsz`, `conf`, `iou`, kelas apa saja yang diprediksi, device, precision.
- ByteTrack config version.
- State machine default config.
- Video source SHA, split manifest version, timestamp logic.

## Protokol menjalankan
1. Pastikan `doctor` dan `video-info` lulus.
2. Pilih satu clip eksplorasi 30–60 detik **bukan untuk final test-driven tuning**.
3. Jalankan inference tanpa mengubah bobot.
4. Export frame-level bbox dengan confidence, overlay dan optional tracker IDs.
5. Catat kejadian nyata: bbox terlewat, false ball, occlusion, ID switch, blur.
6. Freeze config E1 dalam folder `artifacts/runs/E1_<timestamp>/`.
7. Setelah GT test siap, eval E1 dengan config yang dibekukan.

## Contoh Python verifikasi (bukan script final)
```python
from ultralytics import YOLO
model = YOLO('yolo26n.pt')
results = model.predict(source='data/raw/source.mp4', stream=True, imgsz=640)
for result in results:
    # convert bbox to original frame coordinates + timestamp in production code
    pass
```

## Common mistake
Pretrained COCO dapat mendeteksi beberapa kelas termasuk `sports ball`; dalam dataset fine-tuned kita melabel satu kelas `basketball`. Karena class indices/checkpoint berbeda, **buat canonical class mapping**. Filter class resmi berdasarkan `model.names`, jangan hardcode kelas `0` untuk semua checkpoint.

## Result log
- Detector recall per annotated val/test.
- Pelanggaran apakah deteksi 3 bola missing pada frame sulit.
- Event F1 setelah pipeline siap (bukan sekadar bbox mAP).
- Jangan isi angka sampai dijalankan.

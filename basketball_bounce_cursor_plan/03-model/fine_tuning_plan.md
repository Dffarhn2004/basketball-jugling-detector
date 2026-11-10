# E2 — Fine-Tuning YOLO26n

## Objective
Adaptasi pretrained YOLO26n terhadap appearance tiga bola basket dan kondisi blur, overlap, cahaya, floor proximity di video referensi.

## Prerequisites
- E1 baseline run tersimpan.
- YOLO-format detection dataset lengkap (train/val/test temporal).
- Dataset QC lulus.
- Environment dan checkpoint diketahui, GPU jika tersedia.

## Proposed first run (initial, subject to hardware validation)
```python
from ultralytics import YOLO

model = YOLO('yolo26n.pt')
results = model.train(
    data='data/detection/dataset.yaml',
    epochs=50,
    imgsz=640,
    batch=8,
    seed=42,
    project='artifacts/training',
    name='e2_finetune_v1',
    patience=12,
)
```
Angka ini adalah *starting point*, bukan hyperparameter optimal. Sesuaikan batch dengan VRAM; verifikasi signature API pada versi terpasang. Jika training CLI melalui Windows, wajib entrypoint `if __name__ == '__main__'`.

## Training plan
1. Freeze dataset manifest version; pin source split.
2. Load pretrained checkpoint, set single class basketball.
3. Run one clean default training baseline (modifikasi minimum).
4. Observe train/val losses dan val mAP, precision/recall.
5. Jika blur tetap menjadi sumber miss, lakukan run augmentasi khusus (E2b) **hanya setelah** bukti failure.
6. Pilih checkpoint pada validation, tidak pernah test.
7. Simpan `best.pt`, `last.pt` bila ada, config, CSV losses, environment, data hash.

## Apa yang benar-benar 'dituning'?
- **Model weights:** transfer learning/fine-tuning via optimizer dan gradien.
- Hyperparameter training: epoch, image size, LR, batch, augmentation.
- **Bukan** fine-tune neural model: tracker thresholds, event thresholds.

## Failure & termination logic
- Jika val mAP turun vs pretrained, jangan otomatis menaikkan epochs. Periksa data/label/distribusi.
- Jika training tidak konvergen, cek class mapping dan format anotasi.
- Jika OOM, turunkan batch, image size (dicatat), bukan mengganti tanpa log.
- Jika model overfit satu video, pertimbangkan augmentasi dan early stopping.

## Output wajib
`training_run_manifest.json`, `best.pt`, `results.csv`, plots (jika ada), `val_metrics.json`, `dataset_version.txt`, `checkpoint.sha256`.

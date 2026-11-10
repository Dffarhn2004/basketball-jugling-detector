"""Fine-tune E2-blur: hiperparameter sama dengan E2 (artifacts/runs/E2_finetuned_cpu/args.yaml); beda hanya dataset latih
(+ salinan motion blur). Hasil di artifacts/runs/E2_blur_cpu. E2 asli tidak disentuh."""
from pathlib import Path
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
if __name__ == "__main__":
    YOLO(str(ROOT / "yolo26n.pt")).train(
        data=str(ROOT / "configs/train_e2_blur.yaml"), epochs=50, patience=10, batch=8, imgsz=640, device="cpu", workers=0,
        optimizer="AdamW", lr0=0.001, seed=42, deterministic=True, amp=False, close_mosaic=10,
        hsv_h=0.0, hsv_s=0.15, hsv_v=0.15, degrees=5, translate=0.05, scale=0.2, shear=2, fliplr=0.5, mosaic=1.0, erasing=0.4,
        project=str(ROOT / "artifacts/runs"), name="E2_blur_cpu", exist_ok=False, verbose=False)

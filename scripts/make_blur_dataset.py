"""Buat dataset E2-blur: train = gambar asli + salinan motion blur (offline augmentation); val/test disalin apa adanya.

Motion blur = kernel garis (panjang acak 9-31 px, sudut acak 0-180 derajat), seed tetap. Label YOLO disalin tanpa perubahan
(blur searah tidak menggeser pusat bola secara berarti).
"""
import random, shutil
from pathlib import Path
import cv2, numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/cvat_phase2_reviewed/final"
DST = ROOT / "data/cvat_phase2_reviewed/final_blur"
SEED, LMIN, LMAX = 42, 9, 31

def motion_kernel(length: int, angle_deg: float) -> np.ndarray:
    k = np.zeros((length, length), np.float32)
    k[length // 2, :] = 1.0
    m = cv2.getRotationMatrix2D((length / 2 - 0.5, length / 2 - 0.5), angle_deg, 1.0)
    k = cv2.warpAffine(k, m, (length, length))
    return k / max(k.sum(), 1e-6)

if __name__ == "__main__":
    if DST.exists(): raise SystemExit(f"{DST} sudah ada; hapus dulu jika ingin membuat ulang")
    for split in ("val", "test"):
        shutil.copytree(SRC / split / "obj_train_data", DST / split / "obj_train_data")
    out = DST / "train/obj_train_data"; out.mkdir(parents=True)
    rng = random.Random(SEED); n = 0
    for img in sorted((SRC / "train/obj_train_data").glob("*.jpg")):
        shutil.copy2(img, out / img.name); shutil.copy2(img.with_suffix(".txt"), out / img.with_suffix(".txt").name)
        length = rng.randrange(LMIN, LMAX + 1, 2); angle = rng.uniform(0, 180)
        blurred = cv2.filter2D(cv2.imread(str(img)), -1, motion_kernel(length, angle))
        cv2.imwrite(str(out / f"{img.stem}_mb.jpg"), blurred, [cv2.IMWRITE_JPEG_QUALITY, 95])
        shutil.copy2(img.with_suffix(".txt"), out / f"{img.stem}_mb.txt"); n += 1
    print("gambar blur dibuat:", n, "| total train:", len(list(out.glob('*.jpg'))))

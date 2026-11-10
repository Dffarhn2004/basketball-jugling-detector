# Environment Setup — Windows / CPU / NVIDIA GPU

## Minimum
- Python 3.11+ dalam environment terisolasi (pin versi aktual).
- Git, FFmpeg/ffprobe jika memerlukan metadata/encode.
- OpenCV, NumPy, Pandas atau Polars, ultralytics, torch, scipy, matplotlib, PyYAML, pytest.
- GPU NVIDIA optional; CUDA/PyTorch combination harus kompatibel driver.

## Commands contoh Windows PowerShell
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
# setelah requirements.txt ada dan dipin:
pip install -r requirements.txt
python -m bounce_counter doctor
pytest -q
```

## GPU verification
```powershell
nvidia-smi
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```
Jika `torch.cuda.is_available()==False`, jangan menyebut GPU-ready. Verifikasi wheel CUDA versi sesuai docs PyTorch resmi.

## CUDA caveat
Tidak semua GPU laptop / Windows punya CUDA. Jangan hardcode `.cuda()`; gunakan `device` configurable.

## Python package entrypoint Windows
```python
if __name__ == '__main__':
    main()
```
Disarankan pada script yang bisa memicu multiprocessing training/dataloader.

## Storage
File video panjang, frame datasets, model training checkpoints, dan rendered MP4 bisa memakan banyak disk. Hindari menulis semua raw frames saat hanya perlu sampling. Sebelum training/render, periksa free disk.

## Pinned versions
Catat exact version pada `requirements-lock.txt` setelah environment berfungsi; lakukan test import smoke sebelum training.

## Rujukan
- https://docs.pytorch.org/get-started/locally/
- https://docs.ultralytics.com/quickstart/
- https://ffmpeg.org/ffprobe.html

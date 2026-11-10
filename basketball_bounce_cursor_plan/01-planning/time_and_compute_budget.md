# Effort & Compute Budget — Asumsi untuk Perencanaan

Tidak ada data GPU pengguna yang terverifikasi. Nilai di bawah **bukan estimasi durasi aktual**, hanya urutan prioritas resource.

## Fase berat CPU/GPU
1. Ekstraksi frame: CPU + disk, hindari full video 30 FPS tanpa perlu.
2. Anotasi event manual: **waktu manusia** dominan.
3. Training YOLO26n: GPU ideal, batch disesuaikan VRAM.
4. Inferensi video penuh: GPU mempercepat, CPU mungkin bisa namun lambat.
5. Render video: CPU/I/O, gunakan MP4 H.264 + FPS source.

## Strategi hemat resource
- Pretrained smoke test pada 30–60 detik.
- Deteksi training awal `imgsz=640`; uji lebih besar hanya bila bola terlalu kecil.
- `batch` auto atau kecil bila VRAM terbatas; catat nilai aktual.
- Simpan frame representatif, bukan duplikat berurutan ribuan.
- Tahan eksperimen hyperparameter terlalu banyak.
- Dataset dan weight di `data/` / `artifacts/` yang tidak masuk Git secara default.

## Tanyakan hanya jika diperlukan
- GPU/VRAM yang tersedia dan batasan eksekusi lokal/cloud.
- Izin mengunduh dan memproses video.
- Ketersediaan manusia untuk review manual GT.

## Jika tidak ada CUDA
Jalankan unit tests dan P0/P1 smoke subset di CPU; anotasi GT tetap bisa dilakukan. Training penuh hanya setelah opsi komputasi diputuskan.

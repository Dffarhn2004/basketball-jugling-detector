> The Juggling Bounces Challenge, laporan proyek. Bagian ini berdiri sendiri; lihat [README.md](README.md) untuk urutan.

## 1. Analisis Masalah dan Arsitektur

### 1.1 Definisi masalah

- **Input:** satu video (`videofull.mp4`), 1280×720, 30 fps, 36.003 frame (1200,1 detik), H.264. Seorang pria menjuggling tiga bola; tiap frame berisi dua sampai tiga bola. Kamera tetap.
- **Output:** jumlah total sentuhan bola ke lantai, beserta waktu tiap event.
- **Definisi event:** satu event = satu momen saat salah satu bola menyentuh lantai. Bola yang ditangkap atau dipantulkan di tangan bukan event.

### 1.2 Dekomposisi

| Tahap | Pertanyaan | Keluaran |
|---|---|---|
| Lokalisasi | Di mana bola di tiap frame? | Kotak per bola + confidence |
| Tracking | Kotak mana yang bola yang sama antar frame? | Lintasan per bola |
| Deteksi event | Kapan sebuah lintasan menyentuh lantai? | Waktu/frame event |

Detector saja tidak menghitung bounce. Bounce adalah pola temporal pada lintasan: turun, kontak, lalu naik.

### 1.3 Pemilihan model dan trade-off

- **YOLO26n sebagai detector.** Bobot pretrained tersedia, fine-tuning sederhana, keluarannya langsung kotak, dan cukup ringan untuk dijalankan di CPU (sekitar 20 frame per detik pada seluruh video). Model yang lebih besar dapat lebih akurat, tetapi tidak diperlukan karena detector sudah mencapai F1 0,98 setelah fine-tuning.
- **Mengapa bukan model temporal end-to-end** (misalnya TCN atau video transformer): data berlabel waktu kami terbatas (126 event), sedangkan aturan gerak berbasis lintasan transparan dan dapat diaudit per event. Setiap keputusan dapat ditelusuri ke frame tertentu.
- **ByteTrack** dipakai pada tahap awal karena terintegrasi dengan Ultralytics dan memanfaatkan deteksi berconfidence rendah. Kelemahannya baru terlihat kemudian (Bagian 5).

### 1.4 Arsitektur akhir

```
videofull.mp4
   |
   v
Frame decoder (OpenCV, indeks frame = waktu x 30 fps)
   |
   v
Detector YOLO26n fine-tuned (E2), conf >= 0,25
   |
   v
Asosiasi berbasis JARAK pada deteksi mentah (menggantikan IoU ByteTrack)
   |
   v
Deteksi event: titik terendah lintasan, turun lalu naik, dekat lantai
   |
   v
events.csv + video beranotasi (kotak, jejak, penanda, counter)
```


---
[< Ringkasan](00_ringkasan.md) | [ 2. Data dan Strategi Training >](02_data_dan_strategi_training.md) | [Daftar isi](README.md)

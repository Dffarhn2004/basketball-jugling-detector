> The Juggling Bounces Challenge, laporan proyek. Bagian ini berdiri sendiri; lihat [README.md](README.md) untuk urutan.

## 8. Mengapa Metode Ini Bekerja, dan Apa Batasnya

- **Bola cepat dan blur** menurunkan IoU antar frame, sehingga IoU bukan ukuran asosiasi yang baik. Jarak pusat dengan gerbang yang dibatasi ukuran bola jauh lebih toleran, dan prediksi kecepatan konstan menjembatani frame yang hilang.
- **Aturan lantai** (sisi bawah ≥ 0,65 tinggi frame) menolak pantulan di tangan. Aturan ini hanya sah untuk kamera tetap pada posisi seperti ini.
- **Titik terendah lintasan** cocok dengan frame kontak yang kami lihat pada gambar (galat waktu rata-rata 0,53 frame).
- **Terlalu cocok dengan satu skenario.** Semua hasil berasal dari satu video, satu orang, satu kamera. Pada video lain, ambang lantai dan skala gerak perlu disesuaikan.


---
[< 7. Analisis Kegagalan](07_analisis_kegagalan.md) | [ 9. Integritas Eksperimen dan Kemungkinan Bias >](09_integritas_eksperimen_dan_kemungkinan_bias.md) | [Daftar isi](README.md)

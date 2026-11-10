> The Juggling Bounces Challenge, laporan proyek. Bagian ini berdiri sendiri; lihat [README.md](README.md) untuk urutan.

## 7. Analisis Kegagalan

Tugas meminta setiap pantulan yang terlewat atau berlebih disebutkan dengan timestamp, penyebab, dan rencana perbaikan. Untuk segmen ber-GT, daftarnya lengkap. Pada 0–60 detik:

| # | Jenis | Waktu | Penyebab | Rencana perbaikan |
|---|---|---|---|---|
| 1 | FN (GT-0001) | 3,033 s (frame 91) | Bola setengah keluar dari tepi kiri frame (sekitar x 70, y 560). Kontak tidak dapat dipastikan, dan timing GT sendiri ambigu. | Periksa ulang GT pada video asli. Jika kontak memang tidak terlihat, hapus dari GT. |
| 2 | FN (GT-0042) | 23,833 s (frame 715) | Berjarak 1 frame dari GT-0041. Prediksi di 23,767 s sudah dicocokkan dengan GT-0041, sehingga GT-0042 yang tersisa. Kemungkinan satu bounce tercatat dua kali di GT. | Periksa GT-0041/0042. Jika duplikat, hapus salah satunya (maka FN ini hilang). |
| – | FP | – | Tidak ada pada 0–60 detik. | – |

### Segmen tambahan 300–360 s dan 900–960 s

Semua selisih antara GT asli dan prediksi pada dua segmen ini sudah diperiksa lewat klip lambat (0,25x). Hasilnya, **tidak ada kegagalan model yang ditemukan; semua selisih adalah kesalahan GT** menurut penilaian penulis. Daftar lengkap (waktu = frame ÷ 30; toleransi 0,1 s):

| # | Segmen | Jenis | Waktu | Penyebab | Tindak lanjut |
|---|---|---|---|---|---|
| 3 | 300–360 | FN | 300,133 s (GT frame 9004) | GT terlambat 5 frame; prediksi di 299,967 s (frame 8999) benar. Prediksi itu jatuh tepat di luar batas segmen, sehingga tampak sebagai FN. | GT digeser ke frame 8999 |
| 4 | 300–360 | FP, FP, FN | 313,233 s; 313,533 s; GT 313,367 s | GT mencatat satu bounce, padahal ada dua (frame 9397 dan 9406); dua prediksi benar. | GT dipecah menjadi dua event |
| 5 | 900–960 | FP, FN | 955,167 s (prediksi) vs 955,333 s (GT) | GT terlambat 5 frame | GT digeser ke frame 28655 |
| 6 | 900–960 | FP, FN | 955,600 s (prediksi) vs 955,867 s (GT) | GT terlambat 8 frame | GT digeser ke frame 28668 |

Catatan: selisih tepat 3 frame di segmen 900–960 yang sempat tercatat sebagai error berasal dari bug pembulatan di skrip evaluasi (Bagian 6.2), bukan dari model maupun GT. Karena koreksi hanya dilakukan pada titik yang berbeda dan frame koreksi diambil dari prediksi, kesimpulan "tidak ada kegagalan model" hanya berlaku untuk selisih yang terdeteksi; kesalahan yang dilakukan bersama oleh GT dan model tidak akan terlihat (Bagian 9).

### Di luar segmen ber-GT

Di luar segmen ber-GT, hanya dua miss yang terbukti dari verifikasi buta:

| Klip | Waktu | Penyebab | Rencana |
|---|---|---|---|
| V09 | sekitar 751,9 s | Belum didiagnosis | Putar ulang klip, bandingkan deteksi mentah, lintasan, dan aturan |
| V02 | sekitar 989,1 s | Belum didiagnosis | Sama |

**[CELAH]** Kegagalan di luar tiga segmen ber-GT (0–60, 300–360, 900–960 s; total sekitar 4 menit dari 20) belum dapat didaftar per timestamp karena tidak ada GT penuh. Kegagalan dari tahap iterasi awal (107 FN pada baseline E2) sudah dianalisis agregat di Bagian 5.3, bukan per event.


---
[< 6. Hasil Kuantitatif](06_hasil_kuantitatif.md) | [ 8. Mengapa Metode Ini Bekerja, dan Apa Batasnya >](08_mengapa_metode_ini_bekerja_dan_apa_batasnya.md) | [Daftar isi](README.md)

> The Juggling Bounces Challenge, laporan proyek. Bagian ini berdiri sendiri; lihat [README.md](README.md) untuk urutan.

## 10. Kesimpulan

1. Fine-tuning pada anotasi buatan sendiri (111 gambar, 336 kotak) menaikkan F1 detector dari 0,80 menjadi 0,98.
2. Hambatan terbesar bukan detector, melainkan **tracking**: IoU gagal menyambung bola yang cepat dan blur.
3. Mengganti asosiasi IoU dengan asosiasi jarak pada deteksi mentah, plus aturan titik terendah lintasan di zona lantai, menaikkan F1 event dari sekitar 0,27 menjadi 0,98–1,00 pada segmen ber-GT, dengan nol false positive.
4. Pada seluruh video 20 menit, pipeline menghitung 2.685 bounce secara konsisten, dan verifikasi buta mendukung presisinya (20/20), dengan sebagian bounce terlewat.

### Pekerjaan lanjutan

- Hitung manual (atau sampling terstruktur) seluruh bounce video untuk mendapatkan APE total sebagaimana diminta tugas.
- Periksa ulang GT v2 (pemeriksaan kedua, duplikat GT-0041/0042, GT-0001).
- Diagnosis dua bounce terlewat dan kaji aturan jendela agar recall naik.
- Tambahkan augmentasi motion blur pada fine-tuning dan uji pengaruhnya.
- Uji pada video lain (kamera atau orang berbeda) untuk memeriksa generalisasi.
- Ubah laporan ini menjadi PDF sesuai ketentuan tugas.


---
[< 9. Integritas Eksperimen dan Kemungkinan Bias](09_integritas_eksperimen_dan_kemungkinan_bias.md) | [ 11. Kesesuaian dengan Ketentuan Tugas dan Celah yang Tersisa >](11_kesesuaian_dengan_tugas_dan_celah.md) | [Daftar isi](README.md)

> The Juggling Bounces Challenge, laporan proyek. Bagian ini berdiri sendiri; lihat [README.md](README.md) untuk urutan.

## 9. Integritas Eksperimen dan Kemungkinan Bias

Hal-hal yang sebaiknya dinyatakan terbuka dalam laporan:

1. **Kemungkinan tumpang tindih data latih.** Enam dari 75 gambar latih detector diambil pada detik 5, 15, 25, 35, 45, 55, yang berada di dalam jendela evaluasi bounce 0–60 detik. Pengaruhnya pada metrik bounce kemungkinan kecil (enam gambar), tetapi tetap tumpang tindih.
2. **Holdout tidak sepenuhnya buta.** Parameter hanya disetel pada detik 0–30, tetapi hipotesis tentang penyebab kegagalan dibentuk dengan melihat frame dari seluruh 60 detik, termasuk 30–60.
3. **GT v2 dianotasi satu orang dan belum diperiksa kedua kali.** Skor hampir sempurna sebagian mencerminkan kualitas GT yang belum teruji.
4. **Titik kontak diagnostik** pada tujuh kasus berasal dari usulan AI, belum diverifikasi manusia. Verifikasi buta pada Bagian 6.4 dan GT segmen 300–360 s dan 900–960 s (Bagian 6.2) adalah validasi manusia di luar 60 detik pertama.
5. **Dua dugaan penyebab awal ternyata keliru** (fragmentasi ID, detector dropout). Kami mempertahankannya dalam laporan karena ini pelajaran metodologis: kesimpulan dari heuristik atau pemeriksaan visual sekilas harus diuji dengan data mentah sebelum membangun perbaikan.
6. **Sampel verifikasi kecil.** 30 klip memberi rentang ketidakpastian lebar.
7. **Koreksi GT satu arah.** Pada segmen 300–360 s dan 900–960 s, semua selisih GT dan prediksi yang diperiksa (4 kasus) diputuskan sebagai kesalahan GT, lalu GT dikoreksi ke arah prediksi, dengan frame koreksi diambil dari frame prediksi. Hanya titik yang berbeda yang diperiksa ulang; event yang cocok tidak. Skor setelah koreksi (F1 1,00) karenanya adalah batas atas, dan skor dengan GT asli (F1 0,985 pada kedua segmen) lebih tepat dipakai sebagai perkiraan. Idealnya GT diperiksa ulang secara independen oleh orang kedua tanpa melihat prediksi.
8. **Detector dan segmen evaluasi.** Segmen 300–360 s berada dalam rentang latih detector (`train_01`, sekitar enam gambar latih di dalamnya). Hanya segmen 900–960 s (rentang `test_01`) yang tidak terlihat oleh detector maupun penyetelan parameter.
9. **Perbandingan E2 dan E2-blur.** Satu seed dan satu proses training per model; test split detector hanya 18 gambar; selisih hitungan bounce hanya satu event dan terjadi di titik yang GT-nya dikoreksi berdasarkan prediksi E2. Kesimpulannya hanya "tidak ada bukti perbedaan", bukan "blur tidak berguna": blur yang lebih realistis (lokal pada bola) atau lebih banyak data latih belum diuji.


---
[< 8. Mengapa Metode Ini Bekerja, dan Apa Batasnya](08_mengapa_metode_ini_bekerja_dan_apa_batasnya.md) | [ 10. Kesimpulan >](10_kesimpulan.md) | [Daftar isi](README.md)

# Ground Truth Protocol — Seluruh Video

## Mengapa ini wajib
Soal meminta menghitung jumlah pantulan video **secara manual** dan mengaudit setiap miss atau overcount. Label event hasil model tidak dapat menjadi ground truth tanpa verifikasi manual.

## Workflow anotasi efisien
1. Gunakan `ffprobe`/video-info untuk membagi video menjadi segmen **berdasarkan timestamp nyata**.
2. Potongan kerja ideal 30–120 detik dengan mapping waktu absolut tetap. Pilih panjang yang memudahkan review.
3. Dalam setiap segmen, annotator tandai **semua tiga bola** yang menyentuh lantai.
4. Rewatch dan lakukan audit event berdekatan, saat kamera blur, tangan menutup, dan saat dua bola bertemu lantai bersamaan.
5. Gabungkan CSV memakai `time_s_absolute`, bukan timestamp yang kembali nol di setiap klip.
6. Jalankan pemeriksaan gap antar-segmen, duplicate di batas segmen, timestamp monotonic dan total event.
7. Hasil lengkap harus memiliki reviewer sign-off sebelum dipakai pada laporan.

## 2-pass review yang disarankan
- **Pass A:** hitung secara manual setiap segmen.
- **Pass B:** lihat raw video ulang tanpa melihat prediksi model; perbaiki event yang terlewat.
- **Adjudication:** tinjau event `uncertain`, boleh dicatat sebagai uncertain jika fisik tidak dapat dipastikan.
- Jangan menggunakan event auto sebagai referensi tunggal untuk memberi label GT, karena dapat menciptakan confirmation bias.

## Audit & completeness
- Setiap segmen dalam full-video coverage manifest punya status `annotated` dan `reviewed`.
- Tidak boleh ada segmen kosong tanpa alasan eksplisit.
- Cek overlap boundary pada pemotongan klip.
- Hitung `sum(events_per_segment)` sama dengan GT full video setelah menghapus duplikat boundary.
- Simpan versi (`gt_v1.csv`, `gt_v2.csv`) dan perubahan review.

## Istilah angka
- `ground_truth_full_video_count`: total valid manual pada seluruh recorded frames.
- `ground_truth_test_count`: manual count pada held-out test time intervals.
- `model_full_video_count`: prediksi model di seluruh recorded frames.
- `model_test_count`: prediksi model hanya pada test intervals.

Sajikan keduanya terpisah di laporan karena full-video metrics bisa mengandung segmen yang dipakai untuk training.

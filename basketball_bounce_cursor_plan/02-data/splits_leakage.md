# Temporal Split & Leakage Prevention

## Masalah
Jika frame 1000 masuk train dan frame 1001 masuk test, model bisa 'hafal' adegan identik. Random split frame **tidak kredibel** untuk satu video.

## Strategi
- Lakukan split **kontigu per waktu**, misal beberapa blok train, val, dan test yang tidak bertumpang tindih.
- Buat buffer antar blok > panjang window temporal yang pernah dipakai (contoh sampling/tracking smoothing) untuk mengurangi kemiripan boundary.
- Jangan tentukan persentase final sebelum mengetahui total durasi dan isi video; target awal train 60–70%, val 15–20%, test 15–20% sebagai rancangan, disesuaikan agar tiap split mencakup variasi adegan.
- Simpan `data/splits/split_manifest.csv` dengan `start_time_s`, `end_time_s`, `split`, `exclusion_buffer_s`, `source_hash`.

## Satu video vs generalisasi
- Test temporal segment itu holdout **intra-video**, bukan generalisasi lintas subjek/video.
- **Jangan** mengklaim generalisasi antar kamera atau dunia nyata.
- Final `full_video_count` masih boleh dilaporkan untuk memenuhi soal, tetapi harus diberi catatan bahwa model telah melihat sebagian visual dari video pada training.

## Fair comparison
- Seluruh experiment E1/E2/E3 menggunakan test time interval yang sama.
- Untuk E1/E2, hyperparameter tracker dan detector inference tidak boleh dioptimasi khusus test.
- E3 tuning parameter di validation, setelah itu freeze dan evaluasi test.

## Pemeriksaan otomatis
```text
assert not overlap(train, val)
assert not overlap(train, test)
assert not overlap(val, test)
assert every_labeled_frame_has_split_or_explicit_excluded_buffer
assert no_test_file_used_by_train_dataloader
```

## Leakage lewat inspeksi visual
Melihat hasil baseline pada seluruh video boleh untuk memahami challenge, tetapi **jangan** memilih frame test sebagai tambahan training atau menggunakan error test untuk retune. Pisahkan daftar masalah pada test hanya untuk failure analysis akhir.

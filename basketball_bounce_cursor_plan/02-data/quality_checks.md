# Dataset Quality Control & Validator

## Quality gates untuk annotation boxes
- Class ID hanya `0`.
- Nilai `x/y/w/h` dalam `[0,1]`; `w,h>0`.
- Image dan label nama berpasangan.
- Tidak ada file kosong tanpa keputusan bahwa no-ball memang valid.
- Label bbox tidak terbalik, duplikat atau melampaui batas.
- Ambil thumbnail overlay QA untuk train, val, test.

## Quality gates untuk GT event
- `event_id` unik, `time_s` berada dalam panjang video sebenarnya.
- Frame index valid; konversi frame→waktu dicek pada sampling random.
- Event hampir simultan dengan lokasi berbeda **jangan** dibuang hanya karena timestamp sama.
- Peristiwa yang sama pada dua frame berdekatan tidak diberi label double.
- Coverage manifest tidak ada gap.
- Confidence/review status tersedia.

## Quality gates untuk split
- Interval tidak overlapping.
- Exclusion buffer eksplisit.
- Label test tidak dimasukkan ke train loader.
- Dataset hash/manifest dicatat per training run.

## Script validator yang Cursor perlu buat
```shell
python -m bounce_counter validate-data --config configs/dataset.yaml
```
Exit nonzero pada error serius; tulis `artifacts/data_qc/report.json` serta contoh frame bermasalah.

## Laporan statistik
- Counts per split (actual).
- Distribusi jumlah visible balls per frame.
- Rasio frame blur/occlusion (jika ditag).
- Panjang total segmen GT yang sudah reviewed.
- Jumlah event approved, probable, unresolved (actual).

## Kebijakan perbaikan
Perubahan label harus versioned. Jangan edit file ground truth selama final evaluation berjalan. Jika GT direvisi, seluruh eksperimen benchmark diulang pada GT versi baru dan alasan dicatat.

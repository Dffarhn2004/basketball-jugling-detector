# Practical FAQ for Cursor and student

## Haruskah YOLO?
Tidak. Model lain memungkinkan; YOLO dipilih karena deployment/training/tracking sederhana, bukan klaim universal terbaik.

## Apakah YOLO dapat langsung menghitung bounce?
Tidak. Bounding box tiap frame belum mengandung definisi kontak lantai; perlu event detector.

## Apakah ByteTrack deep learning dilatih di sini?
Tidak secara default. Training yang diminta tugas dipenuhi oleh fine-tuning detector YOLO.

## Kenapa dua eksperimen E1/E2?
Menguji efek *model weights* sambil menjaga seluruh parameter pipeline lain identik.

## Kenapa E3?
Memisahkan kenaikan dari tuning tracking/event dari efek fine-tune detector.

## Apakah metrik mAP cukup?
Tidak. Outcome utama tugas adalah kontak lantai. Wajib event TP/FP/FN/F1 dan count error.

## Bagaimana dua bola jatuh bersamaan?
Hitung dua event berbeda jika lokasi/objek kontak berbeda. Dedup berbasis waktu saja salah.

## Bagaimana video tanpa timestamp sempurna?
Audit FPS/timebase/PTS dan dokumentasikan strategi mapping frame→waktu; jangan menganggap VFR = CFR.

## Apakah perlu semua ground truth manual?
Ya, tugas secara eksplisit meminta angka GT video ditentukan manual dan semua error diberi timestamp.

## Apakah angka sekitar 3200 boleh dipakai sebagai ground truth?
Tidak. Klaim dari deskripsi YouTube membahas percobaan yang lebih panjang dari rekaman yang tersedia.

## Kalau E2 lebih buruk dari E1?
Laporkan apa adanya. Analisis data size, label noise, augmentasi, overfitting, dan checkpoint selection.

## Kalau compute terbatas?
Mulai baseline 30–60 detik, dataset kecil berkualitas, `imgsz=640`, batch kecil, CPU smoke tests; training final sesuai resource yang tersedia.

# Demo video output specification

## Overlay minimum
- Bounding box untuk bola yang terdeteksi (confidence optional).
- Tracking ID ketika stabil, garis trajectory beberapa titik terakhir.
- Garis/ROI kontak lantai jika digunakan.
- Live total bounce count, boleh total per track sebagai tambahan dengan catatan ID bisa reset.
- Flash/marker saat event dihitung, timestamp video dan event confidence/diagnostics jika relevan.

## Video engineering
- Output video panjang penuh jika feasible (jangan mengaku full-video bila hanya cuplikan).
- Jaga aspect ratio dan timestamp asli.
- Frame overlay harus ditulis bahkan ketika tidak ada deteksi.
- Gunakan FPS video output yang konsisten dengan timestamp yang dihitung.
- Jika VFR, pilih strategi resampling eksplisit dan catat mapping PTS.
- Simpan metadata input/output, codec, ukuran, framerate, checksum.
- Hasil video harus sesuai `events.csv` dan `summary.json`, tidak dihitung ulang berbeda.

## Kualitas penjelasan dalam video
- Tambahkan intro singkat tentang E1/E2 (opsional) tetapi output utama wajib menampilkan counter actual.
- Jika menampilkan count dua model, beri label jelas per model.
- Jangan menampilkan statistik validasi palsu saat video belum diaudit.

## Publish
- YouTube Unlisted jika akses/legal memungkinkan.
- Jika diblokir copyright otomatis, gunakan Google Drive/LMS seperti di soal.
- Konfirmasi URL aktif dan akses dari mode incognito; tulis URL **di bagian atas PDF**.
- Jangan mengunggah tanpa izin pengguna.

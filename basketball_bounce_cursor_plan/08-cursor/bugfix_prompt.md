# Cursor Prompt — Debugging Protocol

> Baca `AGENTS.md`, `PROJECT_STATUS.md`, dan dokumen fase yang terkait. Jangan melakukan refactor luas. Reproduksi masalah dengan minimal clip atau unit test; klasifikasikan apakah error berasal dari detection, association/tracking, timestamp, floor reference, motion smoothing, event state machine, atau event matching. Beri evidence berupa logs, frame indices, dan timestamp. Buat regression test yang gagal terlebih dahulu lalu patch sekecil mungkin, jalankan tes lagi, laporkan sebelum/sesudah. Jangan mengubah fixed test set atau manual GT agar skor naik. Jika mengubah parameter, kalibrasi di validation, simpan versi run/config baru; jangan overwrite run lama. Update log status.

## Artifact debugging yang perlu dilampirkan
- Input path + sha256, clip time range, FPS/timebase.
- Predicted events sekitar failure dan GT sekitar failure.
- Detection bbox/tracker IDs sejumlah frame sebelum-sesudah.
- Config + model weights hash.
- Root cause, changed files, test logs, next step.

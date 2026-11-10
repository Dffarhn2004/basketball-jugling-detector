# Agent Instructions — Read Before Writing Code

Dokumen ini dibuat agar Cursor menjalankan penelitian secara bertahap dan auditabel.

## Mandat utama

Bangun pipeline penghitung **kontak bola basket ke lantai**, dari video lokal, untuk tepat tiga bola pada video referensi. Wajib mencakup training/fine-tuning deep learning, ground truth manual, evaluasi, kegagalan ber-timestamp, demo video, report PDF, dan sumber kode.

## Batas desain yang disetujui

- Bahasa utama: **Python 3.11+** (versi dipastikan saat setup).
- Detektor awal: **Ultralytics YOLO26n** `yolo26n.pt`.
- Tracker: **ByteTrack** melalui Ultralytics.
- Detektor akhir: checkpoint **fine-tuned** dari pretrained yang sama.
- Event detector: **finite-state machine**, kontak lantai + smoothing lintasan + temporal hysteresis.
- Eksperimen E1/E2/E3: harus menyimpan konfigurasi dan output lengkap.
- Jangan mengintroduksi LSTM, TCN, Video Transformer, SAM2, microservice, React dashboard, database, Docker, queue, atau cloud service tanpa alasan kuat dan persetujuan.
- Jika `yolo26n.pt` tidak dapat dijalankan dalam environment, verifikasi dokumentasi, pin versi dan catat fallback dalam ADR; jangan diam-diam mengganti model.

## Urutan kerja wajib

1. **Audit repository** dan baca semua `README.md`, `AGENTS.md`, `PROJECT_STATUS.md`, `DECISIONS.md`.
2. **Phase 0:** setup project, environment, CLI, config, tests; jangan train dulu.
3. **Phase 1:** video intake, audit FPS/timebase, baseline pretrained dan simpan outputs.
4. **Phase 2:** anotasi, split non-overlap, quality control; pastikan dataset benar.
5. **Phase 3:** fine-tuning, validasi, simpan checkpoint dan artefak.
6. **Phase 4:** tracking & event counting; debug via potongan video.
7. **Phase 5:** evaluasi E1/E2/E3 frozen, audit errors, full-video count, demo, laporan.
8. Update `PROJECT_STATUS.md` setelah setiap phase dan `CHANGELOG.md` untuk perubahan penting.

## Aturan kualitas & akademik

- **Tidak boleh mengarang** jumlah bounce, mAP, F1, FPS, epoch yang sudah dijalankan, GPU, data anotasi, maupun keberhasilan training.
- Jangan gunakan ≈3.200 dari deskripsi YouTube sebagai ground truth.
- Ground truth harus dari **event manual pada video rekaman**, bukan estimasi frekuensi.
- Test set tidak boleh dipakai memilih threshold/hyperparameter; gunakan validation set.
- Frame yang berdekatan tidak boleh tersebar acak ke split berbeda.
- E1 vs E2: sama persis tracker, state machine, threshold, timebase, dataset evaluasi, dan renderer. Berbeda hanya checkpoint detector.
- E3: optimasi pipeline menggunakan validation; jalankan **satu kali evaluasi final** pada test setelah parameter dibekukan.
- Event yang bersamaan dari bola berbeda harus dapat dihitung terpisah.
- Semua TP, FP, FN harus dapat diaudit melalui file hasil dan timestamp.
- Klaim performa harus mengikuti hasil nyata; jangan mengasumsikan fine-tuning pasti lebih baik.

## Aturan implementasi

- Code modular, type hints, docstrings pendek, file kecil, tanpa abstraksi prematur.
- Pisahkan murni (`event_rules`, `matching`, `geometry`, `metrics`) dari I/O (`video`, `weights`, `CSV`, `render`).
- Config YAML/JSON; tidak ada angka threshold hardcoded berserakan.
- Seed ditetapkan, versi dependency dan argumen training disimpan.
- Paths portable dengan `pathlib`; dukung Windows; tidak asumsikan CUDA tersedia.
- Simpan raw outputs dan metadata run; output jangan ditimpa diam-diam.
- Setiap bugfix wajib punya regression test.
- Gunakan `if __name__ == "__main__":` untuk entrypoint multiprocessing di Windows.

## Kapan berhenti dan bertanya

Boleh bertanya **hanya jika input esensial tidak ada**, contoh: file video lokal legal/diizinkan belum tersedia, pilihan GPU/cloud benar-benar mengubah estimasi kerja, atau ground truth memerlukan verifikasi manual pengguna. Jika bukan blocker, ambil default terdokumentasi, catat asumsi, lanjutkan.

**Training GPU besar, pemasangan dependency sistem, transfer data ke cloud, publikasi video, dan pengunggahan GitHub** hanya dilakukan saat pengguna menyetujui aksi tersebut.

## Format respons Cursor setelah mengerjakan phase

1. File yang dibuat/diubah.
2. Perintah dijalankan.
3. Hasil validasi nyata, lengkap angka bila ada.
4. Kendala tersisa.
5. Langkah fase berikutnya.
6. Update file status.

Jangan mengaku sebuah phase selesai tanpa menjalankan acceptance checks yang sesuai.

## Baca spesifikasi detail

- [`00-brief/assignment_requirements.md`](00-brief/assignment_requirements.md)
- [`01-planning/milestones_and_gates.md`](01-planning/milestones_and_gates.md)
- [`06-engineering/repo_structure.md`](06-engineering/repo_structure.md)
- [`05-experiments/metrics_and_matching.md`](05-experiments/metrics_and_matching.md)

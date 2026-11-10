# Milestones, Acceptance Criteria, dan Quality Gates

## Gate P0 — Engineering setup
- [ ] `python -m bounce_counter --help` berfungsi.
- [ ] `pytest -q` berjalan (termasuk unit tests awal).
- [ ] `python -m bounce_counter doctor` mencetak versi Python/Torch/Ultralytics/OpenCV, device dan FFmpeg availability.
- [ ] Dokumentasi setup Windows tersedia.
- [ ] Tidak ada training/download model berjalan tanpa persetujuan pengguna.

## Gate P1 — Pretrained snapshot (penting: sebelum training)
- [ ] Video lokal dilacak provenance-nya (`source`, hash, resolution, frame count, nominal FPS, duration).
- [ ] **E1 baseline** tersimpan dengan checkpoint pretrained.
- [ ] Raw detections/tracks dan sample overlay tersedia.
- [ ] Ada catatan real error examples (dari frame aktual) untuk memilih dataset.
- [ ] Config E1 dibekukan dan punya `run_id`.

## Gate P2 — Dataset
- [ ] Detection boxes berformat YOLO dan lolos validator.
- [ ] Definisi bounce valid vs hand catch bisa diajarkan ke anotator.
- [ ] Split manifest **waktu non-overlap** serta exclusion buffer tersedia.
- [ ] Manual event GT video lengkap + auditor/reviewer.
- [ ] 3 bola simultan dilabel secara independen jika kontak berdekatan.

## Gate P3 — Fine-tuning
- [ ] Run training tercatat (weights, dataset hash/version, epochs, imagesz, augment, seed).
- [ ] Model `best.pt` tersimpan, label class mapping valid.
- [ ] Val detection report benar-benar diproduksi.
- [ ] Hindari memilih model berdasar test set.

## Gate P4 — End-to-end
- [ ] Frame stream, tracks, smoothed positions, candidate contacts, accepted events punya kontrak data yang konsisten.
- [ ] State machine menolak hand catch dan menghitung multiple balls.
- [ ] Unit tests lewat pada kasus occlusion, duplicate, simultaneous hits, missing track.
- [ ] 60s clip terproses end-to-end dan preview benar.

## Gate P5 — Evaluasi, demo, laporan
- [ ] E1/E2 diuji dengan **config pipeline identik**.
- [ ] E3 (bila dijalankan) hasil param validation-frozen, bukan tuning test.
- [ ] Test TP/FP/FN/F1 dan count APE direkam.
- [ ] Setiap FP dan FN punya timestamp + kategori + komentar.
- [ ] Output MP4 ada bbox/ID/trajectory/counter.
- [ ] URL demo valid dan tertera paling atas di PDF.
- [ ] Source + README reproduksi; hasil akhir berisi batasan penelitian.

## Jika gate gagal

Berhenti, tulis kendala ke status, buat reproduksi minimal, perbaiki dan uji ulang. Jangan melompati gate atau mengganti angka menjadi perkiraan.

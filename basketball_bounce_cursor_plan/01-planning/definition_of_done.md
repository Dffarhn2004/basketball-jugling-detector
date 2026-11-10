# Definition of Done (DoD)

Sebuah task selesai bila:
1. Acceptance criteria task terpenuhi.
2. Ada unit/integration test (jika behavior terkait code).
3. Perintah eksekusi aktual dicatat.
4. Artefak tersimpan dalam direktori hasil yang tidak menimpa run lain.
5. Input dan output schema jelas.
6. `PROJECT_STATUS.md` diperbarui.
7. Jika mengubah logika event, ada regression test menggunakan kasus gagal nyata / synthetic.
8. Tidak ada metrics atau klaim hasil yang tidak berasal dari run.

## DoD dataset
- Anotasi mengandung semua bola terlihat, sesuai konvensi bbox.
- Tidak ada label class di luar `basketball=0`.
- YOLO coordinates dibatasi `[0,1]` sesuai format.
- Metadata frame dan split manifest konsisten.
- Audit video dengan timestamp; review manual pada segmen ambigu.

## DoD eksperimen
- `run_id`, git commit, config hash, dataset version, model source, seed, device, timestamp.
- Raw predictions, event CSV, metrics JSON, failure CSV, screenshot sampel.
- E1/E2 comparison tanpa beda konfigurasi terselubung.

## DoD laporan
- Semua 5 bab inti soal terjawab dan hasil konsisten dengan file eksperimen.
- Tabel dan grafik bersumber dari metrik aktual.
- Semua miss/over-count punya timestamp dan penyebab.
- Link Unlisted demo di bagian atas PDF dan aktif.

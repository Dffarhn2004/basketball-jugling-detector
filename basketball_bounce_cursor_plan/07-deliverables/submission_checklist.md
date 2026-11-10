# Final Submission Checklist

## Report
- [ ] Laporan PDF valid, bisa dibuka dan teks terbaca.
- [ ] Link demo ditaruh di bagian atas PDF.
- [ ] Latar masalah + diagram architecture + speed/precision tradeoffs.
- [ ] Data prep, fine-tuning dan augmentasi terdokumentasi.
- [ ] Pipeline bbox→tracking→event counting terjelaskan.
- [ ] Manual video-level GT berisi event per pantulan.
- [ ] Count prediksi vs GT dan APE/Error Rate dihitung.
- [ ] E1/E2/E3 table dengan konfigurasi adil.
- [ ] Seluruh missed dan overcounted bounces punya timestamp serta penyebab.
- [ ] Limitations dan future improvements spesifik.

## Demo
- [ ] Bounding boxes dan IDs/trajectories terlihat.
- [ ] Counter diperbarui berdasarkan actual counted events.
- [ ] Event sekaligus dari dua bola tidak collapse.
- [ ] Audio/video sinkron jika audio disertakan.
- [ ] Link Unlisted/Drive/LMS bisa dibuka tanpa hak akses privat.

## Code
- [ ] Source GitHub/ZIP bisa diakses.
- [ ] README executable dan dependency pinning.
- [ ] No API tokens, passwords, local absolute paths, copyright-sensitive source clips yang tidak boleh dibagikan.
- [ ] Config untuk E1/E2/E3 dan weights path terdokumentasi.
- [ ] Tests pass, perintah reproducible, metadata run disimpan.

## Integrity
- [ ] Tidak memakai ≈3200 video description sebagai manual GT.
- [ ] Tidak mengklaim optimizer melatih ByteTrack/state machine.
- [ ] Training/validation/test independent interval tanpa leakage.
- [ ] Test set digunakan hanya setelah pemilihan hyperparameter.
- [ ] Semua angka laporan berasal dari output nyata.

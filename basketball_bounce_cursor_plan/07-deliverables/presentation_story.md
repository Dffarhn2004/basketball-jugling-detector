# Narasi presentasi: dari baseline menuju bukti perbaikan

## Story arc (7–10 menit; sesuaikan instruksi dosen)

1. **Problem (1 menit):** tiga bola bergerak cepat; satu frame tidak cukup untuk mengetahui bounce.
2. **Architecture (1 menit):** detector, tracker, finite-state event counter. Jelaskan apa yang dilatih.
3. **Baseline E1 (1 menit):** tampilkan contoh deteksi sukses/gagal dan hasil baseline nyata.
4. **Hypothesis (1 menit):** tambah label blur/occlusion, fine-tune untuk meningkatkan kualitas deteksi.
5. **Fine-tuning E2 (1 menit):** data/split/hyperparameter, bandingkan mAP dan bounce metrics tanpa mengubah tracker.
6. **Optimasi E3 (1 menit):** state-machine validation tuning; jelaskan perbedaannya dengan fine-tuning model.
7. **Failure audit (1–2 menit):** contoh per timestamp, miscount event dari hand catch dan ID switch, perbaikan.
8. **Conclusion (1 menit):** hasil final, batasan satu video, langkah selanjutnya.

## Visual yang meyakinkan
- Same-frame comparison E1 vs E2 pada kasus sulit (jangan hanya pilih contoh yang menang).
- Event timelines GT vs prediction, FP/FN colored on report figure.
- Raw CSV mendukung semua klaim count, bukan skor dari pengamatan saja.

## Pertanyaan dosen yang harus disiapkan
- Kenapa YOLO dibanding TrackNet/RT-DETR?
- Kenapa tracking ID perlu kalau hanya total count?
- Bagaimana menentukan bounce bukan hand catch?
- Apa kebocoran data temporal dan cara menghindarinya?
- Apa yang benar-benar di-*train* dan apa yang di-*tune*?
- Bagaimana kejadian simultan dihitung?
- Apakah mAP naik otomatis berarti event F1 naik?
- Bagaimana mengidentifikasi dan meninjau semua false positive/negative?

# Alternative Models & Fallback Policy

## Default tidak berubah tanpa bukti
Detector `YOLO26n`, tracker ByteTrack, event state machine. Jangan menghabiskan banyak waktu melakukan benchmark model lain sebelum pipeline minimum jalan.

## Kapan mengganti detector?
- Model tidak tersedia di package resmi environment pengguna.
- Detector gagal secara sistematis pada bola dan fine-tuning tak memperbaiki dengan data yang cukup.
- Inferensi terlalu lambat untuk deadline atau output tidak kompatibel.

## Alternatif diurutkan berdasarkan biaya migrasi
1. **YOLO model nano/small** versi resmi lain yang berjalan dalam Ultralytics API (fallback versioned).
2. **RT-DETR** detector alternative; tetap perlu ByteTrack dan state machine.
3. **TrackNet family** jika masalah utama bola cepat tak terdeteksi dan siap untuk multi-ball adaptation.
4. **Video event network** jika hand-catch false-positive tidak terselesaikan dengan physics rules dan event labels cukup.

## Evidence sebelum switch
- Nilai error detector / event sebelum switch.
- Jumlah jam engineering tambahan dan besarnya dataset.
- Kesesuaian dengan kewajiban training, reproducibility.
- Dampak fairness pada E1/E2.

## Jika pengguna meminta 'sesimpel mungkin tapi kuat'
Pilihan utama tetap satu detector yang sama sebelum dan sesudah fine-tune, ByteTrack, state machine yang diuji baik. Tambahkan kompleksitas hanya saat failure analysis menuntutnya.

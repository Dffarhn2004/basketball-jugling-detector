# Requirement Traceability — PDF Tugas Resmi

**Sumber:** `Tugas 1 - Deep Learning (S2 - B).pdf`, halaman 1–2.

## Fakta eksplisit dari soal

- Judul: **The Juggling Bounces Challenge**.
- Deadline tercantum: **14 November 2026**.
- Input: video seorang pria memainkan / memantulkan **tiga bola basket**.
- Tujuan: rancang, implementasikan, dan **latih pipeline deep learning** untuk menghitung **total berapa kali bola menyentuh lantai**.
- Masalah perlu didekomposisi menjadi **localization, tracking, temporal event detection**.
- Bebas menentukan arsitektur.

Video: https://www.youtube.com/watch?v=oWqwY1MLBck

## Deliverable A: Project Report PDF

Wajib menjawab:
1. **Problem Analysis & Architecture:** Mengapa model dipilih; trade-off kecepatan, precision, task suitability.
2. **Data & Training Strategy:** Proses training / fine-tuning dan augmentasi motion blur.
3. **Pipeline Engineering:** Transformasi raw output model ke count (centroid tracking, mathematical peak detection, menolak hand catches).
4. **Quantitative Performance:** Hitung ground truth **secara manual** untuk video, bandingkan prediksi, hitung metrik error seperti Error Rate/APE.
5. **Failure Analysis:** **Setiap** pantulan yang terlewat atau berlebih harus punya timestamp, penyebab, rencana perbaikan.

## Deliverable B: Video Demonstrasi

- Video processed output menunjukkan **bounding boxes, tracking IDs / trajectories, live bounce counter**.
- Unggah sebagai YouTube **Unlisted**; jika terhalang otomatis copyright dapat gunakan tautan Google Drive/LMS.
- Cantumkan URL berfungsi **di bagian atas laporan PDF**.

## Deliverable C: Source Code

- GitHub repository **atau** ZIP.
- Kode bersih dan berkomentar, `README.md` berisi cara eksekusi.

## Requirement-to-evidence mapping

| Requirement | Bukti file/output yang perlu dihasilkan |
|---|---|
| Rancang + train DL | config training, log, weights, training plots |
| Localization | bounding box frame & mAP |
| Tracking | track records, track ID overlay |
| Event detection | state machine, event CSV |
| GT manual | `annotations/bounce_events_gt.csv`, review log |
| Final count | summary CSV/JSON |
| Quant performance | test metrics dan full-video count error |
| Every miss/overcount | `errors.csv` + timestamp dan kategori |
| Video demo | output MP4 + link Unlisted |
| Report | PDF final + URL di bagian atas |
| Source | repo link/ZIP, reproduksi README |

## Yang tidak diwajibkan oleh soal

Tidak ada tuntutan untuk membuat website, API, dashboard interaktif, model Transformer, multi-agent, integrasi realtime, atau deployment production. Hindari penambahan scope ini kecuali diminta.

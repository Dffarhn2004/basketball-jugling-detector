# Object Detection Annotation SOP

## Tools disarankan
CVAT atau labeler yang mendukung format YOLO bounding-box. Pilih yang paling cepat dipakai, dokumentasikan versi/export format.

## Kelas
Hanya satu kelas: `0 = basketball`.

## Aturan bbox
- Gambar kotak paling rapat yang masuk akal mengelilingi bagian bola yang terlihat.
- Ketika bola sebagian tertutup, pertahankan aturan anotasi konsisten; catat `occlusion` dalam QA eksternal bila perlu.
- Ketika satu bola menyatu secara visual dengan bola lain, beri masing-masing box jika masih dapat diidentifikasi, jangan digabung satu bbox besar.
- Jangan label benda bulat yang bukan bola.
- Jika objek sama sekali tidak bisa dikenali, catat sebagai kasus `uncertain` untuk review.
- Kualitas bounding box pada frame blur dievaluasi dan dikoreksi manual.

## Format YOLO
Satu baris per bola:
```text
class_id center_x_norm center_y_norm width_norm height_norm
```
Semua nilai koordinat ternormalisasi pada `[0,1]`; `class_id=0`.

## QA anotasi
- Apakah mayoritas frame memuat tiga bola yang dapat terlihat? Jangan memaksa jumlah tiga bila sebagian occluded.
- Cek box terlalu kecil / besar, clipped, coordinates negatif, duplicate label.
- Cek split leakage dan class map.
- Ekspor preview label random dari **setiap** split.

## Bukti untuk laporan
- Total images per split.
- Distribusi ukuran box, jumlah bola terlihat per frame.
- Persentase contoh blur/occlusion (jika dilabel).
- Screenshot quality control sebelum/ sesudah koreksi.

Angka akhir diisi dari dataset aktual, jangan menggunakan target rencana sebagai data hasil.

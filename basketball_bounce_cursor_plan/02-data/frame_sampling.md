# Frame Sampling Strategy (untuk Deteksi Bola)

## Prinsip
Jangan ambil ratusan frame berturut-turut yang hampir identik. Pilih variasi kondisi gerak, jarak dengan lantai, occlusion, blur, overlap, ekstrem pencahayaan.

## Target awal, bukan kewajiban dari soal
- 300–500 frame awal untuk proof-of-concept, kemudian tambah bila learning curve menunjukkan manfaat.
- Balanced sampling berdasarkan segmen train/validation/test yang telah ditentukan.
- Sampel data anotasi yang digunakan **untuk fine-tuning hanya dari train**, validation hanya untuk pemilihan konfigurasi model, test hanya final.

## Protokol sampling
1. Buat split temporal dengan buffer lebih dulu (`splits_leakage.md`).
2. Dari tiap train segment, sampling seragam setiap N detik ditambah kasus sulit yang muncul pada inspeksi E1.
3. Buat manifest berisi `source_frame_index`, `source_time_s`, `split`, `selection_reason`, `image_file`.
4. Deteksi duplikat/hampir sama (pHash opsional) dalam masing-masing split.
5. Jangan mengambil frame test untuk augmentasi maupun training hanya karena baseline gagal di situ.

## Kategori `selection_reason`
- uniform_time
- motion_blur
- overlap_balls
- hand_occlusion
- floor_contact
- small_ball
- unusual_lighting
- track_fragmentation_example

## Bias yang perlu dihindari
- Terlalu banyak gambar kontak lantai hingga model lemah pada tinggi lain.
- Screenshot tersimpan dengan overlay prediksi YOLO, bukan gambar raw.
- Semua sampel sulit berasal dari test dan terselip ke train.
- Memperbanyak frame mirip hanya untuk mengejar jumlah label.

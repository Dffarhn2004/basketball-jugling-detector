# Bounce Event Annotation — Definisi Detail

## Unit hitung
**Satu event** = satu kontak fisik satu bola dengan lantai, walau kontak berlangsung >1 frame.

### Valid
- Bola turun → menyentuh lantai → memantul kembali.
- Bola hanya bergulir? Jika bergulir tanpa putus kontak, tidak otomatis dihitung sebagai rangkaian pantulan; definisikan satu initial contact jika terdapat jatuh yang jelas.
- Dua/ tiga bola menyentuh lantai pada timestamp sama: **dua/tiga event** terpisah.

### Invalid
- Bola berubah arah karena ditangkap/ditampar tangan tanpa kontak lantai.
- Bola mendekati lantai namun tidak menyentuh.
- Multiple consecutive frames berisi kontak yang sama.
- Refleksi/bayangan bola dianggap objek.

## Event timestamp
Pilih frame yang paling jelas menunjukkan pertama kali bola menyentuh lantai atau titik kontak terbaik yang bisa diidentifikasi. Catat `time_s`, `frame_idx`, `x_contact_px`, `y_contact_px`, `annotator`, `confidence`, `review_status`, `notes`.

## Ketidakpastian
`confidence`: `certain`, `probable`, `uncertain`.
- `uncertain` tidak langsung dihapus atau ditebak.
- Reviewer melihat klip sebelum-sesudah (+ audio jika membantu).
- Keputusan final `include`/`exclude`/`unresolved` dicatat.
- Jika unresolved masih ada, laporan menyebutkan dampaknya; jangan mengklaim GT pasti sempurna.

## Konvensi identitas bola
Jangan mengharuskan GT menetapkan ID permanen pada 3 bola. Gunakan `event_id` unik dan `contact_x,y` untuk membedakan event simultan.

## Prosedur manual
1. Tonton klip 5–15 detik per segmen dengan playback lambat.
2. Tandai setiap kontak lintas tiga bola.
3. Review kembali pada kecepatan normal untuk deteksi kontak terlewat.
4. Untuk kandidat ambigu, inspeksi frame demi frame.
5. Simpan hasil CSV dan review log; peninjau kedua jika tersedia.

## Contoh isi CSV (sintetis, BUKAN data video)
```csv
event_id,frame_idx,time_s,x_contact_px,y_contact_px,confidence,review_status,notes
GT-0001,150,5.000,320,610,certain,approved,synthetic_example
GT-0002,150,5.000,510,612,certain,approved,synthetic_simultaneous_example
```

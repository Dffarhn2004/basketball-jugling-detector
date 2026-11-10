# Scope, Non-goals, Success Criteria

## Scope inklusif
- Proses video lokal (`.mp4`, frame-by-frame), berisi tiga bola.
- Bounding box dan confidence untuk tiap bola.
- Tracking antar-frame, trajectory dan ID apabila valid.
- Contact-to-floor event counting dengan timestamp.
- Manual GT untuk seluruh video sesuai definisi eksplisit.
- Fine-tune detektor, bandingkan dengan pretrained.
- Benchmark event dan audit kesalahan.
- Render video anotasi dengan live count.

## Non-goals
- Streaming webcam realtime.
- Menghitung juggling tangan yang tidak mengenai lantai.
- Mengidentifikasi pemain, wajah, atau aktivitas lainnya.
- Membuat aplikasi web/dashboard.
- Menjamin tracking ID tidak pernah berganti.
- Mengklaim generalisasi ke video lain tanpa bukti tambahan.
- Mengklaim world record dari bagian yang tidak terekam.

## Definisi event valid
Satu bola = satu event saat bola membuat kontak **fisik dengan lantai**. Satu kontak yang terjadi beberapa frame hanya dihitung satu kali. Dua bola mengenai lantai pada saat sama = dua event. Tangan menyentuh/mengubah arah bola tanpa kontak lantai = nol event.

## Kriteria selesai (harus berupa bukti, bukan asumsi)
- Semua file required dan scripts tersedia.
- End-to-end pipeline selesai sampai video output.
- GT manual lengkap dan di-review.
- E1/E2/E3 direproduksi dari config/seed.
- Event metrics dan total count tercatat, termasuk confidence interval jika benar-benar dihitung.
- FP dan FN diekspor, diklasifikasi, dan dibahas per timestamp.
- Report PDF + URL video demonstrasi + source.
- Tidak ada klaim metrik rekaan.

## Target kuantitatif
Tidak menetapkan target F1/APE sebagai jaminan. Setelah baseline, tentukan target internal **aspirational**, kemudian ukur apakah tercapai. Soal tidak mencantumkan threshold kelulusan numerik.

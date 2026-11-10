# Trajectory Features & Noise Handling

## Koordinat
Gambar biasanya `y` makin besar ke bawah. Perkiraan titik kontak bola: `(cx, y_bottom)` dari bbox source pixel, bukan hanya centroid.

## Turunan temporal
Dengan posisi `p_t=(x_t,y_t)` dan waktu nyata `t`:
- `vy_t ≈ (y_t - y_(t-1)) / Δt` dalam pixel/s.
- `vy > 0` berarti bergerak turun; `vy < 0` berarti bergerak naik.
- `ay_t ≈ (vy_t - vy_(t-1)) / Δt` hanya jika data stabil.

## Smoothing
- Gunakan median filter / moving average kecil sebagai baseline.
- Hindari smoothing berlebihan yang menghapus bounce yang sangat cepat.
- Gap pendek dapat diinterpolasi **untuk candidate continuity**, tetapi jangan menciptakan event tanpa visual/contact confirmation.
- Gap panjang harus reset state ke unknown.

## Floor proximity
State kontak perlu mengecek `abs(y_bottom - floor_y(x,frame)) <= tolerance_px` atau keanggotaan ROI lantai. Perkiraan lantai dapat berupa polygon/curve sehingga y tergantung x.

## Diagnostic plot
Setiap track pada segmen pendek:
- y_bottom vs timestamp.
- vy smoothed vs timestamp.
- horizontal contact threshold.
- true GT event markers vs pred markers.

## Pitfall
Bola dipegang tangan dapat memiliki local maximum pada y. Oleh karena itu **peak detection saja tidak cukup**; validasi lantai wajib untuk mengurangi false-positive.

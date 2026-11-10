# Floor Contact Geometry Calibration

## Kenapa sulit?
Di kamera perspektif, lantai bukan selalu satu garis horizontal tetap. Selain itu bbox ball bottom dapat bergeser akibat motion blur, kompresi, dan sebagian tertutup.

## Baseline sederhana
1. Pilih satu frame reference dan lihat batas/region kontak lantai.
2. Simpan satu **floor contact band** dengan dua titik garis `y_floor(x)=a*x+b` bila sudut cukup konstan.
3. Jika garis tidak representatif, gunakan polygon ROI dan locally estimated floor contact coordinate.
4. Boleh pakai satu threshold `y` hanya jika divalidasi terhadap sample dari sisi kiri, tengah, kanan.

## Config draft
```yaml
floor:
  mode: line
  x1_px: null
  y1_px: null
  x2_px: null
  y2_px: null
  contact_tolerance_px: null
  # nilai baru diisi setelah inspeksi video nyata
```

## Konsistensi coordinate space
- Floor annotation dibuat pada **original video resolution**.
- Semua deteksi bbox harus di-convert dari resized frame kembali ke original sebelum dibandingkan.
- Overlay renderer memakai basis koordinat yang sama.

## Kamera bergerak?
Jika bergerak, floor line tetap tidak valid. Pilih lightweight stabilization atau calibration per keyframe, tetapi jangan menambah ini tanpa bukti kamera bergerak.

## Debug evidence
Save image overlays: baseline floor line, ball bbox bottom points, accepted/rejected candidate event. Tandai `floor_geometry_error` saat event salah akibat calibration.

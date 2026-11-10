# Video Intake, Provenance, dan Timebase

## Sumber dari tugas
https://www.youtube.com/watch?v=oWqwY1MLBck

Metadata deskripsi yang ditemukan dari halaman publik: judul "3 Basketball Bouncing"; pemilik menggambarkan percobaan hampir 25 menit, sedangkan rekaman kamera berhenti sekitar 20 menit. **Jangan menganggap deskripsi tersebut sebagai hasil hitung manual.**

## Syarat input
- Dapatkan video lokal melalui cara yang sah, mengikuti izin dan ketentuan sumber.
- Simpan sebagai `data/raw/source.mp4` (tidak commit raw jika hak distribusi tidak jelas).
- Simpan `sha256`, ukuran byte, durasi sebenarnya, resolusi, codec, FPS nominal/avg, kemungkinan VFR, jumlah frame, audio.
- Gunakan `ffprobe` jika tersedia untuk metadata video dan frame timestamps.

## Contoh metadata JSON (placeholder)
```json
{
  "source_url": "https://www.youtube.com/watch?v=oWqwY1MLBck",
  "local_path": "data/raw/source.mp4",
  "sha256": "TBD",
  "width": null,
  "height": null,
  "fps_nominal": null,
  "fps_avg": null,
  "frame_count": null,
  "duration_seconds": null,
  "variable_frame_rate": null,
  "rights_notes": "TBD"
}
```

## Aturan timestamp
- Source of truth ideal: frame presentation timestamp (PTS) dalam satuan detik.
- FPS konstan terverifikasi: `time_s = frame_idx/fps` dapat dipakai.
- Video VFR: **jangan** pakai `frame_idx/fps` sebagai satu-satunya timestamp; simpan PTS per frame.
- Renderer tidak boleh diam-diam mengubah urutan/durasi frame tanpa mapping.

## QC awal
1. Video dapat dibuka sampai frame terakhir.
2. Durasi deklarasi sama dengan realitas file; jika berbeda catat.
3. Audio ada/tidak ada dicatat, tetapi bukan dependency.
4. Definisikan ROI lantai dan koordinat video sebelum resize.
5. Frame_index dan timestamp selalu disimpan bersama hasil model.

# Demonstration Video Renderer

## Required overlays dari soal
- Bounding box masing-masing bola.
- Track ID label yang terbaca.
- Trajectory tail beberapa frame.
- Live updating `Total Bounces: N`.

## Recommended additional overlays
- `Bounce!` flash dekat titik kontak selama beberapa frame.
- State (falling/contact/rising) kecil, optional.
- Floor contact line/polygon, optional toggle.
- Run ID / E1 or E2 indicator.

## Keutuhan video
- Maintain original aspect ratio/resolution secara default.
- Preserve timestamp chronology dan FPS; hati-hati variable FPS.
- Render seluruh recorded video untuk deliverable; boleh sediakan short highlight tambahan, bukan pengganti.
- Confirm codec dan MP4 playable di Windows + browser.
- Jika source ada audio dan diizinkan, remux audio dari original tanpa mengubah timestamp; jika tidak, jelaskan demo tanpa audio.

## Rendering order
1. Ingest `video`, `detections/tracks`, `accepted_events`.
2. Gambar bbox, ID, trajectories untuk frame sesuai timestamp.
3. Hitung cumulative accepted events with `event.time_s <= current_timestamp`.
4. Highlight contact dan caption.
5. Save MP4, detect video writer errors, verify opening dan last frame.

## Validasi
- Onscreen count akhir sama persis `accepted_events.csv` length.
- Event simultan menambah counter 2 jika dua kontak valid.
- Track IDs di overlay benar dengan log tracks pada sampled frames.
- Output duration/frame index mapping valid.
- Link demo unlisted/Drive tidak dibuat oleh script tanpa tindakan pengguna.

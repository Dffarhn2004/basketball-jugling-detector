# Physics-Aware Bounce State Machine — Core Algorithm

## Definisi state (per track)
`UNKNOWN -> FALLING -> CONTACT_CANDIDATE -> RISING_CONFIRMED -> COOLDOWN -> FALLING`

## Thresholds configurable, NOT fabricated constants
- `min_downward_velocity_px_s`: batas indikasi descending.
- `min_upward_velocity_px_s`: batas indikasi ascending.
- `contact_tolerance_px`: toleransi floor.
- `confirm_frames`: beberapa frame untuk validasi reversal.
- `max_gap_frames`: berapa gap sebelum track reset.
- `cooldown_ms`: hindari multi-count satu kontak.
- `smoothing_window`: kompromi noise/response.
Semua nilai dipilih menggunakan **validation data**, bukan test.

## Aturan kandidat
1. Track bergerak **turun** cukup jelas menuju area kontak lantai.
2. `bottom_y` berada dekat floor band atau kontak visual terverifikasi.
3. Dalam lookahead singkat (offline), bergerak **naik** setelah titik candidate.
4. Satu event dipancarkan dengan timestamp titik kontak / local maximum `bottom_y` pada window.
5. Masuk cooldown dan tidak emit event duplikat untuk fase kontak sama.

## Pseudocode
```python
for track in active_tracks:
    append_position(track, frame_time)
    if missing_too_long(track):
        reset_state(track)
        continue

    features = smoothed_motion_features(track)
    near_floor = floor_contact_distance(features.bottom_x, features.bottom_y) <= floor_tol

    if track.state == 'UNKNOWN' and features.falling:
        track.state = 'FALLING'
    elif track.state == 'FALLING' and near_floor:
        track.state = 'CONTACT_CANDIDATE'
        track.candidate = current_observation
    elif track.state == 'CONTACT_CANDIDATE':
        if features.rising_confirmed:
            emit_event(track.candidate)
            track.state = 'COOLDOWN'
        elif candidate_timed_out(track):
            track.state = 'UNKNOWN'
    elif track.state == 'COOLDOWN' and cooldown_expired(track):
        track.state = 'UNKNOWN'
```
Pseudocode adalah gambaran, bukan implementasi lengkap. Seringkali perlu buffer lookahead untuk menggeser timestamp event ke kontak sebenarnya.

## Tiga bola simultan
State machine di-maintain per track. Dua track dapat meng-emit event pada frame yang sama. Deduplikasi akhir hanya menyatukan event jika **waktu dan posisi** juga sangat berdekatan (satu kontak fisik yang sama).

## Hand catches
Jika bola berubah arah **jauh dari lantai**, reject dengan reason `not_near_floor` walaupun local maximum. Dalam posisi tangan dekat lantai, bisa ambigu; tandai untuk failure analysis.

## Guardrails
- Bbox hilang saat kontak: jangan emit bounce berdasarkan interpolasi murni tanpa bukti tambahan.
- Track ID switch: event tidak boleh double-count.
- Count = jumlah accepted **event IDs**, bukan jumlah track IDs / peaks mentah.

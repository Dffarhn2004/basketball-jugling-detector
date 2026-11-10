# Event Deduplication and Simultaneous Contacts

## Tujuan
- Satu kontak multi-frame tidak terhitung berkali-kali.
- Dua bola kontak bersamaan tetap terhitung dua.
- Track ID yang berubah dekat lantai tidak otomatis event tambahan.

## Candidate fields
`time_s,frame_idx,contact_x,contact_y,track_id,confidence,reason`.

## Duplikat kandidat
Satu event fisik biasanya memenuhi **kedua** syarat:
1. |Δt| <= `dedup_temporal_tolerance_s`.
2. Distance(contact points) <= `dedup_spatial_tolerance_px` (scale-aware bila ukuran bola berubah menurut x/y).

Jika hanya timestamp sama tetapi lokasi **berbeda jelas**, jangan merge. Jika posisi sama tetapi waktunya jauh, bisa pantulan baru; jangan merge hanya berdasarkan posisi.

## ID switch
- Jika track A berakhir dan track B dimulai pada lokasi/waktu hampir sama, kandidat kontak dapat menjadi duplikat; merge jika evidence tinggi.
- Jangan memaksa track identity lama/new selalu sama; document ambiguity.

## Cross-track collision
Saat dua bola overlap dan keduanya menyentuh lantai dekat satu titik, dedup geometris bisa **menghapus event sah**. Terapkan diameter bola, bbox history, dan track separation sebelum merge. Kasus sangat ambigu harus masuk audit FP/FN.

## Regression tests
1. one ball remains floor 3 frames -> count 1.
2. two balls floor same frame x far apart -> count 2.
3. one contact fragmented into ID 5 and ID 12 -> count 1.
4. two contacts same x 0.5s apart -> count 2.
5. near-floor hand catch and no contact -> count 0.
6. off-camera brief detection gap -> no hallucinated contact.

## Output
`accepted_events.csv`, `rejected_candidates.csv` plus reject/merge reasons to enable failure audit.

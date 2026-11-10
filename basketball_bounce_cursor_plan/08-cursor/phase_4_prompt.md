# Cursor Prompt — Phase 4: Tracker + Event Counter

> Baca `AGENTS.md`, seluruh `04-pipeline/*.md`, `05-experiments/metrics_and_matching.md`, dan `06-engineering/test_strategy.md`. Kerjakan HANYA Phase 4. Implementasikan ByteTrack result normalization, geometry floor ROI/line, coordinate smoothing, velocity, state machine falling→contact candidate→rising, hysteresis, temporal/spatial dedup, dan support two simultaneous bounces. Simpan event CSV dengan timestamp dan diagnostics. Buat unit tests untuk bounce valid, hand catch, duplicate same-frame, two distinct simultaneous balls, ID switch, short track gap, no-detection, moving perspective. Jangan mengubah detector checkpoint baseline. Jalankan pipeline pada clip kecil dengan GT manual jika tersedia, laporkan missed/overcounted timestamps hasil sebenarnya. Update status.

## Acceptance
- Deterministic event extraction for same input+config.
- ID switching tidak otomatis menambah event.
- Simultaneous separate balls tidak otomatis digabung.
- Pure tests pass.

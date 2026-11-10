# Cursor Prompt — Phase 2: Dataset & Human Ground Truth

> Baca `AGENTS.md`, seluruh `02-data/*.md` dan `05-experiments/metrics_and_matching.md`. Implementasikan tooling untuk sampling frames, ekspor dataset label format YOLO, pengecekan bbox, split temporal tanpa frame leakage, dan validasi CSV event GT. Buat template anotasi manual berisi `event_id, video_time_sec, frame_index, x_contact, y_contact, ball_label_optional, annotator, confidence, notes`. Event adalah satu kontak bola-lantai, bukan hand catch. Dua kontak simultan = dua rows. Sediakan tool untuk melihat clip lambat/step frame untuk memudahkan label. **Jangan mengisi ground truth otomatis sebagai seolah-olah manual.** Bila manusia belum menyelesaikan GT, simpan status pending, jangan lanjut klaim evaluasi. Laporkan jumlah frame tersampel/label yang benar-benar ada, double-check label, update status dan tes.

## Acceptance
- Dataset train/val/test temporal split valid.
- Schema manual event jelas dan lulus validator.
- Semua GT entries harus berasal dari review manusia.

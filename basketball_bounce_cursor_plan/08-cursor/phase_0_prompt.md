# Cursor Prompt — Phase 0: Setup & Skeleton

**Copy text below to Cursor Agent:**

> Baca `AGENTS.md`, `README.md`, `00-brief/assignment_requirements.md`, `06-engineering/repo_structure.md`, `06-engineering/cli_interface.md`, `06-engineering/windows_gpu_setup.md`, dan `01-planning/milestones_and_gates.md`. Kerjakan HANYA Phase 0: siapkan skeleton Python sesuai layout yang diusulkan (boleh lakukan penyesuaian minimal yang dijelaskan), `pyproject.toml` / dependency pins yang kompatibel, `.gitignore`, config placeholders, package entrypoint, CLI help, type checking/linting sederhana, dan unit test untuk utilitas pure yang sudah diimplementasikan. Verifikasi Python & Torch device pada komputer ini, uji import Ultralytics, dan catat model/weight availability. Jangan download video, download large weights, fine-tune, atau memalsukan output. Dokumentasikan semua perintah aktual dan hasil smoke tests. Update `PROJECT_STATUS.md` dan `CHANGELOG.md`. Bila dependency incompatibility terjadi, perbaiki dan jelaskan pin versions. Stop setelah gate Phase 0 tercapai.

## Acceptance
- Struktur source valid dan dependency installable.
- `--help` menghasilkan output; `pytest` menjalankan tes nyata.
- Device check (CPU/CUDA/MPS), Python, PyTorch, Ultralytics version tercatat.
- Tidak ada angka benchmark karangan.

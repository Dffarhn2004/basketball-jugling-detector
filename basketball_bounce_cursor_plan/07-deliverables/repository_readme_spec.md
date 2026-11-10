# Specification for executable repository README.md

README repo implementasi (berbeda dari plan README) perlu mencakup:

1. Purpose dan demo screenshot link (bila tersedia).
2. Python, OS, GPU optional, dependency versions, packages/licenses.
3. Project layout dan data yang tidak dibundel.
4. Cara menempatkan video lokal berizin; file name contoh.
5. Setup `python -m venv .venv`, activate Windows/Unix, install lock/requirements.
6. Smoke test environment dan `pytest`.
7. Command `inspect-video`, `extract-frames`, `annotate/validate-annotations`.
8. Command baseline pretrained E1, termasuk checkpoint dan config pinned.
9. Command fine-tuning E2 dan recovery training checkpoint.
10. Command run pipeline infer / event detection / render.
11. Command evaluation vs GT dan match tolerance.
12. Cara membuat report tables dan reproduksi seed.
13. Data privacy / video license and credits.
14. Known issues, limitations, and one-video scope.
15. Tautan sumber model dan atribusi software.

**Perhatian:** contoh CLI baru boleh dicantumkan sebagai perintah siap jalan jika implementasinya benar-benar tersedia dan dites. Selama scaffolding, tandai sebagai planned interface.

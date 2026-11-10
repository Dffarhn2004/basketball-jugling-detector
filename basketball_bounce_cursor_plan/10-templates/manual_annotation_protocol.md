# Human Annotation Session — TEMPLATE

- Source video hash: TBD
- Clip start/end sec: TBD
- Annotator 1: TBD
- Reviewer 2: TBD
- Annotation tool/version: TBD
- Displayed FPS/speed: TBD
- Floor reference specification: TBD

## Event definition reminders
1. Satu kontak bola-lantai = satu event walaupun beberapa frame berdekatan.
2. Bola yang hanya berbalik arah di tangan bukan bounce.
3. Dua bola kontak pada waktu serupa = dua row bila benar-benar keduanya kontak.
4. Label temporal sebaiknya merepresentasikan frame pertama kontak jika teramati; catat kebijakan saat blur.
5. Ketidakpastian dilabel `uncertain`, tidak diam-diam dibuang.
6. Review seluruh rentang klip, jangan sampling beberapa event lalu mengklaim GT lengkap.

## QC
- [ ] Event IDs unik
- [ ] `video_time_sec` increasing/nondecreasing (simultaneous valid)
- [ ] Every event within clip range
- [ ] Double review disagreement resolved and recorded
- [ ] Total per-clip event count confirmed
- [ ] Source/annotation version hashed

## Sign-off
- Primary count: TBD
- Review count: TBD
- Resolved count: TBD
- Open uncertainties: TBD

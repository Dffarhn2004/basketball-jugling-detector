# Data Augmentation — Which and Why?

## Prinsip
Augmentasi harus mendekati gangguan nyata pada video, bukan menambah kerusakan tanpa alasan. Terapkan **hanya pada train**; validation/test raw unchanged.

| Teknik | Mengatasi | Risiko | Kebijakan awal |
|---|---|---|---|
| Brightness/contrast | Pencahayaan | Distorsi berlebihan | ringan |
| HSV adjustments | perubahan warna/lighting | bola jadi tidak realistis | ringan |
| Motion blur | gerakan cepat | bbox jadi ambigu | selektif |
| Gaussian noise | artefak kompresi | noise berlebihan | ringan |
| Scale & translate | perubahan posisi/ukuran | crop bola, kontak lantai hilang | moderat |
| Horizontal flip | sedikit variasi layout | geometri adegan tidak natural | uji hanya pada detection training |
| Mosaic | konteks objek bervariasi | lantai fisik tidak koheren | hati-hati/nonaktifkan jika merugikan |

## Motion blur khusus
- Gunakan custom Albumentations pipeline *jika* API versi Ultralytics mendukung `augmentations` dan sudah diuji.
- Jangan mengklaim blur aktif hanya karena ditulis dalam config; verifikasi sampel augmented image yang benar-benar masuk training.
- Tambahkan augmentasi bertahap; evaluasi val setelah tiap eksperimen.

## Kontaminasi event labels
Bbox augmentation dilakukan pada model **detector**; label bounce temporal **tidak** ikut transformed secara sembarangan. Kalau memotong/mirror video pada event model hipotetis, sinkronkan event timestamps/coordinates secara ketat.

## Ablation sederhana
E2a: default train augmentation.
E2b: default + blur/lighting (opsional jika terjustifikasi).
Jika E2b tidak membantu, laporkan apa adanya dan gunakan E2a.

## Bukti report
- Parameter augment actual.
- 6–12 gambar before/after sample.
- Table delta mAP dan event F1 (hasil nyata).

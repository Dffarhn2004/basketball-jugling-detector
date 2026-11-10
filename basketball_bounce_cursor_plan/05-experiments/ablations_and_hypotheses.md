# Minimal Ablation Studies

## Required / recommended
### A1 Detector fine-tune effect
E1 pretrained vs E2 fine-tuned, tracker + FSM fixed. Ini eksperimen utama.

### A2 Pipeline optimization
E2 fixed vs E3 tuned tracker/event params dengan checkpoint identical.

## Optional only if time
### A3 Floor validation ON/OFF
Bandingkan event FP akibat hand catches; confound: geometric calibration.

### A4 Smoothing window 1/3/5
Eksplorasi tradeoff noise vs delay; **validation-only**.

### A5 Motion blur augmentation ON/OFF
Butuh training run tambahan; hanya saat baseline menunjukkan motion blur sebagai dominant errors.

## Hypothesis log
Untuk tiap ablation:
- Komponen apa berubah?
- Parameter lain tetap?
- Dataset train/val/test mana dipakai?
- Metrik apa prioritas?
- Apakah hasil mendukung hipotesis?

## Praktik ilmiah
Jika fine-tuning malah menurunkan event F1, **itu temuan valid**. Cari sebab berdasarkan saved per-frame predictions, bukan mengubah seluruh pipeline sekaligus sehingga causal interpretation hilang.

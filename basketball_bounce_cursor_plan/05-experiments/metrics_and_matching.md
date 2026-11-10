# Event-Level Matching, Counting Metrics & Fair Evaluation

## Data
GT event: timestamp + optional contact XY. Pred event: timestamp + XY. Satu event GT tidak boleh dipasangkan dengan >1 pred; sebaliknya satu pred tidak boleh dipasangkan dengan >1 GT.

## Temporal tolerance
Gunakan batas temporal yang **dipatok di validation**, misalnya `min(0.10s, 3/fps)` sebagai kandidat awal; nilai aktual harus dipilih berdasarkan FPS dan ketidakpastian anotasi. Jangan berubah setelah melihat test error.

## Matching algorithm
1. Kandidat pasangan jika `abs(pred.time_s - gt.time_s) <= tolerance_s`.
2. Jika dua event hampir simultan dari bola berbeda, gunakan XY contact untuk menghindari pairing silang; jika GT location tidak tersedia, jadikan spatial matching opsional dan dokumentasikan ambiguitas.
3. Cari **one-to-one assignment** yang memaksimalkan jumlah valid match (misalnya Hungarian assignment dengan infeasible pairs diblokir, objective pertama cardinality, kedua time/space cost).
4. `TP = matched pairs`; `FP = unmatched prediction`; `FN = unmatched ground truth`.
5. Ekspor `match_pairs.csv`, `false_positives.csv`, `false_negatives.csv`.

## Event metrics
\[
Precision = TP/(TP+FP)
\]
\[
Recall = TP/(TP+FN)
\]
\[
F1 = 2PR/(P+R)
\]
Jika denominators nol, tentukan conventions secara eksplisit sebelum analisis (mis. undefined -> null, bukan nilai sempurna otomatis).

## Count metrics
```text
N_gt = #valid GT events in evaluated interval
N_pred = #accepted pred events in interval
absolute_error = abs(N_pred - N_gt)
APE_percent = 100 * abs(N_pred - N_gt) / N_gt  (N_gt > 0)
signed_error = N_pred - N_gt
```
Jika N_gt=0, APE **undefined**; pakai absolute error. Total count yang tepat bisa terjadi jika FP=FN (cancel out), karena itu F1 wajib.

## Detector metrics
Compute mAP50, mAP50-95, precision, recall pada box test. Detection mAP tinggi tidak menjamin event F1 tinggi.

## Event localization
- Mean/median absolute timestamp error pada matched TP.
- Spatial error pada kontak jika manual XY valid.
- FPS throughput, total seconds processed, hardware label.

## Split edges
Jangan nilai candidate yang source event-nya berada di buffer exclusion. Jika perlu inference clip context, proses margin di luar eval interval tetapi filter scored events ke interval inti; dedup antar segmen.

## Example synthetic (BUKAN hasil video)
GT=100, pred=100, TP=90 → FP=10, FN=10 → APE=0% tetapi precision=recall=F1=90%. Ini menunjukkan total count error saja menyesatkan.

"""Bandingkan event prediksi videofull.mp4 dengan GT manual pada satu segmen: TP/FP/FN, APE, error ber-timestamp.

Pakai: python scripts/evaluate_test_video.py --start 300 --end 360 [--gt CSV] [--pred CSV] [--tol 0.1]
Prediksi dan GT dibatasi ke [start, end] detik. GT yang dipakai hanya baris review_status != excluded.
"""
import argparse, csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument("--start", type=float, required=True, help="awal segmen (detik)")
p.add_argument("--end", type=float, required=True, help="akhir segmen (detik)")
p.add_argument("--gt", type=Path, default=None, help="default data/annotations/gt_segment_<start>_<end>.csv")
p.add_argument("--pred", type=Path, default=ROOT / "artifacts/runs/Phase4_bridging/bridging_events_full.csv")
p.add_argument("--tol", type=float, default=0.1, help="toleransi detik")
p.add_argument("--out", type=Path, default=None, help="default artifacts/runs/Phase5_gt_eval/<start>_<end>")
a = p.parse_args()
tag = f"{a.start:g}_{a.end:g}"
a.gt = a.gt or ROOT / f"data/annotations/gt_segment_{tag}.csv"
a.out = a.out or ROOT / f"artifacts/runs/Phase5_gt_eval/{tag}"
a.out.mkdir(parents=True, exist_ok=True)

def times(path, skip_excluded=False):
    with path.open(newline="", encoding="utf8") as f:
        return sorted(t for r in csv.DictReader(f)
                      if not (skip_excluded and r.get("review_status") == "excluded")
                      and a.start <= (t := float(r["time_s"])) < a.end)

gt, pred = times(a.gt, True), times(a.pred)
used, tp, errors = set(), [], []
for g in gt:  # pencocokan greedy satu-ke-satu, terdekat dalam toleransi
    best = min((i for i in range(len(pred)) if i not in used and abs(pred[i] - g) <= a.tol + 1e-6),  # +1e-6: hindari galat float pada selisih tepat 3 frame
               key=lambda i: abs(pred[i] - g), default=None)
    if best is None: errors.append({"type": "FN", "time_s": round(g, 3), "cause": "", "fix": ""})
    else: used.add(best); tp.append((g, pred[best]))
errors += [{"type": "FP", "time_s": round(pred[i], 3), "cause": "", "fix": ""} for i in range(len(pred)) if i not in used]
errors.sort(key=lambda e: e["time_s"])
P = len(tp) / len(pred) if pred else 0; R = len(tp) / len(gt) if gt else 0
rep = {"gt_count": len(gt), "pred_count": len(pred), "TP": len(tp), "FP": len(pred) - len(tp), "FN": len(gt) - len(tp),
       "precision": round(P, 4), "recall": round(R, 4), "f1": round(2 * P * R / (P + R), 4) if P + R else 0,
       "APE_percent": round(abs(len(pred) - len(gt)) / len(gt) * 100, 2) if gt else None, "segment_s": [a.start, a.end], "tolerance_s": a.tol}
(a.out / "eval_vs_gt.json").write_text(json.dumps(rep, indent=1))
with (a.out / "errors.csv").open("w", newline="", encoding="utf8") as f:  # isi cause/fix setelah melihat klip
    w = csv.DictWriter(f, fieldnames=["type", "time_s", "cause", "fix"]); w.writeheader(); w.writerows(errors)
print(json.dumps(rep, indent=1)); print(f"{len(errors)} error -> {a.out / 'errors.csv'}")

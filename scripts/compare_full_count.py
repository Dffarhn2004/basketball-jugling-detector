"""Bandingkan GT manual video penuh (annotate_full.py) dengan hitungan pipeline: total, APE, per menit, dan per event.

Pakai:
    python scripts/compare_full_count.py                      # rentang = 0 .. posisi terjauh yang sudah dianotasi
    python scripts/compare_full_count.py --start 0 --end 600  # rentang tertentu (detik)
Keluaran di artifacts/runs/Phase5_full_gt_eval/: summary.json, per_minute.csv, errors.csv.

Catatan: GT yang ditandai saat memutar video memiliki jeda reaksi manusia. Skrip memperkirakan jeda itu (median selisih)
dan mengoreksinya sebelum pencocokan per event. Perbandingan per menit dan total tidak bergantung pada jeda.
"""
from __future__ import annotations
import argparse, csv, json, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def estimate_offset(gt: list[float], pred: list[float], span: float = 0.5, step: float = 0.01, tol: float = 0.08) -> float:
    """Geseran (detik) yang paling banyak mencocokkan GT-geser dengan prediksi dalam `tol`; 0 bila GT atau prediksi kosong.

    Memindai offset, bukan memakai tetangga terdekat: bounce muncul sekitar 0,44 s sekali, sehingga tetangga terdekat
    keliru bila jeda reaksi mendekati separuh jarak itu. Imbang -> pilih offset terkecil.
    Hasil: nilai t sehingga (gt - offset) ~ pred.
    """
    if not gt or not pred: return 0.0
    from bisect import bisect_left
    ps = sorted(pred)

    def hits(o: float) -> int:
        c = 0
        for g in gt:
            x = g - o; k = bisect_left(ps, x)
            near = min((abs(ps[i] - x) for i in (k - 1, k) if 0 <= i < len(ps)), default=9)
            c += near <= tol
        return c
    n = int(span / step); idx = list(range(-n, n + 1)); h = {i: hits(i * step) for i in idx}; top = max(h.values())
    runs, cur = [], []
    for i in idx:                       # rentang offset berurutan yang sama-sama terbaik
        if h[i] == top: cur.append(i)
        elif cur: runs.append(cur); cur = []
    if cur: runs.append(cur)
    run = max(runs, key=lambda r: (len(r), -abs(sum(r) / len(r))))   # terpanjang; imbang -> paling dekat 0
    return round(sum(run) / len(run) * step, 6)                       # tengah rentang, bukan tepinya


def match(gt: list[float], pred: list[float], tol: float) -> tuple[list[tuple[float, float]], list[float], list[float]]:
    """Pencocokan satu-ke-satu serakah (terdekat dalam toleransi). Mengembalikan (pasangan, FN, FP)."""
    used: set[int] = set(); pairs, fn = [], []
    for g in sorted(gt):
        cand = [i for i in range(len(pred)) if i not in used and abs(pred[i] - g) <= tol + 1e-6]
        if cand:
            i = min(cand, key=lambda i: abs(pred[i] - g)); used.add(i); pairs.append((g, pred[i]))
        else:
            fn.append(g)
    return pairs, fn, [pred[i] for i in range(len(pred)) if i not in used]


def per_minute(gt: list[float], pred: list[float], start: float, end: float) -> list[dict]:
    rows = []
    for m in range(int(start // 60), int((end - 1e-9) // 60) + 1):
        lo, hi = max(start, m * 60), min(end, (m + 1) * 60)
        g = sum(lo <= t < hi for t in gt); p = sum(lo <= t < hi for t in pred)
        rows.append({"menit": m + 1, "gt": g, "pred": p, "selisih": p - g, "ape_persen": round(abs(p - g) / g * 100, 2) if g else None, "durasi_s": round(hi - lo, 1)})
    return rows


def read_times(path: Path, fps: float = 30.0, skip_excluded: bool = False) -> list[float]:
    """Waktu event = frame_idx / fps (sama untuk GT dan prediksi agar tidak ada selisih akibat 29,97 vs 30)."""
    with path.open(newline="", encoding="utf8") as f:
        return sorted(int(r["frame_idx"]) / fps for r in csv.DictReader(f) if not (skip_excluded and r.get("review_status") == "excluded"))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gt", type=Path, default=ROOT / "data/annotations/gt_full_video.csv")
    ap.add_argument("--pred", type=Path, default=ROOT / "artifacts/runs/Phase4_bridging/bridging_events_full.csv")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None, help="default: posisi terjauh dari <gt>.progress.json")
    ap.add_argument("--fps", type=float, default=30.0, help="fps untuk mengubah frame ke detik (default 30, sama dengan pipeline)")
    ap.add_argument("--tol", type=float, default=0.2, help="toleransi per event setelah koreksi jeda (detik)")
    ap.add_argument("--out", type=Path, default=ROOT / "artifacts/runs/Phase5_full_gt_eval")
    a = ap.parse_args()
    end = a.end
    if end is None:
        prog = a.gt.with_suffix(".progress.json")
        if not prog.exists(): raise SystemExit("Tidak ada progress; berikan --end (detik) secara eksplisit.")
        j = json.loads(prog.read_text()); end = j["max_frame"] / a.fps
        end = (end // 60) * 60 if end % 60 else end   # hanya menit penuh yang sudah selesai ditonton
    gt_all = read_times(a.gt, a.fps, skip_excluded=True); pred_all = read_times(a.pred, a.fps)
    gt = [t for t in gt_all if a.start <= t < end]; pred = [t for t in pred_all if a.start <= t < end]
    off = estimate_offset(gt, pred); gt_adj = [min(max(t - off, a.start), end - 1e-6) for t in gt]   # dijepit ke rentang agar total per menit = total GT
    pairs, fn, fp = match(gt_adj, pred, a.tol)
    tp = len(pairs); P = tp / len(pred) if pred else 0; R = tp / len(gt) if gt else 0
    summary = {"range_s": [a.start, end], "gt_count": len(gt), "pred_count": len(pred), "selisih": len(pred) - len(gt),
               "APE_persen": round(abs(len(pred) - len(gt)) / len(gt) * 100, 2) if gt else None,
               "offset_jeda_reaksi_s": round(off, 3), "tol_s": a.tol, "TP": tp, "FP": len(fp), "FN": len(fn),
               "precision": round(P, 4), "recall": round(R, 4), "f1": round(2 * P * R / (P + R), 4) if P + R else 0,
               "catatan": "pencocokan per event hanya bermakna bila jeda reaksi relatif konstan; total dan per menit tidak bergantung padanya"}
    pm = per_minute(gt_adj, pred, a.start, end)
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf8")
    with (a.out / "per_minute.csv").open("w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=list(pm[0].keys()) if pm else ["menit"]); w.writeheader(); w.writerows(pm)
    errs = sorted([{"type": "FN", "time_s": round(t + off, 3), "cause": "", "fix": ""} for t in fn] +
                  [{"type": "FP", "time_s": round(t, 3), "cause": "", "fix": ""} for t in fp], key=lambda e: e["time_s"])
    with (a.out / "errors.csv").open("w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=["type", "time_s", "cause", "fix"]); w.writeheader(); w.writerows(errs)
    print(json.dumps(summary, indent=1, ensure_ascii=False))
    print("\nmenit  GT  pred  selisih")
    for r in pm: print(f"{r['menit']:>5} {r['gt']:>4} {r['pred']:>5} {r['selisih']:>+7}")
    print(f"\n-> {a.out}")


if __name__ == "__main__":
    main()

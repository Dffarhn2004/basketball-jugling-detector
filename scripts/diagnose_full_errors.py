"""Diagnosis otomatis penyebab FN pada perbandingan seluruh video, dari deteksi mentah dan lintasan (parameter akhir).

Untuk tiap FN di errors.csv: cari titik padanan pada linimasa pipeline (GT dikoreksi dengan geseran lokal), lalu periksa
 - apakah detector menembak bola dekat lantai di sekitar titik itu (deteksi mentah, ambang tracking 0,3 dan 0,25),
 - apakah ada lintasan yang melewati titik itu, dan syarat mana dari aturan event yang gagal.
Keluaran: artifacts/runs/Phase5_full_gt_eval/fn_diagnosis.csv dan ringkasan di layar. Ini analisis dari data, bukan penilaian visual.
Pakai: python scripts/diagnose_full_errors.py
"""
from __future__ import annotations
import csv, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import phase4_bridging as pb  # noqa: E402

GATE, MAX_MISS, FLOOR, MOVE, WIN, DEDUP = 1.5, 4, 0.65, 15, 5, 0.2
EVAL = ROOT / "artifacts/runs/Phase5_full_gt_eval"
N = 36003


def load_full_raw():
    raw = pb.load_raw()
    d = defaultdict(list)
    for r in pb.read(pb.OUT / "raw_1800_end.csv"):
        x1, y1, x2, y2 = (float(r[k]) for k in ("x1", "y1", "x2", "y2"))
        d[int(r["frame_idx"])].append(((x1 + x2) / 2, (y1 + y2) / 2, y2, max(x2 - x1, y2 - y1), float(r["confidence"])))
    raw.update(d)
    return raw


def candidates(track, tf, win=6):
    """Titik terendah lintasan di sekitar tf dan hasil tiap syarat aturan event (sesuai pb.events)."""
    p = track["pts"]; fr = np.array([a[0] for a in p]); cy = np.array([a[2] for a in p]); by = np.array([a[3] for a in p])
    idx = [i for i in range(len(p)) if abs(fr[i] - tf) <= win]
    if not idx: return None
    i = max(idx, key=lambda k: cy[k])                     # titik terendah (y terbesar) di jendela
    r = {"track": track["id"], "frame": int(fr[i]), "n_pts": len(p), "bottom_frac": round(float(by[i]) / pb.H, 2), "reasons": []}
    a = int(np.searchsorted(fr, fr[i] - WIN, side="left")); b = int(np.searchsorted(fr, fr[i] + WIN, side="right"))
    if len(p) < 5: r["reasons"].append("lintasan terlalu pendek (< 5 titik)")
    if i == 0 or i == len(p) - 1 or a >= i or b <= i + 1: r["reasons"].append("tidak ada titik sebelum/sesudah dalam jendela ±5 frame (lintasan terpotong)")
    else:
        drop = cy[i] - cy[a:i].min(); rise = cy[i] - cy[i + 1:b].min(); r["drop"], r["rise"] = round(float(drop), 1), round(float(rise), 1)
        if by[i] < FLOOR * pb.H: r["reasons"].append("sisi bawah kotak di atas zona lantai")
        if drop < MOVE or rise < MOVE: r["reasons"].append(f"turun/naik < {MOVE} px (turun {drop:.0f}, naik {rise:.0f})")
        if cy[i] < cy[a:b].max(): r["reasons"].append("bukan titik terendah dalam jendela")
    return r


def main() -> None:
    raw = load_full_raw(); tracks = pb.track(raw, gate=GATE, max_miss=MAX_MISS, n=N)
    events = pb.events(tracks, floor=FLOOR, min_drop=MOVE, min_rise=MOVE)
    ev_frames = sorted(e["frame_idx"] for e in events)
    with (pb.OUT / "bridging_events_full.csv").open() as f: saved = sorted(int(r["frame_idx"]) for r in csv.DictReader(f))
    assert ev_frames == saved, f"rekonstruksi event tidak sama dengan berkas tersimpan ({len(ev_frames)} vs {len(saved)})"
    with (ROOT / "data/annotations/gt_full_video.csv").open(encoding="utf8") as f: gt = sorted(int(r["frame_idx"]) for r in csv.DictReader(f))
    with (EVAL / "errors.csv").open(encoding="utf8") as f: errs = list(csv.DictReader(f))

    rows = []
    for e in errs:
        if e["type"] != "FN": continue
        g = round(float(e["time_s"]) * 30)
        near = [(x, min(ev_frames, key=lambda p: abs(p - x))) for x in gt if abs(x - g) <= 90 and x != g]
        offs = [x - p for x, p in near if abs(x - p) <= 12]
        off = int(round(float(np.median(offs)))) if offs else -5
        tf = g - off
        lo, hi = tf - 6, tf + 6
        floor_px = FLOOR * pb.H
        dets = [(f, d) for f in range(max(0, lo), min(N - 1, hi) + 1) for d in raw.get(f, []) if d[2] >= floor_px]
        hi_conf = [x for x in dets if x[1][4] >= 0.3]; lo_conf = [x for x in dets if 0.25 <= x[1][4] < 0.3]
        frames_hi = len({f for f, _ in hi_conf})
        cands = [c for t in tracks if (c := candidates(t, tf)) and abs(c["frame"] - tf) <= 6 and c["bottom_frac"] >= FLOOR - 0.08]
        has_event = [p for p in ev_frames if abs(p - tf) <= 4]
        # kategori
        if has_event: cat, why = "event ada tetapi tidak tercocokkan", f"event pipeline di frame {has_event[0]} (selisih {has_event[0] - tf:+d} frame dari titik padanan)"
        elif not dets: cat, why = "detector tidak menembak", "tidak ada deteksi (confidence ≥ 0,25) dengan sisi bawah di zona lantai pada ±6 frame"
        elif not hi_conf: cat, why = "confidence terlalu rendah", f"deteksi ada ({len(lo_conf)}) tetapi confidence 0,25–0,3 (di bawah ambang tracking 0,3)"
        elif not cands: cat, why = "deteksi tidak tersambung ke lintasan", f"{frames_hi}/13 frame punya deteksi, tetapi tidak ada lintasan yang melewati titik itu"
        else:
            best = min(cands, key=lambda c: len(c["reasons"]))
            cat = "aturan event tidak terpenuhi"; why = "; ".join(best["reasons"]) or "syarat terpenuhi namun event hilang (kemungkinan digabung oleh aturan 0,2 s)"
            if any("terpotong" in r or "pendek" in r for r in best["reasons"]): cat = "lintasan terpotong"
            elif any("turun/naik" in r for r in best["reasons"]): cat = "gerak turun/naik terlalu kecil"
            elif not best["reasons"]: cat = "digabung aturan 0,2 s"
        rows.append({"time_s": e["time_s"], "gt_frame": g, "geseran_lokal_frame": off, "target_frame": tf, "frame_dengan_deteksi_conf>=0.3": f"{frames_hi}/13",
                     "kategori": cat, "keterangan": why})
    out = EVAL / "fn_diagnosis.csv"
    with out.open("w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    for r in rows: print(f"{float(r['time_s']):9.3f}s off{r['geseran_lokal_frame']:>+3} det {r['frame_dengan_deteksi_conf>=0.3']:>5} | {r['kategori']:<38} | {r['keterangan']}")
    print("\nringkasan:", dict(Counter(r["kategori"] for r in rows)), "\n->", out)


if __name__ == "__main__":
    main()

"""Gambar untuk laporan Bagian 5.4 dari data nyata (deteksi mentah E2, 0-60 s) dengan parameter akhir.

  laporan/gambar/iou_dekat_kontak.png      IoU antar kotak deteksi pada frame berurutan: dekat kontak vs lainnya
  laporan/gambar/lintasan_aturan_event.png Lintasan bola, zona lantai, bounce terdeteksi, pembalikan yang ditolak, GT
Statistik yang dipakai di teks disimpan di artifacts/runs/Phase4_bridging/figure_stats.json.
Pakai: python scripts/make_pipeline_figures.py
"""
from __future__ import annotations
import json, sys
from collections import defaultdict
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import phase4_bridging as pb  # noqa: E402
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

GATE, MAX_MISS, FLOOR, MIN_MOVE = 1.5, 4, 0.65, 15      # parameter akhir (dari dev 0-30 s)
OUT = ROOT / "laporan/gambar"
INK, MID, LIGHT = "#111111", "#7a7a7a", "#d9d9d9"
COMMA = FuncFormatter(lambda x, _: f"{x:.1f}".replace(".", ","))


def setup_style() -> None:
    names = {f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({"font.family": "Calibri" if "Calibri" in names else "DejaVu Sans", "font.size": 10, "axes.edgecolor": "#555",
                         "axes.spines.top": False, "axes.spines.right": False, "axes.labelcolor": INK, "xtick.color": "#333", "ytick.color": "#333"})


def iou(a, b) -> float:
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0])); iy = max(0, min(a[3], b[3]) - max(a[1], b[1])); i = ix * iy
    return i / ((a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - i + 1e-9)


def iou_stats(tracks, events):
    boxes = defaultdict(list)
    for r in pb.read(pb.OUT / "raw_0_60s.csv"):
        boxes[int(r["frame_idx"])].append(tuple(float(r[k]) for k in ("x1", "y1", "x2", "y2")))

    def find(f, cx, cy):
        for b in boxes[f]:
            if abs((b[0] + b[2]) / 2 - cx) < 1e-6 and abs((b[1] + b[3]) / 2 - cy) < 1e-6: return b

    ev_frames = defaultdict(list)
    for e in events: ev_frames[e["track_id"]].append(e["frame_idx"])
    near, far = [], []
    for t in tracks:
        p = t["pts"]
        for a, b in zip(p, p[1:]):
            if b[0] - a[0] != 1: continue
            ba, bb = find(a[0], a[1], a[2]), find(b[0], b[1], b[2])
            if ba and bb: (near if any(abs(b[0] - f) <= 4 for f in ev_frames[t["id"]]) else far).append(iou(ba, bb))
    return np.array(near), np.array(far)


def fig_iou(near, far, stats) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 3.2)); bins = np.linspace(0, 1, 26)
    ax.hist(far, bins=bins, weights=np.ones_like(far) / len(far) * 100, color=LIGHT, edgecolor="#9a9a9a", label=f"Frame lain (n = {len(far):,})".replace(",", "."))
    ax.hist(near, bins=bins, weights=np.ones_like(near) / len(near) * 100, color=MID, alpha=.85, edgecolor=INK, label=f"Dekat kontak, ±4 frame (n = {len(near):,})".replace(",", "."))
    ymax = ax.get_ylim()[1]; ax.set_ylim(0, ymax * 1.18)
    ax.axvline(0.2, color=INK, ls="--", lw=1.1); ax.text(0.19, ymax * 1.12, "ambang IoU 0,2\n(ByteTrack, bawaan)", fontsize=8.5, va="top", ha="right")
    for v, c in ((stats["median_iou_far"], "#666"), (stats["median_iou_near"], INK)):
        ax.plot([v, v], [0, ymax], color=c, lw=1.2, ls=":")
        ax.text(v + .008, ymax * 1.02, "median " + f"{v:.2f}".replace(".", ","), ha="left", fontsize=8.5, color=c, fontweight="bold")
    ax.xaxis.set_major_formatter(COMMA)
    ax.set_xlabel("IoU antara kotak deteksi pada dua frame berurutan"); ax.set_ylabel("Persentase tautan (%)")
    ax.legend(frameon=False, fontsize=8.5, loc="upper right", bbox_to_anchor=(1.0, 0.86)); ax.set_xlim(0, 1)
    fig.tight_layout(); fig.savefig(OUT / "iou_dekat_kontak.png", dpi=200); plt.close(fig)


def fig_trajectory(tracks, events, gt):
    f0, f1 = 196, 335
    tin = [t for t in tracks if sum(f0 <= a[0] <= f1 for a in t["pts"]) >= 20]
    styles = [("-", "#444"), ("--", "#808080"), (":", "#222")]
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    ax.axhspan(FLOOR, 1.0, color="#ececec", zorder=0); ax.axhline(FLOOR, color="#555", ls="--", lw=1)
    ax.text(f0 / pb.FPS + .03, FLOOR + .014, "zona lantai: sisi bawah kotak ≥ 0,65 × tinggi frame", fontsize=8.5, va="top", color="#333")
    ev_in, rej_in = [], []
    for k, t in enumerate(tin):
        pts = [a for a in t["pts"] if f0 <= a[0] <= f1]
        fr = np.array([a[0] for a in pts]); by = np.array([a[3] for a in pts]) / pb.H; cy = np.array([a[2] for a in pts]); ts = fr / pb.FPS
        ls, col = styles[k % 3]; ax.plot(ts, by, ls, color=col, lw=1.3, zorder=2, label=f"lintasan bola {k + 1}")
        ev_in += [e for e in events if e["track_id"] == t["id"] and f0 <= e["frame_idx"] <= f1]
        rej_in += [(ts[i], by[i], int(fr[i])) for i in range(5, len(pts) - 5)
                   if cy[i] == cy[i - 5:i + 6].max() and by[i] < FLOOR and cy[i] - cy[i - 5:i].min() >= MIN_MOVE and cy[i] - cy[i + 1:i + 6].min() >= MIN_MOVE]
    for k, e in enumerate(ev_in):
        ax.plot(e["frame_idx"] / pb.FPS, e["bottom_y"] / pb.H, "o", color=INK, ms=8, zorder=5, label="bounce terdeteksi" if k == 0 else None)
    for k, (x, y, _) in enumerate(rej_in):
        ax.plot(x, y, "X", color=INK, ms=9, mfc="white", mew=1.5, zorder=5, label="pembalikan di atas lantai (ditolak)" if k == 0 else None)
    g_in = [g for g in gt if f0 <= g <= f1]
    ax.plot([g / pb.FPS for g in g_in], [1.025] * len(g_in), "|", color=INK, ms=11, mew=1.6, clip_on=False, label="GT manual")
    if ev_in:                                                       # jendela ±5 frame pada satu event
        e = sorted(ev_in, key=lambda e: e["frame_idx"])[len(ev_in) // 2]; c = e["frame_idx"] / pb.FPS
        ax.axvspan(c - 5 / pb.FPS, c + 5 / pb.FPS, ymin=.02, ymax=.98, color="#bdbdbd", alpha=.5, zorder=1)
        ax.annotate("jendela ±5 frame di sekitar satu bounce:\nturun ≥ 15 px sebelum, naik ≥ 15 px sesudah", xy=(c, .93), xytext=(c - .35, .985),
                    fontsize=8, ha="right", va="bottom", arrowprops=dict(arrowstyle="->", color="#333", lw=.9))
    ax.set_ylim(1.0, .20); ax.set_xlim(f0 / pb.FPS, f1 / pb.FPS); ax.set_xlabel("Waktu (detik)")
    ax.set_ylabel("Posisi sisi bawah kotak\n(0 = atas frame, 1 = bawah)"); ax.yaxis.set_major_formatter(COMMA)
    ax.legend(frameon=False, fontsize=8.3, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3)
    fig.tight_layout(); fig.savefig(OUT / "lintasan_aturan_event.png", dpi=200); plt.close(fig)
    return {"tracks_in_window": [t["id"] for t in tin], "window_frames": [f0, f1], "events_in_window": sorted(e["frame_idx"] for e in ev_in),
            "rejected_reversals": [r[2] for r in rej_in], "gt_in_window": g_in}


def main() -> None:
    setup_style(); OUT.mkdir(parents=True, exist_ok=True)
    tracks = pb.track(pb.load_raw(), gate=GATE, max_miss=MAX_MISS)
    events = pb.events(tracks, floor=FLOOR, min_drop=MIN_MOVE, min_rise=MIN_MOVE)
    near, far = iou_stats(tracks, events)
    stats = {"links_near": len(near), "links_far": len(far), "median_iou_near": round(float(np.median(near)), 2), "median_iou_far": round(float(np.median(far)), 2),
             "share_below_0.2_near": round(float((near < .2).mean() * 100), 1), "share_below_0.2_far": round(float((far < .2).mean() * 100), 1),
             "share_below_0.5_near": round(float((near < .5).mean() * 100), 1), "share_below_0.5_far": round(float((far < .5).mean() * 100), 1)}
    fig_iou(near, far, stats)
    gt = [int(r["frame_idx"]) for r in pb.read(ROOT / "data/annotations/bounce_events_gt_v2.csv") if r["review_status"] != "excluded"]
    stats.update(fig_trajectory(tracks, events, gt))
    (pb.OUT / "figure_stats.json").write_text(json.dumps(stats, indent=1))
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()

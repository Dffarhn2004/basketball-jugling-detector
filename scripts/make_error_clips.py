"""Klip lambat (0.25x) di sekitar error evaluasi, dengan penanda GT/PRED, nomor frame, dan label jenis error.

Dua cara pakai:
  1) Dari errors.csv hasil compare_full_count.py (GT video penuh):
       python scripts/make_error_clips.py --errors artifacts/runs/Phase5_full_gt_eval/errors.csv
  2) Titik manual pada segmen ber-GT (kompatibel dengan versi lama):
       python scripts/make_error_clips.py <start> <end> <detik_pusat> [<detik_pusat> ...]
Waktu = frame / 30. Penanda GT memakai waktu GT apa adanya (pada GT video penuh bisa bergeser beberapa frame karena jeda reaksi).
"""
from __future__ import annotations
import argparse, csv
from pathlib import Path
import cv2

ROOT = Path(__file__).resolve().parents[1]
FPS = 30.0


def frames_of(path: Path) -> set[int]:
    with path.open(encoding="utf8", newline="") as f:
        return {int(r["frame_idx"]) for r in csv.DictReader(f)}


def clip_name(idx: int, kind: str, t: float) -> str:
    return f"{idx:02d}_{kind}_{t:08.3f}s.mp4"


def make_clip(cap, out: Path, center_s: float, gt: set[int], pred: set[int], label: str, half: int = 45) -> None:
    fps = cap.get(cv2.CAP_PROP_FPS) or FPS
    c = round(center_s * FPS); a, b = max(0, c - half), c + half
    cap.set(cv2.CAP_PROP_POS_FRAMES, a)
    w = cv2.VideoWriter(str(out), cv2.VideoWriter_fourcc(*"mp4v"), fps / 4, (int(cap.get(3)), int(cap.get(4))))
    for f in range(a, b + 1):
        ok, img = cap.read()
        if not ok: break
        tags = (["GT"] if f in gt else []) + (["PRED"] if f in pred else [])
        cv2.putText(img, f"{label}  frame {f}  t={f / FPS:.3f}s", (15, 30), 0, .8, (0, 255, 0), 2)
        if tags:
            cv2.putText(img, " + ".join(tags), (15, 70), 0, 1.2, (0, 0, 255) if "GT" in tags else (255, 128, 0), 3)
            for _ in range(8): w.write(img)  # tahan penanda lebih lama
        w.write(img)
    w.release()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pos", nargs="*", help="<start> <end> <detik>... (mode lama)")
    ap.add_argument("--errors", type=Path, help="errors.csv dari compare_full_count.py")
    ap.add_argument("--gt", type=Path, default=ROOT / "data/annotations/gt_full_video.csv")
    ap.add_argument("--pred", type=Path, default=ROOT / "artifacts/runs/Phase4_bridging/bridging_events_full.csv")
    ap.add_argument("--video", type=Path, default=ROOT / "videofull.mp4")
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args()
    cap = cv2.VideoCapture(str(a.video))
    if a.errors:
        out = a.out or a.errors.parent / "clips"; out.mkdir(parents=True, exist_ok=True)
        gt, pred = frames_of(a.gt), frames_of(a.pred)
        with a.errors.open(encoding="utf8", newline="") as f: errs = list(csv.DictReader(f))
        for i, e in enumerate(errs, 1):
            t = float(e["time_s"]); make_clip(cap, out / clip_name(i, e["type"], t), t, gt, pred, f"#{i} {e['type']}")
            print(f"{i:02d}  {e['type']}  {t:8.3f} s ({int(t // 60)}:{t % 60:05.2f})  -> {clip_name(i, e['type'], t)}")
        print(f"\n{len(errs)} klip -> {out}")
    else:
        if len(a.pos) < 3: ap.error("beri --errors CSV, atau <start> <end> <detik>...")
        s, e, times = a.pos[0], a.pos[1], [float(x) for x in a.pos[2:]]
        out = a.out or ROOT / f"artifacts/runs/Phase5_gt_eval/{s}_{e}/clips"; out.mkdir(parents=True, exist_ok=True)
        gt = frames_of(ROOT / f"data/annotations/gt_segment_{s}_{e}.csv"); pred = frames_of(a.pred)
        for i, t in enumerate(times, 1):
            make_clip(cap, out / f"err_{t:.3f}.mp4", t, gt, pred, f"#{i}")
        print(*sorted(p.name for p in out.iterdir()))


if __name__ == "__main__":
    main()

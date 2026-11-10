"""Anotasi GT bounce untuk SELURUH video dengan tombol B (versi nyaman untuk sesi panjang, bisa dilanjutkan).

Pakai:
    python scripts/annotate_full.py videofull.mp4
    python scripts/annotate_full.py videofull.mp4 --speed 0.5 --lag-ms 150
Hasil: data/annotations/gt_full_video.csv (format sama dengan gt_segment_*.csv). Posisi terakhir disimpan di
<output>.progress.json, sehingga menjalankan perintah yang sama lagi melanjutkan dari tempat berhenti.

Tombol:
  spasi  putar / jeda          b  tandai bounce (saat memutar, waktu dikurangi --lag-ms; saat jeda: frame persis)
  u      batalkan tanda terakhir   a / d (atau panah)  mundur / maju 1 frame (otomatis jeda)
  r      mundur 3 detik            [ / ]  mundur / maju 10 detik        1 2 3 4  kecepatan 0,25x 0,5x 1x 2x
  q      simpan dan keluar
Indikator hijau "ditandai xN" muncul bila ada tanda di sekitar frame ini (untuk mencegah tanda ganda saat menonton ulang).
Dua bola yang memantul bersamaan boleh ditandai dua kali di frame yang sama.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from bounce_annotator import FIELDS, load, save  # noqa: E402

SPEEDS = {ord("1"): 0.25, ord("2"): 0.5, ord("3"): 1.0, ord("4"): 2.0}
KEY_LEFT, KEY_RIGHT = 2424832, 2555904  # panah di Windows (waitKeyEx)


def marked_near(frames: list[int], frame: int, radius: int = 3) -> int:
    """Jumlah tanda dalam radius frame dari `frame`."""
    return sum(abs(f - frame) <= radius for f in frames)


def lag_adjusted(frame: int, lag_ms: float, fps: float, paused: bool, start: int = 0) -> int:
    """Frame yang dicatat: saat memutar dikurangi waktu reaksi; saat jeda frame persis."""
    return frame if paused else max(start, frame - round(lag_ms / 1000 * fps))


def minute_stats(frames: list[int], frame: int, fps: float) -> tuple[int, int]:
    """(indeks menit saat ini mulai 0, jumlah tanda pada menit itu)."""
    m = int(frame / fps // 60)
    return m, sum(int(f / fps // 60) == m for f in frames)


def new_row(next_id: int, frame: int, fps: float) -> dict:
    return dict(event_id=f"GT-{next_id:04d}", frame_idx=frame, time_s=f"{frame / fps:.6f}", x_contact_px="", y_contact_px="",
                confidence="uncertain", review_status="unreviewed", segment_id=f"{frame / fps:.3f}",
                notes="manual full-video annotation")


def main() -> None:
    import cv2
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", type=Path)
    ap.add_argument("--output", type=Path, default=ROOT / "data/annotations/gt_full_video.csv")
    ap.add_argument("--start", type=float, default=None, help="mulai dari detik ini (default: lanjut dari posisi terakhir)")
    ap.add_argument("--speed", type=float, default=0.5, help="kecepatan awal (default 0.5)")
    ap.add_argument("--lag-ms", type=float, default=150.0, help="kompensasi waktu reaksi saat memutar (default 150 ms)")
    a = ap.parse_args()

    prog_path = a.output.with_suffix(".progress.json")
    rows = load(a.output)
    cap = cv2.VideoCapture(str(a.video)); fps = cap.get(cv2.CAP_PROP_FPS) or 30.0; total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    prog = json.loads(prog_path.read_text()) if prog_path.exists() else {"position": 0, "max_frame": 0}
    frame = int(a.start * fps) if a.start is not None else int(prog["position"]); max_frame = int(prog["max_frame"])
    next_id = max([int(r["event_id"].split("-")[-1]) for r in rows if r["event_id"].split("-")[-1].isdigit()] or [0]) + 1
    speed, paused, flash, undo_stack = a.speed, True, 0, []
    cv2.namedWindow("GT full video", cv2.WINDOW_NORMAL); cv2.resizeWindow("GT full video", 1120, 630)

    def persist() -> None:
        rows.sort(key=lambda r: int(r["frame_idx"])); save(a.output, rows)
        prog_path.write_text(json.dumps({"position": frame, "max_frame": max_frame, "fps": fps, "video": a.video.name}))

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame); pos = frame
    while frame < total:
        if pos != frame: cap.set(cv2.CAP_PROP_POS_FRAMES, frame); pos = frame
        ok, img = cap.read(); pos += 1
        if not ok: break
        max_frame = max(max_frame, frame)
        frames = [int(r["frame_idx"]) for r in rows]; m, mc = minute_stats(frames, frame, fps); near = marked_near(frames, frame)
        t = frame / fps
        cv2.rectangle(img, (0, 0), (img.shape[1], 56), (0, 0, 0), -1)
        cv2.putText(img, f"{int(t // 60):02d}:{t % 60:05.2f}  frame {frame}/{total}  {'JEDA' if paused else f'{speed:g}x'}", (14, 22), 0, .65, (255, 255, 255), 2)
        cv2.putText(img, f"menit {m + 1}: {mc} tanda | total: {len(rows)}  | b=tandai u=batal spasi=putar r=mundur q=keluar", (14, 46), 0, .55, (0, 255, 0), 1)
        if near: cv2.putText(img, f"ditandai x{near}", (img.shape[1] - 260, 90), 0, 1.0, (0, 220, 0), 3)
        if flash > 0: cv2.rectangle(img, (4, 60), (img.shape[1] - 5, img.shape[0] - 5), (0, 0, 255), 6); flash -= 1
        cv2.imshow("GT full video", img)
        key = cv2.waitKeyEx(0 if paused else max(1, int(1000 / (fps * speed))))
        k = key & 0xFF if key not in (KEY_LEFT, KEY_RIGHT) else key
        if k == ord("q"): break
        elif k == ord(" "): paused = not paused
        elif k in SPEEDS: speed = SPEEDS[k]
        elif k == ord("b"):
            f = lag_adjusted(frame, a.lag_ms, fps, paused); rows.append(new_row(next_id, f, fps)); undo_stack.append(next_id); next_id += 1; flash = 3; persist()
        elif k == ord("u") and undo_stack:
            uid = f"GT-{undo_stack.pop():04d}"; rows[:] = [r for r in rows if r["event_id"] != uid]; persist()
        elif k in (ord("a"), KEY_LEFT): frame = max(0, frame - 1); paused = True; continue
        elif k in (ord("d"), KEY_RIGHT): frame = min(total - 1, frame + 1); paused = True; continue
        elif k == ord("r"): frame = max(0, frame - round(3 * fps)); continue
        elif k == ord("["): frame = max(0, frame - round(10 * fps)); continue
        elif k == ord("]"): frame = min(total - 1, frame + round(10 * fps)); continue
        if not paused: frame += 1
        if frame % 300 == 0: persist()
    persist(); cap.release(); cv2.destroyAllWindows()
    print(f"Tersimpan: {len(rows)} tanda -> {a.output}\nPosisi terakhir: {frame / fps:.1f} s (terjauh: {max_frame / fps:.1f} s)")


if __name__ == "__main__":
    main()

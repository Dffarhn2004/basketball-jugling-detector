"""OpenCV helper for first-pass bounce annotation and second-pass review."""
from __future__ import annotations
import argparse, csv, shutil
from pathlib import Path
import cv2

FIELDS = ["event_id","frame_idx","time_s","x_contact_px","y_contact_px","confidence","review_status","segment_id","notes"]
STATUSES = {"approved", "excluded", "unresolved", "unreviewed"}
CONFIDENCES = {"certain", "probable", "uncertain"}


def save(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)


def load(path: Path) -> list[dict]:
    if not path.exists(): return []
    with path.open(newline="", encoding="utf8") as f: return list(csv.DictReader(f))


def review(path: Path, video: Path) -> None:
    rows = load(path)
    if not rows: raise SystemExit("review mode requires an existing CSV")
    backup = path.with_name(path.stem + ".backup-before-review.csv")
    if not backup.exists(): shutil.copy2(path, backup)
    cap = cv2.VideoCapture(str(video)); fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); idx = 0; selected = 0; click = [None]
    def mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN: click[0] = (x, y)
    cv2.namedWindow("bounce review"); cv2.setMouseCallback("bounce review", mouse)
    while True:
        row = rows[selected]; frame = max(0, min(total - 1, int(row["frame_idx"])))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame); ok, img = cap.read()
        if not ok: break
        view = img.copy(); cv2.circle(view, click[0], 5, (0, 0, 255), -1) if click[0] else None
        counts = {s: sum(r.get("review_status", "unreviewed") == s for r in rows) for s in STATUSES}
        text = (f"{row['event_id']}  t={float(row['time_s']):.3f}s frame={frame} "
                f"status={row.get('review_status','unreviewed')} conf={row.get('confidence','uncertain')}\n"
                f"event {selected+1}/{len(rows)}  approved={counts['approved']} excluded={counts['excluded']} "
                f"unresolved={counts['unresolved']} unreviewed={counts['unreviewed']}\n"
                "n/Right next  p/Left prev  a approved  e excluded  u unresolved  c confidence  "
                "+/- frame  x save-click  f full scan  q save/quit")
        for i, line in enumerate(text.splitlines()): cv2.putText(view, line, (15, 25 + i*22), cv2.FONT_HERSHEY_SIMPLEX, .55, (0,255,0), 1)
        cv2.imshow("bounce review", view); key = cv2.waitKey(0) & 0xff
        if key == ord("q"): break
        if key in (ord("n"), 83): selected = min(len(rows)-1, selected+1)
        elif key in (ord("p"), 81): selected = max(0, selected-1)
        elif key in (ord("a"), ord("e"), ord("u")):
            row["review_status"] = {ord("a"):"approved", ord("e"):"excluded", ord("u"):"unresolved"}[key]; save(path, rows)
        elif key == ord("c"):
            row["confidence"] = {"uncertain":"probable", "probable":"certain", "certain":"uncertain"}.get(row.get("confidence","uncertain"), "uncertain"); save(path, rows)
        elif key in (ord("+"), ord("="), ord("-"), ord("_")):
            delta = 1 if key in (ord("+"), ord("=")) else -1; new = max(0, min(total-1, frame+delta)); row["frame_idx"] = str(new); row["time_s"] = f"{new/fps:.6f}"; row["segment_id"] = f"{new/fps:.3f}"; save(path, rows)
        elif key == ord("x") and click[0]: row["x_contact_px"], row["y_contact_px"] = map(str, click[0]); save(path, rows); click[0] = None
        elif key == ord("f"):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0); selected = selected
    save(path, rows); cap.release(); cv2.destroyAllWindows()


def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("video", type=Path); p.add_argument("--output", type=Path, required=True); p.add_argument("--start", type=float, default=0); p.add_argument("--end", type=float); p.add_argument("--review", action="store_true"); args=p.parse_args()
    if args.review: review(args.output, args.video); return
    cap=cv2.VideoCapture(str(args.video)); fps=cap.get(cv2.CAP_PROP_FPS) or 30; total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); start=max(0,int(args.start*fps)); end=min(total,int(args.end*fps)) if args.end else total
    events=load(args.output); next_id=max([int(r['event_id'].split('-')[-1]) for r in events if r.get('event_id','').startswith('GT-') and r['event_id'].split('-')[-1].isdigit()] or [0])+1; frame=start; paused=True; speed=1.0
    while frame < end:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame); ok,img=cap.read()
        if not ok: break
        cv2.putText(img, f"frame={frame} t={frame/fps:.3f}s events={len(events)} | space arrows b u 1/2/4 q", (20,30), cv2.FONT_HERSHEY_SIMPLEX,.55,(0,255,0),1)
        cv2.imshow("bounce annotator",img); key=cv2.waitKey(0 if paused else max(1,int(1000/(fps*speed)))) & 0xff
        if key==ord('q'): break
        if key==ord(' '): paused=not paused
        elif key in (81,ord('a')): frame=max(start,frame-1); paused=True
        elif key in (83,ord('d')): frame=min(end-1,frame+1); paused=True
        elif key in (ord('1'),ord('2'),ord('4')): speed=float(chr(key)); paused=False
        elif key==ord('b'):
            events.append(dict(event_id=f"GT-{next_id:04d}",frame_idx=frame,time_s=f"{frame/fps:.6f}",x_contact_px="",y_contact_px="",confidence="uncertain",review_status="unreviewed",segment_id=f"{frame/fps:.3f}",notes="manual annotation; details pending")); next_id+=1; save(args.output,events)
        elif key==ord('u') and events: events.pop(); save(args.output,events)
        elif not paused: frame+=1
    save(args.output,events); cap.release(); cv2.destroyAllWindows()
if __name__ == "__main__": main()

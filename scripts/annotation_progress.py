"""Print human-review progress for detection and bounce annotation."""
from __future__ import annotations
import argparse, csv
from pathlib import Path

def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument('--manifest',type=Path,default=Path('data/detection/frame_manifest.csv')); p.add_argument('--events',type=Path,default=Path('data/annotations/bounce_events_gt.csv')); args=p.parse_args()
    with args.manifest.open(newline='',encoding='utf8') as f: rows=list(csv.DictReader(f))
    statuses={}
    for row in rows: statuses[row.get('annotation_status','pending')]=statuses.get(row.get('annotation_status','pending'),0)+1
    events=[]
    if args.events.exists():
        with args.events.open(newline='',encoding='utf8') as f: events=list(csv.DictReader(f))
    verified=sum(r.get('review_status')=='approved' for r in events); pending=sum(r.get('review_status') not in {'approved','excluded'} for r in events)
    print(f'frames total={len(rows)} reviewed={statuses.get("approved",0)} pending={len(rows)-statuses.get("approved",0)} rejected={statuses.get("rejected",0)}')
    print(f'bounce events total={len(events)} verified={verified} pending={pending}')
if __name__=='__main__': main()

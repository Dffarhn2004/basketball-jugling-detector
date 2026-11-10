"""Export frames (with a labelled coordinate grid) for manual contact-point reading. FN cases by default."""
from pathlib import Path
import csv, argparse, cv2
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(); ap.add_argument('--kind',default='FN_E2'); ap.add_argument('--offsets',default='-6,-4,-2,0,2,4,6'); a=ap.parse_args()
offs=[int(x) for x in a.offsets.split(',')]
OUT=ROOT/'data/annotations/contact_frames'; cap=cv2.VideoCapture(str(ROOT/'videofull.mp4'))
cases=[r for r in csv.DictReader(open(ROOT/'data/annotations/contact_points_sample.csv',encoding='utf8')) if r['kind']==a.kind]
for c in cases:
    d=OUT/c['case_id']; d.mkdir(parents=True,exist_ok=True); f0=int(float(c['ref_frame_idx']))
    for o in offs:
        fi=f0+o; cap.set(cv2.CAP_PROP_POS_FRAMES,fi); ok,img=cap.read()
        if not ok: continue
        h,w=img.shape[:2]
        for x in range(0,w,100):
            cv2.line(img,(x,0),(x,h),(255,255,0),1); cv2.putText(img,str(x),(x+2,14),0,.45,(0,255,255),1)
        for y in range(0,h,100):
            cv2.line(img,(0,y),(w,y),(255,255,0),1); cv2.putText(img,str(y),(2,y-3),0,.45,(0,255,255),1)
        cv2.putText(img,f"{c['case_id']} frame {fi} (offset {o:+d})",(10,h-12),0,.8,(0,0,255),2)
        cv2.imwrite(str(d/f"frame_{fi}_off{o:+d}.jpg"),img)
print('exported',len(cases),'cases ->',OUT)

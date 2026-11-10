"""Blind verification clips for the bridging method on minutes 2-20 (no GT there).
20 clips centred on predicted events + 10 centred on random times with no predicted event within +/-0.25 s.
Clips are shuffled and labelled V01..V30; the key is saved separately. Played at 10 fps (3x slower), no boxes; a red
frame border flashes on the target frame (centre)."""
from pathlib import Path
import csv, random
import cv2
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'artifacts/runs/Phase5_test_video/verify_clips'; OUT.mkdir(parents=True,exist_ok=True)
random.seed(20261105)
FPSV=29.97002997002997
evr=list(csv.DictReader(open(ROOT/'artifacts/runs/Phase5_test_video/events.csv')))
ev=[int(r['frame_idx'])/FPSV for r in evr]
pool=[t for t in ev if 1<=t<=160]
pos=random.sample(pool,20)
neg=[]
while len(neg)<10:
    t=random.uniform(1,160)
    if min(abs(t-e) for e in ev)>.25 and all(abs(t-n)>3 for n in neg): neg.append(t)
cases=[(t,'predicted') for t in pos]+[(t,'no_prediction') for t in neg]; random.shuffle(cases)
cap=cv2.VideoCapture(str(ROOT/'videotesting.mp4')); W=int(cap.get(3)); H=int(cap.get(4))
key=[]; ws=[]
for i,(t,kind) in enumerate(cases,1):
    cid=f'V{i:02d}'; c=int(round(t*FPSV)); out=cv2.VideoWriter(str(OUT/f'{cid}.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),10,(W,H))
    cap.set(cv2.CAP_PROP_POS_FRAMES,c-15)
    for k in range(31):
        ok,img=cap.read()
        if not ok: break
        if k==15:
            cv2.rectangle(img,(0,0),(W-1,H-1),(0,0,255),12); cv2.putText(img,'TARGET FRAME',(30,60),0,1.4,(0,0,255),4)
        cv2.putText(img,f'{cid}  {k+1}/31',(30,H-25),0,.9,(255,255,255),2); out.write(img)
    out.release(); key.append({'case_id':cid,'time_s':round(t,3),'frame_idx':c,'kind':kind}); ws.append({'case_id':cid,'answer':'','notes':''})
for name,rows,f in [('answer_key_DO_NOT_OPEN.csv',key,['case_id','time_s','frame_idx','kind']),('worksheet_isi_ini.csv',ws,['case_id','answer','notes'])]:
    with (OUT/name).open('w',newline='',encoding='utf8') as fh: w=csv.DictWriter(fh,fieldnames=f); w.writeheader(); w.writerows(rows)
(OUT/'BACA_DULU.txt').write_text("""CARA MENGISI (30 klip, V01-V30)
1. Putar tiap klip (diputar lambat, ~3 detik). Bingkai MERAH berkedip di tengah = TARGET FRAME.
2. Lihat apakah ADA BOLA yang menyentuh LANTAI tepat di sekitar frame target (kira-kira +-3 frame).
3. Isi kolom 'answer' di worksheet_isi_ini.csv dengan:  ada  /  tidak  /  ragu
   ada   = ada bola menyentuh lantai di sekitar frame merah
   tidak = tidak ada bola yang menyentuh lantai di sekitar frame merah
   ragu  = tidak bisa dipastikan
4. JANGAN buka answer_key_DO_NOT_OPEN.csv sebelum selesai (supaya penilaian tidak bias).
Tidak ada jawaban benar/salah soal metode; isi apa yang Anda LIHAT.
""",encoding='utf8')
print(len(key),'clips ->',OUT)

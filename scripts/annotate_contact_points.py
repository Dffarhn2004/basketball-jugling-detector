"""Click-based contact-point annotator for the 40 Phase 4 audit cases (20 FN + 20 FP).
Writes data/annotations/contact_points_sample.csv. Never modifies GT v2 or any model output.
Frames are shown WITHOUT model boxes (independent of predictions); press B to toggle E2 boxes as a hint only.

Keys:  A/D = -1/+1 frame   Q/E = -5/+5 frames   LEFT CLICK = mark ball-floor contact at this frame
       X = no contact visible in window   U = unsure/ambiguous   N/P = next/previous case
       Z = clear this case   B = toggle raw detection boxes   ESC = save and quit
Status values: contact | no_contact | unsure | PENDING.  A click on the contact ball records frame + (x,y)."""
from pathlib import Path
import csv, sys, argparse
import cv2
ROOT=Path(__file__).resolve().parents[1]
WS=ROOT/'artifacts/runs/Phase4_visual_audit/visual_review_worksheet.csv'
OUT=ROOT/'data/annotations/contact_points_sample.csv'
RAW=ROOT/'artifacts/runs/Phase4_diagnostics/raw_detections.csv'
FIELDS=['case_id','kind','ref_time_s','ref_frame_idx','status','marked_frame_idx','x_contact_px','y_contact_px','notes']
INTRO = """
==================== PETUNJUK ANOTASI TITIK KONTAK ====================
TUGAS ANDA: untuk setiap cuplikan (40 kasus), cari frame saat BOLA MENYENTUH LANTAI,
lalu KLIK KIRI tepat di titik sentuh bola dengan lantai.

  D / A      : maju / mundur 1 frame        E / Q : maju / mundur 5 frame
  KLIK KIRI  : tandai titik kontak (tanda silang merah muncul)
  X          : TIDAK ada bola menyentuh lantai di cuplikan ini
  U          : ragu / tidak jelas
  Z          : hapus tanda kasus ini
  N / P      : kasus berikutnya / sebelumnya
  B          : tampil/sembunyi box deteksi (hanya petunjuk)
  ESC        : simpan lalu keluar (progres tersimpan otomatis, bisa dilanjutkan)

Kasus FN-xx : GT bilang ada bounce -> biasanya ada kontak, cari bolanya.
Kasus FP-xx : sistem bilang ada bounce -> kalau memang tidak ada, tekan X.
Tidak ada jawaban benar/salah soal model; tandai apa yang Anda LIHAT saja.
========================================================================
"""
HELP_LINE="D/A=frame  E/Q=5 frame  KLIK=kontak  X=tdk ada  U=ragu  N/P=kasus  ESC=simpan+keluar"
def read(p):
    with Path(p).open(newline='',encoding='utf8') as f: return list(csv.DictReader(f))
def load_cases():
    cases=[]
    for r in read(WS):
        cases.append({'case_id':r['case_id'],'kind':r['kind'],'ref_time_s':r['time_s'],'ref_frame_idx':int(round(float(r['time_s'])*30)),
                      'status':'PENDING','marked_frame_idx':'','x_contact_px':'','y_contact_px':'','notes':''})
    return cases
def save(cases):
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(cases)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--dry-run',action='store_true',help='create CSV and check video/frames, no window'); a=ap.parse_args()
    if not a.dry_run: print(INTRO)
    cases=load_cases()
    if OUT.exists():
        done={r['case_id']:r for r in read(OUT)}
        cases=[done.get(c['case_id'],c) for c in cases]
    for c in cases: c['ref_frame_idx']=int(float(c['ref_frame_idx']))
    cap=cv2.VideoCapture(str(ROOT/'videofull.mp4'))
    if a.dry_run:
        for c in cases[:1]+cases[-1:]:
            cap.set(cv2.CAP_PROP_POS_FRAMES,c['ref_frame_idx']); ok,_=cap.read(); print(c['case_id'],c['ref_frame_idx'],'frame ok' if ok else 'READ FAIL')
        save(cases); print('cases',len(cases),'->',OUT); return
    raw={}
    if RAW.exists():
        for r in read(RAW): raw.setdefault(int(r['frame_idx']),[]).append(r)
    st={'i':next((k for k,c in enumerate(cases) if c['status']=='PENDING'),0),'off':0,'boxes':False}
    win='contact annotator'; cv2.namedWindow(win,cv2.WINDOW_NORMAL)
    def cur(): return cases[st['i']]
    def frame_no(): return max(0,cur()['ref_frame_idx']+st['off'])
    def on_mouse(ev,x,y,flags,_):
        if ev==cv2.EVENT_LBUTTONDOWN:
            c=cur(); c.update(status='contact',marked_frame_idx=frame_no(),x_contact_px=x,y_contact_px=y); save(cases)
    cv2.setMouseCallback(win,on_mouse)
    while True:
        c=cur(); fi=frame_no(); cap.set(cv2.CAP_PROP_POS_FRAMES,fi); ok,img=cap.read()
        if not ok: img=255*cv2.UMat(480,640,cv2.CV_8UC3).get()*0
        if st['boxes']:
            for d in raw.get(fi,[]):
                cv2.rectangle(img,(int(float(d['x1'])),int(float(d['y1']))),(int(float(d['x2'])),int(float(d['y2']))),(0,255,0),1)
        if c['status']=='contact' and str(c['marked_frame_idx'])==str(fi):
            cv2.drawMarker(img,(int(c['x_contact_px']),int(c['y_contact_px'])),(0,0,255),cv2.MARKER_CROSS,30,2)
        txt=f"{c['case_id']} ({st['i']+1}/{len(cases)}) {c['kind']} frame {fi} (ref {c['ref_frame_idx']}, off {st['off']:+d}) status={c['status']}"
        cv2.putText(img,txt,(10,25),0,.6,(0,0,255),2)
        cv2.rectangle(img,(0,img.shape[0]-34),(img.shape[1],img.shape[0]),(0,0,0),-1); cv2.putText(img,HELP_LINE,(10,img.shape[0]-11),0,.6,(255,255,255),1)
        cv2.imshow(win,img)
        k=cv2.waitKey(30)&0xFF
        if k==255: continue
        ch=chr(k).lower() if k<128 else ''
        if k==27: break
        elif ch=='d': st['off']+=1
        elif ch=='a': st['off']-=1
        elif ch=='e': st['off']+=5
        elif ch=='q': st['off']-=5
        elif ch=='x': c.update(status='no_contact',marked_frame_idx='',x_contact_px='',y_contact_px=''); save(cases)
        elif ch=='u': c.update(status='unsure',marked_frame_idx='',x_contact_px='',y_contact_px=''); save(cases)
        elif ch=='z': c.update(status='PENDING',marked_frame_idx='',x_contact_px='',y_contact_px=''); save(cases)
        elif ch=='b': st['boxes']=not st['boxes']
        elif ch=='n': st['i']=min(len(cases)-1,st['i']+1); st['off']=0
        elif ch=='p': st['i']=max(0,st['i']-1); st['off']=0
    save(cases); cv2.destroyAllWindows()
if __name__=='__main__': main()

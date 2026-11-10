"""Klik-saja verifikasi: putar tiap klip V01-V30 berulang, klik tombol ADA / TIDAK / RAGU. Jawaban tersimpan otomatis."""
from pathlib import Path
import csv, sys
import cv2, numpy as np
D=Path(__file__).resolve().parents[1]/'artifacts/runs/Phase4_bridging/verify_clips'
import sys as _s
if len([a for a in _s.argv if not a.startswith('--')])>1: D=Path(_s.argv[1])
WS=D/'worksheet_isi_ini.csv'
def rd():
    return list(csv.DictReader(open(WS,encoding='utf8')))
def save(rows):
    with WS.open('w',newline='',encoding='utf8') as f: w=csv.DictWriter(f,fieldnames=['case_id','answer','notes']); w.writeheader(); w.writerows(rows)
def load(cid):
    cap=cv2.VideoCapture(str(D/f'{cid}.mp4')); fr=[]
    while True:
        ok,im=cap.read()
        if not ok: break
        fr.append(cv2.resize(im,(960,540)))
    return fr
BAR=110; BTN=[('ADA',(0,160,0),'ada'),('TIDAK',(0,0,200),'tidak'),('RAGU',(120,120,120),'ragu')]
def main():
    rows=rd(); idx=next((i for i,r in enumerate(rows) if not r['answer'].strip()),0)
    if '--dry-run' in sys.argv: print(len(rows),'clips, first unanswered:',rows[idx]['case_id'],len(load(rows[idx]['case_id'])),'frames'); return
    W=960; st={'i':idx,'k':0,'click':None,'frames':load(rows[idx]['case_id'])}
    boxes=[]
    for n,(lab,col,val) in enumerate(BTN): boxes.append((20+n*310,540+20,20+n*310+290,540+90,lab,col,val))
    back=(W-110,540+5,W-5,540+30)
    def mouse(ev,x,y,fl,_):
        if ev!=cv2.EVENT_LBUTTONDOWN: return
        for x1,y1,x2,y2,lab,col,val in boxes:
            if x1<=x<=x2 and y1<=y<=y2: st['click']=val
        if back[0]<=x<=back[2] and back[1]<=y<=back[3]: st['click']='back'
    win='Verifikasi bounce'; cv2.namedWindow(win); cv2.setMouseCallback(win,mouse)
    print('Klik ADA / TIDAK / RAGU di jendela. ESC = keluar (jawaban tersimpan otomatis).')
    while True:
        if st['click']:
            c=st['click']; st['click']=None
            if c=='back': st['i']=max(0,st['i']-1)
            else:
                rows[st['i']]['answer']=c; save(rows); st['i']+=1
            if st['i']>=len(rows): break
            st['frames']=load(rows[st['i']]['case_id']); st['k']=0
        fr=st['frames']; im=fr[st['k']%len(fr)].copy(); st['k']+=1
        canvas=np.full((540+BAR,W,3),30,np.uint8); canvas[:540]=im
        cur=rows[st['i']]
        cv2.putText(canvas,f"Klip {cur['case_id']}  ({st['i']+1}/{len(rows)})   jawaban sekarang: {cur['answer'] or '-'}",(20,540+16),0,.55,(255,255,255),1)
        for x1,y1,x2,y2,lab,col,val in boxes:
            cv2.rectangle(canvas,(x1,y1),(x2,y2),col,-1); cv2.putText(canvas,lab,(x1+90 if lab!='TIDAK' else x1+80,y1+46),0,1.1,(255,255,255),3)
        cv2.rectangle(canvas,(back[0],back[1]),(back[2],back[3]),(90,60,0),-1); cv2.putText(canvas,'< KEMBALI',(back[0]+8,back[1]+20),0,.5,(255,255,255),1)
        cv2.putText(canvas,'Ada bola menyentuh LANTAI di frame bingkai MERAH?',(20,540+104),0,.5,(200,200,255),1)
        cv2.imshow(win,canvas)
        if cv2.waitKey(100)&0xFF==27: break
    cv2.destroyAllWindows(); done=sum(1 for r in rd() if r['answer'].strip()); print(f'Tersimpan: {done}/{len(rows)} klip terjawab.')
if __name__=='__main__': main()

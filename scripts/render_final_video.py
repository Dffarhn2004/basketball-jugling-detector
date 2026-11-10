"""Render the final 20-min video: ball boxes + IDs + trails + bounce markers + running bounce counter (frozen bridging params)."""
from pathlib import Path
import csv, sys, subprocess, shutil, argparse
from collections import defaultdict, deque
import cv2, numpy as np
ROOT=Path(__file__).resolve().parents[1]; B=ROOT/'artifacts/runs/Phase4_bridging'
sys.path.insert(0,str(ROOT/'scripts')); import phase4_bridging as pb
def load_all(paths):
    raw=defaultdict(list)
    for p in paths:
        for r in pb.read(p):
            x1,y1,x2,y2=(float(r[k]) for k in ('x1','y1','x2','y2')); raw[int(r['frame_idx'])].append(((x1+x2)/2,(y1+y2)/2,y2,max(x2-x1,y2-y1),float(r['confidence']),x1,y1,x2))
    return raw
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('limit',nargs='?',type=int); ap.add_argument('--video',default=str(ROOT/'videofull.mp4'))
    ap.add_argument('--raw',nargs='+',default=[str(B/'raw_0_60s.csv'),str(B/'raw_1800_end.csv')]); ap.add_argument('--out',default=str(B/'final_video_20min.mp4')); ap.add_argument('--frames',type=int,default=None)
    a=ap.parse_args(); limit=a.limit; VIDEO=a.video; OUTF=Path(a.out)
    raw=load_all(a.raw); n=a.frames or max(raw)+1
    tracks=pb.track({f:[d[:5] for d in v] for f,v in raw.items()},gate=1.5,max_miss=4,n=n)
    ev=pb.events(tracks,floor=.65,min_drop=15,min_rise=15)
    # per-frame: track boxes (tracks with >=3 points) and the box for each point
    tp={}; byframe=defaultdict(list)
    for t in tracks:
        tp[t['id']]=t
        if len(t['pts'])<3: continue
        for (f,cx,cy,by) in t['pts']:
            # find matching raw detection for box extents
            best=min(raw[f],key=lambda d:abs(d[0]-cx)+abs(d[1]-cy)); byframe[f].append((t['id'],best[5],best[6],best[7],by,cx,cy))
    evpos={}
    for e in ev:
        pt=[p for p in tp[e['track_id']]['pts'] if p[0]==e['frame_idx']][0]; evpos[e['frame_idx']]=(int(pt[1]),int(pt[3]))
    evf=sorted(evpos); cap=cv2.VideoCapture(VIDEO); FPSV=cap.get(5) or 30; W,H=int(cap.get(3)),int(cap.get(4)); OW,OH=960,540; sx=OW/W
    tmp=OUTF.with_name(OUTF.stem+'_raw.mp4'); out=cv2.VideoWriter(str(tmp),cv2.VideoWriter_fourcc(*'mp4v'),30,(OW,OH)); trails=defaultdict(lambda:deque(maxlen=14)); count=0; ei=0; flash={}
    total=min(n,limit) if limit else n
    for f in range(total):
        ok,img=cap.read()
        if not ok: break
        img=cv2.resize(img,(OW,OH))
        while ei<len(evf) and evf[ei]<=f: flash[evf[ei]]=evpos[evf[ei]]; count+=1; ei+=1
        for tid,x1,y1,x2,by,cx,cy in byframe.get(f,[]):
            c=(0,255,0); cv2.rectangle(img,(int(x1*sx),int(y1*sx)),(int(x2*sx),int(by*sx)),c,2); cv2.putText(img,f'ball {tid}',(int(x1*sx),int(y1*sx)-6),0,.5,c,1)
            trails[tid].append((int(cx*sx),int(cy*sx)))
            if len(trails[tid])>1: cv2.polylines(img,[np.array(trails[tid],np.int32)],False,(255,180,0),2)
        for ff,(x,y) in list(flash.items()):
            if f-ff>9: del flash[ff]; continue
            cv2.drawMarker(img,(int(x*sx),int(y*sx)),(0,0,255),cv2.MARKER_CROSS,40,3); cv2.putText(img,'BOUNCE +1',(int(x*sx)+20,int(y*sx)-10),0,.8,(0,0,255),2)
        cv2.rectangle(img,(0,0),(OW,44),(0,0,0),-1)
        cv2.putText(img,f'BOUNCES: {count}',(15,32),0,1.1,(0,255,255),3); cv2.putText(img,f't={f/FPSV:7.2f}s  ({int(f/FPSV//60):02d}:{int(f/FPSV%60):02d})',(OW-260,30),0,.8,(255,255,255),2)
        out.write(img)
        if f%3000==0: print(f,count,flush=True)
    out.release(); final=OUTF.with_name(OUTF.stem+'_preview.mp4') if limit else OUTF
    if shutil.which('ffmpeg'):
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(tmp),'-c:v','libx264','-crf','24','-preset','veryfast','-pix_fmt','yuv420p',str(final)],check=True); tmp.unlink()
    else: tmp.replace(final)
    print('done',final,'final count',count,'events',len(ev))
if __name__=='__main__': main()

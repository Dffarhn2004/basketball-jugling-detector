"""Score the blind verification after the user fills worksheet_isi_ini.csv. 'ragu' is excluded and reported."""
from pathlib import Path
import csv
D=Path(__file__).resolve().parents[1]/'artifacts/runs/Phase4_bridging/verify_clips'
import sys as _s
if len([a for a in _s.argv if not a.startswith('--')])>1: D=Path(_s.argv[1])
key={r['case_id']:r for r in csv.DictReader(open(D/'answer_key_DO_NOT_OPEN.csv',encoding='utf8'))}
ans={r['case_id']:r['answer'].strip().lower() for r in csv.DictReader(open(D/'worksheet_isi_ini.csv',encoding='utf8'))}
tp=fp=fn=tn=ragu=blank=0
for c,k in key.items():
    a=ans.get(c,'')
    if a=='': blank+=1
    elif a=='ragu': ragu+=1
    elif k['kind']=='predicted': tp+=a=='ada'; fp+=a=='tidak'
    else: fn+=a=='ada'; tn+=a=='tidak'
print(f'answered: pred-clips ada={tp} tidak={fp} | no-pred clips ada={fn} tidak={tn} | ragu={ragu} blank={blank}')
if tp+fp: print(f'estimated precision = {tp}/{tp+fp} = {tp/(tp+fp):.2f}')
if fn+tn: print(f'bounces missed in no-prediction clips: {fn}/{fn+tn}')
print('rough only: 20+10 clips, wide confidence interval')

import sys,json
from pathlib import Path
H=Path(__file__).resolve().parent.parent;R=H/'root-review'
mode=sys.argv[1];start,end=map(int,sys.argv[2:4]);d=json.loads((H/'story-data.json').read_text());l=json.loads((R/'reading-ledger.json').read_text())
assert mode in ['essential','core-additions']
ss=[s for s in d['screens'] if s['level']<=1] if mode=='essential' else [s for s in d['screens'] if s['level']==2]
key='essentialReadPairIds' if mode=='essential' else 'coreAddedPairsReread'
for s in ss[start-1:end]:
 if s['id'] not in l[key]:l[key].append(s['id'])
(R/'reading-ledger.json').write_text(json.dumps(l,ensure_ascii=False,indent=2)+'\n');print(mode,'actual personally read pairs recorded',start,end,'total',len(l[key]))

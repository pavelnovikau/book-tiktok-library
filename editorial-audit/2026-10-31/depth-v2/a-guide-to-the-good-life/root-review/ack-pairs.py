import sys,json,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent.parent;R=H/'root-review'
start,end=map(int,sys.argv[1:3]);d=json.loads((H/'story-data.json').read_text());l=json.loads((R/'reading-ledger.json').read_text())
for s in d['screens'][start-1:end]:
 if s['id'] not in l['deepReadPairIds']:l['deepReadPairIds'].append(s['id'])
l['currentlyReadStoryDataSha256']=hashlib.sha256((H/'story-data.json').read_bytes()).hexdigest()
(R/'reading-ledger.json').write_text(json.dumps(l,ensure_ascii=False,indent=2)+'\n')
print('Root personally read pairs recorded:',start,end,'total',len(l['deepReadPairIds']))

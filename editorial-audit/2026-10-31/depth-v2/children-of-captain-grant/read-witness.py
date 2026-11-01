import json,sys
from pathlib import Path
p=Path(__file__).parent
l=json.loads((p/'witness-reading-ledger.json').read_text())
c=l['chunks'][int(sys.argv[1])-1]
lines=Path(l['witness']).read_bytes().splitlines(keepends=True)
if len(sys.argv)>2:
 c['read']=True; c['notes']=sys.argv[2]
 l['continuousCompleteRead']=all(x['read'] for x in l['chunks'])
 (p/'witness-reading-ledger.json').write_text(json.dumps(l,ensure_ascii=False,indent=2)+'\n')
 print('Acknowledged',c['chunk'],c['startLine'],c['endLine'])
else:
 print('READ RANGE',c['chunk'],c['startLine'],c['endLine'],'SHA256',c['sha256'])
 print(b''.join(lines[c['startLine']-1:c['endLine']]).decode(),end='')

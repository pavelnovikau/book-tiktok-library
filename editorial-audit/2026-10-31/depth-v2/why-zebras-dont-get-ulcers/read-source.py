from pathlib import Path
import json,sys,hashlib,datetime
root=Path(__file__).resolve().parent
ledger=root/'source-reading-ledger.json'
d=json.loads(ledger.read_text())
if sys.argv[1]=='ack':
 f,a,b=sys.argv[2],int(sys.argv[3]),int(sys.argv[4]);t=(Path(d['sourceRoot'])/f).read_text();r=next(x for x in d['files'] if x['file']==f)
 assert hashlib.sha256((Path(d['sourceRoot'])/f).read_bytes()).hexdigest()==r['sha256']
 if not any(x['start']==a and x['end']==b for x in r['rangesRead']):r['rangesRead'].append({'start':a,'end':b,'firstLine':t.count('\n',0,a)+1,'lastLine':t.count('\n',0,b)+1,'chunkSha256':hashlib.sha256(t[a:b].encode()).hexdigest(),'readAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 ledger.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 print('Acknowledged',f,a,b)
else:
 f,a,b=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]);t=(Path(d['sourceRoot'])/f).read_text();b=min(b,len(t));print(f,'chars',a,b,'of',len(t));print(t[a:b]);print('END',f,a,b)

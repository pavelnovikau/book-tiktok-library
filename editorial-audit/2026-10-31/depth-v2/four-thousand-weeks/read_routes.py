from pathlib import Path
import json,sys,hashlib,html,re,datetime
p=Path(__file__).parent;d=json.loads((p/'story-data.json').read_text());mode=sys.argv[2];level={'essential':1,'core':2,'deep':3}[mode];screens=[s for s in d['screens'] if s['level']<=level];a,b=int(sys.argv[3]),int(sys.argv[4]);subset=screens[a-1:b]
sha=hashlib.sha256(json.dumps(subset,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
if sys.argv[1]=='read':
 print(f'{mode} {a}-{b}/{len(screens)} SHA256 {sha}')
 for s in subset:
  print('\n'+s['id'])
  for l in ['ru','en']:print(l,s['copy'][l]['title']+'\n'+html.unescape(re.sub('<[^>]+>','',s['copy'][l]['body'])))
else:
 f=p/'route-reading-ledger.json';o=json.loads(f.read_text()) if f.exists() else {'reviewer':'implementation agent only; not root or independent acceptance','entries':[]}
 o['entries'].append({'mode':mode,'firstPosition':a,'lastPosition':b,'pairs':len(subset),'rangeSha256':sha,'displayedRuEnReadingAcknowledged':True,'atUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'note':sys.argv[5]})
 f.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n');print('ACK',mode,a,b)

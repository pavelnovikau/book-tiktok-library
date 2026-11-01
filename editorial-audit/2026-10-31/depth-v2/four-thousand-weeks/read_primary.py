import json,hashlib,sys,datetime
from pathlib import Path
ROOT=Path(__file__).parent
PRIMARY=Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-8-private/four-thousand-weeks-edition.json')
d=json.loads(PRIMARY.read_text())
cmd=sys.argv[1]; name=sys.argv[2]; r=next(x for x in d if x['file'].endswith('/'+name))
a=int(sys.argv[3]); b=int(sys.argv[4]); ps=r['paragraphs'][a-1:b]
sha=hashlib.sha256('\n'.join(ps).encode()).hexdigest()
if cmd=='read':
 print(f"FILE {r['file']} P{a:03}–P{b:03}; paragraphs={len(ps)}; SHA256={sha}")
 for i,p in enumerate(ps,a): print(f'P{i:03}: {p}\n')
elif cmd=='ack':
 f=ROOT/'primary-reading-ledger.json'; l=json.loads(f.read_text())
 l['entries'].append({'file':r['file'],'firstParagraph':a,'lastParagraph':b,'rangeSha256':sha,'paragraphs':len(ps),'atUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'displayedReadingAcknowledged':True,'acknowledgement':sys.argv[5]})
 f.write_text(json.dumps(l,ensure_ascii=False,indent=2)+'\n'); print('ACK',name,a,b)

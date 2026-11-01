from pathlib import Path
import json,sys,re,html,hashlib,datetime
b=Path(__file__).parent;d=json.loads((b/'story-data.json').read_text());chunks=[]
for mode,level in [('essential',1),('core',2),('deep',3)]:
 for lang in ['ru','en']:
  cur=[];size=0
  for s in d['screens']:
   if s['level']>level:continue
   c=s['copy'][lang];body=html.unescape(c['body'].replace('</p><p>','\n\n').replace('<p>','').replace('</p>',''));t=f"[{s['id']} level{s['level']}] {c['title']}\n{body}"
   if size+len(t)>18000 and cur:chunks.append({'mode':mode,'lang':lang,'items':cur});cur=[];size=0
   cur.append({'id':s['id'],'text':t});size+=len(t)
  if cur:chunks.append({'mode':mode,'lang':lang,'items':cur})
if sys.argv[1]=='plan':
 print([(i+1,c['mode'],c['lang'],len(c['items']),c['items'][0]['id'],c['items'][-1]['id']) for i,c in enumerate(chunks)])
else:
 n=int(sys.argv[1]);c=chunks[n-1];content='\n\n'.join(x['text']for x in c['items']);digest=hashlib.sha256(content.encode()).hexdigest()
 if len(sys.argv)>2 and sys.argv[2]=='ack':
  p=b/'route-reading-ledger.json';a=json.loads(p.read_text())if p.exists()else {'reviewer':'implementation agent, not root or independent reviewer','chunks':[]}
  assert not any(x['chunk']==n for x in a['chunks']);a['chunks'].append({'chunk':n,'mode':c['mode'],'language':c['lang'],'screenIds':[x['id']for x in c['items']],'displaySha256':digest,'readDisplayedUntruncated':True,'atUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'note':sys.argv[3] if len(sys.argv)>3 else 'Read route in order; checked continuity and attribution.'});p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
 else:print(f"ROUTE CHUNK {n}/{len(chunks)} {c['mode']} {c['lang']} HASH {digest}\n\n{content}\n\nEND ROUTE CHUNK {n}")

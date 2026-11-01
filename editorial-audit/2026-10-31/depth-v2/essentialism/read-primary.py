from pathlib import Path
import json,hashlib,sys,datetime
BASE=Path(__file__).resolve().parent
SRC=Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-8-private/essentialism-edition.json')
H=lambda b:hashlib.sha256(b).hexdigest()
data=json.loads(SRC.read_text()); chunks=[]; buf=[];wc=0
for ri,r in enumerate(data):
 if ri<3 or ri>31:continue
 for pi,p in enumerate(r['paragraphs'],1):
  n=len(p.split())
  if buf and wc+n>1800:chunks.append(buf);buf=[];wc=0
  buf.append({'file':r['file'],'p':pi,'text':p});wc+=n
if buf:chunks.append(buf)
manifest={'source':str(SRC),'sourceSha256':H(SRC.read_bytes()),'paragraphConvention':'1-based index in supplied paragraphs array; includes extracted headings; no print pagination','displayEncoding':'UTF-8, [file Pnnn] followed by exact extracted paragraph; LF; no source text persisted','scope':'info.xhtml, gl1..20 including gl3 continuations, four part openings, pril.xhtml; source record indices 3..31 inclusive','chunks':[],'files':[]}
for r in data:
 manifest['files'].append({'file':r['file'],'paragraphs':len(r['paragraphs']),'reportedWords':r['words'],'sha256CanonicalParagraphs':H(json.dumps(r['paragraphs'],ensure_ascii=False,separators=(',',':')).encode())})
for i,c in enumerate(chunks,1):
 display='\n'.join(f"[{x['file']} P{x['p']:03d}] {x['text']}" for x in c)+'\n'
 ranges=[]
 for x in c:
  if ranges and ranges[-1]['file']==x['file'] and ranges[-1]['end']==x['p']-1:ranges[-1]['end']=x['p']
  else:ranges.append({'file':x['file'],'start':x['p'],'end':x['p']})
 manifest['chunks'].append({'chunk':i,'ranges':ranges,'wordsWhitespace':sum(len(x['text'].split()) for x in c),'paragraphs':len(c),'displayBytes':len(display.encode()),'displaySha256':H(display.encode())})
(BASE/'reading-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
i=int(sys.argv[1]);c=chunks[i-1];m=manifest['chunks'][i-1]
print('CHUNK',i,'OF',len(chunks),json.dumps(m,ensure_ascii=False))
print('\n'.join(f"[{x['file']} P{x['p']:03d}] {x['text']}" for x in c))
with (BASE/'displayed-reading-ledger.jsonl').open('a') as f:f.write(json.dumps({'atUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),**m,'event':'bounded untruncated display requested; agent reads output; not root acceptance'},ensure_ascii=False)+'\n')

from pathlib import Path
import sys,json,hashlib,datetime
b=Path(__file__).parent;plan=json.loads((b/'reading-plan.json').read_text());p=b/'reading-ledger.json'
d=json.loads(p.read_text()) if p.exists() else {'sourceSha256':plan['sourceSha256'],'indexing':plan['indexing'],'claim':'Implementation agent displayed and read original paragraphs continuously; not root acceptance; not official English collation.','chunks':[]}
n=int(sys.argv[1]);c=plan['chunks'][n-1];assert not any(x['chunk']==n for x in d['chunks'])
ranges=[]
for r in c:
 if ranges and ranges[-1]['file']==r['file'] and ranges[-1]['end']+1==r['p']:ranges[-1]['end']=r['p']
 else:ranges.append({'file':r['file'],'start':r['p'],'end':r['p']})
d['chunks'].append({'chunk':n,'ranges':ranges,'paragraphHashes':c,'rangeHash':hashlib.sha256(json.dumps(c,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),'displayedReadingAcknowledged':True,'acknowledgedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'readingNote':sys.argv[2]})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2))

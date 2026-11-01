import sys,hashlib,json
from pathlib import Path
S=Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-10-private/a-guide-to-the-good-life-source')
R=Path(__file__).resolve().parent
name=sys.argv[1];start,end=map(int,sys.argv[2:4]);p=S/name;text=p.read_text();assert 0<=start<end<=len(text)
sha=lambda b:hashlib.sha256(b).hexdigest()
if len(sys.argv)>4 and sys.argv[4]=='ack':
 l=json.loads((R/'reading-ledger.json').read_text());r={'file':name,'start':start,'end':end,'fileSha256':sha(p.read_bytes()),'chunkSha256':sha(text[start:end].encode()),'scope':'Actual untruncated bounded primary text personally read by root; Unicode chars, not pages.'}
 if not any(x['file']==name and x['start']==start and x['end']==end for x in l['primaryRangesActuallyRead']):l['primaryRangesActuallyRead'].append(r)
 (R/'reading-ledger.json').write_text(json.dumps(l,ensure_ascii=False,indent=2)+'\n');print('Recorded actual root source reading',name,start,end)
else:
 print('\nPRIMARY',name,'CHARS',start,end,'OF',len(text),'SHA',sha(p.read_bytes()));print(text[start:end]);print('END PRIMARY',name,start,end)

from pathlib import Path
import datetime,hashlib,json,sys
H=Path(__file__).resolve().parent.parent;R=H/'root-review'
S=Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-8-private/make-time-edition.json')
data=json.loads(S.read_text());idx=int(sys.argv[1]);row=data[idx];a=int(sys.argv[2]);b=int(sys.argv[3]);assert 1<=a<=b<=len(row['paragraphs'])
if len(sys.argv)>4 and sys.argv[4]=='ack':
 l=json.loads((R/'reading-ledger.json').read_text());l['primaryRangesActuallyRead'].append({'record':idx,'file':row['file'],'start':a,'end':b,'indexBase':1,'inclusive':True,'sourceSha256':hashlib.sha256(S.read_bytes()).hexdigest(),'rangeSha256':hashlib.sha256(json.dumps(row['paragraphs'][a-1:b],ensure_ascii=False).encode()).hexdigest(),'scope':'Actual full bounded primary paragraphs personally read in untruncated output. No whole-book claim.','atUtc':datetime.datetime.now(datetime.timezone.utc).isoformat()});(R/'reading-ledger.json').write_text(json.dumps(l,ensure_ascii=False,indent=2)+'\n');print('root primary reads',len(l['primaryRangesActuallyRead']))
else:
 print(f'RECORD {idx} {row["file"]} paragraphs{a}–{b}/{len(row["paragraphs"])};1-based inclusive')
 for n,p in enumerate(row['paragraphs'][a-1:b],a):print(f'[{n}] {p}')

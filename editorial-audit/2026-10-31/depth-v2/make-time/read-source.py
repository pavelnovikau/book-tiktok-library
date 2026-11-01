import pathlib,json,sys,hashlib,datetime
HERE=pathlib.Path(__file__).resolve().parent
SRC=pathlib.Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-8-private/make-time-edition.json')
d=json.loads(SRC.read_text()); idx=int(sys.argv[1]); r=d[idx]; a=int(sys.argv[2]) if len(sys.argv)>2 else 1; b=int(sys.argv[3]) if len(sys.argv)>3 else len(r['paragraphs'])
assert 1<=a<=b<=len(r['paragraphs'])
print(f"RECORD {idx}: {r['file']}; paragraphs {a}-{b}/{len(r['paragraphs'])} (1-based inclusive)")
for n,p in enumerate(r['paragraphs'][a-1:b],a): print(f'[{n}] {p}')
entry={'record':idx,'file':r['file'],'start':a,'end':b,'indexBase':1,'inclusive':True,'sourceSha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'rangeSha256':hashlib.sha256(json.dumps(r['paragraphs'][a-1:b],ensure_ascii=False).encode()).hexdigest(),'action':'bounded continuous text emitted for direct reading','time':datetime.datetime.now().isoformat()}
p=HERE/'private-source-reading-ledger.json'; ledger=json.loads(p.read_text()) if p.exists() else {'private':True,'containsSourceText':False,'source':str(SRC),'events':[]};ledger['events'].append(entry);p.write_text(json.dumps(ledger,ensure_ascii=False,indent=2));p.chmod(0o600)

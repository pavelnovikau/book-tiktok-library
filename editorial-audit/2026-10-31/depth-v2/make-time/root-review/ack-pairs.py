from pathlib import Path
import datetime,hashlib,json,sys
H=Path(__file__).resolve().parent.parent;R=H/'root-review';mode=sys.argv[1];a=int(sys.argv[2]);b=int(sys.argv[3])
d=json.loads((H/'story-data.json').read_text());l=json.loads((R/'reading-ledger.json').read_text())
level={'essential':1,'core':2,'deep':3,'core-additions':2}[mode]
screens=[s for s in d['screens'] if s['level']<=level]
if mode=='core-additions':screens=[s for s in screens if s['level']==2]
assert 1<=a<=b<=len(screens)
key={'essential':'essentialReadPairIds','deep':'deepReadPairIds','core-additions':'coreAddedPairsReread'}[mode]
ids=[s['id'] for s in screens[a-1:b]]
assert not any(i in l[key] for i in ids),'Already acknowledged; do not silently duplicate reading.'
l[key]+=ids
l.setdefault('readBatches',[]).append({'mode':mode,'start':a,'end':b,'ids':ids,'storyDataSha256':hashlib.sha256((H/'story-data.json').read_bytes()).hexdigest(),'atUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Full displayed RU/EN copy personally read, not a count-only check.'})
(R/'reading-ledger.json').write_text(json.dumps(l,ensure_ascii=False,indent=2)+'\n')
print(key,len(l[key]))


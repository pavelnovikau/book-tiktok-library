from pathlib import Path
import datetime,hashlib,json
H=Path(__file__).resolve().parent.parent;R=H/'root-review';Q=R/'qa'
load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-8-private/make-time-edition.json')
data=load(source);l=load(R/'reading-ledger.json');source_sha=sha(source)
for row in l['primaryRangesActuallyRead']:
 assert row['sourceSha256']==source_sha
 record=data[row['record']];assert record['file']==row['file']
 text=record['paragraphs'][row['start']-1:row['end']]
 assert hashlib.sha256(json.dumps(text,ensure_ascii=False).encode()).hexdigest()==row['rangeSha256']
for row in load(R/'protected-baseline.json')['files']:
 assert sha(Path(row['path']))==row['sha256'],row['path']
checks=load(R/'primary-selection-plan.json')['checks']
for target in checks:
 at=target['start']
 for row in sorted([r for r in l['primaryRangesActuallyRead'] if r['record']==target['record']],key=lambda r:r['start']):
  if row['start']<=at<=row['end']:at=row['end']+1
 assert at>target['end'],target
writer=load(H/'private-source-reading-ledger.json')
for row in writer['events']:
 assert row['sourceSha256']==source_sha
 values=data[row['record']]['paragraphs'][row['start']-1:row['end']]
 assert hashlib.sha256(json.dumps(values,ensure_ascii=False).encode()).hexdigest()==row['rangeSha256']
for i,record in enumerate(data):
 if not record['paragraphs']:continue
 at=1
 for row in sorted([r for r in writer['events'] if r['record']==i],key=lambda r:r['start']):
  if row['start']<=at<=row['end']:at=row['end']+1
 assert at>len(record['paragraphs']),('writer-uncovered',i,at)
cov=load(H/'coverage-map.json')
actual=[(x['tactic'],x['sourceRange']['paragraphStart'],x['sourceRange']['paragraphEnd']) for x in cov['tactics'][2:6]]
assert actual==[(3,13,47),(4,48,57),(5,58,63),(6,64,81)]
out={'atUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sourceFileSha256':source_sha,'rootActualRangesHashValid':len(l['primaryRangesActuallyRead']),'allSuggestedIntervalsCovered':len(checks),'writerAllNonemptyRecordsIntervalIntegrity':sum(bool(r['paragraphs']) for r in data),'writerWholeReadingIsNotRootWholeReading':True,'rootWholePrimaryContinuouslyRead':False,'protectedInputsUnchanged':len(load(R/'protected-baseline.json')['files']),'correctedTacticRanges':actual,'workerReadingLedgerByteIdentical':(H/'private-source-reading-ledger.json').read_bytes()==(R/'input-private-source-reading-ledger.json').read_bytes(),'rootPersonalAcceptance':False,'publicationAllowed':False}
(Q/'primary-integrity.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out))

from pathlib import Path
import datetime
import hashlib
import json

R = Path(__file__).resolve().parent
H = R.parent
load = lambda p: json.loads(p.read_text())
sha = lambda b: hashlib.sha256(b).hexdigest()
manifest = load(H / 'reading-manifest.json')
source = Path(manifest['source'])
raw = load(source)
by = {r['file']: r for r in raw}
source_hash = sha(source.read_bytes())
assert source_hash == manifest['sourceSha256']
for r in manifest['files']:
    assert sha(json.dumps(by[r['file']]['paragraphs'], ensure_ascii=False, separators=(',', ':')).encode()) == r['sha256CanonicalParagraphs']
writer_events = [json.loads(line) for line in (H / 'displayed-reading-ledger.jsonl').read_text().splitlines()]
writer_seen = set()
for chunk in manifest['chunks']:
    rows = []
    for r in chunk['ranges']:
        for p in range(r['start'], r['end'] + 1):
            key = (r['file'], p)
            assert key not in writer_seen
            writer_seen.add(key)
            rows.append('[' + r['file'] + ' P' + str(p).zfill(3) + '] ' + by[r['file']]['paragraphs'][p - 1])
    display = '\n'.join(rows) + '\n'
    assert sha(display.encode()) == chunk['displaySha256']
    assert len(display.encode()) == chunk['displayBytes']
    assert any(e['chunk'] == chunk['chunk'] and e['displaySha256'] == chunk['displaySha256'] for e in writer_events)
expected = {(r['file'], p) for r in raw[3:32] for p in range(1, len(r['paragraphs']) + 1)}
assert writer_seen == expected and len(expected) == 1096
ledger = load(R / 'reading-ledger.json')
root_seen = set()
for r in ledger['primaryDisplays']:
    assert r['completeDisplayedRangePersonallyRead'] and r['sourceSha256'] == source_hash
    paragraphs = by[r['file']]['paragraphs'][r['start'] - 1:r['end']]
    assert sha(json.dumps(paragraphs, ensure_ascii=False, separators=(',', ':')).encode()) == r['rangeSha256']
    root_seen |= {(r['file'], p) for p in range(r['start'], r['end'] + 1)}
plan = load(R / 'primary-selection-plan.json')
for r in plan['ranges']:
    assert all((r['file'], p) in root_seen for p in range(r['start'], r['end'] + 1))
assert len(ledger['primaryDisplays']) == 34
for name in ['reading-manifest.json', 'displayed-reading-ledger.jsonl', 'source-reading-ledger.md']:
    assert (H / name).read_bytes() == (R / ('input-' + name)).read_bytes()
protected = load(R / 'qa-protected-baseline.json')
assert all(sha(Path(p).read_bytes()) == before for p, before in protected.items())
report = {
    'atUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'PASS',
    'sourceSha256': source_hash,
    'rootActualPrimaryRanges': len(ledger['primaryDisplays']),
    'rootUniquePrimaryParagraphs': len(root_seen),
    'rootPlannedAdditionalSelectionsCovered': len(plan['ranges']),
    'rootWholePrimaryContinuouslyRead': False,
    'writerReadingLedgerIntegrity': {
        'chunks': len(manifest['chunks']),
        'mainParagraphs': len(writer_seen),
        'files': 29,
        'allRecordedDisplayHashesRecomputed': True,
        'noGapsOrOverlaps': True,
        'writerReadingRecordsUnchanged': True,
        'scope': 'Integrity of the writer records only; does not turn extraction or its counts into root reading.'
    },
    'protectedInputHashesUnchanged': len(protected),
    'publishedEnglishCollation': False,
    'figuresVisuallyRead': False,
    'underlyingStudiesIndependentlyAudited': False
}
(R / 'qa/primary-integrity.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report))

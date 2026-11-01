from pathlib import Path
import copy
import datetime
import hashlib
import html
import json

R = Path(__file__).resolve().parent
H = R.parent
load = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
slice_sha = lambda a: hashlib.sha256(json.dumps(a, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
current = load(H / 'story-data.json')
ledger = load(R / 'reading-ledger.json')
versions = {'final': current, 'input': load(R / 'input-story-data.json')}
previous = copy.deepcopy(current)
for name, version in [('polish-second.json', 'after-first-polish'), ('polish.json', 'first-root-revision')]:
    by_id = {s['id']: s for s in previous['screens']}
    for row in reversed(load(R / name)['repairs']):
        field = by_id[row['screen']]['copy'][row['language']]
        old, new = (html.escape(row[k], quote=False) for k in ['old', 'new'])
        assert new in field['body'], (name, row['screen'], new)
        field['body'] = field['body'].replace(new, old, 1)
    versions[version] = copy.deepcopy(previous)

final_by_id = {s['id']: s for s in current['screens']}
covered = set()
display_checks = []
for category in ['screenDisplays', 'routeDisplays', 'coreAdditionDisplays', 'changedDisplays']:
    for record in ledger[category]:
        assert record['completeDisplayedRangePersonallyRead']
        matches = []
        for version, data in versions.items():
            by_id = {s['id']: s for s in data['screens']}
            if any(i not in by_id for i in record['ids']):
                continue
            selected = [by_id[i] for i in record['ids']]
            if slice_sha(selected) == record['corpusSliceSha256']:
                matches.append(version)
                for s in selected:
                    if s['copy'] == final_by_id[s['id']]['copy']:
                        covered.add(s['id'])
        assert matches, ('unmatched actual displayed version', category, record['ids'])
        display_checks.append({'category': category, 'ids': record['ids'], 'matchesVersions': matches})

assert covered == set(final_by_id), sorted(set(final_by_id) - covered)
changed = [s['id'] for s in current['screens'] if s['id'] not in {x['id'] for x in versions['input']['screens']} or s['copy'] != next((x['copy'] for x in versions['input']['screens'] if x['id'] == s['id']), None)]
assert set(changed) <= covered
essential_reads = [i for r in ledger['routeDisplays'] if r.get('mode') == 'essential' for i in r['ids']]
assert set(s['id'] for s in current['screens'] if s['level'] == 1) <= set(essential_reads)
core_addition_reads = [i for r in ledger['coreAdditionDisplays'] for i in r['ids']]
assert core_addition_reads == [s['id'] for s in current['screens'] if s['level'] == 2]

source = Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-8-private/selfie-edition.json')
records = {r['file']: r for r in load(source)}
seen = set()
display_words = 0
for row in ledger['primaryDisplays']:
    assert row['completeDisplayedRangePersonallyRead'] and row['sourceSha256'] == sha(source)
    ps = records[row['file']]['paragraphs'][row['start'] - 1:row['end']]
    digest = hashlib.sha256(json.dumps(ps, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
    assert len(ps) == row['end'] - row['start'] + 1 and digest == row['rangeSha256']
    display_words += sum(len(p.split()) for p in ps)
    seen.update((row['file'], i) for i in range(row['start'], row['end'] + 1))

writer = load(R / 'input-reading-ledger.json')
assert writer['sourceSha256'] == sha(source)
writer_seen = set()
for chunk in writer['chunks']:
    assert chunk['displayedReadingAcknowledged']
    expected_chunk = set()
    for row in chunk['ranges']:
        ps = records[row['file']]['paragraphs'][row['start'] - 1:row['end']]
        assert len(ps) == row['end'] - row['start'] + 1
        expected_chunk.update((row['file'], i) for i in range(row['start'], row['end'] + 1))
    assert expected_chunk == {(x['file'], x['p']) for x in chunk['paragraphHashes']}
    for row in chunk['paragraphHashes']:
        p = records[row['file']]['paragraphs'][row['p'] - 1]
        assert hashlib.sha256(p.encode()).hexdigest() == row['sha256']
    writer_seen.update(expected_chunk)
main_files = ['OPS/ch1-%d.xhtml' % i for i in range(3, 22)]
main_paragraphs = {(f, i) for f in main_files for i in range(1, len(records[f]['paragraphs']) + 1)}
assert main_paragraphs <= writer_seen and len(main_paragraphs) == writer['mainSpineParagraphs']

baseline = load(R / 'protected-inputs.json')
coordination = load(R / 'coordination-updates.json')['files']
exceptions = []
for file, expected in baseline.items():
    got = sha(Path(file))
    if got != expected:
        assert file in coordination and got == coordination[file]['afterCompletionSha256']
        assert expected == coordination[file]['originalSha256']
        exceptions.append({'path': file, 'originalSha256': expected, 'currentSha256': got, 'reason': coordination[file]['reason']})
for file, expected in load(R / 'huckleberry-inputs.json').items():
    assert sha(Path(file)) == expected, file

report = {
    'atUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'pass',
    'rootPersonalAcceptance': ledger['rootPersonalAcceptance'],
    'rootContinuousWholePrimaryRead': False,
    'finalProseCoveredPairs': len(covered),
    'changedOrNewCopyPairs': len(changed),
    'essentialOrderedPositions': len(set(essential_reads)),
    'coreAdditionPairsReadWithAdjacentRouteEdges': len(core_addition_reads),
    'method': 'Complete input RU/EN read; complete Essential route, each Core addition with actual adjacent edges, all changed Deep-only copy and subsequent exact-hash polish rereads. Shared unchanged prose is not claimed as a third duplicate continuous reread.',
    'displayChecks': display_checks,
    'rootPrimary': {'intervals': len(ledger['primaryDisplays']), 'uniqueParagraphs': len(seen), 'uniqueWordsWhitespace': sum(len(records[f]['paragraphs'][i - 1].split()) for f, i in seen), 'displayedWordsWhitespaceWithOverlap': display_words, 'sourceSha256': sha(source)},
    'writerLedgerIntegrity': {'chunks': len(writer['chunks']), 'uniqueParagraphs': len(writer_seen), 'mainParagraphs': len(main_paragraphs), 'scope': 'Individual paragraph hashes, exact range membership and complete main-spine coverage of recorded writer reading only; not root continuous reading.'},
    'immutableInputs': {'checked': len(baseline), 'unchanged': len(baseline) - len(exceptions), 'exactRootCoordinationExceptions': exceptions},
    'additionalHuckleberryInputsUnchanged': len(load(R / 'huckleberry-inputs.json')),
    'inputSha256': {str(p.relative_to(H)): sha(p) for p in [H / 'story-data.json', H / 'selfie.html', R / 'reading-ledger.json']}
}
(R / 'reading-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: report[k] for k in ['status', 'finalProseCoveredPairs', 'changedOrNewCopyPairs', 'essentialOrderedPositions', 'coreAdditionPairsReadWithAdjacentRouteEdges', 'rootPrimary', 'writerLedgerIntegrity', 'immutableInputs']}, ensure_ascii=False, indent=2))

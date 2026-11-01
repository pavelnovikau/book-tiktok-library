"""Verify evidence records without copying private primary text into the output."""
from pathlib import Path
import json, hashlib, html, re

base = Path(__file__).resolve().parent
read = lambda name: json.loads((base / name).read_text())
digest = lambda blob: hashlib.sha256(blob).hexdigest()
file_hash = lambda name: digest((base / name).read_bytes())
identity = read('source-identity.json')
source_path = Path(identity['sourcePath'])
assert digest(source_path.read_bytes()) == identity['sha256']
source = json.loads(source_path.read_text())
by_file = {record['file']: record for record in source}
assert len(source) == 26
assert sum(record['words'] for record in source) == 97266

ledger = read('reading-ledger.json')
plan = read('reading-plan.json')
assert ledger['sourceSha256'] == plan['sourceSha256'] == identity['sha256']
assert len(ledger['chunks']) == len(plan['chunks']) == 30
seen = []
for index, chunk in enumerate(ledger['chunks'], 1):
    assert chunk['chunk'] == index and chunk['displayedReadingAcknowledged']
    assert chunk['paragraphHashes'] == plan['chunks'][index-1]
    assert digest(json.dumps(chunk['paragraphHashes'], ensure_ascii=False,
                             separators=(',', ':')).encode()) == chunk['rangeHash']
    for item in chunk['paragraphHashes']:
        paragraph = by_file[item['file']]['paragraphs'][item['p']-1]
        assert digest(paragraph.encode()) == item['sha256']
        seen.append((item['file'], item['p']))
expected = [(record['file'], n) for record in source
            if record['file'] != 'OPS/ch2.xhtml'
            for n in range(1, len(record['paragraphs'])+1)]
# The extraction also has a non-body nav record; only explicitly planned records count.
planned_files = {item[0] for item in seen}
expected = [item for item in expected if item[0] in planned_files]
assert seen == expected and len(seen) == len(set(seen))
for item in ledger['selectiveNotes']['paragraphs']:
    assert digest(by_file['OPS/ch2.xhtml']['paragraphs'][item['paragraph']-1].encode()) == item['sha256']
main_files = ['OPS/ch1-%d.xhtml' % n for n in range(3, 22)]
main_pairs = [(name, n) for name in main_files
              for n in range(1, len(by_file[name]['paragraphs'])+1)]
assert len(main_pairs) == 1159 and set(main_pairs) <= set(seen)
assert sum(by_file[name]['words'] for name in main_files) == 92278
assert all(('OPS/ch1-23.xhtml', n) in seen for n in range(1, 8))

data = read('story-data.json')
coverage = read('coverage-map.json')
assert coverage['sourceSha256'] == identity['sha256']
assert len(coverage['units']) == 64
assert [item['file'] for item in coverage['wholeMainSpine']] == main_files
all_screen_ids = []
locator_count = 0
for unit in coverage['units']:
    assert unit['argumentativeJob'] and unit['transition']['from'] and unit['transition']['to']
    for loc in unit['primaryLocators']:
        assert 1 <= loc['start'] <= loc['end'] <= len(by_file[loc['file']]['paragraphs'])
        for n in range(loc['start'], loc['end']+1):
            assert (loc['file'], n) in seen or (
                loc['file'] == 'OPS/ch2.xhtml' and n in
                [item['paragraph'] for item in ledger['selectiveNotes']['paragraphs']])
        locator_count += 1
    for screen_id in unit['screens']:
        screen = next(screen for screen in data['screens'] if screen['id'] == screen_id)
        assert screen['level'] == unit['level'] and screen['sources'] == [1]
        assert screen['claimType'] == 'book'
        assert screen_id in (base/'coverage-map.md').read_text()
        all_screen_ids.append(screen_id)
assert all_screen_ids == [screen['id'] for screen in data['screens'] if screen.get('type') != 'cover']
assert data['contentMode'] == 'explanatory'
assert (data['defaultLanguage'], data['defaultTheme'], data['defaultMode']) == ('ru', 'dark', 'essential')
assert data['targetModes'] == {'essential': 48, 'core': 92, 'deep': 128}

route_ledger = read('route-reading-ledger.json')
assert len(route_ledger['chunks']) == 24
route_chunks = []
for mode, level in [('essential', 1), ('core', 2), ('deep', 3)]:
    for lang in ['ru', 'en']:
        current, size = [], 0
        for screen in data['screens']:
            if screen['level'] > level:
                continue
            copy = screen['copy'][lang]
            body = html.unescape(copy['body'].replace('</p><p>', '\n\n').replace('<p>', '').replace('</p>', ''))
            text = '[%s level%d] %s\n%s' % (screen['id'], screen['level'], copy['title'], body)
            if size + len(text) > 18000 and current:
                route_chunks.append((mode, lang, current)); current, size = [], 0
            current.append((screen['id'], text)); size += len(text)
        if current:
            route_chunks.append((mode, lang, current))
assert len(route_chunks) == 24
for index, (mode, lang, items) in enumerate(route_chunks, 1):
    record = next(item for item in route_ledger['chunks'] if item['chunk'] == index)
    revisions = [item for item in route_ledger.get('finalRevisionRereads', []) if item['chunk'] == index]
    if revisions:
        record = revisions[-1]
    assert record['readDisplayedUntruncated']
    assert record['screenIds'] == [item[0] for item in items]
    assert record['displaySha256'] == digest('\n\n'.join(item[1] for item in items).encode())
    assert (record['mode'], record['language']) == (mode, lang)
assert route_ledger['rootPersonalAcceptance'] is False

parity = read('parity.json')
assert parity['allAuthoredFieldsMatchEmbedded'] and parity['routeCopiesAllExact']
assert parity['paragraphs'] == {'ru': 192, 'en': 192}
for name, expected_hash in parity['hashes'].items():
    assert file_hash(name) == expected_hash
metrics = read('metrics.json')
visits = 0
for tag in ['320', '390', '1024', '1440', 'ios-390']:
    report = read('qa/browser-%s.json' % tag)
    assert report['status'] == 'PASS'
    assert report['traversal']['visits'] == 2144 and not report['traversal']['fail']
    assert not report['runtimeErrors'] and not report['remoteRequests']
    assert report['cleanup']['profileRemoved'] and not report['cleanup']['remainingOwnedPids']
    for name, expected_hash in report['hashes'].items():
        assert file_hash(name) == expected_hash
    assert all(report['nativeInput'][key] for key in ['tapEnterExit', 'longPressGuard', 'textSelectionGuard'])
    visits += report['traversal']['visits']
cold = read('qa/browser-320.json')
assert cold['coldBefore']['top'] == cold['coldAfter']['top'] == 110
assert cold['nativeSettingsKeyboard']
assert all(face['status'] == 'unloaded' for face in cold['coldBefore']['serifFaces'])
static = read('qa/static-audit.json')
assert not static['warnings'] and not static['failures']
result = {'status': 'PASS', 'sourceSha256': identity['sha256'],
          'continuousMainParagraphs': len(main_pairs), 'continuousMainWordsReported': 92278,
          'methodParagraphs': 7, 'displayedPrimaryChunks': 30,
          'coverageUnits': 64, 'validLocatorRanges': locator_count,
          'finalRouteChunksVerified': 24,
          'finalRevisionChunksReread': len(route_ledger['finalRevisionRereads']),
          'exactParagraphParity': parity['paragraphs'],
          'browserRenderedVisits': visits, 'staticPasses': static['passes'],
          'htmlSha256': file_hash('selfie.html'), 'storyDataSha256': file_hash('story-data.json'),
          'rootPersonalAcceptance': False, 'publicationAllowed': False}
(base/'qa/record-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False))

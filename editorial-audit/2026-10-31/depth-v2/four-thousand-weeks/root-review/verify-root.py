from pathlib import Path
import datetime
import hashlib
import html
import json
import re

R = Path(__file__).resolve().parent
H = R.parent
Q = R / 'qa'
load = lambda p: json.loads(p.read_text())
sha = lambda b: hashlib.sha256(b).hexdigest()
slice_sha = lambda screens: sha(json.dumps(screens, ensure_ascii=False, sort_keys=True).encode())
original = load(R / 'input-story-data.json')
final = load(H / 'story-data.json')
ledger = load(R / 'reading-ledger.json')
repairs = load(R / 'repairs.json')
old = {s['id']: s for s in original['screens']}
new = {s['id']: s for s in final['screens']}
assert list(old) == list(new) and len(new) == 87
assert {k:v for k,v in original.items() if k not in ['screens','modes']} == {k:v for k,v in final.items() if k not in ['screens','modes']}
actual_original = []
for row in ledger['screenDisplays']:
    selected = original['screens'][row['start']:row['end']]
    assert row['corpusSliceSha256'] == slice_sha(selected)
    assert row['ids'] == [s['id'] for s in selected] and row['completeDisplayedRangePersonallyRead']
    actual_original.extend(row['ids'])
assert actual_original == list(old)

matched_final = set()
for key in ['changedDisplays','routeDisplays','coreAdditionDisplays']:
    for row in ledger.get(key, []):
        assert row['completeDisplayedRangePersonallyRead']
        selected = [new[sid] for sid in row['ids']]
        if slice_sha(selected) == row['corpusSliceSha256']:
            matched_final.update(row['ids'])
essential = [s for s in final['screens'] if s['level'] <= 1]
assert [sid for row in ledger['routeDisplays'] for sid in row['ids']] == [s['id'] for s in essential]
core_additions = [s for s in final['screens'] if s['level'] == 2]
assert [sid for row in ledger['coreAdditionDisplays'] for sid in row['ids']] == [s['id'] for s in core_additions]
changed = {row['screen'] for row in repairs}
assert len(changed) == 21 and changed <= matched_final
plain = lambda s: html.unescape(re.sub(r'<[^>]+>', '', s))
for sid in new:
    assert new[sid]['level'] == old[sid]['level']
    if sid not in changed:
        assert new[sid] == old[sid], sid
        continue
    row = next(x for x in repairs if x['screen'] == sid)
    for language in ['ru','en']:
        assert plain(new[sid]['copy'][language]['body']) == row['languages'][language]['after']
        assert plain(old[sid]['copy'][language]['body']) == row['languages'][language]['before']
        assert {k:v for k,v in new[sid]['copy'][language].items() if k != 'body'} == {k:v for k,v in old[sid]['copy'][language].items() if k != 'body'}
    if sid == 'part-13-passage-03':
        assert old[sid]['primaryLocators'][0]['lastParagraph'] == 17
        assert new[sid]['primaryLocators'][0]['lastParagraph'] == 18
    else:
        assert new[sid]['primaryLocators'] == old[sid]['primaryLocators']

source_path = Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-8-private/four-thousand-weeks-edition.json')
source_bytes = source_path.read_bytes()
assert sha(source_bytes) == '4d59335257d507e204bcc3f28aab121c6cc0f0aead4cd092fc844787f1f337c0'
source = {row['file']: row for row in json.loads(source_bytes)}
seen = set()
words = 0
for row in ledger['primaryDisplays']:
    assert row['sourceSha256'] == sha(source_bytes) and row['completeDisplayedRangePersonallyRead']
    paragraphs = source[row['file']]['paragraphs'][row['start']-1:row['end']]
    assert row['rangeSha256'] == sha(json.dumps(paragraphs, ensure_ascii=False, separators=(',', ':')).encode())
    assert len(paragraphs) == row['end']-row['start']+1
    words += sum(len(p.split()) for p in paragraphs)
    seen.update((row['file'], i) for i in range(row['start'], row['end']+1))
plan = load(R / 'primary-selection-plan.json')
for row in plan['ranges']:
    assert all((row['file'], i) in seen for i in range(row['start'],row['end']+1))
assert len(ledger['primaryDisplays']) == 28 and len(plan['ranges']) == 27
assert {f'OEBPS/Text/content{i}.html' for i in range(1,15)} <= {f for f,i in seen}

protected = load(R / 'protected-inputs.json')
for name, digest in protected.items():
    assert sha(Path(name).read_bytes()) == digest, name
audit = load(Q / 'structural-audit.json')
assert audit['passes'] == 69 and not audit['failures'] and not audit['warnings']
qa = {}
helpers = {sha(p.read_bytes()): str(p.relative_to(H)) for p in list(R.glob('*.mjs')) + list(Q.glob('*.mjs'))}
for phase in ['cold','cold-en','resume','320','1440']:
    d = load(Q / ('browser-'+phase+'.json'))
    assert d['status'] == 'completed' and d['profileRemoved'] and d['processGroupTerminated']
    assert not d['runtimeErrors'] and not d['remoteRequests'] and not d['ownedProcessRemainders']
    for name, digest in d['inputHashes'].items():
        if name.endswith('.mjs'):
            assert digest in helpers, (phase,name,digest)
        else:
            assert sha((H/name).read_bytes()) == digest, (phase,name)
    helper_bindings = {name:helpers[digest] for name,digest in d['inputHashes'].items() if name.endswith('.mjs')}
    qa[phase] = {'status': d['status'], 'helperSnapshots': helper_bindings, 'profileRemoved': True, 'processGroupTerminated': True}
    if phase.startswith('cold'):
        assert d['coldBefore']['scroll'] == d['coldAfter']['scroll'] == 100
        assert all(x == 'unloaded' for x in d['coldBefore']['serifStatus'])
    if phase in ['320','1440']:
        assert len(d['layouts']) == 40 and sum(x['count'] for x in d['routes']) == 354
        assert d['sources'] == {'open':True,'count':1,'expected':1}
report = {
 'atUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'PASS', 'rootAcceptanceYetGranted':False,
 'originalRuEnPairsPersonallyRead':87,
 'finalEssentialRuEnPairsReread':25,
 'finalCoreAdditionsWithBothActualRouteEdgesReread':40,
 'finalChangedPairsPersonallyRead':21,
 'finalChangedReadMethod':'Level1 changes reread in complete final Essential; level2 changes in final Core additions with both adjacent edges; seven level3 changes reread separately. Earlier intermediate revision reads are retained, not counted as final if hashes differ.',
 'primaryActualRanges':28, 'primaryPlannedRangesCovered':27,
 'primaryUniqueParagraphs':len(seen), 'primaryDisplayedWhitespaceWords':words,
 'rootContinuousWholePrimaryRead':False,
 'protectedInputBindingsUnchanged':len(protected),
 'runtime':qa, 'routePositions':708, 'representativeLayouts':80,
 'harnessCorrections':'Two layout-run failures were harness assumptions: expecting2Sources entries instead of actual1, and retaining a final-screen selector from another book. Reports and helper versions archived. No reader change was required; corrected final layout runs pass. Successful resume uses its archived executed helper; cold runs use their unchanged original helper.',
 'physicalSafariPwaTested':False,
 'metrics':load(H/'metrics.json'),
 'contentHashes':{name:sha((H/name).read_bytes()) for name in ['story-data.json','four-thousand-weeks.html','draft.ru.md','draft.en.md','coverage-map.json','coverage-map.md','sources.md']}
}
(Q/'root-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','originalRuEnPairsPersonallyRead','finalChangedPairsPersonallyRead','primaryActualRanges','primaryUniqueParagraphs','primaryDisplayedWhitespaceWords','protectedInputBindingsUnchanged','routePositions','representativeLayouts']}))

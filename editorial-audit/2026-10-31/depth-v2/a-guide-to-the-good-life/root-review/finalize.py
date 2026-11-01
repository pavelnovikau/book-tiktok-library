from pathlib import Path
import datetime
import hashlib
import json

H = Path(__file__).resolve().parent.parent
R = H / 'root-review'
load = lambda p: json.loads(p.read_text())
dump = lambda p, d: p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
assert not (R / 'personal-review.json').exists(), 'Acceptance is a frozen exact-version record.'
d = load(H / 'story-data.json')
l = load(R / 'reading-ledger.json')
m = load(R / 'qa/metrics.json')
integrity = load(R / 'qa/root-integrity.json')
parity = load(R / 'qa/parity-check.json')
assert l['allCurrentPairsRead'] and l['originalCompleteRuEnDeepRead']
assert len(l['deepReadPairIds']) == 85 and len(set(l['deepReadPairIds'])) == 85
assert len(l['essentialReadPairIds']) == 29 and len(l['coreAddedPairsReread']) == 32
assert len(l['finalChangedPairIdsReread']) == 10
assert set(l['finalChangedPairIdsReread']) == set(integrity['changedPairIds'])
assert len(l['primaryRangesActuallyRead']) == 34
assert len(l['all21SuggestedPrimaryRangesPersonallyRead']) == 21
assert l['sourcesRead'] and l['coverageMapRead'] and l['wholeChapter20And22PrimaryPersonallyRead']
assert all(f['status'] == 'repaired-and-personally-reread' for f in l['pendingFindings'])
assert len(l['pendingFindings']) == 7
assert d['targetModes'] == {'essential': 29, 'core': 61, 'deep': 85}
assert m['unitCount'] == 73 and m['paragraphPairs'] == 153
for name, digest in m['currentContentHashes'].items():
    assert sha(H / name) == digest, name
assert sha(H / 'story-data.json') == l['currentFinalStoryDataSha256']
assert parity['allAuthoredFieldsMatchEmbedding'] and parity['actualPairedParagraphsMatchConnectedDrafts'] == 153
assert integrity['suggestedPrimarySelectionsCovered'] == 21 and integrity['protectedFilesUnchanged']
assert len(integrity['allSixRouteExports']) == 6
assert all(v['exactInOrder'] for v in integrity['allSixRouteExports'].values())

source = load(H / 'source-hashes.json')
source_dir = Path(source['privateSourceDirectory'])
assert source['fileCount'] == len(source['files']) == 358
for row in source['files']:
    assert sha(source_dir / row['file']) == row['sha256'], row['file']
for row in l['primaryRangesActuallyRead']:
    p = source_dir / row['file']
    assert sha(p) == row['fileSha256']
    chunk = p.read_text()[row['start']:row['end']]
    assert hashlib.sha256(chunk.encode()).hexdigest() == row['chunkSha256']
for row in l['additionalPrimaryActuallyRead']:
    assert row['wholeHtmlBodyTextPersonallyRead'] and sha(Path(row['path'])) == row['sha256']
protected = load(R / 'protected-baseline.json')['files']
assert len(protected) == 375
for row in protected:
    assert sha(Path(row['path'])) == row['sha256'], row['path']
audit = load(R / 'qa/structural-audit.json')
assert audit['passes'] == 69 and not audit['warnings'] and not audit['failures']
browsers = {phase: load(R / f'qa/browser-{phase}.json') for phase in ['320', '1440', 'cold', 'resume']}
for phase, b in browsers.items():
    assert b['status'] == 'completed' and not b['runtimeErrors'] and not b['remoteRequests']
    assert b['profileRemoved'] and b['processGroupTerminated'] and not b['ownedProcessRemainders']
    for name, digest in b['inputHashes'].items():
        assert sha(H / name) == digest, (phase, name)
assert browsers['cold']['coldBefore']['scroll'] == browsers['cold']['coldAfter']['scroll'] == 100
assert all(s == 'unloaded' for s in browsers['cold']['coldBefore']['serifStatus'])
assert browsers['cold']['radioArrowKeepsId']
assert len(browsers['resume']['deeperResume']) == 4
assert all(all(v for k, v in row.items() if k not in ['l', 'lower']) for row in browsers['resume']['deeperResume'])
assert all(browsers['resume']['reload'].values()) and browsers['resume']['invalidCurrentId']
for phase in ['320', '1440']:
    assert len(browsers[phase]['routes']) == 6 and len(browsers[phase]['layouts']) == 40
    assert not any(row['bad'] for row in browsers[phase]['routes'])

visuals = [
    'qa/320-mother-and-water-en-dark-sans.png',
    'qa/320-medication-objection-ru-light-serif.png',
]
for name in visuals:
    assert (R / name).is_file()
l.update(
    status='root-personal-reading-complete-and-accepted',
    rootPersonalAcceptance=True,
    publicationAllowed=True,
    atUtc=stamp,
    publicationScope='Only the exact Irvine candidate recorded in personal-review.json; other books remain held.',
    visualScreenshotsPersonallyInspected=[{'file': name, 'sha256': sha(R / name)} for name in visuals],
)
l['shorterRouteReviewPlan'] = 'Completed: all29 Essential pairs; all32 Core additions with both adjacent route edges; all10 final changed pairs reread.'
dump(R / 'reading-ledger.json', l)

coverage = load(H / 'coverage-map.json')
coverage_before = json.loads(json.dumps(coverage))
preacceptance_map_sha = sha(H / 'coverage-map.json')
coverage.update(
    rootPersonalAcceptance=True,
    publicationAllowed=True,
    rootPersonalReview='root-review/personal-review.json',
    rootAcceptanceScope='Exact current retelling. Full main-source reading belongs to writer ledger; root primary reading is selective.',
)
for row in coverage['keyPrimaryPassagesForRoot']:
    assert row['label'] in l['all21SuggestedPrimaryRangesPersonallyRead']
    row['rootReadStatus'] = 'personally-read-in-full-bounded-ranges'
dump(H / 'coverage-map.json', coverage)
check = json.loads(json.dumps(coverage))
check.pop('rootPersonalReview'); check.pop('rootAcceptanceScope')
check['rootPersonalAcceptance'] = False; check['publicationAllowed'] = False
for row in check['keyPrimaryPassagesForRoot']:
    row['rootReadStatus'] = 'pending'
assert check == coverage_before, 'Only acceptance metadata may change after runtime QA.'
coverage_text = (H / 'coverage-map.md').read_text()
coverage_text = coverage_text.replace(
    'All chapters below were read completely. Coverage means substantive selection, not reproduction of every example. Exact unit-to-screen segmentation and primary ranges are in coverage-map.json. Root personal review is pending.',
    'The implementation ledger records complete reading of the English main chapters below. Coverage means substantive selection, not reproduction of every example. Root personally read the complete bilingual retelling, omissions and selected actual primary passages; this is not root continuous whole-primary reading. Exact acceptance is recorded in root-review/personal-review.json. Unit-to-screen segmentation and primary ranges are in coverage-map.json.',
)
(H / 'coverage-map.md').write_text(coverage_text)

content_names = ['story-data.json', d['slug'] + '.html', 'draft.ru.md', 'draft.en.md']
exact = {name: sha(H / name) for name in content_names}
qa = {
    'structuralChecks': 69,
    'exactDraftDataEmbeddedParagraphParity': True,
    'pairedParagraphs': 153,
    'allSixRouteExportsExact': True,
    'freshRoutePositions': sum(row['count'] for phase in ['320', '1440'] for row in browsers[phase]['routes']),
    'representativeLanguageThemeFontLayouts': 80,
    'viewports': [[320, 568], [1440, 900]],
    'genuinelyFirstColdSerifPreserves100px': True,
    'settingsRadioArrowsCannotPage': True,
    'fourExplicitNonfictionDeeperResumePaths': True,
    'actualReloadPreservesLanguageDepthIdAndGlobalPreferences': True,
    'legacyIdsIsolatedAndUnknownCurrentIdOffersStart': True,
    'actualRenderedFontsChecked': True,
    'runtimeErrors': [], 'remoteRuntimeRequests': [],
    'ownedChromeCleanup': True, 'physicalSafariPwaTested': False,
    'visualInspection': l['visualScreenshotsPersonallyInspected'],
    'preacceptanceCoverageSha256': preacceptance_map_sha,
    'acceptedCoverageSha256': sha(H / 'coverage-map.json'),
    'postQaDifference': 'Only coverage acceptance/status metadata and documentation changed. Retelling, drafts, HTML, source ranges, chapter/unit maps and QA harness remain byte-identical to fresh QA. Original preacceptance flags in QA proofs are historical.',
}
assert qa['freshRoutePositions'] == 700
report = {
    'schemaVersion': 1, 'slug': d['slug'], 'atUtc': stamp,
    'verdict': 'PASS-after-root-repair',
    'rootPersonalAcceptance': True, 'publicationAllowed': True,
    'contentMode': 'explanatory', 'counts': d['targetModes'], 'metrics': m['modes'],
    'exactContentHashes': exact,
    'readingLedgerSha256': sha(R / 'reading-ledger.json'),
    'inputReadySha256': sha(R / 'input-ready.json'),
    'personalReading': {
        'all85OriginalRuEnPairsCompletelyRead': True,
        'all10FinalChangedPairsReread': True,
        'coverAndFinalRead': True,
        'all29EssentialPairsRereadInOrder': True,
        'all32CoreAdditionsRereadWithBothAdjacentEdges': True,
        'routeReadingMethod': l['shorterRouteReadingMethod'],
        'completeChapterUnitMapAndOmissionsRead': True,
        'sourcesRead': True,
        'rootWholePrimaryContinuouslyRead': False,
        'rootActualPrimaryRanges': l['primaryRangesActuallyRead'],
        'all21SuggestedSelectionsCovered': True,
        'wholeEnglishChapters20And22Read': True,
        'wholeRussianEditionInfoAndScientificEditorPrefaceRead': l['additionalPrimaryActuallyRead'],
        'narrowCurrentGuidanceChecks': l['narrowCurrentGuidanceChecks'],
    },
    'sourceScope': {
        'englishEdition': 'User-owned OUP ©2009/package2008, ISBN9780195374612.',
        'writer': 'Records complete introduction,22 main chapters and reading program, with selected notes only. Hash/interval integrity checked separately from root selected primary reading.',
        'root': '34 actually read bounded primary intervals cover all21 proposed selections. Chapters20 and22 and the reading program read completely. No claim of root continuous whole-book reading.',
        'russian': 'MIF2021, Vasily Gorokhov translation, Stanislav Naranovich scientific-editor preface, ISBN9785001461937. Root read full edition-info/preface bodies, not the full Russian translation.',
        'rendering': 'Original RU/EN condensation; no published-English/Russian translation collation or Greek/Latin critical-edition certification.',
        'contemporaryChecks': 'Selected NICE recommendations and NIMH GAD treatment section only. They do not constitute systematic scientific validation or a full literature update.',
    },
    'findingsClosed': l['pendingFindings'],
    'requiredOpenFindings': [],
    'meaningAssessment': 'Preserves the whole-life strategy, distinct ancient voices, virtue/tranquility disagreement, negative visualization and its grief limits, explicit Irvine reconstruction of control, past/present fatalism, voluntary discomfort, review and social duties, insults and discipline, grief/anger/wealth/exile/aging arguments, the author’s polemics and reconstruction, actual personal tests and final uncertainty. Concrete cases join the argument rather than generic moral lessons. The separate Russian editor objection remains separate. Author viewpoints have not been replaced by root preferences.',
    'omissions': 'All22 main chapters, introduction and reading program represented. The map explicitly condenses biographies, subsidiary cases, lists, technical ancient-source detail and most notes. It does not reproduce every example or replace an unabridged edition. Historical clinical/political claims remain attributed arguments, not current therapeutic advice.',
    'qa': qa,
    'protectedFilesUnchanged': len(protected),
    'limitations': [
        'Root completely read the resulting bilingual retelling, with selective direct primary checking rather than continuous whole-source reading.',
        'Writer main-text reading and source hashes do not certify all notes, underlying studies or ancient editions.',
        'No whole Russian translation or published English condensation collation.',
        'Two narrow contemporary medical-context checks do not make this a current clinical review.',
        'Offline Chrome and viewport tests; physical iPhone/Safari/PWA untested.',
    ],
}
dump(R / 'personal-review.json', report)
(R / 'personal-review.md').write_text('''# A Guide to the Good Life — root personal acceptance

PASS after seven findings were repaired across ten paired screens. Acceptance applies only to the final hashes in personal-review.json.

I completely read all85 original RU/EN pairs, including cover and final. I reread all29 Essential pairs in order, and every one of the32 Core additions completely with both adjacent route edges. The common Essential prose had already been reread in order; this does not claim a third complete reading of identical shared prose. I personally reread all10 final changed pairs after their repairs. All six route exports match the current JSON/HTML exactly.

I read the full chapter/unit coverage and omission map and Sources. I directly read34 bounded English primary intervals covering all21 proposed selections, including complete chapters20 and22 and the reading program. I also read the actual complete Russian edition-information and scientific-editor preface bodies. Root primary reading was selective, not a continuous whole-book read or dual-edition collation. The writer ledger separately records the full introduction,22 chapters and reading program;358 source hashes and375 protected inputs were checked.

The repairs remove intrusive remarks about how the retelling should be written, resolve first-use names absent from Essential, and restore the actual indirect sting of humor/silence that an overgentle title obscured. They keep the author’s difficult political and counseling positions and final doubts with clear attribution. Naranovich’s disagreement remains an editor’s separate voice. No management/moral checklist replaces the book’s argument, examples and real practices.

Final routes29/61/85. Deep has7870RU/9095EN main-body words, including the reading program and shared final, excluding cover/headings/UI/Sources. Body time is43.72/41.34minutes at180/220wpm; UI framing/headings give46/44minutes. These are reading estimates, not proof of quality.

Fresh root QA passed69 structural checks,700 route positions and80 representative language/theme/font layouts. First genuinely unloaded Serif selection preserved100px scroll; Settings radio arrows, focus/Tab/Escape, explicit deeper-resume labels, actual reload/global preferences, legacy isolation, invalid-ID fallback and rendered fonts passed. I inspected both actual320px screenshots through their last lines. Zero runtime errors or remote runtime requests; owned Chrome groups/profiles removed. No physical Safari/PWA claim.

Only coverage acceptance/status metadata and documentation changed after these tests; all runtime/draft content and actual source locators remain identical. Historical preacceptance proof flags remain intact. Two narrow NICE/NIMH context checks are not a systematic scientific update. Publication is allowed only for this exact Irvine candidate; other unaccepted content remains held.
''')

current = f'Current root acceptance {stamp}: PASS for the exact version in root-review/personal-review.json. Routes29/61/85; Deep7870RU/9095EN main-body words; UI46/44minutes. Earlier worker-phase numbers, hashes and pending statuses below are historical. Root completely read the bilingual retelling and selected actual primary passages, not the whole primary book continuously.'
for name in ['QA.md', 'sources.md', 'HANDOFF.md']:
    assert (R / ('input-' + name)).is_file()
    (H / name).write_text(current + '\n\n---\n\n' + (H / name).read_text())

ready = load(R / 'input-ready.json')
ready.update(
    status='root-personally-accepted', rootPersonalAcceptance=True,
    publicationAllowed=True, bookContentPublicationAllowed=True,
    rootAcceptedAtUtc=stamp, rootPersonalReviewRecord=str(R / 'personal-review.json'),
    rootPersonalReviewSha256=sha(R / 'personal-review.json'),
    rootReadingLedger=str(R / 'reading-ledger.json'),
    inputReadySha256=sha(R / 'input-ready.json'),
    ruBodyWords=7870, enBodyWords=9095,
    readingMetrics=m['modes'],
)
ready['historicalWorkerQa'] = ready.pop('qa')
ready['rootQa'] = qa
ready['historicalWorkerRootReviewRequired'] = ready.pop('rootReviewRequired')
ready['rootReviewRequired'] = []
ready['remainingRequiredWork'] = ['Integrate only the exact accepted HTML and catalogue counts/times.', 'Check exact PR head and production changed assets.']
ready['meaningfulLimitations'] = [x for x in ready['meaningfulLimitations'] if not x.startswith('Root must personally')]
ready['meaningfulLimitations'].append('Root exact-version acceptance is now recorded; source/translation and physical-device limits remain.')
ready['exactContentHashes'] = {name: sha(H / name) for name in ready['exactContentHashes']}
paths = sorted(p for p in H.rglob('*') if p.is_file() and p.name != 'ready.json' and '__pycache__' not in p.parts)
ready['files'] = [{'path': str(p), 'relativePath': str(p.relative_to(H)), 'sha256': sha(p), 'bytes': p.stat().st_size} for p in paths]
ready['allArtifactHashes'] = {str(p.relative_to(H)): {'path': str(p), 'sha256': sha(p), 'bytes': p.stat().st_size} for p in paths}
dump(H / 'ready.json', ready)
for name, row in ready['allArtifactHashes'].items():
    assert sha(Path(row['path'])) == row['sha256'], name
assert all(sha(H / name) == digest for name, digest in exact.items())
print(json.dumps({'accepted': True, 'counts': d['targetModes'], 'bindings': len(paths), 'hashes': exact, 'rootReviewSha256': sha(R / 'personal-review.json')}))

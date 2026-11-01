from pathlib import Path
import datetime
import hashlib
import json

R = Path(__file__).resolve().parent
H = R.parent
load = lambda p: json.loads(p.read_text())
dump = lambda p, d: p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
old_ready = load(R / 'input-ready.json')
assert not load(H / 'ready.json')['rootPersonalAcceptance']
ledger = load(R / 'reading-ledger.json')
parity = load(R / 'qa/parity-check.json')
metrics = load(R / 'qa/metrics.json')
primary = load(R / 'qa/primary-integrity.json')
audit = load(R / 'qa/structural-audit.json')
assert audit['passes'] == 69 and not audit['warnings'] and not audit['failures']
assert parity['status'] == primary['status'] == 'PASS'
assert len(parity['changedPairIds']) == 13
assert {x['id'] for x in load(H / 'story-data.json')['screens']} == {i for x in ledger['screenDisplays'] for i in x['ids']}
assert len({i for x in ledger['routeDisplays'] for i in x['ids']}) == 49
assert len({i for x in ledger['coreAdditionDisplays'] for i in x['ids']}) == 59
assert len({i for x in ledger['changedDisplays'] for i in x['ids']}) == 13
assert primary['rootActualPrimaryRanges'] == 34
assert all(x['status'] == 'repaired-and-personally-reread' for x in ledger['findings'])
browsers = {}
for phase in ['cold', 'cold-en', 'resume', '320', '1440']:
    d = load(R / ('qa/browser-' + phase + '.json'))
    assert d['status'] == 'completed' and d['profileRemoved'] and d['processGroupTerminated']
    assert not d['runtimeErrors'] and not d['remoteRequests']
    assert d['inputHashes']['story-data.json'] == sha(H / 'story-data.json')
    assert d['inputHashes']['essentialism.html'] == sha(H / 'essentialism.html')
    assert d['inputHashes']['root-review/cold-settings.mjs'] == sha(R / 'cold-settings.mjs')
    browsers[phase] = d
assert all(browsers[p]['coldBefore']['scroll'] == browsers[p]['coldAfter']['scroll'] == 100 for p in ['cold', 'cold-en'])
route_positions = sum(r['count'] for p in ['320', '1440'] for r in browsers[p]['routes'])
layouts = sum(len(browsers[p]['layouts']) for p in ['320', '1440'])
assert route_positions == 1128 and layouts == 80
assert len(browsers['resume']['deeperResume']) == 4
for p, before in load(R / 'qa-protected-baseline.json').items():
    assert sha(Path(p)) == before, p
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
ledger.update(
    rootPersonalAcceptance=True,
    completeDraftRead=True,
    finalChangedPairsPersonallyReread=13,
    all49EssentialPairsReread=True,
    all59CoreAdditionsRereadWithAdjacentEdges=True,
    finalMethodRuEnPersonallyRead=True,
    sourceRelationshipLocatorAdded='identity unit: gl1 P57; verified from actually read primary',
    requiredOpenFindings=[],
    publicationAllowed=True
)
dump(R / 'reading-ledger.json', ledger)
note = (
    'Current root acceptance ' + stamp + ': personally accepted exact expanded version. '
    '49/108/125 screens; Deep8749RU/10230EN noncover body words, UI52/50minutes. '
    'Root completely read all125 original RU/EN screens, reread all49Essential pairs and all59Core additions '
    'with adjacent route edges, then personally reread all13final changed pairs. The two final changed '
    'Essential entries were reread separately after route repair; shared prose was not read a third time. '
    'Full247-line coverage/omission map, Sources and handoff read.34actual selected primary ranges checked; '
    'no continuous whole-primary or published-English collation claim. Seven findings closed, including '
    'the Google sleep-pod conclusion, strength of the choice principle and first surviving Anna introduction. '
    '69structural checks,1128route positions,80representative layouts, RU/EN genuinely cold first Serif '
    'at100px, four explicit nonfiction deeperContinue paths, real reload/legacy isolation and cleanup pass. '
    'Actual320px screenshots personally inspected; physical Safari/PWA untested. Writer QA below is historical. '
    'This acceptance supersedes the historical writer handoff flags. Publication may use only these frozen hashes.'
)
for name in ['sources.md', 'QA.md', 'HANDOFF.md', 'coverage-map.md']:
    p = H / name
    p.write_text('Current editorial acceptance\n\n' + note + '\n\n---\n\n' + p.read_text())
dump(H / 'metrics.json', metrics)
content_hashes = {n: sha(H / n) for n in ['story-data.json', 'essentialism.html', 'draft-ru.md', 'draft-en.md', 'coverage-map.json', 'coverage-map.md', 'sources.md', 'metrics.json']}
report = {
    'schemaVersion': 1,
    'slug': 'essentialism',
    'atUtc': stamp,
    'verdict': 'PASS',
    'rootPersonalAcceptance': True,
    'publicationAllowed': True,
    'contentMode': 'explanatory',
    'counts': {'essential': 49, 'core': 108, 'deep': 125},
    'metrics': metrics['modes'],
    'exactContentHashes': content_hashes,
    'readingLedgerSha256': sha(R / 'reading-ledger.json'),
    'inputReadySha256': sha(R / 'input-ready.json'),
    'personalReading': {
        'all125OriginalRuEnScreensCompletelyRead': True,
        'all13FinalChangedPairsReread': True,
        'coverAndFinalRead': True,
        'all49EssentialPairsReread': True,
        'all59CoreAdditionsRereadCompletelyWithBothAdjacentEdges': True,
        'routeReadingMethod': ledger['shorterRouteReadingMethod'],
        'complete247LineCoverageOmissionMapRead': True,
        'sourcesAndHandoffRead': True,
        'selectedActualPrimaryRanges': ledger['primaryDisplays'],
        'all26AdditionalPlannedSelectionsCovered': True,
        'rootWholePrimaryContinuouslyRead': False
    },
    'sourceScope': {
        'edition': 'MIF2015 Russian translation by I. Aizyatulova, ISBN9785000573471; original2014',
        'actualRootReading': '34bounded primary ranges,444unique extracted paragraphs; complete retelling/routes/map. Selective primary checking.',
        'writerReportedMainReading': old_ready['sourceReading'],
        'writerEvidenceIntegrity': primary['writerReadingLedgerIntegrity'],
        'publishedEnglishCollation': False,
        'figuresVisuallyRead': False,
        'underlyingStudiesIndependentlyAudited': False,
        'notesEndmatterContinuouslyRead': False
    },
    'findingsClosed': ledger['findings'],
    'requiredOpenFindings': [],
    'meaningAssessment': 'The developed condensation retains contribution and the recurring explore/eliminate/execute system, concrete cases, actual procedures and important author qualifications across20chapters and the leadership appendix. Root restored the author position rather than replacing it with editor inference. No required quota-padding or missing central-argument finding remains.',
    'omissions': 'Whole map read. Research/history anecdotes and illustrations are selectively condensed as disclosed. Images, most notes and anniversary additions remain outside scope. The appendix-before-final reorder is explicit. Approval is for this retained argument, not the whole edition or every underlying study.',
    'repairs': {'changedPairIds': parity['changedPairIds'], 'exactLanguageChanges': 'root-review/repairs.json', 'metadataChanges': ['Method separates writer continuous reading from root selective checking.', 'Identity source locators add directly checked gl1 P57 for Anna.']},
    'qa': {
        'structuralPasses': 69,
        'warnings': 0,
        'failures': 0,
        'allSixRouteDocumentsMatchExactly': True,
        'allAuthoredFieldsMatchEmbedding': True,
        'rootRoutePositions': route_positions,
        'representativeLayouts': layouts,
        'coldFirstSerifRuEn': 'Both genuinely unloaded before selection;100px exact scroll preserved.',
        'explicitDeeperContinuePaths': 4,
        'reloadPreferencesAndAuthenticLegacyIsolation': True,
        'screenshotsPersonallyViewed': ['root-review/qa/320-promise-en-dark-sans.png', 'root-review/qa/320-helplessness-ru-light-serif.png'],
        'runtimeErrors': 0,
        'externalRuntimeRequests': 0,
        'ownedChromeProcessesProfilesRemoved': True,
        'physicalSafariPwa': False
    },
    'primaryIntegrity': primary,
    'protectedInputHashesUnchanged': 45,
    'limitations': ['Selective root primary reading; no continuous root whole-source read.', 'No published-English collation or systematic spelling verification against it.', 'No visual source figures, full notes/endmatter reading or underlying-study certification.', 'Chrome emulation only; physical iPhone/Safari/PWA untested.']
}
dump(R / 'personal-review.json', report)
md = '# Root personal review — Essentialism\n\nPASS for exact accepted hashes. Publication authorized for this version.\n\n' + note + '\n\n'
md += 'The required corrections restore the author position on choice and the positive sleep-pod conclusion; restore the ticket recipient rescuing a girl; remove source-audit asides from ordinary prose; clarify names, antecedents and the shorter-route Anna/leadership introductions. All final changed prose was personally reread.\n\n'
md += 'The root read the complete retelling and its route continuity, full coverage/omission map and34actual primary ranges. Writer records of27chunks/1096paragraphs were checked for interval/hash integrity; this does not turn that ledger into root whole-source reading. Material edition, image, research and English-collation limits remain explicit.\n\n'
md += 'Counts:49/108/125. Deep8749RU/10230EN body words; UI52/50minutes. Fresh69structural checks,1128route positions and80representative layouts pass. Cold RU/EN Serif retained100px, saved deeperContinue and legacy cases pass; no external runtime requests/errors. Owned Chrome cleaned. No physical Safari/PWA claim.\n\n'
md += 'Exact runtime JSON/HTML:\n\n' + '\n'.join('- ' + n + ': ' + content_hashes[n] for n in ['story-data.json', 'essentialism.html']) + '\n'
(R / 'personal-review.md').write_text(md)
payload = {}
for p in sorted(H.rglob('*')):
    if p.is_file() and p.name != '.DS_Store' and p != H / 'ready.json' and '__pycache__' not in p.parts:
        payload[p.relative_to(H).as_posix()] = {'path': str(p), 'sha256': sha(p), 'bytes': p.stat().st_size}
ready = {
    'schemaVersion': 1,
    'slug': 'essentialism',
    'atUtc': stamp,
    'status': 'root-personally-accepted',
    'rootPersonalAcceptance': True,
    'publicationAllowed': True,
    'bookContentPublicationAllowed': True,
    'counts': report['counts'],
    'bodyMetrics': metrics,
    'sourceReading': report['sourceScope'],
    'rootPersonalReviewRecord': str(R / 'personal-review.json'),
    'rootPersonalReviewSha256': sha(R / 'personal-review.json'),
    'rootReadingLedger': str(R / 'reading-ledger.json'),
    'rootReadingLedgerSha256': sha(R / 'reading-ledger.json'),
    'historicalWriterReady': 'root-review/input-ready.json',
    'historicalWriterVerification': old_ready['verification'],
    'verification': report['qa'],
    'exactContentHashes': content_hashes,
    'manifestHashConvention': 'All payload artifacts frozen; ready.json excludes itself to avoid a cycle. Original writer ready is preserved separately.',
    'files': payload,
    'allArtifactHashes': payload
}
dump(H / 'ready.json', ready)
for name, row in payload.items():
    assert sha(H / name) == row['sha256'], name
print(json.dumps({'status': ready['status'], 'bindings': len(payload), 'jsonSha256': content_hashes['story-data.json'], 'htmlSha256': content_hashes['essentialism.html'], 'rootReportSha256': ready['rootPersonalReviewSha256'], 'counts': report['counts']}))

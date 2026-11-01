from pathlib import Path
import json, hashlib, datetime, shutil

p = Path(__file__).resolve().parent.parent
r, q = p / 'root-review', p / 'root-review/qa'
load = lambda f: json.loads(Path(f).read_text())
sha = lambda f: hashlib.sha256(Path(f).read_bytes()).hexdigest()
write = lambda f, x: Path(f).write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
d, metrics, audit = load(p/'story-data.json'), load(q/'metrics.json'), load(q/'structural-audit.json')
browsers = {k: load(q/f'browser-{k}.json') for k in ['320', '1440', 'consent', 'cold']}
assert all(x['status'] == 'completed' and x['profileRemoved'] and x['processGroupTerminated'] and not x['runtimeErrors'] and not x['remoteRequests'] for x in browsers.values())
assert audit['passes'] == 69 and not audit['warnings'] and not audit['failures']
hashes = {n: sha(p/n) for n in ['story-data.json', 'the-lost-world.html']}
ledger = load(r/'reading-ledger.json')
ledger.update(status='root-personal-reading-completed', atUtc=stamp, finalCandidateHashes=hashes, rootPersonalAcceptance=True, publicationAllowed=True, wholePrimaryContinuouslyReadByRoot=False)
write(r/'reading-ledger.json', ledger)
report = {
    'schemaVersion': 1, 'atUtc': stamp, 'slug': 'the-lost-world', 'candidate': 'expanded-depth-v2',
    'verdict': 'PASS', 'reviewer': 'root', 'rootPersonalAcceptance': True, 'bookContentPublicationAllowed': True,
    'onlyTheseHashesApproved': hashes, 'allOtherUnacceptedBooksRemainHeld': True,
    'readScope': {
        'all125RuEnPairs': True, 'deepSequenceComplete': True, 'essentialRouteComplete': True, 'coreRouteComplete': True,
        'routeReadingMethod': ledger['routesMethod'], 'allChangedFinalPairsReread': True,
        'wholeChapterSceneMapRead': True, 'sourcesAndGlobalMetadataRead': True,
        'primaryRangesActuallyRead': ledger['primaryRangesActuallyRead'],
        'wholePrimaryContinuouslyReadByRoot': False, 'publishedRussianTranslationCollated': False
    },
    'counts': d['targetModes'], 'metrics': metrics,
    'literaryJudgment': {
        'sustainedStory': 'Malone narrates romantic vanity, newsroom errand, comic confrontation, investigation, forest journey, failed approaches, betrayal, captivity, rescues, war, escape and two distinct homecomings as actual events. No management lessons, invented exercises or replacement morals.',
        'viewpoint': 'Challenger reports his prior journey; Malone learns of the capture from Roxton; the Macdona newspaper frame and Malone correction of the sanitised public report remain. No invented omniscient scene.',
        'authorDifficulties': 'Fear, shame, ambition, bloodlust and pity remain distinct. Summerlee objects to war; Challenger celebrates conquest; massacre, enslavement and Malone discomfort remain in the story. Historical theories remain character-world claims.',
        'causalLinks': 'Separate camp raids, Gomez motive, Roxton capture shot and later missed rescue shot, Maretas independent aid, failed balloon, missed fork, actual descent and later-arriving rescue remain connected.',
        'ending': 'Public proof and specimen escape, uncertain later reports, Gladys already-completed marriage and the earlier chronology of the visit, diamond disclosure, equal shares and the offered hand remain. No certain specimen return/death or later expedition is invented.',
        'shorterRoutes': 'Essential ends before ascent, Core at the camp mystery. Both honestly disclose unfinished-opening scope. The invitation/self-restraint promise now precedes the lecture in Essential.',
        'depthDecision': '122 narrative paragraphs carry all16 chapters with sustained action, comedy, fear, changing trust and aftermath. Counts measure the resulting story; they are not a universal target.'
    },
    'rootChanges': [
        {'id': 'isolation', 'change': 'Promote invitation/self-restraint promise to Essential, restoring the missing antecedent for the lecture.', 'primary': 'L1549-1611 within actual root reading L1127-1611'},
        {'id': 'battle', 'change': 'Restore stated pity when finishing off the arrow-struck opponent, RU/EN.', 'primary': 'L6668-6675 within actual root reading L6530-6768'},
        {'id': 'first-journey', 'change': 'Rain and dwindling supplies force retreat, without narrowing the witness wet-season/approaching-rains descriptions, RU/EN.', 'primary': 'L1508-1518; approaching season also in recap L3325'},
        {'id': 'messenger', 'change': 'Clarify RU that money is enclosed for the messenger; EN already unambiguous.', 'primary': 'L5700-5708 within actual root reading L5589-5719'},
        {'id': 'rifle', 'change': 'Retain explicit room setting across the Core join and remove repeated name in RU.'},
        {'id': 'source-map', 'change': 'Correct intact-gate raid window to L4540-4607. Former L4485-4530 window concerns pterodactyl attack.'}
    ],
    'closedSuspicions': [
        {'id': 'money', 'result': 'Stationmaster comparison appears in the original L167-169; retained.'},
        {'id': 'broken-bridge', 'result': 'Roxton explicitly lets Manuel go; Zambo kills the fugitive later below. Retained sequence supported by L3975-4035.'},
        {'id': 'empty-camp', 'result': 'Later gate is open while enclosure stands as left; Malone calls but does not fire. Cartridge comes from Roxton capture shot. Earlier intact-gate raid is separate.'},
        {'id': 'release', 'result': 'Roxton misses the strangler, but his shot causes release. Qualification retained, L6380-6440.'}
    ],
    'verification': {
        'structuralPasses': 69, 'warnings': [], 'failures': [],
        'allAuthoredFieldsMatchEmbeddingExceptGeneratedModeTimes': True, 'connectedDraftParity': {'ru': 122, 'en': 122},
        'protectedBaselineFilesChecked': 131, 'unchangedProtectedFiles': 130,
        'externalChangeOnly': 'Parent-owned depth-v2/PLAN.json changed. Old collectors, reviews, root readers and installed skill files unchanged.',
        'rootBrowser': {
            'completeRuEnRoutePositionsAt320And1440': sum(z['count'] for k in ['320','1440'] for z in browsers[k]['routes']),
            'representativeLayoutsBothLanguagesThemesFonts': sum(len(browsers[k]['layouts']) for k in ['320','1440']),
            'actualDowngradePaths': len(browsers['consent']['downgrades']), 'savedModeReloadPaths': len(browsers['consent']['reloads']),
            'coldSerifNonzeroScrollPreserved': browsers['cold']['coldBefore']['scroll'] == browsers['cold']['coldAfter']['scroll'] > 0,
            'coldSettingsRadioArrowKeepsBookPosition': browsers['cold']['radioArrowKeepsId'],
            'legacyNamespaceSeededAndIsolated': True, 'cancelEscapeFinalAndSimulatedLifecycle': True,
            'offline': True, 'runtimeErrors': 0, 'remoteRequests': 0, 'ownedProfilesAndProcessesRemoved': True, 'physicalSafari': False
        },
        'visualInspection': ['320-fresh-cover', '320-bark-ru-light-serif', '320-shotgun-en-dark-sans', '1440-cover-ru-dark-sans'],
        'historicalWorkerReportsNotReclaimedAsFreshRootChecks': True
    },
    'omissionsAndLimits': [
        'Writer read complete English I-XVI continuously. Root checked selected actual passages and the full scene map; no continuous whole-primary root reading claimed.',
        'Inventories, taxonomy, repeated scenery and minor observations compressed. All16 chapters represented; not unabridged.',
        'No print-variant or published Russian translation collation, or modern biological/anthropological validation.',
        'Short routes explicitly unfinished; late outcomes behind volatile Deep consent.',
        'Chrome emulation and dispatched lifecycle events, not physical Safari/PWA validation.'
    ],
    'progressPolicy': 'Fresh book-tiktok.the-lost-world.depth-v2. namespace; actual legacy diamonds-choice state preserved but not resumed. Shared preferences retained. Deep consent revoked on downgrade/reload/simulated restored lifecycle; contents and global map depth-filtered.',
    'canonicalOldCollectorReadyReviewsAndRootReadersUntouched': True
}
write(r/'personal-review.json', report)
(r/'personal-review.md').write_text('# Root personal review - The Lost World\n\nPASS for the exact JSON/HTML hashes in personal-review.json. Root read all125 RU/EN pairs, both shorter routes, the complete16-chapter map, global metadata/sources and selected actual primary scenes. Complete continuous primary reading belongs to the writer, not root.\n\nThe story retains Malone first-person voice, adventure, humour, fear and vanity, captivity, separate rescues, violent war outcome, Maretas agency, failed balloon and actual exit, public proof, private disappointment and final offered hand. It is not a set of moral lessons.\n\nRoot restored pity in battle and the invitation/promise before the Essential lecture, clarified messenger money and Roxton rooms, and corrected the earlier raid locator. Final changed pairs reread.\n\n33/68/125 screens. Deep narrative8562 RU /10312 EN words; about48/47 minutes, with displayed estimate50. Short modes honestly disclose their unfinished scope.\n\n69 structural checks,904 complete RU/EN route positions at320/1440,80 selected theme/font layouts, real downgrade/reload/legacy-state checks, first cold Serif selection with nonzero scroll and Settings radio arrows passed. No runtime errors or remote requests; owned Chrome trees/profiles cleaned. No physical Safari claim.\n\nOnly this accepted version may be published. Other unaccepted book content remains held.\n')
shutil.copyfile(q/'metrics.json', p/'metrics.json')
for name in ['sources.md', 'QA.md']:
    with (p/name).open('a') as f:
        f.write('\n\n## Root personal acceptance - 2026-11-01\n\nCurrent counts33/68/125. Root read every RU/EN pair and the shorter routes, reviewed the complete16-chapter map and checked the actual primary windows in root-review/reading-ledger.json. Bounded corrections and exact accepted hashes are in root-review/personal-review.json. Current root QA is under root-review/qa. Earlier worker evidence remains historical input-version evidence. Complete primary reading belongs to the writer; root primary checking is selective.\n')
ready = load(r/'input-ready.json')
ready.update(atUtc=stamp, status='root-personally-accepted', rootPersonalAcceptance=True, publicationAllowed=True, candidateHashes=hashes, counts=d['targetModes'], metrics=metrics,
    rootReview={'path':'root-review/personal-review.json','sha256':sha(r/'personal-review.json'),'ledger':'root-review/reading-ledger.json'},
    verification={'exactAuthoringEmbeddedParity':True,'exactConnectedDraftScreenParity':True,'structuralAudit':'root-review/qa/structural-audit.json','structuralPasses':69,'structuralWarnings':0,'structuralFailures':0,'browserReports':[f'root-review/qa/browser-{k}.json' for k in browsers],'chromeEmulationOnly':True,'physicalSafari':False,'literaryAcceptanceByRoot':True,'allFinalChecksBindToCandidateHashes':True}, remainingReview=[])
ready['historicalInputReady'] = 'root-review/input-ready.json'
ready['deliverables'] = [{'path':str(f.resolve()),'relativePath':str(f.relative_to(p)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(p.rglob('*')) if f.is_file() and f.name != 'ready.json']
write(p/'ready.json', ready)
for x in ready['deliverables']:
    assert sha(x['path']) == x['sha256']
print(json.dumps({'status':ready['status'],'hashes':hashes,'rootReviewSha':sha(r/'personal-review.json'),'bindings':len(ready['deliverables']),'counts':d['targetModes'],'coldScroll':browsers['cold']['coldAfter']['scroll']},indent=2))

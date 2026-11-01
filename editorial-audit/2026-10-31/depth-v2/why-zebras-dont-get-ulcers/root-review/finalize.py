from pathlib import Path
import json, hashlib, datetime

H = Path(__file__).resolve().parent.parent
R = H/'root-review'
load = lambda p: json.loads(p.read_text())
dump = lambda p,d: p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
assert not (R/'personal-review.json').exists(), 'Acceptance is a frozen exact-version record.'
d = load(H/'story-data.json'); m = load(R/'qa/metrics-and-integrity.json'); l = load(R/'reading-ledger.json')
assert l['allCurrentPairsRead'] and len(l['deepReadPairIds']) == 107 and len(l['essentialReadPairIds']) == 37 and len(l['coreAddedPairsPersonallyReread']) == 33
assert len(l['primaryRangesActuallyRead']) == 45 and l['sourcesRead'] and l['completeCoverageMapRead']
assert m['inputHashes']['story-data.json'] == sha(H/'story-data.json')
assert m['inputHashes'][d['slug']+'.html'] == sha(H/(d['slug']+'.html'))
audit = load(R/'qa/structural-audit.json'); assert audit['passes'] == 69 and not audit['warnings'] and not audit['failures']
browsers = {p:load(R/f'qa/browser-{p}.json') for p in ['320','1440','cold','resume']}
for p,b in browsers.items():
    assert b['status'] == 'completed' and not b['runtimeErrors'] and not b['remoteRequests']
    assert b['profileRemoved'] and b['processGroupTerminated']
    for name,value in b['inputHashes'].items(): assert sha(H/name) == value, (p,name)
assert browsers['cold']['coldBefore']['scroll'] == browsers['cold']['coldAfter']['scroll'] == 100
assert all(s == 'unloaded' for s in browsers['cold']['coldBefore']['serifStatus'])
assert all(browsers['resume']['reload'].values()) and browsers['resume']['invalidCurrentId']
for f in load(R/'protected-baseline.json')['files']: assert sha(Path(f['path'])) == f['sha256']

l.update(status='root-personal-reading-complete-and-accepted',rootPersonalAcceptance=True,publicationAllowed=True,atUtc=stamp)
l['publicationScope'] = 'Only the exact expanded Zebra version recorded in personal-review.json. Other books and earlier versions remain outside this acceptance.'
dump(R/'reading-ledger.json',l)
report = {
 'schemaVersion':1,'slug':d['slug'],'atUtc':stamp,'verdict':'PASS-after-root-repair',
 'rootPersonalAcceptance':True,'publicationAllowed':True,'contentMode':'explanatory',
 'publicationScope':'Only this exact candidate, not other books or a scientific/medical certification.',
 'counts':d['targetModes'],'metrics':m['modes'],
 'exactContentHashes':{n:sha(H/n) for n in [d['slug']+'.html','story-data.json','draft-ru.md','draft-en.md']},
 'readingLedgerSha256':sha(R/'reading-ledger.json'),'inputReadySha256':sha(R/'input-ready.json'),
 'personalReading':{'all107OriginalRuEnPairsCompletelyRead':True,'allFiveFinalChangedPairsReread':True,'coverAndFinalRead':True,'essential37PairsRereadCompletely':True,'core33AddedPairsRereadCompletelyWithBothAdjacentEdges':True,'routeReadingMethod':l['shorterRouteReadingMethod'],'complete18Chapter68GroupedCaseMapAndOmissionsRead':True,'sourcesRead':True,'wholePrimaryContinuouslyReadByRoot':False,'selectedPrimaryRanges':l['primaryRangesActuallyRead'],'narrowOnlineChecks':l['onlineChecksActuallyRead']},
 'primaryScope':{'edition':'User-owned RU Piter2021, ISBN978-5-4461-1081-0; third-English-edition framework, not a2021 research update.','writerLedger':'Writer records complete reading of both prefaces and18 main chapter bodies, with selective notes. Main-body interval/hash integrity independently checked; this does not convert the writer claim into root whole-source reading.','rootDirectPrimaryChecks':'45 bounded passages, recorded with exact file/chunk hashes. Selected endocrine, ulcer, immune/cancer, development, depression, control, addiction, inequality and coping passages.','english':'Original English rendering of the new condensation; no published-English edition collation.','currentQualifications':'Five narrow qualification screens; six official/primary online checks. Border2019 abstract only. No systematic literature review.'},
 'findingsClosed':[
  {'id':'ZB-R01','screens':['unit-022'],'resolution':'Removed the editorial should-not-be-retold instruction; retained actual gastritis versus ulcer distinction.'},
  {'id':'ZB-R02','screens':['unit-076'],'resolution':'Restored the historical proposed recovery bridge involving stress, replenishment, glucocorticoids and serotonin-transporter expression. Kept its status as a hypothesis and the immediate later candidate-gene qualification.'},
  {'id':'ZB-R03','screens':['unit-044','unit-085','unit-095'],'resolution':'Made Essential references self-contained: possible psychological influence does not assign blame; the lever delivers an addictive drug; income distribution explicitly introduces the public-services pathway.'},
  {'id':'ZB-MAP-01','resolution':'Personally checked all68 grouped-case entry previews and repaired29 grouped-case source locators against45 actual bounded primary reads. All78 final entry/context anchors hash-valid. This is not full-paper or full-chapter verification of every experiment.'}
 ],
 'requiredOpenFindings':[],
 'meaningAssessment':'Preserves the progression from adaptive mobilization and endocrine feedback through distinct organs, development, immunity, pain/memory/sleep/aging, control and prediction, depression, personality/reward/addiction, rank and inequality, and conditional coping. Retains experimental setups, comparisons, mechanisms and alternative explanations, including opposite receptor-adaptation hypotheses, cell redistribution versus suppression, cancer endpoints and replication limits, selection in executive monkeys, nonlinear averaging versus relative inequality, public-resource pathways, and support withdrawal. No generic success/moral lesson replaces the author argument.',
 'omissions':'All18 main chapters are represented. The68 entries group retained examples; they are not an exhaustive list of every case in the original. Subsidiary experiments, quantitative detail, extensive notes, historical digressions and most primary research papers remain omitted or condensed as mapped. Neither maximum depth nor increased length means an unabridged replacement.',
 'qa':{'structuralChecks':69,'exactDraftDataEmbeddedParagraphParity':True,'allSixRouteExportsExact':True,'paragraphsPerLanguage':212,'defaultThemeFontRoutePositions':sum(r['count'] for p in ['320','1440'] for r in browsers[p]['routes']),'representativeLanguageThemeFontLayouts':sum(len(browsers[p]['layouts']) for p in ['320','1440']),'freshViewports':[[320,568],[1440,900]],'firstColdSerifPreserves100px':True,'settingsRadioArrowsCannotPage':True,'actualRenderedFontsChecked':True,'fourExplicitNonfictionDeeperResumePaths':True,'actualReloadPreservesLanguageDepthIdAndGlobalPreferences':True,'actualLegacyIds':['workplace-check','ses-gradient'],'invalidCurrentIdSafelyOffersStart':True,'noRuntimeErrorsOrRemoteRuntimeRequests':True,'ownedChromeCleanup':True,'physicalSafariPwaTested':False,'visualInspection':'Root inspected actual320px EN/dark/Sans immune-mechanism and RU/light/Serif depression-qualification screenshots, intentionally scrolled to the final lines.','harnessCorrection':'First layout attempt failed in the QA harness because a JavaScript id was not interpolated. Those failed records are retained; the harness was corrected and all final checks rerun. No app change was required.'},
 'limitations':['Root read the entire resulting bilingual condensation, not the entire primary book continuously.','Writer whole-main-body source ledger verified for interval/hash integrity; no all-notes or underlying-paper certification.','Animal-to-human extrapolation and historical hypotheses remain qualified. Five modern qualifications do not make this a current clinical review.','English is an original parallel condensation, not a certified published translation.','Chrome offline/file and viewport checks; no physical iPhone/Safari/PWA certification.']
}
dump(R/'personal-review.json',report)
(R/'personal-review.md').write_text('''# Why Zebras Don’t Get Ulcers — personal root acceptance

PASS after five paired-screen repairs and29 grouped-case locator corrections. Acceptance applies only to the exact final hashes in `personal-review.json`.

I completely read all107 original RU/EN screen pairs, including cover and final, then reread all five final changed pairs. I reread all37 Essential pairs in route order. For Core I reread every one of its33 added pairs completely in both languages with the preceding final sentence and following opening sentence; the shared Essential prose was already reread in order. This does not claim a third full rereading of identical shared prose. All six exported routes match the final JSON and HTML exactly.

I read the full18-chapter/68-grouped-case map, its omissions and Sources. I directly checked45 bounded primary passages and six narrow official/primary online sections. These include the actual receptor-adaptation alternatives, maternal-contact comparisons, immune redistribution, cancer endpoint and replication distinctions, Brady selection, candidate-gene recovery hypothesis, addiction relapse, inequality alternatives, and coping conditions. I did not continuously read the whole primary book or collate a published English edition.

The explanation retains experimental setups and the reasoning joining them. Repairs restore one missing historical proposed mechanism, remove an editorial instruction, and resolve three references whose context was absent in Essential. Twenty-nine source entry/context locators were replaced after actual primary reading; all78 final anchors are hash-valid. The68 entries group retained examples, rather than certify every original study.

Final routes37/70/107. Deep contains13219RU/13988EN body words including the shared final, excluding cover/headings/UI/Sources. That is73.44/63.58minutes at180/220wpm; the UI includes headings/framing and displays77/67minutes. Quantity is recorded, not used as a substitute for meaning.

The writer records both prefaces and all18 main chapter bodies of the owned Russian Piter2021 edition, based on the third-English-edition framework. I verified source interval/hash integrity separately from my selected primary reads. Most notes and underlying research papers remain outside that reading. Five narrow modern qualifications do not constitute a systematic scientific update; the Border2019 check is abstract-only.

Fresh root QA passed69 structural checks,856 route positions and80 representative language/theme/font layouts. First genuinely cold Serif loading retained100px scroll. Settings, actual reload/preferences, four explicit deeper-resume paths, two authentic legacy IDs, invalid-ID fallback, navigation, focus and actual rendered fonts passed. Root inspected actual mobile screenshots. Zero runtime errors or remote runtime requests; owned Chrome groups/profiles removed. Physical Safari/PWA remains untested.

Publication is allowed for this exact candidate. Other unaccepted book content remains held.
''')
current='Current root acceptance '+stamp+': PASS for the exact version in root-review/personal-review.json. Routes37/70/107; Deep13219RU/13988EN body words; UI77/67minutes. Earlier worker-phase counts, hashes and checks below are historical. Root read the complete bilingual retelling and selected actual primary passages, not the whole primary book continuously.'
for n in ['QA.md','sources.md','HANDOFF.md']:
    if not (R/('input-'+n)).exists(): (R/('input-'+n)).write_bytes((H/n).read_bytes())
    (H/n).write_text(current+'\n\n---\n\n'+(H/n).read_text())
coverage=load(H/'coverage-map.json');coverage.update(rootPersonalAcceptance=True,publicationAllowed=True,rootPersonalReview='root-review/personal-review.json',rootAcceptanceScope='Exact current candidate; source full-body reading belongs to the implementation ledger, root primary reading selective.')
coverage['meaningfulLimits']=[x.replace("or root's editorial acceptance", "or blanket scientific validation") for x in coverage['meaningfulLimits']]
dump(H/'coverage-map.json',coverage)
text=(H/'coverage-map.md').read_text().replace('Root personal acceptance: pending. Publication: prohibited for this candidate.','Root personal acceptance: recorded for this exact candidate in root-review/personal-review.json. Source whole-body reading below belongs to the writer ledger; root direct primary checking was selective.').replace("or root's editorial acceptance",'or blanket scientific validation')
(H/'coverage-map.md').write_text(text)
ready=load(R/'input-ready.json')
ready.update(status='root-personally-accepted',rootPersonalAcceptance=True,publicationAllowed=True,rootAcceptedAtUtc=stamp,rootPersonalReviewRecord=str(R/'personal-review.json'),rootPersonalReviewSha256=sha(R/'personal-review.json'),rootReadingLedger=str(R/'reading-ledger.json'),inputReadySha256=sha(R/'input-ready.json'),modes=m['modes'],density=m['density'])
ready['historicalWorkerQa']=ready.pop('qa');ready['rootQa']=report['qa']
ready['rootReviewRequiredHistorical']=ready.pop('rootReviewRequired')
ready['rootReviewRequired']=[]
ready['remainingRequiredWork']=['Integrate only this exact accepted HTML and catalogue count/times.','Check exact PR head and production changed assets.']
ready['contentHashes']={n:sha(H/n) for n in ready['contentHashes']}
paths=sorted(p for p in H.rglob('*') if p.is_file() and p.name!='ready.json' and '__pycache__' not in p.parts)
ready['files']={str(p.relative_to(H)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in paths}
ready['allArtifactHashes']={str(p.relative_to(H)):{'path':str(p),'sha256':sha(p)} for p in paths}
dump(H/'ready.json',ready)
for name,r in ready['allArtifactHashes'].items():assert sha(Path(r['path']))==r['sha256'],name
print(json.dumps({'accepted':True,'counts':d['targetModes'],'bindings':len(paths),'hashes':report['exactContentHashes'],'rootReviewSha256':sha(R/'personal-review.json')}))

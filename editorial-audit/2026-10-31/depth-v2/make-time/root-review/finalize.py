from pathlib import Path
import datetime,hashlib,json

H=Path(__file__).resolve().parent.parent;R=H/'root-review'
load=lambda p:json.loads(p.read_text())
dump=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert not (R/'personal-review.json').exists(),'Acceptance is a frozen exact-version record.'
l=load(R/'reading-ledger.json');d=load(H/'story-data.json');m=load(R/'qa/metrics.json')
assert len(l['deepReadPairIds'])==68 and len(l['essentialReadPairIds'])==24 and len(l['coreAddedPairsReread'])==24
assert set(l['finalChangedPairIdsReread'])==set(l['repairsImplementedPairIds']) and len(l['finalChangedPairIdsReread'])==14
assert l['allCurrentPairsRead'] and l['sourcesRead'] and l['coverageMapRead']
assert len(l['pendingFindings'])==7 and all(f['status']=='repaired-and-personally-reread' for f in l['pendingFindings'])
for name,digest in m['currentContentHashes'].items():assert sha(H/name)==digest,name
assert l['currentFinalStoryDataSha256']==sha(H/'story-data.json')
audit=load(R/'qa/structural-audit.json');assert audit['passes']==69 and not audit['warnings'] and not audit['failures']
parity=load(R/'qa/parity-check.json');assert parity['allAuthoredFieldsMatchEmbedding'] and parity['allSixRoutesExact']
assert all(v['exactInOrder'] and v['draftBodyParagraphs']==132 for k,v in m['parity'].items() if k in ['ru','en'])
primary=load(R/'qa/primary-integrity.json')
assert primary['rootActualRangesHashValid']==28 and primary['allSuggestedIntervalsCovered']==26
assert primary['workerReadingLedgerByteIdentical'] and primary['protectedInputsUnchanged']==124
for row in load(R/'protected-baseline.json')['files']:assert sha(Path(row['path']))==row['sha256'],row['path']
browsers={phase:load(R/f'qa/browser-{phase}.json') for phase in ['320','1440','cold','resume']}
for phase,b in browsers.items():
 assert b['status']=='completed' and not b['runtimeErrors'] and not b['remoteRequests']
 assert b['profileRemoved'] and b['processGroupTerminated'] and not b['ownedProcessRemainders']
 for name,digest in b['inputHashes'].items():assert sha(H/name)==digest,(phase,name)
assert browsers['cold']['coldBefore']['scroll']==browsers['cold']['coldAfter']['scroll']==100
assert all(x=='unloaded' for x in browsers['cold']['coldBefore']['serifStatus'])
assert browsers['cold']['radioArrowKeepsId']
assert all(browsers['resume']['reload'].values()) and browsers['resume']['invalidCurrentId']
assert len(browsers['resume']['deeperResume'])==4
assert all(all(v for k,v in row.items() if k not in ['l','lower']) for row in browsers['resume']['deeperResume'])
for phase in ['320','1440']:
 assert len(browsers[phase]['routes'])==6 and len(browsers[phase]['layouts'])==40
 assert not any(row['bad'] for row in browsers[phase]['routes'])
visuals=['qa/320-wooden-railway-en-dark-sans.png','qa/320-brief-workout-ru-light-serif.png']
l.update(status='root-personal-reading-complete-and-accepted',rootPersonalAcceptance=True,publicationAllowed=True,atUtc=stamp,visualScreenshotsPersonallyInspected=[{'file':n,'sha256':sha(R/n)} for n in visuals],publicationScope='Only the exact expanded Make Time version recorded in personal-review.json. Other unaccepted book content remains held.')
l['shorterRouteReviewPlan']='Completed: all24Essential pairs and all24Core additions with both adjacent edges; final14changed pairs reread.'
dump(R/'reading-ledger.json',l)
names=['story-data.json','make-time.html','draft-ru.md','draft-en.md']
exact={name:sha(H/name) for name in names}
qa={'structuralChecks':69,'allAuthoredFieldsMatchEmbedding':True,'exactDraftPairedParagraphs':132,'sharedFinalAdditionalParagraphPair':1,'allSixRoutesExact':True,'freshRoutePositions':sum(row['count'] for phase in ['320','1440'] for row in browsers[phase]['routes']),'representativeLanguageThemeFontLayouts':80,'viewports':[[320,568],[1440,900]],'actualColdFontViewport':[320,568],'genuinelyUnloadedFirstSerifPreserves100px':True,'settingsRadioArrowsCannotPage':True,'fourExplicitNonfictionDeeperResumePaths':True,'actualReloadPreservesDepthIdLanguageAndGlobalPreferences':True,'authenticLegacyIds':['life-pivot','caffeine-cutoff'],'invalidCurrentIdSafelyOffersStart':True,'actualRenderedCustomFontsChecked':True,'navigationFocusSourcesContentsPointerPassed':True,'runtimeErrors':[],'remoteRuntimeRequests':[],'ownedChromeCleanup':True,'physicalSafariPwaTested':False,'screenshotsPersonallyInspected':l['visualScreenshotsPersonallyInspected']}
assert qa['freshRoutePositions']==560
report={'schemaVersion':1,'slug':'make-time','atUtc':stamp,'verdict':'PASS-after-root-repair','rootPersonalAcceptance':True,'publicationAllowed':True,'contentMode':'explanatory','counts':d['targetModes'],'metrics':m['modes'],'exactContentHashes':exact,'readingLedgerSha256':sha(R/'reading-ledger.json'),'inputReadySha256':sha(R/'input-ready.json'),
 'personalReading':{'all68OriginalRuEnPairsCompletelyRead':True,'all14FinalChangedPairsReread':True,'coverAndFinalRead':True,'all24EssentialPairsReread':True,'all24CoreAdditionsRereadCompletelyWithBothAdjacentEdges':True,'routeReadingMethod':l['shorterRouteReadingMethod'],'complete326LineChapterTacticOmissionMapRead':True,'all87MappedContributionsRead':True,'sourcesAndImplementationRead':True,'selectedActualPrimaryRanges':l['primaryRangesActuallyRead'],'all26SuggestedPrimaryIntervalsCovered':True,'rootWholePrimaryContinuouslyRead':False},
 'sourceScope':{'edition':'Owner-supplied RU extraction, A.Kapanadze translation, ISBN9785961420517. Publishing sheet has RU/electronic2019 and bibliography2018; discrepancy disclosed, not resolved by invention. Original2018.','sourceSha256':primary['sourceFileSha256'],'writer':'Records continuous complete extracted main text, all87 tactic narratives,49notes and remaining nonempty front/backmatter. All34nonempty records have complete interval/hash coverage; this verifies ledger integrity, not a new root whole-source reading claim.','root':'28 actual bounded primary reads cover all26 suggested selections. Includes full relevant records for control/list design, daily stages, calendar, email, involvement/rest, energy rationale, nutrition, caffeine, sleep/caregiving, reflection, actual closing pivots and quick start, plus selected other passages and the publishing sheet. Source reading is selective overall.','figures':'No original questionnaire, day-calendar or12movement-sequence image inspected; no missing geometry, utterance or exercise list guessed.','english':'Original EN rendering of this condensation, not published-English collation.','science':'Underlying studies were not independently appraised; historical health arguments and personal experiments remain attributed. No systematic modern clinical/efficacy certification or new medical advice.'},
 'findingsClosed':l['pendingFindings'],'requiredOpenFindings':[],
 'meaningAssessment':'Preserves the Busy Bandwagon/Infinity Pools/defaults problem and the recurring Highlight–Laser–Energize–Reflect mechanism. The intermediate scale, three selection criteria, actual alternative list designs, calendar constraints, author-specific mornings/evenings, product attraction, friction, real costs of leaving a network, email exceptions and time zones, initiating/sustaining work, bodily conditions, author disagreements and actual reflection feedback remain developed. All87 tactics contribute a retained mechanism, procedure, actual case or qualification; they are not87generic slogans. The actual seven-year writing transition, sailing pivot and three-day quick start close the argument without promising an identical life result.',
 'repairs':'Seven findings affect14paired screens plus four tactic-map extents and one supporting source-context addition. Removes intrusive producer/extraction asides, restores actual short-workout rationale/JZ set structure and fasting adaptation, clarifies Flynn’s actual action, author/partner first uses and sailing, resolves the omitted sprint-lab context in shorter routes. Actual research/figure/translation limits remain disclosed.',
 'omissions':'No whole numbered tactic omitted, but the87-entry map is not a reproduction of every instruction or example. Epigraphs, repeated encouragement, usage figures, Packers genealogy, chronometer history, music inventory, much dated product advice, broad disease/longevity promises, numerical study effects, reading catalogue and acknowledgments are compressed or omitted. Original figures and the complete12movement illustration remain unavailable. Main-body and noncover-body word definitions are separate; more words/screens do not independently establish fidelity.',
 'qa':qa,'primaryIntegrity':primary,'protectedFilesUnchanged':124,
 'limitations':['Root completely read the resulting bilingual retelling, with selected actual primary checking; not a continuous whole-primary or published-English read.','Implementation main-text/notes reading is the writer claim with interval/hash integrity; not independent verification of underlying studies.','Original source illustrations and exact questionnaire/calendars were not inspected.','Reader is an original condensed explanation, not an unabridged replacement or an authorized published translation.','Chrome file/offline and viewport checks; physical iPhone/Safari/PWA untested.']}
dump(R/'personal-review.json',report)
(R/'personal-review.md').write_text('''# Make Time — personal root acceptance

PASS after seven findings were closed. Acceptance applies only to the final hashes in personal-review.json.

I completely read all68original RU/EN pairs, including cover/final, then personally reread all14final changed pairs. I reread all24Essential pairs in route order, with edited entries reread after repair. For Core I reread every24added pair completely with both adjacent route edges; common Essential prose was already reread. This does not claim a third complete rereading of identical shared prose. All six final route exports match JSON/HTML exactly.

I read the complete326line chapter/tactic/omission map, all87retained contributions, Sources and implementation account. I directly read28bounded primary selections covering all26suggested intervals, and verified their exact paragraph hashes. The writer’s complete34nonempty-record extraction ledger has interval/hash integrity. This does not turn writer full-source reading into root continuous whole-primary reading. No published-English collation, original-image inspection or underlying-paper appraisal is claimed.

The argument and actual author cases survive. Repairs remove intrusive instructions to the producer and missing-extraction discussion from ordinary reading, restore comparative short-workout reasoning and actual JZ set structure, restore his fasting adaptation, clarify author/partner names and sailing, restore infant Flynn’s concrete action, and introduce the omitted design-sprint context for shorter routes. A generator had mistaken internal steps4–6 for global tactic headings: the actual source was read completely, starts corrected and four resulting extents repaired. A source context was added for the sprint definition.

Final routes24/48/68. Deep has9942RU/11095EN authored body words, or9969RU/11120EN including the shared final. Cover/headings/UI/Sources are excluded from both body measures. Noncover body time is55.38/50.55minutes at180/220wpm; actual reader estimates including framing are58/53minutes. UI Essential20/18, Core41/37. Quantity is reported separately from fidelity.

Fresh root QA passed69structural checks,560route positions and80representative language/theme/font layouts. Genuinely first unloaded Serif selection preserved100px scroll at320×568. Settings arrows/focus/Tab/Escape, explicit deeper Continue, actual reload/preferences, authentic legacy isolation, invalid-ID fallback, navigation, focus/pointer, Sources/Contents and actual rendered fonts passed. Root inspected both actual320px screenshots through their last lines. No runtime errors or remote runtime requests; owned Chrome groups/profiles removed. Physical Safari/PWA untested.

All87tactics have retained substance, but subsidiary examples, instructions, statistics, broad health promises and original visual material are condensed or omitted as mapped. Health propositions remain historical attributed book arguments, not independently certified clinical guidance. Publication is allowed for this exact Make Time candidate only. Other unaccepted content remains held.
''')
current=f'Current root acceptance {stamp}: PASS for the exact version in root-review/personal-review.json. Routes24/48/68; Deep9969RU/11120EN noncover-body words including shared final; UI58/53minutes. Earlier worker-phase metrics, hashes and pending statuses below are historical. Root read the complete bilingual retelling and selected actual primary passages, not the whole primary continuously. Missing source-image detail is disclosed here/in method notes rather than inserted into ordinary reading.'
for name in ['sources.md','QA.md','implementation.md','coverage-map.md']:
 assert (R/('input-'+name)).is_file()
 (H/name).write_text(current+'\n\n---\n\n'+(H/name).read_text())
handoff=load(R/'input-editorial-handoff.json')
handoff['historicalWriterRootMustRead']=handoff.pop('rootMustRead')
handoff['historicalWriterContentHashes']=handoff.pop('contentHashes')
handoff['historicalWriterProofFiles']=handoff.pop('currentProofFiles')
handoff['contentHashes']=exact
handoff['currentProofFiles']=['root-review/personal-review.json','root-review/qa/metrics.json','root-review/qa/parity-check.json','root-review/qa/primary-integrity.json','root-review/qa/structural-audit.json','root-review/qa/browser-320.json','root-review/qa/browser-1440.json','root-review/qa/browser-cold.json','root-review/qa/browser-resume.json']
handoff.update(status='root-personally-accepted',rootPersonalAcceptance=True,publicationAllowed=True,rootPersonalReview='root-review/personal-review.json',remainingRequiredWork=['Exact accepted runtime integration, exact PR head and production asset verification.'])
dump(H/'editorial-handoff.json',handoff)
ready=load(R/'input-ready.json')
ready['historicalWorkerMetrics']=ready['metrics']
ready['metrics']=str(R/'qa/metrics.json')
ready.update(status='root-personally-accepted',rootPersonalAcceptance=True,publicationAllowed=True,bookContentPublicationAllowed=True,rootAcceptedAtUtc=stamp,rootPersonalReviewRecord=str(R/'personal-review.json'),rootPersonalReviewSha256=sha(R/'personal-review.json'),rootReadingLedger=str(R/'reading-ledger.json'),inputReadySha256=sha(R/'input-ready.json'),counts=d['targetModes'],mainBodyWords={mode:{lang:values[lang]['mainBodyWords'] for lang in ['ru','en']} for mode,values in m['modes'].items()},noncoverBodyWords={mode:{lang:values[lang]['noncoverBodyWords'] for lang in ['ru','en']} for mode,values in m['modes'].items()},uiMinutes={mode:{lang:values[lang]['uiMinutes'] for lang in ['ru','en']} for mode,values in m['modes'].items()},readingMetrics=m['modes'],rootQa=qa,rootReviewRequired=[])
ready['historicalWorkerQa']={k:ready.pop(k) for k in ['standardBrowserRenderedVisits','emulatedIPhoneAdditionalVisits']}
ready['remainingRequiredWork']=['Integrate only this exact accepted HTML and catalogue count/times.','Check exact PR head and production changed assets.']
ready['exactContentHashes']=exact
paths=sorted(p for p in H.rglob('*') if p.is_file() and p.name!='ready.json' and '__pycache__' not in p.parts)
ready['files']={str(p.relative_to(H)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in paths}
ready['allArtifactHashes']={str(p.relative_to(H)):{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in paths}
dump(H/'ready.json',ready)
for name,row in ready['allArtifactHashes'].items():assert sha(Path(row['path']))==row['sha256'],name
assert all(sha(H/name)==digest for name,digest in exact.items())
print(json.dumps({'accepted':True,'counts':d['targetModes'],'bindings':len(paths),'exactContentHashes':exact,'rootReviewSha256':ready['rootPersonalReviewSha256']}))

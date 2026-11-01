from pathlib import Path
import json, hashlib, datetime

H = Path(__file__).resolve().parent.parent
R = H / 'root-review'
load = lambda p: json.loads(p.read_text())
dump = lambda p,d: p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
assert not (R/'personal-review.json').exists(), 'Final acceptance is a frozen record; do not overwrite.'
data=load(H/'story-data.json'); metrics=load(R/'qa/metrics.json')
ledger=load(R/'reading-ledger.json'); parity=load(R/'qa/parity.json')
assert ledger['allCurrentPairsRead'] and ledger['lastAdditionalTelegramEditReread']
assert parity['storyDataSha256']==sha(H/'story-data.json') and parity['htmlSha256']==sha(H/'children-of-captain-grant.html')
assert not parity['protectedChanges']
aud=load(R/'qa/structural-audit.json'); assert aud['passes']==69 and not aud['failures'] and not aud['warnings']
browsers={p:load(R/f'qa/browser-{p}.json') for p in ['cold','consent','320','1440']}
for p,b in browsers.items():
    assert b['status']=='completed' and not b['runtimeErrors'] and not b['remoteRequests']
    assert b['profileRemoved'] and b['processGroupTerminated']
    assert b['inputHashes']['children-of-captain-grant.html']==sha(H/'children-of-captain-grant.html')
prefix=load(R/'qa/shorter-prefix-proof.json'); assert all(x['exactPrefixOfDeep'] for x in prefix.values())
ledger.update(status='root-personal-reading-complete-and-accepted',rootPersonalAcceptance=True,publicationAllowed=True,atUtc=stamp)
ledger['publicationScope']='Only the exact content hashes in personal-review.json; not other books or earlier versions.'
dump(R/'reading-ledger.json',ledger)
report={
 'schemaVersion':1,'slug':data['slug'],'atUtc':stamp,'verdict':'PASS-after-root-repair',
 'rootPersonalAcceptance':True,'publicationAllowed':True,
 'publicationScope':'Only this exact candidate; no acceptance of other books.',
 'contentMode':'narrative','counts':data['targetModes'],'metrics':metrics['depths'],
 'exactContentHashes':{n:sha(H/n) for n in ['children-of-captain-grant.html','story-data.json','draft-ru.md','draft-en.md']},
 'readingLedgerSha256':sha(R/'reading-ledger.json'),'inputReadySha256':sha(R/'input-ready.json'),
 'personalReading':{
   'originalPairs':116,'currentPairs':116,'originalCompleteRuEnRead':True,
   'allFinalChangedPairsReread':True,'allCoverWarningFinalCopyRead':True,
   'shorterRouteReadingMethod':ledger['shorterRouteReadingMethod'],
   'essentialContinuousPrefixParagraphs':24,'coreContinuousPrefixParagraphs':67,
   'exactShorterPrefixesVerified':True,'sourcesAndWholeChapterMapRead':True,
   'complete66ChapterEditionOmissionMapRead':True,'wholePrimaryContinuouslyReadByRoot':False,
   'selectedPrimaryLineRanges':ledger['primaryRangesActuallyRead'],'selectedFrenchPrimaryRead':ledger['webPrimaryRead']
 },
 'primaryWitness':{
   'path':'/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-1-private/children-of-captain-grant/primary.txt',
   'sha256':'df5da6648b41f3e2498e6b048a8aa051932d73b70a9d76596177e5a9eec3e8c1',
   'edition':'Historical Horne-edited English Gutenberg2083, 66 chapters (26/19/21), not the 70-chapter French original.',
   'implementationFullReading':'Implementation ledger records all34 bounded chunks of this witness. This remains a writer reading claim, separately hashed; root directly checked selected English passages, including all six final chapters, and one selected French chapter.'
 },
 'findingsClosed':[
   {'id':'GR-R01','screen':'wolves','issue':'The phrase red wolves of the novel interrupted action with an editorial aside.','resolution':'Kept aguara/red-wolf wording as narrative description; removed only the metanarrative qualifier in RU/EN. Primary I.XIX checked.'},
   {'id':'GR-R02','screen':'telegram','issue':'A second metanarrative aside about nardoo and a redundant evidence reminder interrupted the exhausted journey.','resolution':'Confirmed actual preparation in II.XIX, then narrated the coarse flour and bread without a recipe. Glenarvan explicitly believes the yacht captured; removed the additional analytical reminder. Final paired paragraph reread.'},
   {'id':'GR-R03','screen':'father','issue':'Solitude was substituted for reflection in the hope attributed to Grant.','resolution':'Restored reflection and repentance from III.XX L19146–19152; removed the redundant future-verification aside. The hope remains the captain’s own.'},
   {'id':'GR-R04','screen':'arabella','issue':'The person speaking privately with Arabella before the wedding was left unclear.','resolution':'Named the major as the speaker, matching III.XXI. Both final language paragraphs reread.'}
 ],
 'requiredOpenFindings':[],
 'meaningAssessment':'The search develops through the three damaged messages, the missing longitude, successive interpretations and three distinct journeys. The Andes, Robert’s disappearance and rescue, Thalcave and the wolves, the flood and ombu, the storm and Duncan’s bar passage, the farm/Ayrton trust, Australian warning clues and failed overland journey, the New Zealand shipwreck/captivity/taboo escape, the actual written order and Ayrton’s bargain, the children’s night recognition and the island reunion remain causal action. Mary/John and Helena/Glenarvan relationships, Paganel’s comic errors, Robert’s agency and the major’s suspicion are carried by scenes. No invented modern management lesson is appended. Grant’s colonial ambition and the author’s historical narrative frame are not silently replaced by a modern moral.',
 'omissions':'The complete66-chapter retention/omission map is retained. Numerous geographical, botanical, zoological, historical and ethnographic digressions, repeated travel description and incidental dialogue are condensed. Every mapped chapter contributing to this chosen English witness is represented, but this is an original condensation, not an unabridged text or a full French collation. Essential/Core are deliberately unfinished continuous openings, explicitly labelled on cover/final; only Deep includes the resolution and coda.',
 'qa':{
   'structuralChecks':69,'exactDraftDataEmbeddedParity':True,
   'allDefaultFontThemeRoutePositionsAt320And1440':sum(x['count'] for p in ['320','1440'] for x in browsers[p]['routes']),
   'representativeLanguageThemeFontLayouts':sum(len(browsers[p]['layouts']) for p in ['320','1440']),
   'coldFirstSerifNonzeroScrollPreserved':browsers['cold']['coldBefore']['scroll']==100 and browsers['cold']['coldAfter']['scroll']==100,
   'serifActuallyUnloadedBeforeFirstSelection':all(x=='unloaded' for x in browsers['cold']['coldBefore']['serifStatus']),
   'realDowngradePaths':len(browsers['consent']['downgrades']),
   'reloadPaths':len(browsers['consent']['reloads']),
   'simulatedBfcacheAndFinalEntry':True,'actualLegacyId':'paganel-secret',
   'noRuntimeErrorsOrExternalRequests':True,'ownedChromeCleanup':True,
   'hardwareSafariPwaTested':False,'freshQaViewports':[[320,568],[1440,900]],
   'visualInspection':'Root inspected the actual320px English dark Sans action screen and Russian light Serif late action screen. Screens were intentionally captured at the bottom to check the last lines and Next controls.'
 },
 'limitations':[
   'Original condensation of the named Horne-edited66-chapter English witness, not an unabridged edition or a published Russian translation.',
   'Root primary checking was selective. One French chapter was checked directly; no full French70-chapter or modern Russian translation collation.',
   'Historical and fictional flora, fauna and cultural descriptions are not certified as modern scientific or historical claims.',
   'Chrome file/offline and viewport emulation, not physical Safari/PWA or native-touch certification.'
 ]
}
dump(R/'personal-review.json',report)
md='''# Children of Captain Grant — personal root acceptance

PASS after four paired paragraph repairs. Acceptance applies only to the final hashes in `personal-review.json`.

I read all116 original RU/EN screen pairs, including cover, warning and final, then reread every changed pair. I read the complete113-scene map,66-chapter edition/omission map and Sources. Essential and Core contain exact continuous24/67-paragraph prefixes of the story already read in sequence; I verified those prefixes and reread the cut boundaries/shared framing. This does not claim a separate second reading of every identical Core paragraph.

The complete search and three journeys remain an adventure: the damaged messages and changing interpretations, Robert/Thalcave, the storm, Australian trust and suspicion, the captivity and escape, Ayrton’s bargain, the written order, the children’s night recognition and the actual reunion/coda. The text retains humor and relationships through scenes. It contains no substituted management or moral lesson.

Root repairs remove two intrusive editorial asides, restore Grant’s actual hope in reflection/repentance, and identify the major as the person who speaks with Arabella before the wedding. All final paired paragraphs were reread. Key checks used the actual private primary witness, including all six final English chapters; exact earlier ranges and the selected French I.II check are recorded in the ledger. Root did not continuously read the whole primary novel.

Final routes26/69/116. Deep has12410RU/14921EN narrative-body words. Narrative-only estimates are68.94/67.82minutes at180/220wpm; the UI includes titles/framing and displays72/71minutes. Essential/Core are explicitly unfinished portions, not complete alternative plot summaries.

The source is the historical Horne-edited66-chapter English version, not the70-chapter French original. Geographical/history/natural-history digressions and incidental dialogue are condensed as mapped. No full French or published Russian-translation fidelity is claimed.

Fresh exact-hash root QA passed69 structural checks,844 route positions,80 representative language/theme/font layouts, four genuine downgrade paths, three reload paths, simulated BFCache/final entry and actual legacy-state isolation. First Serif loading was genuinely cold and preserved100px scroll. Root inspected actual mobile screenshots. No runtime errors/external runtime requests; all owned Chrome groups/profiles removed. Physical Safari/PWA remains untested.

Publication is allowed for this exact candidate only. All other unaccepted content remains held.
'''
(R/'personal-review.md').write_text(md)
addition='\n\n## Root acceptance — '+stamp+'\n\nThe worker-phase counts, hashes and browser reports above are historical. Root personally read all RU/EN copy and the full maps, repaired four paired paragraphs and accepted only the exact final hashes in root-review/personal-review.json. Final narrative words12410RU/14921EN; counts26/69/116. Fresh root QA:69 structural checks,844 route positions,80 layouts, real downgrade/reload/legacy/cold-Serif checks; zero runtime errors or external requests. Chrome emulation only. Root selected primary passages, not continuous whole-novel reading.\n'
for n in ['QA.md','sources.md']:
    (H/n).write_text((H/n).read_text()+addition)
ready=load(R/'input-ready.json')
ready.update(status='root-personally-accepted',rootPersonalAcceptance=True,publicationAllowed=True,rootAcceptedAtUtc=stamp,
             counts=data['targetModes'],modes=load(H/'metrics.json')['modes'],parts=load(H/'metrics.json')['parts'],
             rootPersonalReview=str(R/'personal-review.json'),rootPersonalReviewSha256=sha(R/'personal-review.json'),
             rootReadingLedger=str(R/'reading-ledger.json'),inputReadySha256=sha(R/'input-ready.json'),
             remainingRequiredWork=['Integrate only this accepted HTML and catalogue count/times; preserve all other public content.','Exact-head checks/merge and changed-production-asset verification remain publisher-owned.'])
ready['authoring']['volumeRationale']='Developed three-part journey and named66-chapter retention/omission map; final12410RU narrative words after personal root repair, not a quota.'
ready['rootQa']=report['qa']
ready['historicalWorkerQa']=ready.pop('qa')
ready['exactCandidateHashes']={n:sha(H/n) for n in ready['exactCandidateHashes']}
paths=sorted(p for p in H.rglob('*') if p.is_file() and p.name!='ready.json' and '__pycache__' not in p.parts)
ready['files']={str(p.relative_to(H)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in paths}
ready['allArtifactHashes']={str(p.relative_to(H)):{'path':str(p),'sha256':sha(p)} for p in paths}
dump(H/'ready.json',ready)
for name,r in ready['allArtifactHashes'].items(): assert sha(Path(r['path']))==r['sha256'],name
print(json.dumps({'accepted':True,'counts':data['targetModes'],'bindings':len(paths),'hashes':report['exactContentHashes'],'rootReviewSha256':sha(R/'personal-review.json')},ensure_ascii=False))

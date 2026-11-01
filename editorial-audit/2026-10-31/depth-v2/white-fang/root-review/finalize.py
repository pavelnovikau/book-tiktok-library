from pathlib import Path
import json, hashlib, datetime
H = Path(__file__).resolve().parent.parent
R = H / 'root-review'
assert not (R / 'personal-review.json').exists(), 'Do not overwrite a completed personal review.'
load = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
d = load(H / 'story-data.json')
m = load(R / 'qa/metrics.json')
l = load(R / 'reading-ledger.json')
assert l['allCurrentPairsRead'] and l['allShorterRoutesReadInBothLanguages']
assert l['boundStoryDataSha256'] == sha(H / 'story-data.json')
for phase in ['320','1440','cold','consent']:
    q = load(R / f'qa/browser-{phase}.json')
    assert q['status'] == 'completed' and q['profileRemoved'] and q['processGroupTerminated']
    assert q['inputHashes']['white-fang.html'] == sha(H / 'white-fang.html')
    assert not q['runtimeErrors'] and not q['remoteRequests']
parity = load(R / 'qa/parity.json')
assert parity['storyDataSha256'] == sha(H / 'story-data.json')
assert parity['htmlSha256'] == sha(H / 'white-fang.html')
l.update(status='root-personally-accepted', rootPersonalAcceptance=True, publicationAllowed=True,
         finalHtmlSha256=sha(H / 'white-fang.html'), atUtc=stamp)
(R / 'reading-ledger.json').write_text(json.dumps(l, ensure_ascii=False, indent=2) + '\n')
findings = [
    {'id':'WF-R01','issue':'Woods and lynx fights were placed before the autumn move to Dawson; the two-dog fight was placed afterwards.', 'resolution':'Rewrote IV.3 as four connected paragraphs: Fort Yukon tests, autumn steamer and paid Dawson exhibit, night/daylight woods contests and lynx, spring arrival of Cherokee. Source IV.3 L4799-4975.'},
    {'id':'WF-R02','issue':'The son was credited with identifying Jim Hall.', 'resolution':'The judge identifies Hall after Weedon switches on the light and descends with him. Source V.5.'},
    {'id':'WF-R03','issue':'Russian generic words for a blow/beating obscured the distinction between Scott\'s cuff and earlier owners\' beatings.', 'resolution':'Restored light cuff in the family paragraph, and the narrower cuff verb in the chicken scene. Actual physical punishment remains; no claim of nonviolent animal training. Source V.3 L6725-6860.'},
    {'id':'WF-R04','issue':'Essential jumped from Bill\'s death to Henry\'s rescue, losing the causal experience of the siege.', 'resolution':'Promoted the coffin platform/camp, dream attack and fire-ring paragraphs together to Essential. No invented expansion.'},
    {'id':'WF-R05','issue':'The revised shared Cherokee paragraph initially referred back to a lynx omitted from shorter routes.', 'resolution':'Neutral shared opening now closes the sequence of contests without a dangling reference. Both shorter routes reread.'},
    {'id':'WF-R06','issue':'Fresh root consent QA found a Russian Continue label still naming Deep in English.', 'resolution':'Localized the one candidate-local label to the actual Russian depth name; fresh exact-hash QA then passed.'}
]
report = {'schemaVersion':1,'slug':'white-fang','atUtc':stamp,'verdict':'PASS-after-root-repair',
 'rootPersonalAcceptance':True,'publicationAllowed':True,'publicationScope':'Only this exact candidate; no acceptance of other books.',
 'contentMode':'narrative','counts':d['targetModes'],'metrics':m['depths'],
 'exactContentHashes':{n:sha(H / n) for n in ['white-fang.html','story-data.json','draft-ru.md','draft-en.md']},
 'readingLedgerSha256':sha(R / 'reading-ledger.json'),'inputReadySha256':sha(R / 'input-ready.json'),
 'personalReading':{'originalPairs':88,'currentPairs':89,'originalCompleteRuEnRead':True,'allFinalChangedPairsReread':True,'essentialCoreBothLanguagesReadInSequence':True,'deepFinalSequenceEstablishedByCompleteInputReadingAndFullChangedParagraphRecheck':True,'sourcesAndWholeChapterMapRead':True,'wholePrimaryContinuouslyReadByRoot':False,'selectedPrimaryLineRanges':l['primaryRangesActuallyRead']},
 'primaryWitness':{'path':'/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-1-private/white-fang/primary.txt','sha256':'3c7226d00fd9b169f0016635d0e461501620f343220ee18db7ca9f083f4ad3f4','implementationFullReading':'All five parts and25 chapters; separate implementation ledger. Root selected direct checking does not replace that attribution.'},
 'findingsClosed':findings,'requiredOpenFindings':[],
 'meaningAssessment':'The story advances through hunger, discovery, bodily danger, coercion, repeated returns, and slowly changing attachment. It retains the cub\'s perceptions and distinct human relationships. Rescue does not create instant trust: Major dies, Matt and Scott are bitten, and the meat/hand/absence/return sequence earns the later attachment. Southern restrictions, Scott\'s own punishment, Hall\'s wrongful last conviction and the judge\'s ignorance, nursing and troubled dreams precede the actual puppies-in-sun ending. No added moral lesson follows it.',
 'omissions':'Repeated theoretical exposition, physiognomic/racial generalizations, incidental speech, several similar skirmishes, some famine episodes, exact medical odds and biological-superiority rhetoric are compressed or omitted as mapped. Shorter routes intentionally stop before Cherokee\'s fight result; they are not full ending-bearing versions. The full selected arc is in Deep.',
 'qa':{'structuralChecks':69,'allDefaultFontThemeRoutePositionsAt320And1440':704,'representativeLanguageThemeFontLayouts':80,'coldFirstSerifNonzeroScrollPreserved':True,'realDowngradePaths':4,'reloadPaths':3,'simulatedBfcacheAndFinalEntry':True,'actualLegacyId':'quiet-last-image','noRuntimeErrorsOrExternalRequests':True,'ownedChromeCleanup':True,'hardwareSafariPwaTested':False},
 'limitations':['Original condensation, not the unabridged novel or a published Russian translation.','No print-variant or published-English translation collation.','Primary checking by root was selective, not continuous whole-novel reading.','Chrome file/offline and viewport emulation, not physical Safari/PWA.']}
(R / 'personal-review.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
text = '# White Fang: root personal acceptance\n\nPASS after direct reading and root repair. This accepts only the exact files below, not a screen quota or other books.\n\nRoot read all88 input RU/EN pairs, the complete source/method and chapter map, then all final changed paragraphs and both shorter cumulative routes in both languages. The final candidate has89 pairs and86 narrative paragraphs. Selected original English passages were read directly; root does not claim continuous whole-novel reading. The implementation agent\'s separate ledger covers all25 chapters.\n\n'
text += report['meaningAssessment'] + '\n\n'
text += '## Required repairs closed\n\n' + '\n'.join('- **'+f['id']+'**: '+f['resolution'] for f in findings) + '\n\n'
text += '## Scope and omissions\n\n' + report['omissions'] + '\n\n'
text += 'Counts are36 /51 /89. Deep contains8,173 RU and10,071 EN narrative words (45.41 /45.78 minutes at180 /220 words per minute). Reader estimates include headings and framing: RU19 /27 /48, EN20 /28 /48 minutes. These are consequences of the retained scenes, not acceptance targets.\n\n'
text += '69 structural checks, exact draft/data/HTML and metadata parity,704 route positions and80 representative layouts passed. Cold first Serif selection retained a nonzero100px scroll; Settings arrows did not advance the story. Four actual downgrades, three saved-mode reloads, native cancel/accept, simulated BFCache lifecycle and final entry retained the fresh-consent rule. The old quiet-last-image state stayed isolated. No runtime errors or remote requests; owned profiles/process groups removed. No physical Safari/PWA test.\n\n'
text += '## Exact accepted content\n\n' + '\n'.join('- `'+n+'`: `'+v+'`' for n,v in report['exactContentHashes'].items()) + '\n\nThe JSON report and reading ledger retain precise evidence boundaries. Older implementation QA and input-ready are historical records, not claims about these revised hashes. No publication has occurred at acceptance.\n'
(R / 'personal-review.md').write_text(text)
p = H / 'sources.md';s = p.read_text().replace('All 85 narrative units','All 86 narrative units')
s = s.replace("Status: ready for root's personal reading, subject to QA and the exact hashes in ready.json. No publication approval.", "Implementation source ledger, followed by root acceptance below; exact current bindings are in ready.json.")
s = s.replace('Root has not yet personally accepted these hashes.', 'Root acceptance of the revised hashes is recorded in root-review/personal-review.json; the initial input remains archived.')
s += '\n\n## Root acceptance, 2026-11-01\n\nRoot read the complete original bilingual retelling, the final repaired paragraphs, both shorter cumulative routes and selected actual primary passages. This is distinct from the implementation agent\'s continuous full-primary reading. IV.3 chronology, the Hall-identification actor, the scale of Scott\'s cuff, Essential\'s fire siege and shared route wording were repaired. Exact hashes, omissions and testing boundaries are in root-review/personal-review.json. This is an original condensation, not full-edition/translation certification.\n'
p.write_text(s)
p = H / 'QA.md';p.write_text('# Current root QA, 2026-11-01\n\nThe current36/51/89 candidate is personally accepted by root. Fresh exact-hash results are in root-review/qa and personal-review.json:69 structural checks,704 route positions,80 representative layouts, cold Serif nonzero scroll and fresh downgrade/reload consent all pass. The initially unlocalized Continue label and its failed test are retained separately; final tests pass. Runtime requests/errors are zero, owned Chrome cleanup passes; physical Safari/PWA is untested.\n\nThe implementation record below describes the earlier32/50/88 input and is preserved as history. It is not a fresh certification of the repaired hashes.\n\n'+p.read_text())
ready = load(R / 'input-ready.json')
ready.update(status='root-personally-accepted', rootPersonalAcceptance=True, publicationAllowed=True, bookContentPublicationAllowed=True, rootReviewRequired=False, rootAcceptedAtUtc=stamp, rootPersonalReview=str(R/'personal-review.json'),rootPersonalReviewSha256=sha(R/'personal-review.json'), counts=d['targetModes'],narrativeParagraphPairs=86,metrics=load(H/'metrics.json'),remaining=['Release integration, CI/PR readiness and production exact-hash verification.'])
ready['rootRequiredReadScope']={k:True for k in ready['rootRequiredReadScope']}
ready['qa']={'implementationHistory':load(R/'input-ready.json')['qa'],'rootCurrent':report['qa']}
for record in ready['deliverables'].values():
    p=Path(record['path']);record.update(sha256=sha(p),bytes=p.stat().st_size)
for pair in ready['routeFiles'].values():
    for record in pair.values():
        p=Path(record['path']);record.update(sha256=sha(p),bytes=p.stat().st_size)
ready['allArtifactHashes']={str(p.relative_to(H)):{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(H.rglob('*')) if p.is_file() and p != H/'ready.json' and '__pycache__' not in p.parts}
(H/'ready.json').write_text(json.dumps(ready,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'accepted':report['exactContentHashes'],'counts':ready['counts'],'reportSha256':sha(R/'personal-review.json'),'artifactBindings':len(ready['allArtifactHashes'])}))

from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda n:json.loads((HERE/n).read_text())
metrics=read('metrics.json');build=read('build-record.json');ledger=read('witness-reading-ledger.json')
html_hash=sha(HERE/'children-of-captain-grant.html');data_hash=sha(HERE/'story-data.json')
phases=['320','390','1024','1440','consent','ios'];reports={p:read(f'qa/browser-{p}.json') for p in phases}
for p,r in reports.items():
 assert r['status']=='completed' and r['profileRemoved'] and r['processGroupTerminated'],p
 assert not r['runtimeErrors'] and not r['remoteRequests'],p
 assert r['inputHashes']=={'children-of-captain-grant.html':html_hash,'story-data.json':data_hash},p
 assert not Path(r['ownedProfile']).exists(),p
for p in ['320','390','1024','1440']:assert reports[p]['renderedInstances']==1688
assert reports['consent']['savedDeep']['paths']==188
assert not read('qa/structural-audit.json')['failures']
assert all(c['passed'] for c in read('qa/content-verification.json')['checks'])
assert read('qa/environment.json')['allSharedBuildHashesMatch']
process_lines=subprocess.check_output(['ps','-axo','pid,ppid,pgid,args'],text=True).splitlines()
owned=[line for line in process_lines if 'Google Chrome' in line and '--user-data-dir=' in line and 'grant-depth-v2-' in line]
assert not owned
cleanup={'atUtc':datetime.now(timezone.utc).isoformat(),'ownedChromeProcessesRemaining':owned,'allSixFinalProfilesAbsent':True,'allSixFinalOwnedProcessGroupsVerifiedAbsent':True,'scope':'Only grant-depth-v2 owned Chrome instances; other sessions not terminated.'}
(HERE/'qa/cleanup-verification.json').write_text(json.dumps(cleanup,indent=2)+'\n')
hashes={n:sha(HERE/n) for n in ['draft-ru.md','draft-en.md','story-data.json','children-of-captain-grant.html','chapter-scene-map.md','edition-omission-map.md','sources.md','witness-reading-ledger.json','metrics.json','QA.md']}
guide='''# Root personal reading handoff

This is an unpublished candidate. No root acceptance is asserted. All review files contain full-story spoilers.

Read `draft-ru.md` and then `draft-en.md` completely: 30 episodes, 113 paragraph pairs, 12,424 RU / 14,936 EN narrative words. The full Deep story is these connected drafts. Compare the 113 paragraph pairs to `story-data.json`; `qa/content-verification.json` establishes exact text transfer, not literary quality.

Read both Essential routes in `routes/essential-ru.md` and `routes/essential-en.md`, and both Core routes in `routes/core-ru.md` and `routes/core-en.md`. These preserve the actual continuous prefixes, 24 and 67 paragraphs. Their final UI framing explicitly calls them unfinished. Read each complete nested route in the standalone HTML too, including cover, warning, final and global Sources; a route dump does not certify browser reading.

Compare `chapter-scene-map.md` / `scene-map.json` and the 66-chapter `edition-omission-map.md`. Evaluate whether the retained people, scenes, humor, uncertainty and three successive journeys sustain the adventure. Word counts and successful QA are not sufficient acceptance.

Use `witness-reading-ledger.json` and `witness-chapter-ranges.json` to open the exact private witness. They contain hashes, locators and reading acknowledgements, no primary text extracts. Check the sensitive mechanisms listed at the end of the omission map: initial interpretation, condor/Thalcave and Portuguese, Robert's decoy ride, false Guinnard trail, Australia reading, authentic Ayrton papers and literal ship orders, Toline's corrective gift, tracks/poison/exposure/letter theft, captivity/tunnel/taboo refuge, signed wrong-country order, private-interview boundary, Ayrton's actual knowledge, night voice, survivors/message names, island disposition and homecoming comedy.

Read `sources.md` before judging edition coverage: complete Horne 66 chapters; only four selective French chapter checks. Full French collation is not claimed. The opening guessed date is not the wreck date; latitude is minutes and longitude is unresolved; the novel's island geography is fictional. Review colonial/narrator qualifications and actual omissions.

Open the standalone HTML locally with fresh book progress. Deep must ask explicitly. Cancel it; test lower-mode contents and Sources. Confirm, then lower the depth, try the saved late Continue and reload: the ending and its saved title must stay protected until renewed session consent. QA is documented in `QA.md`, including the physical Safari/native touch limitation and the initial harness failure.

After these personal reads and comparisons, record root's own verdict bound to the exact candidate hashes. Do not infer that verdict from this implementation handoff. All root gate fields remain false, and publication is not authorized.

## Exact candidate hashes

'''
for n,h in hashes.items():guide+=f'- `{n}` — `{h}`\n'
(HERE/'root-reading-guide.md').write_text(guide)
files={str(p.relative_to(HERE)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='ready.json'}
assert not any(p.is_symlink() for p in HERE.rglob('*'))
ready={
 'schemaVersion':1,'atUtc':datetime.now(timezone.utc).isoformat(),'slug':'children-of-captain-grant',
 'title':{'ru':'Дети капитана Гранта','en':'The Children of Captain Grant'},'author':'Jules Verne',
 'status':'ready-for-root-personal-check','rootPersonalAcceptance':False,'publicationAllowed':False,'replacementPublicationAllowed':False,
 'rootEntireRuEnDraftRead':False,'rootAllNestedRoutesRead':False,'rootCoverageMapCompared':False,'rootKeyPrimaryPassagesChecked':False,'rootOmissionsAndQualificationsReviewed':False,
 'rootAcceptance':None,'published':False,
 'scope':{'ownedDirectory':str(HERE),'newBookDirectoryOnly':True,'subagentsUsed':False,'gitPrDeployUsed':False,'contentServerStarted':False,'sharedInstalledFilesEdited':False,'oldCollectorEdited':False,'rootReaderCatalogueGlobalLedgersEdited':False,'otherCandidatesEdited':False},
 'authoring':{'contentMode':'narrative','order':['complete original Russian connected adventure','matching original English','natural paragraph/scene segmentation'],'connectedEpisodesPerLanguage':30,'narrativeParagraphsPerLanguage':113,'volumeRationale':'The developed whole three-part journey and explicit 66-chapter retention/omission map, not a quota. Rough planning range 12–18k RU words; final 12424 narrative words excludes framing and headings.'},
 'entryPoints':{'rootReadingGuide':'root-reading-guide.md','russianDraft':'draft-ru.md','englishDraft':'draft-en.md','authoringData':'story-data.json','standaloneHtml':'children-of-captain-grant.html','chapterSceneMap':'chapter-scene-map.md','editionOmissionMap':'edition-omission-map.md','sources':'sources.md','actualReadingLedger':'witness-reading-ledger.json','exactMetrics':'metrics.json','qa':'QA.md','shortRoutes':['routes/essential-ru.md','routes/essential-en.md','routes/core-ru.md','routes/core-en.md'],'deepRoutes':'Both full connected drafts plus warning/cover/final in the standalone reader.'},
 'modes':metrics['modes'],'parts':metrics['parts'],'wordDefinition':metrics['wordDefinition'],'timingCaveat':metrics['timingCaveat'],
 'readingEvidence':{'completeActualWitnessRead':True,'witnessPath':ledger['witness'],'witnessSha256':ledger['sha256'],'bytes':960921,'physicalLines':20151,'boundedUntruncatedReadRanges':34,'rangeRehashPassed':True,'chapters':66,'chaptersByPart':[26,19,21],'edition':'Historical Horne-edited English Gutenberg 2083, not the 70-chapter French original','frenchSelectiveChapterChecks':4,'fullFrenchCollation':False,'noPrimaryTextOrExtractFilesInCandidate':True,'priorPublishedPilotsAreExamplesNotQuotas':True,'treasureIslandAndLostWorldRootAcceptanceClaimed':False},
 'spoilers':{'freshProgressNamespace':'book-tiktok.children-of-captain-grant.depth-v2.','sessionOnlyConsent':True,'persistentApproval':False,'loweringDepthRevokes':True,'reloadRestoresApproval':False,'endingBearingSavedTitlesBeforeConsent':False,'inlineWarningBeforeNarrativeParagraph':68,'essentialNarrativeTail':'thaouka','coreNarrativeTail':'camp','deepNarrativeTail':'arabella','essentialAndCoreExplicitlyUnfinished':True},
 'qa':{'structuralPasses':69,'structuralWarnings':0,'structuralFailures':0,'contentAndWitnessChecksPassed':57,'allFinalReportInputHashesMatchCandidate':True,'viewports':[[320,568],[390,844],[1024,768],[1440,900]],'matrixRenderStates':6752,'renderedParagraphArraysCompared':True,'savedDeepConsentPaths':188,'runtimeErrors':0,'remoteRequests':0,'ownedChromeProcessesRemaining':0,'allFinalProfilesRemoved':True,'allFinalProcessGroupsVerifiedTerminated':True,'chromeTimeoutSeconds':30,'nativeSafariOrPhysicalDeviceClaim':False,'nativeTouchCertified':False,'initialHarnessFailureRetained':'qa/browser-consent-initial-failed.json','finalReports':[f'qa/browser-{p}.json' for p in phases],'sharedBuildHashesMatch':True},
 'exactCandidateHashes':hashes,'fileManifestExcludesSelf':True,'files':files,
 'remainingRequiredWork':['Root personally reads the complete resulting RU and EN prose and every nested route, including reader framing.','Root compares coverage and real omissions and checks the key primary mechanisms on these exact candidate hashes.','Root records an explicit personal verdict before publication can be considered.']
}
(HERE/'ready.json').write_text(json.dumps(ready,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':ready['status'],'rootPersonalAcceptance':False,'publicationAllowed':False,'filesInManifest':len(files),'readySha256':sha(HERE/'ready.json'),'candidateHashes':hashes},ensure_ascii=False,indent=2))

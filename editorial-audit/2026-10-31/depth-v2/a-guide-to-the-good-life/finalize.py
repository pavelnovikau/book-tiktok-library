"""Bind this bounded candidate; never grants editorial acceptance or publication."""
from pathlib import Path
import json,hashlib,datetime
D=Path(__file__).resolve().parent
hash=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda n:json.loads((D/n).read_text())
data=load('story-data.json');metrics=load('metrics.json');parity=load('parity-check.json');audit=load('structural-audit.txt');ledger=load('reading-ledger.json');inventory=load('source-hashes.json')
assert data['targetModes']==metrics['counts']==parity['counts']==audit['modes']
for name,sha in metrics['currentContentHashes'].items():assert hash(D/name)==sha,name
assert audit['passes']==69 and not audit['failures'] and not audit['warnings']
reports=[]
for name in ['browser-320.json','browser-390.json','browser-1024.json','browser-1440.json','browser-ios-320.json']:
 q=load('qa/'+name)
 assert q['status']=='local-checks-completed',name
 assert q['traversal']['failures']==[] and not q['errors'] and not q['remoteRuntimeRequests'],name
 assert q['cleanup']['profileRemoved'] and q['cleanup']['remainingOwnedPids']==[],name
 for f,sha in q['inputHashes'].items():assert hash(D/f)==sha,(name,f)
 reports.append(dict(file='qa/'+name,sha256=hash(D/'qa'/name),renderedVisits=q['traversal']['views'],standardInteractionChecks=len(q['interaction']),cleanup=q['cleanup']))
files=[];history=[]
for p in sorted(D.rglob('*')):
 if not p.is_file() or p.name=='ready.json' or '__pycache__' in p.parts:continue
 rel=str(p.relative_to(D));entry=dict(path=str(p),relativePath=rel,sha256=hash(p),bytes=p.stat().st_size)
 if any(x in p.name for x in ['initial-harness-error','before-extra-interactions','before-argument-restoration','superseded-metrics']):history.append(entry)
 else:files.append(entry)
ready=dict(schemaVersion=2,slug=data['slug'],candidate='expanded-depth-v2',candidateRevision=2,atUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 status='ready-for-root-personal-check',rootPersonalAcceptance=False,publicationAllowed=False,bookContentPublicationAllowed=False,
 directory=str(D),standaloneHtml=str(D/(data['slug']+'.html')),contentMode=data['contentMode'],defaults=dict(language='ru',theme='dark',mode='essential',readingFont='sans'),
 counts=data['targetModes'],ruBodyWords=metrics['modes']['deep']['ru']['expositionBodyWords'],enBodyWords=metrics['modes']['deep']['en']['expositionBodyWords'],unitCount=metrics['unitCount'],pairedParagraphCount=metrics['paragraphPairs'],sourceCount=len(data['sources']),mediaCount=0,
 readingMetrics=metrics['modes'],metricDefinitions=metrics['definition'],exactContentHashes=metrics['currentContentHashes'],
 primaryEvidence=dict(englishEdition='OUP ©2009, package2008, ISBN9780195374612',completeMainTextReadInOrder=ledger['mainTextReadCompletelyInNumericSpineOrder'],substantiveFiles=len(ledger['fullMainTextFiles']),substantiveCharacters=ledger['mainTextCharacters'],hashedExtractionFiles=inventory['fileCount'],hashedExtractionCharacters=inventory['totalCharacters'],notesScope='Selected files085,329–341 only; remaining notes, bibliography and index not fully read.',russianScope='MIF2021, Gorokhov translation, Naranovich preface, ISBN9785001461937: edition page and whole preface read; full translation not collated.',privateRawSourcesCopied=False,newWebAcquisition=False),
 qa=dict(structuralPasses=audit['passes'],structuralWarnings=0,structuralFailures=0,authoredFieldsEqualEmbedding=True,actualDraftParagraphPairsEqual=153,renderedVisits=sum(q['renderedVisits'] for q in reports),standardInteractionChecks=sum(q['standardInteractionChecks'] for q in reports),reports=reports,offline=True,runtimeErrors=0,remoteRuntimeRequests=0,ownedChromeCleanup=True,physicalSafariTested=False),
 progressNamespace='book-tiktok.a-guide-to-the-good-life.depth-v2.',sharedPreferenceKey='bookLibrary.preferences.v1',
 rootReviewRequired=dict(completeCurrentRuEn=False,allNestedRoutes=False,chapterArgumentCasePracticeOmissions=False,keyPrimaryPassages=False,editorialDecision=False),
 sourceAndCoverageDocuments=['sources.md','reading-ledger.json','source-hashes.json','reading-dispatch.jsonl','coverage-map.md','coverage-map.json'],
 implementationChecksAreNotEditorialAcceptance=True,
 meaningfulLimitations=['Extensive original condensation, not a full book or authorized translation. Meaningful omissions are mapped after complete English main-text reading.','No complete Russian-translation collation or independent ancient-source critical edition.','Clinical/medical polemics remain attributed historical book arguments, not current advice or a treatment-efficacy certificate.','Physical iPhone/Safari was not tested.','Root must personally read and accept the exact final hashes before publication.'],
 changedOnlyThisDirectory=True,oldCollectorReadyReviewsRootCatalogueSharedSkillLogsGlobalStatusUntouched=True,gitPrDeployOrExternalMessages=False,subagentsUsed=False,
 files=files,supersededHistoricalFiles=history)
(D/'ready.json').write_text(json.dumps(ready,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:ready[k] for k in ['status','counts','ruBodyWords','enBodyWords','rootPersonalAcceptance','publicationAllowed']},ensure_ascii=False))
print('Bound current files:',len(files),'historical files:',len(history),'rendered visits:',ready['qa']['renderedVisits'])

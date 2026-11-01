from pathlib import Path
import collections
import csv
import datetime
import hashlib
import json
import shutil
import subprocess

C = Path('/Users/pn/smartcat/_artifacts/book-tiktok-library')
P = Path('/Users/pn/.t3/checkouts/book-tiktok-library-release07-20261031')
rel = Path('editorial-audit/2026-10-31')
A = C / rel
slug = 'four-thousand-weeks'
H = A / 'depth-v2' / slug
load = lambda p: json.loads(p.read_text())
dump = lambda p,d: p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
base = subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip()
assert base == '34cff4a06af2d6a4cb102b45169a073f9250e396'
dirty = subprocess.check_output(['git','diff','--name-only'],cwd=P,text=True).splitlines()
allowed = str(rel/'publisher-findings/expanded-depth-10-finish.py')
assert set(dirty) <= {allowed}, dirty
for name in dirty:
    assert (P/name).read_bytes() == (C/name).read_bytes()
ready = load(H/'ready.json'); report = load(H/'root-review/personal-review.json')
assert ready['status'] == report['status'] == 'root-personally-accepted'
assert ready['rootPersonalAcceptance'] and ready['publicationAllowed'] and ready['bookContentPublicationAllowed']
assert all(x['status']=='closed' for x in report['findings'])
assert len(ready['allArtifactHashes']) == 98
for name,row in ready['allArtifactHashes'].items():
    assert sha(Path(row['path'])) == row['sha256'], name
assert ready['rootReportSha256'] == sha(H/'root-review/personal-review.json')
old = load(P/'books.json'); cat = json.loads(json.dumps(old))
book = next(x for x in cat['books'] if x['slug']==slug)
assert book['screenCount'] == 52
book['screenCount'] = 87
book['readingMinutes'] = {k:int(v['ru']['uiLabel'].split()[0]) for k,v in report['metrics'].items()}
assert book['readingMinutes'] == {'essential':14,'core':35,'deep':47}
assert len(cat['books']) == 58 and sum(x['screenCount'] for x in cat['books']) == 2861
assert all(x == y for x,y in zip(old['books'],cat['books']) if x['slug']!=slug)
shutil.copyfile(H/(slug+'.html'),P/(slug+'.html')); dump(P/'books.json',cat)

plan = load(A/'depth-v2/PLAN.json'); plan['atUtc'] = stamp
for x in plan['books']:
    if x['slug']==slug:
        x.update(status='root-personally-accepted-awaiting-publication',rootAcceptance=str(H/'root-review/personal-review.json'),rootEntireRuEnDraftRead=True,rootAllNestedRoutesRead=True,rootRouteReadingMethod=report['personalReading']['routeReadingMethod'],rootCoverageMapCompared=True,rootKeyPrimaryPassagesChecked=True,rootOmissionsAndQualificationsReviewed=True,replacementPublicationAllowed=True,expandedCounts=report['counts'],acceptedHashes={n:sha(H/n) for n in ['story-data.json',slug+'.html']})
dump(A/'depth-v2/PLAN.json',plan)
pub = load(A/'publication-state.json')
pub['rootAcceptedNotYetPublished'] = list(dict.fromkeys(pub.get('rootAcceptedNotYetPublished',[])+[slug]))
dump(A/'publication-state.json',pub)
hold = load(A/'publisher-findings/fiction-depth-publication-hold.json');hold['atUtc']=stamp
hold['rootAcceptedExceptions'][slug]={'report':str(H/'root-review/personal-review.json'),'reportSha256':ready['rootReportSha256'],'htmlSha256':sha(H/(slug+'.html')),'jsonSha256':sha(H/'story-data.json')}
dump(A/'publisher-findings/fiction-depth-publication-hold.json',hold)
dispatch = load(A/'publisher-findings/release07-and-ten-worker-dispatch.json')
dispatch.update(atUtc=stamp,currentPublisher='root; personally accepted Four Thousand Weeks release pending',runtimeStatusPolled=False,assignmentCount=len(dispatch['workerAssignments']))
dispatch['latestDepthCompleted'][slug]='Personally accepted25/65/87; release pending'
waiting=[x['slug'] for x in plan['books'] if x['status']=='expanded-awaiting-root-personal-reading']
note='Four Thousand Weeks personally accepted:25/65/87screens;8006RU/9092EN noncover body words; UI Deep47/44minutes. All87RU/EN pairs read, final25Essential and40Core additions with both edges reread, all21revised final pairs read.28actual primary intervals/201paragraphs/24437displayed words; root primary checking selective. Publication pending;10expanded books live. '+str(len(waiting))+' candidates await personal root reading: '+', '.join(waiting)+'. Behave source gaps remain; all62positions retain individual acceptance.'
dispatch['assignmentNote']=note+' Recorded writer assignments: '+str(len(dispatch['workerAssignments']))+'; runtime not polled.'
dump(A/'publisher-findings/release07-and-ten-worker-dispatch.json',dispatch)
status=load(A/'library-status.json');status['asOfUtc']=stamp
for x in status['books']:
    if x['slug']==slug:x.update(maximumDepthStage='root-personally-accepted-awaiting-publication',rootExpandedTextAccepted=True,depthReviewStatus='root-accepted-expanded')
status['maximumDepthStages']=dict(collections.Counter(x['maximumDepthStage'] for x in status['books']))
assert sum(status['maximumDepthStages'].values())==62
status['basis']='62approved positions. Production remains verified PR46 at58books/2826screens until this release is merged and observed. Changed Essentialism/catalogue/homepage were exact; one unchanged prior canary had a documented transport-only failure. Historical factual stages remain distinct from current maximum-depth acceptance.'
dump(A/'library-status.json',status)
labels={'awaiting-expanded-work':'Awaits expanded work','source-map-incomplete':'Primary-source coverage incomplete','expanded-writing-assigned':'Expanded version assigned','root-accepted-and-live':'Personally accepted and live','root-personally-accepted-awaiting-publication':'Personally accepted; release pending','expanded-awaiting-root-personal-reading':'Candidate awaits personal root reading'}
md='# Library depth status\n\nUpdated '+stamp+'. '+note+'\n\n| Current depth stage | Count |\n|---|---:|\n'
md+=''.join('| '+labels.get(k,k)+' | '+str(v)+' |\n' for k,v in status['maximumDepthStages'].items())
md+='\n| Book | Author | Current depth stage |\n|---|---|---|\n'
md+=''.join('| '+x['title']+' | '+x['author']+' | '+labels.get(x['maximumDepthStage'],x['maximumDepthStage'])+' |\n' for x in status['books'])
(A/'library-status.md').write_text(md)
p=A/'library-status.csv'
with p.open(encoding='utf-8-sig',newline='') as f:
    reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
by={x['slug']:x for x in status['books']}
for x in rows:x.update(maximumDepthStage=by[x['slug']]['maximumDepthStage'],rootExpandedTextAccepted=str(by[x['slug']]['rootExpandedTextAccepted']).lower())
with p.open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');writer.writeheader();writer.writerows(rows)
intake=load(A/f'depth-v2/root-intake/{slug}.json')
intake.update(stage='root-personally-accepted-awaiting-publication',rootPersonalAcceptance=True,publicationAllowed=True,rootPersonalReview=str(H/'root-review/personal-review.json'),rootPersonalReviewSha256=ready['rootReportSha256'],readySha256=sha(H/'ready.json'),counts=report['counts'],bodyWords={'ru':8006,'en':9092},sourceScope=report['primaryReading'],hashBindingsVerified=len(ready['allArtifactHashes']),exactAcceptedHashes=report['exactContentHashes'],scope='Exact personally accepted expanded version; publication pending. Original completion/source handoff is preserved in input-ready.json.')
dump(A/f'depth-v2/root-intake/{slug}.json',intake)
(A/'depth-v2/PLAN.md').write_text((A/'depth-v2/PLAN.md').read_text()+'\n\nCurrent '+stamp+': '+note+'\n')
(C/'NEXT_STEPS.md').write_text('# Current personal review queue —2026-11-01\n\n'+note+'\n\nThis block supersedes historical states below.\n\n---\n\n'+(C/'NEXT_STEPS.md').read_text())
(C/'README.md').write_text((C/'README.md').read_text().replace('# Book TikTok Library\n','# Book TikTok Library\n\nCurrent2026-11-01: '+note+' This statement supersedes historical notes below.\n',1))
entry='## 2026-11-01 — Book library: Four Thousand Weeks personally accepted, publication pending\n\nRoot read all87original RU/EN pairs, all25final Essential pairs, all40Core additions with both actual adjacent route edges, and seven revised Deep-only pairs. All21final revised pairs have matching reading evidence. Full chapter/case/omission map, five amended rows, global method/source notes and two current mobile screenshots inspected.28actual primary intervals,201unique paragraphs and24437displayed words; all27planned selections covered. Primary reading remains selective; no complete root/published-English/figure/underlying-study certification.\n\nRestored irreversible commitment/relief, acceptance and patience mechanisms, hope/control ending and actual cases/practices; removed authoring asides and fixed precision/cohesion.25/65/87;8006RU/9092ENbody; UI47/44minutes. Fresh69structural passes,708route positions,80layouts, cold Serif100px in RU/EN, Settings/fonts/sources/focus, explicit deeper resume/reload and authentic legacy isolation pass.3140read-only bindings unchanged. Harness source-count/final-selector corrections archived; no reader change needed for those. Owned Chrome removed; physical Safari/PWA untested.98frozen artifact bindings; root report: editorial-audit/2026-10-31/depth-v2/four-thousand-weeks/root-review/personal-review.json.\n\nAccelerando completion ingested:74artifact/75manifest/78read-only input bindings verified; its expanded text remains personally unaccepted. '+note+'\n\n'
for p in [C/'LOG.md',Path('/Users/pn/smartcat/LOG.md')]:p.write_text(entry+p.read_text())
receipt={'atUtc':stamp,'slug':slug,'baseMerge':base,'rootReview':str(H/'root-review/personal-review.json'),'rootReviewSha256':ready['rootReportSha256'],'acceptedHashes':{n:sha(H/n) for n in ['story-data.json',slug+'.html']},'counts':report['counts'],'candidateBindingsVerified':98,'intendedBooks':58,'intendedScreens':2861,'scope':'Only one accepted public reader and its count/times;57other entries/58other root HTML unchanged. Private evidence excluded.','allOtherNewBookContentHeld':True}
dump(A/'publisher-findings/expanded-depth-11-intake.json',receipt)
shutil.copytree(H,P/rel/'depth-v2'/slug,dirs_exist_ok=True)
names=['depth-v2/PLAN.json','depth-v2/PLAN.md','depth-v2/root-intake/'+slug+'.json','depth-v2/root-intake/amphibian-man.json','depth-v2/root-intake/akselerando.json','publication-state.json','production-catalogue.json','library-status.json','library-status.csv','library-status.md','publisher-findings/fiction-depth-publication-hold.json','publisher-findings/release07-and-ten-worker-dispatch.json']
for name in names:
    (P/rel/name).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(A/name,P/rel/name)
for name in ['NEXT_STEPS.md','README.md','LOG.md']:shutil.copyfile(C/name,P/name)
for pattern in ['expanded-depth-10-*','expanded-depth-11-*','accelerando-expanded-*']:
    for path in (A/'publisher-findings').glob(pattern):
        if path.is_file():shutil.copyfile(path,P/rel/'publisher-findings'/path.name)
print(json.dumps({'base':base,'intendedBooks':58,'intendedScreens':2861,'bindings':98,'stages':status['maximumDepthStages']}))

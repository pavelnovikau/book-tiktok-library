from pathlib import Path
import json, hashlib, datetime, csv, shutil, subprocess, collections

C=Path('/Users/pn/smartcat/_artifacts/book-tiktok-library')
P=Path('/Users/pn/.t3/checkouts/book-tiktok-library-release07-20261031')
rel=Path('editorial-audit/2026-10-31');A=C/rel
slug='children-of-captain-grant';H=A/'depth-v2'/slug
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
load=lambda p:json.loads(p.read_text())
dump=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip()
assert base=='43cb318c047c7a020ac7013143d1a55506f4d933'
assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=P,text=True).strip()
ready=load(H/'ready.json');report=load(H/'root-review/personal-review.json')
assert ready['rootPersonalAcceptance'] and ready['publicationAllowed'] and not report['requiredOpenFindings']
for n,r in ready['allArtifactHashes'].items():assert sha(Path(r['path']))==r['sha256'],n
assert sha(H/'root-review/personal-review.json')==ready['rootPersonalReviewSha256']
oldcat=load(P/'books.json');cat=json.loads(json.dumps(oldcat))
b=next(x for x in cat['books'] if x['slug']==slug)
b['screenCount']=116;b['readingMinutes']={k:v['builderCeilingMinutes']['ru'] for k,v in report['metrics'].items()}
assert all(x==y for x,y in zip(oldcat['books'],cat['books']) if x['slug']!=slug)
shutil.copyfile(H/(slug+'.html'),P/(slug+'.html'));dump(P/'books.json',cat)
assert len(cat['books'])==58 and sum(x['screenCount'] for x in cat['books'])==2615

plan=load(A/'depth-v2/PLAN.json');plan['atUtc']=stamp
for row in plan['books']:
    s=row['slug']
    if s==slug:
        row.update(status='root-personally-accepted-awaiting-publication',rootAcceptance=str(H/'root-review/personal-review.json'),rootEntireRuEnDraftRead=True,rootAllNestedRoutesRead=True,rootCoverageMapCompared=True,rootKeyPrimaryPassagesChecked=True,rootOmissionsAndQualificationsReviewed=True,replacementPublicationAllowed=True,expandedCounts=ready['counts'],acceptedHashes={n:sha(H/n) for n in ['story-data.json',slug+'.html']})
    elif s in ['make-time','essentialism']:
        intake=load(A/f'depth-v2/root-intake/{s}.json')
        row.update(status='expanded-awaiting-root-personal-reading',rootIntake=str(A/f'depth-v2/root-intake/{s}.json'),expandedCounts=intake['counts'])
dump(A/'depth-v2/PLAN.json',plan)
pub=load(A/'publication-state.json');pub['rootAcceptedNotYetPublished']=[slug];dump(A/'publication-state.json',pub)
hold=load(A/'publisher-findings/fiction-depth-publication-hold.json');hold['atUtc']=stamp
hold['rootAcceptedExceptions'][slug]={'report':str(H/'root-review/personal-review.json'),'reportSha256':ready['rootPersonalReviewSha256'],'htmlSha256':sha(H/(slug+'.html')),'jsonSha256':sha(H/'story-data.json')}
dump(A/'publisher-findings/fiction-depth-publication-hold.json',hold)
dispatch=load(A/'publisher-findings/release07-and-ten-worker-dispatch.json');dispatch['atUtc']=stamp
for k in ['workerAssignments','workerTaskIds']:
    for s in ['make-time','essentialism']:dispatch[k].pop(s,None)
dispatch.update(assignmentCount=len(dispatch['workerAssignments']),runtimeStatusPolled=False,currentPublisher='root; personally accepted Children of Captain Grant release',assignmentNote='Make Time and Essentialism completions ingested; no remaining writing assignment in this snapshot. Four candidates await root personal reading. Historical task records below are not active-worker claims.')
dispatch['latestDepthCompleted'].update({slug:'Root personally accepted current26/69/116 candidate; release being prepared','make-time':'Completed;73 bindings verified; root personal reading pending','essentialism':'Completed;50 bindings verified; root personal reading pending'})
dump(A/'publisher-findings/release07-and-ten-worker-dispatch.json',dispatch)
status=load(A/'library-status.json');status['asOfUtc']=stamp
stages={x['slug']:x for x in plan['books']}
for row in status['books']:
    stage=stages[row['slug']]['status']
    row['maximumDepthStage']={'needs-root-depth-and-source-assessment':'awaiting-expanded-work','expanded-source-map-incomplete':'source-map-incomplete'}.get(stage,stage)
    row['rootExpandedTextAccepted']=bool(stages[row['slug']]['rootAcceptance'])
    if row['slug']==slug:row['depthReviewStatus']='root-accepted-expanded'
status['maximumDepthStages']=dict(collections.Counter(x['maximumDepthStage'] for x in status['books']))
assert sum(status['maximumDepthStages'].values())==62
status['basis']='62 approved positions. Production remains PR41 at58books/2536screens until this release is merged/verified. Historical factual stages are distinct from personal maximum-depth acceptance.'
dump(A/'library-status.json',status)
labels={'awaiting-expanded-work':'Awaits expanded work','source-map-incomplete':'Primary-source coverage incomplete','expanded-writing-assigned':'Expanded version assigned','root-accepted-and-live':'Personally accepted and live','root-personally-accepted-awaiting-publication':'Personally accepted; release pending','expanded-awaiting-root-personal-reading':'Candidate awaits personal root reading'}
md='# Library depth status\n\nUpdated '+stamp+'. Live58books/2536screens;62 approved positions. Grant is personally accepted; publication pending. Zebra, Irvine, Make Time and Essentialism await personal reading. No runtime polling.\n\n| Current depth stage | Count |\n|---|---:|\n'+''.join('| '+labels.get(k,k)+' | '+str(v)+' |\n' for k,v in status['maximumDepthStages'].items())
md+='\n| Book | Author | Current depth stage |\n|---|---|---|\n'+''.join('| '+x['title']+' | '+x['author']+' | '+labels.get(x['maximumDepthStage'],x['maximumDepthStage'])+' |\n' for x in status['books'])
(A/'library-status.md').write_text(md)
csvpath=A/'library-status.csv'
with csvpath.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
by={x['slug']:x for x in status['books']}
for x in rows:x.update(maximumDepthStage=by[x['slug']]['maximumDepthStage'],rootExpandedTextAccepted=str(by[x['slug']]['rootExpandedTextAccepted']).lower())
with csvpath.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
intake=load(A/f'depth-v2/root-intake/{slug}.json')
intake.update(stage='root-personally-accepted-awaiting-publication',rootPersonalAcceptance=True,publicationAllowed=True,rootPersonalReview=str(H/'root-review/personal-review.json'),rootPersonalReviewSha256=ready['rootPersonalReviewSha256'],counts=ready['counts'],exactAcceptedHashes=report['exactContentHashes'])
dump(A/f'depth-v2/root-intake/{slug}.json',intake)
note='Children of Captain Grant is personally accepted at26/69/116 after complete RU/EN retelling reading, full coverage/omission maps and selected actual primary checks. Deep12410RU/14921EN narrative words; publication being prepared. Five expanded works are live. Next personal reading: Zebra, Irvine, Make Time, Essentialism. Their completion hashes are verified; prose is unaccepted. Behave actual-primary coverage remains incomplete. All62 positions retain individual root acceptance.'
(A/'depth-v2/PLAN.md').write_text((A/'depth-v2/PLAN.md').read_text()+'\n\nCurrent '+stamp+': '+note+'\n')
(C/'NEXT_STEPS.md').write_text('# Current personal review queue — 2026-11-01\n\n'+note+'\n\nThis current block supersedes historical states below.\n\n---\n\n'+(C/'NEXT_STEPS.md').read_text())
(C/'README.md').write_text((C/'README.md').read_text().replace('# Book TikTok Library\n','# Book TikTok Library\n\nCurrent2026-11-01: '+note+' This statement supersedes historical release notes below.\n',1))
receipt={'atUtc':stamp,'slug':slug,'baseMerge':base,'rootReview':str(H/'root-review/personal-review.json'),'rootReviewSha256':ready['rootPersonalReviewSha256'],'acceptedHashes':{n:sha(H/n) for n in ['story-data.json',slug+'.html']},'counts':ready['counts'],'candidateBindingsVerified':len(ready['allArtifactHashes']),'scope':'Only one personally accepted expanded reader plus catalogue count and reading times. All other58 root HTML and57 catalogue entries remain unchanged. Private evidence is excluded from the public build.','allOtherNewBookContentHeld':True}
dump(A/'publisher-findings/expanded-depth-06-intake.json',receipt)
shutil.copytree(H,P/rel/'depth-v2'/slug,dirs_exist_ok=True)
relative=['depth-v2/PLAN.json','depth-v2/PLAN.md','depth-v2/root-intake/'+slug+'.json','depth-v2/root-intake/make-time.json','depth-v2/root-intake/essentialism.json','publication-state.json','production-catalogue.json','library-status.json','library-status.csv','library-status.md','publisher-findings/fiction-depth-publication-hold.json','publisher-findings/release07-and-ten-worker-dispatch.json']
for n in relative:
    (P/rel/n).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(A/n,P/rel/n)
for n in ['NEXT_STEPS.md','README.md']:shutil.copyfile(C/n,P/n)
for pattern in ['expanded-depth-05-*','expanded-depth-06-*','essentialism-expanded-*']:
    for q in (A/'publisher-findings').glob(pattern):
        if q.is_file():shutil.copyfile(q,P/rel/'publisher-findings'/q.name)
print(json.dumps({'base':base,'intendedBooks':58,'intendedScreens':2615,'bindings':len(ready['allArtifactHashes']),'maximumDepthStages':status['maximumDepthStages']}))

from pathlib import Path
import json, hashlib, datetime, csv, shutil, subprocess, collections
C = Path('/Users/pn/smartcat/_artifacts/book-tiktok-library')
P = Path('/Users/pn/.t3/checkouts/book-tiktok-library-release07-20261031')
A = C / 'editorial-audit/2026-10-31'
rel = Path('editorial-audit/2026-10-31')
H = A / 'depth-v2/white-fang'
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
load = lambda p: json.loads(p.read_text())
dump = lambda p,d: p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
base = subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip()
assert base == '1ac0b366f86fc24404a779e8e0f4a3362b90aaa3'
assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=P,text=True).strip()
ready = load(H/'ready.json'); report = load(H/'root-review/personal-review.json')
assert ready['rootPersonalAcceptance'] and ready['publicationAllowed'] and not report['requiredOpenFindings']
for n,r in ready['allArtifactHashes'].items():
    p=Path(r['path']);assert sha(p)==r['sha256'],n
assert sha(H/'root-review/personal-review.json') == ready['rootPersonalReviewSha256']
oldcat=load(P/'books.json');cat=json.loads(json.dumps(oldcat));b=next(x for x in cat['books'] if x['slug']=='white-fang')
b['screenCount']=89
b['readingMinutes']={k:v['builderCeilingMinutes']['ru'] for k,v in report['metrics'].items()}
assert all(x==y for x,y in zip(oldcat['books'],cat['books']) if x['slug']!='white-fang')
shutil.copyfile(H/'white-fang.html',P/'white-fang.html');dump(P/'books.json',cat)
assert len(cat['books'])==58 and sum(x['screenCount'] for x in cat['books'])==2536

plan=load(A/'depth-v2/PLAN.json');plan['atUtc']=stamp
for row in plan['books']:
    s=row['slug']
    if s=='white-fang':
        row.update(status='root-personally-accepted-awaiting-publication',rootAcceptance=str(H/'root-review/personal-review.json'),rootEntireRuEnDraftRead=True,rootAllNestedRoutesRead=True,rootCoverageMapCompared=True,rootKeyPrimaryPassagesChecked=True,rootOmissionsAndQualificationsReviewed=True,replacementPublicationAllowed=True,expandedCounts=ready['counts'],acceptedHashes={n:sha(H/n) for n in ['story-data.json','white-fang.html']})
    elif s in ['why-zebras-dont-get-ulcers','a-guide-to-the-good-life']:
        intake=load(A/f'depth-v2/root-intake/{s}.json')
        cand=load(A/f'depth-v2/{s}/ready.json')
        row.update(status='expanded-awaiting-root-personal-reading',rootIntake=str(A/f'depth-v2/root-intake/{s}.json'),expandedCounts=cand.get('counts') or {k:v['screens'] for k,v in cand['modes'].items()})
dump(A/'depth-v2/PLAN.json',plan)
pub=load(A/'publication-state.json');pub['rootAcceptedNotYetPublished']=['white-fang'];dump(A/'publication-state.json',pub)
hold=load(A/'publisher-findings/fiction-depth-publication-hold.json');hold['atUtc']=stamp
hold['rootAcceptedExceptions']['white-fang']={'report':str(H/'root-review/personal-review.json'),'reportSha256':ready['rootPersonalReviewSha256'],'htmlSha256':sha(H/'white-fang.html'),'jsonSha256':sha(H/'story-data.json')};dump(A/'publisher-findings/fiction-depth-publication-hold.json',hold)
dispatch=load(A/'publisher-findings/release07-and-ten-worker-dispatch.json');dispatch['atUtc']=stamp
for k in ['workerAssignments','workerTaskIds']:
    for s in ['why-zebras-dont-get-ulcers','a-guide-to-the-good-life']:dispatch[k].pop(s,None)
dispatch['assignmentCount']=len(dispatch['workerAssignments']);dispatch['runtimeStatusPolled']=False
dispatch['currentPublisher']='root; personally accepted White Fang release'
dispatch['latestDepthCompleted'].update({'white-fang':'Root personally accepted current36/51/89 candidate; release being prepared','why-zebras-dont-get-ulcers':'Completed;58 bindings verified; personal root reading pending','a-guide-to-the-good-life':'Completed;54 bindings verified; personal root reading pending','the-lost-world':'Personally accepted, live and production-verified PR40'})
dispatch['published'].update(books=58,screens=2483,rootExpandedAcceptedAndLive=4)
dump(A/'publisher-findings/release07-and-ten-worker-dispatch.json',dispatch)
status=load(A/'library-status.json');status['asOfUtc']=stamp
stages={x['slug']:x['status'] for x in plan['books']}
for row in status['books']:
    stage=stages[row['slug']]
    if stage=='needs-root-depth-and-source-assessment':stage='awaiting-expanded-work'
    if stage=='expanded-source-map-incomplete':stage='source-map-incomplete'
    row['maximumDepthStage']=stage;row['rootExpandedTextAccepted']=bool(next(x for x in plan['books'] if x['slug']==row['slug'])['rootAcceptance'])
status['maximumDepthStages']=dict(collections.Counter(x['maximumDepthStage'] for x in status['books']))
assert sum(status['maximumDepthStages'].values())==62
status['rootExpandedAcceptedPublished']=4;dump(A/'library-status.json',status)
labels={'awaiting-expanded-work':'Awaits expanded work','source-map-incomplete':'Primary-source coverage incomplete','expanded-writing-assigned':'Expanded version assigned','root-accepted-and-live':'Personally accepted and live','root-personally-accepted-awaiting-publication':'Personally accepted; release pending','expanded-awaiting-root-personal-reading':'Candidate awaits personal root reading'}
md='# Library depth status\n\nUpdated '+stamp+'. Live58books/2483screens;62 approved positions. White Fang is personally accepted but not yet published. Callback results for Zebra and Irvine are ingested; their prose is unaccepted. Current assigned work uses Sol max; runtime is not polled.\n\n| Current depth stage | Count |\n|---|---:|\n'
md+=''.join('| '+labels.get(k,k)+' | '+str(v)+' |\n' for k,v in status['maximumDepthStages'].items())
md+='\n| Book | Author | Current depth stage |\n|---|---|---|\n'+''.join('| '+x['title']+' | '+x['author']+' | '+labels.get(x['maximumDepthStage'],x['maximumDepthStage'])+' |\n' for x in status['books'])
(A/'library-status.md').write_text(md)
csvpath=A/'library-status.csv'
with csvpath.open(encoding='utf-8-sig',newline='') as f:
    reader=csv.DictReader(f);fields=reader.fieldnames;csvrows=list(reader)
by={x['slug']:x for x in status['books']}
for row in csvrows:
    row['maximumDepthStage']=by[row['slug']]['maximumDepthStage'];row['rootExpandedTextAccepted']=str(by[row['slug']]['rootExpandedTextAccepted']).lower()
with csvpath.open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');writer.writeheader();writer.writerows(csvrows)
note='White Fang is personally accepted at36/51/89 after root reading and chronology/actor/route repairs; publication is being prepared. Four earlier expanded works are live. Next personal reading: Children of Captain Grant, then Zebra, then Irvine. Zebra and Irvine callbacks are hash-ingested only; Make Time remains assigned. Behave source coverage remains incomplete. All62 positions retain individual root reading and acceptance.'
(A/'depth-v2/PLAN.md').write_text((A/'depth-v2/PLAN.md').read_text()+'\n\nCurrent '+stamp+': '+note+'\n')
(C/'NEXT_STEPS.md').write_text('# Active personal reading and release queue - 2026-11-01\n\n'+note+'\n\nThis current block supersedes historical states below.\n\n---\n\n'+(C/'NEXT_STEPS.md').read_text())
(C/'README.md').write_text((C/'README.md').read_text().replace('# Book TikTok Library\n', '# Book TikTok Library\n\nCurrent2026-11-01: '+note+'\n',1))
intake={'atUtc':stamp,'slug':'white-fang','baseMerge':base,'rootReview':str(H/'root-review/personal-review.json'),'rootReviewSha256':ready['rootPersonalReviewSha256'],'acceptedHashes':{n:sha(H/n) for n in ['story-data.json','white-fang.html']},'counts':ready['counts'],'scope':'Only one personally accepted expanded reader plus catalogue count and reading times. All other58 root HTML and57 catalogue entries unchanged. Private personal-review evidence is not a public asset.','allOtherNewBookContentHeld':True,'candidateBindingsVerified':len(ready['allArtifactHashes'])}
dump(A/'publisher-findings/expanded-depth-05-intake.json',intake)
shutil.copytree(H,P/rel/'depth-v2/white-fang',dirs_exist_ok=True)
relative_files=['depth-v2/PLAN.json','depth-v2/PLAN.md','depth-v2/root-intake/white-fang.json','depth-v2/root-intake/why-zebras-dont-get-ulcers.json','depth-v2/root-intake/a-guide-to-the-good-life.json','publication-state.json','production-catalogue.json','library-status.json','library-status.csv','library-status.md','publisher-findings/fiction-depth-publication-hold.json','publisher-findings/release07-and-ten-worker-dispatch.json']
for name in relative_files:
    (P/rel/name).parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(A/name,P/rel/name)
for name in ['NEXT_STEPS.md','README.md']:shutil.copyfile(C/name,P/name)
for pattern in ['expanded-depth-04-*','expanded-depth-05-*']:
    for p in (A/'publisher-findings').glob(pattern):
        if p.is_file():shutil.copyfile(p,P/rel/'publisher-findings'/p.name)
print(json.dumps({'base':base,'intendedBooks':58,'intendedScreens':2536,'readyBindings':len(ready['allArtifactHashes']),'maximumDepthStages':status['maximumDepthStages']}))

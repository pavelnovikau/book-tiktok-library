from pathlib import Path
import json, datetime, csv, shutil, collections
C=Path('/Users/pn/smartcat/_artifacts/book-tiktok-library')
P=Path('/Users/pn/.t3/checkouts/book-tiktok-library-release07-20261031')
rel=Path('editorial-audit/2026-10-31');A=C/rel
load=lambda p:json.loads(p.read_text())
dump=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
proof=load(A/'publisher-findings/expanded-depth-05-production.json');assert proof['changedAssetsAndCanariesMatch']
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();h=A/'depth-v2/white-fang';review=load(h/'root-review/personal-review.json')
receipt={'atUtc':stamp,'status':'published-and-production-verified','pr':'https://github.com/pavelnovikau/book-tiktok-library/pull/41','head':proof['head'],'merge':proof['merge'],'slug':'white-fang','counts':review['counts'],'narrativeWords':{'ru':8173,'en':10071},'uiReadingMinutes':{k:v['builderCeilingMinutes'] for k,v in review['metrics'].items()},'rootPersonallyReadCompleteRuEnTextAndRoutes':True,'rootWholePrimaryContinuouslyRead':False,'exactAcceptedHashes':{k:v for k,v in review['exactContentHashes'].items() if k in ['white-fang.html','story-data.json']},'checks':'3 SUCCESS; no reviews or inline findings','catalogueBooks':58,'catalogueScreens':2536,'productionHttpAssetMatches':7,'private404s':2,'all69AssetsFreshlyFetched':False,'allOtherPublicContentLocallyUnchanged':True,'allUnacceptedBookContentStillHeld':True,'ownedChromeProcessesProfilesRemoved':True,'rootNextReading':['children-of-captain-grant','why-zebras-dont-get-ulcers','a-guide-to-the-good-life']}
for root in [C,P]:dump(root/rel/'publisher-findings/expanded-depth-05-receipt.json',receipt)
pub=load(A/'publication-state.json');pub.update(verifiedAtUtc=stamp,catalogueScreens=2536,productionMerge=proof['merge'],scope='PR41 White Fang personally accepted and live. Fresh exact HTTP hashes for new reader/catalogue, unchanged homepage and four previous expanded readers; two private404s. Other replacements require individual root reading.',rootAcceptedNotYetPublished=[],allCurrentProductionAssetsVerified=False,changedProductionAssetsVerified=True)
if 'white-fang' not in pub['rootAcceptedExpandedSlugs']:pub['rootAcceptedExpandedSlugs'].append('white-fang')
for n in ['local','readiness','review-threads','production','receipt']:
    p='publisher-findings/expanded-depth-05-'+n+'.json'
    if p not in pub['proofs']:pub['proofs'].append(p)
dump(A/'publication-state.json',pub);shutil.copyfile(P/'books.json',A/'production-catalogue.json')
plan=load(A/'depth-v2/PLAN.json');plan['atUtc']=stamp
for x in plan['books']:
    if x['slug']=='white-fang':x.update(status='root-accepted-and-live',currentScreens=89,currentRuBodyWords=8173,productionMerge=proof['merge'],productionPr=41)
dump(A/'depth-v2/PLAN.json',plan)
intake=load(A/'depth-v2/root-intake/white-fang.json');intake.update(stage='root-accepted-and-live',productionMerge=proof['merge'],productionPr=41);dump(A/'depth-v2/root-intake/white-fang.json',intake)
dispatch=load(A/'publisher-findings/release07-and-ten-worker-dispatch.json');dispatch['atUtc']=stamp;dispatch['currentPublisher']='root; White Fang PR41 merged and production-verified';dispatch['latestDepthCompleted']['white-fang']='Personally accepted, live and production-verified PR41';dispatch['published'].update(books=58,screens=2536,rootExpandedAcceptedAndLive=5,changedAssets41Verified=True);dump(A/'publisher-findings/release07-and-ten-worker-dispatch.json',dispatch)
status=load(A/'library-status.json');status.update(asOfUtc=stamp,rootExpandedAcceptedPublished=5)
for x in status['books']:
    if x['slug']=='white-fang':x.update(maximumDepthStage='root-accepted-and-live',rootExpandedTextAccepted=True,depthReviewStatus='root-accepted-expanded')
for x in status['books']:
    if x['maximumDepthStage']=='expanded-source-map-incomplete':x['maximumDepthStage']='source-map-incomplete'
status['maximumDepthStages']=dict(collections.Counter(x['maximumDepthStage'] for x in status['books']));assert sum(status['maximumDepthStages'].values())==62;dump(A/'library-status.json',status)
labels={'awaiting-expanded-work':'Awaits expanded work','source-map-incomplete':'Primary-source coverage incomplete','expanded-writing-assigned':'Expanded version assigned','root-accepted-and-live':'Personally accepted and live','root-personally-accepted-awaiting-publication':'Personally accepted; release pending','expanded-awaiting-root-personal-reading':'Candidate awaits personal root reading'}
md='# Library depth status\n\nUpdated '+stamp+'. Live58books/2536screens;62 approved positions. Five expanded works are personally accepted/live. Next root reading: Grant, Zebra, Irvine. Their worker packages are not accepted. Runtime is not polled.\n\n| Current depth stage | Count |\n|---|---:|\n'+''.join('| '+labels.get(k,k)+' | '+str(v)+' |\n' for k,v in status['maximumDepthStages'].items())+'\n| Book | Author | Current depth stage |\n|---|---|---|\n'+''.join('| '+x['title']+' | '+x['author']+' | '+labels.get(x['maximumDepthStage'],x['maximumDepthStage'])+' |\n' for x in status['books'])
(A/'library-status.md').write_text(md)
p=A/'library-status.csv'
with p.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
by={x['slug']:x for x in status['books']}
for x in rows:x.update(maximumDepthStage=by[x['slug']]['maximumDepthStage'],rootExpandedTextAccepted=str(by[x['slug']]['rootExpandedTextAccepted']).lower())
with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
note='White Fang PR41 is personally accepted, merged43cb318c and production-verified at36/51/89,8173RU/10071EN narrative words. Five expanded works are personally accepted/live; production58books/2536screens. Next personal reading: Children of Captain Grant, then Zebra, then Irvine. Make Time remains assigned. Other62-position replacements still require separate root acceptance.'
(A/'depth-v2/PLAN.md').write_text((A/'depth-v2/PLAN.md').read_text()+'\n\nProduction '+stamp+': '+note+'\n')
(C/'NEXT_STEPS.md').write_text('# Current root reading queue - 2026-11-01\n\n'+note+'\n\nThis current block supersedes historical states below.\n\n---\n\n'+(C/'NEXT_STEPS.md').read_text())
(C/'README.md').write_text((C/'README.md').read_text().replace('# Book TikTok Library\n','# Book TikTok Library\n\nCurrent2026-11-01: '+note+' Evidence: editorial-audit/2026-10-31/publisher-findings/expanded-depth-05-receipt.json.\n',1))
entry='## 2026-11-01 - Book library: White Fang personally accepted and live\n\nRoot read all88 input RU/EN pairs, all final repaired paragraphs and both complete shorter routes, the whole chapter map/Sources and selected actual primary passages. Restored Fort Yukon/Dawson/lynx/Cherokee chronology, the judge\'s Hall identification, the scale of Scott\'s cuff and Essential\'s fire siege; removed a shorter-route dangling reference.36/51/89;8173RU/10071EN narrative words. Story, delayed trust, violence, nursing, dreams and actual puppy ending remain.\n\n69structural checks, exact draft/data/HTML parity,704route positions,80layouts, true downgrade/reload and cold first Serif100px scroll passed. Owned Chrome cleaned; physical Safari/PWA untested. PR41 merged43cb318c;7production assets match exact hashes and2private404s.58books/2536screens; all other public content locally unchanged. Evidence: _artifacts/book-tiktok-library/editorial-audit/2026-10-31/publisher-findings/expanded-depth-05-receipt.json.\n\nZebra and Irvine callbacks ingested58/54bindings; prose remains unaccepted. Next personal root reading: Grant, Zebra, Irvine. Make Time remains assigned; Behave actual-primary gaps remain. All62 positions retain individual acceptance.\n\n'
for p in [C/'LOG.md',Path('/Users/pn/smartcat/LOG.md')]:p.write_text(entry+p.read_text())
print(json.dumps({'live':True,'books':58,'screens':2536,'rootAcceptedLive':5,'maximumDepthStages':status['maximumDepthStages']}))

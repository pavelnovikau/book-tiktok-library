from pathlib import Path
import json,datetime,csv,collections,shutil

C=Path('/Users/pn/smartcat/_artifacts/book-tiktok-library')
P=Path('/Users/pn/.t3/checkouts/book-tiktok-library-release07-20261031')
rel=Path('editorial-audit/2026-10-31');A=C/rel
load=lambda p:json.loads(p.read_text())
dump=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
proof=load(A/'publisher-findings/expanded-depth-07-production.json')
assert proof['changedAssetsAndCanariesMatch'] and proof['private404sMatch']
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();slug='why-zebras-dont-get-ulcers'
H=A/'depth-v2'/slug;review=load(H/'root-review/personal-review.json')
receipt={'atUtc':stamp,'status':'published-and-production-verified','pr':proof['pr'],'head':proof['head'],'merge':proof['merge'],'slug':slug,'counts':review['counts'],'bodyWords':{'ru':13219,'en':13988},'uiReadingMinutes':{k:{l:v[l]['uiMinutes'] for l in ['ru','en']} for k,v in review['metrics'].items()},'rootPersonallyReadCompleteRuEnRetelling':True,'shorterRoutesMethod':review['personalReading']['routeReadingMethod'],'rootWholePrimaryContinuouslyRead':False,'rootPrimaryRanges':45,'exactAcceptedHashes':{k:v for k,v in review['exactContentHashes'].items() if k in [slug+'.html','story-data.json']},'checks':'3 SUCCESS; no reviews or inline findings','catalogueBooks':58,'catalogueScreens':2671,'productionHttpAssetMatches':9,'private404s':2,'all69AssetsFreshlyFetched':False,'allOtherPublicContentLocallyUnchanged':True,'allUnacceptedBookContentStillHeld':True,'ownedChromeProcessesProfilesRemoved':True,'rootNextReading':['a-guide-to-the-good-life','make-time','essentialism','four-thousand-weeks']}
for root in [C,P]:dump(root/rel/'publisher-findings/expanded-depth-07-receipt.json',receipt)
pub=load(A/'publication-state.json');pub.update(verifiedAtUtc=stamp,catalogueScreens=2671,productionMerge=proof['merge'],scope='PR43 expanded Zebra personally accepted and live. Fresh exact HTTP hashes for new reader/catalogue, homepage and six earlier accepted expanded books; two private404s. Other replacements still require individual root reading.',rootAcceptedNotYetPublished=[],allCurrentProductionAssetsVerified=False,changedProductionAssetsVerified=True)
if slug not in pub['rootAcceptedExpandedSlugs']:pub['rootAcceptedExpandedSlugs'].append(slug)
for n in ['local','readiness','review-threads','merge','production','receipt']:
    f='publisher-findings/expanded-depth-07-'+n+'.json'
    if f not in pub['proofs']:pub['proofs'].append(f)
dump(A/'publication-state.json',pub);shutil.copyfile(P/'books.json',A/'production-catalogue.json')
plan=load(A/'depth-v2/PLAN.json');plan['atUtc']=stamp
for x in plan['books']:
    if x['slug']==slug:x.update(status='root-accepted-and-live',currentScreens=107,currentRuBodyWords=13219,productionMerge=proof['merge'],productionPr=43)
dump(A/'depth-v2/PLAN.json',plan)
intake=load(A/f'depth-v2/root-intake/{slug}.json');intake.update(stage='root-accepted-and-live',productionMerge=proof['merge'],productionPr=43);dump(A/f'depth-v2/root-intake/{slug}.json',intake)
dispatch=load(A/'publisher-findings/release07-and-ten-worker-dispatch.json');dispatch['atUtc']=stamp
dispatch['currentPublisher']='root; expanded Zebra PR43 merged and production-verified'
dispatch['latestDepthCompleted'][slug]='Personally accepted, live and production-verified PR43'
dispatch['published'].update(books=58,screens=2671,rootExpandedAcceptedAndLive=7,changedAssets43Verified=True)
dump(A/'publisher-findings/release07-and-ten-worker-dispatch.json',dispatch)
status=load(A/'library-status.json');status.update(asOfUtc=stamp,rootExpandedAcceptedPublished=7,basis='62 approved positions. Exact changed PR43 production assets and canaries verified at58books/2671screens. Historical factual stages remain distinct from root maximum-depth acceptance.')
for x in status['books']:
    if x['slug']==slug:x.update(maximumDepthStage='root-accepted-and-live',rootExpandedTextAccepted=True,depthReviewStatus='root-accepted-expanded')
status['maximumDepthStages']=dict(collections.Counter(x['maximumDepthStage'] for x in status['books']));assert sum(status['maximumDepthStages'].values())==62
dump(A/'library-status.json',status)
labels={'awaiting-expanded-work':'Awaits expanded work','source-map-incomplete':'Primary-source coverage incomplete','expanded-writing-assigned':'Expanded version assigned','root-accepted-and-live':'Personally accepted and live','root-personally-accepted-awaiting-publication':'Personally accepted; release pending','expanded-awaiting-root-personal-reading':'Candidate awaits personal root reading'}
md='# Library depth status\n\nUpdated '+stamp+'.58 live catalogue books;62 approved positions. Seven expanded versions are personally accepted/live. Four candidates await root reading: Irvine, Make Time, Essentialism, Four Thousand Weeks. Selfie assigned; runtime not polled.\n\n| Current depth stage | Count |\n|---|---:|\n'+''.join('| '+labels.get(k,k)+' | '+str(v)+' |\n' for k,v in status['maximumDepthStages'].items())+'\n| Book | Author | Current depth stage |\n|---|---|---|\n'+''.join('| '+x['title']+' | '+x['author']+' | '+labels.get(x['maximumDepthStage'],x['maximumDepthStage'])+' |\n' for x in status['books'])
(A/'library-status.md').write_text(md)
p=A/'library-status.csv'
with p.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
by={x['slug']:x for x in status['books']}
for x in rows:x.update(maximumDepthStage=by[x['slug']]['maximumDepthStage'],rootExpandedTextAccepted=str(by[x['slug']]['rootExpandedTextAccepted']).lower())
with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
note='Expanded Zebra PR43 is personally accepted, merged and production-verified:37/70/107 screens,13219RU/13988EN body words, Deep77/67minutes in the UI. Seven expanded versions are personally accepted/live; production58books/2671screens. Irvine, Make Time, Essentialism and Four Thousand Weeks await personal reading. Selfie remains assigned. Behave primary-source gaps remain. All62 positions keep individual root acceptance.'
(A/'depth-v2/PLAN.md').write_text((A/'depth-v2/PLAN.md').read_text()+'\n\nProduction '+stamp+': '+note+'\n')
(C/'NEXT_STEPS.md').write_text('# Current personal reading queue —2026-11-01\n\n'+note+'\n\nThis current block supersedes historical states below.\n\n---\n\n'+(C/'NEXT_STEPS.md').read_text())
(C/'README.md').write_text((C/'README.md').read_text().replace('# Book TikTok Library\n','# Book TikTok Library\n\nCurrent2026-11-01: '+note+' Evidence: editorial-audit/2026-10-31/publisher-findings/expanded-depth-07-receipt.json. This statement supersedes historical notes below.\n',1))
entry='## 2026-11-01 — Book library: expanded Sapolsky stress reader personally accepted and live\n\nRoot completely read107 RU/EN retelling pairs and five final changed pairs;37 Essential pairs reread,33 Core additions reread with both neighboring edges. Complete18-chapter/68-grouped-case map and omissions read;45 actual primary ranges and six narrow official/primary online sections checked. No root continuous whole-primary or published-English collation claim. Restored the proposed depression recovery bridge, repaired three shorter-route references and an editorial aside;29 grouped-case entry locators corrected. Final37/70/107,13219RU/13988EN body words; UI Deep77/67minutes.\n\n69 structural checks,856 route positions,80 representative layouts, cold Serif100px, actual reload/preferences, explicit deeper resume and authentic legacy-state checks passed. Owned Chrome removed; physical Safari/PWA untested. PR43 merged '+proof['merge'][:8]+';9 production assets match,2 private404s.58books/2671screens; other public content locally unchanged. Evidence: _artifacts/book-tiktok-library/editorial-audit/2026-10-31/publisher-findings/expanded-depth-07-receipt.json.\n\nFour Thousand Weeks completion ingested46bindings; prose unaccepted. Root queue: Irvine, Make Time, Essentialism, Four Thousand Weeks. Selfie remains assigned, runtime not polled; Behave gaps remain. Seven of62 approved positions meet current personal maximum-depth acceptance.\n\n'
for p in [C/'LOG.md',Path('/Users/pn/smartcat/LOG.md')]:p.write_text(entry+p.read_text())
print(json.dumps({'live':True,'books':58,'screens':2671,'rootAcceptedLive':7,'maximumDepthStages':status['maximumDepthStages']}))

from pathlib import Path
import collections
import csv
import datetime
import json
import shutil

C = Path('/Users/pn/smartcat/_artifacts/book-tiktok-library')
P = Path('/Users/pn/.t3/checkouts/book-tiktok-library-release07-20261031')
rel = Path('editorial-audit/2026-10-31')
A = C/rel
load = lambda p:json.loads(p.read_text())
dump = lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
proof = load(A/'publisher-findings/expanded-depth-08-production.json')
assert proof['changedAssetsAndCanariesMatch'] and proof['private404sMatch']
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
slug = 'a-guide-to-the-good-life'
H = A/'depth-v2'/slug
review = load(H/'root-review/personal-review.json')
receipt = {'atUtc':stamp,'status':'published-and-production-verified','pr':proof['pr'],'head':proof['head'],'merge':proof['merge'],'slug':slug,'counts':review['counts'],'bodyWords':{'ru':7870,'en':9095},'uiReadingMinutes':{k:{language:v[language]['readerUiMinutes'] for language in ['ru','en']} for k,v in review['metrics'].items()},'rootPersonallyReadCompleteRuEnRetelling':True,'shorterRoutesMethod':review['personalReading']['routeReadingMethod'],'rootWholePrimaryContinuouslyRead':False,'rootPrimaryRanges':34,'exactAcceptedHashes':{k:v for k,v in review['exactContentHashes'].items() if k in [slug+'.html','story-data.json']},'checks':'3 SUCCESS; no reviews or inline findings','catalogueBooks':58,'catalogueScreens':2720,'productionHttpAssetMatches':10,'private404s':2,'all69AssetsFreshlyFetched':False,'allOtherPublicContentLocallyUnchanged':True,'allUnacceptedBookContentStillHeld':True,'ownedChromeProcessesProfilesRemoved':True,'rootNextReading':['make-time','essentialism','four-thousand-weeks','selfie']}
for root in [C,P]:
    dump(root/rel/'publisher-findings/expanded-depth-08-receipt.json',receipt)
pub = load(A/'publication-state.json')
pub.update(verifiedAtUtc=stamp,catalogueScreens=2720,productionMerge=proof['merge'],scope='PR44 expanded Irvine personally accepted and live. Fresh exact HTTP hashes for new reader/catalogue, homepage and seven earlier accepted expanded books; two private404s. Other replacements still require individual root reading.',rootAcceptedNotYetPublished=[],allCurrentProductionAssetsVerified=False,changedProductionAssetsVerified=True)
if slug not in pub['rootAcceptedExpandedSlugs']:
    pub['rootAcceptedExpandedSlugs'].append(slug)
for name in ['local','readiness','review-threads','merge','production','receipt']:
    filename = 'publisher-findings/expanded-depth-08-'+name+'.json'
    if filename not in pub['proofs']:
        pub['proofs'].append(filename)
dump(A/'publication-state.json',pub)
shutil.copyfile(P/'books.json',A/'production-catalogue.json')
plan = load(A/'depth-v2/PLAN.json')
plan['atUtc'] = stamp
for x in plan['books']:
    if x['slug'] == slug:
        x.update(status='root-accepted-and-live',currentScreens=85,currentRuBodyWords=7870,productionMerge=proof['merge'],productionPr=44)
dump(A/'depth-v2/PLAN.json',plan)
intake = load(A/f'depth-v2/root-intake/{slug}.json')
intake.update(stage='root-accepted-and-live',productionMerge=proof['merge'],productionPr=44)
dump(A/f'depth-v2/root-intake/{slug}.json',intake)
dispatch = load(A/'publisher-findings/release07-and-ten-worker-dispatch.json')
dispatch['atUtc'] = stamp
dispatch['currentPublisher'] = 'root; expanded Irvine PR44 merged and production-verified'
dispatch['latestDepthCompleted'][slug] = 'Personally accepted, live and production-verified PR44'
dispatch['published'].update(books=58,screens=2720,rootExpandedAcceptedAndLive=8,changedAssets44Verified=True)
dispatch['assignmentNote'] = 'Mindfulness and The Body Keeps the Score remain assigned; no runtime polling. Make Time, Essentialism, Four Thousand Weeks and Selfie await root reading. Eight expanded versions personally accepted and live.'
dump(A/'publisher-findings/release07-and-ten-worker-dispatch.json',dispatch)
status = load(A/'library-status.json')
status.update(asOfUtc=stamp,rootExpandedAcceptedPublished=8,basis='62 approved positions. Exact changed PR44 production assets and canaries verified at58books/2720screens. Historical factual stages remain distinct from root maximum-depth acceptance.')
for x in status['books']:
    if x['slug'] == slug:
        x.update(maximumDepthStage='root-accepted-and-live',rootExpandedTextAccepted=True,depthReviewStatus='root-accepted-expanded')
status['maximumDepthStages'] = dict(collections.Counter(x['maximumDepthStage'] for x in status['books']))
assert sum(status['maximumDepthStages'].values()) == 62
dump(A/'library-status.json',status)
labels = {'awaiting-expanded-work':'Awaits expanded work','source-map-incomplete':'Primary-source coverage incomplete','expanded-writing-assigned':'Expanded version assigned','root-accepted-and-live':'Personally accepted and live','root-personally-accepted-awaiting-publication':'Personally accepted; release pending','expanded-awaiting-root-personal-reading':'Candidate awaits personal root reading'}
md = '# Library depth status\n\nUpdated '+stamp+'.58 live catalogue books;62 approved positions. Eight expanded versions personally accepted/live. Four candidates await root reading: Make Time, Essentialism, Four Thousand Weeks, Selfie. Mindfulness and The Body Keeps the Score remain assigned; runtime not polled.\n\n| Current depth stage | Count |\n|---|---:|\n'
md += ''.join('| '+labels.get(k,k)+' | '+str(v)+' |\n' for k,v in status['maximumDepthStages'].items())
md += '\n| Book | Author | Current depth stage |\n|---|---|---|\n'
md += ''.join('| '+x['title']+' | '+x['author']+' | '+labels.get(x['maximumDepthStage'],x['maximumDepthStage'])+' |\n' for x in status['books'])
(A/'library-status.md').write_text(md)
p = A/'library-status.csv'
with p.open(encoding='utf-8-sig',newline='') as f:
    reader=csv.DictReader(f); fields=reader.fieldnames; rows=list(reader)
by = {x['slug']:x for x in status['books']}
for x in rows:
    x.update(maximumDepthStage=by[x['slug']]['maximumDepthStage'],rootExpandedTextAccepted=str(by[x['slug']]['rootExpandedTextAccepted']).lower())
with p.open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n'); writer.writeheader(); writer.writerows(rows)
note = 'Expanded Irvine PR44 is personally accepted, merged and production-verified:29/61/85screens,7870RU/9095EN body words, Deep46/44minutes in UI. Eight expanded versions personally accepted/live; production58books/2720screens. Make Time, Essentialism, Four Thousand Weeks and Selfie await personal reading. Mindfulness and The Body Keeps the Score remain assigned; runtime not polled. Behave source gaps remain. All62 positions retain individual root acceptance.'
(A/'depth-v2/PLAN.md').write_text((A/'depth-v2/PLAN.md').read_text()+'\n\nProduction '+stamp+': '+note+'\n')
(C/'NEXT_STEPS.md').write_text('# Current personal reading queue —2026-11-01\n\n'+note+'\n\nThis current block supersedes historical states below.\n\n---\n\n'+(C/'NEXT_STEPS.md').read_text())
(C/'README.md').write_text((C/'README.md').read_text().replace('# Book TikTok Library\n','# Book TikTok Library\n\nCurrent2026-11-01: '+note+' Evidence: editorial-audit/2026-10-31/publisher-findings/expanded-depth-08-receipt.json. This statement supersedes historical notes below.\n',1))
entry = '## 2026-11-01 — Book library: expanded Irvine personally accepted and live\n\nRoot completely read85RU/EN retelling pairs, reread29Essential pairs and32Core additions with both neighboring edges, and personally reread10final changed pairs. Full chapter/case/practice/omission map and Sources read;34 actual primary intervals cover all21 proposed selections. English chapters20/22 and reading program read completely; actual Russian edition/editor-preface bodies checked. No root continuous whole-primary or dual-edition collation claim. Seven findings repaired: authoring asides removed, shorter-route names resolved, actual humor/indifference consequence restored. Final29/61/85,7870RU/9095EN body words; UI46/44minutes.\n\n69structural checks,700route positions,80representative layouts, genuinely cold Serif100px, Settings, reload/preferences, explicit deeper resume and legacy isolation passed. Owned Chrome removed; physical Safari/PWA untested. PR44 merged '+proof['merge'][:8]+';10production asset hashes match,2private404s.58books/2720screens; other public content locally unchanged. Evidence: _artifacts/book-tiktok-library/editorial-audit/2026-10-31/publisher-findings/expanded-depth-08-receipt.json.\n\nSelfie callback ingested and64bindings verified; prose still unaccepted. Root queue: Make Time, Essentialism, Four Thousand Weeks, Selfie. Mindfulness/Body remain assigned; runtime not polled. Behave gaps remain. Eight of62 approved positions meet current personal maximum-depth acceptance.\n\n'
for p in [C/'LOG.md',Path('/Users/pn/smartcat/LOG.md')]:
    p.write_text(entry+p.read_text())
print(json.dumps({'live':True,'books':58,'screens':2720,'rootAcceptedLive':8,'maximumDepthStages':status['maximumDepthStages']}))

from pathlib import Path
import json, hashlib

H = Path(__file__).resolve().parent.parent
R = H / 'root-review'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
source = Path(json.loads((H/'source-reading-ledger.json').read_text())['sourceRoot'])
ledger = json.loads((R/'reading-ledger.json').read_text())
name, start, end = '021-978544611081-17.txt', 34346, 37500
if not any(x['file'] == name and x['start'] == start and x['end'] == end for x in ledger['primaryRangesActuallyRead']):
    text = (source/name).read_text()
    ledger['primaryRangesActuallyRead'].append({'file':name,'start':start,'end':end,'fileSha256':sha(source/name),'chunkSha256':hashlib.sha256(text[start:end].encode()).hexdigest(),'scope':'Actual bounded source text displayed and personally read by root; Unicode chars.'})
d = json.loads((H/'story-data.json').read_text())
ledger['essentialReadPairIds'] = [s['id'] for s in d['screens'] if s['level'] <= 1]
ledger['coreReadPairIds'] = [s['id'] for s in d['screens'] if s['level'] <= 2]
ledger['coreAddedPairsPersonallyReread'] = [s['id'] for s in d['screens'] if s['level'] == 2]
ledger['shorterRouteReadingMethod'] = 'All 107 original Deep RU/EN pairs read completely in order. All 37 Essential pairs reread completely in route order. All 33 extra Core pairs reread completely in RU/EN with their immediately preceding final sentence and following first sentence; shared Essential prose already reread in order. This is not a third complete rereading of shared duplicates. Five final changed pairs personally reread after repairs.'
ledger['allCurrentPairsRead'] = True
ledger['finalChangedPairsReread'] = ['unit-022','unit-044','unit-076','unit-085','unit-095']
if not any(x['id'] == 'ZB-R03' for x in ledger['pendingFindings']):
    ledger['pendingFindings'].append({'id':'ZB-R03','screens':['unit-044','unit-085','unit-095'],'type':'shorter-route continuity','finding':'Remove the reference to studies absent from Essential; explicitly identify the addictive drug after a glucocorticoid example; introduce the material public-services pathway without another referring to an omitted preceding pathway.'})
for x in ledger['pendingFindings']:
    x['status'] = 'repaired-and-personally-reread' if x['id'] != 'ZB-MAP-01' else '29-grouped-case-entry-locators-repaired-after-personal-primary-reading'
ledger['sourceMapScope'] = 'All 18 chapter entries and 68 grouped-case entries read; 29 grouped-case entry/context locators repaired. This does not certify every underlying original study or claim continuous full-primary reading by root.'
ledger['finalReadingStorySha256'] = sha(H/'story-data.json')
ledger['rootPersonalAcceptance'] = False
ledger['publicationAllowed'] = False
(R/'reading-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')

paths = [source/'index.json'] + sorted(source.glob('*.txt'))
lib = H.parents[3]
paths += [lib/n for n in ['why-zebras-dont-get-ulcers.html','books.json']]
paths += [lib/'collector-output/why-zebras-dont-get-ulcers'/n for n in ['story-data.json','why-zebras-dont-get-ulcers.html','sources.md','QA.md']]
paths += [Path(x) for x in json.loads((H/'immutable-input-hashes.json').read_text())]
paths = sorted(set(paths))
assert all(p.is_file() for p in paths)
baseline = R/'protected-baseline.json'
assert not baseline.exists(), 'Preserve the first protected root QA baseline.'
baseline.write_text(json.dumps({'scope':'Primary witness files, older corpus and shared code protected during root QA; no whole-literature claim.','files':[{'path':str(p),'sha256':sha(p)} for p in paths]},indent=2)+'\n')

# Reuse the established CDP harness with nonfiction-specific assertions.
s = (H.parent/'children-of-captain-grant/root-review/cold-settings.mjs').read_text()
for a,b in [('children-of-captain-grant','why-zebras-dont-get-ulcers'),('grant-root-cold-','zebra-root-cold-'),('paganel-secret','workplace-check'),("'bar'","'unit-038'"),("'farm'","'unit-039'"),("'kara-tete'","'unit-076'"),("'father'","'unit-095'"),("'shark'","'unit-001'")]:
    s = s.replace(a,b)
s = s.replace(";if(document.getElementById('deepConsentDialog').open)document.getElementById('confirmDeep').click()", '')
begin = s.index(" }else if(phase==='consent'){")
end = s.index(" }else{\n  if([320,1440].includes(width))", begin)
resume = r''' }else if(phase==='resume'){
  report.deeperResume=[];
  for(const l of ['ru','en'])for(const lower of ['essential','core']){
   await lang(l);await choose('deep');await go('unit-076');await choose(lower);await go('cover');
   const r=await ev(`(()=>{const d=JSON.parse(document.getElementById('book-tiktok-data').textContent),b=document.querySelector('[data-start="continue"]'),r={explicit:b.textContent.includes(d.modes.deep.label['${l}']),lowerRetained:document.querySelector('[data-mode].is-active').dataset.mode==='${lower}'};b.click();r.target=localStorage.getItem('${key}lastScreen')==='unit-076';r.deep=document.querySelector('[data-mode].is-active').dataset.mode==='deep';return r})()`);ok(Object.values(r).every(Boolean),'explicit nonfiction deeper resume '+JSON.stringify(r));report.deeperResume.push({l,lower,...r});
  }
  await lang('en');await choose('deep');await go('unit-076');await load();
  report.reload=await ev(`(()=>{const r={language:document.documentElement.lang==='en',depth:document.querySelector('[data-mode].is-active').dataset.mode==='deep',cover:!!document.querySelector('[data-start="continue"]')};document.querySelector('[data-start="continue"]').click();r.target=localStorage.getItem('${key}lastScreen')==='unit-076';return r})()`);ok(Object.values(report.reload).every(Boolean),'nonfiction saved depth/ID reload');
  for(const legacy of ['workplace-check','ses-gradient']){
   await ev(`localStorage.setItem('book-tiktok.why-zebras-dont-get-ulcers.lastScreen','${legacy}');localStorage.removeItem('${key}lastScreen')`);await load();
   ok(await ev(`!document.querySelector('[data-start="continue"]')&&localStorage.getItem('book-tiktok.why-zebras-dont-get-ulcers.lastScreen')==='${legacy}'`),'legacy ID does not masquerade as new expanded progress '+legacy);
  }
  await ev(`localStorage.setItem('${key}lastScreen','workplace-check')`);await load();
  report.invalidCurrentId=await ev(`!document.querySelector('[data-start="continue"]')`);ok(report.invalidCurrentId,'unknown current ID safely offers Start');
  await ev(`document.querySelector('[data-start="begin"]').click()`);ok(await ev(`localStorage.getItem('${key}lastScreen')==='unit-001'`),'Start enters first unit');
'''
s = s[:begin] + resume + s[end:]
s = s.replace("noLabels:!document.querySelector('#story .source-label')", "provenance:'${id}'==='cover'||!!document.querySelector('#story .source-label')")
s = s.replace("document.querySelectorAll('#sourcesList details li').length===113", "document.querySelectorAll('#sourcesList > li').length===6")
begin = s.index("  await choose('core');ok(await ev(")
end = s.index("  report.interactions=",begin)
s = s[:begin] + "  await choose('core');ok(await ev(`document.querySelectorAll('#sourcesList > li').length===6`),'nonfiction global sources remain accessible');\n" + s[end:]
s = s.replace('depth-filtered map checked.', 'all six nonfiction sources accessible at each depth.')
(R/'cold-settings.mjs').write_text(s)
print(json.dumps({'protectedFiles':len(paths),'primaryReadRanges':len(ledger['primaryRangesActuallyRead']),'rootAcceptance':False}))

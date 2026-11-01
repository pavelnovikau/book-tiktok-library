from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent.parent;R=H/'root-review';Q=R/'qa';Q.mkdir(exist_ok=True)
load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
l=load(R/'reading-ledger.json');d=load(H/'story-data.json')
assert len(l['deepReadPairIds'])==85 and len(l['essentialReadPairIds'])==29 and len(l['coreAddedPairsReread'])==32
extra=['default-philosophy','practicing-poverty','why-not-withdraw','humor-and-silence']
l['finalChangedPairIdsReread']+=extra
for x in l['pendingFindings']:x['status']='repaired-and-personally-reread'
l['allCurrentPairsRead']=True;l['shorterRouteReadingMethod']='All85 original Deep pairs read completely in RU/EN. All29 Essential pairs reread in order. All32 Core additions reread completely with the preceding final and following first sentences in route order; shared Essential prose already reread. Ten final changed pairs personally reread after their respective repairs. No third complete rereading of identical shared prose is claimed.'
l['currentFinalStoryDataSha256']=sha(H/'story-data.json');l['rootPersonalAcceptance']=False;l['publicationAllowed']=False
(R/'reading-ledger.json').write_text(json.dumps(l,ensure_ascii=False,indent=2)+'\n')
lib=H.parents[3];src=Path(load(H/'source-hashes.json')['privateSourceDirectory'])
paths=[src/x['file'] for x in load(H/'source-hashes.json')['files']]
paths+=[Path(x['path']) for x in l['additionalPrimaryActuallyRead']]
paths+=[lib/'a-guide-to-the-good-life.html',lib/'books.json',Path('/Users/pn/.t3/checkouts/book-tiktok-library-release07-20261031/a-guide-to-the-good-life.html')]
paths+=[lib/'collector-output/a-guide-to-the-good-life'/n for n in ['story-data.json','a-guide-to-the-good-life.html','sources.md','QA.md']]
installed=Path('/Users/pn/.codex/skills/book-tiktok')
paths+=[installed/n for n in ['SKILL.md','scripts/build_story.mjs','scripts/audit_story_html.mjs','scripts/reader-settings.mjs','assets/standalone-template.html','assets/reader-settings-head.html','assets/reader-settings.html','assets/reader-header.html']]
paths=sorted(set(paths));assert all(p.is_file() for p in paths);assert not (R/'protected-baseline.json').exists()
(R/'protected-baseline.json').write_text(json.dumps({'scope':'Read-only primary witnesses, prior reader/catalogue/collector and installed shared code.','files':[{'path':str(p),'sha256':sha(p)} for p in paths]},indent=2)+'\n')
s=(H.parent/'why-zebras-dont-get-ulcers/root-review/cold-settings.mjs').read_text()
for a,b in [('why-zebras-dont-get-ulcers','a-guide-to-the-good-life'),('zebra-root-cold-','irvine-root-cold-'),('workplace-check','modern-adaptation'),('ses-gradient','trial-with-feedback'),('unit-038','mother-and-water'),('unit-039','mother-and-water-continued'),('unit-076','medication-objection'),('unit-095','reconstructed-stoicism'),('unit-001','whole-life')]:s=s.replace(a,b)
s=s.replace("'final'","'final-doubt'").replace('"final"','"final-doubt"').replace("length===6","length===2").replace('all six nonfiction sources','both nonfiction sources')
(R/'cold-settings.mjs').write_text(s)
s=(H/'verify.mjs').read_text().replace("const dir=path.dirname(fileURLToPath(import.meta.url));","const dir=path.dirname(path.dirname(fileURLToPath(import.meta.url)));fs.mkdirSync(path.join(dir,'root-review','qa'),{recursive:true});")
s=s.replace("path.join(dir,'metrics.json')","path.join(dir,'root-review','qa','metrics.json')").replace("path.join(dir,'parity-check.json')","path.join(dir,'root-review','qa','parity-check.json')")
s+='''\nconst original=JSON.parse(read('root-review/input-story-data.json'));
const changed=d.screens.filter((s,i)=>JSON.stringify(s)!==JSON.stringify(original.screens[i])).map(s=>s.id);
const expected=['default-philosophy','practicing-poverty','evening-review-continued','why-not-withdraw','sex-and-marriage','humor-and-silence','political-extension','emotion-and-counseling-continued','remedy-and-explanation','insult-and-waiting'];
assert(JSON.stringify(changed)===JSON.stringify(expected),'exact ten changed pairs');
for(const k of Object.keys(original))if(k!=='screens')assert(JSON.stringify(d[k])===JSON.stringify(original[k]),'unchanged metadata '+k);
const root=JSON.parse(read('root-review/reading-ledger.json')),source=JSON.parse(read('source-hashes.json'));
const sha=b=>createHash('sha256').update(b).digest('hex');
for(const x of source.files)assert(sha(fs.readFileSync(path.join(source.privateSourceDirectory,x.file)))===x.sha256,'source input '+x.file);
for(const x of JSON.parse(read('root-review/protected-baseline.json')).files)assert(sha(fs.readFileSync(x.path))===x.sha256,'protected '+x.path);
for(const r of root.primaryRangesActuallyRead){const p=path.join(source.privateSourceDirectory,r.file),raw=fs.readFileSync(p);assert(sha(raw)===r.fileSha256,'root source file '+r.file);const chars=Array.from(raw.toString('utf8').replace(/\\r\\n?/g,'\\n'));assert(sha(chars.slice(r.start,r.end).join(''))===r.chunkSha256,'root source range '+r.file+'/'+r.start);}
for(const k of map.keyPrimaryPassagesForRoot){let at=k.characterRange[0];for(const r of root.primaryRangesActuallyRead.filter(r=>r.file===k.file).sort((a,b)=>a.start-b.start))if(r.start<=at&&r.end>at)at=r.end;assert(at>=k.characterRange[1],'all21 primary selections actually read '+k.label)}
const routeProof={};
for(const [mode,level] of [['essential',1],['core',2],['deep',3]])for(const lang of ['ru','en']){const actual=parse(read('route-'+mode+'.'+lang+'.md')).flatMap(u=>u.paragraphs),expected=d.screens.filter(s=>s.type!=='cover'&&s.level<=level).flatMap(s=>[...s.copy[lang].body.matchAll(/<p>([\\s\\S]*?)<\\/p>/g)].map(m=>unescape(m[1])));assert(JSON.stringify(actual)===JSON.stringify(expected),'exact route paragraphs '+mode+'/'+lang);routeProof[mode+'.'+lang]={paragraphs:actual.length,exactInOrder:true};}
const cp=await import('node:child_process');const audit=cp.spawnSync(process.execPath,['/Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs',path.join(dir,d.slug+'.html'),'--min-screens',String(d.screens.length),'--require-bilingual'],{encoding:'utf8'});fs.writeFileSync(path.join(dir,'root-review/qa/structural-audit.json'),audit.stdout);assert(audit.status===0,'structural audit '+audit.stderr);
fs.writeFileSync(path.join(dir,'root-review/qa/root-integrity.json'),JSON.stringify({atUtc:new Date().toISOString(),changedPairIds:changed,allSixRouteExports:routeProof,mainPrimaryFilesHashChecked:source.files.length,rootPrimaryRanges:root.primaryRangesActuallyRead.length,suggestedPrimarySelectionsCovered:map.keyPrimaryPassagesForRoot.length,extraRussianPrimaryFilesRead:root.additionalPrimaryActuallyRead.length,wholePrimaryContinuouslyReadByRoot:false,protectedFilesUnchanged:true,rootPersonalAcceptance:false,publicationAllowed:false},null,2)+'\\n');
'''
(R/'verify.mjs').write_text(s)
print(json.dumps({'protectedFiles':len(paths),'all85PairsRead':True,'tenChangedPairsReread':len(l['finalChangedPairIdsReread']),'rootAcceptance':False}))

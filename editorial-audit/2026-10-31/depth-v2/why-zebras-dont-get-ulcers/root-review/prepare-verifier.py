from pathlib import Path

H = Path(__file__).resolve().parent.parent
s = (H/'qa/measure.mjs').read_text().split('// Browser runs must describe')[0]
s += r'''
const R=path.join(dir,'root-review'),out=path.join(R,'qa');fs.mkdirSync(out,{recursive:true});
const check=(v,m)=>{if(!v)throw Error(m)};
const original=JSON.parse(fs.readFileSync(path.join(R,'input-story-data.json'),'utf8'));
const changed=d.screens.filter((s,i)=>JSON.stringify(s)!==JSON.stringify(original.screens[i])).map(s=>s.id);
check(JSON.stringify(changed)===JSON.stringify(['unit-022','unit-044','unit-076','unit-085','unit-095']),'exact five changed pairs');
for(const k of Object.keys(original))if(k!=='screens')check(JSON.stringify(d[k])===JSON.stringify(original[k]),'unchanged authoring metadata '+k);
const protectedInputs=JSON.parse(fs.readFileSync(path.join(R,'protected-baseline.json'),'utf8'));
for(const f of protectedInputs.files)check(hash(f.path)===f.sha256,'protected input '+f.path);
const coverage=JSON.parse(fs.readFileSync(path.join(dir,'coverage-map.json'),'utf8'));
let caseEntries=0,caseAnchors=0;const repaired=[];
const rootLedger=JSON.parse(fs.readFileSync(path.join(R,'reading-ledger.json'),'utf8'));
for(const r of rootLedger.primaryRangesActuallyRead){const f=path.join(ledger.sourceRoot,r.file),t=Array.from(fs.readFileSync(f,'utf8'));check(hash(f)===r.fileSha256,'root primary file '+r.file);check(createHash('sha256').update(t.slice(r.start,r.end).join('')).digest('hex')===r.chunkSha256,'root primary range '+r.file+'/'+r.start)}
for(const ch of coverage.chapters){
 const file=path.join(ledger.sourceRoot,ch.source.file),text=Array.from(fs.readFileSync(file,'utf8'));check(hash(file)===ch.source.sha256,'coverage chapter source');
 for(const c of ch.cases){caseEntries++;for(const a of c.sourceAnchors||[c.sourceAnchor]){caseAnchors++;check(createHash('sha256').update(text.slice(a.start,a.end).join('')).digest('hex')===a.sha256,'case anchor '+c.name);
  if(c.anchorReview){const ranges=rootLedger.primaryRangesActuallyRead.filter(r=>r.file===ch.source.file).sort((a,b)=>a.start-b.start);let at=a.start;for(const r of ranges){if(r.start<=at&&r.end>at)at=r.end}check(at>=a.end,'repaired anchor personally read '+c.name)}
 }if(c.anchorReview)repaired.push(c.name);}
}
check(coverage.chapters.length===18&&caseEntries===68&&repaired.length===29,'chapter/grouped case counts');
metrics.chapterBodyWords=[];
for(let chapter=1;chapter<=18;chapter++){
 const list=d.screens.filter(s=>s.bookLocation?.chapter===chapter);
 metrics.chapterBodyWords.push({chapter,screens:list.length,ru:list.reduce((n,s)=>n+words(s.copy.ru.body),0),en:list.reduce((n,s)=>n+words(s.copy.en.body),0)});
}
metrics.rootVerification={atUtc:new Date().toISOString(),changedPairIds:changed,allFinalChangedPairsPersonallyReread:rootLedger.finalChangedPairsReread,primaryRanges:rootLedger.primaryRangesActuallyRead.length,wholePrimaryContinuouslyReadByRoot:false,coverageChapters:18,groupedCaseEntries:caseEntries,caseAnchors,personallyRepairedGroupedCaseLocators:repaired.length,allAnchorsHashValid:true,protectedFileCount:protectedInputs.files.length,protectedFilesUnchanged:true,sourceReadingLedger:'Historical writer ledger integrity checked; not a claim that root read the entire book.'};
const audit=await import('node:child_process');const result=audit.spawnSync(process.execPath,['/Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs',path.join(dir,d.slug+'.html'),'--min-screens',String(d.screens.length),'--require-bilingual'],{encoding:'utf8'});
fs.writeFileSync(path.join(out,'structural-audit.json'),result.stdout);check(result.status===0,'structural audit '+result.stderr);
fs.writeFileSync(path.join(out,'metrics-and-integrity.json'),JSON.stringify(metrics,null,2)+'\n');
console.log(JSON.stringify({modes:Object.fromEntries(Object.entries(metrics.modes).map(([k,v])=>[k,{screens:v.screens,ru:v.ru,en:v.en}])),rootVerification:metrics.rootVerification},null,2));
'''
(H/'root-review/verify.mjs').write_text(s)
print('Prepared root-only verifier; historical QA remains untouched.')

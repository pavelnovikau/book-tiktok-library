import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
const root='editorial-audit/2026-10-31/publisher-findings';
const json=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const sha=p=>hash(fs.readFileSync(p));
const embedded=html=>{const m=[...html.matchAll(/<script id="book-tiktok-data" type="application\/json">\s*([\s\S]*?)<\/script>/g)];assert.equal(m.length,1);return JSON.parse(m[0][1]);};
const receipt=json(`${root}/release-08.json`),catalogue=json('books.json'),intake=json(`${root}/release-08-proof/intake.json`);
for(const entry of intake.copied)assert.equal(sha(entry.path),entry.sha256,entry.path);
const results=[];
for(const e of receipt.acceptedCandidates){
 const data=json(`collector-output/${e.slug}/story-data.json`),raw=fs.readFileSync(`collector-output/${e.slug}/${e.slug}.html`,'utf8'),html=fs.readFileSync(`${e.slug}.html`,'utf8');
 assert.deepEqual(embedded(html),embedded(raw),`${e.slug}: effective corpus, sources, modes, media unchanged by integration`);
 assert.equal(sha(e.reviewPath),e.reviewSha256);assert.equal(sha(e.readyPath),e.readySha256);
 const review=json(e.reviewPath);assert.equal(review.verdict,e.originalVerdict);
 if(e.parentClosure){
  const c=json(e.parentClosure);assert.equal(sha(e.parentClosure),e.parentClosureSha256);assert.equal(c.originalReviewSha256,e.reviewSha256);
  const before=structuredClone(data),old=new Map(c.screensBefore.map(s=>[s.id,s]));before.screens=before.screens.map(s=>old.get(s.id)||s);before.sources=c.sourcesBefore;before.methodNote=c.methodNoteBefore;
  assert.equal(hash(JSON.stringify(before,null,2)+'\n'),e.baselineAuthoringSha256);assert(JSON.stringify(review).includes(e.baselineAuthoringSha256));
  for(const s of c.screensAfter)assert.deepEqual(s,data.screens.find(x=>x.id===s.id));
  assert.equal(e.unchangedReviewedPairs,data.screens.length-c.changedScreens.length);assert.equal(e.baselineHtmlReconstructedExactly,true);
 }else{assert.equal(review.verdict,'PASS');for(const suffix of ['story-data.json',e.slug+'.html'])assert(JSON.stringify(review).includes(sha(`collector-output/${e.slug}/${suffix}`)));}
 const counts=Object.fromEntries([['essential',1],['core',2],['deep',3]].map(([mode,level])=>[mode,data.screens.filter(s=>s.level<=level).length]));
 assert.deepEqual(counts,data.targetModes);assert.deepEqual(counts,e.counts);assert.equal(data.contentMode,'narrative');
 assert.equal(data.defaultLanguage,'ru');assert.equal(data.defaultTheme,'dark');assert.equal(data.defaultMode,'essential');
 const b=catalogue.books.find(b=>b.slug===e.slug);assert.equal(b.screenCount,data.screens.length);assert.deepEqual(b.title,data.title);assert.deepEqual(b.description,data.description);assert.deepEqual(b.readingMinutes,e.readingMinutesByLanguage.ru);
 assert(html.includes('const invalidSavedScreen ='));assert(html.includes("if (invalidSavedScreen) { state.mode = 'essential'"));assert(html.includes('BookSettings.connect('));
 if(e.slug==='the-hobbit'){assert(html.includes("sessionStorage.removeItem(storagePrefix + 'spoilerConsent')"));assert(!html.includes("sessionStorage.setItem(storagePrefix + 'spoilerConsent'"));assert(html.includes('memorySpoilerLevel = Math.min(memorySpoilerLevel, levels[mode]);'));assert(html.includes('Continue Deep — ending spoilers'));}
 if(e.rootSha256)assert.equal(sha(b.file),e.rootSha256);
 results.push({slug:e.slug,counts,rootSha256:sha(b.file),effectiveCorpusSha256:hash(JSON.stringify(embedded(html))),unchangedReviewedPairs:e.unchangedReviewedPairs,localizedPairIds:e.checkedScreens});
}
const base=JSON.parse(execFileSync('git',['show',`${receipt.baseMain}:books.json`],{encoding:'utf8'}));let untouched=0;
for(const b of base.books.filter(b=>!results.some(e=>e.slug===b.slug))){assert.deepEqual(catalogue.books.find(x=>x.slug===b.slug),b);assert.equal(sha(b.file),hash(execFileSync('git',['show',`${receipt.baseMain}:${b.file}`],{maxBuffer:10*1024*1024})));untouched++;}
assert.equal(untouched,46);assert.equal(catalogue.books.length,53);assert.equal(catalogue.books.reduce((s,b)=>s+b.screenCount,0),2206);assert.equal(results.reduce((s,e)=>s+e.counts.deep,0),274);
assert.equal(new Set(catalogue.books.map(b=>b.cover.motif)).size,53);
console.log(JSON.stringify({pass:true,accepted:results,untouchedReaders:untouched,books:53,screens:2206,acceptedPairs:274,findings:[]},null,2));

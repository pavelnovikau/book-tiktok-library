import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
const p='editorial-audit/2026-10-31/publisher-findings';
const json=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const sha=p=>hash(fs.readFileSync(p));
const embed=h=>JSON.parse(h.match(/<script id="book-tiktok-data" type="application\/json">\s*([\s\S]*?)<\/script>/)[1]);
const base='e0746dbcf39cce01cf9a75371b19559cd0310f27';
const git=file=>execFileSync('git',['show',base+':'+file],{maxBuffer:10*1024*1024});
const catalogue=json('books.json'),old=JSON.parse(git('books.json'));
const queue=json(`${p}/parent-release09-queue.json`),seal=json(`${p}/release-09-intake-seal.json`),receipt=json(`${p}/release-09.json`);
assert.equal(sha(`${p}/parent-release09-queue.json`),seal.queueSha256);
assert.deepEqual(queue.candidates.map(c=>c.slug),seal.candidateSlugs);
for(const item of json(`${p}/release-09-proof/intake.json`).copied)assert.equal(sha(item.path),item.sha256,item.path);
for(const row of json(`${p}/release-09-proof/reviewed-baseline-bindings.json`))assert(row.authoringReconstructedExactly&&row.htmlReconstructedExactly&&row.allAfterHashesMatch,row.slug);
const results=[];
for(const c of queue.candidates){
 const source=json(`collector-output/${c.slug}/story-data.json`),raw=embed(fs.readFileSync(`collector-output/${c.slug}/${c.slug}.html`,'utf8')),root=embed(fs.readFileSync(c.slug+'.html','utf8'));
 for(const key of ['ready','review','originalReview','closure'])if(c[key])assert.equal(sha(c[key]),c[key+'Sha256']);
 if(c.review){const r=json(c.review);assert.equal(r.verdict,'PASS');for(const f of ['story-data.json',c.slug+'.html'])assert(JSON.stringify(r).includes(sha(`collector-output/${c.slug}/${f}`)));}
 if(c.originalReview){const r=json(c.originalReview);assert(['EDIT','REQUIRES-FIXES'].includes(r.verdict));assert.equal(json(c.closure).originalReviewSha256,c.originalReviewSha256);}
 for(const[k,v]of Object.entries(source))if(!['media','modes'].includes(k))assert.deepEqual(raw[k],v,`${c.slug}/${k}`);
 const expected=structuredClone(raw);
 if(c.slug==='the-potent-self')expected.modes.essential.minutes.ru='4 минуты';
 if(c.slug==='the-giver'){
  const oldData=embed(git('the-giver.html').toString());assert.deepEqual(root.screens,oldData.screens);assert.deepEqual(root.sources,oldData.sources);
  const change=json(c.closure);assert.deepEqual(root.description,change.descriptionAfter);oldData.description=change.descriptionAfter;
  assert.deepEqual(root,oldData,'Giver only description changes');
 }else assert.deepEqual(root,expected,c.slug+' effective corpus, source maps, modes and media');
 const counts=Object.fromEntries([['essential',1],['core',2],['deep',3]].map(([m,l])=>[m,root.screens.filter(s=>s.level<=l).length]));
 if(c.counts)assert.deepEqual(counts,c.counts);
 const b=catalogue.books.find(b=>b.slug===c.slug);assert.equal(b.screenCount,root.screens.length);assert.deepEqual(b.title,root.title);assert.deepEqual(b.description,root.description);
 const accepted=receipt.acceptedCandidates.find(e=>e.slug===c.slug);assert.equal(sha(c.slug+'.html'),accepted.rootSha256);assert.equal(hash(JSON.stringify(root)),accepted.effectiveCorpusSha256);
 assert.deepEqual(b.readingMinutes,Object.fromEntries(Object.entries(root.modes).map(([m,v])=>[m,parseInt(v.minutes.ru)])));
 assert.equal(root.defaultMode,'essential');assert.equal(root.defaultLanguage,'ru');assert.equal(root.defaultTheme,'dark');
 if(c.kind!=='metadata-only-correction')assert(fs.readFileSync(c.slug+'.html','utf8').includes('release09InvalidSavedId'));
 results.push({slug:c.slug,counts,pairs:root.screens.length,sourceCount:root.sources.length,contentMode:root.contentMode,rootSha256:sha(c.slug+'.html'),effectiveCorpusSha256:hash(JSON.stringify(root))});
}
// The three corrected candidates keep all originally reviewed other prose.
for(const slug of ['flowers-for-algernon','the-wee-free-men']){
 const c=json(`${p}/${slug}-meaning-fix-closure.json`),d=json(`collector-output/${slug}/story-data.json`);
 const before=structuredClone(d),map=new Map(c.screensBefore.map(s=>[s.id,s]));before.screens=before.screens.map(s=>map.get(s.id)||s);before.sources=c.sourcesBefore;before.methodNote=c.methodNoteBefore;
 assert.equal(hash(JSON.stringify(before,null,2)+'\n'),c.beforeHashes[`collector-output/${slug}/story-data.json`]);
 for(const s of c.screensAfter)assert.deepEqual(d.screens.find(x=>x.id===s.id),s);
}
const nes=json('collector-output/the-neverending-story/story-data.json');const ids=nes.screens.map(s=>s.id);assert.equal(ids.indexOf('the-price')+1,ids.indexOf('acharis'));
const oldNes=structuredClone(nes);[oldNes.screens[ids.indexOf('the-price')],oldNes.screens[ids.indexOf('acharis')]]=[oldNes.screens[ids.indexOf('acharis')],oldNes.screens[ids.indexOf('the-price')]];
for(const l of [1,2])assert.deepEqual(nes.screens.filter(s=>s.level<=l),oldNes.screens.filter(s=>s.level<=l));
const changedRoots=new Set([...queue.candidates.map(c=>c.slug),'skin-in-the-game','mindfulness']);
let unchangedRoots=0,unchangedMetadata=0;
for(const b of old.books){
 if(!changedRoots.has(b.slug)){assert.equal(sha(b.file),hash(git(b.file)),b.file);unchangedRoots++;}
 if(!queue.candidates.some(c=>c.slug===b.slug)&&b.slug!=='awareness-through-movement'){assert.deepEqual(catalogue.books.find(x=>x.slug===b.slug),b);unchangedMetadata++;}
}
for(const slug of ['skin-in-the-game','mindfulness']){
 const prior=git(slug+'.html').toString(),current=fs.readFileSync(slug+'.html','utf8');assert.deepEqual(embed(prior),embed(current));assert(current.includes('const resumeRequiresDepth = remembered && remembered.level > levels[state.mode];'));
 const restored=current.replace(/^\s*const resumeRequiresDepth = remembered && remembered.level > levels\[state.mode\];\n/m,'').replace(": resumeRequiresDepth ? (state.language === 'ru' ? 'Продолжить: ' : 'Continue: ') + modeLabel(requiredMode(remembered.level)) : remembered ?",': remembered ?');
 assert.equal(restored,prior,slug+' only destination label code delta');
}
const aw=catalogue.books.find(b=>b.slug==='awareness-through-movement'),previousAw=old.books.find(b=>b.slug===aw.slug),awRestored=structuredClone(aw);delete awRestored.searchAliases;assert.deepEqual(awRestored,previousAw);assert.deepEqual(aw.searchAliases,['Сознавание через движение']);
assert.equal(unchangedRoots,47);assert.equal(unchangedMetadata,48);assert.equal(catalogue.books.length,58);assert.equal(catalogue.books.reduce((n,b)=>n+b.screenCount,0),2188);assert.equal(new Set(catalogue.books.map(b=>b.cover.motif)).size,58);
assert.equal(receipt.acceptedPairs,286);assert.equal(receipt.metadataOnlyPairsUnchanged,27);
for(const slug of ['mans-search-for-meaning','ubik','the-martian-chronicles','moondust'])assert(!catalogue.books.some(b=>b.slug===slug));
console.log(JSON.stringify({pass:true,accepted:results,unchangedRoots,unchangedMetadata,books:58,screens:2188,mainPairs:286,metadataPairsUnchanged:27,originalReviewsUnchanged:true,findings:[]},null,2));

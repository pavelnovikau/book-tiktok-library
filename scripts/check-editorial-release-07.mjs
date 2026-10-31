import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
const audit='editorial-audit/2026-10-31';
const json=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const hash=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const sha=p=>hash(fs.readFileSync(p));
const embedded=html=>{const a=[...html.matchAll(/<script id="book-tiktok-data" type="application\/json">\s*([\s\S]*?)<\/script>/g)];assert.equal(a.length,1);return JSON.parse(a[0][1]);};
const receipt=json(`${audit}/publisher-findings/release-07.json`), catalogue=json('books.json');
for (const entry of receipt.extraEvidenceBindings || []) assert.equal(sha(entry.path),entry.sha256);
const results=[];
for(const entry of receipt.acceptedCandidates){
 const {slug}=entry;
 for(const file of entry.files)assert.equal(sha(file.path),file.sha256,file.path);
 assert.equal(sha(entry.reviewPath),entry.reviewSha256);
 assert.equal(sha(entry.readyPath),entry.readySha256);
 const data=json(`collector-output/${slug}/story-data.json`), review=json(entry.reviewPath);
 const raw=embedded(fs.readFileSync(`collector-output/${slug}/${slug}.html`,'utf8'));
 const rootHtml=fs.readFileSync(`${slug}.html`,'utf8');
 assert.deepEqual(embedded(rootHtml),raw,`${slug}: whole effective corpus/sources/media/modes preserved`);
 for(const [key,value] of Object.entries(data))if(!['media','modes'].includes(key))assert.deepEqual(raw[key],value,`${slug}/${key}`);
 let inheritedPairs;
 if(entry.parentClosure){
  const c=json(entry.parentClosure);assert.equal(c.originalReviewSha256,entry.reviewSha256);
  assert.equal(review.verdict,'REQUIRES-FIXES');
  const before=structuredClone(data);
  if(c.screensBefore){
   const old=new Map(c.screensBefore.map(s=>[s.id,s]));before.screens=before.screens.map(s=>old.get(s.id)||s);before.sources=c.sourcesBefore;before.methodNote=c.methodNoteBefore;
   for(const screen of c.screensAfter)assert.deepEqual(screen,data.screens.find(s=>s.id===screen.id));
  }else if(slug==='thinking-fast-and-slow'){
   for(const finding of review.blockingFindings){const s=before.screens.find(s=>s.id===finding.screenId);for(const lang of ['ru','en']){
    assert(s.copy[lang].body.includes(finding.smallestFaithfulCorrection[lang]));
    s.copy[lang].body=s.copy[lang].body.replace(finding.smallestFaithfulCorrection[lang],finding.exactDefectiveWording[lang]);
   }}
  }else{
   assert.equal(slug,'thinking-in-systems');before.sources=before.sources.filter(s=>s.id!==6);
   for(const screen of before.screens)if(c.changedScreens.includes(screen.id))screen.sources=[4];
   for(const lang of ['ru','en'])before.methodNote[lang]=before.methodNote[lang].split(lang==='ru'?' Для примеров':' The rainfall-variability')[0];
  }
  const baseline=c.beforeHashes[`collector-output/${slug}/story-data.json`];
  assert.equal(hash(JSON.stringify(before,null,2)+'\n'),baseline,`${slug}: reconstruct the exact reviewed authoring`);
  assert(JSON.stringify(review).includes(baseline),`${slug}: baseline SHA bound in original independent review`);
  assert.equal(entry.findingAcceptance.length,c.findings.length,`${slug}: every required localized finding closed`);
  inheritedPairs=data.screens.length-c.changedScreens.length;
 }else{
  assert.equal(review.verdict,'PASS');
  const bindings=slug==='seeing-like-a-state'?Object.fromEntries(review.candidateAndReadyHashes.map(x=>[x.path,x.afterSha256])):review.hashVerification.after;
  for(const [file,h] of Object.entries(bindings))assert.equal(sha(file),h,file);
  inheritedPairs=data.screens.length;
 }
 const counts=Object.fromEntries([['essential',1],['core',2],['deep',3]].map(([mode,level])=>[mode,data.screens.filter(s=>s.level<=level).length]));
 assert.deepEqual(counts,data.targetModes);assert.deepEqual(counts,entry.counts);
 const book=catalogue.books.find(b=>b.slug===slug);assert.equal(book.screenCount,counts.deep);assert.deepEqual(book.title,data.title);assert.deepEqual(book.description,data.description);assert.deepEqual(book.readingMinutes,entry.readingMinutesByLanguage.ru);
 assert.equal(data.defaultLanguage,'ru');assert.equal(data.defaultTheme,'dark');assert.equal(data.defaultMode,'essential');assert(rootHtml.includes('const savedScreen ='));
 if(entry.legacyMigration)assert(rootHtml.includes(entry.legacyMigration+'.lastSlide')&&rootHtml.includes('legacyMigration07'));
 if(slug==='project-hail-mary')assert(rootHtml.includes('function allowEnding()')&&rootHtml.includes("if (mode !== 'deep') endingConsent = false;"));
 if(entry.rootSha256)assert.equal(sha(`${slug}.html`),entry.rootSha256);
 results.push({slug,counts,rootSha256:sha(`${slug}.html`),inheritedReviewedPairs:inheritedPairs,changedPairIds:entry.checkedScreens});
}
const base=jsonFromGit('books.json');
function git(file){return execFileSync('git',['show',`${receipt.baseMain}:${file}`],{maxBuffer:10*1024*1024});}
function jsonFromGit(file){return JSON.parse(git(file));}
const accepted=new Set(results.map(x=>x.slug));let unchanged=0;
for(const book of base.books.filter(b=>!accepted.has(b.slug))){assert.equal(sha(book.file),hash(git(book.file)),`${book.slug}: previous runtime preserved`);assert.deepEqual(catalogue.books.find(b=>b.slug===book.slug),book);unchanged++;}
assert.equal(unchanged,receipt.previousUnchangedReaders);
assert.equal(catalogue.books.length,receipt.catalogueBooks);assert.equal(catalogue.books.reduce((n,b)=>n+b.screenCount,0),receipt.catalogueScreens);assert.equal(results.reduce((n,e)=>n+e.counts.deep,0),receipt.acceptedPairs);
assert.equal(new Set(catalogue.books.map(b=>b.cover.motif)).size,catalogue.books.length);
console.log(JSON.stringify({pass:true,accepted:results,previousUnchangedReaders:unchanged,catalogueBooks:catalogue.books.length,catalogueScreens:receipt.catalogueScreens,findings:[]},null,2));

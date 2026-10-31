import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';

const review=path.dirname(fileURLToPath(import.meta.url)),dir=path.dirname(review);
const read=name=>fs.readFileSync(path.join(dir,name),'utf8');
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const data=JSON.parse(read('story-data.json')),html=read('hard-to-be-a-god.html');
const embedded=JSON.parse(html.match(/<script id="book-tiktok-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const {modes,...authored}=embedded;
assert.deepEqual(authored,data,'Authored JSON differs from the effective reader');
const strip=value=>value.replace(/<[^>]+>/g,' ').replace(/&(?:nbsp|amp|lt|gt|quot|#39);/gi,' ').replace(/\s+/g,' ').trim();
const count=value=>(strip(value).match(/[\p{L}\p{N}][\p{L}\p{N}'’\-–—]*/gu)||[]).length;
const normalize=value=>value.replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/\s+/g,' ').trim();
for(const lang of ['ru','en']){
  const draft=read(`draft-${lang}.md`).split(/^## /m).slice(1).map(section=>section.slice(section.indexOf('\n')+1).trim()).join(' ');
  const effective=data.screens.filter(s=>s.evidenceLocator).map(s=>s.copy[lang].body.replace(/<[^>]+>/g,' ')).join(' ');
  assert.equal(normalize(effective),normalize(draft),`Connected ${lang} draft and screens differ`);
}
const original=JSON.parse(read('root-review/input-story-data.json'));
assert.deepEqual(data.screens.map(s=>[s.id,s.level]),original.screens.map(s=>[s.id,s.level]));
const changed=data.screens.filter((s,i)=>JSON.stringify(s)!==JSON.stringify(original.screens[i])).map(s=>s.id);
assert.deepEqual(changed,['cover','deep-warning','drinking-night','aba-tsupik','condor-reversal','kira-window','final']);
const baseline=JSON.parse(read('protected-baseline.json'));
const protectedChecks=Object.entries(baseline).map(([file,expected])=>({file,expected,actual:hash(fs.readFileSync(file))}));
assert(protectedChecks.every(item=>item.expected===item.actual),'Protected historical files changed');
const primary='/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-4-private/hard-to-be-a-god.html';
assert.equal(hash(fs.readFileSync(primary)),'02ef0f659c7e11b1fe60a85fce2be24b68fbac61e47a7a85add49df70cdf900d');
const metrics={wordDefinition:'Unicode letter/number token, retaining internal apostrophes/hyphens/dashes; same regex as maintained builder',rates:{ru:180,en:220},depths:{}};
for(const [mode,level] of [['essential',1],['core',2],['deep',3]]){
  const selected=data.screens.filter(s=>s.level<=level),narrative=selected.filter(s=>s.evidenceLocator);
  const m={screens:selected.length,narrativeScreens:narrative.length,narrativeWords:{},titleSubtitleBodyWords:{},narrativeMinutes:{},builderCeilingMinutes:{}};
  for(const lang of ['ru','en']){
    m.narrativeWords[lang]=narrative.reduce((n,s)=>n+count(s.copy[lang].body),0);
    m.titleSubtitleBodyWords[lang]=selected.reduce((n,s)=>n+count(`${s.copy[lang].title} ${s.copy[lang].subtitle||''} ${s.copy[lang].body||''}`),0);
    m.narrativeMinutes[lang]=Number((m.narrativeWords[lang]/metrics.rates[lang]).toFixed(2));
    m.builderCeilingMinutes[lang]=Math.ceil(m.titleSubtitleBodyWords[lang]/metrics.rates[lang]);
    assert.equal(Number.parseInt(modes[mode].minutes[lang],10),m.builderCeilingMinutes[lang]);
  }
  metrics.depths[mode]=m;
}
assert.deepEqual(Object.values(metrics.depths).map(m=>m.screens),[19,47,94]);
fs.writeFileSync(path.join(dir,'metrics.json'),JSON.stringify(metrics,null,2)+'\n');
const result={atUtc:new Date().toISOString(),jsonSha256:hash(read('story-data.json')),htmlSha256:hash(html),authoredEmbeddedParity:true,connectedDraftsMatch:true,stableIdsAndLevels:true,changedPairs:changed,protectedChecks,primaryWitnessSha256:hash(fs.readFileSync(primary)),metrics};
fs.mkdirSync(path.join(review,'qa'),{recursive:true});
fs.writeFileSync(path.join(review,'qa/content-verification.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:'PASS',hashes:{json:result.jsonSha256,html:result.htmlSha256},deep:metrics.depths.deep,protectedFiles:protectedChecks.length}));

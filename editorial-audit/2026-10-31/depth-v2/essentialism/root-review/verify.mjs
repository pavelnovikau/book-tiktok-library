import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
const dir=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const read=n=>fs.readFileSync(path.join(dir,n),'utf8');
const hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const qa=path.join(dir,'root-review/qa');fs.mkdirSync(qa,{recursive:true});
const d=JSON.parse(read('story-data.json')),h=read('essentialism.html');
const embedded=JSON.parse(h.match(/<script[^>]*id="book-tiktok-data"[^>]*>([\s\S]*?)<\/script>/)[1]);
for(const[key,value]of Object.entries(d))if(key!=='modes')assert.deepEqual(embedded[key],value,'embedded '+key);
for(const mode of Object.keys(d.modes))assert.deepEqual(embedded.modes[mode].minutes,d.modes[mode].minutes);
const decode=t=>t.replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&#x27;|&#39;/g,"'").replace(/&quot;/g,'"').replace(/&nbsp;/g,' ');
const strip=t=>decode(String(t).replace(/<[^>]+>/g,' ')).replace(/\s+/g,' ').trim();
const words=t=>(strip(t).match(/[\p{L}\p{N}][\p{L}\p{N}'’\-–—]*/gu)||[]).length;
const metrics={wordMethod:'Unicode builder tokens. Noncover body excludes titles, subtitles, section labels, UI and source notes; includes the shared final. Main body excludes that final too. Display estimate adds cover and headings.',rates:{ru:180,en:220},modes:{},density:{},parity:{},hashes:{json:hash(path.join(dir,'story-data.json')),html:hash(path.join(dir,'essentialism.html'))}};
let previous=[];
for(const[mode,level]of[['essential',1],['core',2],['deep',3]]){
 const list=d.screens.filter(s=>s.level<=level),ids=list.map(s=>s.id);
 assert.equal(list.length,d.targetModes[mode]);assert.deepEqual(ids.filter(id=>previous.includes(id)),previous,'ordered nesting');previous=ids;
 metrics.modes[mode]={screens:list.length,ids};
 for(const lang of['ru','en']){
  const total=(xs,fn)=>xs.reduce((n,s)=>n+words(fn(s.copy[lang])),0);
  const noncover=list.filter(s=>s.type!=='cover'),main=noncover.filter(s=>!s.final),final=noncover.filter(s=>s.final),cover=list.filter(s=>s.type==='cover');
  const bodyWords=total(noncover,c=>c.body),mainBodyWords=total(main,c=>c.body),sharedFinalBodyWords=total(final,c=>c.body);
  const coverBodyWords=total(cover,c=>c.body),titleWords=total(list,c=>c.title),subtitleWords=total(list,c=>c.subtitle||''),sectionWords=total(list,c=>c.section||'');
  const displayWords=bodyWords+coverBodyWords+titleWords+subtitleWords,rate=metrics.rates[lang],minutes=Math.ceil(displayWords/rate);
  assert.equal(parseInt(embedded.modes[mode].minutes[lang]),minutes,'UI estimate '+mode+'/'+lang);
  metrics.modes[mode][lang]={bodyWords,mainBodyWords,sharedFinalBodyWords,coverBodyWords,titleWords,subtitleWords,sectionWords,bodyMinutes:Number((bodyWords/rate).toFixed(4)),displayWords,displayedCeilingMinutes:minutes,displayedLabel:embedded.modes[mode].minutes[lang]};
  const out=['# '+d.title[lang]+' — '+mode,''];
  for(const s of noncover)out.push('## '+s.id+' — '+s.copy[lang].title,'',decode(s.copy[lang].body.replaceAll('<p>','').replaceAll('</p>','\n\n')).trim(),'');
  assert.equal(read(mode+'.'+lang+'.md'),out.join('\n'),'complete exact route '+mode+'/'+lang);
 }
}
for(const lang of['ru','en']){
 const ps=read('draft-'+lang+'.md').split(/\n## /).slice(1).flatMap(c=>c.slice(c.indexOf('\n\n')+2).trim().split('\n\n'));
 const actual=d.screens.filter(s=>s.type!=='cover').flatMap(s=>[...s.copy[lang].body.matchAll(/<p>([\s\S]*?)<\/p>/g)].map(m=>decode(m[1])));
 assert.deepEqual(actual,ps,'exact connected draft '+lang);assert.equal(ps.length,125);
 metrics.parity[lang]={paragraphs:ps.length,exactInOrder:true};
 const density=d.screens.filter(s=>s.type!=='cover'&&!s.final).map(s=>words(s.copy[lang].body)).sort((a,b)=>a-b),n=density.length;
 metrics.density[lang]={screens:n,min:density[0],max:density.at(-1),median:n%2?density[(n-1)/2]:(density[n/2-1]+density[n/2])/2,mean:Number((density.reduce((a,b)=>a+b,0)/n).toFixed(3))};
}
const old=JSON.parse(read('root-review/input-story-data.json')),repairs=JSON.parse(read('root-review/repairs.json')),ledger=JSON.parse(read('root-review/reading-ledger.json'));
const changed=d.screens.filter((s,i)=>JSON.stringify(s.copy)!==JSON.stringify(old.screens[i].copy)).map(s=>s.id).sort();
assert.deepEqual(changed,[...new Set(repairs.map(r=>r.screen))].sort(),'exact authorized copy repairs');
for(const key of Object.keys(old))if(!['screens','methodNote','modes','unitMap'].includes(key))assert.deepEqual(d[key],old[key],'stable metadata '+key);
for(const s of d.screens){
 const before=old.screens.find(x=>x.id===s.id);assert.equal(s.level,before.level);
 if(!['identity','identity-2','identity-3'].includes(s.id))assert.deepEqual(s.sourceLocators,before.sourceLocators,'unchanged source locators '+s.id);
}
assert.equal(d.unitMap.length,47);assert.deepEqual(JSON.parse(read('coverage-map.json')),d.unitMap);
assert.equal(new Set(ledger.screenDisplays.flatMap(x=>x.ids)).size,125);
assert.equal(new Set(ledger.routeDisplays.flatMap(x=>x.ids)).size,49);
assert.equal(new Set(ledger.coreAdditionDisplays.flatMap(x=>x.ids)).size,59);
assert.deepEqual([...new Set(ledger.changedDisplays.flatMap(x=>x.ids))].sort(),changed);
const source=JSON.parse(fs.readFileSync('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-8-private/essentialism-edition.json','utf8'));
for(const unit of d.unitMap)for(const r of unit.primaryRanges){const file=source.find(x=>x.file===r.file);assert(file&&r.start>=1&&r.end>=r.start&&r.end<=file.paragraphs.length,'source range '+unit.id);}
const protectedInputs=JSON.parse(read('root-review/qa-protected-baseline.json'));
for(const[p,before]of Object.entries(protectedInputs))assert.equal(hash(p),before,'protected input '+p);
assert(!/<(?:script|link)[^>]+(?:src|href)=["']https?:/i.test(h));
assert(!/\b(?:fetch|XMLHttpRequest|WebSocket|EventSource)\s*\(/.test(h));
const audit=spawnSync(process.execPath,['/Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs',path.join(dir,'essentialism.html'),'--min-screens','125','--require-bilingual'],{encoding:'utf8'});
fs.writeFileSync(path.join(qa,'structural-audit.json'),audit.stdout);assert.equal(audit.status,0,audit.stderr);
const report={atUtc:new Date().toISOString(),status:'PASS',allAuthoredFieldsMatchEmbedding:true,modesOnlyEnrichedWithMaintainedLabels:true,draftParagraphs:metrics.parity,allSixRoutesExact:true,changedPairIds:changed,counts:d.targetModes,protectedInputs:Object.keys(protectedInputs).length,rootWholePrimaryContinuouslyRead:false,rootPersonalAcceptance:false,publicationAllowed:false,contentHashes:Object.fromEntries(['story-data.json','essentialism.html','draft-ru.md','draft-en.md','coverage-map.json'].map(n=>[n,hash(path.join(dir,n))]))};
fs.writeFileSync(path.join(qa,'metrics.json'),JSON.stringify(metrics,null,2)+'\n');
fs.writeFileSync(path.join(qa,'parity-check.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({counts:d.targetModes,changedPairs:changed.length,protectedInputs:report.protectedInputs,bodyWords:Object.fromEntries(Object.entries(metrics.modes).map(([m,v])=>[m,{ru:v.ru.bodyWords,en:v.en.bodyWords,uiRu:v.ru.displayedLabel,uiEn:v.en.displayedLabel}]))}));

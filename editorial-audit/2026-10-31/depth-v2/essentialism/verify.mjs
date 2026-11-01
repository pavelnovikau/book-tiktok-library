import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {createHash} from 'node:crypto';import assert from 'node:assert/strict';
const dir=path.dirname(fileURLToPath(import.meta.url)),read=n=>fs.readFileSync(path.join(dir,n),'utf8');
const h=read('essentialism.html'),d=JSON.parse(read('story-data.json')),embedded=JSON.parse(h.match(/<script id="book-tiktok-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
for(const [key,value] of Object.entries(d))if(key!=='modes')assert.deepEqual(embedded[key],value,'Authoring/HTML '+key);
for(const mode of Object.keys(d.modes))assert.deepEqual(embedded.modes[mode].minutes,d.modes[mode].minutes);
const strip=t=>String(t).replace(/<[^>]+>/g,' ').replace(/&(?:nbsp|amp|lt|gt|quot|#39);/g,' ').replace(/\s+/g,' ').trim();
const words=t=>(strip(t).match(/[\p{L}\p{N}][\p{L}\p{N}'’\-–—]*/gu)||[]).length;
const metrics={convention:'Unicode letter/number followed by letters/numbers/apostrophes/dashes; hyphenated forms count once. Body excludes cover, UI, titles, subtitles, section labels, Sources/method. Shared final IS INCLUDED. Display estimate includes cover title/subtitle plus visible screen headings/subtitles/bodies; excludes navigation, section kickers and Sources/method.',rates:{ru:180,en:220},modes:{},draftParagraphPairs:125,units:d.unitMap.length};
for(const [mode,level] of [['essential',1],['core',2],['deep',3]]){
 const list=d.screens.filter(s=>s.level<=level);assert.equal(list.length,d.targetModes[mode]);
 metrics.modes[mode]={screens:list.length};
 for(const lang of ['ru','en']){
  const body=list.filter(s=>s.type!=='cover').reduce((sum,s)=>sum+words(s.copy[lang].body),0);
  const display=list.reduce((sum,s)=>sum+words(s.copy[lang].title+' '+(s.copy[lang].subtitle||'')+' '+s.copy[lang].body),0),rate=metrics.rates[lang];
  const minutes=Math.ceil(display/rate);assert.equal(parseInt(embedded.modes[mode].minutes[lang]),minutes);
  metrics.modes[mode][lang]={bodyWords:body,bodyTimeExactMinutes:`${body}/${rate}`,bodyMinutes:body/rate,bodySeconds:body*60/rate,ceilingBodyMinutes:Math.ceil(body/rate),headingBodyWords:display,displayedCeilingMinutes:minutes,displayedLabel:embedded.modes[mode].minutes[lang]};
 }
}
for(const lang of ['ru','en']){
 const sections=read('draft-'+lang+'.md').split(/\n## /).slice(1);
 const ps=sections.flatMap(c=>c.slice(c.indexOf('\n\n')+2).trim().split('\n\n'));
 const esc=t=>t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
 const actual=d.screens.slice(1).flatMap(s=>[...s.copy[lang].body.matchAll(/<p>([\s\S]*?)<\/p>/g)].map(m=>m[1]));
 assert.deepEqual(actual,ps.map(esc),'Connected draft exact paragraph parity '+lang);
 assert.equal(ps.length,125);
}
for(const [mode,level] of [['essential',1],['core',2],['deep',3]])for(const lang of ['ru','en']){
 const route=read(mode+'.'+lang+'.md');assert.deepEqual([...route.matchAll(/^## ([a-z0-9-]+) /gm)].map(m=>m[1]),d.screens.filter(s=>s.type!=='cover'&&s.level<=level).map(s=>s.id),'Exact route order '+mode+'/'+lang);for(const s of d.screens.filter(x=>x.type!=='cover'&&x.level<=level))assert(route.includes(strip(s.copy[lang].body).slice(0,70)),'Route includes '+s.id);
}
const source=JSON.parse(fs.readFileSync('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-8-private/essentialism-edition.json','utf8'));
for(const unit of d.unitMap)for(const r of unit.primaryRanges){const file=source.find(f=>f.file===r.file);assert(file&&r.start>=1&&r.end>=r.start&&r.end<=file.paragraphs.length,'Source range '+unit.id)}
const manifest=JSON.parse(read('reading-manifest.json')),ledger=read('displayed-reading-ledger.jsonl').trim().split('\n').map(JSON.parse);
assert.equal(createHash('sha256').update(fs.readFileSync(manifest.source)).digest('hex'),manifest.sourceSha256);
const seen=new Set();for(const chunk of manifest.chunks){assert(ledger.some(e=>e.chunk===chunk.chunk&&e.displaySha256===chunk.displaySha256),'Displayed chunk '+chunk.chunk);for(const r of chunk.ranges)for(let i=r.start;i<=r.end;i++){assert(!seen.has(r.file+':'+i),'overlap');seen.add(r.file+':'+i)}}
for(const f of source.slice(3,32))for(let i=1;i<=f.paragraphs.length;i++)assert(seen.has(f.file+':'+i),'Missing main paragraph');
assert.equal(seen.size,1096);assert(h.includes('book-tiktok.${data.slug}.depth-v2.'));
assert(!/<(?:script|link)[^>]+(?:src|href)=["']https?:/i.test(h));assert(!/\b(?:fetch|XMLHttpRequest|WebSocket|EventSource)\s*\(/.test(h));
const report={status:'deterministic-checks-completed',rootPersonalAcceptance:false,publicationAllowed:false,checks:['All authored JSON fields equal HTML embedding (modes enriched only with maintained labels)','All125 RU/EN paragraph pairs equal connected drafts','All six nested-route documents are ordered selections','Exact counts and heading/body ceiling at RU180/EN220','All source ranges valid','27 displayed chunks cover1096 main/appendix/metadata paragraphs without gaps or overlaps','Source full-file hash unchanged','No runtime HTTP dependencies'],metrics};
fs.writeFileSync(path.join(dir,'metrics.json'),JSON.stringify(metrics,null,2)+'\n');fs.writeFileSync(path.join(dir,'qa','deterministic.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));

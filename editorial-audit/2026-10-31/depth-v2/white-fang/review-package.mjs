import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {createHash} from 'node:crypto';
const H=path.dirname(fileURLToPath(import.meta.url));const d=JSON.parse(fs.readFileSync(path.join(H,'story-data.json')));
const html=fs.readFileSync(path.join(H,'white-fang.html'),'utf8');const e=JSON.parse(html.match(/<script id="book-tiktok-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const norm=x=>x.replace(/<[^>]*>/g,' ').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/\s+/g,' ').trim();const words=x=>(norm(x).match(/[\p{L}\p{N}][\p{L}\p{N}'’\-–—]*/gu)||[]).length;
const assert=(x,m)=>{if(!x)throw Error(m)};assert(JSON.stringify(d.screens)===JSON.stringify(e.screens),'embedded screen parity');
const checks=[];const rates={ru:180,en:220};const metrics={wordDefinition:"Unicode letter/number token retaining internal apostrophes, hyphens and dashes; maintained-builder regex",rates,depths:{}};
fs.mkdirSync(path.join(H,'routes'),{recursive:true});
for(const [m,l] of Object.entries({essential:1,core:2,deep:3})){
 const ss=d.screens.filter(s=>s.level<=l);const row={screens:ss.length,narrativeScreens:ss.filter(s=>s.narrative).length,narrativeWords:{},framingBodyWords:{},headingSubtitleWords:{},sectionLabelWords:{},sectionLabelMinutes:{},builderTotalWords:{},narrativeMinutes:{},framingHeadingMinutes:{},builderCeilingMinutes:{}};
 for(const lang of ['ru','en']){
  row.narrativeWords[lang]=ss.filter(s=>s.narrative).reduce((a,s)=>a+words(s.copy[lang].body),0);
  row.framingBodyWords[lang]=ss.filter(s=>!s.narrative).reduce((a,s)=>a+words(s.copy[lang].body),0);
  row.headingSubtitleWords[lang]=ss.reduce((a,s)=>a+words(s.copy[lang].title)+words(s.copy[lang].subtitle||''),0);
  row.sectionLabelWords[lang]=ss.reduce((a,s)=>a+words(s.copy[lang].section),0);
  row.sectionLabelMinutes[lang]=+(row.sectionLabelWords[lang]/rates[lang]).toFixed(2);
  row.builderTotalWords[lang]=row.narrativeWords[lang]+row.framingBodyWords[lang]+row.headingSubtitleWords[lang];
  row.narrativeMinutes[lang]=+(row.narrativeWords[lang]/rates[lang]).toFixed(2);
  row.framingHeadingMinutes[lang]=+((row.framingBodyWords[lang]+row.headingSubtitleWords[lang])/rates[lang]).toFixed(2);
  row.builderCeilingMinutes[lang]=Math.ceil(row.builderTotalWords[lang]/rates[lang]);
  const route=ss.map(s=>`## ${s.copy[lang].title}\n\n${norm(s.copy[lang].body)}`).join('\n\n');
  fs.writeFileSync(path.join(H,'routes',`${m}-${lang}.md`),`# ${d.title[lang]} — ${m}\n\n${route}\n`);
 }
 metrics.depths[m]=row;
}
for(const lang of ['ru','en']){
 const sections=fs.readFileSync(path.join(H,`draft-${lang}.md`),'utf8').split('\n## ').slice(1);const ps=sections.flatMap(s=>s.trim().split('\n\n').slice(1));const actual=d.screens.filter(s=>s.narrative).map(s=>norm(s.copy[lang].body));
 assert(ps.length===86&&JSON.stringify(ps.map(norm))===JSON.stringify(actual),'full paragraph parity '+lang);checks.push({language:lang,paragraphs:ps.length,exactDraftDataHtmlParity:true});
}
for(const lower of [1,2]){const r=d.screens.filter(s=>s.level<=lower);assert(r.at(-2).id==='iv-3-p4','short route stop');assert(!r.some(s=>s.id.startsWith('v-')||s.id.startsWith('iv-4')),'ending in shallow route')}
assert(d.screens.at(-2).id==='v-5-p6','true final image');
assert(d.screens.findIndex(s=>s.id==='deep-warning')+1===d.screens.findIndex(s=>s.id==='iv-4-p1'),'warning position');
const paragraphCounts=d.screens.map(s=>({id:s.id,ru:(s.copy.ru.body.match(/<p>/g)||[]).length,en:(s.copy.en.body.match(/<p>/g)||[]).length}));assert(paragraphCounts.every(r=>r.ru===r.en),'actual paragraph parity');
const narrative=d.screens.filter(s=>s.narrative);metrics.density={ru:{min:Math.min(...narrative.map(s=>words(s.copy.ru.body))),max:Math.max(...narrative.map(s=>words(s.copy.ru.body)))},en:{min:Math.min(...narrative.map(s=>words(s.copy.en.body))),max:Math.max(...narrative.map(s=>words(s.copy.en.body)))}};
fs.writeFileSync(path.join(H,'metrics.json'),JSON.stringify(metrics,null,2)+'\n');
fs.writeFileSync(path.join(H,'qa','structural-parity.json'),JSON.stringify({inputHashes:Object.fromEntries(['story-data.json','white-fang.html','draft-ru.md','draft-en.md'].map(f=>[f,createHash('sha256').update(fs.readFileSync(path.join(H,f))).digest('hex')])),checks,paragraphCounts,embeddedScreenParity:true,nestedRoutes:true,shortRouteStop:'iv-3-p4',ending:'v-5-p6',warningPrecedesOutcome:true},null,2)+'\n');
console.log(JSON.stringify(metrics,null,2));

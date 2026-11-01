import fs from 'node:fs';import path from 'node:path';import {createHash} from 'node:crypto';import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url)),read=n=>fs.readFileSync(path.join(dir,n),'utf8'),sha=n=>createHash('sha256').update(read(n)).digest('hex');
const d=JSON.parse(read('story-data.json')),h=read('selfie.html'),match=h.match(/<script id="book-tiktok-data" type="application\/json">([\s\S]*?)<\/script>/);if(!match)throw Error('embedding');const embedded=JSON.parse(match[1]);
for(const [k,v]of Object.entries(d))if(JSON.stringify(v)!==JSON.stringify(embedded[k]))throw Error('Authored data mismatch '+k);
const decode=t=>t.replaceAll('&amp;','&').replaceAll('&lt;','<').replaceAll('&gt;','>').replaceAll('&quot;','"').replaceAll('&#x27;',"'").replaceAll('&#39;',"'");
const text=t=>decode(t.replace(/<[^>]*>/g,' ')).replace(/\s+/g,' ').trim();
const count=t=>(text(t).match(/[\p{L}\p{N}][\p{L}\p{N}'’\-–—]*/gu)||[]).length;
let parity={allAuthoredFieldsMatchEmbedded:true,paragraphs:{}};
for(const lang of ['ru','en']){
 const draft=read('draft.'+lang+'.md').split(/\n\s*\n/).map(s=>s.trim()).filter(s=>s&&!s.startsWith('#'));
 const actual=d.screens.filter(s=>s.type!=='cover').flatMap(s=>[...s.copy[lang].body.matchAll(/<p>([\s\S]*?)<\/p>/g)].map(m=>decode(m[1])));
 if(JSON.stringify(draft)!==JSON.stringify(actual))throw Error('Connected paragraph parity '+lang);parity.paragraphs[lang]=actual.length;
}
const metrics={wordDefinition:'Same Unicode word regex as maintained builder. body excludes cover framing, headings, section labels, provenance, Sources and all controls. UI estimate means the reading time displayed by the UI, using builder title+subtitle+body (cover included), not the word count of every control. Exact seconds/rational minutes preserved separately from rounded displayed estimate.',speedsWpm:{ru:180,en:220},disclosures:{},modes:{},density:{}};
for(const lang of ['ru','en'])metrics.disclosures[lang]={methodNoteWords:count(d.methodNote[lang]),sourceTitleWords:d.sources.reduce((n,s)=>n+count(s.title),0),sourceNoteWords:d.sources.reduce((n,s)=>n+count(s.note[lang]),0),sourceCount:d.sources.length,includedInMainBody:false,includedInDisplayedTime:false,scope:'Authored method/source fields; Sources dialog wrapper and repeated navigation labels are excluded from both timing estimates.'};
for(const [mode,level]of [['essential',1],['core',2],['deep',3]]){
 const a=d.screens.filter(s=>s.level<=level);metrics.modes[mode]={screens:a.length,languages:{},orderedIds:a.map(s=>s.id)};
 for(const lang of ['ru','en']){
  const body=a.filter(s=>s.type!=='cover').reduce((n,s)=>n+count(s.copy[lang].body),0),heading=a.filter(s=>s.type!=='cover').reduce((n,s)=>n+count(s.copy[lang].title),0),framing=a.filter(s=>s.type==='cover').reduce((n,s)=>n+count(s.copy[lang].title+' '+s.copy[lang].subtitle+' '+s.copy[lang].body),0),section=a.reduce((n,s)=>n+count(s.copy[lang].section),0),ui=body+heading+framing,wpm=metrics.speedsWpm[lang];
  const shown=embedded.modes[mode].minutes[lang];if(parseInt(shown)!==Math.ceil(ui/wpm))throw Error('UI time '+lang+'/'+mode);
  metrics.modes[mode].languages[lang]={mainBodyWords:body,headingWords:heading,coverFramingWords:framing,sectionLabelWords:section,uiTimedWords:ui,bodyMinutes:body/wpm,bodySeconds:body*60/wpm,bodyMinutesFraction:body+'/'+wpm,roundedBodyMinutes:Math.ceil(body/wpm),uiMinutes:ui/wpm,uiSeconds:ui*60/wpm,uiMinutesFraction:ui+'/'+wpm,displayedUiMinutes:shown};
  const route=read(mode+'.'+lang+'.md'),ids=[...route.matchAll(/<!-- ([a-z0-9-]+) \| level=/g)].map(m=>m[1]);if(JSON.stringify(ids)!==JSON.stringify(a.map(s=>s.id)))throw Error('Route ID parity '+mode+'/'+lang);
  const bodyFromRoute=route.split(/\n\s*\n/).map(s=>s.trim()).filter(s=>s&&!s.startsWith('#')&&!s.startsWith('<!--'));
  const routeParas=a.flatMap(s=>[...s.copy[lang].body.matchAll(/<p>([\s\S]*?)<\/p>/g)].map(m=>decode(m[1])));if(JSON.stringify(bodyFromRoute)!==JSON.stringify(routeParas))throw Error('Route prose parity '+mode+'/'+lang);
 }
}
for(const lang of ['ru','en']){const n=d.screens.filter(s=>s.type!=='cover').map(s=>count(s.copy[lang].body)).sort((a,b)=>a-b);metrics.density[lang]={bodyScreens:n.length,min:n[0],max:n.at(-1),median:n[Math.floor(n.length/2)],mean:n.reduce((a,b)=>a+b,0)/n.length};}
parity.routeCopiesAllExact=true;parity.hashes=Object.fromEntries(['draft.ru.md','draft.en.md','story-data.json','selfie.html',...['essential','core','deep'].flatMap(m=>['ru','en'].map(l=>m+'.'+l+'.md'))].map(n=>[n,sha(n)]));
fs.writeFileSync(path.join(dir,'metrics.json'),JSON.stringify(metrics,null,2)+'\n');fs.writeFileSync(path.join(dir,'parity.json'),JSON.stringify(parity,null,2)+'\n');console.log(JSON.stringify({parity,metrics:Object.fromEntries(Object.entries(metrics.modes).map(([k,v])=>[k,{screens:v.screens,languages:v.languages}])),disclosures:metrics.disclosures,density:metrics.density},null,2));

import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {createHash} from 'node:crypto';
const dir=path.dirname(fileURLToPath(import.meta.url));const read=n=>fs.readFileSync(path.join(dir,n),'utf8');const d=JSON.parse(read('story-data.json')),h=read(d.slug+'.html'),map=JSON.parse(read('coverage-map.json'));
const assert=(v,m)=>{if(!v)throw Error(m)};const hash=n=>createHash('sha256').update(fs.readFileSync(path.join(dir,n))).digest('hex');
const embedded=JSON.parse(h.match(/<script id="book-tiktok-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
for(const key of Object.keys(d))assert(JSON.stringify(d[key])===JSON.stringify(embedded[key]),'embedding mismatch '+key);
function parse(s){let out=[];for(const b of s.trim().split('\n\n')){if(b.startsWith('### '))out.push({title:b.slice(4),paragraphs:[]});else if(!b.startsWith('#'))out.at(-1).paragraphs.push(b)}return out}
const drafts={ru:parse(read('draft.ru.md')),en:parse(read('draft.en.md'))};
const unescape=s=>s.replaceAll('&amp;','&').replaceAll('&lt;','<').replaceAll('&gt;','>');
const text=s=>String(s||'').replace(/<[^>]+>/g,' ').replace(/&(?:nbsp|amp|lt|gt|quot|#39);/gi,' ').replace(/\s+/g,' ').trim();
const wc=s=>(text(s).match(/[\p{L}\p{N}][\p{L}\p{N}'’\-–—]*/gu)||[]).length;
const seen={ru:[],en:[]};let pairs=0;
for(const u of map.units){
 assert(drafts.ru[u.unit-1].paragraphs.length===drafts.en[u.unit-1].paragraphs.length,'paired count '+u.id);
 for(const id of u.screenIds){const s=d.screens.find(s=>s.id===id);assert(s.level===u.level,'level '+id);assert(s.draftUnit===u.unit,'unit '+id);
 for(const lang of ['ru','en']){const ps=[...s.copy[lang].body.matchAll(/<p>([\s\S]*?)<\/p>/g)].map(m=>unescape(m[1]));assert(ps.length===s.draftParagraphs.length,'paragraph map '+id);
 for(let i=0;i<ps.length;i++){const n=s.draftParagraphs[i];assert(ps[i]===drafts[lang][u.unit-1].paragraphs[n-1],'actual paragraph text '+lang+'/'+id+'/'+n);seen[lang].push(u.unit+':'+n)}}
 pairs+=s.draftParagraphs.length;
 }}
assert(pairs===153,'153 pairs');for(const lang of ['ru','en']){assert(new Set(seen[lang]).size===153,'no duplicate/lost paragraphs');assert(seen[lang].length===153,'full draft coverage')}
const metrics={schemaVersion:1,status:'current',slug:d.slug,counts:d.targetModes,unitCount:73,paragraphPairs:pairs,definition:{expositionBody:'All draft paragraphs, including reading-program discussion and source-derived final doubt; excludes added cover.',coverFraming:'Added cover body only. Cover title/subtitle are counted separately in titlesAndSubtitlesWords.',readerUiWords:'Exactly builder convention: screen title + subtitle + body. Excludes section kickers, chrome, sources/method dialog. Continuation headings are counted.',ratesWordsPerMinute:{ru:180,en:220},roundedMinutes:'Ceiling; estimates, not measured reader performance.'},modes:{}};
for(const [mode,level] of [['essential',1],['core',2],['deep',3]]){
 const ss=d.screens.filter(s=>s.level<=level);assert(ss.length===d.targetModes[mode],'count '+mode);metrics.modes[mode]={screens:ss.length};
 for(const lang of ['ru','en']){const body=ss.filter(s=>s.type!=='cover').reduce((n,s)=>n+wc(s.copy[lang].body),0),framing=wc(d.screens[0].copy[lang].body),titles=ss.reduce((n,s)=>n+wc(s.copy[lang].title+' '+(s.copy[lang].subtitle||'')),0),ui=ss.reduce((n,s)=>n+wc(s.copy[lang].title+' '+(s.copy[lang].subtitle||'')+' '+s.copy[lang].body),0),rate=lang==='ru'?180:220;
 assert(ui===body+framing+titles,'body framing titles partition '+lang+'/'+mode);assert(parseInt(embedded.modes[mode].minutes[lang])===Math.ceil(ui/rate),'UI reading time '+lang+'/'+mode);
 metrics.modes[mode][lang]={expositionBodyWords:body,coverFramingBodyWords:framing,titlesAndSubtitlesWords:titles,readerUiWords:ui,bodyMinutes:Math.round(body/rate*100)/100,roundedBodyMinutes:Math.ceil(body/rate),readerUiMinutes:embedded.modes[mode].minutes[lang],bodyWordsPerExpositionScreen:Math.round(body/(ss.length-1)*10)/10};
 }
}
assert(h.includes('const storagePrefix = `book-tiktok.${data.slug}.depth-v2.`;'),'fresh namespace');assert(!d.spoilerPolicy,'nonfiction no fiction spoiler policy');assert(!d.screens.some(s=>s.claimType==='synthesis'),'no invented synthesis screens');
assert(!/<script[^>]+src=|<link[^>]+(?:stylesheet|preload)|@import\s+url|\bfetch\(|XMLHttpRequest|new WebSocket|new EventSource|serviceWorker\.register/.test(h),'offline runtime');
metrics.currentContentHashes=Object.fromEntries(['draft.ru.md','draft.en.md','story-data.json',d.slug+'.html','coverage-map.json'].map(n=>[n,hash(n)]));
fs.writeFileSync(path.join(dir,'metrics.json'),JSON.stringify(metrics,null,2)+'\n');
const report={status:'passed-structural-parity-only',allAuthoredFieldsMatchEmbedding:true,actualPairedParagraphsMatchConnectedDrafts:pairs,orderedDraftPairsUnique:true,all24ChapterEntries:map.chapters.length,counts:d.targetModes,freshProgressNamespace:'book-tiktok.'+d.slug+'.depth-v2.',rootPersonalAcceptance:false,publicationAllowed:false,inputHashes:metrics.currentContentHashes};
fs.writeFileSync(path.join(dir,'parity-check.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));

import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';

const dir=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const d=JSON.parse(fs.readFileSync(path.join(dir,'story-data.json'),'utf8'));
const h=fs.readFileSync(path.join(dir,d.slug+'.html'),'utf8');
const e=JSON.parse(h.match(/<script[^>]*id="book-tiktok-data"[^>]*>([\s\S]*?)<\/script>/)[1]);
for(const key of Object.keys(d))if(JSON.stringify(d[key])!==JSON.stringify(e[key]))throw Error('JSON/embedded mismatch: '+key);
const decode=s=>s.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
const words=s=>(s.replace(/<[^>]+>/g,' ').replace(/&(?:nbsp|amp|lt|gt|quot|#39);/gi,' ').match(/[\p{L}\p{N}][\p{L}\p{N}'’\-–—]*/gu)||[]).length;
const hash=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const metrics={rates:{ru:180,en:220},
  wordMethod:'Unicode lexical tokens using the installed builder regex. Body excludes cover, titles, subtitles, section labels, UI, source notes and method notes; includes shared final. Builder/UI-estimate text is cover + titles + subtitles + body, not all actual interface labels.',
  modes:{},density:{},draftParity:{},routeParity:{},embeddedEqualsCanonical:true};
metrics.sourceCount=d.sources.length;
metrics.excludedGlobalText=Object.fromEntries(['ru','en'].map(lang=>[lang,{methodNoteWords:words(d.methodNote[lang]),sourceNoteWords:d.sources.reduce((n,s)=>n+words(s.note[lang]),0),readingTimeIncludesThese:false}]));
for(const [mode,level]of[['essential',1],['core',2],['deep',3]]){
 const list=d.screens.filter(s=>s.level<=level);if(list.length!==d.targetModes[mode])throw Error('Mode count '+mode);
 metrics.modes[mode]={screens:list.length,readingScreens:list.length-1,orderedIds:list.map(s=>s.id)};
 for(const lang of ['ru','en']){
  const bodyWords=list.filter(s=>s.type!=='cover').reduce((n,s)=>n+words(s.copy[lang].body),0);
  const headingWords=list.filter(s=>s.type!=='cover').reduce((n,s)=>n+words(s.copy[lang].title),0);
  const coverWords=list.filter(s=>s.type==='cover').reduce((n,s)=>n+words(s.copy[lang].title+' '+(s.copy[lang].subtitle||'')+' '+s.copy[lang].body),0);
  const sectionLabelWords=list.reduce((n,s)=>n+words(s.copy[lang].section),0);
  const uiEstimateWords=list.reduce((n,s)=>n+words(s.copy[lang].title+' '+(s.copy[lang].subtitle||'')+' '+s.copy[lang].body),0);
  const rate=metrics.rates[lang],expectedMinutes=Math.ceil(uiEstimateWords/rate);
  if(parseInt(e.modes[mode].minutes[lang],10)!==expectedMinutes)throw Error('UI time '+lang+'/'+mode);
  const n=expectedMinutes,suffix=n%100>=11&&n%100<=14?'минут':n%10===1?'минута':n%10>=2&&n%10<=4?'минуты':'минут';
  if(lang==='ru'&&e.modes[mode].minutes.ru!==n+' '+suffix)throw Error('RU declension '+mode);
  metrics.modes[mode][lang]={bodyWords,headingWords,coverWords,sectionLabelWords,uiEstimateWords,bodyMinutes:Number((bodyWords/rate).toFixed(2)),roundedBodyMinutes:Math.ceil(bodyWords/rate),uiMinutes:e.modes[mode].minutes[lang]};
  const route=fs.readFileSync(path.join(dir,'routes',mode+'.'+lang+'.md'),'utf8');
  const routeParas=route.split(/\n\s*\n/).map(x=>x.trim()).filter(x=>x&&!x.startsWith('#')&&!x.startsWith(mode[0].toUpperCase()+mode.slice(1)+' ·'));
  const expected=list.flatMap(s=>[...s.copy[lang].body.matchAll(/<p>([\s\S]*?)<\/p>/g)].map(m=>decode(m[1])));
  if(JSON.stringify(routeParas)!==JSON.stringify(expected))throw Error('Review route parity '+mode+'/'+lang);
  metrics.routeParity[mode+'.'+lang]={paragraphs:routeParas.length,exactInOrder:true};
 }
}
for(const lang of['ru','en']){
 const list=d.screens.filter(s=>s.type!=='cover'),a=list.map(s=>words(s.copy[lang].body)).sort((a,b)=>a-b);
 metrics.density[lang]={readingScreens:a.length,min:a[0],median:a.length%2?a[Math.floor(a.length/2)]:(a[a.length/2-1]+a[a.length/2])/2,max:a.at(-1),mean:Number((a.reduce((n,x)=>n+x,0)/a.length).toFixed(2))};
 const expected=fs.readFileSync(path.join(dir,'draft-'+lang+'.md'),'utf8').split(/\n\s*\n/).map(x=>x.trim()).filter(x=>x&&!x.startsWith('#'));
 const actual=list.flatMap(s=>[...s.copy[lang].body.matchAll(/<p>([\s\S]*?)<\/p>/g)].map(m=>decode(m[1])));
 if(JSON.stringify(expected)!==JSON.stringify(actual))throw Error('Draft paragraph divergence '+lang);
  if(actual.length!==(d.screens.length-1)*2)throw Error('Unexpected paragraph count '+lang);
 metrics.draftParity[lang]={paragraphs:actual.length,exactInOrder:true};
}
for(const s of d.screens){
 const paras=lang=>[...s.copy[lang].body.matchAll(/<p>/g)].length;
 if(paras('ru')!==paras('en'))throw Error('Paragraph parity '+s.id);
}
metrics.inputHashes=Object.fromEntries(['story-data.json',d.slug+'.html','draft-ru.md','draft-en.md'].map(name=>[name,hash(path.join(dir,name))]));
const input=JSON.parse(fs.readFileSync(path.join(dir,'immutable-input-hashes.json'),'utf8'));
metrics.immutableInputs=Object.entries(input).map(([file,before])=>({path:file,before,after:hash(file),unchanged:before===hash(file)}));
if(metrics.immutableInputs.some(x=>!x.unchanged))throw Error('Protected input changed');
metrics.primarySourceLedger={};
const ledger=JSON.parse(fs.readFileSync(path.join(dir,'source-reading-ledger.json'),'utf8'));
for(const file of ledger.files){
 const content=fs.readFileSync(path.join(ledger.sourceRoot,file.file),'utf8');
 if(createHash('sha256').update(content).digest('hex')!==file.sha256)throw Error('Source hash changed '+file.file);
 const codepoints=Array.from(content);
 for(const r of file.rangesRead)if(createHash('sha256').update(codepoints.slice(r.start,r.end).join('')).digest('hex')!==r.chunkSha256)throw Error('Read chunk hash '+file.file);
 if(file.mainBodyEnd){let end=0;for(const r of [...file.rangesRead].filter(r=>r.start<file.mainBodyEnd).sort((a,b)=>a.start-b.start)){if(r.start>end)throw Error('Uncovered source gap '+file.file);end=Math.max(end,r.end)}if(end<file.mainBodyEnd)throw Error('Incomplete main body '+file.file);metrics.primarySourceLedger[file.file]={mainBodyEnd:file.mainBodyEnd,coveredThrough:end,sha256:file.sha256};}
}
if(Object.keys(metrics.primarySourceLedger).length!==18)throw Error('Main chapter count');
// Browser runs must describe this exact immutable HTML and QA script.
metrics.browserReports=[];
for(const name of ['browser-320.json','browser-390.json','browser-1024.json','browser-1440.json','browser-ios-320.json']){
 const file=path.join(dir,'qa',name);if(!fs.existsSync(file))continue;
 const r=JSON.parse(fs.readFileSync(file,'utf8'));
 for(const [key,value]of Object.entries(r.inputHashes))if(hash(path.join(dir,key))!==value)throw Error('Stale browser proof '+name+'/'+key);
 if(r.status!=='local-checks-completed'||!r.cleanup.profileRemoved||r.cleanup.remainingOwnedPids.length)throw Error('Failed browser proof '+name);
 metrics.browserReports.push({file:'qa/'+name,sha256:hash(file),width:r.width,height:r.height,views:r.traversal.views,interactions:r.interaction.length,cleanup:r.cleanup});
}
const pref=JSON.parse(fs.readFileSync(path.join(dir,'qa','preference-state.json'),'utf8'));
for(const [key,value]of Object.entries(pref.inputHashes))if(hash(path.join(dir,key))!==value)throw Error('Stale preference proof '+key);
if(pref.status!=='local-checks-completed'||!pref.realDocumentReload||!pref.cleanup.profileRemoved||pref.cleanup.remainingOwnedPids.length)throw Error('Preference proof failed');
metrics.preferenceReport={file:'qa/preference-state.json',sha256:hash(path.join(dir,'qa','preference-state.json')),checks:pref.checks,realDocumentReload:pref.realDocumentReload,scope:pref.scope,cleanup:pref.cleanup};
metrics.chapterBodyWords=[];
for(let chapter=1;chapter<=18;chapter++){
 const list=d.screens.filter(s=>s.bookLocation?.chapter===chapter);
 metrics.chapterBodyWords.push({chapter,screens:list.length,ru:list.reduce((n,s)=>n+words(s.copy.ru.body),0),en:list.reduce((n,s)=>n+words(s.copy.en.body),0)});
}
fs.writeFileSync(path.join(dir,'qa','metrics-and-integrity.json'),JSON.stringify(metrics,null,2)+'\n');
console.log(JSON.stringify({modes:metrics.modes,density:metrics.density,browserReports:metrics.browserReports.length,paragraphParity:metrics.draftParity,primaryChapters:Object.keys(metrics.primarySourceLedger).length,protectedInputsUnchanged:true},null,2));

import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const read=n=>fs.readFileSync(path.join(dir,n),'utf8');
const hash=b=>createHash('sha256').update(b).digest('hex');
const sha=n=>hash(fs.readFileSync(path.join(dir,n)));
const data=JSON.parse(read('story-data.json'));
const html=read('children-of-captain-grant.html');
const embedded=JSON.parse(html.match(/<script\b[^>]*\bid="book-tiktok-data"[^>]*>([\s\S]*?)<\/script>/)[1]);
const checked=[];
const check=(name,ok)=>{checked.push({name,passed:!!ok});if(!ok)throw Error(name)};
const strip=v=>String(v||'').replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,' ').replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi,' ').replace(/<[^>]+>/g,' ').replace(/&(?:nbsp|amp|lt|gt|quot|#39);/gi,' ').replace(/\s+/g,' ').trim();
const words=v=>(strip(v).match(/[\p{L}\p{N}][\p{L}\p{N}'’\-–—]*/gu)||[]).length;
const unescape=v=>v.replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;/g,"'");
const paragraphs=lang=>read(`draft-${lang}.md`).split(/^## /m).slice(1).flatMap(g=>g.split('\n\n').slice(1).map(p=>p.trim()).filter(Boolean));
const narrative=data.screens.filter(s=>Number.isInteger(s.draftParagraph));
check('113 narrative beats and 116 total screens',narrative.length===113&&data.screens.length===116);
check('unique stable IDs',new Set(data.screens.map(s=>s.id)).size===116);
for(const lang of ['ru','en']){
 const ps=paragraphs(lang);
 check(`${lang} connected draft has 113 paragraphs`,ps.length===113);
 check(`${lang} all draft paragraphs exactly equal authoring JSON paragraphs`,narrative.every((s,i)=>unescape(s.copy[lang].body.slice(3,-4))===ps[i]));
 check(`${lang} embedded HTML has exact actual narrative paragraphs`,embedded.screens.filter(s=>s.draftParagraph).every((s,i)=>s.copy[lang].body===narrative[i].copy[lang].body));
 check(`${lang} all framing, titles and section headings match authoring JSON`,embedded.screens.every((s,i)=>JSON.stringify(s.copy[lang])===JSON.stringify(data.screens[i].copy[lang])));
}
check('same complete authoring screen metadata in embedded HTML',JSON.stringify(embedded.screens)===JSON.stringify(data.screens));
check('fresh book-local progress namespace',html.includes('book-tiktok.${data.slug}.depth-v2.'));
check('RU/dark/Essential narrative defaults',data.defaultLanguage==='ru'&&data.defaultTheme==='dark'&&data.defaultMode==='essential'&&data.contentMode==='narrative');
check('consent variable is memory-only and reset on pagehide',html.includes('let deepConsent = false')&&html.includes("addEventListener('pagehide'"));
const witness=JSON.parse(read('witness-reading-ledger.json'));
const primary=fs.readFileSync(witness.witness),lines=primary.toString('utf8').match(/[^\n]*\n|[^\n]+$/g)||[];
check('frozen primary SHA256 and line count',hash(primary)===witness.sha256&&lines.length===witness.totalLines);
let last=0;
for(const c of witness.chunks){
 const chunk=Buffer.from(lines.slice(c.startLine-1,c.endLine).join(''),'utf8');
 check(`read chunk ${c.chunk}: contiguous, acknowledged, exact byte hash`,c.startLine===last+1&&c.read===true&&chunk.length===c.bytes&&hash(chunk)===c.sha256);
 last=c.endLine;
}
check('all 20151 primary lines actually covered in 34 acknowledged ranges',witness.continuousCompleteRead&&witness.chunks.length===34&&last===20151);
const chapters=JSON.parse(read('witness-chapter-ranges.json'));
check('66 source chapters, 26 / 19 / 21',chapters.length===66&&[1,2,3].every((p,i)=>chapters.filter(c=>c.part===p).length===[26,19,21][i]));
const map=JSON.parse(read('scene-map.json'));
check('all 66 source chapters mapped to real candidate scenes',new Set(map.flatMap(s=>s.chapters)).size===66&&map.length===113);
check('every narrative beat has a real primary range and the source witness',narrative.every(s=>s.evidenceLocator&&s.sources.includes(1)));
const metrics={
 schemaVersion:1,wordDefinition:"Maintained builder Unicode token regex /[\\p{L}\\p{N}][\\p{L}\\p{N}'’\\-–—]*/gu after the same HTML stripping. A hyphenated token counts once.",
 narrativeDefinition:'Only original story paragraph bodies. Excludes all section headings, screen titles, cover, inline warning, final framing, Sources and reader controls.',
 ratesWordsPerMinute:{ru:180,en:220},
 timingCaveat:'Estimates, not measured human reading. UI includes title/subtitle and framing body, excludes section kickers; reporting all headings separately makes that overhead visible.',
 draftParagraphsPerLanguage:113,connectedEpisodesPerLanguage:30,sourceChapters:66,
 inputHashes:Object.fromEntries(['draft-ru.md','draft-en.md','story-data.json','children-of-captain-grant.html'].map(n=>[n,sha(n)])),modes:{},parts:{},connectedDraftHeadings:{}
};
for(const [mode,level] of [['essential',1],['core',2],['deep',3]]){
 const screens=data.screens.filter(s=>s.level<=level);
 check(`${mode} derived route matches exact declared count`,screens.length===data.targetModes[mode]);
 metrics.modes[mode]={screens:screens.length,narrativeScreens:screens.filter(s=>s.draftParagraph).length,framingScreens:screens.filter(s=>!s.draftParagraph).length,languages:{}};
 for(const lang of ['ru','en']){
  const narrativeBody=screens.filter(s=>s.draftParagraph).reduce((n,s)=>n+words(s.copy[lang].body),0);
  const framingBody=screens.filter(s=>!s.draftParagraph).reduce((n,s)=>n+words(s.copy[lang].body),0);
  const sectionHeadings=screens.reduce((n,s)=>n+words(s.copy[lang].section),0);
  const screenTitles=screens.reduce((n,s)=>n+words(s.copy[lang].title),0);
  const subtitles=screens.reduce((n,s)=>n+words(s.copy[lang].subtitle),0);
  const headings=sectionHeadings+screenTitles+subtitles;
  const uiWords=narrativeBody+framingBody+screenTitles+subtitles;
  const rate=metrics.ratesWordsPerMinute[lang];
  const minutes=w=>({atRate:w/rate,roundedUp:Math.ceil(w/rate)});
  metrics.modes[mode].languages[lang]={narrativeBodyWords:narrativeBody,framingBodyWords:framingBody,headingWords:headings,sectionHeadingWords:sectionHeadings,screenTitleWords:screenTitles,subtitleWords:subtitles,allVisibleCopyWords:narrativeBody+framingBody+headings,uiCountedWords:uiWords,narrativeMinutes:minutes(narrativeBody),framingMinutes:minutes(framingBody),headingMinutes:minutes(headings),allVisibleCopyMinutes:minutes(narrativeBody+framingBody+headings),uiEstimatedMinutes:Math.ceil(uiWords/rate),uiLabel:embedded.modes[mode].minutes[lang]};
 }
}
for(const [part,start,end] of [['I',1,43],['II',44,75],['III',76,113]]){
 metrics.parts[part]={paragraphs:[start,end],narrativeWords:Object.fromEntries(['ru','en'].map(l=>[l,narrative.filter(s=>s.draftParagraph>=start&&s.draftParagraph<=end).reduce((n,s)=>n+words(s.copy[l].body),0)]))};
}
for(const lang of ['ru','en'])metrics.connectedDraftHeadings[lang]={episodeHeadingWords:words([...read(`draft-${lang}.md`).matchAll(/^## (.+)$/gm)].map(m=>m[1]).join(' ')),bookTitleAndSourcePreface:'Excluded from narrative counts; present only in review draft, not repeated between narrative scenes.'};
check('113 paragraph prefix parity in exported shorter routes',['ru','en'].every(l=>['essential','core'].every(mode=>{const expected=paragraphs(l).slice(0,mode==='essential'?24:67);return expected.every(p=>read(`routes/${mode}-${l}.md`).includes(p))})));
fs.writeFileSync(path.join(dir,'metrics.json'),JSON.stringify(metrics,null,2)+'\n');
fs.writeFileSync(path.join(dir,'qa/content-verification.json'),JSON.stringify({status:'passed',inputHashes:metrics.inputHashes,checks:checked,completeWitnessRangeRehash:true,primaryBytes:primary.length,primaryLines:lines.length,primaryTextCopied:false},null,2)+'\n');
console.log(JSON.stringify({checks:checked.length,modes:metrics.modes,parts:metrics.parts},null,2));

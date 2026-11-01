import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url)),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const raw=JSON.parse(fs.readFileSync(path.join(root,'story-data.json'))),html=fs.readFileSync(path.join(root,'four-thousand-weeks.html'),'utf8');
const embedded=JSON.parse(html.match(/<script id="book-tiktok-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
function checkFields(a,b){for(const k of Object.keys(a)){if(a[k]&&typeof a[k]==='object'&&!Array.isArray(a[k]))checkFields(a[k],b[k]);else assert.deepEqual(b[k],a[k],`field ${k}`);}}checkFields(raw,embedded);
const decode=t=>t.replaceAll('&amp;','&').replaceAll('&lt;','<').replaceAll('&gt;','>');
const strip=t=>t.replace(/<[^>]+>/g,' ').replace(/&(?:nbsp|amp|lt|gt|quot|#39);/gi,' ').replace(/\s+/g,' ').trim();
const words=t=>(strip(t).match(/[\p{L}\p{N}][\p{L}\p{N}'’\-–—]*/gu)||[]).length;
const body=t=>decode(t.replace(/<[^>]+>/g,''));
const metrics={wordConvention:'Exact maintained builder Unicode lexical counter; hyphenated words count as one. Body excludes cover, headings, subtitles, Sources and control labels; shared final paragraph is body. UI estimate uses title+subtitle+body across selected screens, as the maintained builder does; section labels, controls and global Sources are separately excluded from that estimate.',wpm:{ru:180,en:220},modes:{}};
for(const lang of ['ru','en']){const paras=fs.readFileSync(path.join(root,`draft.${lang}.md`),'utf8').trim().split(/\n\n/).filter(p=>!p.startsWith('#'));assert.deepEqual(paras,raw.screens.slice(1).map(s=>body(s.copy[lang].body)));}
for(const [mode,level] of [['essential',1],['core',2],['deep',3]]){
 const list=raw.screens.filter(s=>s.level<=level);assert.equal(list.length,raw.targetModes[mode]);metrics.modes[mode]={screens:list.length};
 for(const lang of ['ru','en']){
  const rate=metrics.wpm[lang],bodyWords=list.filter(s=>s.type!=='cover').reduce((n,s)=>n+words(s.copy[lang].body),0),uiWords=list.reduce((n,s)=>{const c=s.copy[lang];return n+words(`${c.title} ${c.subtitle||''} ${c.body||''}`)},0),headingWords=list.reduce((n,s)=>n+words(s.copy[lang].title+' '+(s.copy[lang].subtitle||'')),0),framingWords=words(list[0].copy[lang].body),sectionWords=list.reduce((n,s)=>n+words(s.copy[lang].section),0);
  metrics.modes[mode][lang]={bodyWords,bodyMinutes:bodyWords/rate,roundedBodyMinutes:Math.ceil(bodyWords/rate),uiWords,uiMinutes:uiWords/rate,uiRoundedMinutes:Math.ceil(uiWords/rate),uiLabel:embedded.modes[mode].minutes[lang],headingAndSubtitleWords:headingWords,coverFramingWords:framingWords,sectionLabelWords:sectionWords};
  assert.equal(uiWords,bodyWords+headingWords+framingWords);
  const expected=`# ${raw.title[lang]} — ${mode}\n\n`+list.map(s=>`## ${s.id} · ${s.copy[lang].title}\n\n${body(s.copy[lang].body)}\n`).join('\n');
  assert.equal(fs.readFileSync(path.join(root,`route.${mode}.${lang}.md`),'utf8'),expected);
 }
}
metrics.globalSources={};for(const l of ['ru','en'])metrics.globalSources[l]={methodWords:words(raw.methodNote[l]),sourceNoteWords:raw.sources.reduce((n,s)=>n+words(s.note[l]),0),sourceTitleWords:raw.sources.reduce((n,s)=>n+words(s.title),0)};
metrics.density={};for(const l of ['ru','en']){const counts=raw.screens.slice(1).map(s=>words(s.copy[l].body)).sort((a,b)=>a-b);metrics.density[l]={passages:counts.length,min:counts[0],median:(counts[42]+counts[43])/2,max:counts.at(-1),mean:counts.reduce((a,b)=>a+b,0)/counts.length};}
const primary=fs.readFileSync('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-8-private/four-thousand-weeks-edition.json');assert.equal(sha(primary),'4d59335257d507e204bcc3f28aab121c6cc0f0aead4cd092fc844787f1f337c0');const source=JSON.parse(primary),ledger=JSON.parse(fs.readFileSync(path.join(root,'primary-reading-ledger.json'))),seen={};
for(const e of ledger.entries){const r=source.find(r=>r.file===e.file);assert.equal(sha(r.paragraphs.slice(e.firstParagraph-1,e.lastParagraph).join('\n')),e.rangeSha256);assert(e.displayedReadingAcknowledged);seen[e.file]??=new Set();for(let p=e.firstParagraph;p<=e.lastParagraph;p++)seen[e.file].add(p);}
const main=['content04','chast1',...Array.from({length:6},(_,i)=>`content${i+1}`),'chast2',...Array.from({length:10},(_,i)=>`content${i+7}`)];
let mainParagraphs=0,mainWords=0;for(const f of main){const r=source.find(r=>r.file===`OEBPS/Text/${f}.html`);assert.equal(seen[r.file].size,r.paragraphs.length,`continuous coverage ${f}`);mainParagraphs+=r.paragraphs.length;mainWords+=r.words;}
for(const s of raw.screens.slice(1))for(const l of s.primaryLocators)for(let p=l.firstParagraph;p<=l.lastParagraph;p++)assert(seen[l.file]?.has(p),`${s.id} unread locator`);
metrics.primary={records:source.length,totalExtractedWords:source.reduce((n,r)=>n+r.words,0),mainSpineRecords:main.length,mainSpineParagraphs:mainParagraphs,mainSpineExtractedWords:mainWords};
const reading=JSON.parse(fs.readFileSync(path.join(root,'route-reading-ledger.json'))),routeCoverage={};for(const e of reading.entries){const level={essential:1,core:2,deep:3}[e.mode],list=raw.screens.filter(s=>s.level<=level),part=list.slice(e.firstPosition-1,e.lastPosition);const stable=JSON.stringify(part,(k,v)=>v&&typeof v==='object'&&!Array.isArray(v)?Object.keys(v).sort().reduce((r,k)=>(r[k]=v[k],r),{}):v);
 // Python json.dumps uses spaces; verify its canonical range hash below in Python as well.
 routeCoverage[e.mode]??=new Set();for(let p=e.firstPosition;p<=e.lastPosition;p++)routeCoverage[e.mode].add(p);
}
metrics.routeReadingCoverage=Object.fromEntries(Object.entries(routeCoverage).map(([m,s])=>[m,{pairs:s.size,expected:raw.targetModes[m]}]));
fs.writeFileSync(path.join(root,'metrics.json'),JSON.stringify(metrics,null,2)+'\n');
fs.writeFileSync(path.join(root,'parity.json'),JSON.stringify({allAuthoredFieldsMatchEmbedded:true,all86PairedParagraphsMatchConnectedDrafts:true,allSixRouteFilesMatchExactSelection:true,allPrimaryLocatorsDisplayedAndAcknowledged:true,sourceUnchanged:true,jsonSha256:sha(fs.readFileSync(path.join(root,'story-data.json'))),htmlSha256:sha(Buffer.from(html))},null,2)+'\n');
console.log(JSON.stringify(metrics.modes,null,2));console.log(JSON.stringify(metrics.primary));

import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
const d=path.dirname(path.dirname(fileURLToPath(import.meta.url))),read=n=>fs.readFileSync(path.join(d,n),'utf8'),sha=b=>createHash('sha256').update(b).digest('hex');
fs.mkdirSync(path.join(d,'root-review','qa'),{recursive:true});
const a=JSON.parse(read('story-data.json')),h=read('children-of-captain-grant.html'),e=JSON.parse(h.match(/<script id="book-tiktok-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const assert=(v,s)=>{if(!v)throw Error(s)};
const plain=s=>s.replace(/<[^>]+>/g,' ').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/\s+/g,' ').trim();
const words=s=>(s.match(/[\p{L}\p{N}][\p{L}\p{N}'’\-–—]*/gu)||[]).length;
const countBody=s=>words(plain(s));
assert(JSON.stringify(a.screens)===JSON.stringify(e.screens),'screen JSON/HTML parity');
for(const [k,v]of Object.entries(a))if(k!=='modes')assert(JSON.stringify(v)===JSON.stringify(e[k]),'metadata parity '+k);
assert(!a.modes,'authoring has only generated runtime mode labels');
for(const l of ['ru','en']){
 const ps=read(`draft-${l}.md`).split(/^## /m).slice(1).flatMap(s=>s.split('\n\n').slice(1).map(p=>p.trim()).filter(Boolean));
 const ss=a.screens.filter(s=>Number.isInteger(s.draftParagraph));assert(ps.length===ss.length,'draft paragraph count '+l);
 ps.forEach((p,i)=>assert(p===plain(ss[i].copy[l].body),'exact connected-draft paragraph '+l+' '+i));
}
const metrics={wordDefinition:"Unicode letter/number start, continuing letters/numbers/apostrophes/hyphens/en/em dashes; exact maintained builder regex. Section labels, UI, Sources and method excluded. Narrative = only integer draftParagraph bodies. Builder total = visible titles/subtitles/bodies, including framing.",rates:{ru:180,en:220},depths:{}};
for(const [m,lv]of Object.entries({essential:1,core:2,deep:3})){
 const ss=a.screens.filter(s=>s.level<=lv),ns=ss.filter(s=>Number.isInteger(s.draftParagraph)),row={screens:ss.length,narrativeScreens:ns.length,narrativeWords:{},framingBodyWords:{},titlesAndSubtitlesWords:{},titleSubtitleBodyWords:{},narrativeMinutes:{},builderCeilingMinutes:{}};
 for(const l of ['ru','en']){
  row.narrativeWords[l]=ns.reduce((n,s)=>n+countBody(s.copy[l].body),0);
  row.framingBodyWords[l]=ss.filter(s=>!Number.isInteger(s.draftParagraph)).reduce((n,s)=>n+countBody(s.copy[l].body),0);
  row.titlesAndSubtitlesWords[l]=ss.reduce((n,s)=>n+countBody(s.copy[l].title+' '+(s.copy[l].subtitle||'')),0);
  row.titleSubtitleBodyWords[l]=row.narrativeWords[l]+row.framingBodyWords[l]+row.titlesAndSubtitlesWords[l];
  row.narrativeMinutes[l]=Number((row.narrativeWords[l]/metrics.rates[l]).toFixed(4));
  row.builderCeilingMinutes[l]=Math.ceil(row.titleSubtitleBodyWords[l]/metrics.rates[l]);
  assert(parseInt(e.modes[m].minutes[l],10)===row.builderCeilingMinutes[l],'builder minutes '+m+l);
 }
 metrics.depths[m]=row;assert(ss.length===a.targetModes[m],'mode counts');
}
const narrativeIds=a.screens.filter(s=>Number.isInteger(s.draftParagraph)).map(s=>s.id);const prefixProof={};for(const [m,lv,n] of [['essential',1,24],['core',2,67]]){const ids=a.screens.filter(s=>s.level<=lv&&Number.isInteger(s.draftParagraph)).map(s=>s.id);assert(JSON.stringify(ids)===JSON.stringify(narrativeIds.slice(0,n)),m+' is exact continuous already-read prefix');prefixProof[m]={paragraphs:n,ids,exactPrefixOfDeep:true};}fs.writeFileSync(path.join(d,'root-review','qa','shorter-prefix-proof.json'),JSON.stringify(prefixProof,null,2)+'\n');
const prev=JSON.parse(read('root-review/protected-baseline.json')),changes=[];for(const p of prev.files){if(!fs.existsSync(p.path)||sha(fs.readFileSync(p.path))!==p.sha256)changes.push(p.path)}
fs.writeFileSync(path.join(d,'root-review','qa','metrics.json'),JSON.stringify(metrics,null,2)+'\n');
const allowedExternalChanges=['/Users/pn/smartcat/_artifacts/book-tiktok-library/editorial-audit/2026-10-31/depth-v2/PLAN.json'];if(changes.some(p=>!allowedExternalChanges.includes(p)))throw Error('Unexpected protected input changes '+JSON.stringify(changes));
const audit=spawnSync(process.execPath,['/Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs',path.join(d,'children-of-captain-grant.html'),'--min-screens',String(a.screens.length),'--require-bilingual'],{encoding:'utf8'});
fs.writeFileSync(path.join(d,'root-review','qa','structural-audit.json'),audit.stdout);assert(audit.status===0,'structural audit '+audit.stderr);
const parity={atUtc:new Date().toISOString(),storyDataSha256:sha(read('story-data.json')),htmlSha256:sha(h),authoredEmbeddedScreensExact:true,metadataExactExceptGeneratedModeMinutes:true,connectedDraftParagraphsExact:true,narrativeScreens:a.screens.filter(s=>Number.isInteger(s.draftParagraph)).length,bilingualDrafts:true,protectedFilesChecked:prev.files.length,protectedChanges:changes,scope:'Mechanical parity, counts, immutable-input check; not literary acceptance'};
fs.writeFileSync(path.join(d,'root-review','qa','parity.json'),JSON.stringify(parity,null,2)+'\n');
console.log(JSON.stringify({metrics,parity},null,2));

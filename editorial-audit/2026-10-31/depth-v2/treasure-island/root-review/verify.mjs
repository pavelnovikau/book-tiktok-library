import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import{createHash}from'node:crypto';import{spawnSync}from'node:child_process';
const dir=path.dirname(path.dirname(fileURLToPath(import.meta.url))),sha=b=>createHash('sha256').update(b).digest('hex');
const data=JSON.parse(fs.readFileSync(path.join(dir,'story-data.json'),'utf8')),ht=fs.readFileSync(path.join(dir,'treasure-island.html'),'utf8');
const embedded=JSON.parse(ht.match(/<script id="book-tiktok-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const cmp=JSON.parse(JSON.stringify(embedded));delete cmp.modes;if(JSON.stringify(cmp)!==JSON.stringify(data))throw Error('authoring/embedded mismatch');
const strip=s=>s.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,' ').replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi,' ').replace(/<[^>]+>/g,' ').replace(/&(?:nbsp|amp|lt|gt|quot|#39);/gi,' ').replace(/\s+/g,' ').trim();
const count=s=>(strip(s).match(/[\p{L}\p{N}][\p{L}\p{N}'’\-–—]*/gu)||[]).length;
const framing=s=>s.type==='cover'||s.final||s.id==='deep-warning',metrics={wordDefinition:"Maintained builder regex /[\\p{L}\\p{N}][\\p{L}\\p{N}'’\\-–—]*/gu after its HTML stripping. Narrative = story bodies only; excludes cover, Deep warning, final and all titles/sections.",rates:{ru:180,en:220},depths:{}};
const decode=s=>s.replaceAll('&amp;','&').replaceAll('&lt;','<').replaceAll('&gt;','>');
let paragraphs={};
for(const l of ['ru','en']){
 const draft=fs.readFileSync(path.join(dir,`draft-${l}.md`),'utf8'),ps=draft.split(/\n\n/).map(x=>x.trim()).filter(x=>x&&!x.startsWith('#'));
 const fromScreens=data.screens.filter(s=>!framing(s)).map(s=>decode(s.copy[l].body.replace(/^<p>|<\/p>$/g,'')));
 if(JSON.stringify(ps)!==JSON.stringify(fromScreens))throw Error(l+' connected draft mismatch');paragraphs[l]=ps.length;
}
for(const [mode,lev]of Object.entries({essential:1,core:2,deep:3})){
 const list=data.screens.filter(s=>s.level<=lev),row={screens:list.length,narrativeScreens:list.filter(s=>!framing(s)).length,narrativeWords:{},framingBodyWords:{},titlesSubtitlesWords:{},sectionWords:{},titleSubtitleBodyWords:{},narrativeMinutes:{},builderCeilingMinutes:{}};
 for(const l of ['ru','en']){
  row.narrativeWords[l]=list.filter(s=>!framing(s)).reduce((n,s)=>n+count(s.copy[l].body),0);
  row.framingBodyWords[l]=list.filter(framing).reduce((n,s)=>n+count(s.copy[l].body),0);
  row.titlesSubtitlesWords[l]=list.reduce((n,s)=>n+count(s.copy[l].title+' '+(s.copy[l].subtitle||'')),0);
  row.sectionWords[l]=list.reduce((n,s)=>n+count(s.copy[l].section),0);
  row.titleSubtitleBodyWords[l]=list.reduce((n,s)=>n+count(`${s.copy[l].title} ${s.copy[l].subtitle||''} ${s.copy[l].body}`),0);
  row.narrativeMinutes[l]=Number((row.narrativeWords[l]/metrics.rates[l]).toFixed(4));row.builderCeilingMinutes[l]=Math.ceil(row.titleSubtitleBodyWords[l]/metrics.rates[l]);
 }
 metrics.depths[mode]=row;
}
fs.writeFileSync(path.join(dir,'root-review/qa/metrics.json'),JSON.stringify(metrics,null,2)+'\n');
const baseline=JSON.parse(fs.readFileSync(path.join(dir,'protected-baseline.json'),'utf8')),changes=[];
for(const [p,h]of Object.entries(baseline))if(!fs.existsSync(p)||sha(fs.readFileSync(p))!==h)changes.push(p);
if(changes.length)throw Error('protected changes '+JSON.stringify(changes));
const a=spawnSync(process.execPath,['/Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs',path.join(dir,'treasure-island.html'),'--min-screens','96','--require-bilingual'],{encoding:'utf8'});if(a.status!==0)throw Error(a.stdout+a.stderr);const audit=JSON.parse(a.stdout);fs.writeFileSync(path.join(dir,'root-review/qa/structural-audit.json'),JSON.stringify(audit,null,2)+'\n');
if(audit.warnings.length||audit.failures.length)throw Error('audit warning/failure');
const report={status:'mechanical-checks-completed-not-editorial-acceptance',hashes:Object.fromEntries(['story-data.json','treasure-island.html','draft-ru.md','draft-en.md'].map(n=>[n,sha(fs.readFileSync(path.join(dir,n)))])),authoringEmbeddedParity:true,connectedDraftScreenParity:paragraphs,protectedFilesCompared:Object.keys(baseline).length,protectedChanges:changes,counts:data.targetModes,structuralAudit:audit};
fs.writeFileSync(path.join(dir,'root-review/qa/parity-and-protection.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({counts:report.counts,depths:metrics.depths,protected:Object.keys(baseline).length,audit:{passes:audit.passes,warnings:audit.warnings,failures:audit.failures}},null,2));

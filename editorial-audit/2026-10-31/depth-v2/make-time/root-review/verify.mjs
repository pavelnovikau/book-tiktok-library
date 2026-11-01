import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import{createHash}from'node:crypto';
const dir=path.dirname(path.dirname(fileURLToPath(import.meta.url))),read=n=>fs.readFileSync(path.join(dir,n),'utf8'),hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex'),assert=(v,m)=>{if(!v)throw Error(m)};
const d=JSON.parse(read('story-data.json')),h=read('make-time.html'),e=JSON.parse(h.match(/<script[^>]*id="book-tiktok-data"[^>]*>([\s\S]*?)<\/script>/)[1]);
const decode=t=>t.replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&#x27;|&#39;/g,"'").replace(/&quot;/g,'"').replace(/&nbsp;/g,' ');
const plain=s=>decode(s.replace(/<[^>]+>/g,' '));const words=s=>(plain(s).match(/[\p{L}\p{N}][\p{L}\p{N}'’\-–—]*/gu)||[]).length;
assert(JSON.stringify(d.screens)===JSON.stringify(e.screens),'canonical/embedded screen mismatch');assert(JSON.stringify(d.sources)===JSON.stringify(e.sources),'source mismatch');
const metrics={rates:{ru:180,en:220},wordMethod:'Unicode lexical tokens using builder regex; HTML is decoded. Main body excludes cover/final, headings, subtitles, sections, UI and source notes. Noncover body adds final. Framing is counted separately. UI estimate includes all titles, author subtitle, cover/body/final, but excludes section labels and shell controls.',modes:{},density:{},parity:{embeddedEqualsCanonical:true},hashes:{json:hash(path.join(dir,'story-data.json')),html:hash(path.join(dir,'make-time.html'))}};
let prev=[];for(const[mode,level]of[['essential',1],['core',2],['deep',3]]){
 const list=d.screens.filter(s=>s.level<=level),ids=list.map(s=>s.id);assert(ids.length===d.targetModes[mode],'count '+mode);assert(prev.every(id=>ids.includes(id)),'nested '+mode);assert(prev.join('|')===ids.filter(id=>prev.includes(id)).join('|'),'nested order '+mode);prev=ids;
 metrics.modes[mode]={screens:list.length,ids};
 for(const lang of['ru','en']){
  const total=(ls,fn)=>ls.reduce((n,s)=>n+words(fn(s.copy[lang])),0),main=list.filter(s=>s.type!=='cover'&&!s.final),cover=list.filter(s=>s.type==='cover'),final=list.filter(s=>s.final);
  const mainBodyWords=total(main,c=>c.body),sharedFinalBodyWords=total(final,c=>c.body),coverBodyWords=total(cover,c=>c.body),titleWords=total(list,c=>c.title),subtitleWords=total(list,c=>c.subtitle||''),sectionWords=total(list,c=>c.section),framingWords=sharedFinalBodyWords+coverBodyWords+titleWords+subtitleWords;
  const readerWords=mainBodyWords+framingWords,rate=metrics.rates[lang];
  metrics.modes[mode][lang]={mainBodyWords,noncoverBodyWords:mainBodyWords+sharedFinalBodyWords,sharedFinalBodyWords,coverBodyWords,titleWords,subtitleWords,framingWords,sectionLabelWords:sectionWords,readerWords,mainBodyMinutes:Number((mainBodyWords/rate).toFixed(4)),noncoverBodyMinutes:Number(((mainBodyWords+sharedFinalBodyWords)/rate).toFixed(4)),readerMinutes:Number((readerWords/rate).toFixed(4)),uiMinutes:e.modes[mode].minutes[lang]};
  assert(parseInt(e.modes[mode].minutes[lang])===Math.ceil(readerWords/rate),'reading estimate '+mode+'/'+lang);
  let expected=[];for(const s of list){const c=s.copy[lang];expected.push('## '+c.title,'',...c.subtitle?[c.subtitle,'']:[],decode(c.body.replaceAll('<p>','').replaceAll('</p>','\n\n')).trim(),'');}
  assert(read(`${mode}.${lang}.md`)===expected.join('\n'),'route parity '+mode+'/'+lang);
 }
}
for(const lang of['ru','en']){
 const a=d.screens.filter(s=>s.type!=='cover'&&!s.final).map(s=>words(s.copy[lang].body)).sort((a,b)=>a-b);metrics.density[lang]={mainScreens:a.length,min:a[0],median:(a[32]+a[33])/2,max:a.at(-1),mean:Number((a.reduce((n,x)=>n+x,0)/a.length).toFixed(4))};
 const draft=read(`draft-${lang}.md`).split(/^## /m).slice(1).flatMap(s=>s.slice(s.indexOf('\n')+1).trim().split('\n\n'));
 const actual=d.screens.filter(s=>s.type!=='cover'&&!s.final).flatMap(s=>[...s.copy[lang].body.matchAll(/<p>([\s\S]*?)<\/p>/g)].map(m=>decode(m[1])));
 assert(JSON.stringify(draft)===JSON.stringify(actual),'draft body parity '+lang);metrics.parity[lang]={draftBodyParagraphs:draft.length,exactInOrder:true};
}
const cov=JSON.parse(read('coverage-map.json'));assert(cov.tactics.length===87&&cov.tactics.every((t,i)=>t.tactic===i+1&&t.retainedMechanism),'all 87 tactics mapped');
const ledger=JSON.parse(read('private-source-reading-ledger.json'));metrics.sourceReading={records:ledger.sourceOrderRecords.length,nonemptyRecords:ledger.sourceOrderRecords.filter(r=>r.textRead).length,primaryWords:ledger.primaryWords,mainAnd87TacticsRead:ledger.mainTextAnd87TacticsRead,imagesRead:false,publishedEnglishRead:false};
const input=JSON.parse(read('immutable-input-hashes.json'));metrics.immutableInputs=Object.entries(input).map(([p,before])=>({path:p,before,after:hash(p),unchanged:before===hash(p)}));assert(metrics.immutableInputs.every(x=>x.unchanged),'read-only input changed');

const root=JSON.parse(read('root-review/reading-ledger.json'));
const original=JSON.parse(read('root-review/input-story-data.json'));
const changed=d.screens.filter((s,i)=>JSON.stringify(s.copy)!==JSON.stringify(original.screens[i].copy)).map(s=>s.id);
assert(JSON.stringify([...changed].sort())===JSON.stringify([...root.repairsImplementedPairIds].sort()),'exact14paired prose changes');
for(const k of Object.keys(original))if(!['screens','methodNote'].includes(k))assert(JSON.stringify(d[k])===JSON.stringify(original[k]),'unchanged metadata '+k);
for(const s of d.screens){const old=original.screens.find(x=>x.id===s.id);assert(s.level===old.level,'unchanged route level');if(s.id!=='stop-before-empty')assert(JSON.stringify(s.primaryRanges)===JSON.stringify(old.primaryRanges),'unchanged source ranges '+s.id);}
assert(!d.methodNote.ru.includes('Это черновик')&&!d.methodNote.en.includes('A draft awaiting'),'no stale draft label in reader');
const cp=await import('node:child_process');
const audit=cp.spawnSync(process.execPath,['/Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs',path.join(dir,'make-time.html'),'--min-screens','68','--require-bilingual'],{encoding:'utf8'});
fs.writeFileSync(path.join(dir,'root-review/qa/structural-audit.json'),audit.stdout);assert(audit.status===0,'structural audit '+audit.stderr);
metrics.rootPersonalAcceptance=false;metrics.publicationAllowed=false;
metrics.currentContentHashes=Object.fromEntries(['story-data.json','make-time.html','draft-ru.md','draft-en.md','coverage-map.json','argument-map.json'].map(n=>[n,hash(path.join(dir,n))]));
metrics.rootReading={allOriginalPairs:68,finalChangedPairs:changed.length,essentialPairs:root.essentialReadPairIds.length,coreAddedPairs:root.coreAddedPairsReread.length,method:root.shorterRouteReadingMethod,wholePrimaryContinuouslyRead:false};
fs.writeFileSync(path.join(dir,'root-review/qa/metrics.json'),JSON.stringify(metrics,null,2)+'\n');
fs.writeFileSync(path.join(dir,'root-review/qa/parity-check.json'),JSON.stringify({atUtc:new Date().toISOString(),allAuthoredFieldsMatchEmbedding:Object.keys(d).every(k=>JSON.stringify(d[k])===JSON.stringify(e[k])),draftParagraphs:metrics.parity,allSixRoutesExact:true,changedPairIds:changed,counts:d.targetModes,currentContentHashes:metrics.currentContentHashes,rootPersonalAcceptance:false,publicationAllowed:false},null,2)+'\n');
console.log(JSON.stringify({counts:d.targetModes,bodyWords:Object.fromEntries(Object.entries(metrics.modes).map(([mode,v])=>[mode,{ru:v.ru.noncoverBodyWords,en:v.en.noncoverBodyWords}])),changedPairs:changed.length,sourceCount:d.sources.length,protectedInputs:metrics.immutableInputs.length}));

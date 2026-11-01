import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import{createHash}from'node:crypto';
const dir=path.dirname(fileURLToPath(import.meta.url)),read=n=>fs.readFileSync(path.join(dir,n),'utf8'),hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex'),assert=(v,m)=>{if(!v)throw Error(m)};
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
metrics.browser=[];for(const width of[320,390,1024,1440]){
 const r=JSON.parse(read(`qa/browser-${width}.json`));assert(r.status==='local-checks-completed','browser incomplete '+width);assert(r.inputHashes['make-time.html']===metrics.hashes.html,'stale browser HTML '+width);assert(r.inputHashes['story-data.json']===metrics.hashes.json,'stale browser JSON '+width);assert(r.inputHashes['browser-check.mjs']===hash(path.join(dir,'browser-check.mjs')),'stale browser harness '+width);assert(r.cleanup.profileRemoved&&!r.cleanup.remainingOwnedPids.length,'cleanup '+width);metrics.browser.push({width,height:r.height,views:r.traversal.views,interactionAssertions:r.interaction.length,firstReadingFont:r.firstReadingFont,nonzeroScroll:r.nonzeroScroll,errors:r.errors.length,remoteRequests:r.remoteRuntimeRequests.length,cleanup:r.cleanup});
}
metrics.audit=JSON.parse(read('qa/structural.json'));assert(!metrics.audit.failures.length,'structural failure');
metrics.rootPersonalAcceptance=false;metrics.publicationAllowed=false;
fs.writeFileSync(path.join(dir,'metrics.json'),JSON.stringify(metrics,null,2)+'\n');
console.log(JSON.stringify({modes:Object.fromEntries(Object.entries(metrics.modes).map(([m,v])=>[m,{screens:v.screens,ru:v.ru,en:v.en}])),browser:metrics.browser.map(r=>({width:r.width,views:r.views,scroll:r.nonzeroScroll})),immutableInputs:metrics.immutableInputs.length},null,2));

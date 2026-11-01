from pathlib import Path
import hashlib,json

H=Path(__file__).resolve().parent.parent
R=H/'root-review';Q=R/'qa';Q.mkdir(exist_ok=True)
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
l=load(R/'reading-ledger.json')
assert len(l['deepReadPairIds'])==68 and len(l['essentialReadPairIds'])==24 and len(l['coreAddedPairsReread'])==24
assert set(l['finalChangedPairIdsReread'])==set(l['repairsImplementedPairIds']) and len(l['finalChangedPairIdsReread'])==14
assert all(f['status']=='repaired-and-personally-reread' for f in l['pendingFindings'])
l.update(allCurrentPairsRead=True,rootPersonalAcceptance=False,publicationAllowed=False,currentFinalStoryDataSha256=sha(H/'story-data.json'),shorterRouteReadingMethod='All68 original RU/EN Deep pairs completely read. All24 Essential pairs reread in order, with final edited entries reread after repair. All24 Core additions reread completely with both adjacent route edges; common Essential prose had already been reread. All14 final changed pairs personally reread. No third complete rereading of identical shared prose is claimed.')
(R/'reading-ledger.json').write_text(json.dumps(l,ensure_ascii=False,indent=2)+'\n')

checks=[
 ('jake-origin',5,31,53),('jz-origin',7,7,24),('sprint-laboratory',5,54,68),
 ('four-stages-and-imperfect-use',6,1,33),('highlight-choice-size-revision',7,30,70),('list-alternatives',9,58,87),
 ('calendar-and-boundaries',11,1,52),('morning-evening-and-stopping',11,53,97),('useful-notifications-urgent-channel',14,34,44),
 ('harriet-gains-and-losses',16,10,16),('router-and-time-craters',16,44,75),('email-exceptions-announcement',18,21,26),('time-zone-calculation',18,42,56),
 ('involvement-and-rest',24,15,30),('basketball-stroller-and-movement',27,1,22),('different-fasting-snack-choices',29,12,27),('chocolate-notes',53,40,41),
 ('caffeine-not-universal',31,7,14),('caffeine-cutoff',31,31,39),('actual-breaks',33,31,43),
 ('caregiving',37,32,37),('sleep-rhythm',37,26,31),('reflection-hypotheses-prompts',38,12,24),('actual-reflection-and-feedback',40,1,23),
 ('life-pivots',41,7,18),('actual-three-day-start',42,1,10)
]
(R/'primary-selection-plan.json').write_text(json.dumps({'scope':'26 suggested actual source intervals from sources.md. Root actual28 bounded reads are separate; no whole-primary reading claim.','checks':[{'label':label,'record':i,'start':a,'end':b,'indexBase':1,'inclusive':True} for label,i,a,b in checks]},ensure_ascii=False,indent=2)+'\n')

s=(H.parent/'a-guide-to-the-good-life/root-review/cold-settings.mjs').read_text()
for a,b in [('a-guide-to-the-good-life','make-time'),('irvine-root-cold-','make-time-root-cold-'),('modern-adaptation','life-pivot'),('trial-with-feedback','caffeine-cutoff'),('mother-and-water-continued','lost-winter'),('mother-and-water','wooden-railway'),('medication-objection','brief-workout'),('reconstructed-stoicism','fasting-snacks'),('final-doubt','final'),('whole-life','two-streams')]:
 s=s.replace(a,b)
s=s.replace('length===2','length===1').replace('both nonfiction sources','the nonfiction source')
s=s.replace("if(phase==='cold'){", "if(phase==='cold'){\n  report.actualColdViewport={width:320,height:568};")
(R/'cold-settings.mjs').write_text(s)

s=(H/'measure.mjs').read_text().split('metrics.browser=[];')[0]
s=s.replace("const dir=path.dirname(fileURLToPath(import.meta.url)),", "const dir=path.dirname(path.dirname(fileURLToPath(import.meta.url))),")
s+='''
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
fs.writeFileSync(path.join(dir,'root-review/qa/metrics.json'),JSON.stringify(metrics,null,2)+'\\n');
fs.writeFileSync(path.join(dir,'root-review/qa/parity-check.json'),JSON.stringify({atUtc:new Date().toISOString(),allAuthoredFieldsMatchEmbedding:Object.keys(d).every(k=>JSON.stringify(d[k])===JSON.stringify(e[k])),draftParagraphs:metrics.parity,allSixRoutesExact:true,changedPairIds:changed,counts:d.targetModes,currentContentHashes:metrics.currentContentHashes,rootPersonalAcceptance:false,publicationAllowed:false},null,2)+'\\n');
console.log(JSON.stringify({counts:d.targetModes,bodyWords:Object.fromEntries(Object.entries(metrics.modes).map(([mode,v])=>[mode,{ru:v.ru.noncoverBodyWords,en:v.en.noncoverBodyWords}])),changedPairs:changed.length,sourceCount:d.sources.length,protectedInputs:metrics.immutableInputs.length}));
'''
(R/'verify.mjs').write_text(s)
print(json.dumps({'rootRead':68,'essentialReread':24,'coreAdditionsReread':24,'changedReread':14,'suggestedPrimaryIntervals':len(checks),'primaryActualRanges':len(l['primaryRangesActuallyRead']),'rootAcceptance':False}))

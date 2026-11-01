from pathlib import Path
import json, hashlib

H = Path(__file__).resolve().parent.parent
R = H / 'root-review'
parent = H.parent / 'white-fang' / 'root-review'
s = (parent / 'cold-settings.mjs').read_text()
for a,b in [
    ('white-fang','children-of-captain-grant'),
    ('fang-root-cold-','grant-root-cold-'),
    ('quiet-last-image','paganel-secret'),
    ('iv-3-p3','bar'), ('iv-4-p4','bar'), ('iv-4-p5','farm'),
    ('v-3-p2','kara-tete'), ('v-5-p3','father'),
    ('When the light came on','Introducing his friends'),
    ('Когда зажёгся свет','Представить друзей'),
    ('i-1-p1','shark'), ('length===86','length===113'),
    ('length===49','length===67')
]:
    s = s.replace(a,b)
s = s.replace("ok(report.coldBefore.scroll>0&&report.coldBefore.font==='sans','meaningful nonzero cold scroll');", "ok(report.coldBefore.scroll>0&&report.coldBefore.font==='sans','meaningful nonzero cold scroll');ok(report.coldBefore.serifStatus.length>0&&report.coldBefore.serifStatus.every(s=>s==='unloaded'),'Serif genuinely cold before first selection');")
(R / 'cold-settings.mjs').write_text(s)
s = (parent / 'verify.mjs').read_text().replace('white-fang','children-of-captain-grant')
s = s.replace("for(const m of ['essential','core','deep'])assert(JSON.stringify(a.modes[m].label)===JSON.stringify(e.modes[m].label),'mode label parity');", "assert(!a.modes,'authoring has only generated runtime mode labels');")
s = s.replace("s=>s.narrative", "s=>Number.isInteger(s.draftParagraph)")
s = s.replace("s=>!s.narrative", "s=>!Number.isInteger(s.draftParagraph)")
s = s.replace('Narrative = only narrative:true bodies.', 'Narrative = only integer draftParagraph bodies.')
s = s.replace("read(`draft-${l}.md`).split('\\n## ').slice(1).flatMap(s=>s.trim().split('\\n\\n').slice(1))", "read(`draft-${l}.md`).split(/^## /m).slice(1).flatMap(s=>s.split('\\n\\n').slice(1).map(p=>p.trim()).filter(Boolean))")
s = s.replace("for(const l of ['ru','en']){", "for(const l of ['ru','en']){", 1)
needle = "const prev=JSON.parse(read('root-review/protected-baseline.json'))"
prefix = "const narrativeIds=a.screens.filter(s=>Number.isInteger(s.draftParagraph)).map(s=>s.id);const prefixProof={};for(const [m,lv,n] of [['essential',1,24],['core',2,67]]){const ids=a.screens.filter(s=>s.level<=lv&&Number.isInteger(s.draftParagraph)).map(s=>s.id);assert(JSON.stringify(ids)===JSON.stringify(narrativeIds.slice(0,n)),m+' is exact continuous already-read prefix');prefixProof[m]={paragraphs:n,ids,exactPrefixOfDeep:true};}fs.writeFileSync(path.join(d,'root-review','qa','shorter-prefix-proof.json'),JSON.stringify(prefixProof,null,2)+'\\n');\n"
assert needle in s
s = s.replace(needle, prefix + needle)
(R / 'verify.mjs').write_text(s)

library = H.parents[3]
paths = [Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-1-private/children-of-captain-grant/primary.txt')]
paths += [library / 'collector-output' / 'children-of-captain-grant' / n for n in ['story-data.json','children-of-captain-grant.html','sources.md','QA.md']]
paths += [library / 'children-of-captain-grant.html', library / 'books.json']
installed = Path('/Users/pn/.codex/skills/book-tiktok')
paths += [installed / n for n in ['SKILL.md','scripts/build_story.mjs','scripts/reader-settings.mjs','assets/standalone-template.html','assets/reader-settings-head.html','assets/reader-settings.html','assets/reader-header.html']]
assert all(p.is_file() for p in paths)
baseline={'scope':'Root QA start snapshot of primary witness, previous collector/root reader/catalogue, installed shared code; not an implementation-wide provenance claim.','files':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]}
assert not (R / 'protected-baseline.json').exists(), 'Do not overwrite the original protected baseline.'
(R / 'protected-baseline.json').write_text(json.dumps(baseline, indent=2)+'\n')

ledger=json.loads((R / 'reading-ledger.json').read_text())
ledger['allCurrentPairsRead']=True
ledger['finalChangedPairIdsReread']=['wolves','telegram','father','arabella']
ledger['lastAdditionalTelegramEditReread']=True
for mode,level in [('essential',1),('core',2)]:
    data=json.loads((H/'story-data.json').read_text())
    ledger[mode+'ReadPairIds']=[x['id'] for x in data['screens'] if x['level']<=level]
ledger['shorterRouteReadingMethod']='All included prose already read sequentially in Deep; exact continuous 24/67-paragraph prefixes checked mechanically, shared cover/final and each cut boundary read again. No separate second complete rereading of the identical Core prose is claimed.'
for r in [[15765,15928],[15960,16239],[16240,16603],[17060,17365],[9370,9564]]:
    if r not in ledger['primaryRangesActuallyRead']: ledger['primaryRangesActuallyRead'].append(r)
for f in ledger['pendingFindings']:
    f['finding']=f['finding'].replace('Primary V? Horne3.20', 'Primary Horne3.20')
    f['status']='repaired-and-personally-reread'
ledger['rootPersonalAcceptance']=False
ledger['publicationAllowed']=False
ledger['finalReadingStorySha256']=hashlib.sha256((H/'story-data.json').read_bytes()).hexdigest()
(R / 'reading-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
print('Prepared root QA and '+str(len(paths))+' protected input bindings. Acceptance remains false.')

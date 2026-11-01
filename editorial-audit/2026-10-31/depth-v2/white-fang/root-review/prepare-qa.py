from pathlib import Path
import json, hashlib
H = Path(__file__).resolve().parent.parent
R = H / 'root-review'
parent = H.parent / 'the-lost-world' / 'root-review'
s = (parent / 'cold-settings.mjs').read_text()
for a,b in [('the-lost-world','white-fang'),('lost-root-cold-','fang-root-cold-'),('diamonds-choice','quiet-last-image'),('balloon-test','iv-3-p3'),('shotgun','iv-4-p4'),('asphalt','iv-4-p5'),('bark','v-3-p2'),("'hand'","'v-5-p3'"),('Across the table','When the light came on'),('\u0427\u0435\u0440\u0435\u0437 \u0441\u0442\u043e\u043b','\u041a\u043e\u0433\u0434\u0430 \u0437\u0430\u0436\u0451\u0433\u0441\u044f \u0441\u0432\u0435\u0442'),("go('money')","go('i-1-p1')"),('length===122','length===86'),('length===66','length===49')]:
    s = s.replace(a,b)
(R / 'cold-settings.mjs').write_text(s)
s = (parent / 'verify.mjs').read_text().replace('the-lost-world','white-fang')
a = "read(`draft-${l}.md`).split(/^## [IVX]+\\n/gm).slice(1).flatMap(s=>s.trim().split('\\n\\n'))"
b = "read(`draft-${l}.md`).split('\\n## ').slice(1).flatMap(s=>s.trim().split('\\n\\n').slice(1))"
assert a in s
s = s.replace(a,b).replace("read('protected-baseline.json')", "read('root-review/protected-baseline.json')")
(R / 'verify.mjs').write_text(s)
library = H.parents[3]
paths = [Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-1-private/white-fang/primary.txt')]
paths += [library / 'collector-output' / 'white-fang' / n for n in ['story-data.json','white-fang.html','sources.md','QA.md']]
paths += [library / 'white-fang.html', library / 'books.json']
installed = Path('/Users/pn/.codex/skills/book-tiktok')
paths += [installed / n for n in ['SKILL.md','scripts/build_story.mjs','scripts/reader-settings.mjs','assets/standalone-template.html','assets/reader-settings-head.html','assets/reader-settings.html','assets/reader-header.html']]
assert all(p.is_file() for p in paths), [str(p) for p in paths if not p.is_file()]
baseline={'scope':'Root QA start snapshot of primary witness, previous collector/root reader/catalogue, installed shared code; not an implementation-wide provenance claim.','files':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]}
(R / 'protected-baseline.json').write_text(json.dumps(baseline, indent=2)+'\n')
print('Prepared root QA and '+str(len(paths))+' protected input bindings.')

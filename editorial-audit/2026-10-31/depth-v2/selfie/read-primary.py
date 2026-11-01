import json,sys,hashlib
from pathlib import Path
b=Path(__file__).parent
p=Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-8-private/selfie-edition.json')
d={a['file']:a['paragraphs'] for a in json.loads(p.read_text())}
plan=json.loads((b/'reading-plan.json').read_text())
n=int(sys.argv[1]);c=plan['chunks'][n-1]
print('CHUNK',n,'OF',len(plan['chunks']))
for r in c:
 t=d[r['file']][r['p']-1];assert hashlib.sha256(t.encode()).hexdigest()==r['sha256']
 print(f"[{r['file']} P{r['p']:03d}] {t}\n")
print('END CHUNK',n)

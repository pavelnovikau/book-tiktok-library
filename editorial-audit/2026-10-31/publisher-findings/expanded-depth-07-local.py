from pathlib import Path
import json, subprocess, hashlib, datetime

P=Path('/Users/pn/.t3/checkouts/book-tiktok-library-release07-20261031')
C=Path('/Users/pn/smartcat/_artifacts/book-tiktok-library')
rel=Path('editorial-audit/2026-10-31');A=C/rel
slug='why-zebras-dont-get-ulcers';h=A/'depth-v2'/slug
sha=lambda b:hashlib.sha256(b).hexdigest()
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip();assert base=='31de7b228e630e1e34e5787ea5d178f2796db821'
old=json.loads(subprocess.check_output(['git','show',base+':books.json'],cwd=P,text=True));new=json.loads((P/'books.json').read_text())
assert {k:v for k,v in old.items() if k!='books'}=={k:v for k,v in new.items() if k!='books'}
assert len(old['books'])==len(new['books'])==58
for x,y in zip(old['books'],new['books']):
    assert x['slug']==y['slug']
    if x['slug']==slug:assert {k:v for k,v in x.items() if k not in ['screenCount','readingMinutes']}=={k:v for k,v in y.items() if k not in ['screenCount','readingMinutes']}
    else:assert x==y
assert sum(x['screenCount'] for x in new['books'])==2671
names=subprocess.check_output(['git','ls-tree','--name-only',base],cwd=P,text=True).splitlines();roots=[n for n in names if n.endswith('.html') and n!=slug+'.html']
for n in roots:assert (P/n).read_bytes()==subprocess.check_output(['git','show',base+':'+n],cwd=P)
assets={str(p.relative_to(P/'public')):sha(p.read_bytes()) for p in sorted((P/'public').rglob('*')) if p.is_file()}
assert len(assets)==69 and not any(n.startswith(('editorial-audit/','collector-output/','sources/')) for n in assets)
ready=json.loads((h/'ready.json').read_text())
for name,r in ready['allArtifactHashes'].items():
    assert sha(Path(r['path']).read_bytes())==r['sha256'],name
    assert sha((P/rel/'depth-v2'/slug/name).read_bytes())==r['sha256'],name
assert assets[slug+'.html']==sha((h/(slug+'.html')).read_bytes())==sha((P/(slug+'.html')).read_bytes())
r=subprocess.run(['git','diff','--cached','--check'],cwd=P,capture_output=True,text=True)
assert not r.stderr
if r.returncode:
    lines=r.stdout.splitlines();assert len(lines)==2 and lines[0].startswith(str(rel/'depth-v2'/slug/(slug+'.html'))+':') and lines[0].endswith('trailing whitespace.') and lines[1]=='+fonts, including any derivative works, can be bundled, embedded, ',lines
    assert 'fonts, including any derivative works, can be bundled, embedded, \n' in subprocess.check_output(['git','show',base+':'+slug+'.html'],cwd=P,text=True)
report={'atUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','slug':slug,'baseMerge':base,'catalogueBooks':58,'catalogueScreens':2671,'all57OtherCatalogueEntriesUnchanged':True,'allOtherRootHtmlUnchanged':len(roots),'candidateBindingsVerifiedInBothCopies':len(ready['allArtifactHashes']),'acceptedRootAndCompiledHtmlExact':True,'privateEvidenceExcluded':True,'compiledPublicAssetHashes':assets,'localChecks':['npm run check','npm run build:site'],'rootQa':'depth-v2/'+slug+'/root-review/personal-review.json','productionClaim':False,'whitespaceCheck':{'inheritedLicenseFinding':'One trailing space in the bundled OFL license is identical to the base reader. Exact accepted runtime bytes preserved.','allOtherFindings':0}}
for root in [C,P]:(root/rel/'publisher-findings/expanded-depth-07-local.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','unchangedRootHtml':len(roots),'publicAssets':len(assets),'bindings':len(ready['allArtifactHashes']),'inheritedLicenseLine':1}))

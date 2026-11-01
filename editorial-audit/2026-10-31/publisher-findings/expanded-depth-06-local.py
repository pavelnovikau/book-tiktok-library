import json, subprocess, hashlib, datetime
from pathlib import Path

P=Path('/Users/pn/.t3/checkouts/book-tiktok-library-release07-20261031')
C=Path('/Users/pn/smartcat/_artifacts/book-tiktok-library')
rel=Path('editorial-audit/2026-10-31');A=C/rel
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip()
old=json.loads(subprocess.check_output(['git','show',base+':books.json'],cwd=P,text=True))
new=json.loads((P/'books.json').read_text());slug='children-of-captain-grant'
sha=lambda b:hashlib.sha256(b).hexdigest()
assert {k:v for k,v in old.items() if k!='books'}=={k:v for k,v in new.items() if k!='books'}
assert len(old['books'])==len(new['books'])==58
for x,y in zip(old['books'],new['books']):
    assert x['slug']==y['slug']
    if x['slug']==slug:
        assert {k:v for k,v in x.items() if k not in ['screenCount','readingMinutes']}=={k:v for k,v in y.items() if k not in ['screenCount','readingMinutes']}
    else:assert x==y
names=subprocess.check_output(['git','ls-tree','--name-only',base],cwd=P,text=True).splitlines()
roots=[n for n in names if n.endswith('.html') and n!=slug+'.html']
for n in roots:assert (P/n).read_bytes()==subprocess.check_output(['git','show',base+':'+n],cwd=P)
public=P/'public';assert public.is_dir()
assets={str(p.relative_to(public)):sha(p.read_bytes()) for p in sorted(public.rglob('*')) if p.is_file()}
assert len(assets)==69 and not any(n.startswith(('editorial-audit/','collector-output/','sources/')) for n in assets)
h=A/'depth-v2'/slug
assert assets[slug+'.html']==sha((h/(slug+'.html')).read_bytes())==sha((P/(slug+'.html')).read_bytes())
diff=subprocess.run(['git','diff','--cached','--check'],cwd=P,capture_output=True,text=True)
lines=diff.stdout.splitlines();assert not diff.stderr
blank_eof_paths={
 'editorial-audit/2026-10-31/depth-v2/'+slug+'/browser-check.mjs',
 *['editorial-audit/2026-10-31/depth-v2/'+slug+'/routes/'+n for n in ['core-en.md','core-ru.md','essential-en.md','essential-ru.md']],
 'editorial-audit/2026-10-31/publisher-findings/expanded-depth-05-readiness.json',
 'editorial-audit/2026-10-31/publisher-findings/expanded-depth-05-review-threads.json'
}
if diff.returncode:
    blanks=[s for s in lines if s.endswith(': new blank line at EOF.')]
    assert {s.rsplit(':',2)[0] for s in blanks}==blank_eof_paths,blanks
    other=[s for s in lines if s not in blanks]
    assert len(other)==2 and other[0].startswith('editorial-audit/2026-10-31/depth-v2/'+slug+'/'+slug+'.html:') and 'trailing whitespace.' in other[0] and other[1]=='+fonts, including any derivative works, can be bundled, embedded, ',other
    oldh=subprocess.check_output(['git','show',base+':'+slug+'.html'],cwd=P).decode()
    assert 'fonts, including any derivative works, can be bundled, embedded, \n' in oldh
report={
 'atUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','slug':slug,'baseMerge':base,
 'catalogueBooks':58,'catalogueScreens':2615,'all57OtherCatalogueEntriesUnchanged':True,
 'allOtherRootHtmlUnchanged':len(roots),'acceptedRootAndCompiledHtmlExact':True,'privateEvidenceExcluded':True,
 'compiledPublicAssetHashes':assets,'localChecks':['npm run check','npm run build:site'],
 'rootQa':'depth-v2/'+slug+'/root-review/personal-review.json','productionClaim':False,
 'whitespaceCheck':{'inheritedLicenseFinding':'Existing upstream OFL license line retains one trailing space in the private exact-hash duplicate; identical literal is in the base root reader. Runtime bytes preserved.','preservedPrivateArtifactBlankEofPaths':sorted(blank_eof_paths),'reason':'Keep accepted candidate bindings and historical raw CI/review evidence byte-identical. These are private EOF-only findings, not runtime or prose defects.','allOtherFindings':0}
}
for dest in [A/'publisher-findings/expanded-depth-06-local.json',P/rel/'publisher-findings/expanded-depth-06-local.json']:
    dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'unchangedRootHtml':len(roots),'publicAssets':len(assets),'targetDescription':next(x for x in new['books'] if x['slug']==slug)['description'],'preservedPrivateBlankEofFiles':len(blank_eof_paths),'inheritedLicenseLine':1},ensure_ascii=False))

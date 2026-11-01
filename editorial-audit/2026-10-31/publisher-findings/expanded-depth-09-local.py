from pathlib import Path
import datetime
import hashlib
import json
import subprocess

P = Path('/Users/pn/.t3/checkouts/book-tiktok-library-release07-20261031')
C = Path('/Users/pn/smartcat/_artifacts/book-tiktok-library')
rel = Path('editorial-audit/2026-10-31')
A = C / rel
slug = 'make-time'
H = A / 'depth-v2' / slug
sha = lambda b: hashlib.sha256(b).hexdigest()
base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=P, text=True).strip()
assert base == '835f006db9333b5f56076e9f8797d3da39af59ca'
old = json.loads(subprocess.check_output(['git', 'show', base + ':books.json'], cwd=P, text=True))
new = json.loads((P / 'books.json').read_text())
assert {k:v for k,v in old.items() if k != 'books'} == {k:v for k,v in new.items() if k != 'books'}
assert len(old['books']) == len(new['books']) == 58
for x,y in zip(old['books'],new['books']):
    assert x['slug'] == y['slug']
    if x['slug'] == slug:
        assert {k:v for k,v in x.items() if k not in ['screenCount','readingMinutes']} == {k:v for k,v in y.items() if k not in ['screenCount','readingMinutes']}
    else:
        assert x == y
assert sum(x['screenCount'] for x in new['books']) == 2737
names = subprocess.check_output(['git','ls-tree','--name-only',base],cwd=P,text=True).splitlines()
roots = [n for n in names if n.endswith('.html') and n != slug + '.html']
for name in roots:
    assert (P/name).read_bytes() == subprocess.check_output(['git','show',base+':'+name],cwd=P)
assets = {str(p.relative_to(P/'public')):sha(p.read_bytes()) for p in sorted((P/'public').rglob('*')) if p.is_file()}
assert len(assets) == 69 and not any(n.startswith(('editorial-audit/','collector-output/','sources/')) for n in assets)
ready = json.loads((H/'ready.json').read_text())
for name,row in ready['allArtifactHashes'].items():
    assert sha(Path(row['path']).read_bytes()) == row['sha256'],name
    assert sha((P/rel/'depth-v2'/slug/name).read_bytes()) == row['sha256'],name
assert assets[slug+'.html'] == sha((H/(slug+'.html')).read_bytes()) == sha((P/(slug+'.html')).read_bytes())
r = subprocess.run(['git','diff','--cached','--check'],cwd=P,capture_output=True,text=True)
assert not r.stderr
if r.returncode:
    lines = r.stdout.splitlines()
    expected = [
        'editorial-audit/2026-10-31/depth-v2/make-time/coverage-map.md:330: new blank line at EOF.',
        'editorial-audit/2026-10-31/depth-v2/make-time/make-time.html:1374: trailing whitespace.',
        '+fonts, including any derivative works, can be bundled, embedded, ',
        'editorial-audit/2026-10-31/depth-v2/make-time/reader/assets/fonts/SourceSerif4-LICENSE.md:21: trailing whitespace.',
        '+fonts, including any derivative works, can be bundled, embedded, ',
        'editorial-audit/2026-10-31/depth-v2/make-time/root-review/ack-pairs.py:16: new blank line at EOF.',
        'editorial-audit/2026-10-31/depth-v2/make-time/root-review/input-coverage-map.md:326: new blank line at EOF.',
        'editorial-audit/2026-10-31/depth-v2/make-time/root-review/read-pairs.py:22: new blank line at EOF.'
    ]
    assert lines == expected,lines
    assert 'fonts, including any derivative works, can be bundled, embedded, \n' in subprocess.check_output(['git','show',base+':'+slug+'.html'],cwd=P,text=True)
    assert 'fonts, including any derivative works, can be bundled, embedded, \n' in (H/'reader/assets/fonts/SourceSerif4-LICENSE.md').read_text()
    for n in ['coverage-map.md','root-review/ack-pairs.py','root-review/input-coverage-map.md','root-review/read-pairs.py']:
        assert (H/n).read_bytes().endswith(b'\n\n'),n
report = {'atUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','slug':slug,'baseMerge':base,'catalogueBooks':58,'catalogueScreens':2737,'all57OtherCatalogueEntriesUnchanged':True,'allOtherRootHtmlUnchanged':len(roots),'candidateBindingsVerifiedInBothCopies':len(ready['allArtifactHashes']),'acceptedRootAndCompiledHtmlExact':True,'privateEvidenceExcluded':True,'compiledPublicAssetHashes':assets,'localChecks':['npm run check','npm run build:site'],'rootQa':'depth-v2/'+slug+'/root-review/personal-review.json','productionClaim':False,'whitespaceCheck':{'inheritedLicenseFinding':'Two exact copies of the same OFL trailing-space line; already present in base reader.','privateEvidenceBlankEof':4,'allOtherFindings':0,'frozenAcceptedFilesPreserved':True}}
for root in [C,P]:
    (root/rel/'publisher-findings/expanded-depth-09-local.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','unchangedRootHtml':len(roots),'publicAssets':len(assets),'bindings':len(ready['allArtifactHashes']),'inheritedLicenseCopies':2,'privateEofFindings':4}))

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import datetime
import hashlib
import json

C = Path('/Users/pn/smartcat/_artifacts/book-tiktok-library')
P = Path('/Users/pn/.t3/checkouts/book-tiktok-library-release07-20261031')
rel = Path('editorial-audit/2026-10-31/publisher-findings')
local = json.loads((C/rel/'expanded-depth-09-local.json').read_text())
merge = json.loads((C/rel/'expanded-depth-09-merge.json').read_text())
assert merge['merged']
ready = json.loads((C/rel/'expanded-depth-09-readiness.json').read_text())
head = ready['headRefOid']
names = ['make-time.html','books.json','index.html','hard-to-be-a-god.html','thinking-fast-and-slow.html','treasure-island.html','the-lost-world.html','white-fang.html','children-of-captain-grant.html','why-zebras-dont-get-ulcers.html','a-guide-to-the-good-life.html']
private = ['/collector-output/make-time/story-data.json','/editorial-audit/2026-10-31/depth-v2/make-time/draft-ru.md']
routes = {n:('/' if n == 'index.html' else '/' + n[:-5] if n.endswith('.html') else '/' + n) for n in names}

def get(row):
    name, route, expected = row
    url = 'https://book-tiktok-library.vercel.app' + route + '?release=' + head[:8]
    req = Request(url,headers={'Cache-Control':'no-cache','User-Agent':'BookLibraryReleaseVerification/1.0'})
    try:
        with urlopen(req,timeout=25) as response:
            body = response.read(); status = response.status
        got = hashlib.sha256(body).hexdigest()
        result = {'name':name,'url':url,'status':status,'expectedSha256':expected,'actualSha256':got,'matches':status == 200 and got == expected}
        if name == 'books.json':
            cat = json.loads(body)
            result.update(catalogueBooks=len(cat['books']),catalogueScreens=sum(x['screenCount'] for x in cat['books']))
        return result
    except HTTPError as e:
        return {'name':name,'url':url,'status':e.code,'expectedSha256':expected,'matches':expected is None and e.code == 404}
    except Exception as e:
        return {'name':name,'url':url,'error':str(e),'matches':False}

jobs = [(n,routes[n],local['compiledPublicAssetHashes'][n]) for n in names] + [(n,n,None) for n in private]
with ThreadPoolExecutor(max_workers=12) as pool:
    results = list(pool.map(get,jobs))
assets = results[:len(names)]
hidden = results[len(names):]
proof = {'atUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':ready['url'],'head':head,'merge':merge['sha'],'singlePostMergeObservation':True,'publicAssets':assets,'privatePaths':hidden,'changedAssetsAndCanariesMatch':all(x['matches'] for x in assets),'private404sMatch':all(x['matches'] for x in hidden),'allCurrentProductionAssetsVerified':False,'scope':'Fresh exact HTTP hashes for changed Make Time reader/catalogue, homepage and eight earlier root-accepted expanded books. Other assets unchanged locally; not all69 freshly fetched.'}
for root in [C,P]:
    (root/rel/'expanded-depth-09-production.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'assets':len(assets),'matches':sum(x['matches'] for x in assets),'private404s':sum(x['matches'] for x in hidden),'catalogue':next((x.get('catalogueBooks'),x.get('catalogueScreens')) for x in assets if x['name'] == 'books.json')}))
assert proof['changedAssetsAndCanariesMatch'] and proof['private404sMatch'], 'Production not yet verified; do not poll or claim live.'

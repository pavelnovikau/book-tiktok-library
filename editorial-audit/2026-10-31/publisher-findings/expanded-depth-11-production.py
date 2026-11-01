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
load = lambda name: json.loads((C/rel/name).read_text())
local = load('expanded-depth-11-local.json')
merge = load('expanded-depth-11-merge.json')
readiness = load('expanded-depth-11-readiness.json')
assert merge['merged']
head = readiness['headRefOid']
names = ['four-thousand-weeks.html','books.json','index.html','hard-to-be-a-god.html','thinking-fast-and-slow.html','treasure-island.html','the-lost-world.html','white-fang.html','children-of-captain-grant.html','why-zebras-dont-get-ulcers.html','a-guide-to-the-good-life.html','make-time.html','essentialism.html']
private = ['/collector-output/four-thousand-weeks/story-data.json','/editorial-audit/2026-10-31/depth-v2/four-thousand-weeks/draft.ru.md']
def get(row):
    name, route, expected = row
    url = 'https://book-tiktok-library.vercel.app'+route+'?release='+head[:8]
    try:
        with urlopen(Request(url,headers={'Cache-Control':'no-cache','User-Agent':'BookLibraryReleaseVerification/1.0'}),timeout=25) as response:
            body=response.read();status=response.status
        digest=hashlib.sha256(body).hexdigest()
        result={'name':name,'url':url,'status':status,'expectedSha256':expected,'actualSha256':digest,'matches':status==200 and digest==expected}
        if name=='books.json':
            cat=json.loads(body);result.update(catalogueBooks=len(cat['books']),catalogueScreens=sum(x['screenCount'] for x in cat['books']))
        return result
    except HTTPError as e:
        return {'name':name,'url':url,'status':e.code,'expectedSha256':expected,'matches':expected is None and e.code==404}
    except Exception as e:
        return {'name':name,'url':url,'error':str(e),'matches':False}
jobs=[(n,'/' if n=='index.html' else '/'+n[:-5] if n.endswith('.html') else '/'+n,local['compiledPublicAssetHashes'][n]) for n in names]+[(n,n,None) for n in private]
with ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(get,jobs))
assets=results[:len(names)];hidden=results[len(names):]
proof={'atUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':readiness['url'],'head':head,'merge':merge['sha'],'singlePostMergeObservation':True,'publicAssets':assets,'privatePaths':hidden,'changedReaderCatalogueAndHomepageMatch':all(x['matches'] for x in assets[:3]),'changedAssetsAndCanariesMatch':all(x['matches'] for x in assets),'private404sMatch':all(x['matches'] for x in hidden),'allCurrentProductionAssetsVerified':False,'scope':'One fresh HTTP observation of changed Four Thousand Weeks reader/catalogue, homepage and ten prior accepted expanded readers. Other compiled assets unchanged locally; not all69 freshly fetched. Transport failures remain unverified observations and are not retried.'}
for root in [C,P]:(root/rel/'expanded-depth-11-production.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'assetsAttempted':len(assets),'assetHashesMatched':sum(x['matches'] for x in assets),'changedReaderCatalogueHomepageMatch':proof['changedReaderCatalogueAndHomepageMatch'],'private404s':sum(x['matches'] for x in hidden),'failures':[x for x in assets if not x['matches']]}))
assert proof['changedReaderCatalogueAndHomepageMatch'] and proof['private404sMatch'],'Changed production not yet verified; do not poll or claim live.'
assert not [x for x in assets[3:] if not x['matches'] and 'error' not in x],'Observed canary mismatch requires investigation; do not claim all assets unchanged.'

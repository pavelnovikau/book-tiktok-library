from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json,hashlib,datetime

C=Path('/Users/pn/smartcat/_artifacts/book-tiktok-library')
P=Path('/Users/pn/.t3/checkouts/book-tiktok-library-release07-20261031')
rel=Path('editorial-audit/2026-10-31/publisher-findings')
local=json.loads((C/rel/'expanded-depth-06-local.json').read_text())
merge=json.loads((C/rel/'expanded-depth-06-merge.json').read_text())
assert merge['merged'] and merge['sha']=='31de7b228e630e1e34e5787ea5d178f2796db821'
head='f45afafa787ca2ba6aa9b477c1e4f73ad8bf79c3'
names=['children-of-captain-grant.html','books.json','index.html','hard-to-be-a-god.html','thinking-fast-and-slow.html','treasure-island.html','the-lost-world.html','white-fang.html']
private=['/collector-output/children-of-captain-grant/story-data.json','/editorial-audit/2026-10-31/depth-v2/children-of-captain-grant/draft-ru.md']
routes={n:('/' if n=='index.html' else '/'+n[:-5] if n.endswith('.html') else '/'+n) for n in names}
def get(row):
    name,route,expected=row
    url='https://book-tiktok-library.vercel.app'+route+'?release='+head[:8]
    req=Request(url,headers={'Cache-Control':'no-cache','User-Agent':'BookLibraryReleaseVerification/1.0'})
    try:
        with urlopen(req,timeout=25) as r:
            body=r.read();status=r.status
        got=hashlib.sha256(body).hexdigest()
        result={'name':name,'url':url,'status':status,'expectedSha256':expected,'actualSha256':got,'matches':status==200 and got==expected}
        if name=='books.json':
            cat=json.loads(body);result['catalogueBooks']=len(cat['books']);result['catalogueScreens']=sum(x['screenCount'] for x in cat['books'])
        return result
    except HTTPError as e:return {'name':name,'url':url,'status':e.code,'expectedSha256':expected,'matches':expected is None and e.code==404}
    except Exception as e:return {'name':name,'url':url,'error':str(e),'matches':False}
jobs=[(n,routes[n],local['compiledPublicAssetHashes'][n]) for n in names]+[(n,n,None) for n in private]
with ThreadPoolExecutor(max_workers=10) as pool: results=list(pool.map(get,jobs))
assets=results[:len(names)];hidden=results[len(names):]
proof={'atUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':'https://github.com/pavelnovikau/book-tiktok-library/pull/42','head':head,'merge':merge['sha'],'singlePostMergeObservation':True,'publicAssets':assets,'privatePaths':hidden,'changedAssetsAndCanariesMatch':all(x['matches'] for x in assets),'private404sMatch':all(x['matches'] for x in hidden),'allCurrentProductionAssetsVerified':False,'scope':'Fresh exact hashes for changed reader/catalogue, unchanged homepage and five earlier root-accepted expanded readers. Other public assets were proved unchanged locally; not freshly fetched in this observation.'}
for root in [C,P]:(root/rel/'expanded-depth-06-production.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'assets':len(assets),'matches':sum(x['matches'] for x in assets),'private404s':sum(x['matches'] for x in hidden),'catalogue':next((x.get('catalogueBooks'),x.get('catalogueScreens')) for x in assets if x['name']=='books.json'),'allCurrentProductionAssetsVerified':False},ensure_ascii=False))
assert proof['changedAssetsAndCanariesMatch'] and proof['private404sMatch'],'Production not yet verified; no polling or live claim.'

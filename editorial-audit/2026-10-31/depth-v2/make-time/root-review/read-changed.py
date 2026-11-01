from pathlib import Path
import html,json,re,sys
H=Path(__file__).resolve().parent.parent;R=H/'root-review'
d=json.loads((H/'story-data.json').read_text());l=json.loads((R/'reading-ledger.json').read_text());changed=set(l['repairsImplementedPairIds'])
screens=[s for s in d['screens'] if s['id'] in changed]
a=int(sys.argv[1]);b=int(sys.argv[2]);assert 1<=a<=b<=len(screens)
if len(sys.argv)>3 and sys.argv[3]=='ack':
 l.setdefault('finalChangedPairIdsReread',[])
 for s in screens[a-1:b]:
  assert s['id'] not in l['finalChangedPairIdsReread']
  l['finalChangedPairIdsReread'].append(s['id'])
 (R/'reading-ledger.json').write_text(json.dumps(l,ensure_ascii=False,indent=2)+'\n');print('Final changed pairs reread',len(l['finalChangedPairIdsReread']))
else:
 for n,s in enumerate(screens[a-1:b],a):
  print(f'\nCHANGED PAIR{n}/{len(screens)} {s["id"]} LEVEL{s["level"]}')
  for lang in ['ru','en']:
   c=s['copy'][lang];print(lang.upper(),c['title']);print(html.unescape(re.sub('<[^>]+>','',c['body'].replace('</p>','\n\n'))).strip())

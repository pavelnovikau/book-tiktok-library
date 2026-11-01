import sys,json,re,html
from pathlib import Path
p=Path(__file__).resolve().parent.parent
d=json.loads((p/'story-data.json').read_text())
level,start,end=map(int,sys.argv[1:4]);route=[s for s in d['screens'] if s.get('level',1)<=level]
for n in range(start-1,min(end,len(route))):
 s=route[n];print(f"\n{n+1}/{len(route)} {s['id']} L{s.get('level',1)}")
 for lang in ['ru','en']:
  c=s['copy'][lang];print(lang.upper()+': '+c.get('title',''))
  if c.get('subtitle'):print(c['subtitle'])
  print(html.unescape(re.sub('<[^>]+>',' ',c.get('body','').replace('</p>','</p>\n'))))

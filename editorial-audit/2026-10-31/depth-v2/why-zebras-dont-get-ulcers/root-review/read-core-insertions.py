from pathlib import Path
import json,re,html,sys

H=Path(__file__).resolve().parent.parent
d=json.loads((H/'story-data.json').read_text());route=[s for s in d['screens'] if s['level']<=2]
insertions=[(i,s) for i,s in enumerate(route) if s['level']==2]
plain=lambda s:html.unescape(re.sub('<[^>]+>',' ',s)).strip()
def sentences(s):
 return [x.strip() for x in re.split(r'(?<=[.!?])\s+',re.sub(r'\s+',' ',plain(s))) if x.strip()]
start,end=int(sys.argv[1]),int(sys.argv[2])
for j,(i,s) in enumerate(insertions,start=1):
 if not start<=j<=end:continue
 print(f'\nCORE INSERTION {j}/{len(insertions)}: {s["id"]}, route position {i+1}/{len(route)}')
 for l in ['ru','en']:
  prev,nxt=route[i-1],route[i+1]
  print(l.upper(),'PREVIOUS',prev['id'],prev['copy'][l]['title'],sentences(prev['copy'][l]['body'])[-1])
  print(l.upper(),'FULL',s['copy'][l]['title'],plain(s['copy'][l]['body']))
  print(l.upper(),'NEXT',nxt['id'],nxt['copy'][l]['title'],sentences(nxt['copy'][l]['body'])[0])

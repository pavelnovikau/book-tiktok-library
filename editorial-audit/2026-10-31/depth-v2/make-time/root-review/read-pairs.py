from pathlib import Path
import html,json,re,sys
H=Path(__file__).resolve().parent.parent
d=json.loads((H/'story-data.json').read_text())
mode=sys.argv[1];a=int(sys.argv[2]);b=int(sys.argv[3]);level={'essential':1,'core':2,'deep':3,'core-additions':2}[mode]
all_screens=[s for s in d['screens'] if s['level']<=level]
screens=[s for s in all_screens if s['level']==2] if mode=='core-additions' else all_screens
assert 1<=a<=b<=len(screens)
plain=lambda t:html.unescape(re.sub('<[^>]+>','',t.replace('</p>','\n\n'))).strip()
for n,s in enumerate(screens[a-1:b],a):
 print(f'\nPAIR {n}/{len(screens)} {s["id"]} LEVEL {s["level"]}')
 for lang in ['ru','en']:
  c=s['copy'][lang]
  print(lang.upper(),c.get('section',''),c['title'],c.get('subtitle',''))
  if mode=='core-additions':
   ix=next(i for i,x in enumerate(all_screens) if x['id']==s['id'])
   prev=plain(all_screens[ix-1]['copy'][lang].get('body','')) if ix else ''
   nxt=plain(all_screens[ix+1]['copy'][lang].get('body','')) if ix+1<len(all_screens) else ''
   print('PREVIOUS LAST SENTENCE:',re.split(r'(?<=[.!?])\s+',prev)[-1])
  print(plain(c.get('body','')))
  if mode=='core-additions':print('NEXT FIRST SENTENCE:',re.split(r'(?<=[.!?])\s+',nxt)[0])


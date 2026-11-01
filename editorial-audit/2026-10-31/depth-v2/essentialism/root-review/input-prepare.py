from pathlib import Path
import re,json,html,hashlib
B=Path(__file__).resolve().parent
# Ordered after the continuous RU then EN drafts. Levels select existing prose;
# no content is generated to fill a preselected screen count.
rows=[
('promise',1,'1','gl1:5-22'),('success',2,'1','gl1:16-18,68-88'),('hospital',2,'1','gl1:57-64,90-90,145-145'),('cycle',1,'1','gl1:91-124'),
('choice',2,'2','gl2:6-18'),('helplessness',3,'2','gl2:20-32'),('returns',2,'3','gl3:8-16;gl3-3:5-6'),('restaurant',3,'3','gl3:14-15;gl3-3:2-6'),
('strategy',2,'4','gl4:6-15,26-26'),('values',1,'4','gl4:17-24,38-39'),('space',2,'5','gl5:6-20,28-35'),('reading',3,'5','gl5:37-40'),
('meaning',2,'6','gl6:6-12,17-24,33-40'),('fieldwork',2,'6','gl6:42-47'),('play',2,'7','gl7:11-11,21-33'),('asset',2,'8','gl8:5-22,50-52'),('rest',3,'8','gl8:37-49'),
('selection',1,'9','gl9:6-14,42-42'),('duarte',2,'9','gl9:38-41'),('evidence',3,'9','gl9:25-34,44-46'),
('intent',2,'10','gl10:19-45,49-52'),('unfinished',2,'10','gl10:46-48,53-54'),('refusal',1,'11','gl11:10-12,18-24,32-45'),('covey',2,'11','gl11:13-17,22-22'),('manager',2,'11','gl11:46-59'),
('sunk-costs',1,'12','gl12:6-19,29-33,47-47,53-53'),('ownership',3,'12','gl12:21-27,36-38'),('zero-base',2,'12','gl12:39-47,53-53'),('reverse-pilot',2,'12','gl12:48-53'),
('editing',2,'13','gl13:6-14,21-38'),('boundaries',1,'14','gl14:6-23'),('responsibility',2,'14','gl14:24-43'),('buffer',2,'15','gl15:8-22'),('planning',2,'15','gl15:27-28,33-48'),
('herbie',2,'16','gl16:6-15'),('constraint',2,'16','gl16:26-35'),('progress',1,'17','gl17:21-24,31-44'),('tickets',3,'17','gl17:6-10,19-20'),('tokens',3,'17','gl17:29-31'),
('routine',1,'18','gl18:6-29'),('cue',2,'18','gl18:30-43'),('presence',1,'19','gl19:6-23,30-33'),('attention',2,'19','gl19:24-26,35-45'),
('identity',2,'20','gl20:6-46,48-54'),('team',2,'appendix','pril:5-17,42-56'),('roles',2,'appendix','pril:42-55'),('final',1,'20','gl20:55-61')]
# Essential is an entry route through the actual argument. Core restores cases
# and further procedures; Deep adds all remaining authored text. All are nested.
essential={1:[1,2,3],4:[1,2,3],5:[3],7:[2,3],10:[1,2,3],11:[1],16:[3],18:[1,2,3],21:[1,2],23:[1,2,3],25:[1],26:[1,2,3],28:[2],31:[1,2,3],33:[1,2],36:[1,2],37:[1,2,3],40:[1,2,3],42:[1,2,3],44:[1,2],45:[2,3],47:[1,2]}
# Keep essential theory coherent when its illustrative earlier paragraphs are absent.

def parse(lang):
 text=(B/f'draft-{lang}.md').read_text();out=[]
 for chunk in re.split(r'\n## ',text)[1:]:
  title,body=chunk.split('\n\n',1);out.append({'title':re.sub(r'^\d+\. ','',title),'paragraphs':[p.strip() for p in body.strip().split('\n\n')]})
 return out
ru,en=parse('ru'),parse('en');assert len(ru)==len(en)==len(rows)
unit_map=[];screens=[]
sections={'ru':lambda ch:'Приложение' if ch=='appendix' else 'Глава '+ch,'en':lambda ch:'Appendix' if ch=='appendix' else 'Chapter '+ch}
for n,((uid,base,ch,loc),r,e) in enumerate(zip(rows,ru,en),1):
 assert len(r['paragraphs'])==len(e['paragraphs'])
 refs=[]
 for f in loc.split(';'):
  file,ranges=f.split(':')
  for a in ranges.split(','):
   start,end=map(int,a.split('-'));refs.append({'file':f'OEBPS/Text/{file}.xhtml','start':start,'end':end})
 unit={'unit':n,'id':uid,'chapter':ch,'title':{'ru':r['title'],'en':e['title']},'primaryRanges':refs,'screens':[]}
 for pi,(rp,ep) in enumerate(zip(r['paragraphs'],e['paragraphs']),1):
  if uid=='final' and pi==2:continue
  if uid=='final':rp='\n\n'.join(r['paragraphs']);ep='\n\n'.join(e['paragraphs'])
  level=1 if pi in essential.get(n,[]) else (2 if n==40 and pi==4 else base)
  sid=uid if pi==1 else f'{uid}-{pi}'
  copy={}
  for lang,p,title in [('ru',rp,r['title']),('en',ep,e['title'])]:
   copy[lang]={'section':sections[lang](ch),'title':title if pi==1 or uid=='final' else title+f' · {pi}','body':''.join('<p>'+html.escape(x,quote=False)+'</p>' for x in p.split('\n\n'))}
  screen={'id':sid,'level':level,'claimType':'book','sources':[1],'unit':n,'sourceLocators':refs,'copy':copy}
  if uid=='final':screen['final']=True
  screens.append(screen);unit['screens'].append({'id':sid,'level':level,'draftParagraphs':[pi] if uid!='final' else [1,2]})
 unit_map.append(unit)
cover={'id':'cover','level':1,'type':'cover','sources':[1],'copy':{'ru':{'section':'Грег МакКеон','title':'Эссенциализм','subtitle':'Меньше, но лучше','body':''},'en':{'section':'Greg McKeown','title':'Essentialism','subtitle':'Less, but better','body':''}}}
screens.insert(0,cover)
counts={m:sum(s['level']<=l for s in screens) for m,l in [('essential',1),('core',2),('deep',3)]}
method={
'ru':'Оригинальное сокращённое изложение книги 2014 года по предоставленной русской редакции МИФ 2015, перевод И. Айзятуловой, ISBN 9785000573471. Непрерывно прочитаны все 20 глав, четыре вступления к частям и приложение: 47 209 извлечённых слов в 29 файлах, с информацией об издании. Примечания и прочие завершающие материалы не прочитаны непрерывно. Доступна текстовая экстракция, а не изображения и геометрия схем. Истории, исторические разборы и исследования передают аргумент автора; их исходные данные независимо не перепроверялись. Эпизод с Херби — из романа, финальная история — притча. Английский текст — собственный перевод этого изложения, без сверки с официальным английским изданием. Юбилейные дополнения исключены. Точные ссылки на главы, файлы и абзацы доступны ниже; номера абзацев относятся к экстракции, не к печатным страницам. Отбор сокращает случаи и подробности; полный перечень сохранённого и опущенного — в сопровождающей карте.',
'en':'An original condensed exposition of the 2014 book using the supplied Russian MIF 2015 edition, translated by I. Aizyatulova, ISBN 9785000573471. All 20 chapters, four part openings and the appendix were read continuously: 47,209 extracted words in 29 files, including edition information. Notes and other endmatter were not read continuously. The source is a text extraction, without images or diagram geometry. Anecdotes, historical discussions and research present the author\'s argument; their underlying records were not independently reinvestigated. Herbie belongs to a novel; the closing story is a parable. English is an original translation of this exposition, without collation against the official English edition. Anniversary additions are excluded. Exact chapter/file/paragraph references are available below; paragraph numbers belong to the extraction, not printed pages. Selection reduces cases and detail; the accompanying map records retention and omissions.'}
data={'schemaVersion':2,'slug':'essentialism','title':{'ru':'Эссенциализм','en':'Essentialism'},'description':{'ru':'Связное изложение философии вклада, выбора и исполнения Грега МакКеона.','en':'A connected exposition of Greg McKeown\'s philosophy of contribution, choice and execution.'},'defaultLanguage':'ru','defaultTheme':'dark','defaultMode':'essential','contentMode':'explanatory','targetModes':counts,'methodNote':method,'sources':[{'id':1,'title':'Greg McKeown — Essentialism / Эссенциализм · МИФ 2015','url':'https://www.mann-ivanov-ferber.ru/catalog/product/hozyain_svoej_zhizni/','role':'book','note':{'ru':'Источник — предоставленная полная русская редакция; ссылка издателя только библиографическая, не утверждение о чтении сайта. Оригинал 2014; перевод И. Айзятуловой, ISBN 9785000573471.','en':'The source is the supplied complete Russian edition. This publisher link is bibliographic only, not a claim that its webpage was read. Original 2014; Russian translation by I. Aizyatulova, ISBN 9785000573471.'}}],'media':{},'screens':screens,'unitMap':unit_map,'coverageNotes':json.loads((B/'coverage-notes.json').read_text()),'editorialStatus':{'status':'ready-for-root-personal-check','rootPersonalAcceptance':False,'publicationAllowed':False}}
# Match maintained builder word semantics; localize Russian minute forms.
data['modes']={}
for mode,level in [('essential',1),('core',2),('deep',3)]:
 times={}
 for lang,rate in [('ru',180),('en',220)]:
  words=0
  for screen in screens:
   if screen['level']>level:continue
   c=screen['copy'][lang]
   plain=html.unescape(re.sub(r'<[^>]+>',' ',c['title']+' '+c.get('subtitle','')+' '+c['body']))
   words+=len(re.findall(r"[^\W_][\w'’\-–—]*",plain))
  import math
  minutes=max(1,math.ceil(words/rate))
  form='минут' if minutes%100 in range(11,15) else 'минута' if minutes%10==1 else 'минуты' if minutes%10 in [2,3,4] else 'минут'
  times[lang]=f'{minutes} {form}' if lang=='ru' else f'{minutes} min'
 data['modes'][mode]={'minutes':times}
(B/'story-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');(B/'coverage-map.json').write_text(json.dumps(unit_map,ensure_ascii=False,indent=2)+'\n')
# Routes remain direct selections of the connected original drafts.
for mode,level in [('essential',1),('core',2),('deep',3)]:
 for lang in ['ru','en']:
  out=['# '+data['title'][lang]+' — '+mode,'']
  for s in screens[1:]:
   if s['level']<=level:
    out.extend(['## '+s['id']+' — '+s['copy'][lang]['title'],'',html.unescape(re.sub('</p><p>','\n\n',s['copy'][lang]['body'])[3:-4]),''])
  (B/f'{mode}.{lang}.md').write_text('\n'.join(out))
print(json.dumps({'counts':counts,'units':len(unit_map),'paragraphPairs':sum(len(x['paragraphs']) for x in ru)},ensure_ascii=False))

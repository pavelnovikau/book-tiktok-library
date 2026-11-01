from pathlib import Path
import re,json,html,hashlib,math
here=Path(__file__).parent
# Connected drafts precede screen authoring. No story body is generated here.
p=here/'draft-ru.md';s=p.read_text().replace('На другой день после похорон к трактиру','На другой день после похорон отца к трактиру').replace('требование явиться к десяти','указание срока — до десяти');p.write_text(s)
p=here/'draft-en.md';s=p.read_text().replace('The day after the funeral, a blind man','The day after Father\'s funeral, a blind man');p.write_text(s)
def parse(lang):
 a=re.split(r'^## (.+)$',(here/f'draft-{lang}.md').read_text(),flags=re.M)
 return [(a[i].split(' · ')[0],[x.strip() for x in a[i+1].strip().split('\n\n') if x.strip()]) for i in range(1,len(a),2)]
drafts={l:parse(l) for l in ['ru','en']}; assert [len(x[1]) for x in drafts['ru']]==[len(x[1]) for x in drafts['en']]
meta='''inn-arrival|Постоялец|The lodger
inn-evening|Вечер в трактире|An evening at the inn
winter-visitor|Зимний гость|A winter visitor
upstairs|Наверху|Upstairs
rum-request|У постели|At the bedside
blind-visitor|Рука незнакомца|The stranger's hand
hamlet|В соседней деревне|In the hamlet
chest|Над сундуком|Over the chest
road|На дороге|On the road
revenue|После погони|After the pursuit
library|В библиотеке|In the library
expedition|Новые планы|New plans
letter|Письмо из Бристоля|A letter from Bristol
farewell|Перед отъездом|Before leaving
spyglass|В «Подзорной трубе»|At the Spy-glass
quays|По набережной|Along the quays
captain|Разговор в каюте|A cabin conversation
berths|Перед выходом|Before departure
departure|Начало перехода|The passage begins
galley|Камбуз и бочка|Galley and barrel
dick|Разговор за стенкой|Voices on the other side
apple|Не двигаться|Keep still
chart-copy|При лунном свете|In the moonlight
council|За закрытой дверью|Behind a closed door
anchorage|У острова|Off the island
boats|К берегу|Towards shore
marsh|Голоса у топи|Voices by the marsh
tom|Среди деревьев|Amongst the trees
islander|Кто-то впереди|Someone ahead
ben-account|История Бена|Ben's account
white-rock|Звук пушки|A cannon sounds
spring|Доктор: разведка|The doctor: reconnaissance
cargo|Доктор: припасы|The doctor: supplies
gray|Доктор: перед отходом|The doctor: before leaving
current|Доктор: течение|The doctor: the current
last-trip|Доктор: к суше|The doctor: towards land
redruth|Доктор: у частокола|The doctor: by the stockade
flag|Доктор: под флагом|The doctor: beneath the flag
jim-return|Джим: снова со своими|Jim: amongst friends again
sand|Песок и дым|Sand and smoke
morning|Следующее утро|The next morning
truce|Белый флаг|A white flag
terms|У порога|At the threshold
posts|Ожидание|Waiting
attack|У стен дома|Beside the house
casualties|После боя|After the fight
noon|Полуденная жара|Noonday heat
leaving|Снова за оградой|Beyond the fence again
coracle|У белой скалы|At the white rock
cable|Канат|The cable
window|Кормовое окно|The stern window
ebb|Отлив|The ebb
cliffs|Берег утром|The coast in the morning
paddling|Между волнами|Between the waves
bowsprit|Под носом шхуны|Beneath the bow
deck|На палубе|On deck
water|Вода и еда|Water and food
bargain|Вдоль берега|Along the coast
dirK|Просьба Хендса|Hands's request
wine|Бутылка вина|A bottle of wine
inlet|Вход в бухту|Entering the inlet
rigging|Над водой|Above the water
shoulder|На мачте|On the mast
sails|К вечеру|Towards evening
homeward|Дорога к дому|The way to the house
torch|При свете факела|By torchlight
confession|Ответ Джима|Jim's answer
council-outside|Совет снаружи|A council outside
question|Вдвоём|Alone together
spot|Книга и нож|Book and knife
charges|Перед командой|Before the crew
night|Ночью в срубе|Night in the house
patients|Утренний визит|The morning visit
fence|По песку к ограде|Across the sand to the fence
parole|По разные стороны|On opposite sides
warning|Перед поисками|Before the search
breakfast|Завтрак|Breakfast
rope|На верёвке|On a rope
pointer|Под сосной|Beneath a pine
plateau|На плато|On the plateau
echo|Эхо|The echo
tall-tree|Высокое дерево|The tall tree
pit|На краю ямы|At the pit's edge
shots|Из кустов|From the bushes
ben-work|Рассказ по дороге|The story on the way
sea-road|Морской путь|The sea route
cave|В пещере|In the cave
coins|Работа с утра|Work from morning
voices|Голоса внизу|Voices below
point|У песчаного мыса|Off the sandy point
port|Огни порта|Harbour lights
bristol|Снова Бристоль|Bristol again
surf|Последние строки|The last lines'''.splitlines()
assert len(meta)==93,len(meta)
essential={1,3,4,6,7,8,9,10,11,12,15,16,20,21,22,23,26,29,31,39,41,42,43,45,46}
chapters=json.loads((here/'chapter-map.json').read_text())['chapters']
screens=[{'id':'cover','level':1,'type':'cover','sources':[],'copy':{
'ru':{'section':'Начало','title':'Остров сокровищ','subtitle':'Роберт Льюис Стивенсон · Сокращённый рассказ','body':'<p>В приморский трактир приходит незнакомец с сундуком. Джим Хокинс ещё не знает, кто его преследует и куда приведут спрятанные бумаги.</p><p>«Главное» и «Суть книги» — незавершённое начало до боя за частокол включительно. Дальнейшая история и развязка открываются в «Глубоко» после предупреждения.</p>'},
'en':{'section':'Start','title':'Treasure Island','subtitle':'Robert Louis Stevenson · A condensed retelling','body':'<p>A stranger brings a chest to a coastal inn. Jim Hawkins does not yet know who is pursuing him or where the hidden papers will lead.</p><p>Essential and Core are unresolved openings through the stockade battle. The continuation and ending open in Deep after a warning.</p>'}}}]
scene=[];number=0
for ci,(chapter,paras) in enumerate(drafts['ru']):
 for pi,ru in enumerate(paras):
  number+=1;ident,titleRu,titleEn=meta[number-1].split('|');ident=ident.lower()
  if number==47:
   screens.append({'id':'deep-warning','level':3,'claimType':'book','sources':[1],'copy':{
    'ru':{'section':'Продолжение','title':'Дальше — полная история','body':'<p>Дальше раскрываются морская вылазка Джима, поиски сокровищ, исход мятежа и последняя сцена. «Главное» и «Суть книги» заканчиваются раньше и оставляют развязку неизвестной.</p>'},
    'en':{'section':'Continuation','title':'Ahead: the complete story','body':'<p>The continuation reveals Jim’s sea excursion, the treasure hunt, the mutiny’s outcome, and the last scene. Essential and Core stop earlier, leaving the ending unrevealed.</p>'}}})
  level=1 if number in essential else 2 if ci<21 else 3
  ch=chapters[ci];ev=f"PG120 · {chapter} · L{ch['sourceLines'][0]}–{ch['sourceLines'][1]}"
  screen={'id':ident,'level':level,'claimType':'book','sources':[1],'evidenceLocator':ev,'copy':{}}
  for lang,title in [('ru',titleRu),('en',titleEn)]:
   body=drafts[lang][ci][1][pi]
   screen['copy'][lang]={'section':('Рассказ доктора Ливси' if lang=='ru' else "Dr Livesey's account") if 16<=ci+1<=18 else ('Рассказ Джима Хокинса' if lang=='ru' else "Jim Hawkins's account"),'title':title,'body':'<p>'+html.escape(body,quote=False)+'</p>'}
  screens.append(screen);scene.append({'id':ident,'order':number,'level':level,'chapter':chapter,'draftParagraph':pi+1,'sourceLines':ch['sourceLines'],'focalizer':ch['focalizer'],'title':{'ru':titleRu,'en':titleEn}})
screens.append({'id':'final','level':1,'final':True,'claimType':'book','sources':[1],'copy':{
'ru':{'section':'Чтение','title':'У края карты','body':'<p>Выбранная глубина закончилась. «Главное» и «Суть книги» оставляют поиски незавершёнными. «Глубоко» содержит всю сохранённую сюжетную дугу с развязкой.</p><p>Роман и карта сцен доступны через «Источники».</p>'},
'en':{'section':'Reading','title':'At the edge of the map','body':'<p>This reading depth has ended. Essential and Core leave the search unresolved. Deep contains the full retained story arc and ending.</p><p>The novel and scene map are available through Sources.</p>'}}})
counts={mode:sum(s['level']<=level for s in screens) for mode,level in [('essential',1),('core',2),('deep',3)]}
data={'schemaVersion':2,'slug':'treasure-island','author':{'ru':'Роберт Льюис Стивенсон','en':'Robert Louis Stevenson'},'title':{'ru':'Остров сокровищ','en':'Treasure Island'},'description':{'ru':'Джим Хокинс, карта Флинта и плавание «Испаньолы». Сокращённый рассказ по роману Стивенсона.','en':'Jim Hawkins, Flint’s map, and the voyage of the Hispaniola. A condensed retelling of Stevenson’s novel.'},'defaultLanguage':'ru','defaultTheme':'dark','defaultMode':'essential','contentMode':'narrative','spoilerPolicy':'full-plot-in-deep','targetModes':counts,'methodNote':{'ru':'Связный пересказ своими словами по всему английскому роману, главы I–XXXIV. Сначала написаны русская и соответствующая английская версии, затем выделены сцены. Обе — новое сокращение, не опубликованные переводы. «Главное» и «Суть книги» останавливаются после боя за частокол без исхода поисков; продолжение с развязкой — в «Глубоко». Полный внешний текст раскрывает сюжет.','en':'An original connected retelling based on the whole English novel, chapters I–XXXIV. Russian prose and its corresponding English version were written before scene segmentation. Both are new condensations, not published translations. Essential and Core stop after the stockade battle without resolving the search; Deep continues through the ending. The complete external text reveals the plot.'},'sources':[{'id':1,'title':'Robert Louis Stevenson — Treasure Island · Project Gutenberg #120','url':'https://www.gutenberg.org/files/120/120-h/120-h.htm','role':'book','note':{'ru':'Полный английский электронный текст прочитан последовательно, включая последнюю главу. Источник событий и порядка раскрытия. Номера L в карте относятся к строкам использованного текстового файла, не к страницам печатного издания. Внешняя ссылка открывает весь роман.','en':'The complete English electronic text was read continuously, including the last chapter. It supplies events and disclosure order. L numbers in the map refer to lines of the text witness used, not printed pages. The external link opens the whole novel.'}}],'media':{},'screens':screens}
(here/'story-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(here/'scene-map.json').write_text(json.dumps({'containsFullPlotSpoilers':True,'chapters':chapters,'scenes':scene,'routes':{mode:[s['id'] for s in screens if s['level']<=level] for mode,level in [('essential',1),('core',2),('deep',3)]}},ensure_ascii=False,indent=2)+'\n')
lines=['# Treasure Island — chapter and scene coverage','', 'Working editorial map: full plot spoilers. This complete file is for root review; reader Sources shows only the selected depth.','', 'All 34 narrative chapters were read in order from the supplied English PG120 witness. L numbers are actual file lines, not print pages. Logical XVII has a mistaken XXVII heading in that witness; title and order identify it unambiguously.','', 'The two connected drafts were completed before segmentation. Each narrative screen is exactly one pre-existing paragraph, in the same order and language pairing. Short routes are deliberately unresolved openings through XXI; Deep continues XXII–XXXIV.','']
for c in chapters:
 lines += [f"## {c['chapter']} · L{c['sourceLines'][0]}–{c['sourceLines'][1]}",f"Narrator: {c['focalizer']}. Retained: {c['retained']}.",f"Compression: {c['compressedOrOmitted']}.", '']
 for row in scene:
  if row['chapter']==c['chapter']:lines.append(f"- `{row['id']}` · paragraph {row['draftParagraph']} · level {row['level']} · {row['title']['ru']} / {row['title']['en']}")
 lines.append('')
lines += ['## Routes','',f"Derived counts including framing: {counts}.",'', 'Essential omits most preparations, detailed stockade evacuation, Tom’s murder and Hands’s introduction, but keeps the chest pursuit, map, misleading Silver encounter, barrel discovery, shore departure, Ben, reunion, negotiations and battle. No later ship/hunt/return outcome appears.','', 'Core retains every draft paragraph through XXI, including Livesey’s separate account; it stops at the same unresolved point with fuller relationships and material action. Deep adds the continuous remaining arc.','', 'The body does not treat Silver’s tales or the doctor’s historical medical beliefs as independently validated science. Allardyce is a guess, Jim’s larger captive claim is a boast, and Silver’s future remains unknown. Both prior Ben findings remain closed in the new telling.']
(here/'chapter-scene-map.md').write_text('\n'.join(lines)+'\n')
# Human route copies: body only with neutral screen titles, explicitly out of product.
for mode,level in [('essential',1),('core',2),('deep',3)]:
 for lang in ['ru','en']:
  body=[]
  for s in screens:
   if s['level']<=level:body.append('## '+s['id']+' · '+s['copy'][lang]['title']+'\n\n'+html.unescape(re.sub('<[^>]+>','\n',s['copy'][lang]['body'])).strip())
  dest=here/'routes';dest.mkdir(exist_ok=True);(dest/f'{mode}-{lang}.md').write_text('\n\n'.join(body)+'\n')
print(json.dumps({'counts':counts,'narrativeParagraphs':number},ensure_ascii=False))

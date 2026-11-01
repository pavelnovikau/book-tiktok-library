from pathlib import Path
import re,json,html
HERE=Path(__file__).parent
# Written after both complete connected drafts. A paragraph is one complete narrative beat.
raw='''shark|Акула за кормой|The shark astern|1.1
bottle|Стекло на столе|Glass on the table|1.1
fragments|Одна широта|One latitude|1.2
children|Увидеть почерк|To see his handwriting|1.3
mary|Сестра и брат|Sister and brother|1.4
helena|Предложение Элен|Helena's proposal|1.4
departure|Молитва перед отплытием|A prayer before sailing|1.5
stranger|Падение подзорной трубы|The collapsing telescope|1.6
cabin-six|Пассажир шестой каюты|The passenger in cabin six|1.6
wrong-ship|Не «Скотия»|Not Scotia|1.7
staying|Высадка откладывается|Landing postponed|1.8
straits|Южный Крест|The Southern Cross|1.9
chile|Берег без следов|A shore without a trace|1.10
parting|Семеро на суше|Seven ashore|1.10
mules|В кресле по Чили|Through Chile in an armchair|1.11
pass|Стена в проходе|A wall across the pass|1.12
snow|Хижина среди снегов|A hut in the snow|1.12
supper|Неудачный ужин|An unsuccessful supper|1.13
quake|Склон приходит в движение|The slope moves|1.13
missing|Одного не хватает|One is missing|1.14
condor|Точка в небе|A speck in the sky|1.14
shot|Выстрел из долины|A shot from the valley|1.14
lusiads|Книга Камоэнса|The book by Camoens|1.15
thaouka|Конь на свист|A horse at a whistle|1.15,1.16
sand-map|Карта на песке|A map in the sand|1.16
salinas|Высохшее озеро|The dry lake|1.17
scouts|Голос из памяти|A remembered voice|1.18
river|Вода найдена|Water found|1.18
wolves|Глаза в темноте|Eyes in the darkness|1.19
fire|Последняя сухая трава|The last dry grass|1.19
decoy|Прыжок через огонь|A leap through fire|1.19
morning|Навстречу выстрелам|Toward the signal shots|1.19,1.20
fort|Разговорчивый комендант|The talkative commander|1.20,1.21
guinnard|Чужая история|Another man's story|1.21
horns|Рога над грязью|Horns above the mud|1.22
flood|Дерево впереди|A tree ahead|1.22
ombu|Кухня среди ветвей|A kitchen in the branches|1.23
idea|Название с вершины|A name from the treetop|1.23,1.24
australia|Новое чтение|A new reading|1.24
lightning|Огонь над водой|Fire above water|1.25
drifting|Плывущее омбу|The drifting ombu|1.25,1.26
atlantic|Огни у берега|Lights offshore|1.26
farewell|Талькав остаётся|Thalcave stays|1.26
reunion|Место за настоящим столом|A place at a real table|2.1
parallel|Все земли параллели|Every land on the parallel|2.1
islands|Каюта для отца|A cabin for her father|2.2,2.3
wager|Ружьё против трубы|Rifle against telescope|2.4
engine|Винт остановился|The propeller stops|2.5
bar|За полосой бурунов|Beyond the breakers|2.5
farm|Мельница вдали|A distant windmill|2.6
worker|Голос с конца стола|A voice at the table's end|2.6,2.7
papers|Подпись капитана|The captain's signature|2.7
crossing|Другой путь к берегу|Another way to the coast|2.7,2.8
wagon|Комната на колёсах|A room on wheels|2.8
apsley|Ужин в Эпсли|Supper at Apsley|2.9
herd|Пыль над стадом|Dust above the herd|2.10
shoe|Трилистник на подкове|A trefoil horseshoe|2.10,2.11
railway|Разводной мост|The swing bridge|2.11
toline|Мальчик с биркой|The boy with a label|2.12
examination|Где живёт лорд Наполеон|Where Lord Napoleon lives|2.12
compendium|Подаренная география|The gift of a geography|2.12
seymour|Газета в Сеймуре|The newspaper at Seymour|2.13
mozart|Моцарт среди деревьев|Mozart among the trees|2.13,2.14
hunt|Обещание Манглса|Mangles's promise|2.14
alps|Дорога через град|The road through hail|2.15
snowy|Колёса уходят в землю|The wheels sink|2.15
camp|Ночь у Сноуи|Night beside the Snowy|2.15
trackers|Свет между стволами|Light between the trunks|2.15,2.17
name|Как пишется имя|How the name is spelled|2.16
betrayal|Выстрел в лагере|A shot in camp|2.17
writing|Строка под диктовку|A dictated line|2.17
mulrady|Человек на мокрой земле|A man on wet ground|2.18
bridge|Сгоревший переход|The burned crossing|2.18
raft|Один берег позади|One bank behind them|2.19
telegram|Телеграмма в Идене|A telegram at Eden|2.19
macquarie|Плата за проезд|The price of passage|3.1
halley|Чужая палуба|Another deck|3.1,3.2,3.3
charts|Без карты|Without a chart|3.2,3.3,3.4
wreck|Риф в темноте|A reef in the dark|3.4
abandoned|Лодка исчезла|The boat is gone|3.4,3.5
landing|Долгие мили до суши|The long miles ashore|3.6
cave|Дождь у пещеры|Rain at the cave|3.7
waipa|Туман у слияния рек|Fog at the rivers' junction|3.8,3.9
canoe|Вверх по Вайкато|Up the Waikato|3.9
pah|Дом за оградой|The house within the fence|3.10
kara-tete|Рука на плече Элен|A hand on Helena's shoulder|3.10
sentence|Приговор на рассвете|Sentence at sunrise|3.11
digging|Шорох под стеной|Scraping beneath the wall|3.12
hand|Маленькая рука|A small hand|3.12
rope|Трое рывков верёвки|Three pulls on the rope|3.12
sanctuary|Завтрак в гробнице|Breakfast in the tomb|3.13
siege|Горячая земля|The hot ground|3.13
volcano|Камень сдвинулся|The stone moves|3.14
ridge|Без выстрелов|Without a shot|3.14
kauris|Высокие своды леса|High forest arches|3.15
lottin|Пирога на песке|A canoe on the sand|3.15
yacht|Знакомый силуэт|A familiar silhouette|3.15
order|Подлинник приказа|The original order|3.16
prisoner|Запертая каюта|The locked cabin|3.16
silence|Отказ отвечать|The refusal to answer|3.17
bargain|Два разговора Элен|Helena's two interviews|3.17,3.18
confession|До последнего плавания|Before the final voyage|3.18
third-reading|Третья догадка|The third conjecture|3.18
lights|Огонь на острове|Fire on the island|3.19
voice|Зов над волнами|A cry across the waves|3.19
flag|Трое на берегу|Three on the beach|3.19
father|Представить друзей|Introducing his friends|3.20
survivors|Дом из корабельных досок|A house of ship's planks|3.20
swimmer|Ночной пловец|The night swimmer|3.20
tabor|Второе имя острова|The island's second name|3.20
ayrton-island|Человек на скале|The man on the rock|3.20
home|Собор Святого Мунго|St Mungo's Cathedral|3.21
arabella|Секрет под одеждой|The secret under his clothes|3.21'''
rows=[s.split('|') for s in raw.splitlines()]; assert len(rows)==113
chapter_ranges=json.loads((HERE/'witness-chapter-ranges.json').read_text())
by_code={};counts={}
for c in chapter_ranges:
 part=c['part'];counts[part]=counts.get(part,0)+1;by_code[f"{part}.{counts[part]}"]=c

def parse(lang):
 groups=re.split(r'(?m)^## ',(HERE/f'draft-{lang}.md').read_text())[1:];paras=[]
 for group in groups:
  head,*ps=group.split('\n\n')
  for p in ps:
   if p.strip():paras.append((head.strip(),p.strip()))
 return paras
ru,en=parse('ru'),parse('en');assert len(ru)==len(en)==113
L=lambda a,b:{'ru':a,'en':b}
copy=lambda section,title,body:{'section':section,'title':title,'body':body}
cover={'id':'cover','level':1,'type':'cover','sources':[],'copy':{
 'ru':{**copy('Жюль Верн','Дети капитана Гранта','<p>Бутылка из моря приводит двоих детей и их новых друзей на другую сторону света.</p><p class="muted">«Главное» и «Суть книги» — незавершённые начала поисков. Полное приключение и развязка — в «Глубоко» после согласия.</p>'),'subtitle':'Приключенческий роман · Связный пересказ','visualAlt':'Типографская обложка приключенческого романа'},
 'en':{**copy('Jules Verne','The Children of Captain Grant','<p>A bottle from the sea takes two children and their new friends to the other side of the world.</p><p class="muted">Essential and Core are unfinished openings of the search. The complete adventure and resolution are in Deep after consent.</p>'),'subtitle':'An adventure novel · A connected retelling','visualAlt':'A typographic cover for an adventure novel'}}}
warning={'id':'deep-warning','level':3,'claimType':'synthesis','sources':[],'copy':{
 'ru':copy('Дальше — полная история','Предупреждение о развязке','<p>Далее раскрываются поздние события, скрытые причины происходящего и судьбы героев. Вы продолжаете полный маршрут «Глубоко» со спойлерами.</p>'),
 'en':copy('The complete story continues','An ending warning','<p>The following scenes reveal later events, hidden causes and the characters’ outcomes. You are continuing the full Deep route with spoilers.</p>')}}
final={'id':'final','level':1,'final':True,'claimType':'synthesis','sources':[],'copy':{
 'ru':copy('Остановка','Выбранный маршрут прочитан','<p>«Главное» заканчивается после встречи с Талькавом, «Суть книги» — у застрявшего фургона перед продолжением. Это части приключения, а не полная история. «Глубоко» доводит рассказ до авторского завершения.</p>'),
 'en':copy('A stopping point','Your chosen route is complete','<p>Essential ends after meeting Thalcave; Core ends beside the stranded wagon before the continuation. These are portions of the adventure. Deep carries the story through its actual conclusion.</p>')}}
screens=[cover];scene_map=[]
for i,(id,rt,et,codes) in enumerate(rows,1):
 cs=[by_code[c] for c in codes.split(',')];start=min(c['startLine'] for c in cs);end=max(c['endLine'] for c in cs)
 loc='Horne '+', '.join(codes.split(','))+f'; witness L{start}–{end}'
 s={'id':id,'level':1 if i<=24 else 2 if i<=67 else 3,'claimType':'book','sources':[1],'evidenceLocator':loc,'draftParagraph':i,'copy':{'ru':copy(ru[i-1][0],rt,'<p>'+html.escape(ru[i-1][1],quote=False)+'</p>'),'en':copy(en[i-1][0],et,'<p>'+html.escape(en[i-1][1],quote=False)+'</p>')}}
 if i==3:s['sources'].append(2)
 if i==98:s['sources'].append(3)
 if i==110:s['sources'].append(4)
 if i in (112,113):s['sources'].append(5)
 if i==68:screens.append(warning)
 screens.append(s);scene_map.append({'paragraph':i,'id':id,'level':s['level'],'title':L(rt,et),'chapters':codes.split(','),'startLine':start,'endLine':end})
screens.append(final)
urls=['https://www.gutenberg.org/cache/epub/2083/pg2083-images.html','https://fr.wikisource.org/wiki/Les_Enfants_du_capitaine_Grant/Partie_1/Chapitre_II','https://fr.wikisource.org/wiki/Les_Enfants_du_capitaine_Grant/Partie_3/Chapitre_XVII','https://fr.wikisource.org/wiki/Les_Enfants_du_capitaine_Grant/Partie_3/Chapitre_XXI','https://fr.wikisource.org/wiki/Les_Enfants_du_capitaine_Grant/Partie_3/Chapitre_XXII']
titles=['Jules Verne — In Search of the Castaways, Horne edition (Gutenberg 2083)','Jules Verne — Les Enfants du capitaine Grant, Hetzel 1868, I.II','Jules Verne — Les Enfants du capitaine Grant, Hetzel 1868, III.XVII','Jules Verne — Les Enfants du capitaine Grant, Hetzel 1868, III.XXI','Jules Verne — Les Enfants du capitaine Grant, Hetzel 1868, III.XXII']
notes=[L('Полностью прочитанная историческая английская редакция: 26 + 19 + 21 глава. Основной источник событий. Внешняя ссылка раскрывает весь сюжет.','The historical English version read in full: 26 + 19 + 21 chapters. Main narrative witness. The external link reveals the whole plot.'),L('Выборочная проверка начальной записки и единицы широты. Это не сверка всего французского оригинала.','Selected check of the opening message and latitude unit, not a collation of the complete French original.')]+[L('Выборочно проверенная первичная глава. Внешняя страница раскрывает поздние события; открывайте после полного чтения.','A selectively checked primary chapter. The external page reveals later events; open after the full reading.')]*3
sources=[dict(id=i+1,title=titles[i],url=urls[i],role='book',note=notes[i]) for i in range(5)]
data=dict(schemaVersion=2,slug='children-of-captain-grant',title=L('Дети капитана Гранта','The Children of Captain Grant'),author=L('Жюль Верн','Jules Verne'),description=L('Поиски по тридцать седьмой параллели: дети, морская записка и три части большого путешествия.','A search along the thirty-seventh parallel: two children, a message at sea and three parts of a great journey.'),defaultLanguage='ru',defaultTheme='dark',defaultMode='essential',contentMode='narrative',spoilerPolicy='full-plot-in-deep',revision='depth-v2',methodNote=L('Связный пересказ своими словами по полностью прочитанной исторической английской редакции Horne: 66 глав. Это сокращённое приключение, не полный французский оригинал; четыре французские главы сверены выборочно. Вступление Horne не приписано Верну. Островная география и необычайные природные эпизоды принадлежат миру романа; колониальные представления героев не служат современным описанием народов. Короткие режимы оставляют историю незавершённой. Ссылки ведут к полным текстам со спойлерами.','An original-word connected retelling based on a complete reading of the historical Horne-edited English version, 66 chapters. It is a condensed adventure, not the complete French original; four French chapters were selectively checked. Horne’s introduction is not attributed to Verne. Island geography and extraordinary natural episodes belong to the novel; characters’ colonial assumptions do not describe peoples today. Shorter routes leave the story unfinished. External full-text links reveal spoilers.'),sources=sources,media={},screens=screens)
data['targetModes']={name:sum(s['level']<=level for s in screens) for name,level in [('essential',1),('core',2),('deep',3)]}
(HERE/'story-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(HERE/'scene-map.json').write_text(json.dumps(scene_map,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(data['targetModes']))

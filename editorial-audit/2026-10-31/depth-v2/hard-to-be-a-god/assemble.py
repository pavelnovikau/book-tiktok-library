# coding: utf-8
from pathlib import Path
import re,json,html
BASE=Path(__file__).resolve().parent

def parse(lang):
    result={};ch=None
    for p in (BASE/f'draft-{lang}.md').read_text().split('\n\n'):
        if p.startswith('## '):
            h=p[3:].strip();ch='prologue' if h in ['Пролог','Prologue'] else 'epilogue' if h in ['Эпилог','Epilogue'] else 'ch'+re.search(r'\d+',h).group()
            result[ch]=[]
        elif ch and p.strip():result[ch].append(p.strip())
    return result
ru,en=parse('ru'),parse('en')
assert {k:len(v) for k,v in ru.items()}=={k:len(v) for k,v in en.items()}
# One metadata row per paragraph written before segmentation: id | RU title | EN title.
rows={
'prologue':'''lake|День без взрослых|A day without adults
william-tell|Настоящие стрелы|Real arrows
shot|Выше головы|Above his head
forgotten-road|По разные стороны знака|On opposite sides of the sign''',
'ch1':'''night-road|Дон Румата на дороге|Don Rumata on the road
kiun|Человек у стремени|The man at his stirrup
kiun-book|Одна собственная книга|One book of his own
patrol|Патруль у корчмы|The patrol at the inn
shopkeepers|За кружкой пива|Over a mug of beer
kabani|Изобретатель в лесу|The inventor in the forest
midas|Опилки и монеты|Sawdust and coins
condor-arrives|Гость на вертолёте|A visitor by helicopter
first-dispute|Времени не хватает|Not enough time
condor-memory|Стать местным вельможей|Becoming a local lord
gug-arrives|Друг под париком|A friend beneath the wig''',
'ch2':'''uno-morning|Две лохани|Two wash tubs
letters|Утренние письма|The morning's letters
breakfast|Мода на платки|The fashion for handkerchiefs
school|Укрытие в школе|Shelter at the school
gauk-poems|Стихи в оружейной лавке|Poems in the weapons shop
port|Корабли не выпускают|The ships cannot leave
vaga|Счета ночного короля|The night king's accounts
university|Выбрать книгочеев первым|First choice of bookmen''',
'ch3':'''anger|Сжатый кулак|A clenched fist
gauk|На улице Премногоблагодарения|In the Street of Abundant Gratitude
home|Дома ждут|Someone waiting at home
kira|Девушка в кресле|The girl in the armchair
kira-uno|Обед со светильниками|A meal with lamps
kira-family|Почему нельзя домой|Why she cannot go home
white-feather|Белое перо|The white feather''',
'ch4':'''okana-salon|Показать новые ковры|Showing the new carpets
okana-departure|Не получится|He cannot go through with it
pampa-arrives|Пампа больше не пьёт|Pampa no longer drinks
pampa-tavern|Первая чаша|The first drink
pampa-sword|Родовой меч|The ancestral sword
three-prisoners|Государственное дело|A matter of state
okana-news|Рипат у двери|Ripat at the door
drinking-night|Кабаки до рассвета|Taverns until dawn
uno-vigil|Уно с арбалетом|Uno with a crossbow
kira-confession|Это был не сон|It was no dream''',
'ch5':'''lost-court|Кого уже вывезли|Those already taken away
gur|Гур остался|Gur stayed behind
king-shoe|Правая туфля короля|The king's right shoe
reba-smile|Министр улыбается|The minister smiles
purple-chamber|Разговор за портьерой|The conversation behind the curtain
gur-dinner|Сохранились три экземпляра|Three copies survive
court-doctor|Лекарь с сумкой|The physician with a bag
court-medicine|Горькое лекарство|Bitter medicine''',
'ch6':'''leave-home|Сохранить Киру|Keep Kira safe
prince|У спящего мальчика|Beside the sleeping boy
capture|Окно и сеть|The window and the net
prince-bedroom|Мимо открытой спальни|Past the open bedroom''',
'ch7':'''black-escort|Кто распоряжается|Who gives the orders
aba-tsupik|За лиловой портьерой|Behind the purple curtain
interrogation|Чистота золота|The purity of gold
false-budakh|Крик из-за портьеры|A cry behind the curtain
order|Чёрная конница|The black cavalry
reba-bargain|Страх наместника|The governor's fear
uno|Кого нет в прихожей|Missing from the hallway
kira-care|Уксус и лекарство|Vinegar and medicine
kira-bracelet|Браслет для Киры|A bracelet for Kira''',
'ch8':'''blacksmith|Восемь детей кузнеца|The blacksmith's eight children
tameo|Как свободно дышится|How freely one can breathe
clearance|Бумага вместо приказа|A paper instead of an order
prison-bluff|Врач подарен мне|The physician was given to me
budakh-release|Снять петлю|Removing the noose
pampa-release|Друг внизу|A friend below
pampa-rides|Передать баронессе|A message for the baroness
poison|Мешок с лекарствами|The bag of medicines
budakh-meal|Салаты и пирожки|Salads and pastries
budakh-pyramid|Совет всемогущему|Advice to the almighty
budakh-gifts|Дать, защитить, наказать|Give, protect, punish
budakh-remake|Чужая дорога|Their own road''',
'ch9':'''arata-arrives|Монах в кабинете|The monk in the study
arata-scars|Когда его звали Красивым|When he was called the Handsome
arata-lightning|Очень нужны молнии|He needs lightning
arata-targets|Что сделают молнии|What the lightning will do
arata-hope|Надежда за спиной|Hope behind him
arata-leaves|Золото на прежнем месте|The gold in its usual place''',
'ch10':'''budakh-sleep|Пока уснёт Будах|Waiting for Budakh to sleep
condor-reversal|Физически убрать|Physically remove him
earth-decision|Посоветоваться с Базой|Consult the Base
hostage-warning|То, что можно отнять|What can be taken away
kira-book|Книга про них|A book about them
attack|Хозяина не ждали|The master was not expected
kira-window|У окна|At the window''',
'epilogue':'''pashka-account|Рассказ с остановками|A halting account
road-echo|Сидеть и ждать|Sitting and waiting
strawberries|Красное на руках|Red on his hands'''
}
ranges={
'prologue':['001–090','091–149','150–159','160–199'],
'ch1':['001–002','003–034','035–052','053–087','088–091','092–120','121–124','125–136','137–150','151–162','163–174'],
'ch2':['001–035','023–025','035–069','070–095','096–114','115–124','125–142','143–148; ГЛАВА 3:P002'],
'ch3':['001–007','008–040','040–053','054–084','085–114','115–120','121–132'],
'ch4':['001–030','031–053','054–091','092–118','119–157','158–160','161–178','178–184','185–196','197–218'],
'ch5':['001–003','003–018','011–024','024–038','039–074','075–118','119–138','139–158'],
'ch6':['001–013','014–018','019–032','033'],
'ch7':['001–043','044–147','148–184','154–168,185–191','192–210','211–229','230–247','248–264','265–280'],
'ch8':['001–020','021–058','059–082','083–118','119–136','137–147','148–176','177','178–184','185–204','205–212','213–219'],
'ch9':['001–008,016–021','009–015','022–038','039–042','043–047','048–053'],
'ch10':['001–012','013–039','040–055','056–071','072–082','083–101','102–103'],
'epilogue':['001–011','012–033','034–037']}
essential={'prologue':{1,2,3},'ch1':{1,6,7,8,9,11},'ch3':{4,6},'ch5':{2,3,4,7,8}}
core={'prologue':{1,2,3,4},'ch1':set(range(1,12))-{10},'ch2':set(range(1,9)),'ch3':{1,4,5,6,7},'ch4':set(range(1,11))-{7},'ch5':set(range(1,9))-{6}}
sections={
'prologue':('У озера','By the lake'),'ch1':('Ночная дорога','The night road'),'ch2':('Поиски','The search'),'ch3':('Дом','Home'),'ch4':('Вечер','The evening'),'ch5':('При дворе','At court'),'ch6':('Дежурство','On duty'),'ch7':('После ночи','After the night'),'ch8':('По городу','Through the city'),'ch9':('В кабинете','In the study'),'ch10':('Возвращение','Returning'),'epilogue':('На Земле','On Earth')}

def add(id,level,titles,bodies,chapter=None,locator=None,**extra):
    s={'id':id,'level':level,'claimType':'book','sources':[1] if locator else [],'copy':{l:{'section':sections[chapter][i] if chapter else ('Чтение' if l=='ru' else 'Reading'),'title':titles[i],'body':'<p>'+html.escape(bodies[i],quote=False)+'</p>'} for i,l in enumerate(['ru','en'])},**extra}
    if locator:s['evidenceLocator']=locator
    screens.append(s)
    return s
screens=[]
cover=add('cover',1,('Трудно быть богом','Hard to Be a God'),('Румата ищет пропавшего врача в городе, где опасно уметь читать. Под именем дворянина живёт человек с Земли, способный на многое и обязанный не убивать. «Главное» — короткое начало, «Суть книги» — более подробный путь до дворцового представления. Полная история и развязка — в режиме «Глубоко» после предупреждения.','Rumata searches for a missing physician in a city where reading is dangerous. Behind a nobleman’s name lives a visitor from Earth, powerful and bound not to kill. Essential offers a short opening; Core follows a fuller path to the court performance. The complete story and ending are in Deep, after a warning.'),type='cover')
cover['sources']=[1]
for l,author in [('ru','Аркадий и Борис Стругацкие'),('en','Arkady and Boris Strugatsky')]:
    cover['copy'][l]['section']=author
    cover['copy'][l]['subtitle']='Пересказ повести' if l=='ru' else 'A condensed retelling'
    cover['copy'][l]['visualAlt']='Типографическая обложка без сюжетной иллюстрации' if l=='ru' else 'A typographic cover without a plot illustration'
add('deep-warning',3,('Глубоко: история до конца','Deep: the story to its end'),('Этот маршрут включает поздние события, судьбы героев и последнюю сцену повести. Режимы «Главное» и «Суть книги» не раскрывают этих исходов. Если хотите сохранить развязку, переключите глубину. Здесь начинается полный расширенный пересказ.','This route includes the later events, the characters’ outcomes and the novel’s last scene. Those outcomes remain hidden in Essential and Core. Switch depth to preserve the ending. The full expanded condensation begins here.'))
maprows=[]
for chapter,paras in ru.items():
    meta=[x.split('|') for x in rows[chapter].splitlines()]
    assert len(meta)==len(paras)==len(ranges[chapter])
    label='ПРОЛОГ' if chapter=='prologue' else 'ЭПИЛОГ' if chapter=='epilogue' else 'ГЛАВА '+chapter[2:]
    for n,(r,e,m,ran) in enumerate(zip(paras,en[chapter],meta,ranges[chapter]),1):
        level=1 if n in essential.get(chapter,set()) else 2 if n in core.get(chapter,set()) else 3
        items=[(m[0],level,(m[1],m[2]),(r,e),f'D2:{label}:P{ran}')]
        if chapter=='ch3' and n==2:
            a,b=r.split('Оружейная лавка',1);c,d=e.split("Gauk's shop",1)
            items=[('camera',2,('Камень на обруче','The stone in the circlet'),(a.strip(),c.strip()),'D2:ГЛАВА 3:P008–017'),('gauk',3,('Лавка напротив ворот','The shop opposite the gateway'),('Оружейная лавка'+b,"Gauk's shop"+d),'D2:ГЛАВА 3:P018–040')]
        if chapter=='ch3' and n==3:
            a,b=r.split('Дома его встретил',1);c,d=e.split('At home, gloomy',1)
            items=[('revenge-thought',3,('Цена воображаемой мести','The cost of imagined revenge'),(a.strip(),c.strip()),'D2:ГЛАВА 3:P040–041'),('home',1,(m[1],m[2]),('Дома его встретил'+b,'At home, gloomy'+d),'D2:ГЛАВА 3:P042–053')]
        for id,lev,titles,bodies,locator in items:
            s=add(id,lev,titles,bodies,chapter,locator)
            maprows.append({'id':id,'level':lev,'draftSection':chapter,'draftParagraph':n,'title':dict(zip(['ru','en'],titles)),'evidenceLocator':locator})
final=add('final',1,('Конец выбранной глубины','End of the selected depth'),('Вы дошли до конца выбранного маршрута. Режимы «Главное» и «Суть книги» не раскрывают финал; «Глубоко» рассказывает историю до последней сцены. Можно начать выбранный маршрут заново или открыть режим «Глубоко» после предупреждения.','You have reached the end of the selected route. Essential and Core leave the ending unrevealed; Deep follows the story through its last scene. Restart the selected route, or open Deep explicitly after its warning.'),final=True)
for l in ['ru','en']:final['copy'][l]['section']='Маршрут чтения' if l=='ru' else 'Reading route'
for s in screens:
    if s['id'] in ['deep-warning','final']:s['claimType']='synthesis'
counts={m:sum(s['level']<=lev for s in screens) for m,lev in [('essential',1),('core',2),('deep',3)]}
data={'schemaVersion':2,'slug':'hard-to-be-a-god','title':{'ru':'Трудно быть богом','en':'Hard to Be a God'},'author':{'ru':'Аркадий и Борис Стругацкие','en':'Arkady and Boris Strugatsky'},'audience':'adult','spoilerPolicy':'full-plot-in-deep','contentMode':'narrative','description':{'ru':'Расширенный пересказ: Румата ищет врача и укрывает людей в Арканаре. Три вложенные глубины; развязка только в режиме «Глубоко» после согласия.','en':'An expanded condensed story: Rumata seeks a physician and shelters people in Arkanar. Three nested depths; the ending only in Deep after consent.'},'defaultLanguage':'ru','defaultTheme':'dark','defaultMode':'essential','targetModes':counts,'methodNote':{'ru':'Пересказ своими словами по полному русскому электронному тексту официального сайта авторов. В этой работе последовательно прочитаны пролог, все десять глав и эпилог; печатные редакции не сверялись. Сначала написан связный русский рассказ, затем его английский перевод и разбиение. Английский текст — перевод пересказа, а не опубликованный перевод книги. Внешний источник раскрывает весь сюжет.','en':'An original-word condensation of the complete Russian electronic text on the official author site. The prologue, all ten chapters and epilogue were read continuously for this work; print editions were not collated. Connected Russian prose was written first, followed by its English translation and segmentation. English translates the condensation, not a published translation of the novel. The external source reveals the full plot.'},'sources':[{'id':1,'title':'Аркадий и Борис Стругацкие · Трудно быть богом · RUSF','url':'https://www.rusf.ru/abs/books/tbb100.htm','role':'book','note':{'ru':'Официальный полный русский электронный текст, прочитан полностью в последовательных диапазонах. Локаторы D2 обозначают непустые HTML-абзацы внутри частей, не печатные страницы. Карта видимых сцен доступна ниже. Ссылка содержит спойлеры.','en':'The official complete Russian electronic witness, read throughout in consecutive ranges. D2 locators identify nonempty HTML paragraphs within source divisions, not printed pages. The visible-scene map is available below. The link contains spoilers.'}}],'media':{},'screens':screens}
(BASE/'story-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(BASE/'scene-map.json').write_text(json.dumps(maprows,ensure_ascii=False,indent=2)+'\n')
# Exact narrative metrics: same Unicode word definition as the maintained builder.
word=lambda s:len(re.findall(r"[^\W_][^\W_\u200b]*",s)) # replaced below for explicit Unicode parity via JS in QA
stats={}
for mode,lev in [('essential',1),('core',2),('deep',3)]:
    selected=[s for s in screens if s['level']<=lev and 'evidenceLocator' in s]
    stats[mode]={'screensIncludingFraming':counts[mode],'narrativeScreens':len(selected),'whitespaceNarrativeWords':{l:sum(len(re.sub('<[^>]+>',' ',s['copy'][l]['body']).split()) for s in selected) for l in ['ru','en']}}
(BASE/'draft-metrics.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats,ensure_ascii=False,indent=2))

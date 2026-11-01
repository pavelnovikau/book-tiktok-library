from pathlib import Path
import hashlib,json,re

H=Path(__file__).resolve().parent.parent
R=H/'root-review'
data=json.loads((H/'story-data.json').read_text())
ids=[s['id'] for s in data['screens'][1:-1]]
drafts={}
for lang in ['ru','en']:
 text=(H/f'draft-{lang}.md').read_text()
 parts=re.split(r'^## ',text,flags=re.M)
 drafts[lang]={'prefix':parts[0],'units':{id:part for id,part in zip(ids,parts[1:])}}
 assert len(parts)==67
changed=set()

def replace(id,lang,old,new):
 unit=drafts[lang]['units'][id]
 assert unit.count(old)==1,(id,lang,old)
 drafts[lang]['units'][id]=unit.replace(old,new)
 changed.add(id)

def paragraphs(id,lang,new):
 unit=drafts[lang]['units'][id]
 title=unit.split('\n',1)[0]
 assert len(new)==2
 drafts[lang]['units'][id]=title+'\n\n'+'\n\n'.join(new)+'\n\n'
 changed.add(id)

replace('two-streams','ru','Кнапп и Зерацки начинают именно с такого недоумения.','Джейк Кнапп и Джон Зерацки (ДЗ) начинают именно с такого недоумения.')
replace('two-streams','en','Knapp and Zeratsky begin with that bewilderment.','Jake Knapp and John Zeratsky (JZ) begin with that bewilderment.')
replace('wooden-railway','ru','младший Флинн играл с локомотивом','младенец Флинн обслюнявливал локомотив')
replace('wooden-railway','en','his younger son Flynn was playing with an engine','his infant son Flynn was drooling on an engine')
replace('might-do','ru','у ДЗ и Мишель накапливались','у ДЗ и его жены Мишель накапливались')
replace('might-do','en','left JZ and Michelle with hundreds of jobs','left JZ and his wife Michelle with hundreds of jobs')
replace('wholehearted','ru','похожую вовлечённость в плавание','похожую вовлечённость в плавание под парусом')
replace('life-turns','ru','У ДЗ и Мишель таким направлением оказалось плавание.','У ДЗ и его жены Мишель таким направлением оказалось плавание под парусом.')
replace('life-turns','en','For JZ and Michelle, sailing provided that direction.','For JZ and his wife Michelle, sailing provided that direction.')
replace('chocolate-default','ru','после автомобильной поездки с Холли','после автомобильной поездки с женой Холли')
replace('chocolate-default','en','after a drive with Holly','after a drive with his wife Holly')
replace('woods-meditation','ru','после совета Холли','после совета жены Холли')
replace('woods-meditation','en','After Holly recommended Headspace,','After his wife Holly recommended Headspace,')
replace('caregiving','ru','Джейк и Холли услышали','Джейк и его жена Холли услышали')
replace('caregiving','en','Jake and Holly heard','Jake and his wife Holly heard')

replace('battery-body','ru','Рассказывая о них, важно не превращать авторские утверждения о здоровье в отдельное медицинское руководство. ','')
replace('battery-body','en','Describing it must not turn their health assertions into a separate medical handbook. ','')

paragraphs('brief-workout','ru',[
 'Для дней с малым количеством времени авторы рассматривают короткую интенсивную зарядку. Ссылаясь на популярные изложения исследований, они считают интенсивные серии эффективнее более длительной умеренной нагрузки и особенно ценят их как быстрый способ почувствовать прилив сил. Это обоснование книги, а не независимо проверенное превосходство для любого человека. При этом авторы не предлагают ограничить всё движение только такими сериями. Один из их вариантов — семиминутный комплекс из двенадцати упражнений с тридцатисекундными интервалами работы и десятисекундными паузами.',
 'Отдельно описан личный вариант ДЗ «три на три»: трижды в неделю три вида движения — отжимания, приседания и поднятие веса или подтягивания. Книга описывает по одному подходу с максимально возможным для него числом повторений и минутой отдыха после каждого вида. ДЗ использовал доступные предметы вместо обязательного спортивного оборудования. Сложность можно было менять: например, отжиматься от скамьи, если пол пока труден. Этот вариант соседствует с прогулками и отдыхом; по мысли авторов, короткая зарядка помогает втиснуть движение в занятый день, но не требует добавлять её поверх всех остальных нагрузок ради выполнения полного списка.'
])
paragraphs('brief-workout','en',[
 'For days with little time, the authors consider brief intense exercise. Citing popular accounts of research, they regard intense sequences as more effective than longer moderate activity and especially value them as a quick way to feel replenished. This is the book’s rationale, rather than independently verified superiority for every person. They do not suggest restricting all movement to these sequences. One option is a seven-minute sequence of twelve movements, with thirty-second activity intervals and ten-second breaks.',
 'JZ’s personal “three by three” is described separately: three times a week, three movement types—push-ups, squats, and lifting weight or pull-ups. The book describes one set with as many repetitions as he can manage, followed by a minute’s rest after each type. JZ used available objects rather than compulsory gym equipment. Difficulty could change: for example, pushing against a bench when the floor was too difficult. This option sits beside walking and rest. In the authors’ reasoning, a brief workout fits movement into a busy day rather than adding another requirement on top of every other activity merely to complete the list.'
])
replace('prepared-food','ru','В исходном тексте есть широкие утверждения о питании и эволюции; в этом изложении они не превращаются в отдельные доказанные лечебные свойства.','Их объяснение опирается на эволюционный образ охотника-собирателя: простая узнаваемая еда представляется авторам топливом, к которому приспособлен организм.')
replace('prepared-food','en','The source contains broad assertions about food and evolution; this account does not turn them into separately established therapeutic properties.','Their explanation uses the evolutionary picture of a hunter-gatherer: they regard simple recognisable food as fuel the body is adapted to use.')
replace('fasting-snacks','ru','ДЗ экспериментировал с периодическим голоданием и описывал ясность мысли при работе утром без еды.','ДЗ экспериментировал с периодическим голоданием. Сначала голод отвлекал его, но после нескольких попыток он привык и стал описывать ясность мысли при работе утром без еды.')
replace('fasting-snacks','en','JZ experimented with intermittent fasting and described mental clarity while working without food in the morning.','JZ experimented with intermittent fasting. Hunger distracted him initially; after several attempts, he reported adapting and experiencing mental clarity while working without food in the morning.')
replace('fasting-snacks','ru','Здесь нет основания превращать такой рассказ в универсальную рекомендацию читателю или повторять обещания защиты от болезней как установленные результаты.','Однако именно ясность мысли ДЗ называет главным для своей задачи преимуществом: ему хотелось находить силы и внимание для выбранного дела. Его личное наблюдение не устанавливает обещанные долгосрочные эффекты для здоровья.')
replace('fasting-snacks','en','That does not justify turning the account into a universal recommendation or repeating disease-protection promises as established outcomes.','For his purpose, however, JZ calls mental clarity the chief advantage: he wants energy and attention for the chosen activity. His personal observation does not establish the promised long-term health effects.')
replace('chocolate-default','ru','Для этого рассказа достаточно сохранить реальный опыт Джейка и устройство замены, не обещая читателю клинического эффекта.','Свою замену авторы объясняют меньшим количеством сахара и сытностью тёмного шоколада. Джейк связывает с ней более ровное самочувствие; это его опыт изменения привычки, а не установленный клинический эффект.')
replace('chocolate-default','en',"This account can preserve Jake's actual experience and the substitution's mechanism without promising a clinical effect.",'The authors explain the substitution through dark chocolate’s lower sugar content and satiety. Jake associates it with feeling steadier; this is his experience of changing a habit rather than an established clinical effect.')
replace('available-sleep','ru','Этот фрагмент не превращается здесь в самостоятельное правило запрещать себе необходимый сон. ','')
replace('available-sleep','en','This passage does not become a standalone rule against obtaining necessary sleep. ','')

for lang,draft in drafts.items():
 text=draft['prefix']+''.join('## '+draft['units'][id] for id in ids)
 (H/f'draft-{lang}.md').write_text(text)

prepare=(H/'prepare.py').read_text()
marker='tactics=[]\nfor k,(n,i,a) in enumerate(starts):'
assert prepare.count(marker)==1
replacement='''# Root read the actual ranked-priority procedure and all three subsequent tactic headings.
# Internal step numbers4–6 are not global numbered tactics4–6.
root_starts=json.loads((P/'root-review/primary-locator-repairs.json').read_text())
starts=[(n,root_starts[str(n)]['record'],root_starts[str(n)]['paragraphStart']) if str(n) in root_starts else (n,i,a) for n,i,a in starts]
for n,fix in root_starts.items():
 assert primary[fix['record']]['paragraphs'][fix['paragraphStart']-1]==fix['heading']
tactics=[]
for k,(n,i,a) in enumerate(starts):'''
prepare=prepare.replace(marker,replacement)
assert prepare.count('Это черновик для личной редакторской проверки.')==1
assert prepare.count(' A draft awaiting personal editorial review.')==1
prepare=prepare.replace(' Это черновик для личной редакторской проверки.','').replace(' A draft awaiting personal editorial review.','')
(H/'prepare.py').write_text(prepare)
l=json.loads((R/'reading-ledger.json').read_text())
l['repairsImplementedPairIds']=sorted(changed)
l['repairsImplementedNotYetReread']=True
l['globalMethodDraftLabelRemoved']=True
l['rootRepairScope']='Same66 authored units and24/48/68 routes. Source-grounded clarity/flow/identity changes; four tactic-map extents corrected. Root personal rereading and fresh QA remain pending.'
(R/'reading-ledger.json').write_text(json.dumps(l,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'changedPairs':len(changed),'ids':sorted(changed),'sourceMapStartsCorrected':[4,5,6],'sourceMapExtentsChanged':[3,4,5,6],'rootAcceptance':False}))

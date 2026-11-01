from pathlib import Path
import re,json,html,hashlib,datetime
ROOT=Path(__file__).parent
# Drafts exist before these passage assignments. Each paragraph remains verbatim.
def read_draft(lang):
 chunks=(ROOT/f'draft.{lang}.md').read_text().strip().split('\n\n');sections=[]
 for chunk in chunks:
  if chunk.startswith('# '): continue
  if chunk.startswith('## '): sections.append({'heading':chunk[3:],'paras':[]})
  else: sections[-1]['paras'].append(chunk)
 return sections
ru,en=read_draft('ru'),read_draft('en')
levels=[[1,2,2,1],[3,3,2,3],[1,2,2,1],[2,3,3,3],[2,1,3,3],[1,2,1,2],[2,3,3,1],[2,1,2,3],[3,1,2,1],[3,1,3,2],[1,2,3,2],[1,3,2,2,3],[2,2,3,1],[2,3,1,1,1],[1,2,3,2,2],[1,3,1,3],[2,2,2,2,2,2],[2]*10,[1,1,1]]
titles=[
 [('Четыре тысячи недель','Four thousand weeks'),('Система и её обещание','The system and its promise'),('Скамейка в Бруклине','A bench in Brooklyn'),('Не только вопрос настроя','More than a matter of attitude')],
 [('Ритм самих дел','The rhythm of tasks'),('Час, который можно продать','An hour for sale'),('Подготовка без конца','Preparation without end'),('От чего защищала продуктивность','What productivity protected against')],
 [('Письмо порождает письмо','One message produces another'),('Требования тоже растут','Standards grow too'),('Письмо из Нью-Дели','A letter from New Delhi'),('Важное среди незавершённого','Important work among unfinished things')],
 [('Неисчерпаемый мир','An inexhaustible world'),('Что исчезает вместе с неудобством','What disappears with inconvenience'),('Усилие в открытке','The effort in a card'),('Час до первой чашки чая','An hour before the first cup of tea')],
 [('Мы уже внутри времени','Already inside time'),('Выбрать — значит закрыть','Choosing means closing'),('Болезнь не становится благом','Illness does not become a good'),('Возможность, которой могло не быть','An opportunity that might not exist')],
 [('Не все большие камни поместятся','Not all the large rocks fit'),('Сначала выделить время','Give time first'),('Ограничить начатое','Limit work in progress'),('Отказ от привлекательного','Refusing the attractive')],
 [('Мечеть, оставшаяся замыслом','The mosque that stayed an idea'),('Письма Кафки','Kafka’s letters'),('Будущее без противоречий','A future without contradictions'),('Верность и право уйти','Commitment and the right to leave')],
 [('Сорок четыре минуты','Forty-four minutes'),('Из чего складывается опыт','What experience consists of'),('Лента остаётся в голове','The feed remains in the mind'),('Настоящий пляж и настроенная лента','A real beach and a tuned feed')],
 [('Рассказ Шинзена Янга','Shinzen Young’s account'),('Важное бывает неудобным','Important things can be uncomfortable'),('Выход найдётся и без телефона','An exit exists without a phone'),('Не ждать исчезновения дискомфорта','Do not await discomfort’s disappearance')],
 [('Откуда берётся желание предусмотреть всё','The wish to foresee everything'),('Три часа — ожидание','Three hours are an expectation'),('То, чего мы не планировали','What we never planned'),('Намерения без расписки будущего','Intentions without a future guarantee')],
 [('Бесконечное «вот когда»','An endless “once I finally”'),('Ребёнок уже существует','The child already exists'),('Непроданный час','An unsold hour'),('Сияние, которое надо правильно пережить','An aurora to experience correctly')],
 [('Зачем оправдывать отдых','Why must rest justify itself?'),('Другая история досуга','Another history of leisure'),('Остановка требует поддержки','Stopping needs support'),('Прогулку не нужно завершать','A walk needs no completion'),('Право быть неумелым','Permission to be unskilled')],
 [('Ещё несколько секунд','A few more seconds'),('Собственное время чтения','Reading’s own time'),('Облегчение, ускоряющее круг','Relief that accelerates the loop'),('Терпение как действие','Patience as action')],
 [('Три часа перед Дега','Three hours before Degas'),('Сначала рассмотреть механизм','First inspect the mechanism'),('Проблемы и небольшие порции','Problems and small portions'),('Остаться в автобусе','Stay on the bus'),('Когда уходить, когда оставаться','When to leave, when to stay')],
 [('Часов мало без совпадения','Hours need alignment'),('Свобода без общих вечеров','Freedom without shared evenings'),('Отпуск и фика','Holidays and fika'),('Выходной в одиночку','A day off alone'),('Свобода участвовать','Freedom to participate')],
 [('Не требовать вселенского следа','Do not require a cosmic mark'),('Шестьдесят столетних жизней','Sixty hundred-year lives'),('Обычное тоже имеет значение','The ordinary matters too'),('Что возвращать после перерыва','What to restore after interruption')],
 [('Жизнь всё ещё как черновик','Life still feels like a draft'),('Первый вопрос: комфорт или рост','First question: comfort or growth'),('Второй: невыполнимая норма','Second: an impossible standard'),('Третий: разрешение быть собой','Third: permission to be oneself'),('Четвёртый: ожидание готовности','Fourth: waiting to be ready'),('Пятый: результат за пределами жизни','Fifth: results beyond a lifetime')],
 [('1. Конечный объём работы','1. A finite amount of work'),('2. Большие проекты по очереди','2. Large projects in sequence'),('3. Выбранное несовершенство','3. Chosen imperfection'),('4. Замечать сделанное','4. Notice what is done'),('5. Ограничить личный фронт помощи','5. Limit personal civic commitments'),('6. Более скучные устройства','6. More boring devices'),('7. Новизна в обычном','7. Novelty in the ordinary'),('8. Любопытство к человеку','8. Curiosity about another person'),('9. Щедрость без идеального момента','9. Generosity without an ideal moment'),('10. Практика ничегонеделания','10. Practising doing nothing')],
 [('Следующее необходимое дело','The next necessary thing'),('Действие без обещанного спасения','Action without promised rescue'),('Не всё. Но всерьёз','Not everything, but seriously')]
]
# Locators refer to the exact arrays read and acknowledged in primary-reading-ledger.json.
def loc(f,a,b):return {'file':'OEBPS/Text/'+f+'.html','firstParagraph':a,'lastParagraph':b}
def C(n,a,b):return loc('content'+str(n),a,b)
refs=[
 [[C('04',3,7)],[C('04',16,16),C(1,19,20)],[C(1,21,22)],[C(1,30,30)]],
 [[C(1,3,9)],[C(1,13,15)],[C(1,15,17)],[C(1,22,25)]],
 [[C(2,9,11)],[C(2,9,12)],[C(2,20,22)],[C(2,12,13),C(2,23,24)]],
 [[C(2,15,18)],[C(2,24,29)],[C(2,28,29)],[C(2,30,34)]],
 [[C(3,3,10)],[C(3,8,14)],[C(3,15,18)],[C(3,21,26)]],
 [[C(4,3,5)],[C(4,7,8)],[C(4,9,11)],[C(4,12,13)]],
 [[C(4,15,17)],[C(4,17,21)],[C(4,22,25)],[C(4,25,29),C(4,10,10)]],
 [[C(5,3,7)],[C(5,5,9)],[C(5,11,17)],[C(5,15,18)]],
 [[C(6,3,5)],[C(6,6,10)],[C(6,11,14)],[C(6,15,17)]],
 [[C(7,3,7)],[C(7,9,11)],[C(7,12,14)],[C(7,16,19)]],
 [[C(8,3,8)],[C(8,9,14)],[C(8,17,23)],[C(8,25,31)]],
 [[C(9,3,6)],[C(9,7,12)],[C(9,20,25)],[C(9,27,30)],[C(9,32,36)]],
 [[C(10,3,7)],[C(10,8,10)],[C(10,12,17)],[C(10,18,18),C(11,3,3)]],
 [[C(11,4,11)],[C(11,13,20)],[C(11,22,24)],[C(11,25,27)],[C(4,9,10),C(11,25,27)]],
 [[C(12,3,6)],[C(12,8,10)],[C(12,11,14)],[C(12,15,16),C(12,28,28)],[C(12,18,29)]],
 [[C(13,13,15)],[C(13,16,18)],[C(13,20,24)],[C(13,7,12)]],
 [[C(14,7,14)],[C(14,15,17)],[C(14,18,21)],[C(14,22,25)],[C(14,26,28)],[C(14,29,31)]],
 [[C(16,4,6),C(4,9,10)],[C(16,7,8)],[C(16,9,11)],[C(16,12,13)],[C(16,14,16)],[C(16,17,18)],[C(16,19,21)],[C(16,22,24)],[C(16,25,26)],[C(16,27,29)]],
 [[C(14,32,36)],[C(15,5,14)],[C('04',22,23),C(14,10,12),C(15,14,14)]]
]
# Readability-only edits made to both connected drafts before segmenting.
for lang in ['ru','en']:
 f=ROOT/f'draft.{lang}.md';t=f.read_text()
 if lang=='ru':t=t.replace('Повседневное отвлечение, по мысли автора, часто тоже начинается','Повседневное отвлечение, по мысли автора, часто начинается').replace('Здесь условные четыре тысячи недель','Условные четыре тысячи недель')
 else:t=t.replace('Everyday distraction, the author suggests, often also begins','Everyday distraction, the author suggests, often begins').replace('Here the illustrative four thousand weeks','The illustrative four thousand weeks')
 f.write_text(t)
ru,en=read_draft('ru'),read_draft('en')
source={'id':1,'title':'Oliver Burkeman · Four Thousand Weeks / Четыре тысячи недель · owned RU edition, 2023','url':'https://www.oliverburkeman.com/fourthousandweeks','role':'book','note':{'ru':'Основа — предоставленное частное извлечение русского издания: перевод Е. Серегиной, Альпина Паблишер / Альпина Диджитал, 2023; ISBN 978-5-9614-8639-1. Последовательно прочитаны введение, все 14 глав, послесловие и приложение; заголовки частей и примечания проверены отдельно. Ссылка ведёт на страницу автора, а не к частному тексту. Английский пересказ создан по этой же проверенной основе; полной сверки с английским изданием не было.','en':'Based on the supplied private extraction of the Russian edition: translated by E. Seregina, Alpina Publisher / Alpina Digital, 2023; ISBN 978-5-9614-8639-1. Introduction, all 14 chapters, afterword and appendix were read continuously; part headings and notes separately. The link opens the author’s book page, not the private text. The English exposition uses this same checked basis; no complete English-edition collation was performed.'}}
method={'ru':'Связный оригинальный пересказ аргумента: сначала русский текст, затем соответствующий английский, после — короткие фрагменты трёх вложенных глубин. Подробный маршрут развивает все главы, пять заключительных вопросов и десять приёмов, но сокращает часть случаев, исторических подробностей и цитат. Исторические и исследовательские примеры переданы как сообщения книги, без независимой проверки всех исходных работ. В предоставленном текстовом извлечении изображения отсутствуют: обложка и визуальное содержание издания не сверены и не воспроизводятся. Это не полный текст и не авторизованный перевод.','en':'An original connected explanation of the argument: Russian prose first, corresponding English next, short passages in three nested depths afterwards. Deep develops all chapters, five closing questions and ten techniques, while omitting some cases, historical detail and quotations. Historical and research examples are attributed to the book; the underlying works have not all been independently checked. The supplied text extraction contains no images: the edition’s cover and visual material were neither collated nor reproduced. This is neither the full text nor an authorized translation.'}
cover={'id':'cover','level':1,'type':'cover','sources':[],'copy':{}}
for lang,title,author,framing in [('ru','Четыре тысячи недель','Оливер Беркман · Тайм-менеджмент для смертных','Как выбирать в ограниченной жизни, не превращая её в подготовку к будущему. Короткий маршрут даёт общий аргумент; средний добавляет практики, самый подробный — случаи и оговорки.'),('en','Four Thousand Weeks','Oliver Burkeman · Time Management for Mortals','How to choose within a limited life without making it preparation for the future. The short route carries the argument; the middle adds practices, the fullest develops cases and qualifications.')]:
 cover['copy'][lang]={'section':'Книга' if lang=='ru' else 'Book','title':title,'subtitle':author,'body':'<p>'+framing+'</p>','visualAlt':'Типографическая заставка: 4000 недель.' if lang=='ru' else 'Typographic title graphic: 4000 weeks.'}
screens=[cover];pairs=[]
for i,(r,e) in enumerate(zip(ru,en)):
 assert len(r['paras'])==len(e['paras'])==len(levels[i])==len(titles[i])==len(refs[i])
 for j,(rp,ep) in enumerate(zip(r['paras'],e['paras'])):
  sid=f'part-{i+1:02}-passage-{j+1:02}'
  s={'id':sid,'level':levels[i][j],'claimType':'book','sources':[1],'primaryLocators':refs[i][j],'copy':{}}
  for lang,sec,body,k in [('ru',r,rp,0),('en',e,ep,1)]:s['copy'][lang]={'section':sec['heading'],'title':titles[i][j][k],'body':'<p>'+html.escape(body,quote=False)+'</p>'}
  if i==18 and j==2:s['final']=True
  screens.append(s);pairs.append({'id':sid,'section':i+1,'paragraph':j+1,'level':s['level'],'primaryLocators':s['primaryLocators']})
data={'schemaVersion':2,'slug':'four-thousand-weeks','title':{'ru':'Четыре тысячи недель','en':'Four Thousand Weeks'},'description':{'ru':'Развёрнутый пересказ книги Оливера Беркмана о конечности, выборе, внимании и совместном времени.','en':'A developed account of Oliver Burkeman’s argument about finitude, choice, attention and shared time.'},'defaultLanguage':'ru','defaultTheme':'dark','defaultMode':'essential','contentMode':'explanatory','progressNamespace':'book-tiktok.four-thousand-weeks.depth-v2.','targetModes':{m:sum(s['level']<=v for s in screens) for m,v in [('essential',1),('core',2),('deep',3)]},'methodNote':method,'sources':[source],'media':{},'screens':screens}
# Use builder's Unicode lexical counter, rather than whitespace counts.
def wc(s):
 s=re.sub('<[^>]+>',' ',s);s=re.sub(r'&(?:nbsp|amp|lt|gt|quot|#39);',' ',s,flags=re.I)
 return len(re.findall(r"[^\W_][\w'’\-–—]*",s,re.U))
def minutes(n,lang):
 import math
 n=max(1,math.ceil(n));return f'{n} min' if lang=='en' else f'{n} '+('минута' if n%10==1 and n%100!=11 else 'минуты' if n%10 in [2,3,4] and n%100 not in [12,13,14] else 'минут')
data['modes']={}
for mode,level in [('essential',1),('core',2),('deep',3)]:
 data['modes'][mode]={'minutes':{l:minutes(sum(wc(s['copy'][l]['title']+' '+s['copy'][l].get('subtitle','')+' '+s['copy'][l]['body']) for s in screens if s['level']<=level)/(180 if l=='ru' else 220),l) for l in ['ru','en']}}
(ROOT/'story-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(ROOT/'passage-map.json').write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')
for mode,level in [('essential',1),('core',2),('deep',3)]:
 for lang in ['ru','en']:
  chunks=[f'# {data["title"][lang]} — {mode}\n']
  for s in screens:
   if s['level']>level:continue
   c=s['copy'][lang];chunks += [f'## {s["id"]} · {c["title"]}\n',html.unescape(re.sub('<[^>]+>','',c['body']))+'\n']
  (ROOT/f'route.{mode}.{lang}.md').write_text('\n'.join(chunks))
stages=json.loads((ROOT/'authoring-stages.json').read_text());stages['segmentationStage']={'atUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'paragraphs':len(pairs),'note':'One natural paragraph per phone passage; no count quota. Two small bilingual continuity edits remove references to a skipped predecessor.'};(ROOT/'authoring-stages.json').write_text(json.dumps(stages,ensure_ascii=False,indent=2)+'\n')
print(data['targetModes'],data['modes'])

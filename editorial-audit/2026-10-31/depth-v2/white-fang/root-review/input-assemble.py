from pathlib import Path
import re,json,hashlib,html,datetime
H=Path(__file__).resolve().parent
S=Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-1-private/white-fang/primary.txt')
SHA='3c7226d00fd9b169f0016635d0e461501620f343220ee18db7ca9f083f4ad3f4'
def sha(b):return hashlib.sha256(b).hexdigest()
assert sha(S.read_bytes())==SHA

def parse(lang):
 s=(H/f'draft-{lang}.md').read_text()
 return [dict(heading=c.strip().split('\n\n')[0],paragraphs=c.strip().split('\n\n')[1:]) for c in s.split('\n## ')[1:]]
ru,en=parse('ru'),parse('en');assert len(ru)==len(en)==25
# Written after both complete connected drafts; each unit is one whole original paragraph.
# key, exact inclusive source chapter lines, paragraph levels, paragraph titles RU / EN
spec=[
('i-1',83,398,[1,1,1],['Ящик на нартах','Лишняя порция','Пятеро к утру'],['The box on the sled','An extra portion','Five by morning']),
('i-2',399,831,[1,1,2],['На краю света костра','Кофе для Билла','Ружьё ещё не поднято'],['At the edge of firelight','Coffee for Bill','Before the rifle rises']),
('i-3',832,1214,[1,2,3,2,2,1],['Три выстрела','Гроб над снегом','Собственные пальцы','Сон о форте','Разрывы в огне','Четыре упряжки'],['Three shots','The coffin above the snow','His own fingers','A dream of the fort','Gaps in the fire','Four sleds']),
('ii-1',1220,1561,[1,2,2],['После голода','Огни за деревьями','Заяц в воздухе'],['After hunger','Fires beyond the trees','The rabbit in the air']),
('ii-2',1562,1843,[1,2,2],['Пять слепых комочков','Охотники ждут','Ноша Одноглазого'],['Five blind bundles','The hunters wait','One Eye’s burden']),
('ii-3',1844,2027,[1,1,3],['Четвёртая стена','Пустое место у входа','К белому свету'],['The fourth wall','The empty place at the entrance','Towards the white light']),
('ii-4',2028,2399,[1,2,2,2,2],['Шаг в воздух','Семеро в гнезде','Крыло в зубах','Ненадёжная дорога','Материнская пасть'],['A step into air','Seven in the nest','The wing between his teeth','An unreliable path','His mother’s jaws']),
('ii-5',2400,2592,[1,1,1],['Мясо из чужого логова','Под низким потолком','Неделя в пещере'],['Meat from another lair','Under the low roof','A week in the cave']),
('iii-1',2598,2971,[1,1,1,2],['Кичи','Белый Клык','Стены, которые растут','Обожжённый язык'],['Kiche','White Fang','Walls that grow','A burnt tongue']),
('iii-2',2972,3258,[2,1,1],['Обход между жилищами','Вслед за лодкой','На дне лодки'],['The route between dwellings','After the canoe','In the canoe’s bottom']),
('iii-3',3259,3415,[2,3],['За хозяйской спиной','Вода уносит след'],['Behind the master','Water takes the trail']),
('iii-4',3416,3589,[1,1],['Стойбище исчезло','Разломленный кусок'],['The camp is gone','The broken piece']),
('iii-5',3590,3878,[1,3],['Место Лип-Липа','Свои и чужие руки'],['Lip-lip’s place','His people and the others']),
('iii-6',3879,4176,[2,2,2],['Другие щенки','Без рыбы','Встреча за скалой'],['Other puppies','No fish','The meeting beyond the rock']),
('iv-1',4182,4506,[1,1],['Первым в упряжке','Новый пароход'],['First in the team','Another steamer']),
('iv-2',4507,4798,[1,1,1],['Чёрная бутылка','Возвращение к хозяину','Цепь вместо палки'],['The black bottle','Back to the master','A chain instead of wood']),
('iv-3',4799,4975,[1,3,1],['За дверью — противник','Победа до утра','Низенький пёс'],['An opponent beyond the door','Victory until morning','The short dog']),
('iv-4',4976,5414,[3]*5,['Молчаливый преследователь','Первое падение','Всё меньше воздуха','Ствол между зубами','Сто пятьдесят долларов'],['The silent pursuer','The first fall','Less and less air','Steel between the teeth','A hundred and fifty dollars']),
('iv-5',5415,5657,[3,3],['Мясо на снегу','За угол хижины'],['Meat on the snow','Round the cabin corner']),
('iv-6',5658,6148,[3]*5,['Ничего не случилось','Голос и ладонь','Холодная ступенька','Голова под рукой','Лампа в снегу'],['Nothing happened','The voice and the hand','The cold step','His head beneath the arm','A lamp in the snow']),
('v-1',6154,6378,[3]*3,['Чемодан на полу','Обе двери заперты','Последний гудок'],['The suitcase on the floor','Both doors locked','The final whistle']),
('v-2',6379,6621,[3]*3,['Город исчез','Руки вокруг шеи','Тёплый приём'],['The city disappears','Arms around his neck','A warm welcome']),
('v-3',6622,6981,[3]*4,['Семья Скотта','Белые куры','Судья держит слово','По дороге в город'],['Scott’s family','The white hens','The judge keeps his word','On the way to town']),
('v-4',6982,7213,[3]*4,['Смех хозяина','Лошадь упала','Трудный звук','Хозяин едет один'],['The master’s laughter','The horse falls','The difficult sound','The master rides alone']),
('v-5',7214,7519,[3]*6,['Пятьдесят лет','Ступенька наверх','Когда зажёгся свет','Вагоны во сне','До конюшни','Тёплый язык'],['Fifty years','A step upstairs','When the light came on','Streetcars in dreams','To the stables','A warm tongue']),
]
body=[];scene=[]
for n,(key,a,z,levels,tr,te) in enumerate(spec):
 assert len(ru[n]['paragraphs'])==len(en[n]['paragraphs'])==len(levels)==len(tr)==len(te),(key,len(ru[n]['paragraphs']),len(levels))
 for j,(pr,pe,level,rt,et) in enumerate(zip(ru[n]['paragraphs'],en[n]['paragraphs'],levels,tr,te),1):
  locator=f'PG910 · {key.upper().replace("-", ".")} · primary.txt L{a}–{z}'
  # A bridge written at the previous chapter end may enter the next chapter.
  if key=='ii-3' and j==3:locator='PG910 · II.III–IV · primary.txt L1980–2129'
  if key=='ii-5' and j==3:locator='PG910 · II.V–III.I · primary.txt L2400–2633'
  if key=='ii-4' and j==5:locator='PG910 · II.IV–V · primary.txt L2330–2414'
  if key=='iv-3' and j==3:locator='PG910 · IV.III–IV · primary.txt L4799–4990'
  s={'id':f'{key}-p{j}','level':level,'claimType':'book','sources':[1],'evidenceLocator':locator,'narrative':True,'draftChapter':n+1,'draftParagraph':j,'copy':{l:{'section':d[n]['heading'],'title':t,'body':'<p>'+html.escape(p,quote=False)+'</p>'} for l,d,p,t in [('ru',ru,pr,rt),('en',en,pe,et)]}}
  body.append(s);scene.append({'id':s['id'],'level':level,'sourceChapter':key,'locator':locator,'draftChapter':n+1,'draftParagraph':j,'title':{'ru':rt,'en':et}})
cover={'id':'cover','level':1,'type':'cover','sources':[],'copy':{
'ru':{'section':'Джек Лондон','title':'Белый Клык','subtitle':'Сокращённый рассказ по роману · 1906','body':'<p>По замёрзшей реке люди везут длинный ящик. За ними идут голодные волки. Одна волчица подходит к огню слишком близко.</p><p>«Главное» и «Подробнее» ведут к появлению незнакомого противника и останавливаются до исхода боя. «Глубоко» продолжает историю до последней сцены — после вашего согласия.</p>','visualAlt':'Джек Лондон. Белый Клык.'},
'en':{'section':'Jack London','title':'White Fang','subtitle':'A condensed telling of the novel · 1906','body':'<p>On a frozen river two men haul a long box. Hungry wolves follow. One she-wolf comes too close to the fire.</p><p>Essential and Core reach the arrival of an unfamiliar opponent and stop before the fight is resolved. Deep continues to the last scene—after your consent.</p>','visualAlt':'Jack London. White Fang.'}}}
gate={'id':'deep-warning','level':3,'claimType':'synthesis','sources':[],'framing':True,'copy':{
'ru':{'section':'Полный маршрут','title':'Дальше — исход боя и развязка','body':'<p>Далее раскрываются исход схватки, поздние встречи и последняя сцена романа. Это продолжение полной истории. Вы уже подтвердили вход в «Глубоко» в этом открытом документе; понижение глубины или перезагрузка потребуют нового согласия.</p>'},
'en':{'section':'Complete route','title':'Ahead: the fight and the ending','body':'<p>The following scenes reveal the fight’s outcome, later encounters and the novel’s last scene. This continues the complete story. You have confirmed Deep in this open document; lowering depth or reloading requires fresh consent.</p>'}}}
final={'id':'final','level':1,'final':True,'claimType':'synthesis','sources':[],'framing':True,'copy':{
'ru':{'section':'Маршруты чтения','title':'На этой глубине чтение завершено','body':'<p>«Главное» и «Подробнее» заканчиваются появлением незнакомого противника. Продолжение и настоящий финал доступны в «Глубоко» после предупреждения. Если вы уже прочли полный маршрут, можно вернуться к началу.</p>'},
'en':{'section':'Reading routes','title':'This reading depth is complete','body':'<p>Essential and Core end with the unfamiliar opponent’s arrival. The continuation and actual ending are available in Deep after a warning. If you have read the complete route, you can return to the beginning.</p>'}}}
screens=[cover]
for s in body:
 if s['id']=='iv-4-p1':screens.append(gate)
 screens.append(s)
screens.append(final)
counts={m:sum(s['level']<=i for s in screens) for m,i in [('essential',1),('core',2),('deep',3)]}
d={'schemaVersion':2,'slug':'white-fang','author':{'ru':'Джек Лондон','en':'Jack London'},'title':{'ru':'Белый Клык','en':'White Fang'},'description':{'ru':'Связный сокращённый рассказ по роману Джека Лондона. Два коротких маршрута сохраняют развязку; полный маршрут требует согласия.','en':'A connected condensed telling of Jack London’s novel. Two shorter routes preserve the ending; the complete route requires consent.'},'defaultLanguage':'ru','defaultTheme':'dark','defaultMode':'essential','contentMode':'narrative','spoilerPolicy':'full-plot-in-deep','targetModes':counts,'modes':{'essential':{'label':{'ru':'Главное','en':'Essential'}},'core':{'label':{'ru':'Подробнее','en':'Core'}},'deep':{'label':{'ru':'Глубоко','en':'Deep'}}},'methodNote':{'ru':'Оригинальный сокращённый пересказ своими словами, не опубликованный русский перевод. Полностью прочитан английский текст Project Gutenberg №910, все пять частей и 25 глав. Представления и ощущения зверя передаются как повествование Лондона. Полный первоисточник по внешней ссылке раскрывает весь сюжет.','en':'An original condensed retelling, not a published Russian translation. The complete English Project Gutenberg text #910 was read, all five parts and 25 chapters. The animal’s perceptions are told as London’s narrative. The external full-text link reveals the entire plot.'},'sources':[{'id':1,'title':'Jack London — White Fang · Project Gutenberg #910','url':'https://www.gutenberg.org/ebooks/910','role':'book','note':{'ru':'Английский первоисточник: полное чтение всех пяти частей и 25 глав. Электронные диапазоны в карте относятся к проверенному локальному файлу, не к печатным страницам. Внешний полный текст содержит развязку.','en':'English primary witness: all five parts and 25 chapters read completely. Electronic ranges in the map refer to the verified local file, not print pages. The external complete text contains the ending.'}}],'media':{},'screens':screens}
(H/'story-data.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');(H/'scene-map.json').write_text(json.dumps(scene,ensure_ascii=False,indent=2)+'\n')
# Reading ranges are source bytes, including original CRLF endings; front matter does not count as literary reading.
b=S.read_bytes();ls=b.splitlines(keepends=True);ranges=[json.loads(x) for x in (H/'reading-ranges.jsonl').read_text().splitlines()];last=0
for r in ranges:
 assert r['startLine']==last+1;assert sha(b''.join(ls[r['startLine']-1:r['endLine']]))==r['rangeSha256'];last=r['endLine']
assert last==7519
coverage={'source':str(S),'sourceSha256':SHA,'sourceBytes':len(b),'workLines':[83,7519],'excludedFromWorkReading':{'frontMatter':[1,82],'licenseAndEndMatter':[7520,len(ls)]},'fullContinuousLiteraryReading':True,'parts':5,'chapters':25,'readBy':'implementation agent; root must independently review resulting complete RU/EN and critical primary passages','ranges':ranges,'chaptersRead':[{'chapter':key,'startLine':a,'endLine':z,'rangeSha256':sha(b''.join(ls[a-1:z])),'readComplete':True} for key,a,z,*_ in spec]}
(H/'source-coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
(H/'reading-ledger.md').write_text('# Primary reading ledger\n\nComplete direct reading of the supplied English witness: all five parts, all 25 chapters. No contents listing, download or old review counts as reading. No output range was truncated.\n\nSource SHA-256: `'+SHA+'`. Exact byte-range hashes retain original CRLF endings; line ranges are inclusive. Literary work is L83–7519. L1–82 was also displayed but is front matter; L7520 onward is excluded Gutenberg end/license matter.\n\n| Presented range | Bytes | SHA-256 |\n|---|---:|---|\n'+''.join(f"| L{r['startLine']}–{r['endLine']} | {r['bytes']} | `{r['rangeSha256']}` |\n" for r in ranges)+'\nMachine verification: source-coverage.json and read-primary.py. Presented ranges were directly read by this implementation agent; this is not root acceptance.\n')
print(json.dumps({'counts':counts,'narrativeParagraphs':len(body),'chapterParagraphs':[len(c['paragraphs']) for c in ru]}))

from pathlib import Path
import json,re,html,hashlib,shutil
P=Path(__file__).resolve().parent
SRC=Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-8-private/make-time-edition.json')
primary=json.loads(SRC.read_text())
def parse(lang):
 text=(P/f'draft-{lang}.md').read_text();parts=re.split(r'^## ',text,flags=re.M)[1:]
 return [(p.split('\n',1)[0],p.split('\n',1)[1].strip().split('\n\n')) for p in parts]
ru,en=parse('ru'),parse('en');assert len(ru)==len(en)==66
assert all(len(a[1])==len(b[1])==2 for a,b in zip(ru,en))
ids='two-streams wooden-railway lost-winter sprint-laboratory daily-loop middle-scale three-criteria time-and-revision record-repeat priorities small-tasks might-do two-burners personal-sprint calendar-chain reserve-window move-appointments honest-no revise-the-day morning-jz evening-jake stop-before-empty product-attraction restore-friction phone-tools logout-urgent-channel watch-and-distance morning-kryptonite social-cost chosen-news close-tabs-flight router-timer time-craters service-job email-loop reply-windows expectations-timezones send-only holiday-evening living-room begin-highlight music-timer simple-tools wandering-attention wholehearted battery-body cave-framework modest-movement walking-journey brief-workout prepared-food fasting-snacks chocolate-default caffeine-purpose coffee-window woods-meditation real-break voice-meals bedroom-sunset available-sleep caregiving evening-notes jakes-entry gratitude life-turns three-day-start'.split();assert len(ids)==66
levels=[1,2,2,3,1,1,1,1,2,3,3,2,3,3,1,2,3,2,3,2,2,1,2,1,2,1,2,1,3,2,3,2,2,3,2,1,1,3,2,3,1,3,2,1,3,1,3,2,1,3,2,2,3,2,3,2,1,2,1,3,1,1,3,2,1,1]
# Each tuple is extraction record, 1-based inclusive paragraph start and end.
refs=[[(5,6,24)],[(5,31,53)],[(7,7,24)],[(5,54,68)],[(6,1,33)],[(7,23,29),(6,7,8)],[(7,30,64),(53,4,4)],[(7,65,70)],[(9,1,12)],[(9,13,47)],[(9,48,57)],[(9,58,63)],[(9,64,81)],[(9,82,87)],[(11,1,11)],[(11,12,22)],[(11,23,32)],[(11,33,42)],[(11,43,52)],[(11,53,73)],[(11,74,87)],[(11,88,97)],[(12,12,42)],[(12,43,51)],[(14,1,28)],[(14,29,44)],[(14,45,62)],[(16,1,10)],[(16,10,16)],[(16,17,27),(20,9,10)],[(16,28,43),(53,18,18)],[(16,44,60)],[(16,61,75)],[(16,76,94)],[(18,1,5)],[(18,6,26)],[(18,21,26),(18,42,56)],[(18,27,35)],[(18,36,41),(20,1,20)],[(20,11,25)],[(22,1,23)],[(22,24,39)],[(22,40,53)],[(24,1,16)],[(24,17,30)],[(25,4,15),(6,13,16)],[(25,16,50)],[(27,1,22),(53,33,34)],[(27,23,45)],[(27,46,59)],[(29,1,11)],[(29,12,27)],[(29,28,36),(53,40,41),(11,70,70)],[(31,1,20),(31,29,39)],[(31,7,34)],[(33,1,30)],[(33,31,43)],[(35,1,17)],[(37,1,17)],[(37,18,31)],[(37,32,37)],[(38,1,24),(40,1,2)],[(40,12,23)],[(40,3,7)],[(41,1,18),(5,70,73)],[(42,1,10),(6,20,33)]]
assert len(levels)==len(refs)==len(ids)
def loc(rr):
 return [{'file':primary[i]['file'],'record':i,'paragraphStart':a,'paragraphEnd':b,'indexBase':1,'inclusive':True} for i,a,b in rr]
units=[]
for n,(r,e,id,level,rr) in enumerate(zip(ru,en,ids,levels,refs),1):
 units.append({'number':n,'id':id,'level':level,'ruTitle':r[0],'enTitle':e[0],'sourceRanges':loc(rr),'paragraphCount':2})
(P/'argument-map.json').write_text(json.dumps({'draftFirst':True,'units':units},ensure_ascii=False,indent=2)+'\n')
# Tactic assignments name an original explanatory unit; no copied tactic catalogue.
tmap={1:9,2:9,3:10,4:11,5:12,6:13,7:14,8:15,9:16,10:17,11:17,12:18,13:19,14:20,15:21,16:22,17:25,18:26,19:26,20:27,21:27,22:27,23:28,24:28,25:30,26:31,27:31,28:32,29:32,30:33,31:33,32:34,33:34,34:36,35:36,36:36,37:36,38:36,39:37,40:38,41:39,42:37,43:30,44:40,45:39,46:39,47:39,48:41,49:41,50:41,51:42,52:42,53:43,54:43,55:44,56:44,57:44,58:44,59:44,60:45,61:48,62:49,63:49,64:50,65:51,66:51,67:52,68:52,69:53,70:54,71:54,72:55,73:55,74:54,75:55,76:54,77:56,78:56,79:57,80:57,81:58,82:58,83:59,84:59,85:60,86:60,87:61}
# Identify successive tactic headings in actual record/paragraph order, not sorted filenames.
starts=[];expected=1
for i,r in enumerate(primary):
 for p,t in enumerate(r['paragraphs'],1):
  if re.match(r'^'+str(expected)+r'\.\s',t):starts.append((expected,i,p));expected+=1
assert expected==88,(expected,starts[-3:])
tactics=[]
for k,(n,i,a) in enumerate(starts):
 b=starts[k+1][2]-1 if k+1<len(starts) and starts[k+1][1]==i else len(primary[i]['paragraphs'])
 u=units[tmap[n]-1]
 status='compressed-and-combined' if sum(x==tmap[n] for x in tmap.values())>1 else 'retained-with-compression'
 omit='Repetitions, epigraphs and nonessential flourishes omitted; procedure/condition retained in original prose.'
 if n==64:omit='Exact twelve-movement sequence unavailable in text extraction; not reconstructed. JZ procedure and interval structure described; comparative efficacy claims not independently endorsed.'
 if n in [67,69,70,71,72,73,75,77,78,85,86]:omit+=' Broad medical/efficacy promises and numerical study results not reproduced as established guidance.'
 if n==21:omit+=' Harrison history omitted: wristwatch interruption mechanism is sufficient to the argument.'
 if n==51:omit+=' Album/song inventory omitted: distinct activity-specific cue mechanism retained.'
 if n==33:omit+=' Packers genealogy omitted; JZ actual social/stadium choices retained.'
 tactics.append({'tactic':n,'status':status,'sourceRange':loc([(i,a,b)])[0],'unit':u['id'],'screenIds':[u['id']],'firstDepth':['essential','core','deep'][u['level']-1],'retention':u['enTitle'],'omissionsAndReason':omit})
chapter_ranges=[('Opening and system',[5,6],range(1,6)),('Highlight',[7,9,11],range(6,23)),('Laser',[12,14,16,18,20,22,24],range(23,46)),('Energize',[25,27,29,31,33,35,37],range(46,62)),('Reflect',[38,40],range(62,65)),('Life pivot',[41],range(65,66)),('Quick start',[42],range(66,67))]
chapters=[]
for label,records,ns in chapter_ranges:
 chapters.append({'chapter':label,'readRanges':loc([(i,1,len(primary[i]['paragraphs'])) for i in records]),'units':[units[n-1]['id'] for n in ns],'coverage':'Continuous main-text reading; substantial original condensation, not complete reproduction.','omissions':'Epigraphs, repeated exhortations, most historical usage statistics and many subsidiary examples condensed; no entire main chapter omitted.'})
gaps=[{'location':'content06 pp2–5,32; content07 p3; content1.2 p60; content1.4 pp45–51; content2.8 pp12–13; content3.2 pp50–51; content4 p24; content09/content09.2 calendars','kind':'image-only material absent from paragraph extraction','scope':'No source images copied. Diagram geometry, Luke’s pictured utterance, exact reflection questionnaire scale, calendar times not printed in prose, and twelve-exercise list are not inferred. All retained procedures are supported by actual surrounding prose. No owned image path was identified in the supplied prior local records.'}]
coverage={'sourceOrder':'JSON record order, verified by continuous reading and tactic sequence 1–87; never filename lexical sort.','chapters':chapters,'tactics':tactics,'wholeTacticsOmitted':[],'imageGaps':gaps,'backMatter':{'readRecords':[2,3,43,45,47,48,49,50,51,53,54],'omitted':'Dedication, publishing credits, acknowledgments, reading-list catalogue, review requests and most humorous notes are not manuscript chapters. Useful qualifications from notes 4,18,33,40,41 are preserved. Sample-day captions inform author routines; image calendars remain uninspected.'},'englishBoundary':'Original translation of this RU account. No published-English full-edition reading or collation.'}
(P/'coverage-map.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
md=['# Chapter, tactic, and omission map','',coverage['sourceOrder'],'','All 87 tactic narratives were read. All have meaningful retained substance, often combined; no claim of full reproduction.','']
for c in chapters:md += ['## '+c['chapter'],'',c['coverage']+' '+c['omissions'],'', 'Units: '+', '.join(c['units']), '']
md+=['## Every tactic','','| Tactic | Actual source (1-based inclusive) | Unit / first depth | Treatment and omissions |','|---:|---|---|---|']
for t in tactics:
 r=t['sourceRange'];md.append(f"| {t['tactic']} | {r['file']} ¶{r['paragraphStart']}–{r['paragraphEnd']} | {t['unit']} / {t['firstDepth']} | {t['status']}; {t['omissionsAndReason']} |")
md+=['','## Images and secondary material','',gaps[0]['location'], '',gaps[0]['scope'],'',coverage['backMatter']['omitted'],'',coverage['englishBoundary']]
(P/'coverage-map.md').write_text('\n'.join(md)+'\n')
method={'ru':'Самостоятельное сокращённое изложение по полному приватному RU-извлечению «Найди время», перевод А. Капанадзе, ISBN 9785961420517 (оригинал 2018). Основной текст, все 87 тактик и примечания прочитаны по порядку. EN переводит это изложение; с опубликованным английским текстом сверки нет. Изображения анкет, календарей и части процедур в извлечении отсутствуют; их детали не восстановлены по догадке. Авторские эксперименты и утверждения о здоровье не являются здесь независимо проверенными лечебными рекомендациями. Это черновик для личной редакторской проверки.','en':'An original condensed account based on the complete private RU extraction of Make Time, translated by A. Kapanadze, ISBN 9785961420517 (original 2018). Main text, all 87 tactics and notes were read in order. EN translates this account; no published-English collation was performed. Questionnaire, calendar and some procedure images are absent from the extraction; their details are not guessed. Author experiments and health assertions are not independently validated clinical guidance here. A draft awaiting personal editorial review.'}
sections=[('Введение','Opening'),('Главное','Highlight'),('Лазер','Laser'),('Энергия','Energize'),('Осмысление','Reflect'),('Продолжение','Next')]
def section(n):return sections[0 if n<=5 else 1 if n<=22 else 2 if n<=45 else 3 if n<=61 else 4 if n<=64 else 5]
screens=[{'id':'cover','level':1,'type':'cover','sources':[],'copy':{'ru':{'section':'Начало','title':'Найди время','subtitle':'Джейк Кнапп и Джон Зерацки','body':'<p>Главное на день, внимание для него, энергия и наблюдение за тем, что получилось.</p>','visualAlt':'Текстовая обложка'},'en':{'section':'Start','title':'Make Time','subtitle':'Jake Knapp and John Zeratsky','body':'<p>A daily Highlight, attention for it, energy, and observation of what happened.</p>','visualAlt':'Typographic cover'}}}]
for n,(r,e,u) in enumerate(zip(ru,en,units),1):
 sec=section(n)
 screens.append({'id':u['id'],'level':u['level'],'claimType':'book','sources':[1],'primaryRanges':u['sourceRanges'],'copy':{l:{'section':sec[k],'title':v[0],'body':''.join('<p>'+html.escape(s,quote=False)+'</p>' for s in v[1])} for k,(l,v) in enumerate([('ru',r),('en',e)])}})
screens.append({'id':'final','level':1,'final':True,'claimType':'book','sources':[1],'primaryRanges':loc([(42,1,10)]),'copy':{'ru':{'section':'Конец','title':'После третьего вечера','body':'<p>Три дня дают первые наблюдения. Решение о продолжении опирается на них: что получило время, что помогло вниманию, что изменило энергию и какой следующий опыт теперь имеет смысл.</p>'},'en':{'section':'End','title':'After the third evening','body':'<p>Three days provide initial observations. They inform what comes next: what received time, what helped attention, what changed energy, and which experiment now makes sense.</p>'}}})
data={'schemaVersion':2,'slug':'make-time','title':{'ru':'Найди время','en':'Make Time'},'description':{'ru':'Четыре шага Кнаппа и Зерацки, реальные случаи и процедуры 87 тактик в содержательном сокращении.','en':'Knapp and Zeratsky’s four steps, actual cases, and the substance of 87 tactics in a developed condensation.'},'defaultLanguage':'ru','defaultTheme':'dark','defaultMode':'essential','contentMode':'explanatory','spoilerPolicy':'not-applicable','targetModes':{m:sum(s['level']<=l for s in screens) for m,l in [('essential',1),('core',2),('deep',3)]},'methodNote':method,'sources':[{'id':1,'title':'Jake Knapp and John Zeratsky — Make Time / Найди время, ISBN 9785961420517','url':'https://www.penguinrandomhouse.com/books/564727/make-time-by-jake-knapp-and-john-zeratsky/','role':'book','note':{'ru':'Первичный источник — предоставленное владельцем приватное RU-извлечение. Ссылка библиографическая, страница не использовалась как полный текст. Основной текст и 87 тактик прочитаны непрерывно; изображения отсутствуют. Точные локаторы и карта сокращений — в рабочих материалах.','en':'Primary evidence is the owner-supplied private RU extraction. Link is bibliographic; the page was not used as full text. Main text and 87 tactics were read continuously; images are absent. Exact locators and omissions are in the working records.'}}],'media':{},'screens':screens}
(P/'story-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
for m,l in [('essential',1),('core',2),('deep',3)]:
 for lang in ['ru','en']:
  lines=[]
  for s in screens:
   if s['level']<=l:
    c=s['copy'][lang];lines+=['## '+c['title'],'',*([c['subtitle'],''] if c.get('subtitle') else []),html.unescape(c['body'].replace('<p>','').replace('</p>','\n\n')).strip(),'']
  (P/f'{m}.{lang}.md').write_text('\n'.join(lines))
# Finalize source ledger without including private book text.
l=json.loads((P/'private-source-reading-ledger.json').read_text());l['status']='direct continuous reading completed; truncated fragments re-emitted and read';l['sourceOrderRecords']=[{'record':i,'file':r['file'],'paragraphs':len(r['paragraphs']),'words':r['words'],'recordSha256':hashlib.sha256(json.dumps(r,ensure_ascii=False).encode()).hexdigest(),'textRead':bool(r['paragraphs']),'imageInspected':False} for i,r in enumerate(primary)];l['imageGaps']=gaps;l['englishEditionRead']=False;l['primaryWords']=sum(r['words'] for r in primary);l['mainTextAnd87TacticsRead']=True;l['selfEditorialAcceptance']=False
(P/'private-source-reading-ledger.json').write_text(json.dumps(l,ensure_ascii=False,indent=2)+'\n');(P/'private-source-reading-ledger.json').chmod(0o600)
print('Prepared',len(units),'units;',data['targetModes'])

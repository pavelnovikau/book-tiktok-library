from pathlib import Path
import re,json,html,hashlib
P=Path(__file__).resolve().parent

def parse(lang):
 s=(P/f'draft.{lang}.md').read_text(); part=''; out=[]
 for m in re.finditer(r'^(## |### )([^\n]+)\n([\s\S]*?)(?=^## |^### |\Z)',s,re.M):
  if m[1]=='## ':part=m[2];continue
  paras=re.split(r'\n\s*\n',m[3].strip());assert all(paras)
  out.append(dict(part=part,title=m[2],paras=paras))
 return out
ru,en=parse('ru'),parse('en');assert len(ru)==len(en)==58
# Levels were assigned only after the connected RU and EN manuscripts existed.
# A unit's paragraphs stay in one depth; segmentation never removes a caveat
# from a retained unit. Deep is the exact full manuscript, in original order.
config=[
('the-question',1,'Introduction',[0]),('two-systems',1,'1',[2,3,5]),('attention-and-effort',3,'2',[5]),('the-gorilla',3,'1',[3]),('bat-and-ball',1,'3',[7]),('a-complete-looking-story',2,'7',[20]),('the-easier-question',1,'9',[1,23]),
('small-samples',1,'10',[25]),('law-of-small-numbers',3,'10',[0,25]),('the-wheel',1,'11',[28]),('two-kinds-of-anchors',3,'11',[28,29]),('easy-to-recall',1,'Introduction;12',[0,32]),('six-or-twelve',2,'12',[32]),('base-rates',1,'Introduction;14',[0,38]),('bayesian-update',3,'14',[38]),('linda',2,'15',[38]),('linda-and-language',3,'15',[38,39]),('flight-instructors',1,'17',[42]),('coins-and-golf',3,'17',[42]),
('after-the-result',2,'19',[47]),('the-record-of-skill',2,'20',[50]),('formulas-and-judgment',2,'21',[52]),('rules-and-exceptions',3,'21',[52]),('interview-in-parts',2,'21',[54]),('hiring-procedure',2,'21',[55]),('kleins-objection',2,'22',[1,55,56]),('when-intuition-learns',1,'22',[57,58]),('learning-from-feedback',3,'22',[58]),('curriculum-project',2,'23',[59,60]),('outside-view',1,'23',[60,61]),('premortem',2,'24',[65]),
('money-and-utility',2,'25',[66]),('reference-point',1,'25;26',[66,67]),('two-gifts',3,'26',[67]),('diminishing-sensitivity',2,'26',[67,68]),('losses-and-gains',1,'26',[68]),('a-mug-of-ones-own',2,'27',[71]),('goods-for-trade',2,'27',[72]),('probability-weights',1,'29',[76]),('fourfold-pattern',2,'29',[78]),('lawsuit-negotiations',3,'29',[78]),('description-and-experience',3,'30',[82]),('sam-and-tosses',2,'31',[84]),('risk-policy',2,'31',[84,85]),('limits-of-prospect-theory',2,'26',[69]),('same-outcomes-new-frame',1,'34',[92]),('behind-the-frame',3,'34',[92]),
('two-selves',1,'35',[94]),('pain-and-memory',2,'35',[94]),('the-cold-hand',2,'35',[95]),('time-and-stories',3,'35',[95]),('day-reconstruction',3,'37',[98]),('two-wellbeing-questions',2,'37',[98]),('focusing-illusion',2,'38',[100]),('both-selves',1,'Conclusion',[101]),('econs-and-humans',3,'Conclusion',[102]),('limits-of-correction',2,'Conclusion',[103]),('final',1,'Conclusion',[2,101,102,103])]
assert len(config)==58
pub='https://us.macmillan.com/books/9780374533557/thinkingfastandslow/'
sources=[
 dict(id=1,title='Daniel Kahneman — Thinking, Fast and Slow (2011); owned AST 2014 Russian EPUB',url=pub,role='book',note=dict(ru='Основной текст — полный пользовательский EPUB: Школа перевода Баканова, 2013; AST, 2014. Прочитаны опорные разделы для всех удержанных механизмов и опытов, карта пяти частей и заключение. Это выборочное чтение по карте, не сплошное чтение тома. Ссылка идентифицирует оригинал, а не открывает частный EPUB.',en='Primary text: the user’s full Russian EPUB, Bakanov translation school 2013, AST 2014. Complete supporting sections for all retained mechanisms and experiments, the five-part map and conclusion were read. This is mapped selective reading, not a continuous reading of the volume. The link identifies the original rather than opening the private EPUB.')),
 dict(id=2,title='Macmillan — original work and official English introduction',url=pub,role='publisher',note=dict(ru='Открыты страница и доступная часть официального введения. Роль: идентификация оригинала и вводный контекст. Поздние главы подтверждены частным русским текстом, не этой ссылкой. EN — перевод данного сокращения, не колляция с полным английским томом.',en='The page and available official-introduction excerpt were consulted for identification and introductory context. Later chapters are supported by the private Russian text, not this URL. EN translates this condensation; it is not a collation against the complete English volume.')),
 dict(id=3,title='Doyen et al. (2012) — Behavioral Priming',url='https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0029081',role='reference',note=dict(ru='В прочитанной аннотации репликация эффекта замедленной ходьбы зависит от процедуры и ожиданий экспериментатора. Этот сюжет главы 4 не пересказан. Это ограниченная оговорка, не опровержение всех видов прайминга и не проверка якорей.',en='The abstract reports a walking-speed replication sensitive to procedure and experimenter expectations. That Chapter 4 episode is omitted. This limited qualification neither rejects all priming nor revalidates anchoring.')),
 dict(id=4,title='Hagger et al. (2016) — Multilab Preregistered Replication of Ego Depletion',url='https://journals.sagepub.com/doi/10.1177/1745691616652873',role='reference',note=dict(ru='Прочитаны аннотация и вводное описание протокола: 23 лаборатории, малый эффект с интервалом, включающим ноль. Истощение самоконтроля не пересказывается как установленный механизм. Это не исчерпывающий обзор исследований.',en='The abstract and protocol introduction report 23 labs and a small effect with an interval including zero. Ego depletion is not presented as an established mechanism here. This is not an exhaustive research review.')),
 dict(id=5,title='Killingsworth, Kahneman & Mellers (2023) — Income and emotional well-being',url='https://pubmed.ncbi.nlm.nih.gov/36857342/',role='reference',note=dict(ru='Прочитана аннотация совместного переанализа: связь дохода с чувствами различается между группами. Поэтому порог из главы 37 не перенесён в пилот как всеобщая современная норма. Аргумент книги об оценке жизни и ощущениях сохранён.',en='The joint reanalysis abstract reports different income–feeling relationships across groups. The Chapter 37 threshold is therefore not carried over as a universal contemporary rule. The book’s distinction between life evaluation and feelings is retained.'))]
data=dict(schemaVersion=2,slug='thinking-fast-and-slow',title=dict(ru='Думай медленно… решай быстро',en='Thinking, Fast and Slow'),description=dict(ru='Связное расширенное изложение аргумента Канемана: от внимания и интуиции к вероятности, экспертизе, выбору и двум «я».',en='An expanded connected account of Kahneman’s argument: attention and intuition, probability, expertise, choice and the two selves.'),defaultLanguage='ru',defaultTheme='dark',defaultMode='essential',contentMode='explanatory',methodNote=dict(ru='Изложение своими словами по опорным разделам полного пользовательского русского EPUB (AST 2014, перевод 2013; оригинал 2011). Удержанные случаи сверены с текстом всех пяти частей и заключения; сплошное чтение всего тома и сверка с полным EN не заявляются. Это аргумент книги, а не подтверждение всех исторических опытов сегодняшней наукой. Границы и отдельные более поздние исследования указаны в источниках.',en='An original-word account based on supporting sections of the user’s full Russian EPUB (AST 2014, translation 2013; original 2011). Retained cases were checked across all five parts and the conclusion; continuous whole-volume reading and full-English collation are not claimed. This conveys the book’s argument rather than certifying every historical experiment today. Sources state boundaries and selected later research.'),sources=sources,media={},screens=[])
cover=dict(id='cover',type='cover',level=1,sources=[],copy={})
for lang in ['ru','en']:
 cover['copy'][lang]=dict(section='Даниэль Канеман · 2011' if lang=='ru' else 'Daniel Kahneman · 2011',title=data['title'][lang],subtitle='От уверенного впечатления к проверке основания' if lang=='ru' else 'From a confident impression to checking its grounds',body='<p>Как возникают суждения, почему меняется выбор и чем прожитое отличается от запомнившегося.</p>' if lang=='ru' else '<p>How judgments arise, why choices change, and how lived experience differs from remembered experience.</p>')
data['screens'].append(cover);coverage=[]
for n,(a,b,(uid,level,chapter,files)) in enumerate(zip(ru,en,config),1):
 assert len(a['paras'])==len(b['paras']),n
 groups=[];cur=[]
 for j,para in enumerate(a['paras']):
  # Keep full explanatory paragraphs, shared across languages. No sentence
  # chopping, no new prose inserted to meet a screen or length target.
  if cur and (sum(len(a['paras'][k].split()) for k in cur+[j])>135 or sum(len(b['paras'][k].split()) for k in cur+[j])>160):groups.append(cur);cur=[]
  cur.append(j)
 if cur:groups.append(cur)
 # The shared closing unit is one complete ending at every depth.
 if uid=='final':groups=[list(range(len(a['paras'])))]
 ids=[]
 for gidx,g in enumerate(groups):
  sid=uid if gidx==0 else uid+'-continued';ids.append(sid)
  screen=dict(id=sid,level=level,claimType='book',sources=[1],copy={})
  for lang,obj in [('ru',a),('en',b)]:
   title=obj['title'] if gidx==0 else obj['title']+(' · продолжение' if lang=='ru' else ' · continued')
   screen['copy'][lang]=dict(section=obj['part'],title=title,body=''.join('<p>'+html.escape(obj['paras'][k],quote=False)+'</p>' for k in g))
  if uid=='final':screen['final']=True
  data['screens'].append(screen)
 coverage.append(dict(unit=n,id=uid,level=level,chapter=chapter,primaryFiles=[f'content{x}.html' for x in files],screenIds=ids,ruTitle=a['title'],enTitle=b['title'],paragraphs=len(a['paras'])))
data['targetModes']={m:sum(s['level']<=i for s in data['screens']) for m,i in [('essential',1),('core',2),('deep',3)]}
(P/'story-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(P/'coverage-map.json').write_text(json.dumps(dict(slug=data['slug'],status='implementation-map-not-independent-approval',units=coverage),ensure_ascii=False,indent=2)+'\n')
for m,l in [('essential',1),('core',2),('deep',3)]:
 for lang in ['ru','en']:
  out=[f'# {data["title"][lang]} — {m.title()}\n']
  for s in data['screens']:
   if s['level']>l:continue
   c=s['copy'][lang];out.append(f'\n## {c["title"]}\n\n'+html.unescape(re.sub('</p>','\n\n',re.sub('<p>','',c['body']))).strip()+'\n')
  (P/f'{m}.{lang}.md').write_text(''.join(out))
print(json.dumps(dict(targetModes=data['targetModes'],units=len(coverage),paragraphs=sum(x['paragraphs'] for x in coverage)),ensure_ascii=False))

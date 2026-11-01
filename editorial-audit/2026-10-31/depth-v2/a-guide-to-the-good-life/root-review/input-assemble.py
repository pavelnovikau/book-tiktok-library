"""Book-local segmentation. The two connected manuscripts precede this data build."""
from pathlib import Path
import json,re,html,hashlib,datetime
HERE=Path(__file__).resolve().parent
PRIMARY=Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-10-private/a-guide-to-the-good-life-source')
SLUG='a-guide-to-the-good-life'
# These are semantic route choices; screen totals are derived below.
ROWS='''whole-life|1|0
default-philosophy|2|0
school-of-living|2|1
zenos-shipwreck|3|2
virtue-and-tranquility|1|2
four-witnesses|2|3
editors-objection|3|2
renewing-desire|1|4
imagined-loss|1|4
two-fathers|2|4
picnic-objection|1|4
poverty-and-resilience|3|4
cup-and-last-times|3|4
three-domains|1|5
impulse-and-action|1|5
playing-the-match|1|5
manuscript-and-rejection|2|5
past-present-future|1|6
sick-child|2|6
contentment-and-activity|2|6
practicing-poverty|1|7
three-benefits|2|7
pleasure-and-refusal|2|7
evening-review|1|8
signs-of-progress|2|8
why-not-withdraw|1|9
marcus-and-duty|3|9
duty-and-friendship|2|10
annoyance-and-faults|2|10
sex-and-marriage|3|10
force-of-insults|1|11
humor-and-silence|2|11
correcting-conduct|2|11
political-extension|3|11
involuntary-grief|1|12
rational-consolation|2|12
sympathy-without-grief|3|12
anger-as-helper|1|13
annoyance-and-anger|2|13
after-an-outburst|2|13
price-of-invitation|1|14
failure-with-an-audience|3|14
luxury-and-delight|1|15
natural-and-unlimited|2|15
unsought-wealth|2|15
what-exile-leaves|2|16
agrippinus-lunch|3|16
terms-of-age|2|17
age-and-appetite|3|17
fear-of-misliving|2|18
difficult-exception|3|18
begin-unobtrusively|2|19
decline-and-continuity|3|20
emotion-and-counseling|3|20
politics-and-responsibility|3|20
duty-and-desire|2|20
evolution-and-joy|1|21
repurposing-reason|2|21
remedy-and-explanation|3|21
medication-objection|3|21
reconstructed-stoicism|2|21
who-might-choose|1|21
sequence-of-practice|1|22
insult-and-waiting|3|22
chosen-discomfort|2|22
banjo-recital|3|22
opponent-in-the-boat|2|22
fewer-consumer-desires|3|22
temporary-sight-loss|3|22
mother-and-water|2|22
report-of-practice|1|22
reading-program|3|23
final-doubt|1|22'''
rows=[(r.split('|')[0],int(r.split('|')[1]),int(r.split('|')[2])) for r in ROWS.splitlines()]
CHFILE={0:8,1:10,2:11,3:12,4:14,5:15,6:16,7:17,8:18,9:20,10:21,11:22,12:23,13:24,14:25,15:26,16:27,17:28,18:29,19:30,20:32,21:33,22:34,23:35}
def dump(name,d): (HERE/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def words(s):return len(re.findall(r"[^\W_]+(?:[’'–—-][^\W_]+)*",s))
def parse(lang):
 out=[];sec=''
 for b in (HERE/f'draft.{lang}.md').read_text().strip().split('\n\n'):
  if b.startswith('### '):out.append(dict(title=b[4:],section=sec,paragraphs=[]))
  elif b.startswith('## '):sec=b[3:]
  elif not b.startswith('#'):out[-1]['paragraphs'].append(b)
 return out
ru,en=parse('ru'),parse('en');assert len(ru)==len(en)==len(rows)
cover={"id":"cover","type":"cover","level":1,"sources":[],"copy":{
 "ru":{"section":"Уильям Ирвин","title":"Радость жизни","subtitle":"Философия стоицизма для XXI века","body":"<p>Чего хотеть от целой жизни — и как не потратить её на бесконечное исполнение желаний? Ирвин объясняет стоические практики, проверяет их в отношениях, обязанностях и потерях, затем испытывает на собственной жизни.</p>","visualAlt":"Типографическая обложка книги Уильяма Ирвина"},
 "en":{"section":"William B. Irvine","title":"A Guide to the Good Life","subtitle":"The Ancient Art of Stoic Joy","body":"<p>What should we want from a whole life, and how can we avoid spending it endlessly fulfilling desires? Irvine explains Stoic practices, examines them through relationships, obligations and loss, then tests them in his own life.</p>","visualAlt":"Typographic cover for William B. Irvine's book"}}}
screens=[cover];unitmap=[];para_pairs=0
for n,((id,level,ch),r,e) in enumerate(zip(rows,ru,en),1):
 assert len(r['paragraphs'])==len(e['paragraphs']),id
 para_pairs+=len(r['paragraphs']);groups=[];group=[]
 for i in range(len(r['paragraphs'])):
  nextgroup=group+[i]
  if group and (sum(words(r['paragraphs'][j]) for j in nextgroup)>125 or sum(words(e['paragraphs'][j]) for j in nextgroup)>155):
   groups.append(group);group=[]
  group.append(i)
 if group:groups.append(group)
 # Final doubt is a single closing argument. It remains vertically scrollable.
 if id=='final-doubt':groups=[list(range(len(r['paragraphs'])))]
 ids=[]
 for gi,g in enumerate(groups):
  sid=id if gi==0 else id+'-continued'+('' if gi==1 else '-'+str(gi+1));ids.append(sid)
  s=dict(id=sid,level=level,claimType='book',sources=[2] if id=='editors-objection' else [1],copy={})
  for lang,u in [('ru',r),('en',e)]:
   suffix='' if gi==0 else (' · продолжение' if lang=='ru' else ' · continued')+(' '+str(gi+1) if gi>1 else '')
   s['copy'][lang]=dict(section=u['section'],title=u['title']+suffix,body=''.join('<p>'+html.escape(u['paragraphs'][j],quote=False)+'</p>' for j in g))
  s['draftUnit']=n;s['draftParagraphs']=[j+1 for j in g]
  if id=='final-doubt':s['final']=True
  screens.append(s)
 f=next(PRIMARY.glob(f'{CHFILE[ch]:03d}-*.txt'));text=f.read_text()
 loc=dict(file=f.name,characterRange=[0,len(text)],rangeConvention='Unicode, 0-based half-open; complete chapter read')
 if id=='editors-objection':loc=dict(privateEdition='Радость жизни.epub',file='OEBPS/pre.xhtml',scope='Complete scientific editor preface; separate voice')
 if id=='after-an-outburst':loc['additionalFile']='034-part0033.txt (Irvine corrects Seneca on pleasure in anger)'
 unitmap.append(dict(unit=n,id=id,level=level,chapter='Introduction' if ch==0 else 'Reading program' if ch==23 else ch,title={"ru":r['title'],"en":e['title']},paragraphPairs=len(r['paragraphs']),screenIds=ids,primary=loc))
counts={name:sum(s['level']<=level for s in screens) for name,level in [('essential',1),('core',2),('deep',3)]}
data=dict(schemaVersion=2,slug=SLUG,title=dict(ru='Радость жизни',en='A Guide to the Good Life'),
 description=dict(ru='Развёрнутое изложение практического стоицизма Уильяма Ирвина: желание, контроль, отношения, утраты, возражения и личная проверка.',en="An extended account of William B. Irvine's practical Stoicism: desire, control, relationships, loss, objections and his personal trial."),
 defaultLanguage='ru',defaultTheme='dark',defaultMode='essential',contentMode='explanatory',targetModes=counts,
 methodNote=dict(ru='Самостоятельное сокращённое изложение, не перевод книги. Введение, все 22 главы и программа чтения английского OUP-издания (©2009; ISBN 9780195374612) прочитаны полностью и по порядку. Из русского издания МИФ2021 прочитаны выходные сведения и предисловие научного редактора; полного сличения перевода нет. Сокращены биографии, повторные иллюстрации и детали библиографии. Древние позиции, реконструкция Ирвина и возражение редактора различены. Медицинская полемика передана как аргумент книги своего времени, без проверки современной эффективности лечения. Полная карта и точные диапазоны чтения находятся в сопроводительном пакете.',
 en='An original condensed exposition, not a reproduction of the book. The introduction, all 22 chapters and reading program of the English OUP edition (©2009; ISBN 9780195374612) were read completely in order. Only edition information and the scientific editor’s preface were read in the Russian MIF2021 edition; no full translation collation is claimed. Biographies, repeated illustrations and bibliographic detail are shortened. Ancient positions, Irvine’s reconstruction and the editor’s objection remain distinct. Medical polemics are reported as the historical book’s arguments, without a current treatment-efficacy review. The companion package contains the full map and exact reading ranges.'),
 sources=[dict(id=1,title='William B. Irvine — A Guide to the Good Life (OUP, ISBN 9780195374612)',url='https://academic.oup.com/book/50088',role='book',note=dict(ru='Полный частный английский текст: непрерывно прочитаны введение, главы 1–22 и программа чтения. Ссылка идентифицирует издание; материалом служил принадлежащий пользователю EPUB. Отдельные примечания проверены; все примечания, библиография и указатель не заявлены как полностью прочитанные.',en='Complete private English text: continuous reading of the introduction, chapters 1–22 and reading program. The link identifies the edition; evidence came from the user-owned EPUB. Selected notes were checked; complete reading of all notes, bibliography and index is not claimed.')),
 dict(id=2,title='Уильям Ирвин — Радость жизни (МИФ2021): предисловие Станислава Нарановича',url='https://www.mann-ivanov-ferber.ru/catalog/product/radost-zhizni/',role='reference',note=dict(ru='В частном EPUB прочитаны info.xhtml и pre.xhtml полностью. Используется только отдельное возражение научного редактора о добродетели и спокойствии. Перевод Василия Горохова не сличался полностью; русское изложение написано заново по английскому источнику.',en='Private EPUB info.xhtml and pre.xhtml were read completely. Used only for the scientific editor’s separate objection concerning virtue and tranquility. Vasily Gorokhov’s translation was not fully collated; the Russian exposition was written anew from the English witness.'))],media={},screens=screens)
dump('story-data.json',data);dump('coverage-map.json',dict(units=unitmap,counts=counts,paragraphPairs=para_pairs,rootPersonalAcceptance=False,publicationAllowed=False))
for mode,level in [('essential',1),('core',2),('deep',3)]:
 for lang,us in [('ru',ru),('en',en)]:
  parts=['# '+data['title'][lang]+' — '+mode];section=''
  for meta,u in zip(unitmap,us):
   if meta['level']>level:continue
   if section!=u['section']:section=u['section'];parts+=['## '+section]
   parts+=['### '+u['title']]+u['paragraphs']
  (HERE/f'route-{mode}.{lang}.md').write_text('\n\n'.join(parts)+'\n')
print(json.dumps(dict(counts=counts,units=len(rows),paragraphPairs=para_pairs,ruBodyWords=sum(words(p) for u in ru for p in u['paragraphs']),enBodyWords=sum(words(p) for u in en for p in u['paragraphs'])),ensure_ascii=False))

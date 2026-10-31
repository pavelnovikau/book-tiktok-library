"""Segment the already-written original manuscript; never writes outside this collector."""
import html
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manuscript = (root / 'narrative-draft-pass2.md').read_text()
ru, en = manuscript.split('## RU\n\n', 1)[1].split('\n\n## EN\n\n', 1)
paragraphs = {lang: text.strip().split('\n\n') for lang, text in [('ru', ru), ('en', en)]}

# Metadata is applied after manuscript drafting. No target quota or filler.
beats = [
 ('bookshop',1,'Лавка Кореандра','Coreander’s shop',[1,2]),
 ('three-initials',1,'Три буквы','Three initials',[1]),
 ('school-attic',1,'Книга без конца','A book without an end',[1,2]),
 ('fantastica-in-danger',1,'Ничто','The Nothing',[2,12]),
 ('artax-and-morla',1,'Болота Печали','The Swamps of Sadness',[2,9]),
 ('ygramuls-secret',1,'Тайна Играмуль','Ygramul’s secret',[3,9]),
 ('mirror-gate',1,'Мальчик в зеркале','The boy in the mirror',[3,11]),
 ('oracle-and-winds',1,'Где найти человека?','Where is a human child?',[3,4]),
 ('gmork',1,'Скованный охотник','The chained hunter',[4,11]),
 ('return-to-tower',1,'Возвращение к Императрице','Back to the Empress',[4,9]),
 ('the-unseen-reader',1,'Невидимый спутник','The unseen companion',[4,8]),
 ('wandering-mountain',1,'Рассказ начинается снова','The story begins again',[4,9,10]),
 ('a-grain',1,'Одно зёрнышко','A single grain',[5,9]),
 ('forest-and-lion',1,'Ночь леса, утро льва','The forest’s night, the lion’s morning',[5,11]),
 ('sikanda',2,'Подарок Граограмана','Grograman’s gift',[5,9]),
 ('amarganth',1,'Спаситель найден','The saviour is found',[5]),
 ('living-stories',2,'Рассказы становятся явью','Stories become real',[5,10]),
 ('the-price',1,'Чего не помнит Бастиан','What Bastian cannot remember',[5,8,10]),
 ('acharis',3,'Смех вместо плача','Laughter instead of tears',[5,9]),
 ('returning-roads',1,'Дороги по кругу','Roads in circles',[6,9]),
 ('seeing-hand',1,'Колдунья в свите','The sorceress joins them',[6,9]),
 ('xayides-counsel',3,'Пояс невидимости','The belt of invisibility',[6,9]),
 ('banishment',3,'Изгнание друзей','Friends banished',[6,9]),
 ('the-battle',3,'Перед троном','Before the throne',[6,9,11]),
 ('old-emperors',3,'Город Старых Императоров','The City of Old Emperors',[7,10,11]),
 ('sea-of-mist',3,'Один из многих','One among many',[7,9]),
 ('house-of-change',3,'Дом Айуолы','Eyola’s house',[7,8,11]),
 ('picture-mine',3,'Шахта Картин','The Picture Mine',[7,9,11]),
 ('broken-picture',3,'Хрупкий проводник','A fragile guide',[7,9]),
 ('within-auryn',3,'У источника','At the fountain',[7,9]),
 ('unfinished-stories',3,'За Бастиана отвечает друг','A friend answers for Bastian',[7,9,11]),
 ('home',3,'На школьном чердаке','In the school attic',[7,8,11]),
 ('bookshop-again',3,'Снова в лавке','Back in the bookshop',[7,10,12]),
]
assert len(paragraphs['ru']) == len(paragraphs['en']) == len(beats), {k:len(v) for k,v in paragraphs.items()}

source_specs = [
 (1,'Loqueleo Colombia — La historia interminable, publisher sample','https://www.loqueleo.com/co/uploads/2019/07/9789585939301.pdf','book',
  'Прочитано только испанское начало, печатные с. 7–15; перевод Мигеля Саэнса, ISBN 9789585939301. Весь роман не получен. Это не источник официального русского или английского перевода.',
  'Only the Spanish opening, printed pp. 7–15, was read; Miguel Sáenz translation, ISBN 9789585939301. The full novel was not obtained. This does not supply an official Russian or English translation.'),
 (2,'SuperSummary — Prologue–Chapter 3','https://www.supersummary.com/the-neverending-story/prologue-chapter-3-summary/','reference',
  'Прочитаны поэпизодные главы профессионального guide, не полный текст романа. Guide ссылается на перевод Ральфа Манхайма, Penguin, 1984. События отделены от трактовок guide.',
  'The professional guide’s event accounts were read, not the full novel. The guide references Ralph Manheim’s translation, Penguin, 1984. Its events are distinguished from its interpretations.'),
 (3,'SuperSummary — Chapters 4–7','https://www.supersummary.com/the-neverending-story/chapters-4-7-summary/','reference',
  'Поэпизодный вторичный рассказ. Рассмотрены главы и цитируемые отрывки; философские оценки и неточные пояснения guide в рассказ не переносились.',
  'A secondary chapter-event account. Chapters and quoted excerpts were consulted; the guide’s philosophical judgments and imprecise glosses were not adopted.'),
 (4,'SuperSummary — Chapters 8–12','https://www.supersummary.com/the-neverending-story/chapters-8-12-summary/','reference',
  'Проверены последовательность событий и рамка чтения; это вторичный guide, а не прочитанные полные главы. Короткие цитируемые места сверены в доступной критике.',
  'The event sequence and reading frame were checked; this is a secondary guide, not full chapters read. Short quoted passages were cross-checked in accessible criticism.'),
 (5,'SuperSummary — Chapters 13–18','https://www.supersummary.com/the-neverending-story/chapters-13-18-summary/','reference',
  'Вторичный поэпизодный рассказ и небольшие цитаты, прочитанные в guide. Отдельные формулировки проверены по другим источникам; чтение всего издания не заявляется.',
  'Secondary chapter-event accounts and short quotations read in the guide. Selected formulations were checked against other sources; no complete-edition reading is claimed.'),
 (6,'SuperSummary — Chapters 19–22','https://www.supersummary.com/the-neverending-story/chapters-19-22-summary/','reference',
  'Прочитан профессиональный поэпизодный guide, дополненный выбранными первичными цитатами в критике. Это не полный первичный текст и не свидетельство чтения официального RU/EN издания.',
  'The professional chapter-event guide was read, supplemented by selected primary quotations in criticism. This is not full primary text or evidence of reading an official RU/EN edition.'),
 (7,'SuperSummary — Chapters 23–26','https://www.supersummary.com/the-neverending-story/chapters-23-26-summary/','reference',
  'Поздние главы проверены по вторичному последовательному рассказу и выбранным цитируемым местам у исследователей. Полное издание не прочитано. По ссылке есть спойлеры.',
  'The late chapters were checked through a continuous secondary event account and selected passages quoted by researchers. The complete edition was not read. The linked page contains spoilers.'),
 (8,'SuperSummary — Important Quotes','https://www.supersummary.com/the-neverending-story/important-quotes/','book',
  'Небольшие первичные отрывки, воспроизведённые внутри guide, отделены от соседнего комментария. Страницы относятся к указанному guide английскому изданию и здесь не сертифицируются. Ссылка со спойлерами.',
  'Short primary excerpts reproduced inside the guide are distinguished from adjacent commentary. Page references belong to the English edition cited by the guide and are not independently certified here. Spoilers at the link.'),
 (9,'Marcus Schnöbel — Erzählung und Märchen (1995)','https://d-nb.info/1050266595/34','reference',
  'Выбранные разделы академической экзаменационной работы: событийные списки и явно выделенные цитаты романа. Это не издание романа и не рецензируемая монография. Интерпретации исследователя не выданы за события.',
  'Selected sections of an academic state-examination study: event lists and explicitly identified novel quotations. This is neither a novel edition nor a peer-reviewed monograph. The researcher’s interpretations are not presented as events.'),
 (10,'Albert Meier — Postmoderne: Philosophie – Literatur','https://www.litwiss-online.uni-kiel.de/wp-content/uploads/2017/03/Deutschsprachige-Texte-der-Postmoderne-Albert-Meier_Postmoderne.pdf','reference',
  'Выбранные места раздела о романе, печатные с. 92–95. Вторичный комментарий и цитаты различены; приведённые исследователем номера страниц не заменяют проверки издания. Ссылка раскрывает сюжет.',
  'Selected passages in the novel section, printed pp. 92–95. Secondary commentary is distinguished from quotations; the researcher’s page numbers do not replace edition verification. Spoilers at the link.'),
 (11,'Gale / Encyclopedia.com — The Neverending Story, critical anthology','https://www.encyclopedia.com/children/academic-and-educational-journals/neverending-story','reference',
  'Прочитаны относящиеся к роману критические фрагменты, включая явно цитируемые первичные места. Символические трактовки критиков не приняты за авторские объяснения. Ссылка со спойлерами.',
  'Relevant critical extracts, including explicitly quoted primary passages, were read. Critics’ symbolic interpretations are not treated as the author’s explanations. Spoilers at the link.'),
 (12,'Brian Stableford / EBSCO — The Neverending Story by Michael Ende','https://www.ebsco.com/research-starters/literature-and-writing/neverending-story-michael-ende','reference',
  'Прочитана именная справочная статья, раздел Form and Content. Это независимый вторичный рассказ, не первичный текст романа. По ссылке есть спойлеры.',
  'The named reference article’s Form and Content section was read. This is an independent secondary account, not primary novel text. The linked page contains spoilers.'),
]
sources=[dict(id=i,title=t,url=u,role=r,note=dict(ru=ru,en=en)) for i,t,u,r,ru,en in source_specs]
data=dict(schemaVersion=2,slug='the-neverending-story',title=dict(ru='Бесконечная история',en='The Neverending Story'),
 description=dict(ru='Мальчик открывает книгу, в которой от человеческого ребёнка зависит судьба Фантазии.',en='A boy opens a book in which Fantastica’s fate depends on a human child.'),
 defaultLanguage='ru',defaultTheme='dark',defaultMode='essential',contentMode='narrative',spoilerPolicy='full-plot-in-deep',
 methodNote=dict(
  ru='Короткий пересказ своими словами романа Михаэля Энде Die unendliche Geschichte (1979), обеих его частей. Основа — профессиональный поэпизодный guide SuperSummary, выбранные цитируемые первичные отрывки в guide и немецкой/англоязычной критике, испанское начало издательского образца. Полного издания здесь не прочитано; это не официальный RU/EN перевод. Русские имена переданы для этого пересказа. Essential и Core останавливаются до поздней развязки; Deep раскрывает её после отдельного согласия. Внешние источники могут содержать спойлеры.',
  en='An original-word condensation of both parts of Michael Ende’s Die unendliche Geschichte (1979). Based on SuperSummary’s professional chapter-event guide, selected primary passages quoted in that guide and German/English criticism, and the Spanish opening in a publisher sample. No complete edition was read here; this is not an official RU/EN translation. Russian names are rendered for this retelling. Essential and Core stop before the late resolution; Deep reveals it after separate consent. External sources may contain spoilers.'),
 sources=sources,media={},screens=[])
data['screens'].append(dict(id='cover',level=1,type='cover',sources=[],copy={
 'ru':dict(section='Михаэль Энде · 1979',title='Бесконечная история',subtitle='Книга, которая замечает читателя',body='<p>Бастиан прячется от школьных мучителей в книжной лавке. Там его ждёт история, от которой всё труднее оторваться.</p><p class="muted">Essential и Core оставляют позднюю развязку открытой. Deep — обе части романа до конца, со спойлерами.</p>',visualAlt='Текстовая обложка романа Михаэля Энде'),
 'en':dict(section='Michael Ende · 1979',title='The Neverending Story',subtitle='A book that notices its reader',body='<p>Bastian escapes his school tormentors in a bookshop. A story waits there that becomes harder and harder to put down.</p><p class="muted">Essential and Core leave the late resolution open. Deep follows both parts to the end, with spoilers.</p>',visualAlt='Text cover for Michael Ende’s novel')}))
for n,(sid,level,ru_title,en_title,ids) in enumerate(beats):
 section={'ru':'Книга на чердаке' if n<12 else 'В Фантазии','en':'The book in the attic' if n<12 else 'In Fantastica'}
 if n>=24: section={'ru':'Дальше по Фантазии','en':'Further through Fantastica'}
 data['screens'].append(dict(id=sid,level=level,claimType='book',sources=ids,copy={lang:dict(section=section[lang],title=title,body='<p>'+html.escape(paragraphs[lang][n],quote=False)+'</p>') for lang,title in [('ru',ru_title),('en',en_title)]}))
data['screens'].append(dict(id='final',level=1,final=True,claimType='synthesis',sources=[],copy={
 'ru':dict(section='Пауза',title='За следующим поворотом',body='<p>Здесь заканчивается выбранная дорожка чтения. Essential и Core оставляют поздние события открытыми; в Deep рассказ идёт до конца романа.</p><p>Развязка появляется только после предупреждения. Источники и границы пересказа доступны в меню.</p>'),
 'en':dict(section='Pause',title='Beyond the next turn',body='<p>This reading route ends here. Essential and Core leave the late events open; Deep follows the story to the end of the novel.</p><p>The resolution appears only after a warning. Sources and the retelling’s limits are available in the menu.</p>')}))
data['targetModes']={mode:sum(s['level']<=level for s in data['screens']) for mode,level in [('essential',1),('core',2),('deep',3)]}
(root/'story-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'paragraphsPerLanguage':len(beats),'targetModes':data['targetModes'],'sources':len(sources)},ensure_ascii=False))

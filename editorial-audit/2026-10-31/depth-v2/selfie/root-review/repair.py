# coding: utf-8
from pathlib import Path
import datetime
import hashlib
import html
import json
import re

R = Path(__file__).resolve().parent
H = R.parent
load = lambda p: json.loads(p.read_text())
sha = lambda b: hashlib.sha256(b).hexdigest()
original = load(R / 'input-story-data.json')
by_id = {s['id']: s for s in original['screens']}
drafts = {lang: (H / f'draft.{lang}.md').read_text() for lang in ['ru', 'en']}
assert all(drafts[lang] == (R / f'input-draft.{lang}.md').read_text() for lang in drafts), 'One-shot original-draft repair only'
repairs = []

def plain(t):
    return html.unescape(re.sub(r'<[^>]+>', '', t.replace('</p>', '\n\n'))).strip()

def replace(sid, ru_old, ru_new, en_old, en_new, finding='SF-PROSE-01', locator=None):
    for lang, old, new in [('ru', ru_old, ru_new), ('en', en_old, en_new)]:
        assert old in plain(by_id[sid]['copy'][lang]['body']), (sid, lang, old)
        assert drafts[lang].count(old) == 1, (sid, lang, old)
        drafts[lang] = drafts[lang].replace(old, new, 1)
        repairs.append({'screen': sid, 'language': lang, 'finding': finding,
                        'old': old, 'new': new, 'primaryLocator': locator})

replace('reputation-continued',
        'Объяснить социальные награды насилия — не значит оправдать его. ', '',
        'Explaining the social rewards of violence does not excuse it. ', '')
replace('alliances',
        ', а не как экспериментальное объяснение биографии Джона.', '.',
        ', not as an experimental explanation of John’s biography.', '.')
replace('good-for-whom',
        ' Однако детские результаты не превращаются в доказательство, что любой взрослый всегда заботится обо всех одинаково.', '',
        ' The findings do not prove that every adult always cares about everyone equally.', '')
replace('good-for-whom-continued',
        'Это рассказ свидетеля, а не лабораторное подтверждение неизбежности подобного исхода. ', '',
        'This is a witness’s account, not laboratory proof that the outcome was inevitable. ', '')
replace('greek-shores-continued',
        'Экологическая цепочка Нисбетта — предлагаемая историческая интерпретация, а не опыт, изолировавший одну причину на протяжении тысячелетий. Её ценность для книги — сделать привычный индивидуализм исторически возникшим, а не единственно мыслимым устройством сознания.',
        'Эта историческая линия делает привычный индивидуализм возникшим в определённых условиях, а не единственно мыслимым устройством сознания.',
        'Nisbett’s ecological chain is a historical interpretation, not an experiment isolating one cause across millennia. Its value to the book is to make familiar individualism something that arose historically, rather than the only conceivable arrangement of consciousness.',
        'This historical account makes familiar individualism something that arose under particular conditions, rather than the only conceivable arrangement of consciousness.')
replace('harmony-cost-continued',
        'Эти свидетельства и интерпретации не объясняют каждый трагический случай. Их функция в аргументе уже: разные культуры предлагают разные сценарии поражения.',
        'По мысли Сторра, разные культуры предлагают разные сценарии поражения.',
        'These accounts and interpretations do not explain every tragedy. Their role is narrower: different cultures provide different scenarios of defeat.',
        'In Storr’s account, different cultures provide different scenarios of defeat.')
replace('prestige-continued',
        'Настоятель и телевизионная звезда не тождественны; сопоставление касается пути влияния. ', '',
        'An abbot and a television star are not identical; the comparison concerns a route of influence. ', '')
replace('inner-evil',
        ' Биографическая реконструкция не даёт ему прямого доступа к причинам чужой теории.', '',
        ' Biographical reconstruction does not give him direct access to the causes of another person’s theory.', '')
replace('mind-cure-continued',
        'Книга не рекомендует эти методы и не подтверждает лечебные обещания. Её вопрос — куда помещается причина происходящего.',
        'Сторра интересует, куда теперь помещают причину болезни или бедности.',
        'The book neither recommends these methods nor confirms their medical promises. It asks where the cause of events is being located.',
        'Storr asks where the cause of illness or poverty is now being located.')

old_ru = plain(by_id['rogers-continued']['copy']['ru']['body'])
old_en = plain(by_id['rogers-continued']['copy']['en']['body'])
new_ru = 'Сторр не смешивает ценность сочувственного отношения с доказанностью безграничной силы личности. Отношения, которые помогают человеку, и теория об изначально совершенном «я» — разные утверждения. В 1964 году Роджерс получил грант на трёхлетнюю программу групповой терапии в калифорнийских монастырях. Участник проекта Уильям Коулсон позднее вспоминал, что сёстры сначала доверились обещанию большей открытости. Но, по его оценке, освобождение личных желаний обернулось распадом прежнего уклада: из 615 монахинь 300 подали прошения об отказе от пострига спустя год после вмешательства. Роджерс завершил исследование на год раньше намеченного срока. Коулсон считал это провалом. Через его рассказ Сторр показывает столкновение индивидуального освобождения с обязательствами, на которых держалась община.'
new_en = 'Storr does not confuse the value of compassion with proof that individuals possess unlimited power. Helpful relationships and a theory of an originally perfect self are different propositions. In 1964, Rogers received a grant for a three-year programme of encounter groups in Californian convents. Participant William Coulson later recalled that the sisters initially trusted the promise of greater openness. In his assessment, however, liberating personal wishes disrupted their established life: of 615 nuns, 300 applied to leave their order a year after the intervention. Rogers ended the study a year earlier than planned. Coulson considered it a failure. Through his account, Storr shows individual liberation colliding with the commitments sustaining a community.'
replace('rogers-continued', old_ru, new_ru, old_en, new_en, 'SF-CASE-01', 'OPS/ch1-10.xhtml P030')

replace('late-doubt', 'Питера Мартина', 'Питера Марина',
        'Peter Marin’s reporting', 'Peter Marin’s reporting',
        'SF-NAME-01', 'OPS/ch1-12.xhtml P017–018; Harper’s indexed title/byline metadata')
replace('late-doubt',
        ' Это свидетельства и критические интерпретации эпохи, а не психологическая диагностика каждого участника.', '',
        ' These are contemporary accounts and critical interpretations, not psychological diagnoses of every participant.', '')
replace('reason-and-recognition',
        'Сторр передаёт этот материал как историю конкретных отношений, не выводя из него клинический диагноз. Его интересует устойчивое противоречие',
        'Сторра интересует устойчивое противоречие',
        'Storr presents this as the history of particular relationships, without deriving a clinical diagnosis. He is interested in the persistent contradiction',
        'Storr is interested in the persistent contradiction')
replace('rules-change-continued',
        'Это его способ связать историю экономики с историей идеала, а не исчерпывающее объяснение всех реформ или личных решений. Однако связь позволяет понять',
        'Эта связь экономики и идеала помогает понять',
        'This is his way of connecting economic history to the history of an ideal, not an exhaustive explanation of every reform or personal decision. It nevertheless helps explain',
        'This connection between economic history and the history of an ideal helps explain')
replace('baumeister',
        ' Биография помогает понять ставки вопроса, но не заменяет проверку научных выводов.', '',
        ' Biography establishes personal stakes without replacing scrutiny of scientific conclusions.', '')
replace('baumeister-continued',
        ' Это вывод рассматриваемой работы, а не объявление окончательного состояния науки сегодня.', '',
        ' This is the conclusion of the work discussed, not a declaration about the final state of science today.', '')
replace('free-game-cost-continued',
        'Не каждое неудобство тождественно большому экономическому кризису; их связывает движение ответственности к отдельному человеку.',
        'В обоих случаях ответственность смещается к отдельному человеку.',
        'Not every inconvenience equals an economic catastrophe; the connection is a movement of responsibility towards individuals.',
        'In both cases, responsibility shifts towards individuals.')
replace('engelbart-continued',
        'Но Сторр не превращает Энгельбарта в единственного создателя всех последующих систем. Он прослеживает линию влияния через коллективную работу, исследовательские учреждения и последующие заимствования.',
        'Сторр прослеживает дальнейшую жизнь идей Энгельбарта через коллективную работу, исследовательские учреждения и последующие заимствования.',
        'Yet Storr does not make Engelbart the sole inventor of every subsequent system. He follows influence through collaborative work, research institutions and later adaptations.',
        'Storr follows the further life of Engelbart’s ideas through collaborative work, research institutions and later adaptations.')
replace('laboratory',
        'Сторр опирается здесь на исторические рассказы, а не представляет контролируемое сравнение методов управления. ', '',
        'Storr draws on historical accounts here, not a controlled comparison of management methods. ', '')
replace('social-profile-continued',
        'Это объяснение автора относится к описанной им эпохе, прежде всего к развитию Web 2.0 и последствиям кризиса 2008 года. Оно не является проверкой нынешних платформ. Сторра интересует, как обещанная свобода личности может совпасть с усилением самоконтроля и конкуренции.',
        'На фоне развития Web 2.0 и последствий кризиса 2008 года Сторр замечает, как обещанная свобода личности совпадает с усилением самоконтроля и конкуренции.',
        'This is the author’s explanation of the period he describes, particularly Web 2.0 and the aftermath of the 2008 crisis. It is not an assessment of present platforms. He asks how promised personal freedom can coincide with stronger self-monitoring and competition.',
        'Against the development of Web 2.0 and the aftermath of the 2008 crisis, Storr notices promised personal freedom coinciding with stronger self-monitoring and competition.')
replace('selfie-drone-continued',
        'Это конкретный собеседник, а не представитель всех инженеров. ', '',
        'This is one interviewee, not a representative of every engineer. ', '')

market_ru = [
    'Антрополог Элис Марвик объясняет Сторру, что вместе с условиями труда меняется и представление о собственной ценности. Вместо компании, которая обучает и годами удерживает сотрудника, возникает поток временных работников. Каждый сам поддерживает навыки и ищет следующий контракт; невозможность найти работу теперь легко объявить его личным провалом. Сторр связывает это с рассказом Джереми о сне на складе и риске остаться без оплаты. Даже свобода переходить между проектами требует постоянного управления собой: рынок вознаграждает инициативу и статус, а человек сам подстраивает под него свою жизнь.',
    'Требование совершенствоваться создаёт и потребительский рынок. Шоу с преображениями, средства для похудения и пособия по эффективности продают способы стать более подходящим человеком. Марвик описывает, как стремление к независимости может закончиться усвоением корпоративных норм. При этом она видит и выгоды такого коммерческого интереса: по её мнению, признание геев и лесбиянок ценными потребителями помогало поддержать борьбу за их права. В рассказе Сторра культура не просто давит извне — её награды постепенно становятся нашими собственными желаниями.'
]
market_en = [
    'Anthropologist Alice Marwick tells Storr that changing employment conditions also change how people understand their worth. Instead of a company training and retaining employees for years, a stream of temporary workers emerges. Each must maintain skills and seek the next contract; failing to find work can now be declared a personal failure. Storr connects this with Jeremy’s account of sleeping in a warehouse and risking no payment. Even the freedom to move between projects demands continual self-management: the market rewards initiative and status, and individuals reshape their own lives around it.',
    'The demand for improvement also creates a consumer market. Makeover programmes, weight-loss products and efficiency manuals sell ways of becoming a more suitable person. Marwick describes how pursuing independence can end in adopting corporate norms. She also sees benefits in commercial interest: in her view, recognising gay and lesbian people as valuable consumers helped support demands for their rights. In Storr’s account, culture does more than press from outside; its rewards gradually become desires we experience as our own.'
]
for lang, paras in [('ru', market_ru), ('en', market_en)]:
    anchor = plain(by_id['selfie-drone-continued']['copy'][lang]['body'])
    # The short interviewee-disclaimer sentence was removed above.
    anchor = anchor.replace('Это конкретный собеседник, а не представитель всех инженеров. ', '').replace('This is one interviewee, not a representative of every engineer. ', '')
    assert drafts[lang].count(anchor) == 1
    drafts[lang] = drafts[lang].replace(anchor, '\n\n'.join(paras) + '\n\n' + anchor, 1)
    repairs.append({'screen': 'market-in-the-self', 'language': lang, 'finding': 'SF-MEAN-01',
                    'old': None, 'new': paras, 'primaryLocator': 'OPS/ch1-17.xhtml P050–061'})

replace('political-heroes-continued',
        ' Его разбор не является полной теорией выборов или позднейших политических событий.', '',
        ' His analysis is not a complete theory of elections or subsequent political developments.', '')
replace('protected-child',
        'Здесь важно значение, а не способ: внешне привилегированная жизнь',
        'Внешне привилегированная жизнь',
        'The meaning matters here, not the method: an outwardly privileged life',
        'An outwardly privileged life')
replace('admiration',
        ' Сторр сохраняет именно эту атрибуцию: он слышит её версию поступков, а не читает чувства всех участников.', '',
        ' Storr preserves that attribution: he hears her account of her actions, not the feelings of every participant.', '')
replace('admiration-continued',
        'Этот рассказ не нужен для нового требования ненавидеть себя. Он показывает различие между признанием человеческой ценности и зависимостью от превосходства.',
        'Для Сторра здесь важно различие между признанием человеческой ценности и зависимостью от превосходства.',
        'The story does not support a new demand to hate oneself. It distinguishes recognition of human worth from dependence on superiority.',
        'For Storr, the distinction between recognising human worth and depending on superiority matters here.')
replace('austen-heinz',
        ' Это журналистская реконструкция; присутствие автора при личных сценах не подразумевается.', '',
        ' This is journalistic reconstruction; the author’s presence at private scenes is not implied.', '')
replace('entrapment',
        ' Это оценка сестры, а не экспериментальное установление причин.', '',
        ' This is his sister’s assessment, not an experimental finding about causation.', '')
replace('entrapment-continued',
        'Он не обязан принять все мечты Хайнца, чтобы считать публичную травлю несправедливой. И не обязан считать социальные навыки достаточными, чтобы заметить цену их недостатка.',
        'Сторр признаёт неловкость и просчёты Хайнца в общении, но считает травлю несправедливой.',
        'He need not accept every ambition of Heinz’s to consider public harassment unjust. Nor must he consider social skills adequate to recognise the cost of their absence.',
        'Storr recognises Heinz’s social awkwardness and mistakes while considering the harassment unjust.',
        'SF-COPY-01', 'OPS/ch1-20.xhtml P027–035')
replace('self-reconsidered-continued',
        'Этот поворот нужен, чтобы финал не стал новым мифом о возможности выбрать любое «я». ', '',
        'This turn prevents the ending becoming another myth about choosing any self. ', '')
replace('final',
        'Это не отмена критики Долины и не признание, что технический прогресс разрешил человеческие противоречия. ', '',
        'This neither cancels his criticism of Silicon Valley nor establishes that technical progress has solved human contradictions. ', '')

for lang, text in drafts.items():
    (H / f'draft.{lang}.md').write_text(text)
(R / 'repairs.json').write_text(json.dumps(repairs, ensure_ascii=False, indent=2) + '\n')
(R / 'prose-revision.json').write_text(json.dumps({
    'atUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'stage': 'Connected bilingual prose revised before segmentation',
    'rootPersonalAcceptance': False,
    'draftSha256': {lang: sha(text.encode()) for lang, text in drafts.items()},
    'changedOrNewScreenIds': sorted({r['screen'] for r in repairs}),
    'sourceScope': 'Actual selected source passages and publisher byline metadata; no full root or published-English collation.'
}, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'records': len(repairs), 'changedOrNewScreenIds': len({r['screen'] for r in repairs}), 'newScreen': 'market-in-the-self'}))

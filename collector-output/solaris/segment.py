# -*- coding: utf-8 -*-
"""Segment the already-written manuscript. Run from this directory."""
import html
import json
from pathlib import Path

root = Path(__file__).resolve().parent
old = json.loads((root / 'story-data.json').read_text())
text = (root / 'narrative-draft.md').read_text()
paras = {lang: text.split('## ' + lang.upper() + '\n\n')[1].split('\n## ')[0].strip().split('\n\n') for lang in ('ru', 'en')}
assert len(paras['ru']) == len(paras['en']) == 29
j = {
    'schemaVersion': 2, 'slug': 'solaris',
    'title': {'ru': 'Солярис', 'en': 'Solaris'},
    'author': {'ru': 'Станислав Лем', 'en': 'Stanisław Lem'},
    'description': {
        'ru': 'Пустая станция над чужим океаном. Крис Кельвин встречает женщину, которую потерял десять лет назад. Краткое изложение романа Станислава Лема своими словами.',
        'en': 'An empty station above an alien ocean. Kris Kelvin meets the woman he lost ten years ago. A concise original-word retelling of Stanisław Lem’s novel.'},
    'defaultLanguage': 'ru', 'defaultTheme': 'dark', 'defaultMode': 'essential',
    'contentMode': 'narrative', 'audience': 'adult', 'spoilerPolicy': 'full-plot-in-deep',
    'methodNote': {
        'ru': 'Краткое изложение романа «Солярис» (1961) своими словами, а не текст перевода или экранизации. Непосредственно прочитан разрешённый первый раздел в переводе Билла Джонстона. Дальнейшие события сверены по открытым поглавным разборам LitCharts, польским учебным материалам и указанным цитируемым фрагментам романа. Полного издания не читали; точный объём проверки указан в примечаниях. Хари / Harey и Снаут / Snaut соответствуют Rheya и Snow старого английского перевода, на котором основаны англоязычные разборы. Essential/Core сохраняют позднюю развязку; Deep открывается после отдельного подтверждения. Внешние источники содержат спойлеры.',
        'en': 'A concise original-word retelling of Solaris (1961), not the text of a translation or film. The authorized first chapter in Bill Johnston’s translation was read directly. Later events were checked through public LitCharts chapter accounts, Polish study materials and the specified quoted passages from the novel. No complete edition was read; notes identify the exact scope. Harey and Snaut correspond to Rheya and Snow in the older English translation used by the English-language guides. Essential/Core withhold the late resolution; Deep requires separate consent. External sources contain spoilers.'},
    'media': old['media'], 'sources': [], 'screens': []}

def source(n, title, url, role, ru, en):
    j['sources'].append(dict(id=n, title=title, url=url, role=role, note=dict(ru=ru, en=en)))

source(1, 'Stanisław Lem · Newcomer · Bill Johnston',
       'https://english.lem.pl/works/novels/solaris/47-look-inside-solaris', 'book',
       'Разрешённая первая глава прочитана целиком. Прибытие и разговор со Снаутом; это не полное издание.',
       'Complete authorized first chapter read: arrival and Snaut’s welcome. This is not a complete edition.')
source(2, 'Stanisław Lem · Lem’s opinion',
       'https://english.lem.pl/works/novels/solaris/44-lems-opinion', 'author',
       'Короткий авторский комментарий о создании романа и пределах уверенных толкований; не источник поздних событий.',
       'Short author commentary on composition and interpretive caution; not evidence for later events.')
source(3, 'Lem estate · A new translation of Solaris',
       'https://english.lem.pl/works/novels/solaris/196-a-new-translation-of-solaris', 'publisher',
       'Объявление перевода Джонстона 2011 года. Сведения об издании и именах, не полное чтение.',
       'Announcement of Johnston’s 2011 translation. Edition and naming context, not a full reading.')
source(4, 'Paweł Kozioł · Culture.pl · Solaris', 'https://culture.pl/en/work/solaris-stanislaw-lem', 'review',
       'Прочитаны сюжетная и критическая части статьи. Толкования остаются толкованиями; сведения статьи о переводах устарели. Ссылка со спойлерами.',
       'Plot and critical sections consulted. Interpretations remain interpretations; the translation information is outdated. Link contains spoilers.')
source(5, 'Paul Brians · Washington State University · Solaris',
       'https://brians.wsu.edu/2016/10/12/study-guide-for-stanislaw-lem-solaris-1961/', 'reference',
       'Четырнадцать разделов доступны в индексированном тексте; прямой адрес отдаёт 403. Вопросы не использованы как ответы. Контекст прежней проверки, не новый доступ к роману.',
       'Fourteen sections available as indexed text; direct address returns 403. Questions were not treated as answers. Prior-check context, not new novel access.')
source(6, 'Bryk / Interia · Solaris · Chapter account',
       'https://www.bryk.pl/lektury/stanislaw-lem/solaris.streszczenie-szczegolowe', 'reference',
       'Проверены открытые учебные описания поздней последовательности. Это пересказ, не первичный текст и не сертификат всего романа. Ссылка со спойлерами.',
       'Public study descriptions of the later sequence checked. A guide, not primary text or whole-novel certification. Link contains spoilers.')
source(7, 'Agnieszka Kubies · Różne oblicza spotkania z Obcym · 2013',
       'https://solaris.lem.pl/prace/PracaMgr_Agnieszka_Kubies.pdf', 'review',
       'Прочитаны относящиеся к роману страницы 64–67 диссертации на сайте наследия Лема. Только сверка действий; моральные толкования не заимствованы. Ссылка со спойлерами.',
       'Solaris discussion on printed pp. 64–67 of the estate-hosted thesis consulted. Action corroboration, not adoption of its moral interpretations. Link contains spoilers.')
source(8, 'Ireneusz Staroń · Solaris · University of Białystok · 2023',
       'https://repozytorium.uwb.edu.pl/jspui/bitstream/11320/14845/2/Proza_polska_przelomu_XX_i_XXI_wieku.pdf', 'review',
       'Проверен фрагмент статьи на печатных страницах 58–60, включая цитату из романа. Остальная книга и предлагаемое психоаналитическое толкование не пересказываются. Ссылка со спойлерами.',
       'Printed pp. 58–60 of the essay consulted, including its novel quotation. The rest of the volume and its psychoanalytic interpretation are not retold. Link contains spoilers.')
source(9, 'Marcin Czerwiński · Eksperyment Myślowy · Solaris · 2026',
       'https://eksperymentmyslowy.pl/2026/02/18/em-poleca-45-dlaczego-warto-czytac-solaris-stanislawa-lema-po-65-latach-od-pierwszego-wydania/', 'review',
       'Проверены приведённые польские фрагменты романа и библиографические сведения. Выводы статьи не объявлены фактами сюжета. Ссылка со спойлерами.',
       'Quoted Polish novel passages and bibliography checked. The essay’s conclusions are not presented as plot facts. Link contains spoilers.')
source(10, 'Redakcja klp.pl · Solaris · Chapter account', 'https://klp.pl/solaris/a-10013-2.html', 'reference',
       'Проверены разделы от Narada до Sny. Используются действия и порядок; неточное слово «ничто» о структуре тела не перенесено. Ссылка со спойлерами.',
       'Sections Narada through Sny checked for actions and order; its inaccurate “nothingness” description of bodily structure is excluded. Link contains spoilers.')
slugs = ['chapter-2-the-solarists', 'chapter-3-the-visitors', 'chapter-4-sartorius',
         'chapter-5-rheya', 'chapter-6-the-little-apocrypha', 'chapter-7-the-conference',
         'chapter-8-the-monsters', 'chapter-9-the-liquid-oxygen', 'chapter-10-conversation',
         'chapter-11-the-thinkers', 'chapter-12-the-dreams', 'chapter-13-victory',
         'chapter-14-the-old-mimoid']
for chapter, slug in enumerate(slugs, 2):
    source(chapter + 9, f'LitCharts · Solaris · Chapter {chapter}',
           'https://www.litcharts.com/lit/solaris/' + slug, 'reference',
           'Прочитаны относящиеся к изложению открытые сюжетные абзацы этой главы. Платные скрытые части не читались. Пересказ использует имена Rheya/Snow; здесь Harey/Snaut. Ссылка со спойлерами.',
           'Relevant public plot paragraphs for this chapter consulted; locked portions were not read. The guide uses Rheya/Snow, rendered here as Harey/Snaut. Link contains spoilers.')

# Levels are assigned to the connected manuscript, never used to request padding.
meta = [
    ('kelvin-arrives', 1, 'Капсула', 'The capsule', [1]),
    ('broken-welcome', 1, 'Снаут', 'Snaut', [1]),
    ('solaristics-library', 1, 'История Соляриса', 'A history of Solaris', [11]),
    ('gibarian-traces', 2, 'След Гибаряна', 'Gibarian’s trail', [12]),
    ('sartorius-door', 2, 'За дверью', 'Behind the door', [13, 4]),
    ('harey-at-window', 1, 'У окна', 'By the window', [14]),
    ('kelvin-first-response', 1, 'Ракета', 'The shuttle', [14, 7]),
    ('snaut-mirrors', 2, 'После запуска', 'After the launch', [15]),
    ('berton-testimony', 2, 'Старый протокол', 'An old report', [15, 13]),
    ('two-dresses', 1, 'Два платья', 'Two dresses', [16, 4]),
    ('blood-examination', 2, 'Совещание', 'The conference', [16, 10]),
    ('harey-questions', 1, 'Она требует правды', 'She wants the truth', [17]),
    ('alien-forms', 2, 'Рядом с Гизе', 'Reading Giese', [17]),
    ('two-experiments', 1, 'Два замысла', 'Two proposals', [17, 10]),
    ('recordings-and-learning', 3, 'Пропавший магнитофон', 'The missing recorder', [18]),
    ('oxygen-attempt', 3, 'Шипение в темноте', 'Hissing in the dark', [18, 6, 7]),
    ('new-shared-time', 3, 'Нынешняя Хари', 'Harey now', [18, 10]),
    ('earth-promise', 3, 'Покинуть Солярис', 'Leaving Solaris', [19]),
    ('thought-transmission', 3, 'Под электродами', 'Under the electrodes', [20]),
    ('history-after-transmission', 3, 'Опять библиотека', 'Back to the library', [20, 10]),
    ('dreams-after-experiment', 3, 'Сны', 'The dreams', [21]),
    ('earthly-plans', 3, 'Дом на Земле', 'A house on Earth', [22]),
    ('sleep-and-absence', 3, 'Пустая каюта', 'The empty cabin', [22, 4]),
    ('reported-final-will', 3, 'Письмо', 'The letter', [22, 6, 4]),
    ('victory-irony', 3, 'Успех', 'Success', [22, 7, 6]),
    ('imperfect-god', 3, 'Несовершенный бог', 'An imperfect god', [23]),
    ('old-mimoid', 3, 'Старый мимоид', 'The old mimoid', [23]),
    ('hand-and-wave', 3, 'Рука и волна', 'Hand and wave', [8, 9, 23]),
    ('cruel-expectation', 3, 'Ожидание', 'Waiting', [9, 23]),
]
cover = dict(id='cover', type='cover', level=1, sources=[], media='ocean-gap', copy={})
for lang in ('ru', 'en'):
    cover['copy'][lang] = dict(
        section='Роман · 1961' if lang == 'ru' else 'A novel · 1961',
        title=j['title'][lang], subtitle=j['author'][lang],
        body='<p>Крис Кельвин прилетает изучать чужой океан. На станции его ждёт женщина, которую он потерял десять лет назад.</p><p class="muted">Essential и Core останавливаются до поздней развязки. Deep раскрывает её после отдельного подтверждения; там есть самоубийство и утрата.</p>' if lang == 'ru' else '<p>Kris Kelvin arrives to study an alien ocean. On the station he finds the woman he lost ten years ago.</p><p class="muted">Essential and Core stop before the late resolution. Deep reveals it after separate consent; it includes suicide and loss.</p>')
j['screens'].append(cover)
for idx, (sid, level, ru, en, ids) in enumerate(meta):
    if idx == 14:
        j['screens'].append(dict(id='deep-warning', level=3, claimType='book', sources=[], copy={
            'ru': dict(section='Deep', title='Дальше — развязка', body='<p>Продолжение раскрывает поздние события и последнюю сцену романа. В нём есть самоубийство и утрата. Essential и Core заканчиваются раньше. Чтобы сохранить развязку для самостоятельного чтения, переключитесь на один из этих режимов.</p>'),
            'en': dict(section='Deep', title='The resolution follows', body='<p>The continuation reveals later events and the novel’s final scene. It includes suicide and loss. Essential and Core end earlier. To leave the resolution for reading the novel yourself, switch to either of those modes.</p>')}))
    screen = dict(id=sid, level=level, claimType='book', sources=ids, copy={})
    for lang, title in [('ru', ru), ('en', en)]:
        section = ('Станция' if idx < 14 else 'Deep · Продолжение') if lang == 'ru' else ('The station' if idx < 14 else 'Deep · Continuation')
        screen['copy'][lang] = dict(section=section, title=title, body='<p>' + html.escape(paras[lang][idx], quote=False) + '</p>')
    j['screens'].append(screen)
j['screens'].append(dict(id='final', level=1, final=True, claimType='book', sources=[], copy={
    'ru': dict(section='Чтение закончено', title='Солярис', body='<p>Essential и Core сохраняют позднюю развязку. Продолжение и последняя сцена доступны в Deep после подтверждения.</p>'),
    'en': dict(section='End of reading', title='Solaris', body='<p>Essential and Core leave the late resolution undisclosed. The continuation and final scene are available in Deep after consent.</p>')}))
j['targetModes'] = {mode: sum(s['level'] <= level for s in j['screens']) for mode, level in [('essential', 1), ('core', 2), ('deep', 3)]}
# Same computed estimates as the maintained builder, with correct RU inflection.
j['modes'] = {
    'essential': {'minutes': {'ru': '3 минуты', 'en': '3 min'}},
    'core': {'minutes': {'ru': '5 минут', 'en': '5 min'}},
    'deep': {'minutes': {'ru': '9 минут', 'en': '9 min'}},
}
(root / 'story-data.json').write_text(json.dumps(j, ensure_ascii=False, indent=2) + '\n')
print(j['targetModes'], len(j['sources']))

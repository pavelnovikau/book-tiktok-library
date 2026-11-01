# -*- coding: utf-8 -*-
from pathlib import Path
import json

R = Path(__file__).resolve().parent
H = R.parent
repairs = json.loads((R / 'repairs.json').read_text())
edits = {x['screen']: x for x in repairs}
changes = [
('part-13-passage-03', 'ru', 'Она различала физическую разрушительность алкоголизма и спешки, но видела', 'Она не приравнивала физический вред спешки к разрушительным последствиям алкоголизма, но видела'),
('part-13-passage-03', 'en', 'She distinguished the physical destructiveness of alcoholism and hurry, while seeing', 'She did not equate the physical harm of hurry with alcoholism, but saw'),
('part-14-passage-01', 'ru', 'В его рассказе проступают настороженные лица торговцев и прежде незамеченная тень, намекающая на человека за пределами полотна.', 'Он стал различать настороженные лица торговцев и прежде незамеченную тень, намекающую на человека за пределами полотна.'),
('part-14-passage-01', 'en', 'His account describes wary faces and a previously unnoticed shadow suggesting somebody beyond the canvas.', 'He began to notice wary faces and a previously unseen shadow suggesting somebody beyond the canvas.'),
('part-14-passage-01', 'ru', 'Смысл реального задания Робертс', 'Смысл задания Робертс'),
('part-14-passage-01', 'en', "Roberts's actual assignment", "Roberts's assignment"),
('part-15-passage-03', 'ru', 'По изложению Беркмана, связь проявлялась даже среди пенсионеров, у которых не было собственного рабочего отпуска. Он служит автору свидетельством', 'В книге подчёркивается, что связь проявлялась даже среди пенсионеров, у которых не было собственного рабочего отпуска. Для Беркмана этот результат говорит'),
('part-15-passage-03', 'en', 'In Burkeman’s account, the association appeared even among pensioners, who had no working holiday of their own. It serves the author as evidence', 'The book reports the association even among pensioners, who had no working holiday of their own. For Burkeman this supports the case'),
('part-15-passage-04', 'ru', 'Получался выходной, когда жена работала, дети учились, а гости не могли прийти. ', ''),
('part-15-passage-04', 'en', "One's day off arrived while a wife worked, children attended school and visitors could not come. ", ''),
('part-18-passage-04', 'ru', ' Он противостоит привычке видеть исключительно растущий остаток.', ''),
('part-18-passage-04', 'en', ' It counters the habit of seeing only the growing remainder.', ''),
('part-18-passage-06', 'ru', ' Телефон снова становится больше инструментом, чем бесконечной игрушкой.', ''),
('part-18-passage-06', 'en', ' The phone becomes more of a tool again and less of an endless toy.', ''),
('part-18-passage-06', 'ru', 'Они уменьшают конкретные поводы', 'Такие настройки уменьшают конкретные поводы'),
('part-18-passage-06', 'en', 'They reduce specific invitations', 'These changes reduce specific invitations'),
('part-18-passage-07', 'ru', 'Они показывают альтернативу накоплению', 'Такие занятия показывают альтернативу накоплению'),
('part-18-passage-07', 'en', 'They offer an alternative to accumulating', 'These activities offer an alternative to accumulating'),
]
for sid, language, old, new in changes:
    item = edits[sid]['languages'][language]
    assert item['after'].count(old) == 1, (sid, language, old)
    item['after'] = item['after'].replace(old, new)
for language in ['ru', 'en']:
    path = H / f'draft.{language}.md'
    text = path.read_text()
    for sid, lang, old, new in changes:
        if lang != language:
            continue
        assert text.count(old) == 1, (sid, language, old)
        text = text.replace(old, new)
    path.write_text(text)
for sid in sorted({x[0] for x in changes}):
    edits[sid]['reasons'].append('FW-COPY-02: final reread repaired antecedents, removed duplicated wording and clarified the author’s stated distinction.')
(R / 'repairs.json').write_text(json.dumps(repairs, ensure_ascii=False, indent=2) + '\n')
print('Final reading polish:', len({x[0] for x in changes}), 'paired screens; rebuild required.')

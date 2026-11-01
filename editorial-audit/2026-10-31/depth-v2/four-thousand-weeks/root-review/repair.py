# -*- coding: utf-8 -*-
from pathlib import Path
import datetime
import html
import json
import re

R = Path(__file__).resolve().parent
H = R.parent
original = json.loads((R / 'input-story-data.json').read_text())
data = json.loads((H / 'story-data.json').read_text())
assert data == original, 'Run this repair once against the personally read input.'
by = {s['id']: s for s in data['screens']}
planned = {}
reasons = {}
def plain(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s))
def change(sid, language, old, new, reason):
    key = sid, language
    current = planned.get(key, plain(by[sid]['copy'][language]['body']))
    assert current.count(old) == 1, (sid, language, old)
    planned[key] = current.replace(old, new)
    reasons.setdefault(sid, []).append(reason)
def rewrite(sid, ru, en, reason):
    for language, text in [('ru', ru), ('en', en)]:
        planned[sid, language] = text
    reasons.setdefault(sid, []).append(reason)

change('part-07-passage-01', 'ru', ' Это легенда, объясняющая перфекционистское избегание, а не исторический факт, независимо установленный Беркманом.', '', 'FW-COPY-01: the opening already identifies the actual source legend; remove a redundant verification aside.')
change('part-07-passage-01', 'en', ' This is a legend explaining perfectionist avoidance, rather than a historical event Burkeman independently establishes.', '', 'FW-COPY-01')

rewrite('part-07-passage-04',
'Развивая мысль Роберта Гудина об оседлости и определённости, Беркман защищает выбор, закреплённый обязательством. Долгая приверженность делу или отношениям позволяет получить то, что не возникает при непрерывном сравнении вариантов. Особенно важен для него шаг, закрывающий лёгкий путь назад: съехаться, вступить в брак, подать заявление об увольнении. В его объяснении такой выбор способен принести облегчение: вместо бесконечного перебора возможных жизней человек встречается с последствиями одной действительной. При этом Беркман признаёт, что некоторые отношения стоит прекратить, а некоторые решения бывают плохими. Нужно различать конкретную непригодность выбранного пути и разочарование от несовершенства любого реального пути. Сознательный отказ и серьёзное обязательство требуют одного — расстаться с мечтой сохранить все возможности без потерь.',
'Developing Robert Goodin’s account of settling, Burkeman defends a choice secured by commitment. Sustained dedication to work or relationships allows experiences unavailable through continual comparison of alternatives. He particularly values a step that closes the easy way back: moving in together, marrying, handing in a resignation. In his account, such a decision can bring relief: instead of endlessly comparing possible lives, one encounters the consequences of an actual one. Yet Burkeman acknowledges that some relationships should end and some decisions are bad. A particular path’s unsuitability must be distinguished from disappointment that every real path is imperfect. Deliberate rejection and serious commitment both require relinquishing the dream of keeping every possibility without loss.',
'FW-MEAN-01: restore the author’s mechanism of irreversible commitment and its possible relief, alongside his explicit poor-choice qualification; content4 P025–029.')

change('part-08-passage-04', 'ru', ' Это не доказательство одинакового воздействия соцсетей на каждого человека, а описанный им опыт.', '', 'FW-COPY-01: retain autobiographical attribution without a universal-effect audit aside.')
change('part-08-passage-04', 'en', ' This is his described experience, not proof of identical social-media effects on everyone.', '', 'FW-COPY-01')
change('part-09-passage-01', 'ru', 'Это опыт конкретного человека в конкретной практике; он не превращается в совет читателю повторить обливания или в обещание устранить физическую боль одной концентрацией.', 'После уединения Янг, по его воспоминанию, заметил перемену и в повседневных делах: прежние раздражение и скука уступали интересу, когда он переставал сопротивляться самому переживанию.', 'FW-CASE-01: replace an audit aside with Young’s actual reported everyday aftermath; content6 P003–005. No cold-water procedure or quantities added.')
change('part-09-passage-01', 'en', 'It is one person\'s experience in a particular practice, not advice to repeat the dousing or a promise that concentration alone will eliminate physical pain.', 'After the retreat, Young recalled a change in everyday tasks too: irritation and boredom gave way to interest when he stopped resisting the experience itself.', 'FW-CASE-01')

rewrite('part-09-passage-04',
'Беркман предлагает перестать ждать, что важное дело однажды перестанет вызывать дискомфорт. Непонимание, скука и неуверенность для него — часть столкновения с реальностью, а не сигнал немедленно менять занятие. Пока человек требует сначала устранить эти чувства, часть внимания уходит на борьбу с самим фактом ограничений. Признание, что задача трудна и её исход нельзя полностью подчинить себе, возвращает внимание к работе. Так автор объясняет парадокс: согласие с отсутствием окончательного решения само становится практическим решением. В его опыте спокойнее заниматься сложным проектом удаётся именно после отказа от требования, чтобы всё ощущалось лёгким, управляемым и заранее надёжным.',
'Burkeman proposes giving up the expectation that important work will one day cease to feel uncomfortable. Incomprehension, boredom and uncertainty are, for him, part of encountering reality rather than signals to change activities immediately. Demanding that these feelings first disappear directs some attention towards fighting the very fact of limitation. Acknowledging that a task is difficult and its outcome cannot be fully controlled returns attention to the work. This explains his paradox: accepting the absence of a final solution itself becomes a practical solution. In his experience, settling calmly into a difficult project becomes possible after relinquishing the demand that everything feel easy, manageable and secure in advance.',
'FW-MEAN-02: restore the author’s affirmative account of accepting discomfort rather than reframing it as a narrowly bounded attention observation; content6 P012–017. The account remains explicitly attributed, not a diagnosis.')

change('part-11-passage-03', 'ru', ' Это анализ определённого профессионального устройства, а не утверждение о каждом юристе.', '', 'FW-COPY-01: attribution and the modal wording already bound Kaveny’s analysis.')
change('part-11-passage-03', 'en', ' This analyzes a particular professional arrangement rather than asserting something about every lawyer.', '', 'FW-COPY-01')

rewrite('part-13-passage-03',
'Психотерапевт Стефани Браун рассказывала Беркману о преуспевающих клиентах Кремниевой долины, которым было трудно спокойно просидеть даже сеанс. Остановка поднимала тревогу, и новым движением они пытались её подавить. Браун сравнивала это с механизмом зависимости: средство облегчения порождает последствия, вызывающие ещё большую потребность в том же средстве. Она различала физическую разрушительность алкоголизма и спешки, но видела сходство психологического круга: тревожно, что не успеваю; ускоряюсь; замечаю ещё больше требований и меньше контроля; снова ускоряюсь. Выход она связывала с переменой взгляда: признать, что делам требуется собственное время, и перестать искать спасение в очередном ускорении. Тогда работа над медленным проектом может стать выбранным занятием, а не раздражающей задержкой.',
'Psychotherapist Stephanie Brown told Burkeman about successful Silicon Valley clients who struggled to sit quietly even through a session. Stopping brought up anxiety, which renewed motion helped suppress. Brown compared this with a mechanism of addiction: a source of relief produces consequences that increase the need for the same source. She distinguished the physical destructiveness of alcoholism and hurry, while seeing a similar psychological loop: fear of falling behind prompts acceleration; acceleration reveals more demands and less control; still more speed follows. She connected a way out with a changed perspective: acknowledge that activities require their own time and stop seeking rescue in another acceleration. Work on a slow project can then become a chosen activity rather than an irritating delay.',
'FW-MEAN-03: retain the actual analogy’s physical non-equivalence and restore Brown’s described change of perspective; content10 P012–018. Remove reader-diagnosis authoring language.')

change('part-14-passage-01', 'ru', 'Он описывает изменение собственного внимания, не устанавливая норматив в восемьдесят минут для любого зрителя.', 'В его рассказе проступают настороженные лица торговцев и прежде незамеченная тень, намекающая на человека за пределами полотна.', 'FW-CASE-02: replace a universal-timing disclaimer with concrete details in Burkeman’s reported Degas experience; content11 P009–011. No direct image inspection claimed.')
change('part-14-passage-01', 'en', 'He describes a change in his attention, not an eighty-minute standard for every viewer.', 'His account describes wary faces and a previously unnoticed shadow suggesting somebody beyond the canvas.', 'FW-CASE-02')
change('part-14-passage-02', 'ru', 'Это частный рассказ о терпеливом разбирательстве, не обещание, что каждый человек сможет сам исправить любую неисправность.', 'Для Пека это пример практического навыка: выдержать начальное непонимание и дать себе время разобраться, прежде чем хвататься за первое действие ради ощущения контроля.', 'FW-MEAN-03: restore Peck’s practical generalization with attribution instead of reducing the case to an isolated anecdote; content11 P013–019.')
change('part-14-passage-02', 'en', 'This is a particular account of patient investigation, not a promise that anyone can fix every malfunction alone.', 'For Peck, this illustrates a practical skill: tolerate initial incomprehension and allow time to investigate before grabbing at an action merely to feel in control.', 'FW-MEAN-03')
change('part-14-passage-04', 'ru', ' Это притча о развитии, а не расписание карьерного успеха. Верность направлению даёт возможность получить его поздние плоды; сама по себе она не доказывает, что всякий выбранный маршрут обязательно хорош.', '', 'FW-COPY-01: remove repeated non-guarantee commentary; the actual bus parable remains, and the immediately following passage retains the leave/stay distinction.')
change('part-14-passage-04', 'en', ' This is a parable of development, not a career-success timetable. Commitment makes later possibilities accessible; it does not itself establish that every chosen route is good.', '', 'FW-COPY-01')

change('part-15-passage-03', 'ru', 'Этот показатель нельзя превращать в доказательство лечебного действия каникул для конкретного человека.', 'По изложению Беркмана, связь проявлялась даже среди пенсионеров, у которых не было собственного рабочего отпуска.', 'FW-CASE-03: retain book-level reporting and the dispensing measure; restore the counterintuitive pensioner result that develops time’s network value, content12 P011–014. No underlying-study certification.')
change('part-15-passage-03', 'en', 'This measure must not become proof of holidays\' therapeutic effects for a particular person.', 'In Burkeman’s account, the association appeared even among pensioners, who had no working holiday of their own.', 'FW-CASE-03')
change('part-15-passage-04', 'ru', 'Беркман не приписывает всю историю режима календарной реформе; он использует её как конкретное проявление разрушения общего времени.', 'В приведённой им жалобе рабочий не знает, что делать со своим выходным: жена на заводе, дети в школе, а гости не могут прийти.', 'FW-CASE-03: replace an irrelevant regime-history disclaimer with the actual reported worker’s complaint; content12 P015–016. Indirect summary, no invented dialogue.')
change('part-15-passage-04', 'en', 'Burkeman does not attribute the regime\'s whole history to calendar reform; he uses it as a concrete instance of shared time being broken apart.', 'In the complaint he cites, a worker does not know what to do with his day off: his wife is at the factory, the children at school, and visitors cannot come.', 'FW-CASE-03')

change('part-16-passage-02', 'ru', 'Если они перекрываются, всю историю цивилизации можно мысленно охватить удивительно небольшим числом людей.', 'Выстроив такие жизни в цепочку без промежутков, всю историю цивилизации можно мысленно охватить удивительно небольшим числом людей.', 'FW-PRECISION-01: the source describes an unbroken chain, not overlapping hundred-year intervals; content13 P016–017.')
change('part-16-passage-02', 'en', 'With overlapping lives, the whole history of civilization can be mentally spanned by surprisingly few people.', 'An unbroken sequence of such lives lets us span the history of civilization with surprisingly few people.', 'FW-PRECISION-01')
change('part-16-passage-03', 'ru', 'Роман способен что-то дать нескольким читателям, не становясь новым Толстым.', 'Роман может что-то дать нескольким читателям, даже если его автор не станет новым Толстым.', 'FW-COPY-02: distinguish the novel from its author in the Tolstoy comparison; content13 P021–023.')
change('part-16-passage-03', 'en', 'A novel can offer something to a few readers without becoming another Tolstoy.', 'A novel can offer something to a few readers even if its author never becomes another Tolstoy.', 'FW-COPY-02')
change('part-17-passage-05', 'ru', ' Это не уравнивание профессионального знания с невежеством.', '', 'FW-COPY-01: remove editorial rebuttal; preserve the author’s actual institutional-improvisation argument and uncertainty.')
change('part-17-passage-05', 'en', ' This does not equate professional knowledge with ignorance.', '', 'FW-COPY-01')

change('part-18-passage-04', 'ru', 'Такой перечень не закрывает все задачи и не доказывает достаточность любой работы.', 'Такой перечень позволяет увидеть конкретные маленькие победы, которые иначе теряются за бесконечным остатком.', 'FW-PRACTICE-01: restore the author’s positive small-wins mechanism in place of an adequacy disclaimer; content16 P012–013.')
change('part-18-passage-04', 'en', 'Such a list neither closes every task nor proves all work adequate.', 'Such a list makes specific small wins visible when they would otherwise disappear behind the endless remainder.', 'FW-PRACTICE-01')
change('part-18-passage-04', 'ru', 'обычные действия тоже могут быть достижением.', 'даже почистить зубы или сварить кофе может быть достижением.', 'FW-PRACTICE-01: actual low-threshold examples, content16 P013.')
change('part-18-passage-04', 'en', 'ordinary actions can also be achievements.', 'even brushing one’s teeth or making coffee can be an achievement.', 'FW-PRACTICE-01')
change('part-18-passage-06', 'ru', 'Автор не обещает, что такие настройки исправят личность или обеспечат полную концентрацию.', 'Журналистка Нелли Боулз описывала, как после перехода к чёрно-белому экрану телефон стал для неё больше инструментом и меньше игрушкой.', 'FW-PRACTICE-01: retain the actual cited grey-screen experience with attribution, content16 P018.')
change('part-18-passage-06', 'en', 'The author does not promise that these settings will repair one\'s personality or deliver complete concentration.', 'Journalist Nellie Bowles described the monochrome screen as making her phone feel more like a tool and less like a toy.', 'FW-PRACTICE-01')
change('part-18-passage-07', 'ru', ' Эти примеры не обещают буквально удвоить срок жизни.', '', 'FW-COPY-01: the digest never states a literal lifespan-doubling claim; remove the unattached rebuttal.')
change('part-18-passage-07', 'en', ' These examples do not promise literally to double a lifespan.', '', 'FW-COPY-01')
change('part-18-passage-08', 'ru', 'Опираясь на Тома Хобсона,', 'Опираясь на специалиста по дошкольному образованию Тома Хобсона,', 'FW-CONTEXT-01: identify Hobson’s actual role on first body appearance, content16 P023.')
change('part-18-passage-08', 'en', 'Drawing on Tom Hobson,', 'Drawing on early-childhood educator Tom Hobson,', 'FW-CONTEXT-01')
change('part-18-passage-08', 'ru', ' Оно не отменяет личных границ и не делает любое чужое поведение приемлемым.', '', 'FW-COPY-01: remove inserted coaching qualification absent from this procedure; the book’s selected relationship and exploitation limits remain elsewhere.')
change('part-18-passage-08', 'en', ' It abolishes neither personal boundaries nor distinctions between acceptable and unacceptable behaviour.', '', 'FW-COPY-01')
change('part-18-passage-09', 'ru', '; перед читателем предложенная практика, а не свидетельство окончательно преобразившегося автора.', '.', 'FW-COPY-01: preserve Burkeman’s actual admission without an authoring aside.')
change('part-18-passage-09', 'en', '; readers encounter a proposed practice rather than testimony from an author who has completed his transformation.', '.', 'FW-COPY-01')

rewrite('part-19-passage-02',
'В послесловии Беркман прямо связывает всю книгу с отказом от надежды: когда-нибудь удовлетворить все требования, избавиться от болезненных переживаний и стать полновластным хозяином жизни. У экологического активиста Деррика Дженсена и буддийской учительницы Пемы Чодрон он находит объяснение освобождающей стороны этого отказа. Ожидание, что внешняя сила или само будущее всё исправит, может отнимать способность действовать сейчас. Потери уже произошли, мир не станет полностью безопасным, времени на всё не будет. Признание этого, в логике автора, позволяет перестать защищать мечту о полной надёжности и заняться тем, на что действительно можно повлиять. Оставшиеся возможности не обесцениваются: конкретное улучшение имеет смысл и без обещания, что вся история закончится благополучно.',
'In the afterword Burkeman explicitly connects the whole book with relinquishing hope: the hope of eventually meeting every demand, escaping painful experiences and becoming life’s complete master. In environmental activist Derrick Jensen and Buddhist teacher Pema Chödrön, he finds an explanation of this relinquishment’s liberating side. Waiting for an outside force, or the future itself, to fix everything can remove the ability to act now. Losses have already happened; the world will not become entirely safe; there will not be time for everything. In the author’s reasoning, acknowledging this lets us stop defending the dream of complete security and attend to what we can actually influence. Remaining possibilities retain value: a concrete improvement matters without a promise that the whole story will end well.',
'FW-MEAN-04: restore the afterword’s explicit connection between the whole book and relinquishing hope of complete control, rather than first reassuring the reader that not every hope is meant; content15 P005–014. Preserve agency and the value of remaining possibilities.')

repairs = []
for screen in data['screens']:
    sid = screen['id']
    if sid not in reasons:
        continue
    item = {'screen': sid, 'reasons': list(dict.fromkeys(reasons[sid])), 'languages': {}}
    for language in ['ru', 'en']:
        key = sid, language
        if key not in planned:
            continue
        before = plain(screen['copy'][language]['body'])
        after = planned[key]
        assert before != after and '\n\n' not in after
        item['languages'][language] = {'before': before, 'after': after}
    repairs.append(item)

for language in ['ru', 'en']:
    path = H / f'draft.{language}.md'
    text = path.read_text()
    for item in repairs:
        pair = item['languages'][language]
        assert text.count(pair['before']) == 1, item['screen']
        text = text.replace(pair['before'], pair['after'])
    (R / f'planned-draft.{language}.md').write_text(text)
for language in ['ru', 'en']:
    (H / f'draft.{language}.md').write_text((R / f'planned-draft.{language}.md').read_text())

# The new Brown outcome explicitly uses paragraph18, which was personally read.
path = H / 'compile.py'
text = path.read_text()
old = '[C(10,12,17)],[C(10,18,18),C(11,3,3)]'
assert text.count(old) == 1
path.write_text(text.replace(old, '[C(10,12,18)],[C(10,18,18),C(11,3,3)]'))
(R / 'repairs.json').write_text(json.dumps(repairs, ensure_ascii=False, indent=2) + '\n')
print('Applied draft repairs:', len(repairs), 'pairs; body alone is not yet rebuilt or accepted.')

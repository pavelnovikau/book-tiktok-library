# -*- coding: utf-8 -*-
"""Segment the already-written original prose; never reconstruct source text."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parent
draft = (ROOT / 'argument-draft-pass2.md').read_text()
trims = [
    (' Важна возможность самому освоить переживание; это авторское наблюдение, а не предлагаемое здесь упражнение с ребёнком.', ' Важна возможность самому освоить переживание.'),
    (" The opportunity to master the experience oneself matters; this is the author's observation, not an exercise proposed here for a child.", ' The opportunity to master the experience oneself matters.'),
    (' В этом пересказе сохранена логика урока, но не воспроизведена полная физическая инструкция для его выполнения.', ''),
    (" This account retains the lesson's logic without reproducing a complete physical instruction for performing it.", ''),
    (' Это пример предполагаемого переноса обучения, а не инструкция читателю брать топор или вставать на стул.', ' Это конкретный пример предполагаемого переноса обучения.'),
    (' This illustrates the proposed transfer of learning; it is not an instruction to the reader to take up an axe or climb onto a chair.', ' This is a concrete example of the proposed transfer of learning.'),
]
for old, new in trims:
    draft = draft.replace(old, new)
(ROOT / 'argument-draft-pass2.md').write_text(draft)
ru = draft.split('## RU\n\n')[1].split('\n\n## EN')[0].strip().split('\n\n')
en = draft.split('## EN\n\n')[1].strip().split('\n\n')
assert len(ru) == len(en) == 20

specs = [
    ('capacity-and-use', 1, 'Способность и действие', 'Capacity and action', [1]),
    ('unwritten-letter', 2, 'Ненаписанное письмо', 'The unwritten letter', [1]),
    ('rousseau-learning', 3, 'Как Руссо учился читать', 'How Rousseau learned to read', [1]),
    ('divided-action', 1, 'Действие, разделённое надвое', 'An action divided', [1]),
    ('cross-motivation', 1, 'Что делает второй мотив', 'What the second motive does', [1, 2, 3]),
    ('child-learning', 2, 'Ребёнок осваивает движение', 'A child learns the movement', [1]),
    ('acture', 1, 'Осанка как способ действия', 'Posture as a manner of acting', [2]),
    ('opposing-contractions', 2, 'Два встречных усилия', 'Two opposing efforts', [2]),
    ('four-qualities', 1, 'Как различить способы действия', 'Distinguishing ways of acting', [3, 4]),
    ('head-to-sitting', 1, 'От подъёма головы к сидению', 'From lifting the head to sitting', [3]),
    ('discrimination', 2, 'Заметить меньшую разницу', 'Noticing smaller differences', [2, 3]),
    ('breath-and-return', 1, 'Дыхание и обратный путь', 'Breathing and the return path', [3]),
    ('during-the-action', 2, 'Проверка по ходу движения', 'Checking during the movement', [2, 3]),
    ('anticipating-movement', 3, 'Представить, затем выполнить', 'Anticipate, then carry out', [3]),
    ('graded-experience', 2, 'Как устроено обучение', 'How learning is arranged', [3]),
    ('pelvic-support', 2, 'Таз, опора и движение', 'Pelvis, support and movement', [3]),
    ('transfer-example', 3, 'От одного движения к другому', 'From one movement to another', [3]),
    ('sexuality-and-limits', 3, 'Предположение о переносе', 'The proposed transfer', [3, 5]),
    ('relearning', 1, 'Что меняет переобучение', 'What relearning changes', [2, 3]),
    ('final', 1, 'Возможность действовать иначе', 'The possibility of acting differently', [2, 3]),
]
section_ru = ['Способность'] * 3 + ['Принуждение'] * 3 + ['Тело и действие'] * 2 + ['Переобучение'] * 7 + ['Перенос'] * 3 + ['Переобучение', 'Завершение']
section_en = ['Capacity'] * 3 + ['Compulsion'] * 3 + ['Body and action'] * 2 + ['Relearning'] * 7 + ['Transfer'] * 3 + ['Relearning', 'Closing']
sources = [
    {
        'id': 1,
        'title': 'Moshe Feldenkrais — El poder del yo, Paidós, 2015: official sample',
        'url': 'https://proassetspdlcom.cdnstatics2.com/usuaris/libros_contenido/arxius/30/29550_El_poder_del_yo.pdf',
        'role': 'book',
        'note': {
            'ru': 'Официальный испанский фрагмент The Potent Self: главы 1–2, печатные с. 53–66. Не полное издание; RU/EN — самостоятельный пересказ, не официальный перевод.',
            'en': 'Official Spanish sample of The Potent Self: Chapters 1–2, printed pp. 53–66. Not a complete edition; RU/EN are original-word accounts, not official translations.',
        },
    },
    {
        'id': 2,
        'title': 'Tiffany Sankary — Feldenkrais Illustrated, Chapter 14: Emotions & Posture',
        'url': 'https://www.movementandcreativity.com/blog/podcast/2019/1/31/chapter-14-emotions-posture-feldenkrais-illustrated',
        'role': 'primary',
        'note': {
            'ru': 'Авторские цитаты из The Potent Self с номерами страниц и явным разрешением Frog Books / Somatic Resources на перепечатку. Связь эмоций и мышечного действия, acture, встречные сокращения, переобучение. Другие цитируемые на странице книги не использованы как текст The Potent Self.',
            'en': 'Quotations from The Potent Self with page references and explicit reprint permission from Frog Books / Somatic Resources. Emotional and muscular organization, acture, opposing contractions and relearning. Other books quoted on the page were not treated as The Potent Self.',
        },
    },
    {
        'id': 3,
        'title': 'Mark Reese — Moshe Feldenkrais: A Life in Movement, Chapter 6',
        'url': 'https://feldenkraisinstitute.com.au/wp-content/uploads/2018/08/REESE-2015-Moshe-Feldenkrais-A-Life-in-Movement-Ch.6.pdf',
        'role': 'review',
        'note': {
            'ru': 'Подробный разбор именно The Potent Self, печатные с. 280–287 и 296: уроки глав 13, 15, 17 и авторские цитаты. Вторичный источник и переданные им первичные фрагменты разграничены; полный текст уроков и все случаи не прочитаны.',
            'en': 'Detailed discussion specifically of The Potent Self, printed pp. 280–287 and 296: lessons in Chapters 13, 15 and 17, with author quotations. Secondary exposition is distinguished from the primary passages it quotes; complete lessons and all cases were not read.',
        },
    },
    {
        'id': 4,
        'title': 'Nicolette de Saint-Amour — Learning To Learn, Feldenkrais Guild',
        'url': 'https://feldenkrais.com/learning-to-learn-a-lifes-journey-by-nicolette-de-saint-amour/',
        'role': 'reference',
        'note': {
            'ru': 'Использован только фрагмент, явно отнесённый к главе The Potent Self о правильной осанке: четыре признака координации. Дальнейшие советы из Learn to Learn и современные толкования не выданы за процедуру этой книги.',
            'en': "Only the section explicitly attributed to The Potent Self's chapter on correct posture is used: four qualities of coordination. Later advice from Learn to Learn and modern interpretations are not passed off as this book's procedure.",
        },
    },
    {
        'id': 5,
        'title': 'North Atlantic Books / Penguin Random House — The Potent Self, 2002',
        'url': 'https://www.penguinrandomhouse.com/books/48695/the-potent-self-by-moshe-feldenkrais-foreword-by-mark-reese/',
        'role': 'publisher',
        'note': {
            'ru': 'Название, автор, предисловие Марка Риза, ISBN 9781583940686, 288 страниц; издатель подтверждает место сексуальности в теме книги. Это описание, не основной текст и не доказательство эффективности.',
            'en': 'Title, author, Mark Reese foreword, ISBN 9781583940686, 288 pages; the publisher confirms sexuality as part of the subject. A description, not main text or efficacy evidence.',
        },
    },
]
data = {
    'schemaVersion': 2,
    'slug': 'the-potent-self',
    'title': {'ru': 'The Potent Self', 'en': 'The Potent Self'},
    'author': {'ru': 'Моше Фельденкрайз', 'en': 'Moshe Feldenkrais'},
    'description': {
        'ru': 'Моше Фельденкрайз: от конкурирующих мотивов к переобучению действию. Краткое изложение по выбранным авторским фрагментам и подробному разбору Марка Риза.',
        'en': "Moshe Feldenkrais: from competing motivations to relearning action. A concise account based on selected author passages and Mark Reese's detailed discussion.",
    },
    'defaultLanguage': 'ru',
    'defaultTheme': 'dark',
    'defaultMode': 'essential',
    'contentMode': 'explanatory',
    'spoilerPolicy': 'not-applicable',
    'methodNote': {
        'ru': 'Самостоятельное краткое RU/EN изложение основного аргумента и описанных в книге процедур. Прочитаны официальный испанский фрагмент Paidós (с. 53–66), авторские цитаты с разрешением на перепечатку у Tiffany Sankary и подробный разбор Марка Риза (с. 280–287, 296). Полное издание и все случаи не прочитаны. Уроки описаны в третьем лице, без полной инструкции для выполнения. Физиология и перенос в интимную жизнь переданы как авторские предположения; клиническая эффективность не проверялась. Это не официальный перевод.',
        'en': "An original-word RU/EN condensation of the central argument and the book's described learning procedures. Consulted: the official Paidós Spanish sample (pp. 53–66), author quotations reprinted with permission by Tiffany Sankary, and Mark Reese's detailed account (pp. 280–287, 296). A complete edition and all cases were not read. Lessons are described in the third person without complete instructions for performing them. Physiology and transfer to intimate life remain attributed proposals; clinical efficacy was not assessed. Not an official translation.",
    },
    'sources': sources,
    'media': {
        'reading-cover': {
            'file': './cover-pass2.svg',
            'alt': {'ru': 'Типографская обложка: The Potent Self, Moshe Feldenkrais', 'en': 'Typographic cover: The Potent Self, Moshe Feldenkrais'},
            'credit': {'ru': 'Обложка этого конспекта; не воспроизведение обложки издания.', 'en': 'Cover for this reading account; not a reproduction of the published cover.'},
        },
    },
    'screens': [{
        'id': 'cover', 'level': 1, 'type': 'cover', 'sources': [5], 'media': 'reading-cover',
        'copy': {
            'ru': {
                'section': 'Моше Фельденкрайз', 'title': 'The Potent Self', 'subtitle': 'Спонтанность и принуждение',
                'body': '<p>Как конкурирующие мотивы входят в движение — и что Фельденкрайз понимает под переобучением.</p><p class="muted">Краткое изложение по выбранным авторским фрагментам и разбору Марка Риза. Описание уроков, не инструкция для выполнения.</p>',
            },
            'en': {
                'section': 'Moshe Feldenkrais', 'title': 'The Potent Self', 'subtitle': 'Spontaneity and Compulsion',
                'body': "<p>How competing motivations enter movement, and what Feldenkrais means by relearning.</p><p class=\"muted\">A concise account from selected author passages and Mark Reese's discussion. Lessons are described, not supplied as instructions for performance.</p>",
            },
        },
    }],
}
for i, (sid, level, title_ru, title_en, refs) in enumerate(specs):
    screen = {
        'id': sid, 'level': level, 'claimType': 'synthesis' if sid == 'final' else 'book', 'sources': refs,
        'copy': {
            'ru': {'section': section_ru[i], 'title': title_ru, 'body': '<p>' + html.escape(ru[i], quote=False) + '</p>'},
            'en': {'section': section_en[i], 'title': title_en, 'body': '<p>' + html.escape(en[i], quote=False) + '</p>'},
        },
    }
    if sid == 'final':
        screen['final'] = True
    data['screens'].append(screen)
data['targetModes'] = {mode: sum(s['level'] <= level for s in data['screens']) for mode, level in [('essential', 1), ('core', 2), ('deep', 3)]}
(ROOT / 'story-data.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print('Derived cumulative counts:', data['targetModes'])

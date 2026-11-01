# coding: utf-8
from pathlib import Path
import copy
import html
import json
import re

R = Path(__file__).resolve().parent
H = R.parent
load = lambda p: json.loads(p.read_text())
dump = lambda p, d: p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')

def parse(lang):
    units = []
    section = None
    for paragraph in (H / f'draft.{lang}.md').read_text().split('\n\n'):
        paragraph = paragraph.strip()
        if paragraph.startswith('## '):
            section = paragraph[3:]
        elif paragraph.startswith('### '):
            units.append({'title': paragraph[4:], 'section': section, 'paragraphs': []})
        elif paragraph and not paragraph.startswith('# '):
            units[-1]['paragraphs'].append(paragraph)
    assert len(units) == 64
    assert all(len(u['paragraphs']) == (5 if i == 48 else 3) for i, u in enumerate(units, 1))
    return units

draft = {lang: parse(lang) for lang in ['ru', 'en']}
data = load(R / 'input-story-data.json')
old = {s['id']: s for s in data['screens']}
mapping = load(R / 'input-coverage-map.json')
screens = [copy.deepcopy(old['cover'])]
offset = 1
for row in mapping['units']:
    unit = row['unit']
    first = old[row['screens'][0]]
    if unit == 48:
        groups = [([0, 1], row['screens'][0]), ([2, 3], 'market-in-the-self'), ([4], row['screens'][1])]
    elif unit == 64:
        groups = [([0, 1, 2], 'final')]
    else:
        groups = [([0, 1], row['screens'][0]), ([2], row['screens'][1])]
    row['screens'] = [sid for _, sid in groups]
    for indices, sid in groups:
        screen = copy.deepcopy(old.get(sid, first))
        screen.update(id=sid, draftParagraphs=[offset + j for j in indices])
        if sid == 'market-in-the-self':
            screen['primaryLocators'] = [{'file': 'OPS/ch1-17.xhtml', 'start': 50, 'end': 61}]
        for lang in ['ru', 'en']:
            if sid == 'market-in-the-self':
                screen['copy'][lang]['title'] = {'ru': 'Рынок внутри человека', 'en': 'The market within the self'}[lang]
            screen['copy'][lang]['body'] = ''.join('<p>' + html.escape(draft[lang][unit - 1]['paragraphs'][j], quote=False) + '</p>' for j in indices)
        if sid == 'late-doubt':
            screen['sources'] = [1, 2]
        screens.append(screen)
    offset += len(draft['ru'][unit - 1]['paragraphs'])
assert offset - 1 == 194
assert len(screens) == len({s['id'] for s in screens}) == 129
data['screens'] = screens
data['targetModes'] = {mode: sum(s['level'] <= level for s in screens) for mode, level in [('essential', 1), ('core', 2), ('deep', 3)]}
assert data['targetModes'] == {'essential': 49, 'core': 93, 'deep': 129}
data['sources'].append({
    'id': 2, 'title': 'Harper’s Magazine — The new narcissism, by Peter Marin (bibliographic entry)',
    'url': 'https://harpers.org/tag/cults/', 'role': 'publisher',
    'note': {
        'ru': 'Индекс издателя подтверждает имя Питер Марин. В предоставленном русском извлечении напечатано «Мартин»; здесь имя нормализовано. Проверена только библиографическая запись. Полная статья не прочитана: прямой доступ требовал оплаты.',
        'en': 'The publisher index confirms Peter Marin’s byline. The supplied Russian extraction prints “Martin”; the name is normalised here. Only bibliographic metadata was checked. The complete article was not read: direct access required payment.'
    }
})
mapping['rootRevision'] = {
    'status': 'personal-review-in-progress',
    'unit24': 'Concrete Coulson-attributed convent outcome restored from OPS/ch1-10.xhtml P030.',
    'unit31': 'Marin byline normalised using publisher metadata only; source translation discrepancy and402 are disclosed.',
    'unit48': 'Five draft paragraphs; added two-paragraph market mechanism at a separate Essential screen. All five paragraphs are sequential original exposition.',
    'paragraphsPerLanguage': 194,
    'rootPersonalAcceptance': False
}
dump(H / 'story-data.json', data)
dump(H / 'coverage-map.json', mapping)
for lang in ['ru', 'en']:
    for mode, level in [('essential', 1), ('core', 2), ('deep', 3)]:
        pieces = [f'# {data["title"][lang]} — {mode}']
        for screen in screens:
            if screen['level'] <= level:
                c = screen['copy'][lang]
                body = html.unescape(re.sub(r'</p>\s*<p>', '\n\n', c['body']).replace('<p>', '').replace('</p>', ''))
                pieces.append(f'<!-- {screen["id"]} | level={screen["level"]} -->\n\n## {c["title"]}\n\n' + body)
        (H / f'{mode}.{lang}.md').write_text('\n\n'.join(pieces) + '\n')
print(json.dumps({'counts': data['targetModes'], 'paragraphsPerLanguage': 194, 'publicSources': len(data['sources'])}))

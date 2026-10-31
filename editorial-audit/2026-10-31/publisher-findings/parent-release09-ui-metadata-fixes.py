"""Apply CM-01/02 and explicit nonfiction resume-depth labels in a release repo.

Run after the maintained shell has been synchronized. No book-body changes.
Requires the expected old wording or the already-corrected wording; idempotent.
"""
import hashlib
import html
import json
from pathlib import Path
import re
import sys

PATTERN = r'(<script\b(?=[^>]*\bid="book-tiktok-data")[^>]*>)([\s\S]*?)(</script>)'
OLD_DESCRIPTION = {
    'ru': 'Джонас получает необычное назначение и начинает узнавать мир, которого его община не помнит. Краткий рассказ по первому роману Лоис Лоури.',
    'en': 'An unusual Assignment leads Jonas into a world his community no longer remembers. A concise retelling of Lois Lowry’s first novel.',
}
NEW_DESCRIPTION = {
    'ru': 'Джонас получает необычное назначение и начинает узнавать мир, которого его община не помнит. Краткий рассказ по первому роману цикла Лоис Лоури.',
    'en': 'An unusual Assignment leads Jonas into a world his community no longer remembers. A concise retelling of the first novel in Lois Lowry’s Giver Quartet.',
}


def fix_description(description):
    for language in ['ru', 'en']:
        assert description[language] in [OLD_DESCRIPTION[language], NEW_DESCRIPTION[language]], (language, description[language])
        description[language] = NEW_DESCRIPTION[language]


def fix_reader_description(value):
    match = re.search(PATTERN, value)
    assert match
    data = json.loads(match[2])
    original = json.loads(match[2])
    fix_description(data['description'])
    assert data['screens'] == original['screens'] and data['sources'] == original['sources']
    if data == original:
        result = value
    else:
        result = re.sub(PATTERN, lambda m: m[1] + json.dumps(data, ensure_ascii=False, indent=2) + m[3], value, count=1)
    meta = re.search(r'(<meta\s+name="description"\s+content=")([^"]*)(")', result)
    assert meta and html.unescape(meta[2]) in [OLD_DESCRIPTION['ru'], NEW_DESCRIPTION['ru']]
    result = result[:meta.start(2)] + html.escape(NEW_DESCRIPTION['ru'], quote=True) + result[meta.end(2):]
    return result


def explicit_resume_depth(value):
    if 'const resumeRequiresDepth = remembered && remembered.level > levels[state.mode];' in value:
        assert "modeLabel(requiredMode(remembered.level))" in value
        return value
    pattern = r'(?m)^(\s*)const primaryLabel = (resumeHasEnding \?[^\n]+);$'
    matches = list(re.finditer(pattern, value))
    assert len(matches) == 1
    match = matches[0]
    expression = match[2]
    assert expression.count(': remembered ?') == 1
    expression = expression.replace(': remembered ?', ": resumeRequiresDepth ? (state.language === 'ru' ? 'Продолжить: ' : 'Continue: ') + modeLabel(requiredMode(remembered.level)) : remembered ?", 1)
    replacement = match[1] + 'const resumeRequiresDepth = remembered && remembered.level > levels[state.mode];\n' + match[1] + 'const primaryLabel = ' + expression + ';'
    return value[:match.start()] + replacement + value[match.end():]


def apply(release_root):
    release_root = Path(release_root)
    catalogue_path = release_root / 'books.json'
    catalogue = json.loads(catalogue_path.read_text())
    records = {b['slug']: b for b in catalogue['books']}
    fix_description(records['the-giver']['description'])
    aliases = records['awareness-through-movement'].get('searchAliases') or []
    assert isinstance(aliases, list) and all(isinstance(x, str) for x in aliases)
    if 'Сознавание через движение' not in aliases:
        records['awareness-through-movement']['searchAliases'] = aliases + ['Сознавание через движение']
    planned = {catalogue_path: json.dumps(catalogue, ensure_ascii=False, indent=2) + '\n'}
    giver = release_root / 'the-giver.html'
    planned[giver] = fix_reader_description(giver.read_text())
    for slug in ['skin-in-the-game', 'mindfulness']:
        target = release_root / (slug + '.html')
        planned[target] = explicit_resume_depth(target.read_text())
    potent = release_root / 'the-potent-self.html'
    if potent.exists():
        text = potent.read_text()
        match = re.search(PATTERN, text)
        assert match
        data = json.loads(match[2])
        before_screens = data['screens']
        label = data['modes']['essential']['minutes']['ru']
        assert label in ['4 минут', '4 минуты']
        if label == '4 минут':
            data['modes']['essential']['minutes']['ru'] = '4 минуты'
            text = re.sub(PATTERN, lambda m: m[1] + json.dumps(data, ensure_ascii=False, indent=2) + m[3], text, count=1)
        assert data['screens'] == before_screens
        planned[potent] = text
    result = []
    for target, text in planned.items():
        before = target.read_bytes()
        after = text.encode()
        if before != after:
            target.write_bytes(after)
        result.append({'path': str(target.relative_to(release_root)), 'changed': before != after,
                       'beforeSha256': hashlib.sha256(before).hexdigest(),
                       'afterSha256': hashlib.sha256(after).hexdigest()})
    return result


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'Usage: python3 parent-release09-ui-metadata-fixes.py <prepared-release-repo>'
    print(json.dumps({'changes': apply(sys.argv[1]), 'scope': 'CM-01/02; MIG-01 explicit destination labels, no nonfiction confirmation dialog or body change.'}, ensure_ascii=False, indent=2))

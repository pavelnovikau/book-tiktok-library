"""Developer font audit. Requires fontTools with WOFF2 support; no network."""
import hashlib
import json
from pathlib import Path
from fontTools.ttLib import TTFont

root = Path(__file__).resolve().parents[1]
fonts = root / 'skills/book-tiktok/assets/fonts'
russian = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
specs = [
    ('Geist-Variable.woff2', 'a369fcf5628ea2aa4e1b9e2ec6a5b3624e365bda588e1f0f2f12b564f728fbb8', True, 'LICENSE.txt'),
    ('GeistSerif-Regular.woff2', 'd11c9077e61bda553e2eea121409c584504319e08f972d11e0a38ed4b14de398', False, 'GeistSerif-LICENSE.txt'),
    ('SourceSerif4-Regular.woff2', '6b053e98f0838afe81f3e784727be4583a7c13bb42f198dc5202ecffee0aaee0', True, 'SourceSerif4-LICENSE.md'),
]
result = []
for file, expected, covers_ru, license_file in specs:
    font = TTFont(fonts / file)
    sha = hashlib.sha256((fonts / file).read_bytes()).hexdigest()
    assert sha == expected, file + ': font changed; re-audit before updating digest'
    cmap = font.getBestCmap()
    missing = ''.join(c for c in russian if ord(c) not in cmap)
    assert (not missing) if covers_ru else len(missing) == 66, file + ': unexpected RU coverage'
    assert all(ord(c) in cmap for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'), file
    license_text = (fonts / license_file).read_text()
    assert 'Copyright' in license_text and 'SIL OPEN FONT LICENSE Version 1.1' in license_text
    if 'Regular' in file:
        assert 'fvar' not in font and font['OS/2'].usWeightClass == 400
    result.append(dict(file=file, sha256=sha, bytes=(fonts/file).stat().st_size,
                       family=font['name'].getDebugName(1), version=font['name'].getDebugName(5),
                       encodedCharacters=len(cmap), missingRussian=missing,
                       weight=font['OS/2'].usWeightClass,
                       axes=[dict(tag=a.axisTag, minimum=a.minValue, maximum=a.maxValue) for a in font['fvar'].axes] if 'fvar' in font else [],
                       license=license_file))
assert (root/'fonts/Geist-Variable.woff2').read_bytes() == (fonts/'Geist-Variable.woff2').read_bytes()
print(json.dumps(result, ensure_ascii=False, indent=2))

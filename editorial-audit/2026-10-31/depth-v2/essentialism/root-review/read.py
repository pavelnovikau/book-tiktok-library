from pathlib import Path
import datetime
import hashlib
import html
import json
import re
import sys

R = Path(__file__).resolve().parent
H = R.parent
SOURCE = Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-8-private/essentialism-edition.json')
load = lambda p: json.loads(p.read_text())
dump = lambda p, d: p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
digest = lambda b: hashlib.sha256(b).hexdigest()
stamp = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()

def plain(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s.replace('</p>', '\n\n'))).strip()

kind = sys.argv[1]
if kind == 'screens':
    start, end = map(int, sys.argv[2:4])
    data = load(H / 'story-data.json')['screens'][start:end]
    offered = {'kind': kind, 'start': start, 'end': end, 'ids': [s['id'] for s in data], 'corpusSliceSha256': digest(json.dumps(data, ensure_ascii=False, sort_keys=True).encode())}
    dump(R / 'offered.json', offered)
    for index, screen in enumerate(data, start):
        print(f"\n[{index} {screen['id']} L{screen['level']}]")
        for lang in ['ru', 'en']:
            c = screen['copy'][lang]
            print(lang.upper(), c.get('section', ''), '|', c.get('title', ''), '|', c.get('subtitle', ''))
            print(plain(c.get('body', '')))
elif kind in ['changed', 'route', 'core-additions']:
    corpus = load(H / 'story-data.json')['screens']
    if kind == 'changed':
        ids = {x['screen'] for x in load(R / 'repairs.json')}
        if len(sys.argv) > 2:
            ids &= set(sys.argv[2:])
        selected = [s for s in corpus if s['id'] in ids]
        start, end = 0, len(selected)
        full_route = corpus
    elif kind == 'route':
        mode = sys.argv[2]
        start, end = map(int, sys.argv[3:5])
        full_route = [s for s in corpus if s['level'] <= {'essential': 1, 'core': 2, 'deep': 3}[mode]]
        selected = full_route[start:end]
    else:
        start, end = map(int, sys.argv[2:4])
        full_route = [s for s in corpus if s['level'] <= 2]
        selected = [s for s in full_route if s['level'] == 2][start:end]
    offered = {'kind': kind, 'start': start, 'end': end, 'ids': [s['id'] for s in selected], 'corpusSliceSha256': digest(json.dumps(selected, ensure_ascii=False, sort_keys=True).encode())}
    dump(R / 'offered.json', offered)
    for screen in selected:
        index = next(i for i, s in enumerate(full_route) if s['id'] == screen['id'])
        print(f"\n[{index} {screen['id']} L{screen['level']}]")
        for lang in ['ru', 'en']:
            if kind == 'core-additions':
                before = full_route[index - 1] if index else None
                after = full_route[index + 1] if index + 1 < len(full_route) else None
                if before:
                    print('PREVIOUS', before['id'], re.split(r'(?<=[.!?])\s+', plain(before['copy'][lang].get('body', '')))[-1])
            c = screen['copy'][lang]
            print(lang.upper(), c.get('section', ''), '|', c.get('title', ''), '|', c.get('subtitle', ''))
            print(plain(c.get('body', '')))
            if kind == 'core-additions' and after:
                print('NEXT', after['id'], re.split(r'(?<=[.!?])\s+', plain(after['copy'][lang].get('body', '')))[0])
elif kind == 'primary':
    file = sys.argv[2]
    start, end = map(int, sys.argv[3:5])
    data = load(SOURCE)
    record = next(r for r in data if r['file'] == file)
    paragraphs = record['paragraphs'][start - 1:end]
    assert len(paragraphs) == end - start + 1
    offered = {'kind': kind, 'file': file, 'start': start, 'end': end, 'indexBase': 1, 'inclusive': True, 'sourceSha256': digest(SOURCE.read_bytes()), 'rangeSha256': digest(json.dumps(paragraphs, ensure_ascii=False, separators=(',', ':')).encode())}
    dump(R / 'offered.json', offered)
    print(json.dumps(offered, ensure_ascii=False))
    for index, paragraph in enumerate(paragraphs, start):
        print(f'[{file} P{index:03d}] {paragraph}\n')
elif kind == 'primary-plan':
    index = int(sys.argv[2])
    plan = load(R / 'primary-selection-plan.json')
    data = {r['file']: r for r in load(SOURCE)}
    groups = []
    current = []
    words = 0
    for row in plan['ranges']:
        if current and words + row['wordsWhitespace'] > 1700:
            groups.append(current)
            current = []
            words = 0
        current.append(row)
        words += row['wordsWhitespace']
    if current:
        groups.append(current)
    ranges = []
    print('PRIMARY GROUP', index, 'OF', len(groups))
    for row in groups[index]:
        file, start, end = row['file'], row['start'], row['end']
        paragraphs = data[file]['paragraphs'][start - 1:end]
        ranges.append({'kind': 'primary', 'file': file, 'start': start, 'end': end, 'indexBase': 1, 'inclusive': True, 'sourceSha256': digest(SOURCE.read_bytes()), 'rangeSha256': digest(json.dumps(paragraphs, ensure_ascii=False, separators=(',', ':')).encode())})
        print(json.dumps(ranges[-1], ensure_ascii=False))
        for pindex, paragraph in enumerate(paragraphs, start):
            print(f'[{file} P{pindex:03d}] {paragraph}\n')
    dump(R / 'offered.json', {'kind': 'primary-batch', 'group': index, 'ranges': ranges})
elif kind == 'ack':
    offered = load(R / 'offered.json')
    ledger = load(R / 'reading-ledger.json')
    offered.update(atUtc=stamp(), completeDisplayedRangePersonallyRead=True)
    key = {'screens': 'screenDisplays', 'changed': 'changedDisplays', 'route': 'routeDisplays', 'core-additions': 'coreAdditionDisplays'}.get(offered['kind'], 'primaryDisplays')
    ledger.setdefault(key, [])
    if offered['kind'] == 'primary-batch':
        ledger[key].extend({**r, 'atUtc': offered['atUtc'], 'completeDisplayedRangePersonallyRead': True, 'group': offered['group']} for r in offered['ranges'])
    else:
        ledger[key].append(offered)
    dump(R / 'reading-ledger.json', ledger)
    print('Acknowledged actual reading:', offered.get('ids', offered.get('file')))
else:
    raise ValueError(kind)

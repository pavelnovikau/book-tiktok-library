from pathlib import Path
import collections
import csv
import datetime
import hashlib
import json
import shutil
import subprocess

C = Path('/Users/pn/smartcat/_artifacts/book-tiktok-library')
P = Path('/Users/pn/.t3/checkouts/book-tiktok-library-release07-20261031')
rel = Path('editorial-audit/2026-10-31')
A = C / rel
slug = 'essentialism'
H = A / 'depth-v2' / slug
load = lambda p: json.loads(p.read_text())
dump = lambda p, d: p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=P, text=True).strip()
assert base == '91bad9ffa0ac09a9618b8139bd4613a33b712c6f'
assert not subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=P, text=True).strip()
ready = load(H / 'ready.json')
report = load(H / 'root-review/personal-review.json')
assert ready['rootPersonalAcceptance'] and ready['publicationAllowed'] and ready['bookContentPublicationAllowed']
assert not report['requiredOpenFindings']
assert len(ready['allArtifactHashes']) == 97
for name, row in ready['allArtifactHashes'].items():
    assert sha(Path(row['path'])) == row['sha256'], name
assert sha(H / 'root-review/personal-review.json') == ready['rootPersonalReviewSha256']
old = load(P / 'books.json')
cat = json.loads(json.dumps(old))
book = next(x for x in cat['books'] if x['slug'] == slug)
assert book['screenCount'] == 36
book['screenCount'] = 125
book['readingMinutes'] = {k: int(v['ru']['displayedLabel'].split()[0]) for k, v in report['metrics'].items()}
assert book['readingMinutes'] == {'essential': 21, 'core': 45, 'deep': 52}
assert all(x == y for x, y in zip(old['books'], cat['books']) if x['slug'] != slug)
assert len(cat['books']) == 58 and sum(x['screenCount'] for x in cat['books']) == 2826
shutil.copyfile(H / (slug + '.html'), P / (slug + '.html'))
dump(P / 'books.json', cat)

plan = load(A / 'depth-v2/PLAN.json')
plan['atUtc'] = stamp
for x in plan['books']:
    if x['slug'] == slug:
        x.update(status='root-personally-accepted-awaiting-publication', rootAcceptance=str(H / 'root-review/personal-review.json'), rootEntireRuEnDraftRead=True, rootAllNestedRoutesRead=True, rootRouteReadingMethod=report['personalReading']['routeReadingMethod'], rootCoverageMapCompared=True, rootKeyPrimaryPassagesChecked=True, rootOmissionsAndQualificationsReviewed=True, replacementPublicationAllowed=True, expandedCounts=report['counts'], acceptedHashes={n: sha(H / n) for n in ['story-data.json', slug + '.html']})
dump(A / 'depth-v2/PLAN.json', plan)
pub = load(A / 'publication-state.json')
pub['rootAcceptedNotYetPublished'] = [slug]
dump(A / 'publication-state.json', pub)
hold = load(A / 'publisher-findings/fiction-depth-publication-hold.json')
hold['atUtc'] = stamp
hold['rootAcceptedExceptions'][slug] = {'report': str(H / 'root-review/personal-review.json'), 'reportSha256': ready['rootPersonalReviewSha256'], 'htmlSha256': sha(H / (slug + '.html')), 'jsonSha256': sha(H / 'story-data.json')}
dump(A / 'publisher-findings/fiction-depth-publication-hold.json', hold)
dispatch = load(A / 'publisher-findings/release07-and-ten-worker-dispatch.json')
dispatch.update(atUtc=stamp, currentPublisher='root; personally accepted expanded Essentialism release', runtimeStatusPolled=False, assignmentCount=len(dispatch['workerAssignments']), assignmentNote='Essentialism personally accepted49/108/125 after complete bilingual retelling reading, all49Essential pairs and59Core additions with adjacent edges, the full247-line chapter/omission map and34actual primary ranges. Seven findings closed across13paired screens. Deep8749RU/10230EN noncover body words; UI52/50minutes. Source checking selective overall. Release pending; nine expanded versions live. Four Thousand Weeks, Selfie, Mindfulness, Monday Begins on Saturday and The Body Keeps the Score await root reading. Amphibian Man remains assigned; no runtime polling. Behave source coverage incomplete.62approved positions retain individual acceptance.')
dispatch['latestDepthCompleted'][slug] = 'Root personally accepted49/108/125; release pending'
dump(A / 'publisher-findings/release07-and-ten-worker-dispatch.json', dispatch)
status = load(A / 'library-status.json')
status['asOfUtc'] = stamp
stages = {x['slug']: x for x in plan['books']}
for x in status['books']:
    stage = stages[x['slug']]['status']
    x['maximumDepthStage'] = {'needs-root-depth-and-source-assessment': 'awaiting-expanded-work', 'expanded-source-map-incomplete': 'source-map-incomplete'}.get(stage, stage)
    x['rootExpandedTextAccepted'] = bool(stages[x['slug']]['rootAcceptance'])
    if x['slug'] == slug:
        x['depthReviewStatus'] = 'root-accepted-expanded'
status['maximumDepthStages'] = dict(collections.Counter(x['maximumDepthStage'] for x in status['books']))
assert sum(status['maximumDepthStages'].values()) == 62
status['basis'] = '62 approved positions. Verified production remains PR45,58books/2737screens until this release is merged/verified. Historical factual stages are distinct from root maximum-depth acceptance.'
dump(A / 'library-status.json', status)
labels = {'awaiting-expanded-work': 'Awaits expanded work', 'source-map-incomplete': 'Primary-source coverage incomplete', 'expanded-writing-assigned': 'Expanded version assigned', 'root-accepted-and-live': 'Personally accepted and live', 'root-personally-accepted-awaiting-publication': 'Personally accepted; release pending', 'expanded-awaiting-root-personal-reading': 'Candidate awaits personal root reading'}
md = '# Library depth status\n\nUpdated ' + stamp + '.62approved positions. Nine personally accepted expanded books live; Essentialism accepted, release pending. Five completed candidates await root reading. Amphibian Man remains assigned; no runtime polling.\n\n| Current depth stage | Count |\n|---|---:|\n'
md += ''.join('| ' + labels.get(k, k) + ' | ' + str(v) + ' |\n' for k, v in status['maximumDepthStages'].items())
md += '\n| Book | Author | Current depth stage |\n|---|---|---|\n'
md += ''.join('| ' + x['title'] + ' | ' + x['author'] + ' | ' + labels.get(x['maximumDepthStage'], x['maximumDepthStage']) + ' |\n' for x in status['books'])
(A / 'library-status.md').write_text(md)
p = A / 'library-status.csv'
with p.open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f); fields = reader.fieldnames; rows = list(reader)
by = {x['slug']: x for x in status['books']}
for x in rows:
    x.update(maximumDepthStage=by[x['slug']]['maximumDepthStage'], rootExpandedTextAccepted=str(by[x['slug']]['rootExpandedTextAccepted']).lower())
with p.open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n'); writer.writeheader(); writer.writerows(rows)
intake = load(A / f'depth-v2/root-intake/{slug}.json')
intake.update(stage='root-personally-accepted-awaiting-publication', rootPersonalAcceptance=True, publicationAllowed=True, rootPersonalReview=str(H / 'root-review/personal-review.json'), rootPersonalReviewSha256=ready['rootPersonalReviewSha256'], readySha256=sha(H / 'ready.json'), counts=report['counts'], bodyWords={'ru': 8749, 'en': 10230}, hashBindingsVerified=len(ready['allArtifactHashes']), exactAcceptedHashes=report['exactContentHashes'], scope='Root personally accepted this exact expanded version after complete bilingual retelling reading, shorter-route continuity, whole coverage map and selected primary checks. Publication pending.')
dump(A / f'depth-v2/root-intake/{slug}.json', intake)
note = 'Essentialism personally accepted49/108/125 after complete bilingual retelling reading, all49Essential pairs and59Core additions with adjacent edges, the full247-line chapter/omission map and34actual primary ranges. Seven findings closed across13paired screens. Deep8749RU/10230EN noncover body words; UI52/50minutes. Source checking selective overall. Release pending; nine expanded versions live. Four Thousand Weeks, Selfie, Mindfulness, Monday Begins on Saturday and The Body Keeps the Score await root reading. Amphibian Man remains assigned; no runtime polling. Behave source coverage incomplete.62approved positions retain individual acceptance.'
(A / 'depth-v2/PLAN.md').write_text((A / 'depth-v2/PLAN.md').read_text() + '\n\nCurrent ' + stamp + ': ' + note + '\n')
(C / 'NEXT_STEPS.md').write_text('# Current personal review queue —2026-11-01\n\n' + note + '\n\nThis block supersedes historical states below.\n\n---\n\n' + (C / 'NEXT_STEPS.md').read_text())
(C / 'README.md').write_text((C / 'README.md').read_text().replace('# Book TikTok Library\n', '# Book TikTok Library\n\nCurrent2026-11-01: ' + note + ' This statement supersedes historical notes below.\n', 1))
receipt = {'atUtc': stamp, 'slug': slug, 'baseMerge': base, 'rootReview': str(H / 'root-review/personal-review.json'), 'rootReviewSha256': ready['rootPersonalReviewSha256'], 'acceptedHashes': {n: sha(H / n) for n in ['story-data.json', slug + '.html']}, 'counts': report['counts'], 'candidateBindingsVerified': len(ready['allArtifactHashes']), 'scope': 'Only one personally accepted expanded reader plus catalogue count/times;57 other catalogue entries and58 other root HTML unchanged. Evidence excluded from public build.', 'allOtherNewBookContentHeld': True}
dump(A / 'publisher-findings/expanded-depth-10-intake.json', receipt)
shutil.copytree(H, P / rel / 'depth-v2' / slug, dirs_exist_ok=True)
names = ['depth-v2/PLAN.json', 'depth-v2/PLAN.md', 'depth-v2/root-intake/' + slug + '.json', 'depth-v2/root-intake/the-body-keeps-the-score.json', 'depth-v2/root-intake/monday-begins-on-saturday.json', 'publication-state.json', 'production-catalogue.json', 'library-status.json', 'library-status.csv', 'library-status.md', 'publisher-findings/fiction-depth-publication-hold.json', 'publisher-findings/release07-and-ten-worker-dispatch.json']
for name in names:
    (P / rel / name).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(A / name, P / rel / name)
for name in ['NEXT_STEPS.md', 'README.md', 'LOG.md']:
    shutil.copyfile(C / name, P / name)
for pattern in ['expanded-depth-09-*', 'expanded-depth-10-*', 'amphibian-expanded-*']:
    for q in (A / 'publisher-findings').glob(pattern):
        if q.is_file():
            shutil.copyfile(q, P / rel / 'publisher-findings' / q.name)
print(json.dumps({'base': base, 'intendedBooks': 58, 'intendedScreens': 2826, 'bindings': len(ready['allArtifactHashes']), 'maximumDepthStages': status['maximumDepthStages']}))

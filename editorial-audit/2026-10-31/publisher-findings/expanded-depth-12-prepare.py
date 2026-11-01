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
slug = 'selfie'
H = A / 'depth-v2' / slug
load = lambda p: json.loads(p.read_text())
dump = lambda p, d: p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=P, text=True).strip()
assert base == '5070d51ea0d93db5896fdd7bfe112aa1debffac5'
assert not subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=P, text=True).strip()
ready = load(H / 'ready.json')
review = load(H / 'root-review/personal-review.json')
assert ready['status'] == review['status'] == 'root-personally-accepted'
assert all(ready[k] for k in ['rootPersonalAcceptance', 'publicationAllowed', 'bookContentPublicationAllowed'])
assert all(x['status'] == 'closed' for x in review['findings'])
assert len(ready['allArtifactHashes']) == 127
for name, row in ready['allArtifactHashes'].items():
    assert sha(Path(row['path'])) == row['sha256'], name
assert ready['rootReportSha256'] == sha(H / 'root-review/personal-review.json')
old = load(P / 'books.json')
cat = json.loads(json.dumps(old))
book = next(x for x in cat['books'] if x['slug'] == slug)
assert book['screenCount'] == 62
book['screenCount'] = 129
book['readingMinutes'] = {k: v['ru']['uiRoundedMinutes'] for k, v in review['metrics'].items()}
assert book['readingMinutes'] == {'essential': 25, 'core': 47, 'deep': 63}
assert len(cat['books']) == 58 and sum(x['screenCount'] for x in cat['books']) == 2928
assert all(x == y for x, y in zip(old['books'], cat['books']) if x['slug'] != slug)
shutil.copyfile(H / 'selfie.html', P / 'selfie.html')
dump(P / 'books.json', cat)

plan = load(A / 'depth-v2/PLAN.json')
plan['atUtc'] = stamp
for x in plan['books']:
    if x['slug'] == slug:
        x.update(status='root-personally-accepted-awaiting-publication', rootAcceptance=str(H / 'root-review/personal-review.json'),
                 rootEntireRuEnDraftRead=True, rootAllNestedRoutesRead=True,
                 rootRouteReadingMethod=review['personalReading']['routeReadingMethod'], rootCoverageMapCompared=True,
                 rootKeyPrimaryPassagesChecked=True, rootOmissionsAndQualificationsReviewed=True,
                 replacementPublicationAllowed=True, expandedCounts=review['counts'],
                 acceptedHashes={n: sha(H / n) for n in ['story-data.json', 'selfie.html']})
dump(A / 'depth-v2/PLAN.json', plan)
pub = load(A / 'publication-state.json')
pub['rootAcceptedNotYetPublished'] = list(dict.fromkeys(pub.get('rootAcceptedNotYetPublished', []) + [slug]))
dump(A / 'publication-state.json', pub)
hold = load(A / 'publisher-findings/fiction-depth-publication-hold.json')
hold['atUtc'] = stamp
hold['rootAcceptedExceptions'][slug] = {'report': str(H / 'root-review/personal-review.json'), 'reportSha256': ready['rootReportSha256'],
                                      'htmlSha256': sha(H / 'selfie.html'), 'jsonSha256': sha(H / 'story-data.json')}
dump(A / 'publisher-findings/fiction-depth-publication-hold.json', hold)
waiting = [x['slug'] for x in plan['books'] if x['status'] == 'expanded-awaiting-root-personal-reading']
assert len(waiting) == 6
note = ('Selfie personally accepted, publication pending:49/93/129screens;10644RU/11929EN body words; Deep UI63/58minutes. '
        'Root covered all129final bilingual pairs, including30changed/new pairs and all shorter-route transitions, '
        'the complete coverage/omission map and65actual primary intervals/452unique paragraphs. Primary root checks remain selective. '
        'Eleven expanded versions remain live; production58books/2861screens. '
        + str(len(waiting)) + ' candidates await root reading: ' + ', '.join(waiting) + '. '
        'All62positions retain individual root acceptance. Behave source gaps remain; no recorded writer assignment, runtime not polled.')
dispatch_path = A / 'publisher-findings/release07-and-ten-worker-dispatch.json'
dispatch = load(dispatch_path)
dispatch.update(atUtc=stamp, currentPublisher='root; personally accepted Selfie release pending', runtimeStatusPolled=False,
                assignmentCount=len(dispatch['workerAssignments']), assignmentNote=note)
dispatch['latestDepthCompleted'][slug] = 'Personally accepted49/93/129; release pending'
dump(dispatch_path, dispatch)
status = load(A / 'library-status.json')
status.update(asOfUtc=stamp, basis='62approved positions. ' + note + ' Historical factual stages remain distinct from maximum-depth acceptance.')
for x in status['books']:
    if x['slug'] == slug:
        x.update(maximumDepthStage='root-personally-accepted-awaiting-publication', rootExpandedTextAccepted=True,
                 depthReviewStatus='root-accepted-expanded')
status['maximumDepthStages'] = dict(collections.Counter(x['maximumDepthStage'] for x in status['books']))
assert sum(status['maximumDepthStages'].values()) == 62
dump(A / 'library-status.json', status)
labels = {'awaiting-expanded-work': 'Awaits expanded work', 'source-map-incomplete': 'Primary-source coverage incomplete',
          'expanded-writing-assigned': 'Expanded version assigned', 'root-accepted-and-live': 'Personally accepted and live',
          'root-personally-accepted-awaiting-publication': 'Personally accepted; release pending',
          'expanded-awaiting-root-personal-reading': 'Candidate awaits personal root reading'}
md = '# Library depth status\n\nUpdated ' + stamp + '. ' + note + '\n\n| Current depth stage | Count |\n|---|---:|\n'
md += ''.join('| ' + labels.get(k, k) + ' | ' + str(v) + ' |\n' for k, v in status['maximumDepthStages'].items())
md += '\n| Book | Author | Current depth stage |\n|---|---|---|\n'
md += ''.join('| ' + x['title'] + ' | ' + x['author'] + ' | ' + labels.get(x['maximumDepthStage'], x['maximumDepthStage']) + ' |\n' for x in status['books'])
(A / 'library-status.md').write_text(md)
csv_path = A / 'library-status.csv'
with csv_path.open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    fields, rows = reader.fieldnames, list(reader)
by_slug = {x['slug']: x for x in status['books']}
for x in rows:
    x.update(maximumDepthStage=by_slug[x['slug']]['maximumDepthStage'], rootExpandedTextAccepted=str(by_slug[x['slug']]['rootExpandedTextAccepted']).lower())
with csv_path.open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
intake_path = A / 'depth-v2/root-intake/selfie.json'
intake = load(intake_path)
intake.update(stage='root-personally-accepted-awaiting-publication', rootPersonalAcceptance=True, publicationAllowed=True,
              rootPersonalReview=str(H / 'root-review/personal-review.json'), rootPersonalReviewSha256=ready['rootReportSha256'],
              readySha256=sha(H / 'ready.json'), counts=review['counts'], bodyWords={'ru': 10644, 'en': 11929},
              sourceScope=review['primaryReading'], hashBindingsVerified=127, exactAcceptedHashes=review['exactContentHashes'],
              scope='Exact personally accepted expanded version; publication pending. Original writer completion is preserved in input-ready.json.')
dump(intake_path, intake)
(A / 'depth-v2/PLAN.md').write_text((A / 'depth-v2/PLAN.md').read_text() + '\n\nCurrent ' + stamp + ': ' + note + '\n')
(C / 'NEXT_STEPS.md').write_text('# Current personal reading queue —2026-11-01\n\n' + note + '\n\nThis block supersedes historical states below.\n\n---\n\n' + (C / 'NEXT_STEPS.md').read_text())
(C / 'README.md').write_text((C / 'README.md').read_text().replace('# Book TikTok Library\n', '# Book TikTok Library\n\nCurrent2026-11-01: ' + note + ' This statement supersedes historical notes below.\n', 1))
entry = ('## 2026-11-01 — Book library: Selfie personally accepted, publication pending\n\n'
         'Root read128input RU/EN pairs, the entire coverage/omission map and final shorter routes; all129final pairs and30changed/new pairs have version-matching reading evidence. '
         '65actual source intervals,452unique paragraphs/33014unique whitespace words checked. Writer ledger integrity verifies1159main paragraphs in30acknowledged displays; root source reading remains selective. '
         'Restored Coulson programme outcomes and Marwick market/labour mechanism, corrected Marin byline and Heinz contrast, trimmed repeated audit asides and repaired cohesion. '
         '49/93/129screens;10644RU/11929EN body words; UI63/58minutes. Fresh69structural passes,1084route positions,160layouts, cold Serif100px RU/EN, fonts/Settings/focus, explicit deeper Continue and authentic legacy isolation pass. '
         '127frozen artifact bindings;3121baseline inputs preserved except two separately hash-recorded root PLAN coordination changes.70additional Huck bindings unchanged. Chrome cleaned; physical Safari/PWA untested. '
         'Huck completed33/84/159; its68writer bindings plus ready/manifest verified, root reading still pending.\n\n' + note + '\n\n')
for p in [C / 'LOG.md', Path('/Users/pn/smartcat/LOG.md')]:
    p.write_text(entry + p.read_text())
receipt = {'atUtc': stamp, 'slug': slug, 'baseMerge': base, 'rootReview': str(H / 'root-review/personal-review.json'),
           'rootReviewSha256': ready['rootReportSha256'], 'acceptedHashes': {n: sha(H / n) for n in ['story-data.json', 'selfie.html']},
           'counts': review['counts'], 'candidateBindingsVerified': 127, 'intendedBooks': 58, 'intendedScreens': 2928,
           'scope': 'Only Selfie public reader and its count/times;57other entries/58other root HTML unchanged. Private evidence excluded.',
           'allOtherNewBookContentHeld': True}
dump(A / 'publisher-findings/expanded-depth-12-intake.json', receipt)
shutil.copytree(H, P / rel / 'depth-v2/selfie', dirs_exist_ok=True)
names = ['depth-v2/PLAN.json', 'depth-v2/PLAN.md', 'depth-v2/root-intake/selfie.json', 'depth-v2/root-intake/adventures-of-huckleberry-finn.json',
         'publication-state.json', 'production-catalogue.json', 'library-status.json', 'library-status.csv', 'library-status.md',
         'publisher-findings/fiction-depth-publication-hold.json', 'publisher-findings/release07-and-ten-worker-dispatch.json']
for name in names:
    (P / rel / name).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(A / name, P / rel / name)
for name in ['NEXT_STEPS.md', 'README.md', 'LOG.md']:
    shutil.copyfile(C / name, P / name)
for pattern in ['expanded-depth-11-*', 'expanded-depth-12-*', 'huckleberry-finn-expanded-*']:
    for path in (A / 'publisher-findings').glob(pattern):
        if path.is_file():
            shutil.copyfile(path, P / rel / 'publisher-findings' / path.name)
print(json.dumps({'base': base, 'intendedBooks': 58, 'intendedScreens': 2928, 'bindings': 127, 'stages': status['maximumDepthStages']}))

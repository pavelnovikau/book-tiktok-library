from pathlib import Path
import collections
import csv
import datetime
import hashlib
import json
import shutil

C = Path('/Users/pn/smartcat/_artifacts/book-tiktok-library')
P = Path('/Users/pn/.t3/checkouts/book-tiktok-library-release07-20261031')
rel = Path('editorial-audit/2026-10-31')
A = C / rel
F = A / 'publisher-findings'
slug = 'four-thousand-weeks'
H = A / 'depth-v2' / slug
load = lambda p: json.loads(p.read_text())
dump = lambda p, d: p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
proof = load(F / 'expanded-depth-11-production.json')
readiness = load(F / 'expanded-depth-11-readiness.json')
merge = load(F / 'expanded-depth-11-merge.json')
threads = load(F / 'expanded-depth-11-review-threads.json')
assert merge['merged'] and merge['sha'] == proof['merge']
assert readiness['headRefOid'] == proof['head']
assert proof['changedReaderCatalogueAndHomepageMatch'] and proof['private404sMatch']
assert not [x for x in proof['publicAssets'] if not x['matches'] and 'error' not in x]
assert len(readiness['statusCheckRollup']) == 3
assert all(x.get('conclusion', x.get('state')) == 'SUCCESS' for x in readiness['statusCheckRollup'])
assert not readiness['reviews']
assert not threads['review_threads']
observed = next(x for x in proof['publicAssets'] if x['name'] == 'books.json')
assert observed['catalogueBooks'] == 58 and observed['catalogueScreens'] == 2861
ready = load(H / 'ready.json')
review = load(H / 'root-review/personal-review.json')
assert ready['rootPersonalAcceptance'] and ready['publicationAllowed']
assert ready['rootReportSha256'] == sha(H / 'root-review/personal-review.json')
for name, row in ready['allArtifactHashes'].items():
    assert sha(Path(row['path'])) == row['sha256'], name
pr = int(proof['pr'].rstrip('/').split('/')[-1])
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
matched = sum(x['matches'] for x in proof['publicAssets'])
unobserved = [x for x in proof['publicAssets'] if not x['matches']]
scope = (f'Changed Four Thousand Weeks reader, catalogue and homepage verified by exact HTTP hashes; '
         f'{matched} of {len(proof["publicAssets"])} attempted public assets match, plus two private404s. '
         'Other public content is unchanged locally. Any transport-only unobserved canary remains documented without retry. '
         'This is not a fresh observation of all 69 public assets. Other replacements require individual root reading.')
pub = load(A / 'publication-state.json')
assert slug not in pub['rootAcceptedExpandedSlugs']
pub['rootAcceptedExpandedSlugs'].append(slug)
accepted_count = len(pub['rootAcceptedExpandedSlugs'])
assert accepted_count == 11
pub.update(verifiedAtUtc=stamp, catalogueBooks=58, catalogueScreens=2861,
           productionMerge=proof['merge'], scope=scope,
           rootAcceptedNotYetPublished=[x for x in pub.get('rootAcceptedNotYetPublished', []) if x != slug],
           allCurrentProductionAssetsVerified=False, changedProductionAssetsVerified=True)
for name in ['local', 'readiness', 'review-threads', 'merge', 'production', 'receipt']:
    filename = 'publisher-findings/expanded-depth-11-' + name + '.json'
    if filename not in pub['proofs']:
        pub['proofs'].append(filename)
dump(A / 'publication-state.json', pub)
shutil.copyfile(P / 'books.json', A / 'production-catalogue.json')
plan = load(A / 'depth-v2/PLAN.json')
plan['atUtc'] = stamp
for x in plan['books']:
    if x['slug'] == slug:
        x.update(status='root-accepted-and-live', currentScreens=87, currentRuBodyWords=8006,
                 productionMerge=proof['merge'], productionPr=pr)
dump(A / 'depth-v2/PLAN.json', plan)
intake_path = A / f'depth-v2/root-intake/{slug}.json'
intake = load(intake_path)
intake.update(stage='root-accepted-and-live', productionMerge=proof['merge'], productionPr=pr,
              productionProof='publisher-findings/expanded-depth-11-production.json')
dump(intake_path, intake)
dispatch_path = F / 'release07-and-ten-worker-dispatch.json'
dispatch = load(dispatch_path)
dispatch.update(atUtc=stamp, runtimeStatusPolled=False,
                currentPublisher=f'root; expanded Four Thousand Weeks PR{pr} merged and production-verified')
dispatch['latestDepthCompleted'][slug] = f'Personally accepted, live and production-verified PR{pr}'
dispatch['published'].update(books=58, screens=2861, rootExpandedAcceptedAndLive=accepted_count,
                             **{f'changedAssets{pr}Verified': True})
queue_order = ['selfie', 'mindfulness', 'monday-begins-on-saturday', 'the-body-keeps-the-score', 'amphibian-man', 'akselerando']
waiting = {x['slug'] for x in plan['books'] if x['status'] == 'expanded-awaiting-root-personal-reading'}
queue = [x for x in queue_order if x in waiting] + sorted(waiting - set(queue_order))
assert len(queue) == 6
assignments = sorted(dispatch['workerAssignments'])
dispatch['assignmentCount'] = len(assignments)
note = (f'Four Thousand Weeks PR{pr} personally accepted, merged and production-verified: '
        '25 / 65 / 87 screens; 8,006 RU / 9,092 EN body words; Deep UI 47 / 44 minutes. '
        'Eleven expanded versions are personally accepted and live; production has 58 books / 2,861 screens. '
        f'{len(queue)} completed candidates await personal reading: ' + ', '.join(queue) + '. '
        f'{len(assignments)} recorded writer assignments; runtime not polled. '
        'Behave source gaps remain. All 62 positions retain individual root acceptance.')
dispatch['assignmentNote'] = note
dump(dispatch_path, dispatch)
hold_path = F / 'fiction-depth-publication-hold.json'
hold = load(hold_path)
hold['atUtc'] = stamp
hold['rootAcceptedExceptions'][slug]['productionPr'] = pr
hold['rootAcceptedExceptions'][slug]['productionMerge'] = proof['merge']
dump(hold_path, hold)
status = load(A / 'library-status.json')
status.update(asOfUtc=stamp, rootExpandedAcceptedPublished=accepted_count,
              basis='62 approved positions. ' + scope + ' Historical factual stages remain distinct from current maximum-depth acceptance.')
for x in status['books']:
    if x['slug'] == slug:
        x.update(maximumDepthStage='root-accepted-and-live', rootExpandedTextAccepted=True,
                 depthReviewStatus='root-accepted-expanded')
status['maximumDepthStages'] = dict(collections.Counter(x['maximumDepthStage'] for x in status['books']))
assert sum(status['maximumDepthStages'].values()) == 62
assert status['maximumDepthStages']['root-accepted-and-live'] == 11
dump(A / 'library-status.json', status)
labels = {'awaiting-expanded-work': 'Awaits expanded work', 'source-map-incomplete': 'Primary-source coverage incomplete',
          'expanded-writing-assigned': 'Expanded version assigned', 'root-accepted-and-live': 'Personally accepted and live',
          'root-personally-accepted-awaiting-publication': 'Personally accepted; release pending',
          'expanded-awaiting-root-personal-reading': 'Candidate awaits personal root reading'}
md = '# Library depth status\n\nUpdated ' + stamp + '. ' + note + '\n\n| Current depth stage | Count |\n|---|---:|\n'
md += ''.join(f'| {labels.get(k, k)} | {v} |\n' for k, v in status['maximumDepthStages'].items())
md += '\n| Book | Author | Current depth stage |\n|---|---|---|\n'
md += ''.join(f'| {x["title"]} | {x["author"]} | {labels.get(x["maximumDepthStage"], x["maximumDepthStage"])} |\n' for x in status['books'])
(A / 'library-status.md').write_text(md)
csv_path = A / 'library-status.csv'
with csv_path.open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    fields, rows = reader.fieldnames, list(reader)
by_slug = {x['slug']: x for x in status['books']}
for x in rows:
    x.update(maximumDepthStage=by_slug[x['slug']]['maximumDepthStage'],
             rootExpandedTextAccepted=str(by_slug[x['slug']]['rootExpandedTextAccepted']).lower())
with csv_path.open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
receipt = {'atUtc': stamp, 'status': 'published-and-production-verified', 'pr': proof['pr'],
           'head': proof['head'], 'merge': proof['merge'], 'slug': slug, 'counts': review['counts'],
           'bodyWords': {'ru': 8006, 'en': 9092},
           'uiReadingMinutes': {k: {lang: v[lang]['uiRoundedMinutes'] for lang in ['ru', 'en']} for k, v in review['metrics'].items()},
           'rootPersonallyReadCompleteRuEnRetelling': True,
           'shorterRoutesMethod': review['personalReading']['routeReadingMethod'],
           'rootWholePrimaryContinuouslyRead': False, 'primaryReading': review['primaryReading'],
           'exactAcceptedHashes': {k: v for k, v in review['exactContentHashes'].items() if k in [slug + '.html', 'story-data.json']},
           'rootReportSha256': ready['rootReportSha256'], 'checks': '3 SUCCESS; no reviews or inline findings',
           'catalogueBooks': 58, 'catalogueScreens': 2861, 'productionHttpAssetMatches': matched,
           'attemptedPublicAssets': len(proof['publicAssets']), 'unobservedCanaries': unobserved,
           'productionScope': scope, 'private404s': sum(x['matches'] for x in proof['privatePaths']),
           'all69AssetsFreshlyFetched': False, 'allOtherPublicContentLocallyUnchanged': True,
           'allUnacceptedBookContentStillHeld': True, 'ownedChromeProcessesProfilesRemoved': True,
           'physicalSafariPwaTested': False, 'rootNextReading': queue}
for root in [C, P]:
    dump(root / rel / 'publisher-findings/expanded-depth-11-receipt.json', receipt)
(A / 'depth-v2/PLAN.md').write_text((A / 'depth-v2/PLAN.md').read_text() + '\n\nProduction ' + stamp + ': ' + note + '\n')
(C / 'NEXT_STEPS.md').write_text('# Current personal reading queue — 2026-11-01\n\n' + note + '\n\nThis block supersedes historical states below.\n\n---\n\n' + (C / 'NEXT_STEPS.md').read_text())
(C / 'README.md').write_text((C / 'README.md').read_text().replace('# Book TikTok Library\n', '# Book TikTok Library\n\nCurrent 2026-11-01: ' + note + ' Evidence: editorial-audit/2026-10-31/publisher-findings/expanded-depth-11-receipt.json. This statement supersedes historical notes below.\n', 1))
entry = ('## 2026-11-01 — Book library: expanded Four Thousand Weeks personally accepted and live\n\n'
         'Root read all 87 original RU/EN pairs, all 25 final Essential pairs and 40 Core additions with both actual adjacent route edges; '
         'all 21 final revised pairs were read against their current hashes. Full coverage/omission map, amended rows and global source/method notes read. '
         'Checked 28 actual primary intervals, 201 unique paragraphs / 24,437 displayed whitespace words. Root primary reading was selective. '
         'Restored commitment, discomfort, patience, control/hope ending and actual cases; removed authoring asides and repaired cohesion.\n\n'
         'Fresh QA: 69 structural passes, 708 route positions, 80 representative layouts, genuinely cold RU/EN Serif at 100 px, Settings/focus, '
         'explicit deeper Continue, preferences/reload and authentic legacy isolation. Harness-only assumptions corrected with history preserved. '
         '98 accepted artifact bindings match in both copies. Owned Chrome removed; physical Safari/PWA untested. '
         f'PR{pr} merged {proof["merge"][:8]}; {matched} of {len(proof["publicAssets"])} attempted public hashes match, including the changed reader/catalogue/homepage, '
         'plus two private404s. Any transport failures remain explicitly unobserved without retry; all 69 assets were not freshly fetched. '
         'Evidence: _artifacts/book-tiktok-library/editorial-audit/2026-10-31/publisher-findings/expanded-depth-11-receipt.json.\n\n' + note + '\n\n')
for log in [C / 'LOG.md', Path('/Users/pn/smartcat/LOG.md')]:
    log.write_text(entry + log.read_text())
print(json.dumps({'live': True, 'pr': pr, 'books': 58, 'screens': 2861,
                  'rootAcceptedLive': accepted_count, 'maximumDepthStages': status['maximumDepthStages']}))

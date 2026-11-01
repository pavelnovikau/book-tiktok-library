from pathlib import Path
import collections
import csv
import datetime
import json
import shutil

C = Path('/Users/pn/smartcat/_artifacts/book-tiktok-library')
P = Path('/Users/pn/.t3/checkouts/book-tiktok-library-release07-20261031')
rel = Path('editorial-audit/2026-10-31')
A = C / rel
load = lambda p: json.loads(p.read_text())
dump = lambda p, d: p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
proof = load(A / 'publisher-findings/expanded-depth-10-production.json')
assessment = load(A / 'publisher-findings/expanded-depth-10-production-assessment.json')
assert assessment['changedReaderCatalogueAndHomepageMatch'] and proof['private404sMatch']
assert assessment['freshPublicHashesMatched'] == sum(x['matches'] for x in proof['publicAssets']) == 11
observed = next(x for x in proof['publicAssets'] if x['name'] == 'books.json')
assert observed['catalogueBooks'] == 58 and observed['catalogueScreens'] == 2826
pr = int(proof['pr'].rstrip('/').split('/')[-1])
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
slug = 'essentialism'
H = A / 'depth-v2' / slug
review = load(H / 'root-review/personal-review.json')
pub = load(A / 'publication-state.json')
assert slug not in pub['rootAcceptedExpandedSlugs']
pub['rootAcceptedExpandedSlugs'].append(slug)
accepted_count = len(pub['rootAcceptedExpandedSlugs'])
assert accepted_count == 10
pub.update(verifiedAtUtc=stamp, catalogueBooks=58, catalogueScreens=2826, productionMerge=proof['merge'], scope='Expanded Essentialism personally accepted and live. Fresh exact HTTP hashes for changed reader/catalogue, homepage and eight earlier accepted expanded books; two private404s. Captain Grant could not be freshly observed due to a TLS handshake timeout; its unchanged local hash matches the prior verified release. Other replacements require individual root reading.', rootAcceptedNotYetPublished=[x for x in pub.get('rootAcceptedNotYetPublished', []) if x != slug], allCurrentProductionAssetsVerified=False, changedProductionAssetsVerified=True)
for name in ['local', 'readiness', 'review-threads', 'merge', 'production', 'production-assessment', 'receipt']:
    filename = 'publisher-findings/expanded-depth-10-' + name + '.json'
    if filename not in pub['proofs']:
        pub['proofs'].append(filename)
dump(A / 'publication-state.json', pub)
shutil.copyfile(P / 'books.json', A / 'production-catalogue.json')
plan = load(A / 'depth-v2/PLAN.json')
plan['atUtc'] = stamp
for x in plan['books']:
    if x['slug'] == slug:
        x.update(status='root-accepted-and-live', currentScreens=125, currentRuBodyWords=8749, productionMerge=proof['merge'], productionPr=pr)
dump(A / 'depth-v2/PLAN.json', plan)
intake = load(A / ('depth-v2/root-intake/' + slug + '.json'))
intake.update(stage='root-accepted-and-live', productionMerge=proof['merge'], productionPr=pr)
dump(A / ('depth-v2/root-intake/' + slug + '.json'), intake)
dispatch = load(A / 'publisher-findings/release07-and-ten-worker-dispatch.json')
dispatch.update(atUtc=stamp, runtimeStatusPolled=False, currentPublisher='root; expanded Essentialism PR' + str(pr) + ' merged and production-verified')
dispatch['latestDepthCompleted'][slug] = 'Personally accepted, live and production-verified PR' + str(pr)
dispatch['published'].update(books=58, screens=2826, rootExpandedAcceptedAndLive=accepted_count, **{'changedAssets' + str(pr) + 'Verified': True})
queue_order = ['four-thousand-weeks', 'selfie', 'mindfulness', 'monday-begins-on-saturday', 'the-body-keeps-the-score']
waiting = {x['slug'] for x in plan['books'] if x['status'] == 'expanded-awaiting-root-personal-reading'}
queue = [x for x in queue_order if x in waiting] + sorted(waiting - set(queue_order))
assignments = sorted(dispatch['workerAssignments'])
dispatch['assignmentCount'] = len(assignments)
dispatch['assignmentNote'] = 'Expanded Essentialism personally accepted/live. Completed root-reading queue: ' + ', '.join(queue) + '. Current assignments: ' + ', '.join(assignments) + '. Runtime not polled.'
dump(A / 'publisher-findings/release07-and-ten-worker-dispatch.json', dispatch)
status = load(A / 'library-status.json')
status.update(asOfUtc=stamp, rootExpandedAcceptedPublished=accepted_count, basis='62 approved positions. Exact changed Essentialism production assets and canaries verified at58books/2826screens. Historical factual stages remain distinct from root maximum-depth acceptance.')
for x in status['books']:
    if x['slug'] == slug:
        x.update(maximumDepthStage='root-accepted-and-live', rootExpandedTextAccepted=True, depthReviewStatus='root-accepted-expanded')
status['maximumDepthStages'] = dict(collections.Counter(x['maximumDepthStage'] for x in status['books']))
assert sum(status['maximumDepthStages'].values()) == 62
dump(A / 'library-status.json', status)
labels = {'awaiting-expanded-work': 'Awaits expanded work', 'source-map-incomplete': 'Primary-source coverage incomplete', 'expanded-writing-assigned': 'Expanded version assigned', 'root-accepted-and-live': 'Personally accepted and live', 'root-personally-accepted-awaiting-publication': 'Personally accepted; release pending', 'expanded-awaiting-root-personal-reading': 'Candidate awaits personal root reading'}
note = 'Expanded Essentialism PR' + str(pr) + ' personally accepted, merged and production-verified:49/108/125screens,8749RU/10230EN noncover body words, Deep52/50minutes in UI. Ten expanded versions personally accepted/live; production58books/2826screens. ' + str(len(queue)) + ' completed candidates await personal reading: ' + ', '.join(queue) + '. ' + str(len(assignments)) + ' assignments: ' + ', '.join(assignments) + '; runtime not polled. Behave source gaps remain. All62positions retain individual root acceptance.'
md = '# Library depth status\n\nUpdated ' + stamp + '. ' + note + '\n\n| Current depth stage | Count |\n|---|---:|\n'
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
receipt = {'atUtc': stamp, 'status': 'published-and-production-verified', 'pr': proof['pr'], 'head': proof['head'], 'merge': proof['merge'], 'slug': slug, 'counts': review['counts'], 'bodyWords': {'ru': 8749, 'en': 10230}, 'uiReadingMinutes': {k: {language: v[language]['displayedLabel'] for language in ['ru', 'en']} for k, v in review['metrics'].items()}, 'rootPersonallyReadCompleteRuEnRetelling': True, 'shorterRoutesMethod': review['personalReading']['routeReadingMethod'], 'rootWholePrimaryContinuouslyRead': False, 'rootPrimaryRanges': 34, 'exactAcceptedHashes': {k: v for k, v in review['exactContentHashes'].items() if k in [slug + '.html', 'story-data.json']}, 'checks': '3SUCCESS; no reviews or inline findings', 'catalogueBooks': 58, 'catalogueScreens': 2826, 'productionHttpAssetMatches': 11, 'attemptedPublicAssets': 12, 'unobservedCanary': assessment['unobservedPriorCanary'], 'productionScope': 'Changed reader and catalogue verified; one unchanged prior canary failed only at transport', 'private404s': 2, 'all69AssetsFreshlyFetched': False, 'allOtherPublicContentLocallyUnchanged': True, 'allUnacceptedBookContentStillHeld': True, 'ownedChromeProcessesProfilesRemoved': True, 'rootNextReading': queue}
for root in [C, P]:
    dump(root / rel / 'publisher-findings/expanded-depth-10-receipt.json', receipt)
(A / 'depth-v2/PLAN.md').write_text((A / 'depth-v2/PLAN.md').read_text() + '\n\nProduction ' + stamp + ': ' + note + '\n')
(C / 'NEXT_STEPS.md').write_text('# Current personal reading queue —2026-11-01\n\n' + note + '\n\nThis current block supersedes historical states below.\n\n---\n\n' + (C / 'NEXT_STEPS.md').read_text())
(C / 'README.md').write_text((C / 'README.md').read_text().replace('# Book TikTok Library\n', '# Book TikTok Library\n\nCurrent2026-11-01: ' + note + ' Evidence: editorial-audit/2026-10-31/publisher-findings/expanded-depth-10-receipt.json. This statement supersedes historical notes below.\n', 1))
entry = '## 2026-11-01 — Book library: expanded Essentialism personally accepted and live\n\nRoot completely read125RU/EN original screens; reread49Essential pairs and59Core additions with both adjacent route edges; personally reread13final changed pairs. Full247-line coverage/omission map, Sources and handoff read.34actual selected primary intervals checked,444unique paragraphs; writer reading ledger integrity checked separately. No root continuous whole-primary, published-English, source-figure or underlying-study certification. Seven findings closed: choice principle, sleep-pod conclusion, actual rescue, ordinary-body audit asides, antecedents/names and shorter-route Anna/leadership context.\n\nFresh69structural checks,1128route positions,80representative layouts, genuinely cold RU/EN Serif100px, Settings, reload/preferences, explicit deeperContinue and authentic legacy isolation passed. Owned Chrome removed; physical Safari/PWA untested.97frozen bindings exact in canonical/prepared copies. PR' + str(pr) + ' merged ' + proof['merge'][:8] + ';11of12attempted production asset hashes match, including the changed reader/catalogue;2private404s. Captain Grant TLS-only timeout preserved without retry; its local hash matches prior verified production.58books/2826screens. Evidence: _artifacts/book-tiktok-library/editorial-audit/2026-10-31/publisher-findings/expanded-depth-10-receipt.json.\n\nBody callback read;80output/152input hashes verified, text still unaccepted. Amphibian callback read;71manifestbindings and ready self-hash verified, expanded text still unaccepted. Root began Four Thousand Weeks and personally read its first20RU/EN screens; no acceptance yet. ' + note + '\n\n'
for p in [C / 'LOG.md', Path('/Users/pn/smartcat/LOG.md')]:
    p.write_text(entry + p.read_text())
print(json.dumps({'live': True, 'pr': pr, 'books': 58, 'screens': 2826, 'rootAcceptedLive': accepted_count, 'maximumDepthStages': status['maximumDepthStages']}))

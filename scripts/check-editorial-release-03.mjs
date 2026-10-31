import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';

const audit = 'editorial-audit/2026-10-31';
const json = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const sha = file => hash(fs.readFileSync(file));
const embedded = html => JSON.parse(html.match(/<script id="book-tiktok-data" type="application\/json">\s*([\s\S]*?)<\/script>/)[1]);
const receipt = json(`${audit}/publisher-findings/release-03.json`);
const catalogue = json('books.json');
const results = [];
for (const accepted of receipt.acceptedCandidates) {
  const { slug } = accepted;
  const review = json(accepted.reviewPath);
  assert.equal(sha(accepted.reviewPath), accepted.reviewSha256, `${slug}: original review preserved`);
  if (accepted.closedFindings) {
    assert.equal(review.verdict, 'REQUIRES-FIXES');
    assert.equal(accepted.newHashesAcceptedExplicitly, true);
    const findings = review.requiredFindings.map(finding => finding.id || finding.findingId).sort();
    assert.deepEqual(findings, [...accepted.closedFindings].sort(), `${slug}: every required finding closed`);
    assert.equal(sha(accepted.closurePath), accepted.closureSha256, `${slug}: source closure evidence`);
    for (const [file, digest] of Object.entries(json(accepted.closurePath).hashes)) assert.equal(sha(file), digest);
  } else {
    assert.equal(review.verdict, 'PASS');
    assert.deepEqual(review.requiredFindings, []);
    const reviewed = review.reviewedFiles || review.reviewedArtifacts;
    for (const file of Array.isArray(reviewed) ? reviewed : Object.values(reviewed)) assert.equal(sha(file.relativePath || file.path), file.sha256, `${slug}: independent PASS hash`);
  }
  for (const file of accepted.acceptedDeliverables) assert.equal(sha(file.path), file.sha256, `${slug}: accepted file immutable`);
  const ready = json(`${audit}/ready/${slug}.json`);
  for (const file of ready.deliverables) assert.equal(sha(file.path), file.sha256, `${slug}: READY hash`);
  const data = json(`collector-output/${slug}/story-data.json`);
  const html = fs.readFileSync(`${slug}.html`, 'utf8');
  const effective = embedded(html);
  const collector = embedded(fs.readFileSync(`collector-output/${slug}/${slug}.html`, 'utf8'));
  for (const [key, value] of Object.entries(data)) {
    assert.deepEqual(effective[key], value, `${slug}: root ${key}`);
    assert.deepEqual(collector[key], value, `${slug}: collector ${key}`);
  }
  assert.deepEqual(effective.modes, collector.modes);
  assert.equal(data.defaultLanguage, 'ru');
  assert.equal(data.defaultTheme, 'dark');
  assert.equal(data.defaultMode, 'essential');
  const counts = Object.fromEntries([['essential', 1], ['core', 2], ['deep', 3]].map(([mode, level]) => [mode, data.screens.filter(screen => screen.level <= level).length]));
  assert.deepEqual(counts, data.targetModes);
  assert.deepEqual(counts, accepted.counts);
  const readyCounts = ready.counts.after || ready.counts;
  assert.deepEqual(counts, Object.fromEntries(Object.keys(counts).map(mode => [mode, readyCounts[mode]])));
  const book = catalogue.books.find(book => book.slug === slug);
  assert.equal(book.screenCount, counts.deep);
  assert.deepEqual(book.description, data.description);
  assert.deepEqual(book.readingMinutes, accepted.readingMinutesByLanguage.ru);
  assert(html.includes('const savedScreen ='), `${slug}: removed progress protection`);
  if (data.spoilerPolicy === 'full-plot-in-deep') {
    assert.equal(data.contentMode, 'narrative');
    assert.equal(book.spoilerPolicy, data.spoilerPolicy);
    if (slug === 'akselerando') {
      assert(html.includes("mode: 'essential', // Book-local: consent is renewed on every page load."));
      assert(html.includes('async function goToId(id)'));
      assert(html.includes("if (mode === 'deep' && !(await confirmDeep())) return;"));
      assert(html.includes('accelerandoSpoilerDialog'));
      assert.deepEqual(effective.media, collector.media);
    } else assert(html.includes("if (state.mode === 'deep') state.mode = 'essential';"));
  } else assert.equal(data.contentMode, 'explanatory');
  results.push({ slug, counts, rootSha256: sha(`${slug}.html`), sourceCount: data.sources.length });
}
assert.equal(catalogue.books.length, 33);
assert.equal(catalogue.books.reduce((n, book) => n + book.screenCount, 0), receipt.catalogueScreens);
assert(!catalogue.books.some(book => book.slug === 'hard-to-be-a-god'));
const monday = catalogue.books.find(book => book.slug === 'monday-begins-on-saturday');
assert.equal(monday.cover.motif, 'enchanted-lab');
assert.deepEqual(monday.collections, []);
assert.equal(monday.audience, 'general');
const base = JSON.parse(execFileSync('git', ['show', `${receipt.baseMain}:books.json`], { encoding: 'utf8' }));
const updated = new Set(results.map(book => book.slug));
let unchangedReaders = 0;
for (const book of base.books.filter(book => !updated.has(book.slug))) {
  assert.equal(sha(book.file), hash(execFileSync('git', ['show', `${receipt.baseMain}:${book.file}`], { maxBuffer: 10 * 1024 * 1024 })));
  assert.deepEqual(catalogue.books.find(current => current.slug === book.slug), book);
  unchangedReaders++;
}
assert.equal(unchangedReaders, 22);
console.log(JSON.stringify({ accepted: results, pairs: results.reduce((n, book) => n + book.counts.deep, 0), unchangedReaders, findings: [] }, null, 2));

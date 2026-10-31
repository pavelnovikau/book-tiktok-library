import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const audit = 'editorial-audit/2026-10-31';
const slugs = ['four-thousand-weeks', 'mindfulness', 'a-guide-to-the-good-life', 'the-body-keeps-the-score', 'amphibian-man', 'selfie'];
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
const json = file => JSON.parse(read(file));
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex');
const embedded = html => JSON.parse(html.match(/<script id="book-tiktok-data" type="application\/json">\s*([\s\S]*?)<\/script>/)[1]);
const catalogue = json('books.json');
const results = [];

for (const slug of slugs) {
  const ready = json(`${audit}/ready/${slug}.json`);
  const review = json(`${audit}/reviews/${slug}.json`);
  assert.equal(review.verdict, 'PASS', `${slug}: independent verdict`);
  assert.deepEqual(review.requiredFindings, [], `${slug}: unresolved content findings`);
  const reviewed = review.reviewedFiles || review.reviewedArtifacts;
  const files = Array.isArray(reviewed) ? reviewed : Object.values(reviewed);
  assert.equal(files.length, 2, `${slug}: reviewed authoring and HTML required`);
  for (const file of files) {
    assert.equal(sha(file.path), file.sha256, `${slug}: reviewed hash ${file.path}`);
    assert(ready.deliverables.some(item => item.path === file.path && item.sha256 === file.sha256), `${slug}: READY/review mismatch`);
  }
  for (const file of ready.deliverables) assert.equal(sha(file.path), file.sha256, `${slug}: READY hash ${file.path}`);
  const data = json(`collector-output/${slug}/story-data.json`);
  const html = read(`${slug}.html`);
  const effective = embedded(html);
  const collector = embedded(read(`collector-output/${slug}/${slug}.html`));
  for (const [key, value] of Object.entries(data)) {
    assert.deepEqual(effective[key], value, `${slug}: effective root ${key}`);
    assert.deepEqual(collector[key], value, `${slug}: effective collector ${key}`);
  }
  assert.deepEqual(effective.modes, collector.modes, `${slug}: derived mode labels/times`);
  assert.equal(review.actualRuEnPairCount, data.screens.length, `${slug}: reviewed pair count`);
  const counts = Object.fromEntries([['essential', 1], ['core', 2], ['deep', 3]].map(([mode, level]) => [mode, data.screens.filter(screen => screen.level <= level).length]));
  assert.deepEqual(counts, data.targetModes, `${slug}: nested counts`);
  assert.deepEqual(counts, ready.counts, `${slug}: READY counts`);
  const book = catalogue.books.find(book => book.slug === slug);
  assert.equal(book.screenCount, counts.deep, `${slug}: catalogue count`);
  assert.deepEqual(book.description, data.description, `${slug}: catalogue description`);
  assert.deepEqual(book.readingMinutes, Object.fromEntries(Object.entries(effective.modes).map(([mode, value]) => [mode, Number(value.minutes.ru.match(/\d+/)[0])])), `${slug}: catalogue RU minutes`);
  assert.equal(data.defaultLanguage, 'ru');
  assert.equal(data.defaultTheme, 'dark');
  assert.equal(data.defaultMode, 'essential');
  assert(html.includes('const savedScreen ='), `${slug}: removed progress protection`);
  if (slug === 'amphibian-man') {
    assert.equal(data.contentMode, 'narrative');
    assert.equal(book.spoilerPolicy, 'full-plot-in-deep');
    assert.equal(book.audience, 'teen-14-plus');
    assert.equal(book.cover.motif, 'sea-air');
    assert(html.includes('if (state.mode === \'deep\') state.mode = \'essential\';'));
    assert(html.includes("if (mode === 'deep' && !allowEnding()) return;"));
    assert(html.includes('target.level === 3 && !allowEnding()'));
  } else assert.equal(data.contentMode, 'explanatory');
  results.push({ slug, counts, rootSha256: sha(`${slug}.html`), sourceCount: data.sources.length });
}
assert.equal(catalogue.books.length, 32);
assert.equal(catalogue.books.reduce((total, book) => total + book.screenCount, 0), 3168);
console.log(JSON.stringify({ accepted: results, pairs: results.reduce((total, book) => total + book.counts.deep, 0), findings: [] }, null, 2));

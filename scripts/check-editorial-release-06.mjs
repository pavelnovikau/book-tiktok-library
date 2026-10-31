import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';

const audit = 'editorial-audit/2026-10-31';
const read = file => fs.readFileSync(file, 'utf8');
const json = file => JSON.parse(read(file));
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const sha = file => hash(fs.readFileSync(file));
const embedded = html => {
  const blocks = [...html.matchAll(/<script id="book-tiktok-data" type="application\/json">\s*([\s\S]*?)<\/script>/g)];
  assert.equal(blocks.length, 1, 'exactly one effective corpus');
  return JSON.parse(blocks[0][1]);
};
const receipt = json(`${audit}/publisher-findings/release-06.json`);
const catalogue = json('books.json');
const accepted = new Set(receipt.acceptedCandidates.map(entry => entry.slug));
const results = [];
for (const entry of receipt.acceptedCandidates) {
  const { slug } = entry;
  const review = json(entry.reviewPath);
  assert.equal(review.verdict, 'PASS');
  assert.equal(sha(entry.reviewPath), entry.reviewSha256);
  assert.equal(sha(entry.reviewPath.replace('.json', '.md')), entry.reviewMarkdownSha256);
  assert.equal(sha(entry.readyPath), entry.readySha256);
  assert.equal(entry.reviewBindings[entry.readyPath], entry.readySha256);
  for (const file of entry.acceptedDeliverables) {
    assert.equal(sha(file.path), file.sha256, file.path);
    assert.equal(file.sha256, entry.reviewBindings[file.path]);
  }
  const canonical = json(`collector-output/${slug}/story-data.json`);
  const original = embedded(read(`collector-output/${slug}/${slug}.html`));
  const root = read(`${slug}.html`);
  assert.deepEqual(embedded(root), original, `${slug}: reviewed effective corpus/media/modes`);
  for (const [key, value] of Object.entries(canonical)) if (key !== 'media') assert.deepEqual(original[key], value, `${slug}: canonical ${key}`);
  assert.equal(canonical.contentMode, 'explanatory');
  assert.equal(canonical.defaultLanguage, 'ru');
  assert.equal(canonical.defaultTheme, 'dark');
  assert.equal(canonical.defaultMode, 'essential');
  const counts = Object.fromEntries([['essential', 1], ['core', 2], ['deep', 3]].map(([mode, level]) => [mode, canonical.screens.filter(screen => screen.level <= level).length]));
  assert.deepEqual(counts, canonical.targetModes);
  assert.deepEqual(counts, entry.counts);
  assert.deepEqual(counts, json(entry.readyPath).counts);
  const book = catalogue.books.find(book => book.slug === slug);
  assert.equal(book.screenCount, counts.deep);
  assert.deepEqual(book.title, canonical.title);
  assert.deepEqual(book.description, canonical.description);
  assert.deepEqual(book.readingMinutes, entry.readingMinutesByLanguage.ru);
  assert(root.includes('const savedScreen ='));
  assert.equal(sha(`${slug}.html`), entry.rootSha256);
  if (slug === 'hermes-nous') {
    assert(root.includes('bookHermesNous.lastSlide') && root.includes('legacyMigration06'));
    assert(/research brief/i.test(book.title.en));
    assert(/not a condensed authored book/.test(original.methodNote.en));
    assert(/not recovered/.test(original.methodNote.en));
  }
  if (slug === 'huberman-protocols') {
    assert(/Selected reading/.test(book.description.en));
    assert(/remaining sections and full text were not read/i.test(original.methodNote.en));
    assert(!book.tags.includes('nutrition') && !book.tags.includes('exercise'));
  }
  results.push({ slug, counts, sha256: sha(`${slug}.html`), sources: canonical.sources.length });
}
const base = JSON.parse(execFileSync('git', ['show', `${receipt.baseMain}:books.json`]));
let unchanged = 0;
for (const book of base.books.filter(book => !accepted.has(book.slug))) {
  const before = execFileSync('git', ['show', `${receipt.baseMain}:${book.file}`], { maxBuffer: 10 * 1024 * 1024 });
  assert.equal(sha(book.file), hash(before), `${book.slug}: previous accepted root preserved`);
  assert.deepEqual(catalogue.books.find(entry => entry.slug === book.slug), book);
  unchanged++;
}
assert.equal(unchanged, receipt.previousUnchangedReaders);
assert.equal(catalogue.books.length, receipt.catalogueBooks);
assert.equal(catalogue.books.reduce((count, book) => count + book.screenCount, 0), receipt.catalogueScreens);
assert.equal(results.reduce((count, entry) => count + entry.counts.deep, 0), receipt.acceptedPairs);
assert.equal(new Set(catalogue.books.map(book => book.cover.motif)).size, catalogue.books.length);
console.log(JSON.stringify({ pass: true, accepted: results, previousUnchangedReaders: unchanged, catalogueBooks: receipt.catalogueBooks, catalogueScreens: receipt.catalogueScreens, findings: [] }, null, 2));

import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const audit = 'editorial-audit/2026-10-31';
const read = file => fs.readFileSync(file, 'utf8');
const json = file => JSON.parse(read(file));
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const sha = file => hash(fs.readFileSync(file));
const embedded = html => JSON.parse(html.match(/<script id="book-tiktok-data" type="application\/json">\s*([\s\S]*?)<\/script>/)[1]);
const receipt = json(`${audit}/publisher-findings/release-04.json`);
const catalogue = json('books.json');
const accepted = [];
for (const entry of receipt.acceptedCandidates) {
  const { slug } = entry;
  const review = json(entry.reviewPath);
  assert.equal(sha(entry.reviewPath), entry.reviewSha256, `${slug}: independent review unchanged`);
  assert.equal(sha(entry.readyPath), entry.readySha256);
  for (const file of entry.acceptedDeliverables) assert.equal(sha(file.path), file.sha256, file.path);
  for (const file of json(entry.readyPath).deliverables) assert.equal(sha(file.path), file.sha256);
  if (entry.independentPassHashBinding) {
    assert.equal(review.verdict, 'PASS');
    const bindings = slug === 'adventures-of-huckleberry-finn'
      ? Object.fromEntries(review.hashes.files.map(file => [path.relative('/Users/pn/smartcat/_artifacts/book-tiktok-library', file.path), file.after]))
      : Object.fromEntries(Object.entries(review.hashes.after.files).map(([file, record]) => [file, record.sha256]));
    for (const file of entry.acceptedDeliverables) assert.equal(sha(file.path), bindings[file.path]);
    assert.equal(sha(entry.readyPath), bindings[entry.readyPath]);
  } else {
    assert.equal(review.verdict, 'REQUIRES-FIXES');
    assert(entry.newHashesAcceptedExplicitly && entry.originalReviewNotRelabeledAsPASS);
    assert.equal(sha(entry.closurePath), entry.closureSha256);
    const closure = json(entry.closurePath);
    assert.equal(entry.reviewSha256, closure.baseIndependentReview.sha256);
    assert.deepEqual(entry.closedFindings, closure.findings);
    const fixes = slug === 'hard-to-be-a-god'
      ? Object.values(closure.changes).map(change => [change.new, change.old])
      : review.findings.flatMap(finding => Object.values(finding.smallestCorrection).filter(Boolean).map(change => [change.new, change.old]));
    for (const file of entry.onlyRequiredPhrasesChangedProof) {
      let reverted = read(file.path);
      for (const [corrected, old] of fixes) {
        assert.equal(reverted.split(corrected).length, 2, `${slug}: fix must occur exactly once`);
        reverted = reverted.replace(corrected, old);
      }
      assert.equal(hash(reverted), file.reconstructedReviewedSha256, `${slug}: all unrelated prose and runtime unchanged`);
    }
  }
  const html = read(`${slug}.html`);
  const data = json(`collector-output/${slug}/story-data.json`);
  const collector = embedded(read(`collector-output/${slug}/${slug}.html`));
  const effective = embedded(html);
  assert.deepEqual(effective, collector, `${slug}: entire effective corpus preserved`);
  for (const [key, value] of Object.entries(data)) {
    if (key !== 'modes') assert.deepEqual(effective[key], value, `${slug}: ${key}`);
  }
  assert(html.includes('const savedScreen ='));
  assert.equal(data.defaultLanguage, 'ru');
  assert.equal(data.defaultTheme, 'dark');
  assert.equal(data.defaultMode, 'essential');
  const counts = Object.fromEntries([['essential', 1], ['core', 2], ['deep', 3]].map(([mode, level]) => [mode, data.screens.filter(screen => screen.level <= level).length]));
  assert.deepEqual(counts, data.targetModes);
  assert.deepEqual(counts, entry.counts);
  const book = catalogue.books.find(item => item.slug === slug);
  assert.deepEqual(book.description, data.description);
  assert.deepEqual(book.readingMinutes, entry.readingMinutesByLanguage.ru);
  assert.equal(book.screenCount, counts.deep);
  assert.equal(sha(`${slug}.html`), entry.rootSha256);
  if (book.spoilerPolicy === 'full-plot-in-deep') {
    assert(html.includes("if (state.mode === 'deep') state.mode = 'essential';"));
    if (slug === 'adventures-of-huckleberry-finn') {
      assert(html.includes('spoilerDialog.addEventListener(\'cancel\''));
      assert(html.includes("if (mode !== 'deep') spoilersAccepted = false;"));
    } else {
      assert(html.includes("if (mode === 'deep' && !allowEnding()) return;"));
      assert(html.includes('if (target && target.level === 3 && !allowEnding()) return;'));
    }
  }
  accepted.push({ slug, counts, sourceCount: data.sources.length, rootSha256: entry.rootSha256 });
}
const base = JSON.parse(execFileSync('git', ['show', `${receipt.baseMain}:books.json`], { encoding: 'utf8' }));
for (const book of base.books) {
  assert.equal(sha(book.file), hash(execFileSync('git', ['show', `${receipt.baseMain}:${book.file}`], { maxBuffer: 10 * 1024 * 1024 })), `${book.slug}: accepted previous root changed`);
  assert.deepEqual(catalogue.books.find(item => item.slug === book.slug), book);
}
assert.equal(base.books.length, 33);
assert.equal(catalogue.books.length, 37);
assert.equal(catalogue.books.reduce((n, book) => n + book.screenCount, 0), 2499);
assert.equal(accepted.reduce((n, book) => n + book.counts.deep, 0), 146);
console.log(JSON.stringify({ accepted, previousReadersByteIdentical: base.books.length, findings: [] }, null, 2));

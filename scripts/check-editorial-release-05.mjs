import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';

const audit = 'editorial-audit/2026-10-31';
const text = file => fs.readFileSync(file, 'utf8');
const json = file => JSON.parse(text(file));
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const sha = file => hash(fs.readFileSync(file));
const relative = file => file.replace('/Users/pn/smartcat/_artifacts/book-tiktok-library/', '');
const embedded = html => {
  const matches = [...html.matchAll(/<script id="book-tiktok-data" type="application\/json">\s*([\s\S]*?)<\/script>/g)];
  assert.equal(matches.length, 1, 'Exactly one effective corpus');
  return JSON.parse(matches[0][1]);
};
const receipt = json(`${audit}/publisher-findings/release-05.json`);
const catalogue = json('books.json');
const result = [];
for (const accepted of receipt.acceptedCandidates) {
  const { slug } = accepted;
  const review = json(accepted.reviewPath);
  assert.equal(sha(accepted.reviewPath), accepted.reviewSha256, `${slug}: independent report preserved`);
  assert.equal(sha(accepted.reviewPath.replace('.json', '.md')), accepted.reviewMarkdownSha256);
  assert.equal(sha(accepted.readyPath), accepted.readySha256);
  for (const file of accepted.acceptedDeliverables) assert.equal(sha(file.path), file.sha256, file.path);
  const ready = json(accepted.readyPath);
  for (const file of [...ready.deliverables, ...(ready.supportingFiles || [])]) {
    assert.equal(sha(relative(file.canonicalPath || file.path)), file.sha256);
  }
  if (slug === 'meditations') {
    assert.equal(review.verdict, 'PASS');
    assert.deepEqual(review.requiredFixes, []);
    assert.equal(review.hashIntegrity.protectedFileCount, 74);
    assert.equal(review.hashIntegrity.files.length, 74);
    assert(review.hashIntegrity.allUnchanged);
    for (const file of review.hashIntegrity.files) assert.deepEqual(file.before, file.after);
    const bindings = Object.fromEntries(review.hashIntegrity.files.map(file => [file.path, file.after.sha256]));
    for (const file of accepted.acceptedDeliverables) assert.equal(sha(file.path), bindings[file.path]);
    assert.equal(sha(accepted.readyPath), bindings[accepted.readyPath]);
  } else if (slug === 'antifragile') {
    assert.equal(review.verdict, 'PASS');
    assert.deepEqual(review.findings, []);
    assert.equal(review.actualRuEnPairCount, 24);
    assert(review.candidateUnchangedDuringReview);
    for (const file of accepted.acceptedDeliverables) assert.equal(sha(file.path), review.hashesAfter[file.path].sha256);
    assert.equal(sha(accepted.readyPath), review.hashesAfter[accepted.readyPath].sha256);
  } else {
    assert.equal(review.verdict, 'REQUIRES-FIXES');
    assert(accepted.newHashesAcceptedExplicitly && accepted.originalReviewNotRelabeledAsPASS);
    assert.equal(sha(accepted.closurePath), accepted.closureSha256);
    const closure = json(accepted.closurePath);
    assert.equal(closure.reviewSha256, accepted.reviewSha256);
    assert.deepEqual([...accepted.closedFindings].sort(), review.findings.filter(f => f.required).map(f => f.id).sort());
    for (const [file, digest] of Object.entries(closure.acceptedFinalHashes)) assert.equal(sha(file), digest);
  }
  const canonical = json(`collector-output/${slug}/story-data.json`);
  const collector = embedded(text(`collector-output/${slug}/${slug}.html`));
  const html = text(`${slug}.html`);
  const effective = embedded(html);
  assert.deepEqual(effective, collector, `${slug}: entire reviewed embedded corpus/media/modes preserved`);
  for (const [key, value] of Object.entries(canonical)) {
    if (key !== 'media') assert.deepEqual(effective[key], value, `${slug}: authoring ${key}`);
  }
  assert.equal(sha(`${slug}.html`), accepted.rootSha256);
  assert.equal(canonical.defaultLanguage, 'ru');
  assert.equal(canonical.defaultTheme, 'dark');
  assert.equal(canonical.defaultMode, 'essential');
  assert(html.includes('const savedScreen ='));
  const counts = Object.fromEntries([['essential', 1], ['core', 2], ['deep', 3]].map(([mode, level]) => [mode, canonical.screens.filter(s => s.level <= level).length]));
  assert.deepEqual(counts, canonical.targetModes);
  assert.deepEqual(counts, accepted.counts);
  assert.deepEqual(counts, ready.counts);
  const book = catalogue.books.find(b => b.slug === slug);
  assert.equal(book.screenCount, counts.deep);
  assert.deepEqual(book.description, canonical.description);
  assert.deepEqual(book.readingMinutes, accepted.readingMinutesByLanguage.ru);
  if (slug === 'meditations') {
    const quotes = effective.screens.filter(screen => screen.quotation);
    assert.equal(quotes.length, 14);
    for (const screen of quotes) {
      for (const language of ['ru', 'en']) {
        assert(screen.copy[language].body.includes(screen.quotation.text[language]));
        assert(screen.copy[language].body.includes(screen.quotation.translators[language]));
      }
    }
    assert.equal(quotes.at(-1).quotation.ruPrintedSection, 'XII.35');
    assert.equal(quotes.at(-1).quotation.locator, 'XII.36');
    assert.match(effective.media['title-leaf'].dataUri, /^data:image\/png;base64,/);
  }
  if (slug === 'the-left-hand-of-darkness') {
    assert.equal(canonical.contentMode, 'narrative');
    assert.equal(canonical.spoilerPolicy, 'full-plot-in-deep');
    assert(html.includes("if (state.mode === 'deep') state.mode = 'essential';"));
    assert(html.includes("if (mode === 'deep' && !allowEnding()) return;"));
    assert(html.includes("if (mode !== 'deep') endingConsent = false;"));
    const screens = Object.fromEntries(canonical.screens.map(s => [s.id, s]));
    assert(screens['waking-in-the-tent'].sources.includes(24));
    for (const id of [4, 23, 24, 25]) assert.equal(canonical.sources.find(s => s.id === id).role, 'reference');
    for (const id of accepted.checkedScreens) assert.equal(screens[id].level, 3);
    for (const finding of review.findings.slice(0, 3)) {
      for (const language of ['ru', 'en']) assert(!screens[finding.screenIds[0]].copy[language].body.includes(finding.exactWording[language]));
    }
  } else assert.equal(canonical.contentMode, 'explanatory');
  result.push({ slug, counts, rootSha256: sha(`${slug}.html`), sourceCount: canonical.sources.length });
}
const base = JSON.parse(execFileSync('git', ['show', `${receipt.baseMain}:books.json`], { encoding: 'utf8' }));
const changed = new Set(result.map(b => b.slug));
let unchangedReaders = 0;
for (const book of base.books.filter(b => !changed.has(b.slug))) {
  assert.equal(sha(book.file), hash(execFileSync('git', ['show', `${receipt.baseMain}:${book.file}`], { maxBuffer: 10 * 1024 * 1024 })));
  assert.deepEqual(catalogue.books.find(b => b.slug === book.slug), book);
  unchangedReaders++;
}
assert.equal(unchangedReaders, receipt.previousUnchangedReaders);
assert.equal(catalogue.books.length, receipt.catalogueBooks);
assert.equal(catalogue.books.reduce((n, b) => n + b.screenCount, 0), receipt.catalogueScreens);
assert.equal(result.reduce((n, b) => n + b.counts.deep, 0), receipt.acceptedPairs);
assert.equal(new Set(catalogue.books.map(b => b.cover.motif)).size, catalogue.books.length);
console.log(JSON.stringify({ accepted: result, pairs: receipt.acceptedPairs, unchangedReaders, findings: [] }, null, 2));

import fs from 'node:fs';
import './check-reader-navigation.mjs';
import {assertReaderUsability} from '../skills/book-tiktok/scripts/reader-usability.mjs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const failures = [];

function fail(message) {
  failures.push(message);
}

function isObject(value) {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function checkLocalized(value, label) {
  if (!isObject(value)) {
    fail(`${label} must be an object with ru/en strings`);
    return;
  }
  for (const language of ['ru', 'en']) {
    if (typeof value[language] !== 'string' || !value[language].trim()) {
      fail(`${label}.${language} must be a non-empty string`);
    }
  }
}

function readJson(filename) {
  try {
    return JSON.parse(fs.readFileSync(path.join(root, filename), 'utf8'));
  } catch (error) {
    fail(`${filename}: ${error.message}`);
    return null;
  }
}

function walkFiles(directory) {
  if (!fs.existsSync(directory)) return [];
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const filename = path.join(directory, entry.name);
    return entry.isDirectory() ? walkFiles(filename) : [filename];
  });
}

const catalogue = readJson('books.json');

// Validate every released runtime, including independent route readers.
for (const book of catalogue?.books || []) {
  try { assertReaderUsability(fs.readFileSync(path.join(root, book.file), 'utf8')); }
  catch (error) { fail(`${book.file}: reader usability: ${error.message}`); }
}


if (catalogue) {
  if (catalogue.schema !== 2) fail('books.json.schema must be 2');
  if (!Array.isArray(catalogue.sections)) fail('books.json.sections must be an array');
  if (!Array.isArray(catalogue.collections)) fail('books.json.collections must be an array');
  if (!Array.isArray(catalogue.books)) fail('books.json.books must be an array');
}

const sectionIds = new Set();
for (const [index, section] of (catalogue?.sections || []).entries()) {
  const label = `sections[${index}]`;
  if (!isObject(section)) {
    fail(`${label} must be an object`);
    continue;
  }
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(section.id || '')) fail(`${label}.id must be kebab-case`);
  if (sectionIds.has(section.id)) fail(`duplicate section id: ${section.id}`);
  sectionIds.add(section.id);
  checkLocalized(section.label, `${label}.label`);
  checkLocalized(section.description, `${label}.description`);
}

const collectionIds = new Set();
for (const [index, collection] of (catalogue?.collections || []).entries()) {
  const label = `collections[${index}]`;
  if (!isObject(collection)) {
    fail(`${label} must be an object`);
    continue;
  }
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(collection.id || '')) fail(`${label}.id must be kebab-case`);
  if (collection.id === 'unassigned') fail(`${label}.id "unassigned" is reserved for books outside collections`);
  if (collectionIds.has(collection.id)) fail(`duplicate collection id: ${collection.id}`);
  collectionIds.add(collection.id);
  checkLocalized(collection.label, `${label}.label`);
}

// Discovery v1 is additive to schema 2. Existing standalone/story-data contracts
// and older catalogues without this extension continue to validate.
const discovery = catalogue?.discovery;
const discoveryIds = {};
if (discovery !== undefined) {
  if (!isObject(discovery) || discovery.version !== 1) fail('discovery.version must be 1');
  for (const kind of ['types', 'genres', 'subjects', 'topics']) {
    const ids = discoveryIds[kind] = new Set();
    if (!Array.isArray(discovery?.[kind])) { fail(`discovery.${kind} must be an array`); continue; }
    for (const [index, item] of discovery[kind].entries()) {
      const label = `discovery.${kind}[${index}]`;
      if (!isObject(item)) { fail(`${label} must be an object`); continue; }
      if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(item.id || '')) fail(`${label}.id must be kebab-case`);
      if (item.id === 'all') fail(`${label}.id "all" is reserved`);
      if (ids.has(item.id)) fail(`duplicate discovery ${kind} id: ${item.id}`);
      ids.add(item.id);
      checkLocalized(item.label, `${label}.label`);
      if (item.aliases !== undefined) {
        if (!Array.isArray(item.aliases) || item.aliases.length > 12) fail(`${label}.aliases must be an array of at most 12 useful search terms`);
        else {
          const aliases = new Set();
          for (const alias of item.aliases) {
            if (typeof alias !== 'string' || !alias.trim() || alias !== alias.trim() || alias.length > 80) {
              fail(`${label}.aliases must contain short non-empty trimmed strings`);
              continue;
            }
            const normalized = alias.normalize('NFKC').toLowerCase().replace(/ё/g, 'е');
            if (aliases.has(normalized)) fail(`${label}.aliases contains a duplicate: ${alias}`);
            aliases.add(normalized);
          }
        }
      }
    }
  }
  if ([...discoveryIds.types].sort().join(',') !== 'fiction,nonfiction') fail('discovery.types must contain fiction and nonfiction only');
  for (const id of discoveryIds.genres) {
    if (discoveryIds.subjects.has(id)) fail(`genre and subject IDs must be distinct: ${id}`);
  }
  for (const [key, knownIds] of [['legacySections', sectionIds], ['legacyCollections', new Set([...collectionIds, 'unassigned'])]]) {
    const mappings = discovery?.[key];
    if (!isObject(mappings)) { fail(`discovery.${key} must be an object`); continue; }
    for (const id of knownIds) {
      if (!Object.hasOwn(mappings, id)) fail(`discovery.${key} is missing a mapping for ${id}`);
    }
    for (const [id, mapping] of Object.entries(mappings)) {
      const label = `discovery.${key}.${id}`;
      if (!knownIds.has(id)) fail(`${label} references an unknown legacy ID`);
      if (!isObject(mapping)) { fail(`${label} must be an object`); continue; }
      if (Object.keys(mapping).some(field => !['type', 'topic', 'query'].includes(field))) fail(`${label} may only map to visible type/topic/query controls`);
      if (mapping.type !== undefined && !discoveryIds.types.has(mapping.type)) fail(`${label}.type references an unknown type`);
      if (mapping.topic !== undefined && !discoveryIds.genres.has(mapping.topic) && !discoveryIds.subjects.has(mapping.topic)) fail(`${label}.topic references an unknown genre or subject`);
      if (mapping.query !== undefined && (typeof mapping.query !== 'string' || !mapping.query.trim())) fail(`${label}.query must be a non-empty string`);
    }
  }
}

function checkDiscoveryRefs(values, kind, label) {
  if (!Array.isArray(values)) { fail(`${label} must be an array`); return; }
  const assigned = new Set();
  for (const id of values) {
    if (!discoveryIds[kind]?.has(id)) fail(`${label} references unknown ${kind} ID: ${id}`);
    if (assigned.has(id)) fail(`${label} contains duplicate value: ${id}`);
    assigned.add(id);
  }
}

const bookSlugs = new Set();
const bookFiles = new Set();
const bookCoverMotifs = new Set();
let totalScreens = 0;
const allowedCoverTypes = new Set(['year', 'constraint', 'split', 'typographic']);
const allowedCoverMotifs = new Set(['habit-cycle', 'balance', 'crash', 'bottleneck', 'relay', 'distill', 'clock', 'weeks', 'mirror', 'stress', 'acceleration', 'door', 'protocol-stack', 'treasure-map', 'plateau', 'terrain', 'body-map', 'archipelago', 'control-field', 'open-knot', 'somatic-trace', 'attention-return', 'causal-layers', 'inherited-path', 'quality-bridge', 'convex-response', 'latitude-search', 'conditioned-trust', 'rule-loop', 'testimony-compass', 'chalk-boundary', 'scale-question', 'sea-air', 'enchanted-lab', 'watchtower', 'river-raft', 'needs-bridge', 'five-disciplines', 'common-city', 'ice-crossing', 'dual-frame', 'stock-flow', 'two-orbits', 'memory-spectrum', 'commons-rules', 'paradigm-shift', 'legibility-grid', 'moving-hearth', 'north-needle', 'null-gravity', 'shutter-court', 'dry-lake', 'suit-radio', 'desert-cycle', 'unforced-motion', 'ocean-station', 'maze-trace', 'twin-serpents', 'meaning-choice', 'buried-cabin', 'canal-reflection', 'regression-spray', 'faceted-prototype']);
const allowedCoverTones = new Set(['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'magenta']);
const allowedAudiences = new Set(['general', 'teen-14-plus', 'adult']);
const allowedSpoilerPolicies = new Set(['not-applicable', 'spoiler-free', 'full-plot-in-deep']);

for (const [index, book] of (catalogue?.books || []).entries()) {
  const label = `books[${index}]`;
  if (book.searchAliases !== undefined && (!Array.isArray(book.searchAliases) || book.searchAliases.some(alias => typeof alias !== 'string' || !alias.trim() || alias.length > 80))) fail(`${label}.searchAliases must contain short non-empty strings`);
  if (!isObject(book)) {
    fail(`${label} must be an object`);
    continue;
  }

  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(book.slug || '')) fail(`${label}.slug must be kebab-case`);
  if (bookSlugs.has(book.slug)) fail(`duplicate book slug: ${book.slug}`);
  bookSlugs.add(book.slug);

  if (typeof book.file !== 'string' || path.basename(book.file) !== book.file || !book.file.endsWith('.html')) {
    fail(`${label}.file must be a root-level .html filename`);
  }
  if (bookFiles.has(book.file)) fail(`duplicate book file: ${book.file}`);
  bookFiles.add(book.file);

  if (!sectionIds.has(book.section)) fail(`${label}.section references unknown section: ${book.section}`);
  if (discovery !== undefined) {
    checkDiscoveryRefs(book.workTypes, 'types', `${label}.workTypes`);
    checkDiscoveryRefs(book.genres, 'genres', `${label}.genres`);
    checkDiscoveryRefs(book.subjects, 'subjects', `${label}.subjects`);
    checkDiscoveryRefs(book.tags, 'topics', `${label}.tags`);
    const types = Array.isArray(book.workTypes) ? book.workTypes : [];
    const genres = Array.isArray(book.genres) ? book.genres : [];
    const subjects = Array.isArray(book.subjects) ? book.subjects : [];
    if (!types.length) fail(`${label}.workTypes must contain at least one type`);
    if (types.includes('fiction') && !genres.length) fail(`${label}: fiction needs a recognizable genre`);
    if (types.includes('nonfiction') && !subjects.length) fail(`${label}: nonfiction needs a subject`);
    if (genres.length && !types.includes('fiction')) fail(`${label}: genres require the fiction work type`);
    if (types.length > 1 || book.workTypeLabel !== undefined) checkLocalized(book.workTypeLabel, `${label}.workTypeLabel`);
  }
  if (!Array.isArray(book.tags) || book.tags.length === 0) fail(`${label}.tags must be a non-empty array`);
  else {
    const tags = new Set();
    for (const tag of book.tags) {
      if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(tag || '')) fail(`${label}.tags contains a non-kebab-case value: ${tag}`);
      if (tags.has(tag)) fail(`${label}.tags contains duplicate value: ${tag}`);
      tags.add(tag);
    }
  }
  if (!Array.isArray(book.collections)) fail(`${label}.collections must be an array`);
  else {
    const assigned = new Set();
    for (const collection of book.collections) {
      if (!collectionIds.has(collection)) fail(`${label}.collections references unknown collection: ${collection}`);
      if (assigned.has(collection)) fail(`${label}.collections contains duplicate value: ${collection}`);
      assigned.add(collection);
    }
  }
  if (!allowedAudiences.has(book.audience)) fail(`${label}.audience must be one of ${[...allowedAudiences].join(', ')}`);
  if (!allowedSpoilerPolicies.has(book.spoilerPolicy)) fail(`${label}.spoilerPolicy must be one of ${[...allowedSpoilerPolicies].join(', ')}`);
  if (!Number.isInteger(book.screenCount) || book.screenCount < 3) fail(`${label}.screenCount must be an integer >= 3`);
  else totalScreens += book.screenCount;

  checkLocalized(book.title, `${label}.title`);
  checkLocalized(book.author, `${label}.author`);
  checkLocalized(book.description, `${label}.description`);

  const minutes = book.readingMinutes;
  if (!isObject(minutes)) {
    fail(`${label}.readingMinutes must contain essential/core/deep`);
  } else {
    const values = ['essential', 'core', 'deep'].map(key => minutes[key]);
    if (values.some(value => !Number.isInteger(value) || value < 1)) fail(`${label}.readingMinutes values must be positive integers`);
    if (values.every(Number.isInteger) && !(values[0] <= values[1] && values[1] <= values[2])) {
      fail(`${label}.readingMinutes must be cumulative: essential <= core <= deep`);
    }
  }

  if (!isObject(book.cover)) fail(`${label}.cover must be an object`);
  else {
    if (!allowedCoverTypes.has(book.cover.type)) fail(`${label}.cover.type must be one of ${[...allowedCoverTypes].join(', ')}`);
    if (!allowedCoverMotifs.has(book.cover.motif)) fail(`${label}.cover.motif must be one of ${[...allowedCoverMotifs].join(', ')}`);
    if (bookCoverMotifs.has(book.cover.motif)) fail(`${label}.cover.motif must be unique in the catalogue: ${book.cover.motif}`);
    bookCoverMotifs.add(book.cover.motif);
    if (!allowedCoverTones.has(book.cover.tone)) fail(`${label}.cover.tone must be one of ${[...allowedCoverTones].join(', ')}`);
  }

  const filePath = path.join(root, book.file || '');
  if (!fs.existsSync(filePath)) {
    fail(`${label}.file does not exist: ${book.file}`);
    continue;
  }

  const html = fs.readFileSync(filePath, 'utf8');
  if (!/^<!doctype html>/i.test(html.trimStart())) fail(`${book.file}: missing HTML doctype`);
  if (!/<meta\s+name=["']viewport["']/i.test(html)) fail(`${book.file}: missing viewport meta`);
  if (!/<title>[^<]+<\/title>/i.test(html)) fail(`${book.file}: missing title`);
  if (!/href=["']\.\/["']/i.test(html)) fail(`${book.file}: missing library home link (href="./")`);
  if (!/(libraryButton|btn-library)/.test(html)) fail(`${book.file}: missing identifiable library home control`);
  if (/<script[^>]+src=["']https?:/i.test(html)) fail(`${book.file}: remote runtime script is not allowed`);
  if (/<link[^>]+rel=["']stylesheet["'][^>]+href=["']https?:/i.test(html)) fail(`${book.file}: remote stylesheet is not allowed`);

  const screenMeta = html.match(/<meta\s+name=["']book-tiktok:screens["']\s+content=["'](\d+)["']/i);
  if (screenMeta && Number(screenMeta[1]) !== book.screenCount) {
    fail(`${book.file}: manifest screenCount ${book.screenCount} does not match metadata ${screenMeta[1]}`);
  }

  const bookData = html.match(/<script[^>]+id=["']book-data["'][^>]*>([\s\S]*?)<\/script>/i);
  if (bookData) {
    try {
      const parsed = JSON.parse(bookData[1]);
      if (Array.isArray(parsed.slides) && parsed.slides.length !== book.screenCount) {
        fail(`${book.file}: manifest screenCount ${book.screenCount} does not match book-data slides ${parsed.slides.length}`);
      }
    } catch (error) {
      fail(`${book.file}: invalid book-data JSON: ${error.message}`);
    }
  }
}

const indexPath = path.join(root, 'index.html');
if (!fs.existsSync(indexPath)) {
  fail('index.html is missing');
} else {
  const indexHtml = fs.readFileSync(indexPath, 'utf8');
  if (!indexHtml.includes("fetch('./books.json', { cache: 'no-store' })")) fail('index.html must load books.json without an HTTP-cache shortcut');
  if (!indexHtml.includes('id="typeFilter"')) fail('index.html is missing the work-type filter');
  if (!/<select\s+[^>]*id="topicFilter"/.test(indexHtml)) fail('index.html is missing the native genre/subject selector');
  if (!indexHtml.includes('id="resetFilters"')) fail('index.html is missing the clear-all action');
  if (!indexHtml.includes('id="filterSummary"')) fail('index.html is missing the live result count');
  if (/id="(?:sectionFilter|collectionFilter|collectionSummary)"/.test(indexHtml)) fail('index.html must not expose legacy shelf/collection controls');
  if (/Сыну · 14\+|For my son · 14\+|Без подборки|No collection/.test(indexHtml)) fail('index.html must not expose personal or administrative collection choices');
  if (!indexHtml.includes('id="searchInput"')) fail('index.html is missing catalogue search');
  if (!indexHtml.includes('function coverArtwork(book)') || !indexHtml.includes('data-cover-motif')) {
    fail('index.html is missing semantic SVG cover artwork');
  }
  // New catalogue identities require both a registered motif and an SVG recipe.
  for (const motif of ['buried-cabin', 'canal-reflection', 'regression-spray']) {
    if (!indexHtml.includes(`'${motif}': true`)) fail(`index.html: missing registered cover motif ${motif}`);
    if (!indexHtml.includes(`motif === '${motif}'`)) fail(`index.html: missing SVG cover recipe ${motif}`);
  }
  if (!indexHtml.includes('id="bookStat"') || !indexHtml.includes('id="screenStat"') || !indexHtml.includes('id="topicStat"')) {
    fail('index.html is missing automatic counters');
  }
  if (!/<link\s+rel=["']manifest["']\s+href=["']\.\/manifest\.webmanifest["']/i.test(indexHtml)) fail('index.html is missing the web app manifest');
  if (!indexHtml.includes("navigator.serviceWorker.register('./sw.js', { updateViaCache: 'none' })")) fail('index.html must bypass the HTTP cache when checking for a service-worker update');
}

for (const filename of ['manifest.webmanifest', 'sw.js', 'icons/icon-192.png', 'icons/icon-512.png', 'icons/apple-touch-icon.png']) {
  if (!fs.existsSync(path.join(root, filename))) fail(`${filename} is missing`);
}

const serviceWorker = fs.readFileSync(path.join(root, 'sw.js'), 'utf8');
if (!serviceWorker.includes("fetch(request, { cache: 'no-store' })")) fail('sw.js must perform network-first catalogue/navigation requests without an HTTP-cache shortcut');

const vercelConfig = readJson('vercel.json');
const headerRules = new Map((vercelConfig.headers || []).map(rule => [rule.source, rule.headers || []]));
function headerValue(source, key) {
  return (headerRules.get(source) || []).find(header => header.key.toLowerCase() === key.toLowerCase())?.value || '';
}
if (!headerValue('/books.json', 'Cache-Control').includes('no-store')) fail('vercel.json must serve books.json with no-store');
if (!headerValue('/sw.js', 'Cache-Control').includes('must-revalidate')) fail('vercel.json must revalidate sw.js');
if (!headerValue('/', 'Cache-Control').includes('must-revalidate')) fail('vercel.json must revalidate the catalogue shell');

const skillRoot = path.join(root, 'skills', 'book-tiktok');
const skillFiles = [
  'SKILL.md',
  'agents/openai.yaml',
  'assets/standalone-template.html',
  'assets/reader-header.html',
  'assets/reader-settings-head.html',
  'assets/reader-settings.html',
  'assets/story-data.example.json',
  'assets/fonts/Geist-Variable.woff2',
  'assets/fonts/GeistMono-Variable.woff2',
  'assets/fonts/LICENSE.txt',
  'assets/fonts/GeistSerif-Regular.woff2',
  'assets/fonts/GeistSerif-LICENSE.txt',
  'assets/fonts/SourceSerif4-Regular.woff2',
  'assets/fonts/SourceSerif4-LICENSE.md',
  'references/content-model.md',
  'references/data-contract.md',
  'references/html-spec.md',
  'references/reader-settings.md',
  'scripts/build_story.mjs',
  'scripts/reader-settings.mjs',
  'scripts/audit_story_html.mjs'
];

for (const filename of skillFiles) {
  if (!fs.existsSync(path.join(skillRoot, filename))) fail(`book-tiktok skill is missing ${filename}`);
}

const skillEntrypoint = path.join(skillRoot, 'SKILL.md');
if (fs.existsSync(skillEntrypoint)) {
  const skillText = fs.readFileSync(skillEntrypoint, 'utf8');
  if (!/^---\s*\nname:\s*book-tiktok\s*\ndescription:/m.test(skillText)) fail('book-tiktok SKILL.md has invalid frontmatter');
  if (/\/Users\/|\.codex\/skills\/book-tiktok/.test(skillText)) fail('book-tiktok SKILL.md contains a machine-specific path');
  if (!skillText.includes('<skill-dir>/scripts/build_story.mjs')) fail('book-tiktok SKILL.md is missing its portable builder command');
}

const skillTreeFiles = walkFiles(skillRoot);
for (const filename of skillTreeFiles) {
  const extension = path.extname(filename).toLowerCase();
  if (!['.md', '.mjs', '.json', '.yaml', '.yml', '.html', '.txt'].includes(extension)) continue;
  const text = fs.readFileSync(filename, 'utf8');
  if (/\/Users\/|[A-Za-z]:\\Users\\/.test(text)) fail(`book-tiktok skill contains a machine-specific path: ${path.relative(skillRoot, filename)}`);
}

if (skillFiles.every(filename => fs.existsSync(path.join(skillRoot, filename)))) {
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'book-tiktok-skill-check-'));
  const output = path.join(tempDir, 'skill-example.html');
  try {
    const build = spawnSync(process.execPath, [
      path.join(skillRoot, 'scripts', 'build_story.mjs'),
      path.join(skillRoot, 'assets', 'story-data.example.json'),
      '--out', output
    ], { cwd: root, encoding: 'utf8' });
    if (build.status !== 0) {
      fail(`book-tiktok example build failed: ${(build.stderr || build.stdout || '').trim()}`);
    } else {
      const audit = spawnSync(process.execPath, [
        path.join(skillRoot, 'scripts', 'audit_story_html.mjs'), output,
        '--min-screens', '1', '--require-bilingual'
      ], { cwd: root, encoding: 'utf8' });
      if (audit.status !== 0) {
        fail(`book-tiktok example audit failed: ${(audit.stderr || audit.stdout || '').trim()}`);
      } else {
        try {
          const report = JSON.parse(audit.stdout);
          if (report.failures?.length || report.warnings?.length) fail('book-tiktok example audit returned warnings or failures');
        } catch (error) {
          fail(`book-tiktok example audit returned invalid JSON: ${error.message}`);
        }
      }
    }
  } finally {
    fs.rmSync(tempDir, { recursive: true, force: true });
  }
}

if (failures.length) {
  console.error(`Library validation failed (${failures.length}):`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(`Library validation passed: ${bookSlugs.size} books, ${sectionIds.size} sections, ${collectionIds.size} collections, ${totalScreens} screens.`);
console.log('Book TikTok skill validation passed: portable package, example build and audit.');

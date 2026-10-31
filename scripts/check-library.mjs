import fs from 'node:fs';
import path from 'node:path';
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

const catalogue = readJson('books.json');

if (catalogue) {
  if (catalogue.schema !== 1) fail('books.json.schema must be 1');
  if (!Array.isArray(catalogue.genres)) fail('books.json.genres must be an array');
  if (!Array.isArray(catalogue.books)) fail('books.json.books must be an array');
}

const genreIds = new Set();
for (const [index, genre] of (catalogue?.genres || []).entries()) {
  const label = `genres[${index}]`;
  if (!isObject(genre)) {
    fail(`${label} must be an object`);
    continue;
  }
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(genre.id || '')) fail(`${label}.id must be kebab-case`);
  if (genreIds.has(genre.id)) fail(`duplicate genre id: ${genre.id}`);
  genreIds.add(genre.id);
  checkLocalized(genre.label, `${label}.label`);
}

const bookSlugs = new Set();
const bookFiles = new Set();
let totalScreens = 0;
const allowedCoverTypes = new Set(['year', 'constraint', 'split', 'typographic']);

for (const [index, book] of (catalogue?.books || []).entries()) {
  const label = `books[${index}]`;
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

  if (!genreIds.has(book.genre)) fail(`${label}.genre references unknown genre: ${book.genre}`);
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
  else if (!allowedCoverTypes.has(book.cover.type)) fail(`${label}.cover.type must be one of ${[...allowedCoverTypes].join(', ')}`);

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
  if (!indexHtml.includes("fetch('./books.json'")) fail('index.html must load books.json');
  if (!indexHtml.includes('id="genreFilter"')) fail('index.html is missing the genre filter');
  if (!indexHtml.includes('id="bookStat"') || !indexHtml.includes('id="screenStat"')) fail('index.html is missing automatic counters');
}

if (failures.length) {
  console.error(`Library validation failed (${failures.length}):`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(`Library validation passed: ${bookSlugs.size} books, ${genreIds.size} genres, ${totalScreens} screens.`);

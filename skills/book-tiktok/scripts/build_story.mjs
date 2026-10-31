#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const args = process.argv.slice(2);
const dataArg = args.find((arg) => !arg.startsWith('--'));
const outIndex = args.indexOf('--out');
const outArg = outIndex >= 0 ? args[outIndex + 1] : null;

if (!dataArg || (outIndex >= 0 && !outArg)) {
  console.error('Usage: build_story.mjs <story-data.json> [--out <book-slug.html>]');
  process.exit(2);
}

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const skillDir = path.resolve(scriptDir, '..');
const dataPath = path.resolve(dataArg);
const dataDir = path.dirname(dataPath);
const templatePath = path.join(skillDir, 'assets', 'standalone-template.html');
const geistPath = path.join(skillDir, 'assets', 'fonts', 'Geist-Variable.woff2');
const geistMonoPath = path.join(skillDir, 'assets', 'fonts', 'GeistMono-Variable.woff2');

function fail(message) {
  throw new Error(message);
}

function requireString(value, label, allowEmpty = false) {
  if (typeof value !== 'string' || (!allowEmpty && !value.trim())) fail(`${label} must be a non-empty string`);
}

function requireLocalized(value, label, allowEmpty = false) {
  if (!value || typeof value !== 'object') fail(`${label} must contain ru and en`);
  requireString(value.ru, `${label}.ru`, allowEmpty);
  requireString(value.en, `${label}.en`, allowEmpty);
}

function htmlEscape(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[char]);
}

function stripHtml(value) {
  return String(value || '')
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&(?:nbsp|amp|lt|gt|quot|#39);/gi, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function wordCount(value) {
  const text = stripHtml(value);
  return text ? (text.match(/[\p{L}\p{N}][\p{L}\p{N}'’\-–—]*/gu) || []).length : 0;
}

function mimeFor(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const map = {
    '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
    '.webp': 'image/webp', '.gif': 'image/gif', '.svg': 'image/svg+xml', '.avif': 'image/avif'
  };
  return map[ext] || null;
}

function localizedMinutes(minutes, language) {
  if (typeof minutes === 'string') return minutes;
  if (!Number.isFinite(minutes) || minutes < 1) fail(`Invalid ${language} reading time`);
  return language === 'ru' ? `${Math.ceil(minutes)} минут` : `${Math.ceil(minutes)} min`;
}

const raw = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
const data = structuredClone(raw);

if (data.schemaVersion !== 2) fail('schemaVersion must be 2');
requireString(data.slug, 'slug');
if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(data.slug)) fail('slug must use lowercase letters, digits, and hyphens');
requireLocalized(data.title, 'title');
requireLocalized(data.description, 'description');

data.defaultLanguage ||= 'ru';
data.defaultTheme ||= 'dark';
data.defaultMode ||= 'essential';
if (data.contentMode !== undefined && !['narrative', 'explanatory'].includes(data.contentMode)) fail('contentMode must be narrative or explanatory when supplied');
if (!['ru', 'en'].includes(data.defaultLanguage)) fail('defaultLanguage must be ru or en');
if (!['light', 'dark'].includes(data.defaultTheme)) fail('defaultTheme must be light or dark');
if (!['essential', 'core', 'deep'].includes(data.defaultMode)) fail('defaultMode must be essential, core, or deep');

if (!Array.isArray(data.sources)) fail('sources must be an array');
const sourceIds = new Set();
for (const [index, source] of data.sources.entries()) {
  if (!Number.isInteger(source.id) || source.id < 1) fail(`sources[${index}].id must be a positive integer`);
  if (sourceIds.has(source.id)) fail(`Duplicate source id ${source.id}`);
  sourceIds.add(source.id);
  requireString(source.title, `sources[${index}].title`);
  requireString(source.url, `sources[${index}].url`);
  if (!/^https?:\/\//i.test(source.url)) fail(`sources[${index}].url must be http(s)`);
  requireLocalized(source.note, `sources[${index}].note`);
  if (!['book', 'publisher', 'author', 'primary', 'review', 'reference'].includes(source.role)) {
    fail(`sources[${index}].role is not recognized`);
  }
}

if (!Array.isArray(data.screens) || data.screens.length < 3) fail('screens must contain at least cover, one body screen, and final screen');
const screenIds = new Set();
let coverCount = 0;
let finalCount = 0;
for (const [index, screen] of data.screens.entries()) {
  requireString(screen.id, `screens[${index}].id`);
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(screen.id)) fail(`screens[${index}].id must be a stable kebab-case id`);
  if (screenIds.has(screen.id)) fail(`Duplicate screen id ${screen.id}`);
  screenIds.add(screen.id);
  if (![1, 2, 3].includes(screen.level)) fail(`screens[${index}].level must be 1, 2, or 3`);
  if (screen.type === 'cover') coverCount += 1;
  if (screen.final) finalCount += 1;
  if (screen.type !== 'cover' && !['book', 'corroboration', 'synthesis'].includes(screen.claimType)) {
    fail(`screens[${index}].claimType must be book, corroboration, or synthesis`);
  }
  if (!Array.isArray(screen.sources)) fail(`screens[${index}].sources must be an array`);
  for (const sourceId of screen.sources) {
    if (!sourceIds.has(sourceId)) fail(`Screen ${screen.id} references unknown source ${sourceId}`);
  }
  if (!screen.copy || typeof screen.copy !== 'object') fail(`screens[${index}].copy must contain ru and en`);
  for (const language of ['ru', 'en']) {
    const copy = screen.copy[language];
    if (!copy || typeof copy !== 'object') fail(`screens[${index}].copy.${language} is required`);
    requireString(copy.section, `screens[${index}].copy.${language}.section`);
    requireString(copy.title, `screens[${index}].copy.${language}.title`);
    requireString(copy.body, `screens[${index}].copy.${language}.body`, screen.type === 'cover');
    if (copy.subtitle !== undefined) requireString(copy.subtitle, `screens[${index}].copy.${language}.subtitle`, true);
    if (copy.visualAlt !== undefined) requireString(copy.visualAlt, `screens[${index}].copy.${language}.visualAlt`, true);
  }
}

if (coverCount !== 1 || data.screens[0].type !== 'cover') fail('Exactly one cover is required and it must be the first screen');
if (data.screens[0].level !== 1) fail('The cover must be level 1');
if (finalCount !== 1 || !data.screens.at(-1).final) fail('Exactly one final screen is required and it must be last');
if (data.screens.at(-1).level !== 1) fail('The final screen must be level 1 so every mode reaches it');

data.media ||= {};
if (!data.media || typeof data.media !== 'object' || Array.isArray(data.media)) fail('media must be an object keyed by media id');
for (const [mediaId, media] of Object.entries(data.media)) {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(mediaId)) fail(`Invalid media id ${mediaId}`);
  requireLocalized(media.alt, `media.${mediaId}.alt`, true);
  requireLocalized(media.credit, `media.${mediaId}.credit`, true);
  if (media.file) {
    const resolved = path.resolve(dataDir, media.file);
    if (!fs.existsSync(resolved)) fail(`Media file not found: ${media.file}`);
    const mime = media.mime || mimeFor(resolved);
    if (!mime || !mime.startsWith('image/')) fail(`Cannot determine image MIME type for ${media.file}`);
    media.dataUri = `data:${mime};base64,${fs.readFileSync(resolved).toString('base64')}`;
    delete media.file;
    delete media.mime;
  }
  if (!media.dataUri || !/^data:image\/[a-z0-9.+-]+;base64,/i.test(media.dataUri)) fail(`media.${mediaId} needs file or an image dataUri`);
}

for (const screen of data.screens) {
  if (screen.media && !data.media[screen.media]) fail(`Screen ${screen.id} references unknown media ${screen.media}`);
}

const modeDefinitions = {
  essential: { level: 1, label: { ru: 'Главное', en: 'Essential' } },
  core: { level: 2, label: { ru: 'Суть книги', en: 'Core' } },
  deep: { level: 3, label: { ru: 'Глубоко', en: 'Deep' } }
};

if (!data.targetModes || typeof data.targetModes !== 'object') {
  fail('targetModes is required and must record the exact cumulative counts derived from the finished content');
}
for (const mode of Object.keys(modeDefinitions)) {
  if (!Number.isInteger(data.targetModes[mode]) || data.targetModes[mode] < 1) {
    fail(`targetModes.${mode} must be a positive integer`);
  }
}

data.modes ||= {};
const counts = {};
const words = {};
for (const [mode, definition] of Object.entries(modeDefinitions)) {
  const visible = data.screens.filter((screen) => screen.level <= definition.level);
  counts[mode] = visible.length;
  words[mode] = { ru: 0, en: 0 };
  for (const screen of visible) {
    for (const language of ['ru', 'en']) {
      const copy = screen.copy[language];
      words[mode][language] += wordCount(`${copy.title} ${copy.subtitle || ''} ${copy.body || ''}`);
    }
  }
  const configured = data.modes[mode] || {};
  if (configured.label) requireLocalized(configured.label, `modes.${mode}.label`);
  const computed = {
    ru: Math.max(1, Math.ceil(words[mode].ru / 180)),
    en: Math.max(1, Math.ceil(words[mode].en / 220))
  };
  const suppliedMinutes = configured.minutes || computed;
  data.modes[mode] = {
    label: configured.label || definition.label,
    minutes: {
      ru: localizedMinutes(suppliedMinutes.ru, 'ru'),
      en: localizedMinutes(suppliedMinutes.en, 'en')
    }
  };
}

if (!(counts.essential < counts.core && counts.core < counts.deep)) {
  fail(`Nested modes must grow strictly; got ${counts.essential}/${counts.core}/${counts.deep}`);
}

if (counts.essential !== data.targetModes.essential || counts.core !== data.targetModes.core || counts.deep !== data.targetModes.deep) {
  fail(`Corpus does not match exact targetModes: expected ${data.targetModes.essential}/${data.targetModes.core}/${data.targetModes.deep}, got ${counts.essential}/${counts.core}/${counts.deep}`);
}

if (data.methodNote) requireLocalized(data.methodNote, 'methodNote');

const outputPath = path.resolve(outArg || path.join(dataDir, `${data.slug}.html`));
fs.mkdirSync(path.dirname(outputPath), { recursive: true });

let template = fs.readFileSync(templatePath, 'utf8');
const replacements = {
  '__TITLE_RU__': htmlEscape(data.title.ru),
  '__DESCRIPTION_RU__': htmlEscape(data.description.ru),
  '__SCREEN_COUNT__': String(data.screens.length),
  '__MODE_COUNTS__': `${counts.essential},${counts.core},${counts.deep}`,
  '__GEIST_WOFF2__': fs.readFileSync(geistPath).toString('base64'),
  '__GEIST_MONO_WOFF2__': fs.readFileSync(geistMonoPath).toString('base64'),
  '__READER_HEADER__': fs.readFileSync(path.join(skillDir, 'assets', 'reader-header.html'), 'utf8'),
  '__BOOK_TIKTOK_DATA__': JSON.stringify(data).replace(/<\//g, '<\\/')
};

for (const [placeholder, value] of Object.entries(replacements)) {
  if (!template.includes(placeholder)) fail(`Template placeholder missing: ${placeholder}`);
  template = template.split(placeholder).join(value);
}

const unresolved = template.match(/__[A-Z0-9_]+__/g);
if (unresolved) fail(`Unresolved template placeholders: ${[...new Set(unresolved)].join(', ')}`);

fs.writeFileSync(outputPath, template);

console.log(JSON.stringify({
  output: outputPath,
  bytes: Buffer.byteLength(template),
  screens: data.screens.length,
  levels: data.screens.reduce((result, screen) => {
    result[screen.level] = (result[screen.level] || 0) + 1;
    return result;
  }, {}),
  modes: counts,
  words,
  sources: data.sources.length,
  media: Object.keys(data.media).length
}, null, 2));

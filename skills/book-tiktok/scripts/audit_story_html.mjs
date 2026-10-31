#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const fileArg = args.find((arg) => !arg.startsWith('--'));

function optionValue(name, fallback) {
  const index = args.indexOf(name);
  if (index < 0) return fallback;
  const value = args[index + 1];
  if (!value || value.startsWith('--')) throw new Error(`${name} requires a value`);
  return value;
}

if (!fileArg) {
  console.error('Usage: audit_story_html.mjs <book.html> [--min-screens N] [--require-bilingual]');
  process.exit(2);
}

const filePath = path.resolve(fileArg);
const minScreens = Number(optionValue('--min-screens', '1'));
const requireBilingual = args.includes('--require-bilingual');

if (!Number.isInteger(minScreens) || minScreens < 1) {
  throw new Error('--min-screens must be a positive integer');
}

const html = fs.readFileSync(filePath, 'utf8');
const failures = [];
const warnings = [];
const passes = [];

function record(target, name, detail = '') {
  target.push(detail ? `${name}: ${detail}` : name);
}

function check(name, condition, detail = '') {
  record(condition ? passes : failures, name, detail);
}

function warn(name, condition, detail = '') {
  if (!condition) record(warnings, name, detail);
}

function metaValue(name) {
  const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const pattern = new RegExp(`<meta\\s+name=["']${escaped}["']\\s+content=["']([^"']*)["']`, 'i');
  return html.match(pattern)?.[1] ?? null;
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

function allMatches(pattern, text = html) {
  return [...text.matchAll(pattern)];
}

function parseV2Data() {
  const match = html.match(/<script\b[^>]*\bid=["']book-tiktok-data["'][^>]*>([\s\S]*?)<\/script>/i);
  if (!match) return null;
  try {
    return JSON.parse(match[1]);
  } catch (error) {
    record(failures, 'valid v2 data JSON', error.message);
    return null;
  }
}

function legacyActiveSegment() {
  const assignments = allMatches(/(?:^|\n)\s*slides\s*=\s*([A-Za-z_$][\w$]*)\s*;/g);
  const assignment = assignments.at(-1);
  if (assignment) {
    const variable = assignment[1];
    const escaped = variable.replace(/[$]/g, '\\$&');
    const declaration = new RegExp(`(?:var|let|const)\\s+${escaped}\\s*=`).exec(html);
    if (declaration && declaration.index < assignment.index) {
      return { variable, segment: html.slice(declaration.index, assignment.index) };
    }
  }

  const declaration = /(?:var|let|const)\s+slides\s*=/.exec(html);
  if (!declaration) return { variable: null, segment: html };
  return { variable: 'slides', segment: html.slice(declaration.index) };
}

function parseLegacyData() {
  const active = legacyActiveSegment();
  const activeCalls = allMatches(/storySlide\(\s*["']([^"']+)["']\s*,\s*([123])/g, active.segment);
  const globalCalls = allMatches(/storySlide\(\s*["']([^"']+)["']\s*,\s*([123])/g);
  const levels = activeCalls.reduce((result, match) => {
    result[match[2]] += 1;
    return result;
  }, { 1: 0, 2: 0, 3: 0 });
  const ids = activeCalls.map((match) => match[1]);
  return {
    activeVariable: active.variable,
    screens: activeCalls.map((match) => ({ id: match[1], level: Number(match[2]) })),
    levels,
    orphanCalls: Math.max(0, globalCalls.length - activeCalls.length),
    duplicateIds: [...new Set(ids.filter((id, index) => ids.indexOf(id) !== index))]
  };
}

check('doctype', /^\s*<!doctype html>/i.test(html));
check('viewport meta', /<meta\s+name=["']viewport["'][^>]*>/i.test(html));
check('inline styles', /<style[\s>]/i.test(html));
check('inline script', /<script(?:\s[^>]*)?>[\s\S]*<\/script>/i.test(html));
check('Russian document language', /<html\b[^>]*\blang=["']ru["']/i.test(html));

const forbiddenRuntime = [
  ['external script', /<script\b[^>]*\bsrc\s*=/i],
  ['external stylesheet', /<link\b[^>]*\brel=["']stylesheet["']/i],
  ['CSS import', /@import\s/i],
  ['runtime fetch', /\bfetch\s*\(/],
  ['runtime XHR', /\bXMLHttpRequest\b/],
  ['runtime WebSocket', /\bnew\s+WebSocket\b/],
  ['runtime EventSource', /\bEventSource\b/],
  ['service worker', /navigator\.serviceWorker|serviceWorker\.register/],
  ['remote CSS asset', /url\(\s*["']?https?:\/\//i],
  ['remote media source', /\bsrc\s*=\s*["']https?:\/\//i]
];

for (const [label, pattern] of forbiddenRuntime) {
  check(`no ${label}`, !pattern.test(html));
}

for (const id of ['contentsButton', 'languageButton', 'sourcesButton', 'themeButton']) {
  check(`${id} control`, new RegExp(`id=["']${id}["']`).test(html));
}

check('light Flexoki paper', /--color-bg\s*:\s*#fffcf0/i.test(html));
check('Flexoki ink', /--color-text\s*:\s*#100f0f/i.test(html));
check('quiet Flexoki action color', /--color-primary\s*:\s*(?:#1c6c66|#5b2fc2)/i.test(html));
check('dark theme', /data-theme=["']dark["']|\[data-theme=["']dark["']\]/i.test(html));
check('embedded font', (html.match(/data:font\/woff2;base64,/gi) || []).length >= 2, 'Geist and Geist Mono expected');
check('saved state', /localStorage/.test(html));
check('keyboard navigation', /addEventListener\(["']keydown["']/.test(html));
check('pointer navigation', /addEventListener\(["']pointerup["']/.test(html));
check('reduced motion', /prefers-reduced-motion/.test(html));
check('safe-area handling', /safe-area-inset-(?:top|bottom)/.test(html));
check('dynamic viewport', /100dvh/.test(html));
check('desktop reading layout', /desktop-rail/.test(html) && /@media\s*\(min-width:\s*(?:900|1024)px\)/.test(html));
check('visible focus treatment', /:focus-visible/.test(html));
check('sources disclosure', /id=["']sourcesDialog["']/.test(html));
check('chapters dialog', /id=["']contentsDialog["']/.test(html));
check('no gradients', !/\b(?:linear|radial|conic)-gradient\s*\(/i.test(html));
check('no left-accent border', !/border-left\s*:/i.test(html));

const literalIds = allMatches(/\bid=["']([^"']+)["']/g).map((match) => match[1]);
const duplicateLiteralIds = [...new Set(literalIds.filter((id, index) => literalIds.indexOf(id) !== index))];
check('no duplicate literal IDs', duplicateLiteralIds.length === 0, duplicateLiteralIds.join(', '));

const data = parseV2Data();
const format = data ? 'v2' : 'legacy';
let screenCount = 0;
let levels = { 1: 0, 2: 0, 3: 0 };
let modes = null;
let words = null;

if (data) {
  check('v2 schema version', data.schemaVersion === 2, String(data.schemaVersion));
  check('valid slug', typeof data.slug === 'string' && /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(data.slug), String(data.slug));
  check('screens array', Array.isArray(data.screens));
  check('sources array', Array.isArray(data.sources));

  const screens = Array.isArray(data.screens) ? data.screens : [];
  const sources = Array.isArray(data.sources) ? data.sources : [];
  screenCount = screens.length;
  const screenIds = screens.map((screen) => screen.id);
  const duplicateScreenIds = [...new Set(screenIds.filter((id, index) => screenIds.indexOf(id) !== index))];
  check('unique stable screen IDs', duplicateScreenIds.length === 0 && screenIds.every((id) => typeof id === 'string' && /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id)), duplicateScreenIds.join(', '));

  levels = screens.reduce((result, screen) => {
    if ([1, 2, 3].includes(screen.level)) result[screen.level] += 1;
    return result;
  }, { 1: 0, 2: 0, 3: 0 });
  modes = { essential: levels[1], core: levels[1] + levels[2], deep: screenCount };
  check('all screen levels valid', levels[1] + levels[2] + levels[3] === screenCount);
  check('user-approved target modes present', data.targetModes && ['essential', 'core', 'deep'].every((mode) => Number.isInteger(data.targetModes[mode]) && data.targetModes[mode] > 0));
  if (data.targetModes) {
    check('corpus matches user-approved target modes', data.targetModes.essential === modes.essential && data.targetModes.core === modes.core && data.targetModes.deep === modes.deep, `${data.targetModes.essential}/${data.targetModes.core}/${data.targetModes.deep} target vs ${modes.essential}/${modes.core}/${modes.deep} data`);
  }
  check('one first cover', screens.filter((screen) => screen.type === 'cover').length === 1 && screens[0]?.type === 'cover' && screens[0]?.level === 1);
  check('one last final', screens.filter((screen) => screen.final).length === 1 && screens.at(-1)?.final === true && screens.at(-1)?.level === 1);

  const sourceIds = sources.map((source) => source.id);
  const sourceSet = new Set(sourceIds);
  check('unique source IDs', sourceSet.size === sourceIds.length && sourceIds.every((id) => Number.isInteger(id) && id > 0));
  check('direct source URLs', sources.every((source) => typeof source.url === 'string' && /^https?:\/\//i.test(source.url)));
  check('source roles', sources.every((source) => ['book', 'publisher', 'author', 'primary', 'review', 'reference'].includes(source.role)));
  check('bilingual source notes', sources.every((source) => source.note?.ru?.trim() && source.note?.en?.trim()));

  const badCopy = [];
  const badClaimType = [];
  const badSourceRefs = [];
  const weakSourceCoverage = [];
  const translationSkew = [];
  words = { ru: 0, en: 0 };
  for (const screen of screens) {
    const complete = ['ru', 'en'].every((language) => {
      const copy = screen.copy?.[language];
      return copy && typeof copy.section === 'string' && copy.section.trim() && typeof copy.title === 'string' && copy.title.trim() && typeof copy.body === 'string';
    });
    if (!complete) badCopy.push(screen.id);
    if (screen.type !== 'cover' && !['book', 'corroboration', 'synthesis'].includes(screen.claimType)) badClaimType.push(screen.id);
    if (!Array.isArray(screen.sources) || screen.sources.some((sourceId) => !sourceSet.has(sourceId))) badSourceRefs.push(screen.id);
    if (['book', 'corroboration'].includes(screen.claimType) && (!screen.sources || !screen.sources.length)) weakSourceCoverage.push(screen.id);
    const ruWords = wordCount(`${screen.copy?.ru?.title || ''} ${screen.copy?.ru?.body || ''}`);
    const enWords = wordCount(`${screen.copy?.en?.title || ''} ${screen.copy?.en?.body || ''}`);
    words.ru += ruWords;
    words.en += enWords;
    if (screen.type !== 'cover' && ruWords > 0 && enWords > 0) {
      const ratio = ruWords / enWords;
      if (ratio < 0.45 || ratio > 1.8) translationSkew.push(screen.id);
    }
  }
  check('complete RU/EN screen copy', badCopy.length === 0, badCopy.join(', '));
  check('claim provenance on every screen', badClaimType.length === 0, badClaimType.join(', '));
  check('valid screen source references', badSourceRefs.length === 0, badSourceRefs.join(', '));
  warn('source coverage gaps', weakSourceCoverage.length === 0, weakSourceCoverage.join(', '));
  warn('large RU/EN density skew', translationSkew.length === 0, translationSkew.join(', '));

  const media = data.media && typeof data.media === 'object' ? data.media : {};
  const mediaIds = new Set(Object.keys(media));
  check('embedded media data', Object.values(media).every((item) => /^data:image\/[a-z0-9.+-]+;base64,/i.test(item.dataUri || '')));
  check('valid media references', screens.every((screen) => !screen.media || mediaIds.has(screen.media)));
  check('bilingual media credits', Object.values(media).every((item) => item.alt?.ru !== undefined && item.alt?.en !== undefined && item.credit?.ru !== undefined && item.credit?.en !== undefined));
} else {
  const legacy = parseLegacyData();
  screenCount = legacy.screens.length || Number(metaValue('book-tiktok:screens') || 0);
  levels = legacy.levels;
  modes = { essential: levels[1], core: levels[1] + levels[2], deep: screenCount };
  check('detectable active legacy corpus', legacy.screens.length > 0, legacy.activeVariable || 'none');
  check('unique active story IDs', legacy.duplicateIds.length === 0, legacy.duplicateIds.join(', '));
  check('no orphan story corpus', legacy.orphanCalls === 0, `${legacy.orphanCalls} unreachable storySlide calls`);
}

const screenMeta = metaValue('book-tiktok:screens');
check('screen metadata', screenMeta !== null);
if (screenMeta !== null) check('screen metadata matches data', Number(screenMeta) === screenCount, `${screenMeta} meta vs ${screenCount} data`);

check('detectable screen count', screenCount > 0);
check('minimum screen count', screenCount >= minScreens, `${screenCount} detected, ${minScreens} required`);
check('essential layer present', levels[1] > 0, String(levels[1]));
check('core layer present', levels[2] > 0, String(levels[2]));
check('deep layer present', levels[3] > 0, String(levels[3]));

const modesMeta = metaValue('book-tiktok:modes');
check('mode metadata', modesMeta !== null);
if (modesMeta && modes) {
  const parsed = modesMeta.split(',').map((value) => Number(value.trim()));
  check('mode metadata matches layers', parsed.length === 3 && parsed[0] === modes.essential && parsed[1] === modes.core && parsed[2] === modes.deep, `${modesMeta} meta vs ${modes.essential},${modes.core},${modes.deep} data`);
  check('strictly nested modes', modes.essential < modes.core && modes.core < modes.deep, `${modes.essential}/${modes.core}/${modes.deep}`);
}

const languageMeta = metaValue('book-tiktok:languages');
const bilingual = languageMeta
  ? /(?:^|,)ru(?:,|$)/.test(languageMeta) && /(?:^|,)en(?:,|$)/.test(languageMeta)
  : /language\s*===\s*["']ru["']/.test(html) && /["']en["']\s*:\s*["']ru["']|["']ru["']\s*:\s*["']en["']/.test(html);

if (requireBilingual) check('RU/EN implementation', bilingual);
else warn('language metadata', Boolean(languageMeta), 'add book-tiktok:languages metadata for deterministic audits');

warn('descriptive filename', path.basename(filePath).toLowerCase() !== 'index.html', 'prefer <book-slug>.html for a shareable standalone file');
warn('large artifact', Buffer.byteLength(html) <= 8 * 1024 * 1024, `${Buffer.byteLength(html)} bytes`);

const report = {
  file: filePath,
  format,
  bytes: Buffer.byteLength(html),
  screenCount,
  levels,
  modes,
  words,
  passes: passes.length,
  warnings,
  failures
};

console.log(JSON.stringify(report, null, 2));
process.exit(failures.length ? 1 : 0);

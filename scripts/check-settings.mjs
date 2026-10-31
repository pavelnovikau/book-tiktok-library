import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { settingsBody, settingsHead } from '../skills/book-tiktok/scripts/reader-settings.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const catalogue = JSON.parse(fs.readFileSync(path.join(root, 'books.json'), 'utf8'));
const assets = 'skills/book-tiktok/assets';
const digest = value => createHash('sha256').update(value).digest('hex');
const fontDigests = Object.fromEntries(['Geist-Variable.woff2', 'GeistSerif-Regular.woff2', 'SourceSerif4-Regular.woff2'].map(file => [file, digest(fs.readFileSync(path.join(root, assets, 'fonts', file)))]));
for (const file of ['index.html', ...catalogue.books.map(b=>b.file)]) {
  const html = fs.readFileSync(path.join(root, file), 'utf8');
  assert(html.includes('BookSettings.connect('), `${file}: missing page-state adapter`);
  assert(!html.includes("state.theme = state.theme === 'dark' ? 'light' : 'dark'"), `${file}: old direct toggle still attached`);
  assert(html.includes(settingsBody().trim()), `${file}: stale Settings modal`);
  const withoutSettingsHead = html.replace(/<!-- book-reader-settings-head:start -->[\s\S]*?<!-- book-reader-settings-head:end -->/, '');
  const hasStandaloneSans = /@font-face\s*\{\s*font-family:\s*["']Geist["']/.test(withoutSettingsHead);
  assert(html.includes(settingsHead({ includeSans: !hasStandaloneSans }).trim()), `${file}: stale preferences/fonts`);
  assert.equal((html.match(/id="bookSettingsDialog"/g) || []).length, 1, `${file}: duplicate Settings`);
  for (const [family, filename] of [['Geist','Geist-Variable.woff2'], ['Geist Serif','GeistSerif-Regular.woff2'], ['Source Serif 4','SourceSerif4-Regular.woff2']]) {
    const face = [...html.matchAll(/@font-face\s*\{([^}]*)\}/g)].find(m=>m[1].includes(`font-family: "${family}"`))?.[1];
    const data = face?.match(/base64,([^"\s)]+)/)?.[1];
    assert(data && digest(Buffer.from(data,'base64'))===fontDigests[filename], `${file}: ${family} must use the verified embedded font`);
  }
}
console.log(`Settings validation passed: homepage + ${catalogue.books.length} readers, exact maintained module and embedded font bytes.`);

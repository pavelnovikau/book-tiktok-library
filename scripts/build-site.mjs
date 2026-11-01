import fs from 'node:fs';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const output = path.join(root, 'public');
const catalogue = JSON.parse(fs.readFileSync(path.join(root, 'books.json'), 'utf8'));
const readers = catalogue.books.map(book => book.file);
if (readers.some(file => typeof file !== 'string' || path.basename(file) !== file || !file.endsWith('.html'))) {
  throw new Error('Only registered root-level HTML readers may be published');
}
// Vercel excludes the authoring skill tree. Keep the publication gate self-contained.
for (const file of readers) {
  const html = fs.readFileSync(path.join(root, file), 'utf8');
  const raw = html.match(/<script id="book-tiktok-data"[^>]*>([\s\S]*?)<\/script>/)?.[1];
  assert(raw, `${file}: missing reader data`);
  const data = JSON.parse(raw);
  assert.equal(data.defaultMode, 'deep', `${file}: fresh default must be Deep`);
  assert(!data.screens.some(s => s.kind === 'notice' || ['deep-warning', 'deep-notice'].includes(s.id)), `${file}: service-only reading page`);
  assert(html.includes('// reader-usability-v1'), `${file}: missing maintained navigation integration`);
  assert(html.includes("mode: modeOrder.includes(stored('mode', 'deep')) ? stored('mode', 'deep') : 'deep',"), `${file}: runtime fallback must be Deep`);
}
const files = ['index.html', 'books.json', 'manifest.webmanifest', 'sw.js', ...readers];
fs.rmSync(output, { recursive: true, force: true });
fs.mkdirSync(output);
for (const file of files) fs.copyFileSync(path.join(root, file), path.join(output, file));
for (const directory of ['fonts', 'icons']) {
  fs.cpSync(path.join(root, directory), path.join(output, directory), { recursive: true });
}
console.log(`Public build: ${readers.length} registered readers plus catalogue, PWA shell, fonts and icons. Collector/source/audit folders excluded.`);

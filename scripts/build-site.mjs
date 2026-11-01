import fs from 'node:fs';
import {assertReaderUsability} from '../skills/book-tiktok/scripts/reader-usability.mjs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const output = path.join(root, 'public');
const catalogue = JSON.parse(fs.readFileSync(path.join(root, 'books.json'), 'utf8'));
const readers = catalogue.books.map(book => book.file);
if (readers.some(file => typeof file !== 'string' || path.basename(file) !== file || !file.endsWith('.html'))) {
  throw new Error('Only registered root-level HTML readers may be published');
}
for (const file of readers) assertReaderUsability(fs.readFileSync(path.join(root, file), 'utf8'));
const files = ['index.html', 'books.json', 'manifest.webmanifest', 'sw.js', ...readers];
fs.rmSync(output, { recursive: true, force: true });
fs.mkdirSync(output);
for (const file of files) fs.copyFileSync(path.join(root, file), path.join(output, file));
for (const directory of ['fonts', 'icons']) {
  fs.cpSync(path.join(root, directory), path.join(output, directory), { recursive: true });
}
console.log(`Public build: ${readers.length} registered readers plus catalogue, PWA shell, fonts and icons. Collector/source/audit folders excluded.`);

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';

// Compare served bytes with a specific Git release, never infer deployment from merge.
const option = name => process.argv.find(arg => arg.startsWith(`--${name}=`))?.slice(name.length + 3);
const ref = option('ref') || 'HEAD';
const output = option('out');
if (!output) throw new Error('--out=<proof.json> is required');
const origin = option('origin') || 'https://book-tiktok-library.vercel.app';
const read = file => execFileSync('git', ['show', `${ref}:${file}`], { maxBuffer: 10 * 1024 * 1024 });
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const catalogue = JSON.parse(read('books.json'));
const assetPaths = execFileSync('git', ['ls-tree', '-r', '--name-only', ref, '--', 'fonts', 'icons'], { encoding: 'utf8' }).trim().split('\n').filter(Boolean);
const files = ['index.html', 'books.json', 'manifest.webmanifest', 'sw.js', ...catalogue.books.map(book => book.file), ...assetPaths];
const startedAt = new Date().toISOString();
const expectedCommit = execFileSync('git', ['rev-parse', ref], { encoding: 'utf8' }).trim();
const responses = [];
let cursor = 0;
async function observe(file, excluded = false) {
  const route = file === 'index.html' ? '/' : file.endsWith('.html') ? `/${file.slice(0, -5)}` : `/${file}`;
  const url = new URL(route, origin);
  url.searchParams.set('release-proof', expectedCommit);
  try {
    const response = await fetch(url, { cache: 'no-store', signal: AbortSignal.timeout(20000) });
    const bytes = Buffer.from(await response.arrayBuffer());
    const result = { file, route, url: response.url, status: response.status, checkedAt: new Date().toISOString(), sha256: hash(bytes) };
    if (excluded) Object.assign(result, { excluded: true, pass: response.status === 404 });
    else Object.assign(result, { expectedSha256: hash(read(file)), pass: response.status === 200 && hash(bytes) === hash(read(file)) });
    if (file === 'books.json' && response.ok) {
      const live = JSON.parse(bytes);
      Object.assign(result, { catalogueBooks: live.books.length, catalogueScreens: live.books.reduce((n, book) => n + book.screenCount, 0) });
    }
    if (file.endsWith('.html') && file !== 'index.html' && response.ok) {
      const match = bytes.toString().match(/<script id="book-tiktok-data" type="application\/json">\s*([\s\S]*?)<\/script>/);
      if (match) {
        const data = JSON.parse(match[1]);
        Object.assign(result, { effectivePairs: data.screens.length, contentMode: data.contentMode || 'legacy', targetModes: data.targetModes, effectiveCorpusSha256: hash(JSON.stringify(data)) });
      }
    }
    return result;
  } catch (error) { return { file, route, pass: false, error: error.message }; }
}
await Promise.all(Array.from({ length: 4 }, async () => {
  while (cursor < files.length) { const index = cursor++; responses[index] = await observe(files[index]); }
}));
const excluded = [];
for (const file of ['collector-output/amphibian-man/story-data.json', 'editorial-audit/2026-10-31/publisher-findings/release-02.json', 'skills/book-tiktok/SKILL.md', 'private/index.html', 'research/index.html', '.env.local']) excluded.push(await observe(file, true));
const proof = { startedAt, completedAt: new Date().toISOString(), kind: 'actual-production-byte-and-effective-corpus-verification', origin, expectedCommit, publicAllowlistFiles: files.length, catalogueBooks: catalogue.books.length, catalogueScreens: catalogue.books.reduce((n, book) => n + book.screenCount, 0), pass: [...responses, ...excluded].every(result => result.pass), responses, excluded };
fs.mkdirSync(path.dirname(output), { recursive: true });
fs.writeFileSync(output, JSON.stringify(proof, null, 2) + '\n');
console.log(JSON.stringify({ output, pass: proof.pass, assets: files.length, books: proof.catalogueBooks, screens: proof.catalogueScreens, failures: [...responses, ...excluded].filter(result => !result.pass) }, null, 2));
if (!proof.pass) process.exitCode = 1;

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const directory = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(directory, '../..');
const output = path.join(directory, 'nonviolent-communication.html');

// Use the maintained builder; this book-local presentation keeps explanatory
// source maps intact while moving provenance chrome into the Sources dialog.
execFileSync(process.execPath, [
  path.join(root, 'skills/book-tiktok/scripts/build_story.mjs'),
  path.join(directory, 'story-data.json'), '--out', output
], { stdio: 'inherit' });

let html = fs.readFileSync(output, 'utf8');
const marker = '<style id="nonviolent-communication-source-presentation">';
if (html.includes(marker)) throw new Error('Duplicate local presentation');
html = html.replace('</head>', `${marker}
  :root { --nvc-cover-measure: 42rem; }
  html[data-content-mode="explanatory"] .source-label { display: none; }
  html .cover-visual { display: none; }
  html .cover-layout { display: flex; max-width: var(--nvc-cover-measure); margin-inline: auto; }
  html .cover-actions { align-self: stretch; }
</style>\n</head>`);
fs.writeFileSync(output, html);

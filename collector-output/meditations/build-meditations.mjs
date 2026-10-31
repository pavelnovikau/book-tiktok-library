import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

// The maintained builder owns the reader. These two book-local rules keep
// source research inside its dialog and make the documentary title leaf fit.
const dir = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(dir, '../..');
const output = path.join(dir, 'meditations.html');
execFileSync(process.execPath, [path.join(root, 'skills/book-tiktok/scripts/build_story.mjs'), path.join(dir, 'story-data.json'), '--out', output], { stdio: 'inherit' });
const style = `<style id="meditations-presentation">
.source-label { display: none; }
.cover-visual.has-image img { object-fit: contain; }
@media (max-width: 899px) {
  .cover-layout { gap: var(--space-3); }
  .cover-visual.has-image { min-height: 0; padding: var(--space-3); grid-template-rows: auto; }
  .cover-visual.has-image img { max-height: var(--meditations-title-leaf-height, 120px); }
  .cover-visual figcaption { display: none; }
}
</style>`;
fs.writeFileSync(output, fs.readFileSync(output, 'utf8')
  .replace('</head>', `${style}\n</head>`)
  .replace("start: 'Начать просмотр'", "start: 'Начать чтение'"));

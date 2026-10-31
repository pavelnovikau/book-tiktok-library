// Build only this collector with the maintained builder, then apply narrow
// book-local spoiler and cover corrections. No shared template/shell mutations.
import fs from 'node:fs';import crypto from 'node:crypto';import path from 'node:path';import {fileURLToPath} from 'node:url';import {spawnSync} from 'node:child_process';
const here=path.dirname(fileURLToPath(import.meta.url)), dir=path.dirname(here), root=path.resolve(dir,'../..');
const output=path.join(dir,'flowers-for-algernon.html');
const built=spawnSync(process.execPath,[path.join(root,'skills/book-tiktok/scripts/build_story.mjs'),path.join(dir,'story-data.json'),'--out',output],{encoding:'utf8'});
process.stdout.write(built.stdout);process.stderr.write(built.stderr);if(built.status!==0)process.exit(built.status||1);
let html=fs.readFileSync(output,'utf8');
const replace=(from,to)=>{if(!html.includes(from))throw Error('Maintained shell changed; patch anchor missing: '+from.slice(0,85));html=html.replace(from,to)};
replace('      function text() { return ui[state.language]; }',`      // Fresh consent is document-local. Stored depth is a preference, not consent.
      let endingConsent = false;
      if (state.mode === 'deep') state.mode = 'essential';
      const spoilerDialog = document.createElement('dialog');
      spoilerDialog.id = 'spoilerDialog';
      spoilerDialog.setAttribute('aria-labelledby', 'spoilerTitle');
      document.body.appendChild(spoilerDialog);
      let pendingEnding = null;
      function guardEnding(action) {
        if (endingConsent) { action(); return; }
        if (els.contentsDialog.open) els.contentsDialog.close();
        const ru = state.language === 'ru';
        spoilerDialog.innerHTML = '<div class="dialog-shell"><div class="dialog-body"><h2 id="spoilerTitle">' + (ru ? 'Deep раскрывает развязку' : 'Deep reveals the ending') + '</h2><p>' + (ru ? 'Дальше — решающие открытия и исходы истории Чарли и Элджернона, включая последние записи. Читать со спойлерами?' : 'The decisive discoveries and outcomes of Charlie and Algernon’s story follow, including the final entries. Read with spoilers?') + '</p><div class="flowers-spoiler-actions"><button class="button button-primary" type="button" data-ending-accept>' + (ru ? 'Читать Deep со спойлерами' : 'Read Deep with spoilers') + '</button><button class="button" type="button" data-ending-cancel>' + (ru ? 'Остаться здесь' : 'Stay here') + '</button></div></div></div>';
        pendingEnding = action;
        spoilerDialog.querySelector('[data-ending-accept]').onclick = () => { const action = pendingEnding; pendingEnding = null; endingConsent = true; spoilerDialog.close(); if (action) action(); };
        spoilerDialog.querySelector('[data-ending-cancel]').onclick = () => { pendingEnding = null; spoilerDialog.close(); };
        spoilerDialog.showModal();
      }
      spoilerDialog.addEventListener('cancel', () => { pendingEnding = null; });
      function text() { return ui[state.language]; }`);
replace('      function goToPosition(position, direction) {\n        const list = visibleScreens();',`      function goToPosition(position, direction) {
        const list = visibleScreens();
        const target = list[Math.max(0, Math.min(position, list.length - 1))];
        if (target.level === 3 && !endingConsent) { guardEnding(() => goToPosition(position, direction)); return; }`);
replace('      function goToId(id) {\n        let list = visibleScreens();',`      function goToId(id) {
        const target = data.screens.find(screen => screen.id === id);
        if (target?.level === 3 && !endingConsent) { guardEnding(() => goToId(id)); return; }
        let list = visibleScreens();`);
replace("        if (!modeOrder.includes(mode)) return;\n        const currentId", "        if (!modeOrder.includes(mode)) return;\n        if (mode === 'deep' && !endingConsent) { guardEnding(() => setMode(mode)); return; }\n        const currentId");
replace('escapeHtml(copyOf(screen).title)}</span></button>`).join(\'\');', 'escapeHtml(screen.level === 3 && !endingConsent ? (state.language === \'ru\' ? \'Скрыто до предупреждения\' : \'Hidden until spoiler consent\') : copyOf(screen).title)}</span></button>`).join(\'\');');
// Replace the template’s explanatory placeholder with a book-specific colophon.
const start='        const visual = coverMediaFor(screen) || `';
const a=html.indexOf(start),b=html.indexOf('\n        return `<article',a);
if(a<0||b<0)throw Error('cover anchor changed');
html=html.slice(0,a)+`        const visual = coverMediaFor(screen) || '<div class="cover-visual flowers-cover" aria-hidden="true"><div class="flowers-colophon"><span>' + (state.language === 'ru' ? 'ДЭНИЕЛ КИЗ' : 'DANIEL KEYES') + '</span><strong>1966</strong><span>' + (state.language === 'ru' ? 'ЧАРЛИ ГОРДОН<br>ЭЛДЖЕРНОН' : 'CHARLIE GORDON<br>ALGERNON') + '</span></div></div>';`+html.slice(b);
replace("start: 'Начать просмотр'", "start: 'Начать чтение'");
replace("coverTop: 'СИСТЕМА / ИДЕЯ / СЛЕДСТВИЕ', coverBottom: 'ОДНА МОДЕЛЬ, КОТОРУЮ СТОИТ УНЕСТИ'", "coverTop: 'ДЭНИЕЛ КИЗ', coverBottom: 'РОМАН 1966 ГОДА'");
replace("coverTop: 'SYSTEM / IDEA / CONSEQUENCE', coverBottom: 'ONE MODEL TO CARRY FORWARD'", "coverTop: 'DANIEL KEYES', coverBottom: 'THE 1966 NOVEL'");
replace('</head>',`<style id="flowers-local-style">
.flowers-spoiler-actions { display:flex; flex-wrap:wrap; gap:var(--space-3); margin-top:var(--space-5); }
.flowers-colophon { display:grid; gap:var(--space-6); font-family:var(--font-mono); }
.flowers-colophon strong { font-family:var(--font-reading); font-size:var(--text-4xl); line-height:var(--line-height-tight, 1.1); }
.flowers-colophon span { font-size:var(--text-sm); color:var(--color-text-muted); }
@media (prefers-reduced-motion: reduce) { .story-slide { animation:none !important; } }
</style></head>`);
fs.writeFileSync(output,html);
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
fs.writeFileSync(path.join(here,'build-result.json'),JSON.stringify({maintainedBuild:JSON.parse(built.stdout),finalBytes:Buffer.byteLength(html),htmlSHA256:sha(output),dataSHA256:sha(path.join(dir,'story-data.json')),builderSHA256:sha(path.join(root,'skills/book-tiktok/scripts/build_story.mjs')),templateSHA256:sha(path.join(root,'skills/book-tiktok/assets/standalone-template.html'))},null,2)+'\n');
console.log('Book-local cover and Deep-consent corrections applied.');

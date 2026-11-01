import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
const here=path.dirname(fileURLToPath(import.meta.url));
const installed='/Users/pn/.codex/skills/book-tiktok';
const out=path.join(here,'white-fang.html');
const built=spawnSync(process.execPath,[path.join(installed,'scripts/build_story.mjs'),path.join(here,'story-data.json'),'--out',out],{encoding:'utf8'});
if(built.status!==0)throw Error(built.stderr||built.stdout);
let html=fs.readFileSync(out,'utf8');
const replacements=[];
function replace(before,after,label){
 if(!html.includes(before)||html.indexOf(before)!==html.lastIndexOf(before))throw Error('Expected one anchor: '+label);
 html=html.replace(before,after);replacements.push(label);
}
replace('const storagePrefix = `book-tiktok.${data.slug}.`;','const storagePrefix = `book-tiktok.${data.slug}.depth-v2.`;','isolated candidate progress namespace');
replace("      function text() { return ui[state.language]; }",`      // Candidate-local ending protection. Never persists consent.
      let deepConsent = false;
      let pendingDeep = null;
      let consentFocus = null;
      if (state.mode === 'deep') state.mode = 'essential';
      const consent = document.getElementById('deepConsentDialog');
      const confirmDeep = document.getElementById('confirmDeep');
      const cancelDeep = document.getElementById('cancelDeep');
      function requestDeep(action) {
        if (deepConsent) { action(); return; }
        pendingDeep = action;
        consentFocus = document.activeElement;
        if (els.contentsDialog.open) els.contentsDialog.close();
        if (els.sourcesDialog.open) els.sourcesDialog.close();
        const ru = state.language === 'ru';
        document.getElementById('deepConsentTitle').textContent = ru ? 'Открыть полную историю?' : 'Open the complete story?';
        document.getElementById('deepConsentText').textContent = ru
          ? 'Режим «Глубоко» раскрывает поздние события, судьбы героев и последнюю сцену. Режимы «Главное» и «Подробнее» не раскрывают финал. После перехода в короткий режим или ухода со страницы потребуется новое согласие.'
          : 'Deep reveals later events, the characters’ outcomes and the last scene. Essential and Core leave the ending unrevealed. Switching to a shorter mode or leaving this page requires fresh consent.';
        confirmDeep.textContent = ru ? 'Читать «Глубоко» со спойлерами' : 'Read Deep with spoilers';
        cancelDeep.textContent = ru ? 'Сохранить развязку' : 'Preserve the ending';
        if (!consent.open) consent.showModal();
        cancelDeep.focus({preventScroll:true});
      }
      confirmDeep.addEventListener('click', () => {
        const action = pendingDeep;
        pendingDeep = null;
        deepConsent = true;
        consent.close();
        if (action) action();
      });
      cancelDeep.addEventListener('click', () => consent.close());
      consent.addEventListener('close', () => {
        pendingDeep = null;
        if (consentFocus?.isConnected) consentFocus.focus({preventScroll:true});
      });
      // A restored page must ask again; no consent is read from any storage.
      addEventListener('pagehide', () => { deepConsent = false; });
      addEventListener('pageshow', event => {
        if (event.persisted) {
          deepConsent = false;
          state.mode = state.mode === 'deep' ? 'essential' : state.mode;
          state.position = 0;
          render();
        }
      });
      function text() { return ui[state.language]; }`,'volatile native Deep consent');
replace('      function goToId(id) {\n        let list = visibleScreens();',`      function goToId(id) {
        const target = data.screens.find(screen => screen.id === id);
        if (target?.level === 3 && !deepConsent) {
          requestDeep(() => goToId(id));
          return;
        }
        let list = visibleScreens();`,'guard saved or explicit hidden target');
replace("      function setMode(mode) {\n        if (!modeOrder.includes(mode)) return;",`      function setMode(mode) {
        if (!modeOrder.includes(mode)) return;
        if (mode === 'deep' && !deepConsent) {
          requestDeep(() => setMode(mode));
          return;
        }
        if (mode !== 'deep') deepConsent = false;`,'guard every depth picker and revoke after downgrade');
replace(`        const rememberedId = continueSaved ? stored('lastScreen', '') : '';
        if (rememberedId) goToId(rememberedId);
        else goToPosition(Math.min(1, visibleScreens().length - 1), 'forward');`,
`        const rememberedId = continueSaved ? stored('lastScreen', '') : '';
        if (rememberedId && data.screens.some(screen => screen.id === rememberedId)) goToId(rememberedId);
        else {
          if (rememberedId) removeStored('lastScreen');
          goToPosition(Math.min(1, visibleScreens().length - 1), 'forward');
        }`,'safe invalid saved ID fallback');
replace('        document.querySelectorAll(\'[data-open-sources]\').forEach((button) => {',`        document.querySelectorAll('[data-open-deep]').forEach((button) => {
          button.addEventListener('click', () => requestDeep(() => {
            setMode('deep');
            goToId('deep-warning');
          }));
        });
        document.querySelectorAll('[data-open-sources]').forEach((button) => {`,'explicit local entry from shared final');
replace("${copy.body || ''}${sourceLabel(screen)}</div></article>`;", "${copy.body || ''}${screen.final && state.mode !== 'deep' ? `<p><button class=\"button button-primary\" type=\"button\" data-open-deep>${state.language === 'ru' ? 'Открыть «Глубоко» — спойлеры' : 'Open Deep — spoilers'}</button></p>` : ''}${sourceLabel(screen)}</div></article>`;",'final entry control without chronology reset');
const visualLine=html.split('\n').find(line=>line.includes('const visual = coverMediaFor(screen)'));
replace(visualLine,`        const visual = coverMediaFor(screen) || '<div class="cover-visual"><div class="cover-mark"><span class="cover-eyebrow">' + escapeHtml(data.author[state.language]) + '</span><p class="lede">' + escapeHtml(copy.title) + '</p><span class="cover-eyebrow">' + (state.language === 'ru' ? 'Роман · 1906' : 'A novel · 1906') + '</span></div></div>';`,'quiet typographic cover');
const sourceLine=html.split('\n').find(line=>line.includes('els.sourcesList.innerHTML = data.sources.map'));
replace(sourceLine,sourceLine+`
        const ru = state.language === 'ru';
        const map = visibleScreens().filter(screen => screen.evidenceLocator).map(screen =>
          '<li><strong>' + escapeHtml(copyOf(screen).title) + '</strong><br><span>' + escapeHtml(screen.evidenceLocator) + '</span></li>').join('');
        els.sourcesList.insertAdjacentHTML('beforeend', '<li><details><summary>' +
          (ru ? 'Карта сцен выбранной глубины' : 'Scene map for the selected depth') +
          '</summary><p>' + (ru ? 'PG910: строки проверенного электронного файла; это не печатные страницы. Показана карта текущей глубины, полная — только после согласия на «Глубоко».' : 'PG910: lines in the verified electronic witness, not print pages. This map follows the current depth; the complete map requires Deep consent.') + '</p><ol>' + map + '</ol></details></li>');`,'global depth-filtered source map');
replace('  <script id="book-tiktok-data" type="application/json">',`  <!-- candidate-local-deep-guard:v1 -->
  <dialog id="deepConsentDialog" aria-labelledby="deepConsentTitle" aria-describedby="deepConsentText">
    <div class="dialog-shell">
      <header class="dialog-header"><h2 id="deepConsentTitle"></h2></header>
      <div class="dialog-body"><p id="deepConsentText"></p></div>
      <footer class="dialog-footer"><button class="button" id="cancelDeep" type="button"></button><button class="button button-primary" id="confirmDeep" type="button"></button></footer>
    </div>
  </dialog>
  <script id="book-tiktok-data" type="application/json">`,'native consent markup');
replace('      function goToPosition(position, direction) {\n        const list = visibleScreens();', `      function goToPosition(position, direction) {
        if (state.mode === 'deep' && !deepConsent) {
          requestDeep(() => goToPosition(position, direction));
          return;
        }
        const list = visibleScreens();`, 'guard direct position route');
replace('      function renderSources() {', `      // Keep the active chapter visible when a phone layout becomes a desktop rail.
      addEventListener('resize', () => requestAnimationFrame(() => requestAnimationFrame(() => {
        const active = els.desktopContentsList.querySelector('.is-active');
        if (active && els.desktopContentsList.getBoundingClientRect().height > 0)
          active.scrollIntoView({block: 'center'});
      })));
      function renderSources() {`, 'resynchronize the rail after viewport resize');
replace('Продолжить Deep — спойлеры финала','Продолжить «Глубоко» — спойлеры финала','localized resume depth');
// Book-local Russian time inflection; the installed builder remains read-only.
const dataPattern=/(<script id="book-tiktok-data" type="application\/json">)([\s\S]*?)(<\/script>)/;
const dataMatch=html.match(dataPattern);
if(!dataMatch)throw Error('Missing embedded data');
const embedded=JSON.parse(dataMatch[2]);
for(const mode of Object.values(embedded.modes)){
 const minutes=Number.parseInt(mode.minutes.ru,10);
 if(!Number.isInteger(minutes))throw Error('Invalid Russian reading minutes');
 const ending=minutes%100>=11&&minutes%100<=14?'минут':minutes%10===1?'минута':minutes%10>=2&&minutes%10<=4?'минуты':'минут';
 mode.minutes.ru=`${minutes} ${ending}`;
}
html=html.replace(dataPattern,(_,a,b,c)=>a+JSON.stringify(embedded,null,2).replaceAll('<','\\u003c')+c);
replacements.push('Russian reading-time inflection');
fs.writeFileSync(out,html);
const tracked=['SKILL.md','scripts/build_story.mjs','scripts/reader-settings.mjs','assets/standalone-template.html','assets/reader-settings-head.html','assets/reader-settings.html','assets/reader-header.html'];
const report={builder:installed,readOnly:true,replacements,installedHashes:Object.fromEntries(tracked.map(file=>[file,createHash('sha256').update(fs.readFileSync(path.join(installed,file))).digest('hex')])),outputBytes:Buffer.byteLength(html)};
fs.writeFileSync(path.join(here,'build-record.json'),JSON.stringify(report,null,2)+'\n');
console.log(built.stdout.trim());console.log(JSON.stringify({localPatches:replacements.length,bytes:report.outputBytes}));
